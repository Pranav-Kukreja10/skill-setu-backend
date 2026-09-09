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
