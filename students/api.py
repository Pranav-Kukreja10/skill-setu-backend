from ninja import Router, File, Body
from ninja.files import UploadedFile
from typing import List, Optional, Dict, Any
from datetime import datetime
from django.utils import timezone
from django.db import transaction, models, OperationalError
from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.security import JWTAuth, RecruiterAuth, StudentAuth
from students.models import StudentProfile, TestSession, Notification
from recruiters.models import JobListing, JobApplication, Company
from students.services import (
    extract_text_from_file,
    generate_role_fit_matrix,
    build_skills_matrix,
    compute_profile_strength
)
from students.ai_gateway import AIGateway
from students.grader import ResilientGrader
from students.search import index_student_profile, rank_student_profiles
from recruiters.search import rank_job_listings, compute_job_skill_overlap
from students.recommendations import (
    compute_personalized_recommendations,
    compute_skill_gap_roadmap
)
from students.schemas import (
    StudentProfileInSchema, 
    StudentProfileOutSchema, 
    ResumeUploadOutSchema, 
    ResumeAnalysisInSchema, 
    ResumePreviewOutSchema,
    TestGenerationOutSchema, 
    TestSubmissionInSchema, 
    TestGradingOutSchema,
    RecruiterSearchQueryIn,
    RecruiterSearchResponseOut,
    JobDiscoveryFeedOut,
    JobDiscoveryItemOut,
    PersonalizedRecommendationsFeedOut,
    SkillGapRoadmapOut,
    NotificationsResponseOut,
    NotificationItemOut,
    DeadlinesHubOut,
    UpcomingInterviewOut,
    UpcomingDeadlineOut
)
from recruiters.schemas import (
    CandidateJobSearchIn,
    CandidateJobSearchResponseOut,
    JobApplicationApplyIn,
    JobApplicationOut,
    StudentMyApplicationOut,
    ApplicantStudentOut
)

# Protect all routes inside this domain with our verified JWTAuth bearer token
router = Router(tags=["Students"], auth=JWTAuth())


def _student_to_out_schema(profile: StudentProfile) -> dict:
    """Format StudentProfile to StudentProfileOutSchema dict with safe fallback defaults."""
    p_strength, breakdown = compute_profile_strength(profile)
    return {
        "id": profile.id,
        "username": profile.user.username,
        "email": profile.user.email,
        "bio": profile.bio or "",
        "current_designation": getattr(profile, 'current_designation', "") or "",
        "experience_years": getattr(profile, 'experience_years', 0.0) or 0.0,
        "institution": profile.institution or "",
        "department": profile.department or "",
        "degree": profile.degree or "",
        "cgpa": profile.cgpa,
        "graduation_year": profile.graduation_year,
        "github_handle": profile.github_handle,
        "github_url": getattr(profile, 'github_url', "") or "",
        "linkedin_url": profile.linkedin_url or "",
        "portfolio_url": profile.portfolio_url or "",
        "certifications": getattr(profile, 'certifications', []) or [],
        "skills_matrix": profile.skills_matrix or {},
        "skills_categorized": profile.skills_categorized or {},
        "raw_extracted_skills": profile.raw_extracted_skills or [],
        "role_fit_matrix": profile.role_fit_matrix or {},
        "target_roles": profile.target_roles or [],
        "placement_status": profile.placement_status or "UNPLACED",
        "overall_confidence_score": profile.overall_confidence_score,
        "profile_strength_score": p_strength,
        "profile_strength_breakdown": breakdown,
        "is_verified": profile.is_verified
    }


def _application_to_schema(app: JobApplication) -> JobApplicationOut:
    """Helper to convert a JobApplication to JobApplicationOut schema."""
    student = app.student
    user = student.user
    p_strength = compute_profile_strength(student)[0]
    return JobApplicationOut(
        id=app.id,
        listing_id=app.listing.id,
        listing_title=app.listing.title,
        company_name=app.listing.company.name,
        student=ApplicantStudentOut(
            id=user.id,
            student_profile_id=student.id,
            username=user.username,
            email=user.email,
            bio=student.bio or "",
            current_designation=getattr(student, 'current_designation', "") or "",
            experience_years=getattr(student, 'experience_years', 0.0) or 0.0,
            institution=student.institution or "",
            department=student.department or "",
            github_url=getattr(student, 'github_url', "") or "",
            certifications=getattr(student, 'certifications', []) or [],
            profile_strength_score=p_strength,
            skills_matrix=student.skills_matrix or {},
            raw_extracted_skills=student.raw_extracted_skills or [],
            role_fit_matrix=student.role_fit_matrix or {},
            target_roles=student.target_roles or [],
            overall_confidence_score=student.overall_confidence_score,
            is_verified=student.is_verified,
            placement_status=student.placement_status,
            is_blind=False
        ),
        status=app.status,
        match_score=app.match_score,
        recruiter_notes=app.recruiter_notes or "",
        interview_date=getattr(app, 'interview_date', None),
        status_history=app.status_history or [],
        created_at=app.created_at,
        updated_at=app.updated_at
    )


# ---------------------------------------------------------
# 1. RESUME MANAGEMENT & AI PARSING
# ---------------------------------------------------------

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


@router.post("/resume-preview-extract", response={200: ResumePreviewOutSchema, 400: dict})
def preview_and_extract_resume(request, file: UploadedFile = File(...)):
    """
    Candidate Upload Preview & Review Interface:
    Parses resume in-memory, queries AI Gateway for skills, academic credentials, 
    social links, and categorized competencies, but DOES NOT commit to the database.
    Allows the candidate to preview, verify, and edit their details in the UI first.
    """
    allowed_extensions = ('.pdf', '.docx', '.txt', '.md')
    if not file.name.lower().endswith(allowed_extensions):
        return 400, {"message": "Unsupported file format. Supported file types: PDF, DOCX, TXT, MD."}

    try:
        raw_text = extract_text_from_file(file)
        if not raw_text:
            return 400, {"message": "The file appears to be empty or unscannable."}

        # Query Cloud AI Gateway
        analysis = AIGateway.extract_skills_and_projects(raw_text)
        certs = analysis.get("certifications", [])

        # Build candidate skills matrix Ws = 0.6*Pe + 0.4*Er with +15% credential boost
        skills_matrix = build_skills_matrix(analysis.get("skills", []), certs)

        return 200, {
            "success": True,
            "raw_text": raw_text,
            "current_designation": analysis.get("current_designation", ""),
            "experience_years": float(analysis.get("experience_years", 0.0) or 0.0),
            "academic_credentials": analysis.get("academic_credentials", {}),
            "skills_categorized": analysis.get("skills_categorized", {}),
            "skills_matrix": skills_matrix,
            "projects": analysis.get("projects", []),
            "certifications": certs,
            "target_roles": analysis.get("target_roles", []),
            "social_links": analysis.get("social_links", {})
        }
    except Exception as e:
        return 400, {"message": f"Preview Extraction Error: {str(e)}"}


@router.post("/analyze-resume", response={200: StudentProfileOutSchema, 400: dict})
def analyze_student_resume(request, payload: ResumeAnalysisInSchema):
    """
    Submits raw parsed text to the AI Gateway, auto-extracts skills,
    academic credentials, categorized competencies, and projects,
    calculates fitment matrices, and saves the candidate profile to PostgreSQL.
    """
    raw_text = payload.raw_text
    if not raw_text:
        return 400, {"message": "No raw text provided for analysis."}
        
    try:
        # 1. Trigger Cloud AI Gateway
        analysis_result = AIGateway.extract_skills_and_projects(raw_text)
        extracted_skills_list = analysis_result.get("skills", [])
        extracted_certs = analysis_result.get("certifications", [])
        
        # 2. Compile structured skills matrix with dynamic weights & +15% credential boost
        skills_matrix = build_skills_matrix(extracted_skills_list, extracted_certs)
        flat_skills_list = [s["name"] for s in extracted_skills_list if s.get("name")]
        
        # 3. Retrieve and update Student Profile
        profile, created = StudentProfile.objects.get_or_create(user=request.auth)
        
        # 4. Calculate dynamic industry fit matrix using structured weights
        fit_matrix = generate_role_fit_matrix(skills_matrix)
        
        # 5. Save results to PostgreSQL fields
        profile.skills_matrix = skills_matrix
        profile.raw_extracted_skills = flat_skills_list
        profile.projects = analysis_result.get("projects", [])
        profile.certifications = extracted_certs
        profile.target_roles = analysis_result.get("target_roles", [])
        profile.role_fit_matrix = fit_matrix

        # Structured skills categorized
        if "skills_categorized" in analysis_result and analysis_result["skills_categorized"]:
            profile.skills_categorized = analysis_result["skills_categorized"]

        # Academic credentials (populate if currently empty)
        acad = analysis_result.get("academic_credentials", {})
        if acad:
            if not profile.institution and acad.get("institution"):
                profile.institution = acad["institution"]
            if not profile.department and acad.get("department"):
                profile.department = acad["department"]
            if not profile.degree and acad.get("degree"):
                profile.degree = acad["degree"]
            if profile.cgpa is None and acad.get("cgpa") is not None:
                profile.cgpa = acad["cgpa"]
            if profile.graduation_year is None and acad.get("graduation_year") is not None:
                profile.graduation_year = acad["graduation_year"]

        # Social links (populate if currently empty)
        social = analysis_result.get("social_links", {})
        if social:
            if not profile.github_handle and social.get("github_handle"):
                profile.github_handle = social["github_handle"]
            if not getattr(profile, 'github_url', None) and social.get("github"):
                profile.github_url = social["github"]
            if not profile.linkedin_url and social.get("linkedin_url"):
                profile.linkedin_url = social["linkedin_url"]
            if not profile.portfolio_url and social.get("portfolio_url"):
                profile.portfolio_url = social["portfolio_url"]

        # Current designation and experience (populate if present)
        if analysis_result.get("current_designation") and not profile.current_designation:
            profile.current_designation = analysis_result["current_designation"]
        if analysis_result.get("experience_years") is not None and profile.experience_years == 0.0:
            try:
                profile.experience_years = float(analysis_result["experience_years"])
            except (ValueError, TypeError):
                pass

        profile.bio = f"Auto-extracted {len(skills_matrix)} skills and {len(profile.projects)} projects."
        profile.save()

        # Re-index dense vector and text search corpus
        try:
            index_student_profile(profile)
        except Exception:
            pass
        
        return 200, _student_to_out_schema(profile)
    except Exception as e:
        return 400, {"message": f"AI Parsing/Sync Failure: {str(e)}"}


# ---------------------------------------------------------
# 2. PROFILE MANAGEMENT (GET / PUT / POST /me)
# ---------------------------------------------------------

@router.get("/me", response=StudentProfileOutSchema)
def get_my_profile(request):
    """Retrieve the currently logged-in student's full verified profile."""
    profile, _ = StudentProfile.objects.get_or_create(user=request.auth)
    return _student_to_out_schema(profile)


@router.put("/me", response=StudentProfileOutSchema)
def update_my_profile_put(request, payload: StudentProfileInSchema):
    """
    Update candidate's profile, including academic credentials, social links,
    certifications, categorized competencies, target roles, and placement status.
    """
    profile, _ = StudentProfile.objects.get_or_create(user=request.auth)
    
    if payload.bio is not None:
        profile.bio = payload.bio
    if payload.current_designation is not None:
        profile.current_designation = payload.current_designation
    if payload.experience_years is not None:
        profile.experience_years = payload.experience_years
    if payload.institution is not None:
        profile.institution = payload.institution
    if payload.department is not None:
        profile.department = payload.department
    if payload.degree is not None:
        profile.degree = payload.degree
    if payload.cgpa is not None:
        profile.cgpa = payload.cgpa
    if payload.graduation_year is not None:
        profile.graduation_year = payload.graduation_year
    if payload.github_handle is not None:
        profile.github_handle = payload.github_handle
    if payload.github_url is not None:
        profile.github_url = payload.github_url
    if payload.linkedin_url is not None:
        profile.linkedin_url = payload.linkedin_url
    if payload.portfolio_url is not None:
        profile.portfolio_url = payload.portfolio_url
    if payload.certifications is not None:
        profile.certifications = payload.certifications
    if payload.placement_status is not None:
        profile.placement_status = payload.placement_status
    if payload.target_roles is not None:
        profile.target_roles = payload.target_roles
    if payload.skills_categorized is not None:
        profile.skills_categorized = payload.skills_categorized

    if payload.skills_matrix is not None:
        certs = payload.certifications if payload.certifications is not None else (profile.certifications or [])
        raw_skills = [
            {
                "name": k,
                "project_evidence_score": v.get("project_evidence", 50) if isinstance(v, dict) else 50,
                "experience_recency_score": v.get("experience_recency", 50) if isinstance(v, dict) else 50
            }
            for k, v in payload.skills_matrix.items()
        ]
        profile.skills_matrix = build_skills_matrix(raw_skills, certs)
        profile.role_fit_matrix = generate_role_fit_matrix(profile.skills_matrix)
    elif payload.certifications is not None and profile.skills_matrix:
        raw_skills = [
            {
                "name": k,
                "project_evidence_score": v.get("project_evidence", 50) if isinstance(v, dict) else 50,
                "experience_recency_score": v.get("experience_recency", 50) if isinstance(v, dict) else 50
            }
            for k, v in profile.skills_matrix.items()
        ]
        profile.skills_matrix = build_skills_matrix(raw_skills, payload.certifications)
        profile.role_fit_matrix = generate_role_fit_matrix(profile.skills_matrix)

    profile.save()

    # Re-index search corpus with updated qualifications
    try:
        index_student_profile(profile)
    except Exception:
        pass

    return _student_to_out_schema(profile)


@router.post("/me", response=StudentProfileOutSchema)
def update_my_profile_post(request, payload: StudentProfileInSchema):
    """Backwards-compatible POST /me route for updating student profile."""
    return update_my_profile_put(request, payload)


# ---------------------------------------------------------
# 3. TECHNICAL SCREENING & ADAPTIVE VIVA TESTING
# ---------------------------------------------------------

@router.get("/generate-test", response={200: TestGenerationOutSchema, 400: dict})
def get_student_screening_test(request, role_title: str):
    """
    Generates a personalized, progressive 5-question technical screening test
    tailored to the student's resume profile, and saves the session in PostgreSQL.
    """
    profile = get_object_or_404(StudentProfile, user=request.auth)
    
    if not profile.skills_matrix:
        return 400, {
            "message": "Your profile has no extracted skills. Please upload and parse your resume first."
        }
        
    try:
        skills_keys = list(profile.skills_matrix.keys())
        
        test_session = AIGateway.generate_adaptive_test(
            role_title=role_title,
            skills=skills_keys,
            projects=profile.projects
        )
        
        db_session = TestSession.objects.create(
            student_profile=profile,
            target_role=role_title,
            questions_data=test_session["questions"]
        )
        
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
            "role_title": role_title,
            "session_id": db_session.id,
            "questions": secured_questions
        }
    except Exception as e:
        return 400, {"message": f"Test Generation Failure: {str(e)}"}


@router.post("/submit-test", response={200: TestGradingOutSchema, 400: dict})
def submit_student_screening_test(request, data: TestSubmissionInSchema = Body(...)):
    """
    Submits, grades, and verifies a student's completed screening test using database-backed sessions.
    Evaluates MCQ time decay, Gemini Viva rubrics, and the non-linear CS plagiarism penalty.
    """
    profile = get_object_or_404(StudentProfile, user=request.auth)
    
    db_session = get_object_or_404(TestSession, id=data.session_id, student_profile=profile)
    
    if db_session.is_completed:
        return 400, {"message": "This test session has already been completed and graded."}
    
    role_fit_data = profile.role_fit_matrix.get(data.target_role)
    if not role_fit_data:
        return 400, {"message": f"You do not have a parsed resume score for the role: {data.target_role}"}
        
    resume_rating = float(role_fit_data.get("score", 0))

    try:
        submitted_answers = [{"id": ans.id, "answer_text": ans.answer_text, "time_taken_seconds": ans.time_taken_seconds} for ans in data.answers]
        
        grading_result = ResilientGrader.evaluate_test_submission(
            submitted_answers=submitted_answers,
            original_questions=db_session.questions_data,
            resume_rating=resume_rating
        )
        
        role_fit_data["verified_confidence_score"] = grading_result["confidence_score"]
        profile.role_fit_matrix[data.target_role] = role_fit_data
        profile.overall_confidence_score = grading_result["confidence_score"]
        
        if grading_result["confidence_score"] >= 60:
            profile.is_verified = True
            
        profile.save()

        # Trigger search corpus and embedding indexing post-grading
        try:
            index_student_profile(profile)
        except Exception:
            pass
        
        db_session.is_completed = True
        db_session.save()

        return 200, {
            "success": True,
            "cognitive_score": grading_result["cognitive_score"],
            "mcq_average": grading_result["mcq_average"],
            "viva_average": grading_result["viva_average"],
            "confidence_score": grading_result["confidence_score"],
            "feedback_log": grading_result["feedback_log"]
        }
    except Exception as e:
        return 400, {"message": f"Grading Engine Failure: {str(e)}"}


# ---------------------------------------------------------
# 4. JOB & INTERNSHIP DISCOVERY FEED
# ---------------------------------------------------------

@router.get("/jobs/feed", response=JobDiscoveryFeedOut)
def get_job_discovery_feed(
    request,
    role_type: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None,
    skill_tag: Optional[str] = None,
    q: Optional[str] = None
):
    """
    Active Openings Feed:
    Displays published job and internship openings with dynamic filters for
    role type, location, remote arrangement, stipend/CTC, and required technical skills.
    Excludes past deadlines automatically.
    """
    qs = JobListing.objects.filter(
        status=JobListing.ListingStatus.PUBLISHED
    ).select_related('company', 'recruiter__user')

    # Exclude expired deadlines
    qs = qs.filter(
        models.Q(application_deadline__gte=timezone.now()) |
        models.Q(application_deadline__isnull=True)
    )

    if role_type:
        qs = qs.filter(role_type=role_type)
    if location:
        qs = qs.filter(location__icontains=location)
    if is_remote is not None:
        qs = qs.filter(is_remote=is_remote)
    if skill_tag:
        qs = qs.filter(required_skills__icontains=skill_tag)
    if q:
        qs = qs.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(company__name__icontains=q)
        )

    qs = qs.order_by('-created_at')

    feed_items = []
    for l in qs:
        feed_items.append(JobDiscoveryItemOut(
            id=l.id,
            title=l.title,
            company_id=l.company.id,
            company_name=l.company.name,
            company_logo=l.company.branding_logo_url or "",
            company_website=l.company.website or "",
            role_type=l.role_type,
            location=l.location,
            is_remote=getattr(l, 'is_remote', False),
            stipend_or_ctc=l.stipend_or_ctc,
            tenure=l.tenure or "",
            open_positions=l.open_positions,
            required_skills=l.required_skills or [],
            eligibility_criteria=l.eligibility_criteria or {},
            application_deadline=getattr(l, 'application_deadline', None),
            description=l.description,
            created_at=l.created_at
        ))

    return JobDiscoveryFeedOut(
        total_jobs=len(feed_items),
        jobs=feed_items
    )


# ---------------------------------------------------------
# 5. NATURAL-LANGUAGE CANDIDATE JOB SEARCH
# ---------------------------------------------------------

@router.post("/jobs/search", response=CandidateJobSearchResponseOut)
def search_jobs_post(request, payload: CandidateJobSearchIn):
    """
    Plain-Language Job Search Bar (POST):
    Matches candidate inquiries (e.g. 'Remote Python Django backend internship paying 40k')
    against published postings using 3-signal fusion (Skill overlap + BGE dense vector + Postgres full-text).
    """
    results = rank_job_listings(
        query=payload.query,
        limit=payload.limit or 10,
        role_type=payload.role_type,
        location=payload.location,
        is_remote=payload.is_remote
    )
    return results


@router.get("/jobs/search", response=CandidateJobSearchResponseOut)
def search_jobs_get(
    request,
    q: str,
    limit: int = 10,
    role_type: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None
):
    """Plain-Language Job Search Bar (GET query parameters)."""
    results = rank_job_listings(
        query=q,
        limit=limit,
        role_type=role_type,
        location=location,
        is_remote=is_remote
    )
    return results


# ---------------------------------------------------------
# 6. ONE-CLICK DIRECT APPLY & CONCURRENCY RESILIENCE
# ---------------------------------------------------------

@router.post("/jobs/{listing_id}/apply", response={201: JobApplicationOut, 400: dict, 404: dict, 409: dict})
def apply_to_job(request, listing_id: int, payload: Optional[JobApplicationApplyIn] = None):
    """
    One-Click Direct Apply Workflow:
    Attaches the candidate's verified skills profile and calculates instant match score.
    Strict Concurrency: Implements select_for_update() row locks on JobListing and StudentProfile
    to prevent double application or stale state transitions, catching OperationalError (409 Conflict).
    Checks application deadlines and creates an automated confirmation notification.
    """
    try:
        with transaction.atomic():
            listing = JobListing.objects.select_for_update().filter(id=listing_id).select_related('company').first()
            if not listing:
                return 404, {"message": "Job listing not found."}
            if listing.status != JobListing.ListingStatus.PUBLISHED:
                return 400, {"message": "This listing is not currently open for applications."}
            if listing.application_deadline and listing.application_deadline < timezone.now():
                return 400, {"message": "The application deadline for this position has passed."}

            student_profile, _ = StudentProfile.objects.select_for_update().get_or_create(user=request.auth)

            existing = JobApplication.objects.filter(listing=listing, student=student_profile).first()
            if existing:
                return 400, {"message": "You have already applied to this listing."}

            # Deterministic skill fitment snapshot
            student_skills = list((student_profile.skills_matrix or {}).keys())
            match_score, _ = compute_job_skill_overlap(student_skills, listing.required_skills or [])

            now_iso = timezone.now().isoformat()
            initial_history = [{
                "status": JobApplication.ApplicationStatus.APPLIED,
                "timestamp": now_iso,
                "note": payload.cover_note if payload and payload.cover_note else "Application submitted."
            }]

            application = JobApplication.objects.create(
                listing=listing,
                student=student_profile,
                status=JobApplication.ApplicationStatus.APPLIED,
                match_score=match_score,
                status_history=initial_history
            )

            # Create immediate candidate notification
            Notification.objects.create(
                user=request.auth,
                title="Application Submitted",
                message=f"You successfully applied for '{listing.title}' at '{listing.company.name}'. Status: Applied.",
                notification_type=Notification.NotificationType.APPLICATION_REVIEW,
                related_application_id=application.id,
                related_listing_id=listing.id
            )

    except OperationalError:
        return 409, {"message": "Database row contention: Operation locked by a concurrent process. Please retry."}

    return 201, _application_to_schema(application)


# ---------------------------------------------------------
# 7. CANDIDATE APPLICATION TRACKER
# ---------------------------------------------------------

@router.get("/applications", response=List[StudentMyApplicationOut])
def get_my_application_tracker(request):
    """
    Candidate Application Tracker:
    Pipeline tracker displaying active applications alongside live status indicators
    (Applied, Under Review, Shortlisted, Interview, Offered, Rejected) and full timeline history.
    """
    student = StudentProfile.objects.filter(user=request.auth).first()
    if not student:
        return []

    apps = JobApplication.objects.filter(student=student).select_related('listing__company').order_by('-created_at')
    
    out = []
    for a in apps:
        comp = a.listing.company
        out.append(StudentMyApplicationOut(
            id=a.id,
            listing_id=a.listing.id,
            listing_title=a.listing.title,
            company_name=comp.name if comp else "",
            company_logo=comp.branding_logo_url if comp else "",
            location=a.listing.location,
            stipend_or_ctc=a.listing.stipend_or_ctc,
            role_type=a.listing.role_type,
            status=a.status,
            match_score=a.match_score,
            recruiter_notes=a.recruiter_notes or "",
            interview_date=getattr(a, 'interview_date', None),
            status_history=a.status_history or [],
            created_at=a.created_at
        ))
    return out


# ---------------------------------------------------------
# 8. REVERSE MATCHING & PERSONALIZED RECOMMENDATIONS
# ---------------------------------------------------------

@router.get("/recommendations", response=PersonalizedRecommendationsFeedOut)
def get_personalized_recommendations(request, limit: int = 10):
    """
    Reverse Matching & Personalized Recommendations:
    Scores all active job postings against the candidate's verified skills_matrix.
    Returns high-fit listings with match percentages, matched skills, and missing skill badges.
    """
    profile, _ = StudentProfile.objects.get_or_create(user=request.auth)
    return compute_personalized_recommendations(profile, limit=limit)


# ---------------------------------------------------------
# 9. SKILL-GAP & UPSKILLING ROADMAP
# ---------------------------------------------------------

@router.get("/skill-gap-roadmap", response=SkillGapRoadmapOut)
def get_skill_gap_roadmap(request, target_role: Optional[str] = None):
    """
    Skill-Gap & Upskilling Roadmap:
    Analyzes market demand frequencies across active postings and benchmark roles.
    Produces prioritized 'Skills to build next' with estimated match percentage boosts
    and actionable engineering project ideas.
    """
    profile, _ = StudentProfile.objects.get_or_create(user=request.auth)
    return compute_skill_gap_roadmap(profile, target_role=target_role)


# ---------------------------------------------------------
# 10. NOTIFICATIONS & DEADLINES HUB
# ---------------------------------------------------------

@router.get("/notifications", response=NotificationsResponseOut)
def get_notifications(request):
    """
    Candidate Notifications Hub:
    Returns live notifications for application reviews, status transitions,
    scheduled interview dates, and system updates.
    """
    notifs = Notification.objects.filter(user=request.auth).order_by('-created_at')
    unread_count = notifs.filter(is_read=False).count()
    total_count = notifs.count()

    items = [
        NotificationItemOut(
            id=n.id,
            title=n.title,
            message=n.message,
            notification_type=n.notification_type,
            related_application_id=n.related_application_id,
            related_listing_id=n.related_listing_id,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in notifs[:50]
    ]

    return NotificationsResponseOut(
        unread_count=unread_count,
        total_count=total_count,
        notifications=items
    )


@router.post("/notifications/read-all", response=dict)
def mark_all_notifications_read(request):
    """Marks all notifications for the authenticated student as read."""
    updated = Notification.objects.filter(user=request.auth, is_read=False).update(is_read=True)
    return {"success": True, "marked_read_count": updated}


@router.post("/notifications/{notification_id}/read", response={200: dict, 404: dict})
def mark_notification_read(request, notification_id: int):
    """Marks an individual notification as read."""
    notif = Notification.objects.filter(id=notification_id, user=request.auth).first()
    if not notif:
        return 404, {"message": "Notification not found."}
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    return 200, {"success": True, "message": "Notification marked as read."}


@router.get("/deadlines", response=DeadlinesHubOut)
def get_deadlines_hub(request):
    """
    Deadlines & Interview Calendar Hub:
    Surfaces upcoming interview dates for active candidate applications
    and approaching deadlines across published listings.
    """
    now = timezone.now()

    # Upcoming interviews for current student
    interviews_qs = JobApplication.objects.filter(
        student__user=request.auth,
        status=JobApplication.ApplicationStatus.INTERVIEW,
        interview_date__gte=now
    ).select_related('listing__company').order_by('interview_date')

    upcoming_interviews = [
        UpcomingInterviewOut(
            application_id=a.id,
            listing_id=a.listing.id,
            listing_title=a.listing.title,
            company_name=a.listing.company.name,
            interview_date=a.interview_date,
            status=a.status
        )
        for a in interviews_qs
    ]

    # Upcoming application deadlines for published job listings
    deadlines_qs = JobListing.objects.filter(
        status=JobListing.ListingStatus.PUBLISHED,
        application_deadline__gte=now
    ).select_related('company').order_by('application_deadline')[:15]

    upcoming_deadlines = [
        UpcomingDeadlineOut(
            listing_id=l.id,
            title=l.title,
            company_name=l.company.name,
            application_deadline=l.application_deadline,
            stipend_or_ctc=l.stipend_or_ctc,
            location=l.location
        )
        for l in deadlines_qs
    ]

    return DeadlinesHubOut(
        upcoming_interviews=upcoming_interviews,
        upcoming_deadlines=upcoming_deadlines
    )


@router.post("/deadlines/check-reminders", response={200: dict})
def trigger_deadline_reminders(request):
    """
    Automated Deadline Reminder Service:
    Scans active published listings expiring within the next 72 hours.
    Dispatches DEADLINE_APPROACHING notifications to matching students
    who have not yet applied.
    """
    from datetime import timedelta
    now = timezone.now()
    window = now + timedelta(hours=72)

    expiring_listings = JobListing.objects.filter(
        status=JobListing.ListingStatus.PUBLISHED,
        application_deadline__gte=now,
        application_deadline__lte=window
    ).select_related('company')

    alerts_created = 0
    for listing in expiring_listings:
        applied_student_ids = set(
            JobApplication.objects.filter(listing=listing).values_list('student_id', flat=True)
        )
        candidates = StudentProfile.objects.exclude(id__in=applied_student_ids).select_related('user')
        req_skills = set(s.lower().strip() for s in (listing.required_skills or []))

        for candidate in candidates:
            cand_skills = set(s.lower().strip() for s in (candidate.skills_matrix or {}).keys())
            overlap = len(req_skills.intersection(cand_skills))
            title_match = any(
                listing.title.lower() in tr.lower() or tr.lower() in listing.title.lower()
                for tr in (candidate.target_roles or [])
            )
            if overlap >= 1 or title_match:
                already_notified = Notification.objects.filter(
                    user=candidate.user,
                    notification_type=Notification.NotificationType.DEADLINE_APPROACHING,
                    related_listing_id=listing.id
                ).exists()
                if not already_notified:
                    time_left = listing.application_deadline - now
                    hours_left = max(1, int(time_left.total_seconds() // 3600))
                    Notification.objects.create(
                        user=candidate.user,
                        title=f"Deadline Approaching: {listing.title}",
                        message=f"Application window for '{listing.title}' at '{listing.company.name}' closes in approximately {hours_left} hours ({listing.application_deadline.strftime('%b %d, %I:%M %p UTC')}). Submit your application now!",
                        notification_type=Notification.NotificationType.DEADLINE_APPROACHING,
                        related_listing_id=listing.id
                    )
                    alerts_created += 1

    return 200, {
        "success": True,
        "expiring_listings_checked": expiring_listings.count(),
        "deadline_reminders_dispatched": alerts_created
    }


# ---------------------------------------------------------
# 11. RECRUITER TALENT SEARCH (POST & GET)
# ---------------------------------------------------------

@router.post("/search", response=RecruiterSearchResponseOut, auth=RecruiterAuth())
def search_students_post(request, payload: RecruiterSearchQueryIn):
    """
    Recruiter Three-Signal Hybrid Search & Ranking (POST):
    Restricted strictly to authenticated recruiters and admins.
    Supports blind: bool toggle for objective skill-first hiring.
    """
    limit = payload.limit or 10
    blind = payload.blind or False
    results = rank_student_profiles(query=payload.query, limit=limit, blind=blind)
    return results


@router.get("/search", response=RecruiterSearchResponseOut, auth=RecruiterAuth())
def search_students_get(request, q: str, limit: int = 10, blind: bool = False):
    """
    Recruiter Three-Signal Hybrid Search & Ranking (GET query param).
    Restricted strictly to authenticated recruiters and admins.
    Supports blind=true query parameter.
    """
    results = rank_student_profiles(query=q, limit=limit, blind=blind)
    return results


@router.get("/", response=List[StudentProfileOutSchema], auth=RecruiterAuth())
def list_students(request):
    """Retrieve all student profiles for recruiters."""
    profiles = StudentProfile.objects.select_related('user').all()
    return [_student_to_out_schema(p) for p in profiles]
