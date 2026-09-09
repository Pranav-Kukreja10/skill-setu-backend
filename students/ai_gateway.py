import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from students.ollama_client import OllamaClient

# Force Python to read the .env file directly from the disk
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

class AIGateway:
    """
    Unified, model-agnostic gateway featuring a Dynamic Round-Robin Load Balancer.
    Pools Gemini 3.5 Flash Lite and 3.1 Flash Lite to effectively double the 
    free-tier RPM limits and provides instant fallover on rate limits (429).
    """
    
    # 1. Define our high-capacity Model Pool
    MODEL_POOL = [
        "gemini-3.5-flash-lite", 
        "gemini-3.1-flash-lite"
    ]
    
    # Simple in-memory counter to alternate models across requests
    _request_counter = 0
    
    @classmethod
    def _get_next_model(cls) -> str:
        """Round-robin selector to distribute load evenly."""
        model = cls.MODEL_POOL[cls._request_counter % len(cls.MODEL_POOL)]
        cls._request_counter += 1
        return model

    @staticmethod
    def extract_skills_and_projects(raw_text: str) -> dict:
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
            prompt = (
                f"Analyze the following resume text. Extract all technical/vocational skills "
                f"and projects. Return ONLY a JSON object matching this schema.\n\n"
                f"Resume Text:\n{raw_text[:6000]}"
            )
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "projects": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {"type": "STRING"},
                                "technologies": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "description": {"type": "STRING"}
                            },
                            "required": ["title", "technologies", "description"]
                        }
                    }
                },
                "required": ["skills", "projects"]
            }
            return AIGateway._execute_with_fallover(prompt, response_schema, timeout=60)
            
        elif provider == "local":
            return OllamaClient.analyze_resume_text(raw_text)
        else:
            return {"skills": ["Python"], "projects": []}

    @staticmethod
    def generate_adaptive_test(role_title: str, skills: list, projects: list) -> dict:
        provider = os.getenv("AI_PROVIDER", "local").lower()
        
        if provider == "cloud":
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
                                "options": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "correct_answer": {"type": "STRING"},
                                "explanation": {"type": "STRING"}      
                            },
                            "required": ["id", "question_text", "type", "difficulty", "explanation"]
                        }
                    }
                },
                "required": ["questions"]
            }
            return AIGateway._execute_with_fallover(prompt, response_schema, timeout=90)
        else:
            return {"questions": []}

    @staticmethod
    def _execute_with_fallover(prompt: str, response_schema: dict, timeout: int) -> dict:
        """
        Core Execution Engine: Routes the request to the active round-robin model.
        If a rate limit (429) or timeout occurs, it automatically falls over to the backup model.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        # 1. Select the primary model via Round-Robin
        primary_model = AIGateway._get_next_model()
        
        # 2. Identify the backup model
        backup_model = AIGateway.MODEL_POOL[0] if primary_model == AIGateway.MODEL_POOL[1] else AIGateway.MODEL_POOL[1]

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
                "temperature": 0.1
            }
        }

        try:
            # 3. Attempt execution on Primary Model
            print(f"[AIGateway] Routing request to primary model: {primary_model}")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{primary_model}:generateContent?key={api_key}"
            response = requests.post(url, json=payload, timeout=timeout)
            
            if response.status_code == 429:
                raise requests.exceptions.RequestException("Rate Limit Hit")
                
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            # 4. Instant Fallover to Backup Model
            print(f"[AIGateway] Primary model {primary_model} failed ({str(e)}). Falling over to {backup_model}...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{backup_model}:generateContent?key={api_key}"
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()

        result_json = response.json()
        text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_response, strict=False)
