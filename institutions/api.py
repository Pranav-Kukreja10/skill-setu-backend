from ninja import Router
from typing import List, Optional, Dict, Any
from django.db import models
from accounts.models import User
from accounts.security import AcademiaAuth
from students.models import StudentProfile
from students.services import compute_profile_strength
from recruiters.models import Company, JobListing, JobApplication
from institutions.models import Institution, Department, FacultyProfile
from institutions.schemas import (
    InstitutionOut, InstitutionCreateIn,
    DepartmentOut, DepartmentCreateIn,
    FacultyProfileOut, FacultyProfileUpdateIn,
    PlacementOverviewOut,
    BranchWiseReportOut, BranchPlacementStatOut,
    StudentRosterReportOut, StudentPlacementStatusOut, StudentOfferDetail,
    SkillGapAnalysisOut, SkillDeficitItemOut,
    InDemandSkillsOut, InDemandSkillItemOut,
    PlacementTrendsOut
)

# ---------------------------------------------------------------------------
# ROUTER 1: INSTITUTION & FACULTY PROFILE MANAGEMENT
# ---------------------------------------------------------------------------
institutions_router = Router(tags=["Institutions & Faculty Management"])

@institutions_router.get("/directory", response=List[InstitutionOut])
def list_institution_directory(request):
    """
    Public Institutional Directory:
    Lists all verified colleges, universities, and polytechnics along with their active departments.
    Used for student registration, candidate academic credentials, and recruiter filtering.
    """
    institutions = Institution.objects.filter(is_verified=True).prefetch_related("departments")
    results = []
    for inst in institutions:
        departments = [
            DepartmentOut(
                id=d.id,
                name=d.name,
                code=d.code,
                head_of_department=d.head_of_department,
                created_at=d.created_at
            )
            for d in inst.departments.all()
        ]
        results.append(InstitutionOut(
            id=inst.id,
            name=inst.name,
            code=inst.code,
            institution_type=inst.institution_type,
            state=inst.state,
            city=inst.city,
            website=inst.website,
            nirf_rank=inst.nirf_rank,
            is_verified=inst.is_verified,
            branding_logo_url=inst.branding_logo_url,
            departments=departments,
            created_at=inst.created_at
        ))
    return results


@institutions_router.post("/", response={201: InstitutionOut, 400: dict}, auth=AcademiaAuth())
def create_institution(request, payload: InstitutionCreateIn):
    """
    Register a new institution (Requires ACADEMIA or ADMIN token).
    """
    if Institution.objects.filter(name__iexact=payload.name).exists():
        return 400, {"message": f"Institution with name '{payload.name}' already exists."}
    
    inst = Institution.objects.create(
        name=payload.name,
        code=payload.code,
        institution_type=payload.institution_type or Institution.InstitutionType.COLLEGE,
        state=payload.state or "",
        city=payload.city or "",
        website=payload.website,
        nirf_rank=payload.nirf_rank,
        branding_logo_url=payload.branding_logo_url,
        is_verified=True
    )
    return 201, InstitutionOut(
        id=inst.id,
        name=inst.name,
        code=inst.code,
        institution_type=inst.institution_type,
        state=inst.state,
        city=inst.city,
        website=inst.website,
        nirf_rank=inst.nirf_rank,
        is_verified=inst.is_verified,
        branding_logo_url=inst.branding_logo_url,
        departments=[],
        created_at=inst.created_at
    )


@institutions_router.post("/{institution_id}/departments", response={201: DepartmentOut, 404: dict, 400: dict}, auth=AcademiaAuth())
def add_department(request, institution_id: int, payload: DepartmentCreateIn):
    """
    Add a department to an institution (Requires ACADEMIA or ADMIN token).
    """
    try:
        inst = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return 404, {"message": "Institution not found."}

    if Department.objects.filter(institution=inst, name__iexact=payload.name).exists():
        return 400, {"message": f"Department '{payload.name}' already exists in this institution."}

    dept = Department.objects.create(
        institution=inst,
        name=payload.name,
        code=payload.code or "",
        head_of_department=payload.head_of_department or ""
    )
    return 201, DepartmentOut(
        id=dept.id,
        name=dept.name,
        code=dept.code,
        head_of_department=dept.head_of_department,
        created_at=dept.created_at
    )


@institutions_router.get("/faculty/me", response=FacultyProfileOut, auth=AcademiaAuth())
def get_faculty_profile(request):
    """
    Fetch authenticated faculty user's profile, designation, and associated institution.
    """
    user = request.auth
    fp, _ = FacultyProfile.objects.get_or_create(user=user)

    inst_out = None
    if fp.institution:
        departments = [
            DepartmentOut(
                id=d.id,
                name=d.name,
                code=d.code,
                head_of_department=d.head_of_department,
                created_at=d.created_at
            )
            for d in fp.institution.departments.all()
        ]
        inst_out = InstitutionOut(
            id=fp.institution.id,
            name=fp.institution.name,
            code=fp.institution.code,
            institution_type=fp.institution.institution_type,
            state=fp.institution.state,
            city=fp.institution.city,
            website=fp.institution.website,
            nirf_rank=fp.institution.nirf_rank,
            is_verified=fp.institution.is_verified,
            branding_logo_url=fp.institution.branding_logo_url,
            departments=departments,
            created_at=fp.institution.created_at
        )

    dept_out = None
    if fp.department:
        dept_out = DepartmentOut(
            id=fp.department.id,
            name=fp.department.name,
            code=fp.department.code,
            head_of_department=fp.department.head_of_department,
            created_at=fp.department.created_at
        )

    return FacultyProfileOut(
        id=fp.id,
        user_id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        institution=inst_out,
        department=dept_out,
        designation=fp.designation,
        employee_id=fp.employee_id,
        contact_phone=fp.contact_phone or user.phone_number or "",
        is_institution_admin=fp.is_institution_admin,
        created_at=fp.created_at
    )


@institutions_router.put("/faculty/me", response=FacultyProfileOut, auth=AcademiaAuth())
def update_faculty_profile(request, payload: FacultyProfileUpdateIn):
    """
    Update authenticated faculty user's designation, institution, and department.
    """
    user = request.auth
    fp, _ = FacultyProfile.objects.get_or_create(user=user)

    if payload.first_name is not None:
        user.first_name = payload.first_name
    if payload.last_name is not None:
        user.last_name = payload.last_name
    if payload.first_name is not None or payload.last_name is not None:
        user.save()

    if payload.designation is not None:
        fp.designation = payload.designation
    if payload.employee_id is not None:
        fp.employee_id = payload.employee_id
    if payload.contact_phone is not None:
        fp.contact_phone = payload.contact_phone

    if payload.institution_id:
        try:
            fp.institution = Institution.objects.get(id=payload.institution_id)
        except Institution.DoesNotExist:
            pass

    if payload.department_id:
        try:
            fp.department = Department.objects.get(id=payload.department_id)
        except Department.DoesNotExist:
            pass

    fp.save()
    return get_faculty_profile(request)


# ---------------------------------------------------------------------------
# ROUTER 2: IDEMPOTENT INSTITUTIONAL PLACEMENT REPORTING (SIH COMPLIANT)
# ---------------------------------------------------------------------------
placement_router = Router(tags=["Placement Reporting"], auth=AcademiaAuth())

@placement_router.get("/overview", response=PlacementOverviewOut)
def get_placement_overview(request):
    """
    Idempotent Institutional Placement KPI Overview:
    Uses distinct student set aggregations to guarantee exact counts across network retries.
    """
    total_students = StudentProfile.objects.count()
    placed_students = StudentProfile.objects.filter(placement_status=StudentProfile.PlacementStatus.PLACED).count()
    unplaced_students = max(0, total_students - placed_students)
    rate = round((placed_students / total_students * 100.0), 2) if total_students > 0 else 0.0

    total_companies = Company.objects.count()
    total_openings = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED).count()
    total_applications = JobApplication.objects.count()

    # Idempotent counts via distinct student_id
    offers_extended = JobApplication.objects.filter(
        status=JobApplication.ApplicationStatus.OFFERED
    ).values("student_id").distinct().count()

    shortlisted = JobApplication.objects.filter(
        status=JobApplication.ApplicationStatus.SHORTLISTED
    ).values("student_id").distinct().count()

    interview_pipeline = JobApplication.objects.filter(
        status=JobApplication.ApplicationStatus.INTERVIEW
    ).values("student_id").distinct().count()

    return PlacementOverviewOut(
        total_students=total_students,
        placed_students=placed_students,
        unplaced_students=unplaced_students,
        placement_rate_percentage=rate,
        total_companies=total_companies,
        total_job_openings=total_openings,
        total_applications=total_applications,
        offers_extended=offers_extended,
        shortlisted_candidates=shortlisted,
        interview_pipeline_count=interview_pipeline
    )


@placement_router.get("/branch-wise", response=BranchWiseReportOut)
def get_branch_wise_report(request):
    """
    Idempotent Branch/Departmental Placement Metrics:
    Returns department-level placement rates, average cognitive scores, and top skills.
    """
    departments = StudentProfile.objects.exclude(department="").values_list("department", flat=True).distinct()
    
    branch_stats = []
    for dept in sorted(list(departments)):
        qs = StudentProfile.objects.filter(department=dept)
        total = qs.count()
        placed = qs.filter(placement_status=StudentProfile.PlacementStatus.PLACED).count()
        rate = round((placed / total * 100.0), 2) if total > 0 else 0.0

        avg_conf = qs.aggregate(models.Avg("overall_confidence_score"))["overall_confidence_score__avg"] or 0.0

        # Extract top skills in this branch
        skill_counts = {}
        for p in qs:
            for s in (p.skills_matrix or {}).keys():
                skill_counts[s] = skill_counts.get(s, 0) + 1
        top_skills = sorted(skill_counts.keys(), key=lambda x: skill_counts[x], reverse=True)[:5]

        branch_stats.append(BranchPlacementStatOut(
            department=dept,
            total_students=total,
            placed_students=placed,
            placement_rate_percentage=rate,
            average_confidence_score=round(float(avg_conf), 2),
            top_skills=top_skills
        ))

    return BranchWiseReportOut(departments=branch_stats)


@placement_router.get("/student-status", response=StudentRosterReportOut)
def get_student_roster_status(request, department: Optional[str] = None):
    """
    Faculty Student Roster:
    Comprehensive list of students, verified scores, placement statuses, and received offers.
    """
    qs = StudentProfile.objects.select_related("user").all()
    if department:
        qs = qs.filter(department__iexact=department)

    roster = []
    for p in qs:
        # Fetch active offers for student
        offer_apps = JobApplication.objects.filter(
            student=p,
            status=JobApplication.ApplicationStatus.OFFERED
        ).select_related("listing__company")

        offers = []
        for oa in offer_apps:
            offers.append(StudentOfferDetail(
                listing_id=oa.listing.id,
                listing_title=oa.listing.title,
                company_name=oa.listing.company.name if oa.listing.company else "",
                stipend_or_ctc=oa.listing.stipend_or_ctc,
                role_type=oa.listing.role_type,
                status=oa.status
            ))

        p_strength = compute_profile_strength(p)[0]
        roster.append(StudentPlacementStatusOut(
            student_id=p.user.id,
            profile_id=p.id,
            username=p.user.username,
            email=p.user.email,
            institution=p.institution or "Campus Student",
            department=p.department or "General Engineering",
            placement_status=p.placement_status,
            overall_confidence_score=p.overall_confidence_score,
            profile_strength_score=p_strength,
            is_verified=p.is_verified,
            certifications=getattr(p, "certifications", []) or [],
            target_roles=p.target_roles or [],
            offers=offers
        ))

    return StudentRosterReportOut(total_students=len(roster), roster=roster)


@placement_router.get("/skill-gaps", response=SkillGapAnalysisOut)
def get_faculty_skill_gap_analysis(request, department: Optional[str] = None):
    """
    Faculty Institutional Oversight: Departmental & College-wide Skill Gap Visibility.
    Aggregates active recruiter requirements vs student skill supply,
    identifying highest deficit competencies and curriculum recommendations.
    """
    stu_qs = StudentProfile.objects.all()
    if department:
        stu_qs = stu_qs.filter(department__iexact=department)
    total_students = stu_qs.count()

    active_listings = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED)
    total_listings = active_listings.count()

    # Aggregate skill frequency in listings
    demand_counts = {}
    for l in active_listings:
        for s in (l.required_skills or []):
            s_clean = s.lower().strip()
            if s_clean:
                demand_counts[s_clean] = demand_counts.get(s_clean, 0) + 1

    # Student supply across the department
    supply_counts = {}
    proficiency_sums = {}
    for p in stu_qs:
        for s_name, s_data in (p.skills_matrix or {}).items():
            s_clean = s_name.lower().strip()
            weight = s_data.get("weight", 50) if isinstance(s_data, dict) else 50
            supply_counts[s_clean] = supply_counts.get(s_clean, 0) + 1
            proficiency_sums[s_clean] = proficiency_sums.get(s_clean, 0) + weight

    # Calculate deficit metrics for top demanded skills
    deficit_items = []
    all_evaluated_skills = set(list(demand_counts.keys())[:25])
    for s_clean in sorted(demand_counts.keys(), key=lambda k: demand_counts[k], reverse=True)[:25]:
        all_evaluated_skills.add(s_clean)

    for skill in all_evaluated_skills:
        d_cnt = demand_counts.get(skill, 0)
        s_cnt = supply_counts.get(skill, 0)
        d_pct = round((d_cnt / total_listings * 100.0), 2) if total_listings > 0 else 0.0
        s_pct = round((s_cnt / total_students * 100.0), 2) if total_students > 0 else 0.0
        deficit_pct = max(0.0, round(d_pct - s_pct, 2))
        avg_prof = round(proficiency_sums.get(skill, 0) / s_cnt, 2) if s_cnt > 0 else 0.0

        deficit_items.append(SkillDeficitItemOut(
            skill=skill.title(),
            market_demand_count=d_cnt,
            market_demand_percentage=d_pct,
            student_supply_count=s_cnt,
            student_supply_percentage=s_pct,
            deficit_percentage=deficit_pct,
            average_student_proficiency=avg_prof
        ))

    deficit_items.sort(key=lambda x: (x.deficit_percentage, x.market_demand_count), reverse=True)

    # Faculty Recommendations based on top deficits
    recommendations = []
    top_deficits = [item.skill for item in deficit_items[:4] if item.deficit_percentage > 10.0]
    if top_deficits:
        recommendations.append(
            f"Industry demand gap detected for [{', '.join(top_deficits)}]. Recommend integrating hands-on laboratory modules or industry-certified guest workshops."
        )
    recommendations.append(
        "Encourage students with medium proficiency to complete end-to-end portfolio projects and obtain recognized credentials to boost Ws proficiency weights."
    )
    if department:
        recommendations.append(
            f"Cross-reference {department} elective syllabus with benchmark role requirements to improve campus placement fitment."
        )

    return SkillGapAnalysisOut(
        department=department or "All Departments",
        total_students=total_students,
        total_active_postings=total_listings,
        deficit_skills=deficit_items[:15],
        faculty_recommendations=recommendations
    )


@placement_router.get("/in-demand-skills", response=InDemandSkillsOut)
def get_in_demand_skills_analytics(request):
    """
    Market Demand Radar & Skill Deficit Index:
    Surfaces high-frequency hiring skills across all active postings compared against campus supply.
    """
    active_listings = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED).select_related("company__industry")
    total_listings = active_listings.count()
    total_students = StudentProfile.objects.count()

    demand_counts = {}
    for l in active_listings:
        for s in (l.required_skills or []):
            s_clean = s.lower().strip()
            if s_clean:
                demand_counts[s_clean] = demand_counts.get(s_clean, 0) + 1

    # Student supply
    supply_counts = {}
    for p in StudentProfile.objects.all():
        for s_name in (p.skills_matrix or {}).keys():
            s_clean = s_name.lower().strip()
            supply_counts[s_clean] = supply_counts.get(s_clean, 0) + 1

    in_demand_items = []
    for skill, d_cnt in sorted(demand_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        s_cnt = supply_counts.get(skill, 0)
        d_pct = round((d_cnt / total_listings * 100.0), 2) if total_listings > 0 else 0.0
        coverage_pct = round((s_cnt / total_students * 100.0), 2) if total_students > 0 else 0.0
        deficit_idx = round(max(0.0, (d_cnt - s_cnt) / max(1, d_cnt)), 2)

        in_demand_items.append(InDemandSkillItemOut(
            skill=skill.title(),
            demand_postings_count=d_cnt,
            demand_percentage=d_pct,
            student_supply_count=s_cnt,
            supply_coverage_percentage=coverage_pct,
            deficit_index=deficit_idx
        ))

    # Top hiring sectors
    sector_counts = {}
    for l in active_listings:
        sec_name = l.company.industry.name if (l.company and l.company.industry) else "General Technology"
        sector_counts[sec_name] = sector_counts.get(sec_name, 0) + 1

    top_sectors = [
        {"sector": sec, "active_postings": count, "percentage": round(count / total_listings * 100.0, 2) if total_listings > 0 else 0.0}
        for sec, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    return InDemandSkillsOut(
        total_active_listings=total_listings,
        total_students_indexed=total_students,
        in_demand_skills=in_demand_items,
        top_hiring_sectors=top_sectors
    )


@placement_router.get("/trends", response=PlacementTrendsOut)
def get_recruitment_pipeline_trends(request):
    """
    Recruitment Funnel & Pipeline Conversion Trends:
    Computes hiring stage velocities (Applied -> Reviewed -> Shortlisted -> Interview -> Offered -> Placed)
    and role type breakdowns.
    """
    total_applications = JobApplication.objects.count()
    applied_count = JobApplication.objects.filter(status=JobApplication.ApplicationStatus.APPLIED).count()
    reviewed_count = JobApplication.objects.filter(status=JobApplication.ApplicationStatus.UNDER_REVIEW).count()
    shortlisted_count = JobApplication.objects.filter(status=JobApplication.ApplicationStatus.SHORTLISTED).count()
    interview_count = JobApplication.objects.filter(status=JobApplication.ApplicationStatus.INTERVIEW).count()
    offered_count = JobApplication.objects.filter(status=JobApplication.ApplicationStatus.OFFERED).count()
    placed_students_count = StudentProfile.objects.filter(placement_status=StudentProfile.PlacementStatus.PLACED).count()

    # Stage conversion percentages
    shortlist_pct = round((shortlisted_count + interview_count + offered_count) / total_applications * 100.0, 2) if total_applications > 0 else 0.0
    interview_pct = round((interview_count + offered_count) / max(1, (shortlisted_count + interview_count + offered_count)) * 100.0, 2)
    offer_pct = round(offered_count / max(1, (interview_count + offered_count)) * 100.0, 2)
    overall_offer_pct = round(offered_count / total_applications * 100.0, 2) if total_applications > 0 else 0.0

    # Role type breakdown
    active_listings = JobListing.objects.all()
    full_time = active_listings.filter(role_type=JobListing.RoleType.FULL_TIME).count()
    internship = active_listings.filter(role_type=JobListing.RoleType.INTERNSHIP).count()
    contract = active_listings.filter(role_type=JobListing.RoleType.CONTRACT).count()

    active_companies = Company.objects.filter(job_listings__isnull=False).distinct().count()

    return PlacementTrendsOut(
        total_applications=total_applications,
        funnel_stages={
            "applied": applied_count,
            "under_review": reviewed_count,
            "shortlisted": shortlisted_count,
            "interview": interview_count,
            "offered": offered_count,
            "placed_students": placed_students_count
        },
        conversion_rates={
            "application_to_shortlist_pct": shortlist_pct,
            "shortlist_to_interview_pct": interview_pct,
            "interview_to_offer_pct": offer_pct,
            "overall_offer_rate_pct": overall_offer_pct
        },
        role_type_distribution={
            "full_time": full_time,
            "internship": internship,
            "contract": contract
        },
        active_companies_count=active_companies
    )
