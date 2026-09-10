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

# --- FACULTY PROFILE SCHEMAS ---

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
