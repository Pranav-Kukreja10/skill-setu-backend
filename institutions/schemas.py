from ninja import Schema
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- INSTITUTION & DEPARTMENT SCHEMAS ---

class DepartmentOut(Schema):
    id: int
    name: str
    code: str
    head_of_department: Optional[str] = ""
    created_at: datetime

class DepartmentCreateIn(Schema):
    name: str
    code: Optional[str] = ""
    head_of_department: Optional[str] = ""

class InstitutionOut(Schema):
    id: int
    name: str
    code: Optional[str] = None
    institution_type: str
    state: str
    city: str
    website: Optional[str] = None
    nirf_rank: Optional[int] = None
    is_verified: bool
    branding_logo_url: Optional[str] = None
    departments: List[DepartmentOut] = []
    created_at: datetime

class InstitutionCreateIn(Schema):
    name: str
    code: Optional[str] = None
    institution_type: Optional[str] = "COLLEGE"
    state: Optional[str] = ""
    city: Optional[str] = ""
    website: Optional[str] = None
    nirf_rank: Optional[int] = None
    branding_logo_url: Optional[str] = None

# --- FACULTY PROFILE & SETTINGS SCHEMAS ---

class FacultyCommonSettingsSchema(Schema):
    theme: str = "system"
    language: str = "en"
    timezone: str = "Asia/Kolkata"
    email_alerts: bool = True
    in_app_alerts: bool = True
    high_contrast: bool = False
    reduce_motion: bool = False

class PlacementOversightPreferencesSchema(Schema):
    auto_verify_internship_milestones: bool = False
    alert_on_unplaced_final_years: bool = True
    skill_deficit_threshold_pct: int = 40
    enable_digilocker_auto_sync: bool = True

class CurriculumAnalyticsPreferencesSchema(Schema):
    benchmark_comparison_tier: str = "NATIONAL"  # NATIONAL, STATE, TIER_1
    include_vocational_tracks: bool = True
    share_department_radar_with_recruiters: bool = True

class FacultyExposurePreferencesSchema(Schema):
    fdp_and_industrial_training_alerts: bool = True
    consultancy_invitation_sharing: bool = True

class FacultySettingsOutSchema(Schema):
    common: FacultyCommonSettingsSchema = FacultyCommonSettingsSchema()
    placement_oversight: PlacementOversightPreferencesSchema = PlacementOversightPreferencesSchema()
    curriculum_analytics: CurriculumAnalyticsPreferencesSchema = CurriculumAnalyticsPreferencesSchema()
    faculty_exposure: FacultyExposurePreferencesSchema = FacultyExposurePreferencesSchema()

class FacultySettingsUpdateIn(Schema):
    common: Optional[Dict[str, Any]] = None
    placement_oversight: Optional[Dict[str, Any]] = None
    curriculum_analytics: Optional[Dict[str, Any]] = None
    faculty_exposure: Optional[Dict[str, Any]] = None

class FacultyProfileOut(Schema):
    id: int
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    institution: Optional[InstitutionOut] = None
    department: Optional[DepartmentOut] = None
    designation: str
    employee_id: Optional[str] = None
    contact_phone: str
    is_institution_admin: bool
    preferences: Optional[Dict[str, Any]] = None
    created_at: datetime

class FacultyProfileUpdateIn(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    institution_id: Optional[int] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    employee_id: Optional[str] = None
    contact_phone: Optional[str] = None

# --- PLACEMENT REPORTING SCHEMAS (SIH COMPLIANT) ---

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

# --- FACULTY INDUSTRY COLLABORATION SCHEMAS (PS REQUIREMENT) ---

class FacultyOpportunityApplyIn(Schema):
    statement_of_purpose: Optional[str] = ""
    research_areas: Optional[List[str]] = []
    preferred_start_date: Optional[datetime] = None

