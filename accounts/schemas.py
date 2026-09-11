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
    auth_provider: str = "LOCAL"
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None

# --- OAUTH2 SSO SCHEMAS ---

class OAuthUrlOutSchema(Schema):
    google_auth_url: str
    github_auth_url: str

class OAuthLoginInSchema(Schema):
    provider: str = Field(..., description="'google' or 'github'")
    token_or_code: str = Field(..., description="Google ID Token / Access Token or GitHub Authorization Code")
    role: Optional[str] = Field("STUDENT", description="Role to assign if auto-provisioning a new account (STUDENT, RECRUITER, ACADEMIA)")

class OAuthAuthResponseOut(Schema):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    email: str
    avatar_url: Optional[str] = None
    is_new_user: bool
    auth_provider: str
    message: str
