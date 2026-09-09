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
    
    @staticmethod
    def extract_skills_and_projects(raw_text: str) -> dict:
        """
        Task 1: Resume Extraction. Routed strictly to gemini-3.1-flash-lite.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            model = os.getenv("MODEL_RESUME_PARSER", "gemini-3.1-flash-lite")
            
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
                f"and personal projects. Return ONLY a JSON object matching this schema.\n\n"
                f"Resume Text:\n{raw_text[:6000]}"
            )

            return AIGateway._execute_gemini_request(model, prompt, response_schema)
            
        elif provider == "local":
            return OllamaClient.analyze_resume_text(raw_text)
        else:
            return {"skills": ["Python", "Django", "PostgreSQL", "Git"], "projects": []}

    @staticmethod
    def generate_adaptive_test(role_title: str, skills: list, projects: list) -> dict:
        """
        Task 2: Progressive Test Generation. Routed strictly to gemini-3.5-flash-lite.
        """
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            model = os.getenv("MODEL_TEST_GENERATOR", "gemini-3.5-flash-lite")
            
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
                f"You are a strict technical interviewer. Generate a personalized 5-question test for a candidate "
                f"applying for the role of '{role_title}'.\n"
                f"Candidate Extracted Skills: {skills}\n"
                f"Candidate Projects: {projects}\n\n"
                f"Enforce these strict progressive difficulty criteria:\n"
                f"1. Question 1 (MCQ - EASY): Core language/tool syntax check. Focus on basic code literacy.\n"
                f"2. Question 2 (MCQ - EASY): Basic framework mechanics.\n"
                f"3. Question 3 (MCQ - MEDIUM): Directly target a technical choice made in one of their listed projects.\n"
                f"4. Question 4 (VIVA - MEDIUM): Open-ended question asking the candidate to explain their architectural patterns.\n"
                f"5. Question 5 (VIVA - HARD): High-load, system failure, or optimization stress test matching their technology stack.\n\n"
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
