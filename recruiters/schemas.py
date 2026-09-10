from ninja import Schema
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- COMPANY SCHEMAS ---

class CompanyCreateIn(Schema):
    name: str
    registration_number: Optional[str] = ""
    website: Optional[str] = ""
    industry_id: Optional[int] = None
    branding_logo_url: Optional[str] = ""
    description: Optional[str] = ""
    headquarters: Optional[str] = ""

class CompanyUpdateIn(Schema):
    registration_number: Optional[str] = None
    website: Optional[str] = None
    industry_id: Optional[int] = None
    branding_logo_url: Optional[str] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None

class CompanyOut(Schema):
    id: int
    name: str
    registration_number: Optional[str] = ""
    is_verified: bool
    website: Optional[str] = ""
    industry_id: Optional[int] = None
    industry_name: Optional[str] = None
    branding_logo_url: Optional[str] = ""
    description: Optional[str] = ""
    headquarters: Optional[str] = ""
    created_at: datetime

# --- RECRUITER PROFILE SCHEMAS ---

class RecruiterProfileUpdateIn(Schema):
    designation: Optional[str] = None
    department: Optional[str] = None
    contact_phone: Optional[str] = None

class RecruiterProfileOut(Schema):
    id: int
    user_id: int
    username: str
    email: str
    designation: str
    department: Optional[str] = ""
    contact_phone: Optional[str] = ""
    is_company_admin: bool
    company: Optional[CompanyOut] = None

# --- JOB LISTING SCHEMAS ---

class JobListingCreateIn(Schema):
    title: str
    role_type: Optional[str] = "FULL_TIME"  # FULL_TIME, INTERNSHIP, FACULTY_INTERNSHIP, FDP, etc.
    target_audience: Optional[str] = "STUDENT"  # STUDENT, FACULTY, ALL
    status: Optional[str] = "DRAFT"  # DRAFT, PUBLISHED
    stipend_or_ctc: str
    location: str
    is_remote: Optional[bool] = False
    application_deadline: Optional[datetime] = None
    tenure: Optional[str] = ""
    open_positions: Optional[int] = 1
    required_skills: List[str] = []
    eligibility_criteria: Optional[Dict[str, Any]] = {}
    description: str
    # DEI attributes
    is_diversity_drive: Optional[bool] = False
    target_gender: Optional[str] = "ALL"
    dei_initiatives: Optional[List[str]] = []

class JobListingUpdateIn(Schema):
    title: Optional[str] = None
    role_type: Optional[str] = None
    target_audience: Optional[str] = None
    status: Optional[str] = None
    stipend_or_ctc: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    application_deadline: Optional[datetime] = None
    tenure: Optional[str] = None
    open_positions: Optional[int] = None
    required_skills: Optional[List[str]] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    # DEI attributes
    is_diversity_drive: Optional[bool] = None
    target_gender: Optional[str] = None
    dei_initiatives: Optional[List[str]] = None

class JobListingOut(Schema):
    id: int
    company_id: int
    company_name: str
    company_logo: Optional[str] = ""
    company_website: Optional[str] = ""
    company_headquarters: Optional[str] = ""
    recruiter_id: int
    recruiter_name: str
    title: str
    role_type: str
    target_audience: str = "STUDENT"
    status: str
    stipend_or_ctc: str
    location: str
    is_remote: bool = False
    application_deadline: Optional[datetime] = None
    tenure: Optional[str] = ""
    open_positions: int
    required_skills: List[str] = []
    eligibility_criteria: Dict[str, Any] = {}
    description: str
    is_diversity_drive: bool = False
    target_gender: str = "ALL"
    dei_initiatives: List[str] = []
    applications_count: int = 0
    created_at: datetime
    updated_at: datetime


# --- CANDIDATE NLP JOB SEARCH SCHEMAS ---

class CandidateJobSearchIn(Schema):
    query: str
    limit: Optional[int] = 10
    role_type: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None

class CandidateJobSearchResultOut(Schema):
    id: int
    title: str
    role_type: str
    status: str
    stipend_or_ctc: str
    location: str
    is_remote: bool = False
    application_deadline: Optional[datetime] = None
    tenure: Optional[str] = ""
    open_positions: int
    required_skills: List[str] = []
    eligibility_criteria: Dict[str, Any] = {}
    description: str
    company_id: int
    company_name: str
    company_logo: Optional[str] = ""
    company_website: Optional[str] = ""
    company_headquarters: Optional[str] = ""
    recruiter_id: int
    recruiter_name: str
    recruiter_designation: str
    match_score: float
    skill_overlap_score: float
    semantic_score: float
    fulltext_score: float
    matched_skills: List[str] = []

class CandidateJobSearchResponseOut(Schema):
    query: str
    total_results: int
    results: List[CandidateJobSearchResultOut]

# --- APPLICATION LIFECYCLE SCHEMAS ---

class JobApplicationApplyIn(Schema):
    cover_note: Optional[str] = ""

class JobApplicationStatusUpdateIn(Schema):
    status: str  # APPLIED, UNDER_REVIEW, SHORTLISTED, INTERVIEW, OFFERED, REJECTED
    note: Optional[str] = ""
    interview_date: Optional[datetime] = None

class ApplicantStudentOut(Schema):
    id: int
    student_profile_id: int
    username: str
    email: str
    bio: Optional[str] = None
    current_designation: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    institution: Optional[str] = None
    department: Optional[str] = None
    github_url: Optional[str] = ""
    certifications: List[Dict[str, Any]] = []
    profile_strength_score: float = 0.0
    skills_matrix: Dict[str, Any] = {}
    raw_extracted_skills: List[str] = []
    role_fit_matrix: Dict[str, Any] = {}
    target_roles: List[str] = []
    overall_confidence_score: float
    is_verified: bool
    placement_status: str
    is_blind: bool = False

class JobApplicationOut(Schema):
    id: int
    listing_id: int
    listing_title: str
    company_name: str
    student: ApplicantStudentOut
    status: str
    match_score: float
    recruiter_notes: Optional[str] = ""
    interview_date: Optional[datetime] = None
    status_history: List[Dict[str, Any]] = []
    # PS Internship Progress Fields
    internship_status: str = "NOT_STARTED"
    mentor_name: Optional[str] = ""
    mentor_designation: Optional[str] = ""
    mentor_feedback: Optional[str] = ""
    mentor_rating: Optional[float] = None
    completion_certificate_url: Optional[str] = ""
    internship_report_url: Optional[str] = ""
    weekly_progress_logs: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime

class StudentMyApplicationOut(Schema):
    id: int
    listing_id: int
    listing_title: str
    company_name: str
    company_logo: Optional[str] = ""
    location: str
    stipend_or_ctc: str
    role_type: str
    status: str
    match_score: float
    recruiter_notes: Optional[str] = ""
    interview_date: Optional[datetime] = None
    status_history: List[Dict[str, Any]] = []
    # PS Internship Progress Fields
    internship_status: str = "NOT_STARTED"
    mentor_name: Optional[str] = ""
    mentor_designation: Optional[str] = ""
    mentor_feedback: Optional[str] = ""
    mentor_rating: Optional[float] = None
    completion_certificate_url: Optional[str] = ""
    internship_report_url: Optional[str] = ""
    weekly_progress_logs: List[Dict[str, Any]] = []
    created_at: datetime

class InternshipProgressUpdateIn(Schema):
    internship_status: str  # NOT_STARTED, IN_PROGRESS, COMPLETED, TERMINATED
    mentor_name: Optional[str] = None
    mentor_designation: Optional[str] = None
    mentor_feedback: Optional[str] = None
    mentor_rating: Optional[float] = None
    completion_certificate_url: Optional[str] = None
    internship_report_url: Optional[str] = None

class InternshipMilestoneLogIn(Schema):
    week_number: int
    milestone_summary: str
    hours_logged: Optional[int] = 40
    deliverables_url: Optional[str] = ""

# --- INDUSTRY LEARNING PROGRAMS & COLLABORATION INITIATIVES ---

class LearningProgramOut(Schema):
    id: int
    company_id: int
    company_name: str
    company_logo: Optional[str] = ""
    title: str
    program_type: str
    target_audience: str
    description: str
    skills_covered: List[str] = []
    instructor_or_mentor: Optional[str] = ""
    duration: str
    mode: str
    registration_deadline: Optional[datetime] = None
    start_date: Optional[datetime] = None
    is_certified: bool
    branding_banner_url: Optional[str] = ""
    enrolled_students_count: int = 0
    enrolled_faculty_count: int = 0
    created_at: datetime

class LearningProgramCreateIn(Schema):
    title: str
    program_type: str = "WORKSHOP"
    target_audience: str = "ALL"
    description: str
    skills_covered: List[str] = []
    instructor_or_mentor: Optional[str] = ""
    duration: str = "4 Weeks"
    mode: str = "ONLINE"
    registration_deadline: Optional[datetime] = None
    start_date: Optional[datetime] = None
    is_certified: bool = True
    branding_banner_url: Optional[str] = ""


# --- PLACEMENT REPORTING SCHEMAS ---

class PlacementOverviewOut(Schema):
    total_students: int
    placed_students: int
    unplaced_students: int
    placement_rate_percentage: float
    total_companies: int
    total_job_openings: int
    total_applications: int
    offers_extended: int
    shortlisted_candidates: int
    interview_pipeline_count: int

class BranchPlacementStatOut(Schema):
    department: str
    total_students: int
    placed_students: int
    placement_rate_percentage: float
    average_confidence_score: float
    top_skills: List[str] = []

class BranchWiseReportOut(Schema):
    departments: List[BranchPlacementStatOut]

class StudentOfferDetail(Schema):
    listing_id: int
    listing_title: str
    company_name: str
    stipend_or_ctc: str
    role_type: str
    status: str

class StudentPlacementStatusOut(Schema):
    student_id: int
    profile_id: int
    username: str
    email: str
    institution: str
    department: str
    placement_status: str
    overall_confidence_score: float
    profile_strength_score: float = 0.0
    is_verified: bool
    certifications: List[Dict[str, Any]] = []
    target_roles: List[str] = []
    offers: List[StudentOfferDetail] = []

class StudentRosterReportOut(Schema):
    total_students: int
    roster: List[StudentPlacementStatusOut]

class SkillDeficitItemOut(Schema):
    skill: str
    market_demand_count: int
    market_demand_percentage: float
    student_supply_count: int
    student_supply_percentage: float
    deficit_percentage: float
    average_student_proficiency: float

class SkillGapAnalysisOut(Schema):
    department: Optional[str] = "All Departments"
    total_students: int
    total_active_postings: int
    deficit_skills: List[SkillDeficitItemOut] = []
    faculty_recommendations: List[str] = []

class InDemandSkillItemOut(Schema):
    skill: str
    demand_postings_count: int
    demand_percentage: float
    student_supply_count: int
    supply_coverage_percentage: float
    deficit_index: float

class InDemandSkillsOut(Schema):
    total_active_listings: int
    total_students_indexed: int
    in_demand_skills: List[InDemandSkillItemOut] = []
    top_hiring_sectors: List[Dict[str, Any]] = []

class PlacementTrendsOut(Schema):
    total_applications: int
    funnel_stages: Dict[str, int]
    conversion_rates: Dict[str, float]
    role_type_distribution: Dict[str, int]
    active_companies_count: int
