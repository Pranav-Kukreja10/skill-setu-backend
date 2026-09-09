from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from students.models import StudentProfile
from students.schemas import StudentProfileInSchema, StudentProfileOutSchema
from accounts.security import JWTAuth

# Protect all routes in this router with our JWTAuth dependency
router = Router(tags=["Students"], auth=JWTAuth())

@router.get("/", response=List[StudentProfileOutSchema])
def list_students(request):
    """Retrieve all student profiles for recruiters."""
    profiles = StudentProfile.objects.select_related('user').all()
    
    result = []
    for profile in profiles:
        result.append({
            "id": profile.id,
            "username": profile.user.username,
            "email": profile.user.email,
            "github_handle": profile.github_handle,
            "bio": profile.bio,
            "skills": profile.skills,
            "placement_status": profile.placement_status,
            "github_score": profile.github_score,
        })
    return result

@router.post("/me", response=StudentProfileOutSchema)
def update_my_profile(request, payload: StudentProfileInSchema):
    """Create or update the currently logged-in student's profile."""
    # request.auth contains the User object provided by JWTAuth
    profile, created = StudentProfile.objects.get_or_create(user=request.auth)
    
    profile.github_handle = payload.github_handle or profile.github_handle
    profile.bio = payload.bio or profile.bio
    profile.skills = payload.skills
    profile.placement_status = payload.placement_status
    profile.save()

    return {
        "id": profile.id,
        "username": request.auth.username,
        "email": request.auth.email,
        "github_handle": profile.github_handle,
        "bio": profile.bio,
        "skills": profile.skills,
        "placement_status": profile.placement_status,
        "github_score": profile.github_score,
    }
