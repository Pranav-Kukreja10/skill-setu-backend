from ninja import Router, Query
from typing import List, Optional
from datetime import datetime
from django.db import transaction, models, OperationalError
from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.security import JWTAuth, RecruiterAuth, StudentAuth, AcademiaAuth
from students.models import StudentProfile, IndustrySector, Notification
from students.services import compute_profile_strength
from recruiters.models import Company, RecruiterProfile, JobListing, JobApplication, LearningProgram
from recruiters.schemas import (
    CompanyCreateIn, CompanyUpdateIn, CompanyOut,
    RecruiterProfileUpdateIn, RecruiterProfileOut,
    RecruiterSettingsOutSchema, RecruiterSettingsUpdateIn,
    JobListingCreateIn, JobListingUpdateIn, JobListingOut,
    CandidateJobSearchIn, CandidateJobSearchResponseOut, CandidateJobSearchResultOut,
    JobApplicationApplyIn, JobApplicationStatusUpdateIn, JobApplicationOut, StudentMyApplicationOut,
    ApplicantStudentOut, InternshipProgressUpdateIn, InternshipMilestoneLogIn,
    LearningProgramOut, LearningProgramCreateIn,
    LearningProgressUpdateIn, LearningProgressUpdateOut,
    LearningProgramRecommendationItem, LearningRecommendationsResponseOut,
    PlacementOverviewOut, BranchWiseReportOut, BranchPlacementStatOut,
    StudentRosterReportOut, StudentPlacementStatusOut, StudentOfferDetail,
    SkillDeficitItemOut, SkillGapAnalysisOut, InDemandSkillItemOut, InDemandSkillsOut, PlacementTrendsOut
)
from students.recommendations import compute_skill_gap_roadmap
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

    comp_id = recruiter.company_id
    active_jobs = JobListing.objects.filter(company_id=comp_id, status=JobListing.ListingStatus.PUBLISHED).count() if comp_id else 0
    shortlisted = JobApplication.objects.filter(listing__company_id=comp_id, status=JobApplication.ApplicationStatus.SHORTLISTED).count() if comp_id else 0
    interviews = JobApplication.objects.filter(listing__company_id=comp_id, status=JobApplication.ApplicationStatus.INTERVIEW).count() if comp_id else 0
    total_apps = JobApplication.objects.filter(listing__company_id=comp_id).count() if comp_id else 0
    verified_apps = JobApplication.objects.filter(listing__company_id=comp_id, student__is_verified=True).count() if comp_id else 0
    pass_rate = round((verified_apps / total_apps * 100), 1) if total_apps > 0 else 85.0

    metrics_dict = {
        "active_listings_count": active_jobs,
        "shortlisted_talent_count": shortlisted,
        "interviews_scheduled_count": interviews,
        "total_applicants_count": total_apps,
        "verification_pass_rate": pass_rate,
    }

    return 200, RecruiterProfileOut(
        id=recruiter.id,
        user_id=request.auth.id,
        username=request.auth.username,
        email=request.auth.email,
        first_name=getattr(request.auth, 'first_name', '') or '',
        last_name=getattr(request.auth, 'last_name', '') or '',
        avatar_url=getattr(request.auth, 'avatar_url', None),
        designation=recruiter.designation,
        department=recruiter.department,
        contact_phone=recruiter.contact_phone,
        is_company_admin=recruiter.is_company_admin,
        company=comp_out,
        preferences=recruiter.get_preferences(),
        metrics=metrics_dict
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

@recruiters_router.get("/me/settings", response={200: RecruiterSettingsOutSchema, 400: dict})
def get_my_recruiter_settings(request):
    """
    Retrieve authenticated recruiter's workflow, blind screening, and alert preferences.
    """
    recruiter, _ = RecruiterProfile.objects.get_or_create(
        user=request.auth,
        defaults={"designation": "Talent Acquisition Specialist", "is_company_admin": True}
    )
    return 200, recruiter.get_preferences()

@recruiters_router.put("/me/settings", response={200: RecruiterSettingsOutSchema, 400: dict})
@recruiters_router.patch("/me/settings", response={200: RecruiterSettingsOutSchema, 400: dict})
def update_my_recruiter_settings(request, payload: RecruiterSettingsUpdateIn):
    """
    Update recruiter's granular preferences:
    - common: theme, language, timezone, email/in-app alerts, accessibility
    - candidate_screening: default blind screening, minimum engineering score filter, NHEQF level
    - hiring_workflow: auto-advance high match candidates, review assignment, alert frequency
    - branding: diversity employer badge, public company profile visibility
    """
    recruiter, _ = RecruiterProfile.objects.get_or_create(
        user=request.auth,
        defaults={"designation": "Talent Acquisition Specialist", "is_company_admin": True}
    )
    current = recruiter.get_preferences()
    if payload.common is not None:
        current["common"].update(payload.common)
    if payload.candidate_screening is not None:
        current["candidate_screening"].update(payload.candidate_screening)
    if payload.hiring_workflow is not None:
        current["hiring_workflow"].update(payload.hiring_workflow)
    if payload.branding is not None:
        current["branding"].update(payload.branding)
    recruiter.preferences = current
    recruiter.save(update_fields=['preferences'])
    return 200, current

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
    apps_count = getattr(listing, 'applications_count', None)
    if apps_count is None:
        apps_count = getattr(listing, 'apps_count', None)
    if apps_count is None and hasattr(listing, 'applications'):
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
        description=listing.description,
        is_diversity_drive=getattr(listing, 'is_diversity_drive', False),
        target_gender=getattr(listing, 'target_gender', "ALL") or "ALL",
        dei_initiatives=getattr(listing, 'dei_initiatives', []) or [],
        min_nheqf_level=getattr(listing, 'min_nheqf_level', 'LEVEL_4_5') or 'LEVEL_4_5',
        applications_count=apps_count or 0,
        created_at=listing.created_at,
        updated_at=listing.updated_at
    )

def dispatch_new_opportunity_notifications(listing: JobListing) -> int:
    """
    Automated Opportunity Notification Dispatcher:
    Scans active student profiles and matches them against the published listing.
    If a student has a skill overlap (>= 25%) or matching target roles, sends a
    NEW_OPPORTUNITY notification.
    Uses bulk queries to completely eliminate N+1 overhead.
    """
    if listing.status != JobListing.ListingStatus.PUBLISHED:
        return 0

    req_skills = [s.lower().strip() for s in (listing.required_skills or [])]
    students = StudentProfile.objects.select_related('user').all()

    # Pre-fetch all user IDs who have already received this notification in 1 query
    already_notified_user_ids = set(
        Notification.objects.filter(
            notification_type=Notification.NotificationType.NEW_OPPORTUNITY,
            related_listing_id=listing.id
        ).values_list('user_id', flat=True)
    )

    notifications_to_create = []
    for s in students:
        if s.user_id in already_notified_user_ids:
            continue

        cand_skills = [sk.lower().strip() for sk in (s.skills_matrix or {}).keys()]
        overlap, _ = compute_job_skill_overlap(cand_skills, req_skills)
        title_match = any(
            listing.title.lower() in tr.lower() or tr.lower() in listing.title.lower()
            for tr in (s.target_roles or [])
        )
        if overlap >= 0.25 or title_match:
            notifications_to_create.append(Notification(
                user=s.user,
                title=f"New Opportunity: {listing.title} at {listing.company.name}",
                message=f"A new {listing.role_type.replace('_', ' ').title()} matching your skill profile was just posted: '{listing.title}' ({listing.stipend_or_ctc}, {listing.location}). Apply now!",
                notification_type=Notification.NotificationType.NEW_OPPORTUNITY,
                related_listing_id=listing.id
            ))

    if notifications_to_create:
        Notification.objects.bulk_create(notifications_to_create)

    return len(notifications_to_create)

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
        description=payload.description,
        is_diversity_drive=payload.is_diversity_drive or False,
        target_gender=payload.target_gender or "ALL",
        dei_initiatives=payload.dei_initiatives or [],
        min_nheqf_level=payload.min_nheqf_level or 'LEVEL_4_5'
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
    if payload.min_nheqf_level is not None:
        listing.min_nheqf_level = payload.min_nheqf_level
    if payload.is_diversity_drive is not None:
        listing.is_diversity_drive = payload.is_diversity_drive
    if payload.target_gender is not None:
        listing.target_gender = payload.target_gender
    if payload.dei_initiatives is not None:
        listing.dei_initiatives = payload.dei_initiatives

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
        internship_status=app.internship_status,
        mentor_name=app.mentor_name or "",
        mentor_designation=app.mentor_designation or "",
        mentor_feedback=app.mentor_feedback or "",
        mentor_rating=app.mentor_rating,
        completion_certificate_url=app.completion_certificate_url or "",
        internship_report_url=app.internship_report_url or "",
        weekly_progress_logs=app.weekly_progress_logs or [],
        created_at=app.created_at,
        updated_at=app.updated_at
    )

@applications_router.post("/listings/{listing_id}/apply", response={201: JobApplicationOut, 200: JobApplicationOut, 400: dict, 404: dict, 409: dict}, auth=StudentAuth())
def apply_to_listing(request, listing_id: int, payload: Optional[JobApplicationApplyIn] = None):
    """
    Student submits application to a job or internship listing (Idempotent).
    Calculates instant match score between candidate's skills and listing requirements.
    ACID row-locking and OperationalError handling.
    Safely returns 200 OK on network retry if application already exists.
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
                # Idempotent return: application already exists
                return 200, _application_to_schema(existing)

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

            # Idempotency check: if application is already in target_status and no new note is provided, return existing state
            if application.status == target_status and (not payload.note or payload.note == application.recruiter_notes):
                return 200, _application_to_schema(application)

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
            internship_status=a.internship_status,
            mentor_name=a.mentor_name or "",
            mentor_designation=a.mentor_designation or "",
            mentor_feedback=a.mentor_feedback or "",
            mentor_rating=a.mentor_rating,
            completion_certificate_url=a.completion_certificate_url or "",
            internship_report_url=a.internship_report_url or "",
            weekly_progress_logs=a.weekly_progress_logs or [],
            created_at=a.created_at
        ))
    return out


@applications_router.patch("/{application_id}/internship-progress", response={200: JobApplicationOut, 400: dict, 403: dict, 404: dict}, auth=RecruiterAuth())
def update_internship_progress(request, application_id: int, payload: InternshipProgressUpdateIn):
    """
    Recruiter & Mentor Internship Progress Supervision (PS Requirement):
    Updates live internship lifecycle status, logs mentor qualitative review remarks,
    sets 1-5 performance rating, and attaches verified completion certificate URL or report.
    When marked COMPLETED, automatically records verified internship into candidate's digital portfolio.
    """
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    application = JobApplication.objects.select_related('listing__company', 'student__user').filter(id=application_id).first()
    if not application:
        return 404, {"message": "Application not found."}
    if application.listing.company_id != recruiter.company_id and request.auth.role != User.Role.ADMIN:
        return 403, {"message": "You can only manage internships for your company."}

    valid_statuses = [choice[0] for choice in JobApplication.InternshipStatus.choices]
    if payload.internship_status not in valid_statuses:
        return 400, {"message": f"Invalid internship status '{payload.internship_status}'. Must be one of {valid_statuses}."}

    application.internship_status = payload.internship_status
    if payload.mentor_name is not None:
        application.mentor_name = payload.mentor_name
    if payload.mentor_designation is not None:
        application.mentor_designation = payload.mentor_designation
    if payload.mentor_feedback is not None:
        application.mentor_feedback = payload.mentor_feedback
    if payload.mentor_rating is not None:
        application.mentor_rating = max(1.0, min(5.0, float(payload.mentor_rating)))
    if payload.completion_certificate_url is not None:
        application.completion_certificate_url = payload.completion_certificate_url
    if payload.internship_report_url is not None:
        application.internship_report_url = payload.internship_report_url
    application.save()

    # Automatic Digital Portfolio Hook upon Completion
    if payload.internship_status == JobApplication.InternshipStatus.COMPLETED:
        student = application.student
        internships = list(student.internships or [])
        already_added = any(
            i.get('company') == application.listing.company.name and i.get('role') == application.listing.title
            for i in internships
        )
        if not already_added:
            internships.append({
                "company": application.listing.company.name,
                "role": application.listing.title,
                "duration": application.listing.tenure or "Internship",
                "mentor_name": application.mentor_name or "",
                "mentor_designation": application.mentor_designation or "",
                "mentor_feedback": application.mentor_feedback or "",
                "mentor_rating": application.mentor_rating or 5.0,
                "certificate_url": application.completion_certificate_url or "",
                "report_url": application.internship_report_url or "",
                "completed_at": datetime.now().isoformat()
            })
            student.internships = internships
            student.save(update_fields=['internships'])

        # Real-time alert to candidate
        Notification.objects.create(
            user=student.user,
            title=f"Internship Completed: {application.listing.title}",
            message=f"Congratulations! Your internship at '{application.listing.company.name}' has been marked Completed with a rating of {application.mentor_rating or 5.0}/5.0. Verified credential added to your Digital Portfolio.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=application.id,
            related_listing_id=application.listing.id
        )

    return 200, _application_to_schema(application)


# ---------------------------------------------------------
# ROUTER 4: INDUSTRY LEARNING PROGRAMS & COLLABORATION INITIATIVES
# ---------------------------------------------------------
programs_router = Router(tags=["Industry Learning Programs & Collaboration"])

def _resolve_request_user(request):
    user = getattr(request, 'auth', None)
    if user:
        return user
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        try:
            import jwt
            from django.conf import settings
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return User.objects.filter(id=payload.get("user_id")).first()
        except Exception:
            pass
    return None

def _parse_program_meta(program: LearningProgram, student_profile: Optional[StudentProfile] = None):
    text = program.description or ""
    modules = []
    if "Modules:" in text:
        parts = text.split("Modules:")[1].strip().split("\n")
        for p in parts:
            clean_p = p.strip()
            if clean_p and (clean_p[0].isdigit() or clean_p.startswith("-")):
                dot_idx = clean_p.find(".")
                if dot_idx != -1 and dot_idx < 4:
                    clean_p = clean_p[dot_idx + 1:].strip()
                elif clean_p.startswith("-"):
                    clean_p = clean_p[1:].strip()
                if clean_p:
                    modules.append(clean_p)
    if not modules:
        skills = program.skills_covered or []
        for i, s in enumerate(skills[:5], 1):
            modules.append(f"Module {i}: Advanced Applied {s}")
        if not modules:
            modules = [
                "Module 1: Foundations & Architecture",
                "Module 2: Core Practical Workflows",
                "Module 3: Advanced Implementation",
                "Module 4: Industry Capstone Project"
            ]

    skills_lower = [s.lower().strip() for s in (program.skills_covered or [])]
    if any(s in skills_lower for s in ['figma', 'ui/ux design', 'ui/ux', 'ui design', 'ux design', 'wireframing', 'design systems', 'wcag accessibility', 'prototyping', 'motion design', 'interaction design']):
        domain = "Design & Creative Arts"
    elif any(s in skills_lower for s in ['business analysis', 'bpmn workflows', 'market research', 'agile & scrum', 'project management', 'supply chain', 'operations management', 'crm systems', 'salesforce']):
        domain = "Business & Management"
    elif any(s in skills_lower for s in ['tally prime', 'gst compliance', 'statutory auditing', 'taxation', 'tds', 'financial modeling', 'dcf valuation', 'financial reporting', 'cost accounting', 'quantitative analysis']):
        domain = "Commerce & Finance"
    elif program.company and program.company.industry:
        ind_name = program.company.industry.name
        if ind_name == "Design & Creative Arts":
            domain = "Design & Creative Arts"
        elif ind_name in ["Commerce & Accounting", "Finance & Banking"]:
            domain = "Commerce & Finance"
        elif ind_name == "Business & Management":
            domain = "Business & Management"
        else:
            domain = "Engineering & Tech"
    else:
        domain = "Engineering & Tech"

    prog_type_str = str(program.program_type).upper()
    if "CERTIFICATION" in prog_type_str or "FELLOWSHIP" in program.title.upper():
        level = "Advanced"
    elif "WORKSHOP" in prog_type_str:
        level = "Intermediate"
    elif "TRAINING" in prog_type_str:
        level = "Beginner to Intermediate"
    else:
        level = "Intermediate"

    rating = round(4.7 + (program.id % 4) * 0.08, 1)

    is_enrolled = False
    user_progress = 0
    completed_modules = []
    if student_profile:
        if program.enrolled_students.filter(id=student_profile.id).exists():
            is_enrolled = True
        pref = student_profile.preferences or {}
        course_prog = pref.get("course_progress", {}).get(str(program.id), {})
        if course_prog:
            is_enrolled = True
            user_progress = int(course_prog.get("progress", 0))
            completed_modules = course_prog.get("completed_modules", [])

    return {
        "domain": domain,
        "modules": modules,
        "level": level,
        "rating": rating,
        "is_enrolled": is_enrolled,
        "user_progress": user_progress,
        "completed_modules": completed_modules
    }

def _program_to_schema(program: LearningProgram, student_profile: Optional[StudentProfile] = None) -> LearningProgramOut:
    s_count = getattr(program, 'enrolled_students_count', None)
    if s_count is None:
        s_count = program.enrolled_students.count()
    f_count = getattr(program, 'enrolled_faculty_count', None)
    if f_count is None:
        f_count = program.enrolled_faculty.count()

    meta = _parse_program_meta(program, student_profile)

    return LearningProgramOut(
        id=program.id,
        company_id=program.company.id,
        company_name=program.company.name,
        company_logo=program.company.branding_logo_url or "",
        title=program.title,
        program_type=program.program_type,
        target_audience=program.target_audience,
        description=program.description,
        skills_covered=program.skills_covered or [],
        instructor_or_mentor=program.instructor_or_mentor or "",
        duration=program.duration,
        mode=program.mode,
        registration_deadline=program.registration_deadline,
        start_date=program.start_date,
        is_certified=program.is_certified,
        branding_banner_url=program.branding_banner_url or "",
        enrolled_students_count=s_count,
        enrolled_faculty_count=f_count,
        created_at=program.created_at,
        domain=meta["domain"],
        modules=meta["modules"],
        rating=meta["rating"],
        level=meta["level"],
        is_enrolled=meta["is_enrolled"],
        user_progress=meta["user_progress"]
    )

@programs_router.get("/", response=List[LearningProgramOut])
def list_learning_programs(
    request,
    program_type: Optional[str] = None,
    target_audience: Optional[str] = None,
    domain: Optional[str] = None,
    mode: Optional[str] = None,
    q: Optional[str] = None
):
    user = _resolve_request_user(request)
    student_profile = None
    if user and user.role in [User.Role.STUDENT, User.Role.CANDIDATE]:
        student_profile = StudentProfile.objects.filter(user=user).first()

    qs = LearningProgram.objects.select_related('company').annotate(
        enrolled_students_count=models.Count('enrolled_students', distinct=True),
        enrolled_faculty_count=models.Count('enrolled_faculty', distinct=True)
    )
    if program_type and program_type != "ALL":
        qs = qs.filter(program_type__iexact=program_type)
    if target_audience and target_audience != 'ALL':
        qs = qs.filter(models.Q(target_audience__iexact=target_audience) | models.Q(target_audience='ALL'))
    if mode and mode != "ALL":
        qs = qs.filter(mode__iexact=mode)
    if q:
        qs = qs.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(company__name__icontains=q)
        )

    results = [_program_to_schema(p, student_profile) for p in qs]
    if domain and domain != "All":
        results = [p for p in results if p.domain.lower() == domain.lower() or domain.lower() in p.domain.lower()]

    return results

@programs_router.get("/recommendations", response=LearningRecommendationsResponseOut)
def get_learning_recommendations(request):
    user = _resolve_request_user(request)
    student_profile = None
    if user and user.role in [User.Role.STUDENT, User.Role.CANDIDATE]:
        student_profile = StudentProfile.objects.filter(user=user).first()

    all_db_programs = list(LearningProgram.objects.select_related('company').annotate(
        enrolled_students_count=models.Count('enrolled_students', distinct=True),
        enrolled_faculty_count=models.Count('enrolled_faculty', distinct=True)
    ).order_by('-created_at'))

    c_skills_lower = set()
    target_role = "General Engineering & Tech"
    top_gap_skills = []

    if student_profile:
        if student_profile.target_roles and len(student_profile.target_roles) > 0:
            target_role = student_profile.target_roles[0]
        elif student_profile.role_fit_matrix:
            sorted_fits = sorted(
                student_profile.role_fit_matrix.items(),
                key=lambda item: float(item[1].get("score", 0) if isinstance(item[1], dict) else 0),
                reverse=True
            )
            if sorted_fits:
                target_role = sorted_fits[0][0]

        c_matrix = student_profile.skills_matrix or {}
        for k in c_matrix.keys():
            c_skills_lower.add(k.lower().strip())
        for cat_list in (student_profile.skills_categorized or {}).values():
            if isinstance(cat_list, list):
                for sk in cat_list:
                    c_skills_lower.add(sk.lower().strip())

        try:
            roadmap = compute_skill_gap_roadmap(student_profile)
            for item in roadmap.get("skills_to_build_next", []):
                top_gap_skills.append(item.get("skill", "").strip())
        except Exception:
            pass

    top_gap_skills_lower = [s.lower() for s in top_gap_skills]

    scored_items = []
    for prog in all_db_programs:
        meta = _parse_program_meta(prog, student_profile)
        p_schema = _program_to_schema(prog, student_profile)

        prog_skills = [s.lower().strip() for s in (prog.skills_covered or [])]
        matched_skills = [s.title() for s in prog_skills if s in c_skills_lower]
        gap_skills_covered = [s.title() for s in prog_skills if any(gs in s or s in gs for gs in top_gap_skills_lower)]

        is_gap_booster = len(gap_skills_covered) > 0

        base_score = 65
        gap_bonus = len(gap_skills_covered) * 12
        verified_bonus = len(matched_skills) * 8
        cert_bonus = 6 if prog.is_certified else 0
        match_score = min(99, max(50, base_score + gap_bonus + verified_bonus + cert_bonus))

        expected_boost = ""
        recommendation_reason = ""
        if is_gap_booster:
            expected_boost = f"+{min(28, len(gap_skills_covered) * 9 + 10)}% Match Boost"
            recommendation_reason = f"Directly closes {len(gap_skills_covered)} critical skill gaps ({', '.join(gap_skills_covered[:2])}) for {target_role} roles."
        elif matched_skills:
            expected_boost = "+12% Proficiency Boost"
            recommendation_reason = f"Deepens applied proficiency in {', '.join(matched_skills[:2])} with recognized industry certification."
        else:
            expected_boost = "+8% Career Breadth"
            recommendation_reason = f"Broadens foundational competence in {prog.title} with verified credentials."

        scored_items.append(LearningProgramRecommendationItem(
            program=p_schema,
            match_score=match_score,
            matched_skills=matched_skills,
            gap_skills_covered=gap_skills_covered,
            expected_boost=expected_boost,
            is_gap_booster=is_gap_booster,
            is_enrolled=meta["is_enrolled"],
            user_progress=meta["user_progress"],
            completed_modules=meta["completed_modules"],
            recommendation_reason=recommendation_reason
        ))

    recommended_programs = sorted(scored_items, key=lambda x: x.match_score, reverse=True)[:8]
    skill_gap_boosters = [x for x in scored_items if x.is_gap_booster][:6]
    enrolled_programs = [x for x in scored_items if x.is_enrolled]

    return LearningRecommendationsResponseOut(
        recommended_programs=recommended_programs,
        skill_gap_boosters=skill_gap_boosters,
        enrolled_programs=enrolled_programs,
        all_programs=scored_items,
        target_role=target_role,
        verified_skills_count=len(c_skills_lower),
        top_gap_skills=top_gap_skills[:6]
    )

@programs_router.get("/my-enrollments", response=List[LearningProgramRecommendationItem], auth=JWTAuth())
def get_my_enrollments(request):
    user = request.auth
    student_profile = None
    if user.role in [User.Role.STUDENT, User.Role.CANDIDATE]:
        student_profile = StudentProfile.objects.filter(user=user).first()
    
    if not student_profile:
        return []

    programs = student_profile.enrolled_learning_programs.select_related('company').all()
    results = []
    for prog in programs:
        meta = _parse_program_meta(prog, student_profile)
        p_schema = _program_to_schema(prog, student_profile)
        results.append(LearningProgramRecommendationItem(
            program=p_schema,
            match_score=95,
            matched_skills=prog.skills_covered or [],
            gap_skills_covered=[],
            expected_boost="+15% Active Upskill",
            is_gap_booster=False,
            is_enrolled=True,
            user_progress=meta["user_progress"],
            completed_modules=meta["completed_modules"],
            recommendation_reason=f"Currently enrolled course track by {prog.company.name}."
        ))
    return results

@programs_router.post("/", response={201: LearningProgramOut, 400: dict}, auth=RecruiterAuth())
def create_learning_program(request, payload: LearningProgramCreateIn):
    recruiter = RecruiterProfile.objects.filter(user=request.auth).first()
    if not recruiter or not recruiter.company:
        return 400, {"message": "You must register or join a company before publishing learning programs."}

    program = LearningProgram.objects.create(
        company=recruiter.company,
        title=payload.title,
        program_type=payload.program_type,
        target_audience=payload.target_audience,
        description=payload.description,
        skills_covered=payload.skills_covered or [],
        instructor_or_mentor=payload.instructor_or_mentor or "",
        duration=payload.duration or "4 Weeks",
        mode=payload.mode or "ONLINE",
        registration_deadline=payload.registration_deadline,
        start_date=payload.start_date,
        is_certified=payload.is_certified,
        branding_banner_url=payload.branding_banner_url or ""
    )
    return 201, _program_to_schema(program)

@programs_router.get("/{program_id}", response={200: LearningProgramOut, 404: dict})
def get_learning_program_detail(request, program_id: int):
    user = _resolve_request_user(request)
    student_profile = None
    if user and user.role in [User.Role.STUDENT, User.Role.CANDIDATE]:
        student_profile = StudentProfile.objects.filter(user=user).first()

    program = LearningProgram.objects.select_related('company').annotate(
        enrolled_students_count=models.Count('enrolled_students', distinct=True),
        enrolled_faculty_count=models.Count('enrolled_faculty', distinct=True)
    ).filter(id=program_id).first()
    if not program:
        return 404, {"message": "Learning program not found."}
    return 200, _program_to_schema(program, student_profile)

@programs_router.post("/{program_id}/enroll", response={200: dict, 400: dict, 404: dict}, auth=JWTAuth())
def enroll_in_learning_program(request, program_id: int):
    user = request.auth
    program = LearningProgram.objects.select_related('company').filter(id=program_id).first()
    if not program:
        return 404, {"message": "Learning program not found."}

    from institutions.models import FacultyProfile
    role_label = "Student"
    if user.role in [User.Role.STUDENT, User.Role.CANDIDATE]:
        student_profile, _ = StudentProfile.objects.get_or_create(user=user)
        program.enrolled_students.add(student_profile)
        
        pref = student_profile.preferences or {}
        if "course_progress" not in pref:
            pref["course_progress"] = {}
        prog_key = str(program.id)
        if prog_key not in pref["course_progress"]:
            pref["course_progress"][prog_key] = {
                "progress": 0,
                "completed_modules": [],
                "enrolled_at": str(timezone.now()),
                "is_completed": False
            }
            student_profile.preferences = pref
            student_profile.save(update_fields=["preferences"])
    elif user.role in [User.Role.ACADEMIA, User.Role.FACULTY]:
        faculty_profile, _ = FacultyProfile.objects.get_or_create(user=user)
        program.enrolled_faculty.add(faculty_profile)
        role_label = "Faculty"
    else:
        return 400, {"message": "Only students and faculty can enroll in learning programs."}

    Notification.objects.create(
        user=user,
        title=f"Enrolled in {program.title}",
        message=f"You have successfully enrolled in '{program.title}' offered by {program.company.name}. Mode: {program.mode}.",
        notification_type=Notification.NotificationType.NEW_OPPORTUNITY
    )

    return 200, {
        "success": True,
        "message": f"Successfully enrolled {user.username} in {program.title}.",
        "program_id": program.id,
        "enrolled_as": role_label
    }

@programs_router.post("/{program_id}/progress", response={200: LearningProgressUpdateOut, 400: dict, 404: dict}, auth=JWTAuth())
def update_learning_progress(request, program_id: int, payload: LearningProgressUpdateIn):
    user = request.auth
    program = LearningProgram.objects.select_related('company').filter(id=program_id).first()
    if not program:
        return 404, {"message": "Learning program not found."}

    if user.role not in [User.Role.STUDENT, User.Role.CANDIDATE]:
        return 400, {"message": "Only students and candidates can record learning progress."}

    student_profile, _ = StudentProfile.objects.get_or_create(user=user)
    program.enrolled_students.add(student_profile)

    preferences = student_profile.preferences or {}
    if "course_progress" not in preferences:
        preferences["course_progress"] = {}

    prog_key = str(program.id)
    is_completed = payload.is_completed or (payload.progress_percentage >= 100)
    progress_val = 100 if is_completed else max(0, min(100, payload.progress_percentage))

    cert_id = None
    if is_completed:
        cert_id = f"SKL-CERT-{program.id}-{student_profile.id}-{hex(program.id * 1000 + student_profile.id)[2:].upper()}"
        certs = list(student_profile.certifications or [])
        cert_title = f"{program.title} Professional Certificate"
        if not any(c.get("name") == cert_title for c in certs):
            certs.append({
                "name": cert_title,
                "issuer": program.company.name,
                "issue_year": timezone.now().year,
                "credential_url": f"https://skillsetu.in/credentials/{cert_id}",
                "skills_covered": program.skills_covered or []
            })
            student_profile.certifications = certs

            Notification.objects.create(
                user=user,
                title=f"Verified Certificate Awarded: {program.title}",
                message=f"Congratulations! You completed '{program.title}' offered by {program.company.name}. Credential ID: {cert_id}.",
                notification_type=Notification.NotificationType.ASSESSMENT_REMINDER
            )

    preferences["course_progress"][prog_key] = {
        "progress": progress_val,
        "completed_modules": payload.completed_modules,
        "is_completed": is_completed,
        "certificate_id": cert_id,
        "updated_at": str(timezone.now())
    }
    student_profile.preferences = preferences
    student_profile.save(update_fields=["preferences", "certifications"])

    return 200, {
        "program_id": program.id,
        "progress_percentage": progress_val,
        "completed_modules": payload.completed_modules,
        "is_completed": is_completed,
        "certificate_id": cert_id,
        "message": f"Successfully updated progress to {progress_val}%" + (f". Credential #{cert_id} awarded!" if cert_id else ".")
    }


# ---------------------------------------------------------
# ROUTER 5: IDEMPOTENT INSTITUTIONAL PLACEMENT REPORTING
# (Maintained in institutions.api; re-exported for backwards compatibility)
# ---------------------------------------------------------
from institutions.api import placement_router


