from ninja import Schema
from typing import List, Optional

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
    skills: List[str]
    placement_status: str
    github_score: float

class ResumeUploadOutSchema(Schema):
    success: bool 
    message: str 
    raw_text: str 