from ninja import Schema
from typing import List, Optional, Dict, Any

# --- PHASE 1 & 2 SCHEMAS (Resume Upload & Parsing) ---

class ResumeUploadOutSchema(Schema):
    success: bool
    message: str
    raw_text: str

class ResumeAnalysisInSchema(Schema):
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


# --- PHASE 3 SCHEMAS (Test Generation) ---

class QuestionOutSchema(Schema):
    id: int
    question_text: str
    type: str  # "MCQ" or "VIVA"
    difficulty: str  # "EASY", "MEDIUM", "HARD"
    options: Optional[List[str]] = None  # Only populated for MCQ

class TestGenerationOutSchema(Schema):
    role_title: str
    session_id: int  # Clean, database-backed session tracking
    questions: List[QuestionOutSchema]


# --- PHASE 4 SCHEMAS (Test Submission & Grading) ---

class StudentAnswerInSchema(Schema):
    id: int
    answer_text: str

class TestSubmissionInSchema(Schema):
    target_role: str
    session_id: int  # Simple reference to the PostgreSQL active session
    answers: List[StudentAnswerInSchema]

class FeedbackDetailSchema(Schema):
    id: int
    question_text: str
    type: str
    student_answer: str
    score: int
    feedback: str

class TestGradingOutSchema(Schema):
    success: bool
    cognitive_score: int
    mcq_average: int
    viva_average: int
    confidence_score: int
    feedback_log: List[FeedbackDetailSchema]
