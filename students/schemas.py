from ninja import Schema
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- PHASE 1 & 2 SCHEMAS (Resume Upload, Review & Profile) ---

class ResumeUploadOutSchema(Schema):
    success: bool
    message: str
    raw_text: str

class ResumeAnalysisInSchema(Schema):
    raw_text: str

class CertificationSchema(Schema):
    name: str
    issuer: Optional[str] = ""
    issue_year: Optional[int] = None
    credential_url: Optional[str] = ""
    skills_covered: List[str] = []

class ProfileStrengthBreakdownSchema(Schema):
    cognitive_score: float = 0.0
    projects_experience_score: float = 0.0
    certifications_score: float = 0.0
    academics_score: float = 0.0

class ResumePreviewOutSchema(Schema):
    success: bool
    raw_text: str
    current_designation: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    academic_credentials: Dict[str, Any] = {}
    skills_categorized: Dict[str, List[str]] = {}
    skills_matrix: Dict[str, Any] = {}
    projects: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []
    target_roles: List[str] = []
    social_links: Dict[str, str] = {}

# --- GRANULAR PREFERENCES & PERSONALISATION SCHEMAS ---

class NotificationPreferencesSchema(Schema):
    opportunity_alerts: bool = True
    deadline_reminders: bool = True
    scheme_alerts: bool = True
    application_status_updates: bool = True

class FeaturePreferencesSchema(Schema):
    show_affirmative_action_schemes: bool = True
    show_diversity_job_badges: bool = True
    smart_roadmap_recommendations: bool = True
    reverse_matching_radar: bool = True

class PrivacyPreferencesSchema(Schema):
    participate_in_diversity_hiring: bool = True
    share_profile_with_verified_recruiters: bool = True

class StudentPreferencesSchema(Schema):
    notifications: NotificationPreferencesSchema = NotificationPreferencesSchema()
    features: FeaturePreferencesSchema = FeaturePreferencesSchema()
    privacy: PrivacyPreferencesSchema = PrivacyPreferencesSchema()

class StudentPreferencesUpdateIn(Schema):
    notifications: Optional[Dict[str, bool]] = None
    features: Optional[Dict[str, bool]] = None
    privacy: Optional[Dict[str, bool]] = None

class StudentProfileInSchema(Schema):
    bio: Optional[str] = None
    gender: Optional[str] = None
    current_designation: Optional[str] = None
    experience_years: Optional[float] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    degree: Optional[str] = None
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None
    github_handle: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    skills_matrix: Optional[Dict[str, Any]] = None
    skills_categorized: Optional[Dict[str, Any]] = None
    target_roles: Optional[List[str]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    internships: Optional[List[Dict[str, Any]]] = None
    achievements: Optional[List[Dict[str, Any]]] = None
    academic_records: Optional[List[Dict[str, Any]]] = None
    placement_status: Optional[str] = "UNPLACED"
    preferences: Optional[Dict[str, Any]] = None

class StudentProfileOutSchema(Schema):
    id: int
    username: str
    email: str
    gender: str = "PREFER_NOT_TO_SAY"
    bio: Optional[str] = None
    current_designation: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    institution: Optional[str] = ""
    department: Optional[str] = ""
    degree: Optional[str] = ""
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None
    github_handle: Optional[str] = None
    github_url: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    portfolio_url: Optional[str] = ""
    certifications: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    internships: List[Dict[str, Any]] = []
    achievements: List[Dict[str, Any]] = []
    academic_records: List[Dict[str, Any]] = []
    skills_matrix: Dict[str, Any] = {}
    skills_categorized: Dict[str, Any] = {}
    raw_extracted_skills: List[str] = []
    role_fit_matrix: Dict[str, Any] = {}
    target_roles: List[str] = []
    placement_status: str
    overall_confidence_score: float
    profile_strength_score: float = 0.0
    profile_strength_breakdown: Optional[ProfileStrengthBreakdownSchema] = None
    is_verified: bool
    preferences: Dict[str, Any] = {}

# --- DIGITAL PORTFOLIO & INTERNSHIP MILESTONE SCHEMAS (PS REQUIREMENT) ---

class AchievementItemSchema(Schema):
    title: str
    issuer: Optional[str] = ""
    year: Optional[int] = None
    description: Optional[str] = ""
    proof_url: Optional[str] = ""

class AchievementsUpdateInSchema(Schema):
    achievements: List[AchievementItemSchema]

class StudentPortfolioOutSchema(Schema):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    current_designation: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    institution: Optional[str] = ""
    department: Optional[str] = ""
    degree: Optional[str] = ""
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None
    github_url: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    portfolio_url: Optional[str] = ""
    is_verified: bool
    overall_confidence_score: float
    profile_strength_score: float = 0.0
    profile_strength_breakdown: Optional[ProfileStrengthBreakdownSchema] = None
    placement_status: str
    target_roles: List[str] = []
    skills_matrix: Dict[str, Any] = {}
    skills_categorized: Dict[str, Any] = {}
    role_fit_matrix: Dict[str, Any] = {}
    certifications: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    internships: List[Dict[str, Any]] = []
    achievements: List[Dict[str, Any]] = []
    academic_records: List[Dict[str, Any]] = []
    active_internships: List[Dict[str, Any]] = []
    is_blind: bool = False

class MilestoneLogCreateIn(Schema):
    week_number: int
    milestone_summary: str
    hours_logged: Optional[int] = 40
    deliverables_url: Optional[str] = ""

class ActiveInternshipDetailOut(Schema):
    application_id: int
    listing_id: int
    title: str
    company_name: str
    company_logo: Optional[str] = ""
    location: str
    stipend_or_ctc: str
    role_type: str
    internship_status: str
    mentor_name: Optional[str] = ""
    mentor_designation: Optional[str] = ""
    mentor_feedback: Optional[str] = ""
    mentor_rating: Optional[float] = None
    completion_certificate_url: Optional[str] = ""
    internship_report_url: Optional[str] = ""
    weekly_progress_logs: List[Dict[str, Any]] = []


# --- PHASE 3 SCHEMAS (Test Generation) ---

class QuestionOutSchema(Schema):
    id: int
    question_text: str
    type: str  # "MCQ" or "VIVA"
    difficulty: str  # "EASY", "MEDIUM", "HARD"
    options: Optional[List[str]] = None  # Only populated for MCQ

class TestGenerationOutSchema(Schema):
    role_title: str
    session_id: int
    questions: List[QuestionOutSchema]

# --- PHASE 4 SCHEMAS (Test Submission & Grading) ---

class StudentAnswerInSchema(Schema):
    id: int
    answer_text: str
    time_taken_seconds: Optional[int] = 15

class TestSubmissionInSchema(Schema):
    target_role: str
    session_id: int
    answers: List[StudentAnswerInSchema]

class FeedbackDetailSchema(Schema):
    id: int
    question_text: str
    type: str
    student_answer: str
    score: int
    feedback: str

class TestGradingOutSchema(Schema):
    success: bool
    cognitive_score: int
    mcq_average: int
    viva_average: int
    confidence_score: int
    feedback_log: List[FeedbackDetailSchema] = []
    retest_required: bool = False
    fault_acknowledged: bool = False
    message: Optional[str] = ""
    retest_session_id: Optional[int] = None

# --- PHASE 5 SCHEMAS (Recruiter Hybrid Search & Ranking) ---

class RecruiterSearchQueryIn(Schema):
    query: str
    limit: Optional[int] = 10
    blind: Optional[bool] = False

class StudentSearchResultOut(Schema):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    skills_matrix: Dict[str, Any] = {}
    raw_extracted_skills: List[str] = []
    role_fit_matrix: Dict[str, Any] = {}
    target_roles: List[str] = []
    institution: Optional[str] = None
    department: Optional[str] = None
    overall_confidence_score: float
    is_verified: bool
    is_blind: bool = False
    final_score: float
    skill_tag_score: float
    semantic_score: float
    fulltext_score: float
    verification_boost: float = 1.0
    matched_skills: List[str] = []
    inferred_sector: Optional[str] = None

class RecruiterSearchResponseOut(Schema):
    query: str
    inferred_sector: Optional[str] = None
    matched_query_skills: List[str] = []
    weights_used: Dict[str, float]
    total_results: int
    is_blind: bool = False
    results: List[StudentSearchResultOut]

# --- PHASE 6 SCHEMAS: DISCOVERY FEED, RECOMMENDATIONS, ROADMAP, NOTIFICATIONS ---

class JobDiscoveryItemOut(Schema):
    id: int
    title: str
    company_id: int
    company_name: str
    company_logo: Optional[str] = ""
    company_website: Optional[str] = ""
    role_type: str
    location: str
    is_remote: bool
    stipend_or_ctc: str
    tenure: Optional[str] = ""
    open_positions: int
    required_skills: List[str] = []
    eligibility_criteria: Dict[str, Any] = {}
    application_deadline: Optional[datetime] = None
    description: str
    is_diversity_drive: bool = False
    target_gender: str = "ALL"
    dei_initiatives: List[str] = []
    created_at: datetime

class JobDiscoveryFeedOut(Schema):
    total_jobs: int
    jobs: List[JobDiscoveryItemOut]

class PersonalizedRecommendationItemOut(Schema):
    listing_id: int
    title: str
    company_name: str
    company_logo: Optional[str] = ""
    location: str
    is_remote: bool
    role_type: str
    stipend_or_ctc: str
    tenure: Optional[str] = ""
    application_deadline: Optional[datetime] = None
    match_percentage: float
    fit_level: str
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    required_skills: List[str] = []
    description: str

class PersonalizedRecommendationsFeedOut(Schema):
    candidate_id: int
    candidate_skills_count: int
    total_recommendations: int
    recommendations: List[PersonalizedRecommendationItemOut]

class MarketDemandSkillOut(Schema):
    skill: str
    market_demand_percentage: float
    candidate_proficiency: int
    status: str

class SkillToBuildNextOut(Schema):
    skill: str
    priority: str
    market_demand_percentage: float
    expected_match_boost: str
    actionable_project: str

class SkillGapRoadmapOut(Schema):
    candidate_id: int
    target_role_analyzed: str
    total_jobs_analyzed: int
    candidate_verified_skills_count: int
    market_demand_breakdown: List[MarketDemandSkillOut]
    skills_to_build_next: List[SkillToBuildNextOut]

class NotificationItemOut(Schema):
    id: int
    title: str
    message: str
    notification_type: str
    related_application_id: Optional[int] = None
    related_listing_id: Optional[int] = None
    is_read: bool
    created_at: datetime

class NotificationsResponseOut(Schema):
    unread_count: int
    total_count: int
    notifications: List[NotificationItemOut]

class UpcomingInterviewOut(Schema):
    application_id: int
    listing_id: int
    listing_title: str
    company_name: str
    interview_date: datetime
    status: str

class UpcomingDeadlineOut(Schema):
    listing_id: int
    title: str
    company_name: str
    application_deadline: datetime
    stipend_or_ctc: str
    location: str

class DeadlinesHubOut(Schema):
    upcoming_interviews: List[UpcomingInterviewOut]
    upcoming_deadlines: List[UpcomingDeadlineOut]

# --- PHASE 7 SCHEMAS: MULTI-DOMAIN GOVERNMENT & AFFIRMATIVE ACTION SCHEMES ---

class GovernmentSchemeOutSchema(Schema):
    id: int
    title: str
    sponsoring_agency: str
    domain: str
    scheme_type: str
    target_gender: str
    benefit_summary: str
    description: str
    eligible_degrees: List[str] = []
    min_cgpa: Optional[float] = None
    application_deadline: Optional[datetime] = None
    official_portal_url: str
    status: str
    badge_color: str
    is_eligible: Optional[bool] = None
    match_reasons: List[str] = []
    created_at: datetime

class GovernmentSchemeCreateIn(Schema):
    title: str
    sponsoring_agency: str
    domain: Optional[str] = "ALL"
    scheme_type: Optional[str] = "SCHOLARSHIP"
    target_gender: Optional[str] = "FEMALE_ONLY"
    benefit_summary: str
    description: str
    eligible_degrees: Optional[List[str]] = []
    min_cgpa: Optional[float] = None
    application_deadline: Optional[datetime] = None
    official_portal_url: str
    badge_color: Optional[str] = "purple"

class LiveSchemesFeedOut(Schema):
    total_schemes: int
    user_gender: Optional[str] = None
    schemes: List[GovernmentSchemeOutSchema]
