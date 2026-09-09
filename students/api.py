from ninja import Router, File
from ninja.files import UploadedFile
from typing import List
from django.shortcuts import get_object_or_404
from students.models import StudentProfile
from students.services import extract_text_from_file, generate_role_fit_matrix
from students.ai_gateway import AIGateway  # <--- IMPORT THE GATEWAY HERE
from students.schemas import StudentProfileInSchema, StudentProfileOutSchema, ResumeUploadOutSchema, ResumeAnalysisInSchema, TestGenerationOutSchema, QuestionOutSchema
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
    if not file.name.lower().endswith(allowed_extensions):
        return 400, {
            "message": "Unsupported file format. Supported file types: PDF, DOCX, TXT, MD."
        }
        
    try:
        raw_text = extract_text_from_file(file)
        if not raw_text:
            return 400, {"message": "The file appears to be empty or unscannable."}
            
        return 200, {
            "success": True,
            "message": f"Resume ({file.name}) successfully parsed in-memory.",
            "raw_text": raw_text
        }
    except Exception as e:
        return 400, {"message": f"Parsing Error: {str(e)}"}

@router.post("/analyze-resume", response={200: StudentProfileOutSchema, 400: dict})
def analyze_student_resume(request, payload: ResumeAnalysisInSchema):
    """
    Submits raw parsed text to the AI Gateway, auto-extracts skills 
    and projects, maps them against role benchmarks, and saves the 
    profile structure to PostgreSQL.
    """
    raw_text = payload.raw_text
    if not raw_text:
        return 400, {"message": "No raw text provided for analysis."}
        
    try:
        # 1. Trigger the Unified AI Gateway (Automatically routes based on .env)
        analysis_result = AIGateway.extract_skills_and_projects(raw_text)
        extracted_skills = analysis_result.get("skills", [])
        
        # 2. Get the student's database profile (linked to the authenticated user)
        profile, created = StudentProfile.objects.get_or_create(user=request.auth)
        
        # 3. Calculate dynamic industry fit matrix
        fit_matrix = generate_role_fit_matrix(extracted_skills)
        
        # 4. Save results to PostgreSQL fields
        profile.skills = extracted_skills
        profile.projects = analysis_result.get("projects", [])
        profile.role_fit_matrix = fit_matrix
        profile.bio = f"Auto-extracted {len(extracted_skills)} skills and {len(analysis_result.get('projects', []))} projects."
        profile.save()
        
        # Return populated profile matching StudentProfileOutSchema
        return 200, {
            "id": profile.id,
            "username": request.auth.username,
            "email": request.auth.email,
            "github_handle": profile.github_handle,
            "bio": profile.bio,
            "skills": profile.skills,
            "role_fit_matrix": profile.role_fit_matrix,
            "overall_confidence_score": profile.overall_confidence_score,
            "is_verified": profile.is_verified
        }
    except Exception as e:
        return 400, {"message": f"AI Parsing/Sync Failure: {str(e)}"}

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
            "role_fit_matrix": profile.role_fit_matrix,
            "overall_confidence_score": profile.overall_confidence_score,
            "is_verified": profile.is_verified,
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
        "role_fit_matrix": profile.role_fit_matrix,
        "overall_confidence_score": profile.overall_confidence_score,
        "is_verified": profile.is_verified,
    }

@router.get("/generate-test", response={200: TestGenerationOutSchema, 400: dict})
def get_student_screening_test(request, role_title: str):
    """
    Generates a personalized, progressive 5-question technical screening test
    tailored to the student's resume profile and target career path.
    """
    profile = get_object_or_404(StudentProfile, user=request.auth)
    
    if not profile.skills:
        return 400, {
            "message": "Your profile has no extracted skills. Please upload and parse your resume first."
        }
        
    try:
        # Trigger our Unified AIGateway adaptive generation engine
        test_session = AIGateway.generate_adaptive_test(
            role_title=role_title,
            skills=profile.skills,
            projects=profile.projects
        )
        
        # Strip correct answers and grading rubrics before sending the payload to the client
        secured_questions = []
        for q in test_session["questions"]:
            secured_questions.append({
                "id": q["id"],
                "question_text": q["question_text"],
                "type": q["type"],
                "difficulty": q["difficulty"],
                "options": q.get("options")
            })
            
        return 200, {
            "role_title": test_session["role_title"],
            "questions": secured_questions,
            "test_session_token": test_session["test_session_token"]
        }
    except Exception as e:
        return 400, {"message": f"Test Generation Failure: {str(e)}"}