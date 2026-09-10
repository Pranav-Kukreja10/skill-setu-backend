from ninja import Router, Query
from typing import List, Optional
from datetime import datetime
from django.db import transaction, models, OperationalError
from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.security import JWTAuth, RecruiterAuth, StudentAuth, AcademiaAuth
from students.models import StudentProfile, IndustrySector, Notification
from students.services import compute_profile_strength
from recruiters.models import Company, RecruiterProfile, JobListing, JobApplication
from recruiters.schemas import (
    CompanyCreateIn, CompanyUpdateIn, CompanyOut,
    RecruiterProfileUpdateIn, RecruiterProfileOut,
    JobListingCreateIn, JobListingUpdateIn, JobListingOut,
    CandidateJobSearchIn, CandidateJobSearchResponseOut, CandidateJobSearchResultOut,
    JobApplicationApplyIn, JobApplicationStatusUpdateIn, JobApplicationOut, StudentMyApplicationOut,
    ApplicantStudentOut,
    PlacementOverviewOut, BranchWiseReportOut, BranchPlacementStatOut,
    StudentRosterReportOut, StudentPlacementStatusOut, StudentOfferDetail,
    SkillDeficitItemOut, SkillGapAnalysisOut, InDemandSkillItemOut, InDemandSkillsOut, PlacementTrendsOut
)
from recruiters.search import index_job_listing, rank_job_listings, compute_job_skill_overlap

# ---------------------------------------------------------
# ROUTER 1: RECRUITER & COMPANY PROFILE MANAGEMENT
# ---------------------------------------------------------
recruiters_router = Router(tags=["Recruiters"], auth=RecruiterAuth())

@recruiters_router.get("/me", response={200: RecruiterProfileOut, 404: dict})
def get_my_recruiter_profile(request):
    """Retrieve logged-in recruiter's identity, designation, and associated company profile."""
    recruiter, created = RecruiterProfile.objects.get_or_create(
        user=request.auth,
        defaults={"designation": "Talent Acquisition Specialist", "is_company_admin": True}
    )
    
    comp_out = None
    if recruiter.company:
        c = recruiter.company
        comp_out = CompanyOut(
            id=c.id,
            name=c.name,
            registration_number=c.registration_number,
            is_verified=c.is_verified,
            website=c.website,
            industry_id=c.industry_id,
            industry_name=c.industry.name if c.industry else None,
            branding_logo_url=c.branding_logo_url,
            description=c.description,
            headquarters=c.headquarters,
            created_at=c.created_at
        )

    return 200, RecruiterProfileOut(
        id=recruiter.id,
        user_id=request.auth.id,
        username=request.auth.username,
        email=request.auth.email,
        designation=recruiter.designation,
        department=recruiter.department,
        contact_phone=recruiter.contact_phone,
        is_company_admin=recruiter.is_company_admin,
        company=comp_out
    )

@recruiters_router.put("/me", response={200: RecruiterProfileOut, 400: dict})
def update_my_recruiter_profile(request, payload: RecruiterProfileUpdateIn):
    """Update recruiter's designation, department, or contact phone."""
    recruiter, _ = RecruiterProfile.objects.get_or_create(
        user=request.auth,
        defaults={"designation": "Talent Acquisition Specialist", "is_company_admin": True}
    )
    if payload.designation is not None:
        recruiter.designation = payload.designation
    if payload.department is not None:
        recruiter.department = payload.department
    if payload.contact_phone is not None:
        recruiter.contact_phone = payload.contact_phone
    recruiter.save()

    return get_my_recruiter_profile(request)

@recruiters_router.post("/company", response={200: CompanyOut, 400: dict})
def create_or_link_company(request, payload: CompanyCreateIn):
    """Register a new company profile or link existing one, setting caller as company admin."""
    recruiter, _ = RecruiterProfile.objects.get_or_create(
        user=request.auth,
        defaults={"designation": "Talent Acquisition Specialist", "is_company_admin": True}
    )
    
    industry = None
    if payload.industry_id:
        industry = IndustrySector.objects.filter(id=payload.industry_id).first()

    company, created = Company.objects.get_or_create(
        name=payload.name,
        defaults={
            "registration_number": payload.registration_number or "",
            "website": payload.website or "",
            "industry": industry,
            "branding_logo_url": payload.branding_logo_url or "",
            "description": payload.description or "",
            "headquarters": payload.headquarters or ""
        }
    )

    recruiter.company = company
    recruiter.is_company_admin = True
    recruiter.save()

    return 200, CompanyOut(
        id=company.id,
        name=company.name,
        registration_number=company.registration_number,
        is_verified=company.is_verified,
        website=company.website,
        industry_id=company.industry_id,
        industry_name=company.industry.name if company.industry else None,
        branding_logo_url=company.branding_logo_url,
        description=company.description,
        headquarters=company.headquarters,
        created_at=company.created_at
    )

@recruiters_router.get("/company", response={200: CompanyOut, 404: dict})
def get_my_company(request):
    """Retrieve caller's company profile and institutional verification status."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    if not recruiter or not recruiter.company:
        return 404, {"message": "No company profile associated with this recruiter."}
    
    c = recruiter.company
    return 200, CompanyOut(
        id=c.id,
        name=c.name,
        registration_number=c.registration_number,
        is_verified=c.is_verified,
        website=c.website,
        industry_id=c.industry_id,
        industry_name=c.industry.name if c.industry else None,
        branding_logo_url=c.branding_logo_url,
        description=c.description,
        headquarters=c.headquarters,
        created_at=c.created_at
    )

@recruiters_router.put("/company", response={200: CompanyOut, 400: dict, 403: dict})
def update_company(request, payload: CompanyUpdateIn):
    """Update company details, branding, website, and registration (company admin only)."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    if not recruiter or not recruiter.company:
        return 400, {"message": "Recruiter does not belong to any company."}
    if not recruiter.is_company_admin and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "Only company administrators can modify company profile."}

    company = recruiter.company
    if payload.registration_number is not None:
        company.registration_number = payload.registration_number
    if payload.website is not None:
        company.website = payload.website
    if payload.branding_logo_url is not None:
        company.branding_logo_url = payload.branding_logo_url
    if payload.description is not None:
        company.description = payload.description
    if payload.headquarters is not None:
        company.headquarters = payload.headquarters
    if payload.industry_id is not None:
        company.industry = IndustrySector.objects.filter(id=payload.industry_id).first()

    company.save()

    return 200, CompanyOut(
        id=company.id,
        name=company.name,
        registration_number=company.registration_number,
        is_verified=company.is_verified,
        website=company.website,
        industry_id=company.industry_id,
        industry_name=company.industry.name if company.industry else None,
        branding_logo_url=company.branding_logo_url,
        description=company.description,
        headquarters=company.headquarters,
        created_at=company.created_at
    )


# ---------------------------------------------------------
# ROUTER 2: JOB & INTERNSHIP POSTING ENGINE
# ---------------------------------------------------------
listings_router = Router(tags=["Job & Internship Listings"])

def _listing_to_schema(listing: JobListing) -> JobListingOut:
    apps_count = getattr(listing, 'apps_count', None)
    if apps_count is None:
        apps_count = listing.applications.count()
    return JobListingOut(
        id=listing.id,
        company_id=listing.company.id,
        company_name=listing.company.name,
        company_logo=listing.company.branding_logo_url or "",
        company_website=listing.company.website or "",
        company_headquarters=listing.company.headquarters or "",
        recruiter_id=listing.recruiter.id,
        recruiter_name=listing.recruiter.user.username,
        title=listing.title,
        role_type=listing.role_type,
        status=listing.status,
        stipend_or_ctc=listing.stipend_or_ctc,
        location=listing.location,
        is_remote=getattr(listing, 'is_remote', False),
        application_deadline=getattr(listing, 'application_deadline', None),
        tenure=listing.tenure or "",
        open_positions=listing.open_positions,
        required_skills=listing.required_skills or [],
        eligibility_criteria=listing.eligibility_criteria or {},
        description=listing.description,
        applications_count=apps_count,
        created_at=listing.created_at,
        updated_at=listing.updated_at
    )

def dispatch_new_opportunity_notifications(listing: JobListing) -> int:
    """
    Automated Opportunity Notification Dispatcher:
    Scans active student profiles and matches them against the published listing.
    If a student has a skill overlap (>= 25%) or matching target roles, sends a
    NEW_OPPORTUNITY notification.
    """
    if listing.status != JobListing.ListingStatus.PUBLISHED:
        return 0

    req_skills = [s.lower().strip() for s in (listing.required_skills or [])]
    students = StudentProfile.objects.select_related('user').all()
    count = 0
    for s in students:
        already_notified = Notification.objects.filter(
            user=s.user,
            notification_type=Notification.NotificationType.NEW_OPPORTUNITY,
            related_listing_id=listing.id
        ).exists()
        if already_notified:
            continue

        cand_skills = [sk.lower().strip() for sk in (s.skills_matrix or {}).keys()]
        overlap, _ = compute_job_skill_overlap(cand_skills, req_skills)
        title_match = any(
            listing.title.lower() in tr.lower() or tr.lower() in listing.title.lower()
            for tr in (s.target_roles or [])
        )
        if overlap >= 0.25 or title_match:
            Notification.objects.create(
                user=s.user,
                title=f"New Opportunity: {listing.title} at {listing.company.name}",
                message=f"A new {listing.role_type.replace('_', ' ').title()} matching your skill profile was just posted: '{listing.title}' ({listing.stipend_or_ctc}, {listing.location}). Apply now!",
                notification_type=Notification.NotificationType.NEW_OPPORTUNITY,
                related_listing_id=listing.id
            )
            count += 1
    return count

@listings_router.post("/", response={201: JobListingOut, 400: dict}, auth=RecruiterAuth())
def create_job_listing(request, payload: JobListingCreateIn):
    """
    Create a new job or internship listing (defaults to DRAFT).
    Automatically indexes denormalized search_corpus and dense BGE vector.
    Dispatches automated opportunity notifications if published immediately.
    """
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    if not recruiter or not recruiter.company:
        return 400, {"message": "You must register or join a company before creating listings."}

    target_status = getattr(payload, 'status', None) or JobListing.ListingStatus.DRAFT

    listing = JobListing.objects.create(
        recruiter=recruiter,
        company=recruiter.company,
        title=payload.title,
        role_type=payload.role_type or JobListing.RoleType.FULL_TIME,
        status=target_status,
        stipend_or_ctc=payload.stipend_or_ctc,
        location=payload.location,
        is_remote=payload.is_remote or False,
        application_deadline=payload.application_deadline,
        tenure=payload.tenure or "",
        open_positions=payload.open_positions or 1,
        required_skills=payload.required_skills or [],
        eligibility_criteria=payload.eligibility_criteria or {},
        description=payload.description
    )

    # Index embedding and search corpus
    index_job_listing(listing)

    if target_status == JobListing.ListingStatus.PUBLISHED:
        dispatch_new_opportunity_notifications(listing)

    return 201, _listing_to_schema(listing)

@listings_router.get("/my-listings", response=List[JobListingOut], auth=RecruiterAuth())
def get_my_company_listings(request):
    """Fetch all listings created by the recruiter's company across all lifecycle statuses."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    if not recruiter or not recruiter.company:
        return []
    listings = JobListing.objects.filter(company=recruiter.company).select_related('company', 'recruiter__user').annotate(
        apps_count=models.Count('applications')
    )
    return [_listing_to_schema(l) for l in listings]

# Candidate NLP Job Search (Declared before /{listing_id} so /search is not caught as a listing ID)
@listings_router.post("/search", response=CandidateJobSearchResponseOut, auth=StudentAuth())
def candidate_job_search_post(request, payload: CandidateJobSearchIn):
    """
    Candidate NLP Job Search (POST):
    Natural language query matching candidates against active job listings & hiring recruiters.
    Uses three-signal fusion: Deterministic Skill Overlap (40%) + BGE Dense Semantic (40%) + Full-Text Rank (20%).
    """
    limit = payload.limit or 10
    results = rank_job_listings(
        query=payload.query,
        limit=limit,
        role_type=payload.role_type,
        location=payload.location
    )
    return results

@listings_router.get("/search", response=CandidateJobSearchResponseOut, auth=StudentAuth())
def candidate_job_search_get(
    request,
    q: str,
    limit: int = 10,
    role_type: Optional[str] = None,
    location: Optional[str] = None
):
    """
    Candidate NLP Job Search (GET query parameter).
    """
    results = rank_job_listings(
        query=q,
        limit=limit,
        role_type=role_type,
        location=location
    )
    return results

@listings_router.get("/", response=List[JobListingOut], auth=JWTAuth())
def list_published_listings(
    request,
    role_type: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None,
    sector_id: Optional[int] = None
):
    """Public candidate endpoint to browse and filter published job & internship postings."""
    qs = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED).select_related('company', 'recruiter__user').annotate(
        apps_count=models.Count('applications')
    )
    if role_type:
        qs = qs.filter(role_type=role_type)
    if location:
        qs = qs.filter(location__icontains=location)
    if is_remote is not None:
        qs = qs.filter(is_remote=is_remote)
    if sector_id:
        qs = qs.filter(company__industry_id=sector_id)

    return [_listing_to_schema(l) for l in qs]

@listings_router.get("/{listing_id}", response={200: JobListingOut, 404: dict}, auth=JWTAuth())
def get_job_listing(request, listing_id: int):
    """Fetch full details of a specific job or internship listing."""
    listing = JobListing.objects.filter(id=listing_id).select_related('company', 'recruiter__user').first()
    if not listing:
        return 404, {"message": "Job listing not found."}
    return 200, _listing_to_schema(listing)

@listings_router.put("/{listing_id}", response={200: JobListingOut, 400: dict, 403: dict, 404: dict}, auth=RecruiterAuth())
def update_job_listing(request, listing_id: int, payload: JobListingUpdateIn):
    """Edit listing metadata. Re-generates search corpus and BGE vector index."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).select_related('company', 'recruiter__user').first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "You can only edit listings from your own company."}

    was_published = (listing.status == JobListing.ListingStatus.PUBLISHED)
    if payload.status is not None:
        listing.status = payload.status
    if payload.title is not None:
        listing.title = payload.title
    if payload.role_type is not None:
        listing.role_type = payload.role_type
    if payload.stipend_or_ctc is not None:
        listing.stipend_or_ctc = payload.stipend_or_ctc
    if payload.location is not None:
        listing.location = payload.location
    if payload.is_remote is not None:
        listing.is_remote = payload.is_remote
    if payload.application_deadline is not None:
        listing.application_deadline = payload.application_deadline
    if payload.tenure is not None:
        listing.tenure = payload.tenure
    if payload.open_positions is not None:
        listing.open_positions = payload.open_positions
    if payload.required_skills is not None:
        listing.required_skills = payload.required_skills
    if payload.eligibility_criteria is not None:
        listing.eligibility_criteria = payload.eligibility_criteria
    if payload.description is not None:
        listing.description = payload.description

    listing.save()
    index_job_listing(listing)

    if listing.status == JobListing.ListingStatus.PUBLISHED and not was_published:
        dispatch_new_opportunity_notifications(listing)

    return 200, _listing_to_schema(listing)

@listings_router.post("/{listing_id}/publish", response={200: JobListingOut, 400: dict, 404: dict}, auth=RecruiterAuth())
def publish_listing(request, listing_id: int):
    """Publish a draft listing to campus candidates and notify matching applicants."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).select_related('company', 'recruiter__user').first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "Permission denied."}

    listing.status = JobListing.ListingStatus.PUBLISHED
    listing.save()
    index_job_listing(listing)
    dispatch_new_opportunity_notifications(listing)
    return 200, _listing_to_schema(listing)

@listings_router.post("/{listing_id}/archive", response={200: JobListingOut, 400: dict, 404: dict}, auth=RecruiterAuth())
def archive_listing(request, listing_id: int):
    """Archive a listing, hiding it from candidate search."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).select_related('company', 'recruiter__user').first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "Permission denied."}

    listing.status = JobListing.ListingStatus.ARCHIVED
    listing.save()
    return 200, _listing_to_schema(listing)

@listings_router.post("/{listing_id}/close", response={200: JobListingOut, 400: dict, 404: dict}, auth=RecruiterAuth())
def close_listing(request, listing_id: int):
    """Close applications for a job listing."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).select_related('company', 'recruiter__user').first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "Permission denied."}

    listing.status = JobListing.ListingStatus.CLOSED
    listing.save()
    return 200, _listing_to_schema(listing)

@listings_router.delete("/{listing_id}", response={200: dict, 403: dict, 404: dict}, auth=RecruiterAuth())
def delete_listing(request, listing_id: int):
    """Delete a listing."""
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "Permission denied."}

    listing.delete()
    return 200, {"success": True, "message": "Listing deleted successfully."}


# ---------------------------------------------------------
# ROUTER 3: APPLICATION LIFECYCLE & CANDIDATE REVIEW
# ---------------------------------------------------------
applications_router = Router(tags=["Application Lifecycle"])

def _application_to_schema(app: JobApplication, blind: bool = False) -> JobApplicationOut:
    student = app.student
    user = student.user
    
    username_val = f"Candidate #{student.id}" if blind else user.username
    email_val = "[REDACTED]" if blind else user.email
    bio_val = "[REDACTED]" if (blind and student.bio) else student.bio
    inst_val = "[REDACTED]" if (blind and student.institution) else (student.institution or None)
    github_val = "[REDACTED]" if blind else (getattr(student, 'github_url', "") or "")
    p_strength = compute_profile_strength(student)[0]

    student_schema = ApplicantStudentOut(
        id=user.id,
        student_profile_id=student.id,
        username=username_val,
        email=email_val,
        bio=bio_val,
        current_designation=getattr(student, 'current_designation', "") or "",
        experience_years=getattr(student, 'experience_years', 0.0) or 0.0,
        institution=inst_val,
        department=student.department or None,
        github_url=github_val,
        certifications=getattr(student, 'certifications', []) or [],
        profile_strength_score=p_strength,
        skills_matrix=student.skills_matrix or {},
        raw_extracted_skills=student.raw_extracted_skills or [],
        role_fit_matrix=student.role_fit_matrix or {},
        target_roles=student.target_roles or [],
        overall_confidence_score=student.overall_confidence_score,
        is_verified=student.is_verified,
        placement_status=student.placement_status,
        is_blind=blind
    )

    return JobApplicationOut(
        id=app.id,
        listing_id=app.listing.id,
        listing_title=app.listing.title,
        company_name=app.listing.company.name,
        student=student_schema,
        status=app.status,
        match_score=app.match_score,
        recruiter_notes=app.recruiter_notes or "",
        interview_date=getattr(app, 'interview_date', None),
        status_history=app.status_history or [],
        created_at=app.created_at,
        updated_at=app.updated_at
    )

@applications_router.post("/listings/{listing_id}/apply", response={201: JobApplicationOut, 400: dict, 404: dict, 409: dict}, auth=StudentAuth())
def apply_to_listing(request, listing_id: int, payload: Optional[JobApplicationApplyIn] = None):
    """
    Student submits application to a job or internship listing.
    Calculates instant match score between candidate's skills and listing requirements.
    ACID row-locking and OperationalError handling.
    """
    from django.utils import timezone
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

            # Initial application notification for student
            Notification.objects.create(
                user=request.auth,
                title="Application Submitted",
                message=f"You successfully applied for '{listing.title}' at '{listing.company.name}'. Status: Applied.",
                notification_type=Notification.NotificationType.APPLICATION_REVIEW,
                related_application_id=application.id,
                related_listing_id=listing.id
            )

    except OperationalError:
        return 409, {"message": "Database row contention: Operation locked by a concurrent reviewer. Please retry."}

    return 201, _application_to_schema(application)

@applications_router.get("/listings/{listing_id}/applications", response={200: List[JobApplicationOut], 403: dict, 404: dict}, auth=RecruiterAuth())
def get_listing_applications(request, listing_id: int, blind: bool = False):
    """
    Recruiter candidate review pipeline:
    Lists all applicants for a listing, ranked by match score and verification.
    Supports blind=True toggle for anonymized, skill-first hiring.
    """
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    listing = JobListing.objects.filter(id=listing_id).first()
    if not listing:
        return 404, {"message": "Listing not found."}
    if listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "You can only view applications for your company's listings."}

    applications = JobApplication.objects.filter(listing=listing).select_related(
        'student__user', 'listing__company'
    ).order_by('-match_score', '-student__is_verified', '-student__overall_confidence_score')

    return 200, [_application_to_schema(app, blind=blind) for app in applications]

@applications_router.post("/{application_id}/status", response={200: JobApplicationOut, 400: dict, 403: dict, 404: dict, 409: dict}, auth=RecruiterAuth())
def update_application_status(request, application_id: int, payload: JobApplicationStatusUpdateIn):
    """
    Recruiter transitions candidate application status:
    APPLIED -> UNDER_REVIEW -> SHORTLISTED -> INTERVIEW -> OFFERED -> REJECTED.
    
    ACID & Strict Concurrency:
    Uses select_for_update() row locks on JobApplication and StudentProfile.
    
    Unified Ecosystem Hook:
    When transitioned to OFFERED, StudentProfile.placement_status is atomically synchronized to PLACED.
    Triggers student Notification automatically with interview details and feedback notes.
    """
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    target_status = payload.status.upper()
    valid_statuses = [choice[0] for choice in JobApplication.ApplicationStatus.choices]
    if target_status not in valid_statuses:
        return 400, {"message": f"Invalid status '{payload.status}'. Must be one of {valid_statuses}."}

    try:
        # Strict ACID row-locking
        with transaction.atomic():
            application = JobApplication.objects.select_for_update().select_related(
                'listing__company', 'student__user'
            ).filter(id=application_id).first()

            if not application:
                return 404, {"message": "Application not found."}
            if application.listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
                return 403, {"message": "You can only manage applications for your company."}

            # Row-lock the student profile
            student = StudentProfile.objects.select_for_update().get(id=application.student_id)

            application.status = target_status
            if payload.note:
                application.recruiter_notes = payload.note
            if payload.interview_date is not None:
                application.interview_date = payload.interview_date

            # Append to audit trail
            history = list(application.status_history or [])
            history.append({
                "status": target_status,
                "timestamp": datetime.now().isoformat(),
                "updated_by": request.auth.username,
                "note": payload.note or "",
                "interview_date": payload.interview_date.isoformat() if payload.interview_date else None
            })
            application.status_history = history
            application.save()

            # Automatic placement ecosystem hook
            if target_status == JobApplication.ApplicationStatus.OFFERED:
                student.placement_status = StudentProfile.PlacementStatus.PLACED
                student.save(update_fields=['placement_status'])

            # Automated Student Notification Hook
            notif_type = (
                Notification.NotificationType.INTERVIEW_SCHEDULED
                if target_status == JobApplication.ApplicationStatus.INTERVIEW
                else Notification.NotificationType.STATUS_CHANGE
            )
            sched_info = f" Scheduled interview: {payload.interview_date.strftime('%b %d, %Y %I:%M %p UTC')}." if payload.interview_date else ""
            note_info = f" Note: '{payload.note}'" if payload.note else ""
            Notification.objects.create(
                user=student.user,
                title=f"Application Stage: {target_status.replace('_', ' ').title()}",
                message=f"Your application for '{application.listing.title}' at '{application.listing.company.name}' has advanced to {target_status.replace('_', ' ').title()}.{sched_info}{note_info}",
                notification_type=notif_type,
                related_application_id=application.id,
                related_listing_id=application.listing.id
            )

    except OperationalError:
        return 409, {"message": "Database row contention: Operation locked by a concurrent reviewer. Please retry."}

    return 200, _application_to_schema(application)

@applications_router.get("/my-applications", response=List[StudentMyApplicationOut], auth=StudentAuth())
def get_my_applications(request):
    """Candidate portal: track active applications, current stages, and recruiter feedback."""
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
# ROUTER 4: IDEMPOTENT INSTITUTIONAL PLACEMENT REPORTING
# (Now cleanly maintained in institutions.api; re-exported for backwards compatibility)
# ---------------------------------------------------------
from institutions.api import placement_router

