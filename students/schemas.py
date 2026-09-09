from ninja import Schema
from typing import List, Optional, Dict, Any

class ResumeUploadOutSchema(Schema):
    success: bool
    message: str
    raw_text: str

class StudentProfileInSchema(Schema):
    github_handle: Optional[str] = None
    bio: Optional[str] = None
    skills: List[str] = []
    placement_status: str = "UNPLACED"

class StudentProfileOutSchema(Schema):
    id: int
    username: str
    email: str
    github_handle: Optional[str] = None
    bio: Optional[str] = None
    skills: List[str] = []
    role_fit_matrix: Dict[str, Any] = {}
    overall_confidence_score: float
    is_verified: bool

class ResumeAnalysisInSchema(Schema):
    raw_text: str


class QuestionOutSchema(Schema):
    id: int
    question_text: str
    type: str  # "MCQ" or "VIVA"
    difficulty: str  # "EASY", "MEDIUM", "HARD"
    options: Optional[List[str]] = None  # Only populated for MCQ
    # We do NOT send the correct_answer to the frontend to prevent client-side inspection/cheating!

class TestGenerationOutSchema(Schema):
    role_title: str
    questions: List[QuestionOutSchema]
    # We return an encrypted or obfuscated session key containing the correct answers and grading rubrics
    test_session_token: str 
