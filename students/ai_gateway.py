import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from students.ollama_client import OllamaClient

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
