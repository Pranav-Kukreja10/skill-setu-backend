import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from students.ollama_client import OllamaClient

# Force Python to read the .env file directly from the disk on every call
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

class AIGateway:
    """
    Unified, model-agnostic AI Gateway. Routes specific screening tasks 
    to dedicated Gemini models to optimize response times and free-tier RPD quotas.
    """
    
    # Model Tier Definitions based on your AI Studio Limits
    MODEL_RESUME_PARSER = "gemini-3.1-flash-lite"
    MODEL_TEST_GENERATOR = "gemini-3.5-flash-lite"
    
    @staticmethod
    def extract_skills_and_projects(raw_text: str) -> dict:
        """
        Task 1: Resume Extraction. Routed strictly to gemini-3.1-flash-lite.
        Extracts skills with project evidence and experience recency ratings.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            model = os.getenv("MODEL_RESUME_PARSER", AIGateway.MODEL_RESUME_PARSER)
            
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "skills": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "name": {"type": "STRING"},
                                "project_evidence_score": {
                                    "type": "INTEGER", 
                                    "description": "0-100 score of how deeply applied and complex this skill is inside their listed projects"
                                },
                                "experience_recency_score": {
                                    "type": "INTEGER", 
                                    "description": "0-100 score of how recent and tenure-backed this skill is inside their professional experience"
                                }
                            },
                            "required": ["name", "project_evidence_score", "experience_recency_score"]
                        }
                    },
                    "projects": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {"type": "STRING"},
                                "technologies": {
                                    "type": "ARRAY",
                                    "items": {"type": "STRING"}
                                },
                                "description": {"type": "STRING"}
                            },
                            "required": ["title", "technologies", "description"]
                        }
                    },
                    "target_roles": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                        "description": "Job titles or target roles candidate is seeking, inferred from resume headline, summary, and experience"
                    },
                    "current_designation": {
                        "type": "STRING",
                        "description": "Candidate's current or most recent job title or professional identity"
                    },
                    "experience_years": {
                        "type": "NUMBER",
                        "description": "Estimated total years of work/professional experience (0 for freshers/students)"
                    },
                    "academic_credentials": {
                        "type": "OBJECT",
                        "properties": {
                            "institution": {"type": "STRING"},
                            "degree": {"type": "STRING"},
                            "department": {"type": "STRING"},
                            "cgpa": {"type": "NUMBER"},
                            "graduation_year": {"type": "INTEGER"}
                        }
                    },
                    "skills_categorized": {
                        "type": "OBJECT",
                        "properties": {
                            "technical_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "frameworks": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "tools": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "soft_skills": {"type": "ARRAY", "items": {"type": "STRING"}}
                        }
                    },
                    "social_links": {
                        "type": "OBJECT",
                        "properties": {
                            "github": {"type": "STRING"},
                            "linkedin": {"type": "STRING"},
                            "portfolio": {"type": "STRING"}
                        }
                    },
                    "certifications": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "name": {"type": "STRING"},
                                "issuer": {"type": "STRING"},
                                "issue_year": {"type": "INTEGER"},
                                "credential_url": {"type": "STRING"},
                                "skills_covered": {"type": "ARRAY", "items": {"type": "STRING"}}
                            },
                            "required": ["name"]
                        }
                    }
                },
                "required": ["skills", "projects", "target_roles"]
            }

            prompt = (
                f"You are an expert multi-domain resume parser. Analyze the following candidate resume text across ANY professional domain "
                f"(Business Administration, Management, Finance, Commerce, Engineering, Technology, Design, Accounting, Marketing, Human Resources, Supply Chain, etc.).\n"
                f"Extract:\n"
                f"1. 'skills': List of all domain-specific skills, functional competencies, and software/tools. Assign:\n"
                f"   - 'project_evidence_score' (0-100): How deeply applied/demonstrated is this skill in projects, case studies, audits, or portfolio deliverables?\n"
                f"   - 'experience_recency_score' (0-100): How recent and tenure-backed is this skill across work or internship experience?\n"
                f"2. 'projects': Academic, personal, or professional initiatives (title, technologies/tools/methods used, description of outcomes/impact).\n"
                f"3. 'target_roles': 1-4 specific job titles candidate is qualified for or seeking (e.g. 'Financial Analyst', 'UI/UX Designer', 'Accountant', 'Marketing Associate', 'Software Engineer').\n"
                f"4. 'academic_credentials': institution, degree (e.g. BBA, MBA, B.Com, B.Tech, M.Com, BE, B.Des), department, cgpa, graduation_year.\n"
                f"5. 'current_designation': Most recent job title or professional title (leave empty if student/fresher).\n"
                f"6. 'experience_years': Total years of professional work experience (0.0 if student or fresher).\n"
                f"7. 'skills_categorized': Group extracted competencies dynamically into:\n"
                f"   - 'technical_skills': Core functional/domain skills (e.g., Financial Modeling, Auditing, User Research, Python, Tax Filing, Brand Strategy, CAD).\n"
                f"   - 'frameworks': Methodologies, standard practices, regulatory standards, or architectures (e.g., GAAP, IFRS, Agile, Scrum, Design Thinking, Six Sigma, SWOT, React, Django).\n"
                f"   - 'tools': Software, platforms, utilities, and applications (e.g., Excel, Tally, SAP, Figma, Tableau, Salesforce, Docker, Bloomberg, QuickBooks, Jira).\n"
                f"   - 'soft_skills': Leadership, stakeholder communication, negotiation, problem-solving, collaboration.\n"
                f"8. 'social_links': github, linkedin, portfolio URLs if present.\n"
                f"9. 'certifications': Professional certifications, accreditations, or licenses (e.g. AWS Certified, CFA, NPTEL, Coursera Meta, Figma Certified, CPA) with name, issuer, issue_year, and covered skills.\n\n"
                f"Return ONLY a JSON object matching the schema.\n\n"
                f"Resume Text:\n{raw_text[:6000]}"
            )

            res = AIGateway._execute_gemini_request(model, prompt, response_schema)
            if isinstance(res, dict):
                res.setdefault("current_designation", "")
                res.setdefault("experience_years", 0.0)
                res.setdefault("academic_credentials", {})
                res.setdefault("skills_categorized", {"technical_skills": [], "frameworks": [], "tools": [], "soft_skills": []})
                res.setdefault("social_links", {})
                res.setdefault("certifications", [])
            return res
            
        elif provider == "local":
            res = OllamaClient.analyze_resume_text(raw_text)
            if isinstance(res, dict):
                res.setdefault("current_designation", "")
                res.setdefault("experience_years", 0.0)
                res.setdefault("academic_credentials", {})
                res.setdefault("skills_categorized", {"technical_skills": [], "frameworks": [], "tools": [], "soft_skills": []})
                res.setdefault("social_links", {})
            return res
        else:
            return {
                "skills": [],
                "projects": [],
                "target_roles": [],
                "current_designation": "",
                "experience_years": 0.0,
                "academic_credentials": {},
                "skills_categorized": {"technical_skills": [], "frameworks": [], "tools": [], "soft_skills": []},
                "social_links": {}
            }

    @staticmethod
    def generate_adaptive_test(role_title: str, skills: list, projects: list) -> dict:
        """
        Task 2: Progressive Test Generation. Routed strictly to gemini-3.5-flash-lite.
        Universally assesses candidates across any professional domain.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            model = os.getenv("MODEL_TEST_GENERATOR", AIGateway.MODEL_TEST_GENERATOR)
            
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "questions": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "id": {"type": "INTEGER"},
                                "question_text": {"type": "STRING"},
                                "type": {"type": "STRING", "enum": ["MCQ", "VIVA"]},
                                "difficulty": {"type": "STRING", "enum": ["EASY", "MEDIUM", "HARD"]},
                                "options": {
                                    "type": "ARRAY",
                                    "items": {"type": "STRING"}
                                },
                                "correct_answer": {"type": "STRING"},  # "A", "B", "C", "D" or null
                                "explanation": {"type": "STRING"}      # Rubric standard for grading
                            },
                            "required": ["id", "question_text", "type", "difficulty", "explanation"]
                        }
                    }
                },
                "required": ["questions"]
            }

            prompt = (
                f"You are an expert domain interviewer across any professional industry. Generate a personalized 5-question test for a candidate "
                f"applying for the role of '{role_title}'.\n"
                f"Candidate Extracted Skills: {skills}\n"
                f"Candidate Projects/Experience Deliverables: {projects}\n\n"
                f"Enforce these progressive difficulty criteria adapted to the specific domain of '{role_title}':\n"
                f"1. Question 1 (MCQ - EASY): Core terminology, fundamental principle, or tool literacy check.\n"
                f"2. Question 2 (MCQ - EASY): Basic methodology, framework, regulatory standard, or design principle application.\n"
                f"3. Question 3 (MCQ - MEDIUM): Directly target a strategic, technical, or procedural decision from their listed projects or case studies.\n"
                f"4. Question 4 (VIVA - MEDIUM): Open-ended question asking the candidate to explain their methodology, architectural patterns, or workflow strategy.\n"
                f"5. Question 5 (VIVA - HARD): High-stakes scenario, edge case, audit challenge, trade-off analysis, or crisis response matching their field.\n\n"
                f"For VIVA questions, set 'options' to null and 'correct_answer' to null, and write a detailed "
                f"grading rubric explanation of what a high-quality answer must mention."
            )

            test_data = AIGateway._execute_gemini_request(model, prompt, response_schema)
            
            # Obfuscate correct answers and grading rubrics into a base64 session token
            import base64
            session_data = json.dumps({"questions": test_data["questions"]})
            session_token = base64.b64encode(session_data.encode()).decode()
            
            return {
                "role_title": role_title,
                "questions": test_data["questions"],
                "test_session_token": session_token
            }
        else:
            return {"questions": []}

    @staticmethod
    def _execute_gemini_request(model_name: str, prompt_text: str, schema: dict) -> dict:
        """Sends a robust, schema-enforced POST request to the Google Gemini API with a 120s timeout."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": schema,
                "temperature": 0.1
            }
        }

        try:
            # Set timeout to 120 seconds to completely eliminate free-tier ReadTimeout crashes
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result_json = response.json()
            text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
        except Exception as e:
            raise ConnectionError(f"Gemini API request failed on model {model_name}: {str(e)}")
