#Go to http://127.0.0.1:8000/api/v1/docs after python manage.py runserver
from ninja import NinjaAPI, Router, Schema
from typing import List, Optional

api = NinjaAPI(
    title="Skill Setu API",
    version="1.0.0",
    docs_url="/docs"
)

# ----------------- SCHEMAS -----------------

class TokenOut(Schema):
    access_token: str
    token_type: str = "bearer"
    role: str

class LoginIn(Schema):
    username: str
    password: str

class StudentOut(Schema):
    id: int
    name: str
    email: str
    skills: List[str]
    github_handle: Optional[str] = None
    placement_status: str

class RecruiterOut(Schema):
    id: int
    company_name: str
    industry: str
    contact_email: str

class ListingOut(Schema):
    id: int
    title: str
    company_name: str
    role_type: str
    required_skills: List[str]
    stipend: Optional[str] = None

# ----------------- ROUTERS -----------------

auth_router = Router(tags=["Authentication"])
students_router = Router(tags=["Students"])
recruiters_router = Router(tags=["Recruiters"])
listings_router = Router(tags=["Listings"])

@auth_router.post("/login", response=TokenOut)
def login_stub(request, payload: LoginIn):
    return {
        "access_token": "mock-jwt-token-xyz",
        "token_type": "bearer",
        "role": "student"
    }

@students_router.get("/", response=List[StudentOut])
def list_students_stub(request):
    return [
        {
            "id": 1,
            "name": "Alex Dev",
            "email": "alex@university.edu",
            "skills": ["Python", "React", "Docker"],
            "github_handle": "alexdev",
            "placement_status": "unplaced"
        }
    ]

@recruiters_router.get("/", response=List[RecruiterOut])
def list_recruiters_stub(request):
    return [
        {
            "id": 101,
            "company_name": "Acme Innovations",
            "industry": "Enterprise Software",
            "contact_email": "talent@acme.example"
        }
    ]

@listings_router.get("/", response=List[ListingOut])
def list_listings_stub(request):
    return [
        {
            "id": 501,
            "title": "Backend Engineering Intern",
            "company_name": "Acme Innovations",
            "role_type": "Internship",
            "required_skills": ["Python", "Django", "PostgreSQL"],
            "stipend": "INR 25,000/month"
        }
    ]

# ----------------- REGISTER -----------------

api.add_router("/auth", auth_router)
api.add_router("/students", students_router)
api.add_router("/recruiters", recruiters_router)
api.add_router("/listings", listings_router)