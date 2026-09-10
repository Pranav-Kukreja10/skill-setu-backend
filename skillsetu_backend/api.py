# Skill Setu API Central Orchestrator
# Go to http://127.0.0.1:8000/api/v1/docs after python manage.py runserver
from ninja import NinjaAPI

from accounts.api import router as accounts_router
from students.api import router as students_router, schemes_router
from recruiters.api import (
    recruiters_router,
    listings_router,
    applications_router,
    programs_router
)
from institutions.api import (
    placement_router,
    institutions_router
)

api = NinjaAPI(
    title="Skill Setu API",
    version="1.0.0",
    docs_url="/docs"
)

# Authentication & User Identity Domain
api.add_router("/auth", accounts_router)

# Student Screening, Resume Analysis & Testing Domain
api.add_router("/students", students_router)

# Multi-Domain Government & Affirmative Action Schemes
api.add_router("/schemes", schemes_router)

# Recruiter & Company Profile Management Domain
api.add_router("/recruiters", recruiters_router)

# Job & Internship Posting Engine + Candidate NLP Search
api.add_router("/listings", listings_router)

# Application Lifecycle & Candidate Review Pipeline
api.add_router("/applications", applications_router)

# Industry Learning Programs, Workshops & Collaboration Initiatives (PS Requirement)
api.add_router("/programs", programs_router)

# Institutional Placement Analytics & Faculty Reporting
api.add_router("/placement", placement_router)

# Colleges, Universities, Departments & Faculty Profiles
api.add_router("/institutions", institutions_router)


