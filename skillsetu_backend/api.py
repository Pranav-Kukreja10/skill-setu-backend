#Go to http://127.0.0.1:8000/api/v1/docs after python manage.py runserver
from ninja import NinjaAPI, Router, Schema
from typing import List, Optional

# 1. IMPORT THE REAL ROUTERS HERE
from accounts.api import router as accounts_router
from students.api import router as students_router

api = NinjaAPI(
    title="Skill Setu API",
    version="1.0.0",
    docs_url="/docs"
)

# ----------------- SCHEMAS & MOCK ROUTERS (Keep only the Recruiters/Listings stubs) -----------------

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

recruiters_router = Router(tags=["Recruiters"])
listings_router = Router(tags=["Listings"])

@recruiters_router.get("/", response=List[RecruiterOut])
def list_recruiters_stub(request):
    return [{"id": 101, "company_name": "Acme Innovations", "industry": "Enterprise Software", "contact_email": "talent@acme.example"}]

@listings_router.get("/", response=List[ListingOut])
def list_listings_stub(request):
    return [{"id": 501, "title": "Backend Engineering Intern", "company_name": "Acme Innovations", "role_type": "Internship", "required_skills": ["Python", "Django", "PostgreSQL"], "stipend": "INR 25,000/month"}]


# ----------------- REGISTER ROUTERS -----------------

# 2. REGISTER THE REAL ACCOUNTS ROUTER (This contains both /login and /register)
api.add_router("/auth", accounts_router)

# Register the real students router
api.add_router("/students", students_router)

# Register the remaining mocks
api.add_router("/recruiters", recruiters_router)
api.add_router("/listings", listings_router)
