from pydantic import EmailStr, Field
from ninja import Schema
from typing import Optional

class UserRegisterSchema(Schema):
    username: str = Field(..., max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., description="STUDENT, RECRUITER, ACADEMIA, or ADMIN")
    phone_number: Optional[str] = None

class UserLoginSchema(Schema):
    username: str
    password: str

class UserProfileOutSchema(Schema):
    id: int
    username: str
    email: str
    role: str
    phone_number: Optional[str] = None
