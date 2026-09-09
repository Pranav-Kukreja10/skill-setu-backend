import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from students.ollama_client import OllamaClient
import base64

# Force Python to read the .env file directly from the disk on every load
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

class AIGateway:
    """
    Unified, model-agnostic gateway with Tiered Load Balancing.
    Routes tasks to specific Gemini models based on complexity to maximize 
    free-tier Request Per Day (RPD) limits.
    """
    
    # Model Tier Definitions based on your AI Studio Limits
    TIER_HIGH = "gemini-3.5-flash-lite"     # 500 RPD - Best Reasoning
    TIER_MEDIUM = "gemini-3.1-flash-lite"   # 500 RPD - Standard Extraction
    TIER_FALLBACK = "gemini-2.5-flash-lite" # 20 RPD - Emergency Fallback
    
    @staticmethod
    def extract_skills_and_projects(raw_text: str) -> dict:
        """
        Extraction is a Medium-Complexity task. We route this to TIER_MEDIUM 
        to save our TIER_HIGH limits for the complex test generation.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            # Pass the designated model tier to the cloud router
            return AIGateway._extract_via_gemini(raw_text, target_model=AIGateway.TIER_MEDIUM)
        elif provider == "local":
            return OllamaClient.analyze_resume_text(raw_text)
        else:
            return {
                "skills": ["Python", "Django", "PostgreSQL", "Git"],
                "projects": [
                    {
                        "title": "Mock Project",
                        "technologies": ["Django", "PostgreSQL"],
                        "description": "Mocked fallback resume parsing outcome."
                    }
                ]
            }

    @staticmethod
    def _extract_via_gemini(raw_text: str, target_model: str) -> dict:
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={api_key}"
        
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "skills": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
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
                }
            },
            "required": ["skills", "projects"]
        }

        prompt = (
            f"Analyze the following resume text. Extract all technical/vocational skills "
            f"and projects. Return ONLY a JSON object matching this schema.\n\n"
            f"Resume Text:\n{raw_text[:6000]}"
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
                "temperature": 0.1
            }
        }

        try:
            # High-performance, low-overhead direct API call (10-second timeout is plenty for cloud)
            response = requests.post(url, json=payload, timeout=60)
            
            # Auto-Fallback Logic if we hit a 429 Rate Limit on TIER_MEDIUM
            if response.status_code == 429 and target_model != AIGateway.TIER_FALLBACK:
                return AIGateway._extract_via_gemini(raw_text, target_model=AIGateway.TIER_FALLBACK)
                
            response.raise_for_status()
            
            result_json = response.json()
            text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
        except Exception as e:
            raise ConnectionError(f"Cloud Gemini extraction failed on model {target_model}: {str(e)}")



# Add this class method inside the AIGateway class:

    @staticmethod
    def generate_adaptive_test(role_title: str, skills: list, projects: list) -> dict:
        """
        Generates a 5-question progressively adaptive test tailored specifically 
        to the student's claimed resume projects and target industry benchmark.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            return AIGateway._generate_test_via_gemini(role_title, skills, projects)
        else:
            # High-fidelity mock fallback test for offline development
            mock_questions = [
                {
                    "id": 1,
                    "question_text": f"Which of the following is a core characteristic of building systems with {skills[0] if skills else 'Programming'}?",
                    "type": "MCQ",
                    "difficulty": "EASY",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "A",
                    "explanation": "Core fundamental concept verification."
                },
                {
                    "id": 2,
                    "question_text": "How do you handle routing states in your typical application configurations?",
                    "type": "MCQ",
                    "difficulty": "EASY",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "B",
                    "explanation": "Framework execution logic."
                },
                {
                    "id": 3,
                    "question_text": f"In your project '{projects[0]['title'] if projects else 'Main Project'}', how did you manage data validation?",
                    "type": "MCQ",
                    "difficulty": "MEDIUM",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "C",
                    "explanation": "ProjectClaim verification."
                },
                {
                    "id": 4,
                    "question_text": "Explain the architectural advantages of the technology stack choices you made in your projects.",
                    "type": "VIVA",
                    "difficulty": "MEDIUM",
                    "options": None,
                    "correct_answer": None,
                    "explanation": "Looking for clear structural articulation and framework differences."
                },
                {
                    "id": 5,
                    "question_text": "If your primary system experiences a 10x spike in traffic, describe your immediate bottleneck resolution plan.",
                    "type": "VIVA",
                    "difficulty": "HARD",
                    "options": None,
                    "correct_answer": None,
                    "explanation": "Looking for concurrency, database index optimization, or caching explanations."
                }
            ]
            
            # Pack rubrics into session token
            session_data = json.dumps({"questions": mock_questions})
            token = base64.b64encode(session_data.encode()).decode()
            
            return {
                "role_title": role_title,
                "questions": mock_questions,
                "test_session_token": token
            }

    @staticmethod
    def _generate_test_via_gemini(role_title: str, skills: list, projects: list) -> dict:
        api_key = os.getenv("GEMINI_API_KEY")
        model = AIGateway.TIER_HIGH  # gemini-3.5-flash-lite (500 RPD)
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        # Define the strict output schema
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
                            "correct_answer": {"type": "STRING"},  # E.g., "A", "B", "C", "D" or null
                            "explanation": {"type": "STRING"}      # Rubric standard for grading
                        },
                        "required": ["id", "question_text", "type", "difficulty", "explanation"]
                    }
                }
            },
            "required": ["questions"]
        }

        # Dynamic, progressively adaptive prompt instruction
        prompt = (
            f"You are a strict technical interviewer. Generate a personalized 5-question test for a candidate "
            f"applying for the role of '{role_title}'.\n"
            f"Candidate Extracted Skills: {skills}\n"
            f"Candidate Projects: {projects}\n\n"
            f"Enforce these strict progressive difficulty criteria:\n"
            f"1. Question 1 (MCQ - EASY): Core language/tool syntax check. Focus on basic code literacy.\n"
            f"2. Question 2 (MCQ - EASY): Basic framework mechanics (e.g. Django vs Flask depending on their stack).\n"
            f"3. Question 3 (MCQ - MEDIUM): Directly target a technical choice made in one of their listed projects.\n"
            f"4. Question 4 (VIVA - MEDIUM): Open-ended question asking the candidate to explain their architectural patterns.\n"
            f"5. Question 5 (VIVA - HARD): High-load, system failure, or optimization stress test matching their technology stack.\n\n"
            f"For VIVA questions, set 'options' to null and 'correct_answer' to null, and write a detailed "
            f"grading rubric explanation of what a high-quality answer must mention."
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
                "temperature": 0.3
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result_json = response.json()
            text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
            test_data = json.loads(text_response)
            
            # Obfuscate correct answers and grading rubrics into a base64 session token
            session_data = json.dumps({"questions": test_data["questions"]})
            session_token = base64.b64encode(session_data.encode()).decode()
            
            return {
                "role_title": role_title,
                "questions": test_data["questions"],
                "test_session_token": session_token
            }
        except Exception as e:
            raise ConnectionError(f"Cloud Gemini test generation failed: {str(e)}")
