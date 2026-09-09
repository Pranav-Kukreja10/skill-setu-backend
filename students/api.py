from ninja import Router, File
from ninja.files import UploadedFile
from typing import List
from django.shortcuts import get_object_or_404
from students.models import StudentProfile
from students.services import extract_text_from_file
from students.schemas import StudentProfileInSchema, StudentProfileOutSchema, ResumeUploadOutSchema
from accounts.security import JWTAuth

# Protect all routes inside this domain with our verified JWTAuth bearer token
router = Router(tags=["Students"], auth=JWTAuth())

@router.post("/resume-upload", response={200: ResumeUploadOutSchema, 400: dict})
def upload_resume(request, file: UploadedFile = File(...)):
    """
    Receives an uploaded resume (PDF, DOCX, TXT, MD) from the React frontend,
    extracts text instantly in-memory, and returns the parsed output.
    """
    allowed_extensions = ('.pdf', '.docx', '.txt', '.md')
    
    # Enforce strict multi-format validation
    if not file.name.lower().endswith(allowed_extensions):
        return 400, {
            "message": "Unsupported file format. Supported file types: PDF, DOCX, TXT, MD."
        }
        
    try:
        raw_text = extract_text_from_file(file)
        
        if not raw_text:
            return 400, {"message": "The file appears to be empty, encrypted, or unscannable."}
            
        return 200, {
            "success": True,
            "message": f"Resume ({file.name}) successfully parsed in-memory.",
            "raw_text": raw_text
        }
    except Exception as e:
        return 400, {"message": f"Parsing Error: {str(e)}"}


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
