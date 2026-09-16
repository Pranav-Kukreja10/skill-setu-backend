from django.db import models
from django.conf import settings
from pgvector.django import VectorField, HnswIndex

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, blank=True, help_text="Corporate Identification / Tax Registration ID")
    is_verified = models.BooleanField(default=False, help_text="Institutional / Platform verification badge")
    website = models.URLField(blank=True, max_length=500)
    industry = models.ForeignKey(
        'students.IndustrySector',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies'
    )
    branding_logo_url = models.CharField(max_length=500, blank=True, help_text="Company logo or branding banner URL")
    description = models.TextField(blank=True)
    headquarters = models.CharField(max_length=255, blank=True, help_text="City, State, Country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_companies'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='recruiters',
        null=True,
        blank=True
    )
    designation = models.CharField(max_length=150, help_text="e.g. Lead Technical Recruiter, VP of Engineering")
    department = models.CharField(max_length=150, blank=True, help_text="e.g. Talent Acquisition, Infrastructure Team")
    bio = models.TextField(blank=True, default='', help_text="Recruiter professional biography and hiring philosophy")
    linkedin_url = models.URLField(max_length=500, blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='', help_text="City, Country")
    experience_years = models.FloatField(default=0.0, blank=True)
    hiring_mode_preference = models.CharField(
        max_length=20,
        default='COMPANY',
        choices=[('COMPANY', 'Company Hiring'), ('INDIVIDUAL', 'Independent Recruiter / Self Hiring')],
        help_text="Default hiring attribution mode"
    )
    contact_phone = models.CharField(max_length=30, blank=True)
    is_company_admin = models.BooleanField(default=False, help_text="Authorizes editing company verification, website, branding")
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Recruiter workflow, blind screening, and alert preferences"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_recruiter_profiles'

    def get_preferences(self) -> dict:
        defaults = {
            "common": {
                "theme": "system",
                "language": "en",
                "timezone": "Asia/Kolkata",
                "email_alerts": True,
                "in_app_alerts": True,
                "high_contrast": False,
                "reduce_motion": False,
            },
            "candidate_screening": {
                "default_blind_screening": False,
                "minimum_engineering_score_filter": 60.0,
                "require_verified_assessment": False,
                "preferred_nheqf_level": "LEVEL_5_5",
            },
            "hiring_workflow": {
                "auto_advance_high_match": False,
                "application_review_assignment": "MANUAL",
                "new_applicant_alert_frequency": "INSTANT",
            },
            "branding": {
                "show_diversity_employer_badge": True,
                "public_company_profile_visible": True,
            }
        }
        current = self.preferences or {}
        merged = {}
        for section, sec_defaults in defaults.items():
            merged[section] = {**sec_defaults, **current.get(section, {})}
        return merged

    def __str__(self):
        comp = self.company.name if self.company else "Independent"
        return f"{self.user.username} ({self.designation} at {comp})"

class JobListing(models.Model):
    class RoleType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full-Time Job'
        INTERNSHIP = 'INTERNSHIP', 'Student Internship'
        APPRENTICESHIP = 'APPRENTICESHIP', 'Apprenticeship'
        CONTRACT = 'CONTRACT', 'Contract'
        LIVE_PROJECT = 'LIVE_PROJECT', 'Live Industry Project'
        FACULTY_INTERNSHIP = 'FACULTY_INTERNSHIP', 'Faculty Internship'
        FDP = 'FDP', 'Faculty Development Program (FDP)'
        INDUSTRIAL_TRAINING = 'INDUSTRIAL_TRAINING', 'Industrial Training'
        CONSULTANCY = 'CONSULTANCY', 'Consultancy Opportunity'
        RESEARCH_PROJECT = 'RESEARCH_PROJECT', 'Collaborative Research Project'
        WORKSHOP = 'WORKSHOP', 'Industry Workshop'
        GUEST_LECTURE = 'GUEST_LECTURE', 'Guest Lecture / Mentorship'
        INNOVATION_CHALLENGE = 'INNOVATION_CHALLENGE', 'Innovation Challenge / Hackathon'

    class TargetAudience(models.TextChoices):
        STUDENT = 'STUDENT', 'Students & Candidates'
        FACULTY = 'FACULTY', 'Academicians & Faculty'
        ALL = 'ALL', 'Students & Faculty'

    class ListingStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'
        CLOSED = 'CLOSED', 'Closed'

    class HiringMode(models.TextChoices):
        COMPANY = 'COMPANY', 'Company Hiring'
        INDIVIDUAL = 'INDIVIDUAL', 'Independent Recruiter / Self Hiring'

    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name='job_listings'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='job_listings'
    )
    hiring_mode = models.CharField(
        max_length=20,
        choices=HiringMode.choices,
        default=HiringMode.COMPANY,
        help_text="Designates if hiring on behalf of a company or self/independent recruiter"
    )
    title = models.CharField(max_length=255, help_text="e.g. Junior Backend Engineer, Robotics Intern, EV Powertrain FDP")
    role_type = models.CharField(max_length=30, choices=RoleType.choices, default=RoleType.FULL_TIME)
    target_audience = models.CharField(max_length=20, choices=TargetAudience.choices, default=TargetAudience.STUDENT)
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.DRAFT)
    
    stipend_or_ctc = models.CharField(max_length=100, help_text="e.g. INR 40,000/month, 12 - 16 LPA, or Sponsored Grant")
    location = models.CharField(max_length=255, help_text="e.g. Bengaluru, Remote, Pune (Hybrid)")
    is_remote = models.BooleanField(default=False, help_text="Flag indicating remote work option")
    application_deadline = models.DateTimeField(null=True, blank=True, help_text="Last date to submit applications")
    tenure = models.CharField(max_length=100, blank=True, help_text="e.g. 6 Months, Permanent, 2 Weeks")
    open_positions = models.IntegerField(default=1)
    min_nheqf_level = models.CharField(
        max_length=25,
        default='LEVEL_4_5',
        blank=True,
        help_text="NEP 2020 Minimum qualification level: LEVEL_4_5 (Cert), LEVEL_5_0 (Dip), LEVEL_5_5 (3-Yr Deg), LEVEL_6_0 (4-Yr Deg)"
    )
    
    # Skills and requirements
    required_skills = models.JSONField(default=list, help_text="Standardized or raw skill requirements e.g. ['python', 'django', 'postgresql']")
    eligibility_criteria = models.JSONField(
        default=dict,
        blank=True,
        help_text="Arbitrary rules e.g. {'min_cgpa': 7.5, 'branches': ['CSE', 'IT'], 'min_confidence_score': 60}"
    )
    description = models.TextField(help_text="Detailed job description, responsibilities, and perks")
    
    # Diversity, Equity & Inclusion (DEI) attributes
    is_diversity_drive = models.BooleanField(default=False, help_text="Designates an affirmative action or diversity hiring initiative")
    target_gender = models.CharField(
        max_length=20,
        choices=[("ALL", "All Eligible"), ("FEMALE_ONLY", "Women Only / Female Candidates"), ("PREFER_DIVERSITY", "Diversity Preference")],
        default="ALL",
        help_text="Target demographic for the posting"
    )
    dei_initiatives = models.JSONField(
        default=list,
        blank=True,
        help_text="DEI perks & programs e.g. ['Women in Tech Mentorship', 'Inclusive Childcare Support', 'Equal Pay Certified']"
    )
    
    # Denormalized NLP search corpus & 384-dim BGE dense embedding
    search_corpus = models.TextField(blank=True, default='')
    embedding = VectorField(dimensions=384, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_job_listings'
        ordering = ['-created_at']
        indexes = [
            HnswIndex(
                name='job_listing_hnsw_idx',
                fields=['embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops'],
            ),
        ]

    @property
    def hiring_display_name(self) -> str:
        if self.hiring_mode in ['INDIVIDUAL', 'SELF']:
            user = self.recruiter.user if (self.recruiter and self.recruiter.user) else None
            if user:
                full = f"{user.first_name} {user.last_name}".strip()
                return full or user.username
            return "Independent Recruiter"
        return self.company.name if self.company else "Partner Enterprise"

    def __str__(self):
        return f"{self.title} @ {self.hiring_display_name} ({self.status}) [{self.role_type}]"

class JobApplication(models.Model):
    class ApplicationStatus(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW = 'INTERVIEW', 'Interview'
        OFFERED = 'OFFERED', 'Offered'
        REJECTED = 'REJECTED', 'Rejected'

    class InternshipStatus(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        TERMINATED = 'TERMINATED', 'Terminated'

    listing = models.ForeignKey(
        JobListing,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED
    )
    match_score = models.FloatField(default=0.0, help_text="Snapshot score (0.0 to 1.0) of candidate fitment at application time")
    recruiter_notes = models.TextField(blank=True, help_text="Private recruiter feedback and review remarks")
    interview_date = models.DateTimeField(null=True, blank=True, help_text="Scheduled interview timestamp")
    status_history = models.JSONField(
        default=list,
        blank=True,
        help_text="Chronological audit trail: [{'status': '...', 'timestamp': '...', 'note': '...'}]"
    )

    # PS Requirement: Progress tracking, mentor feedback, and internship completion records
    internship_status = models.CharField(
        max_length=30,
        choices=InternshipStatus.choices,
        default=InternshipStatus.NOT_STARTED,
        help_text="Live lifecycle status of the internship/training"
    )
    mentor_name = models.CharField(max_length=150, blank=True, default="", help_text="Assigned industry mentor / lead")
    mentor_designation = models.CharField(max_length=150, blank=True, default="", help_text="Mentor corporate designation")
    mentor_feedback = models.TextField(blank=True, default="", help_text="Qualitative mentor review and evaluation remarks")
    mentor_rating = models.FloatField(null=True, blank=True, help_text="Performance rating on a scale of 1.0 to 5.0")
    completion_certificate_url = models.CharField(max_length=500, blank=True, default="", help_text="Verified credential / certificate URL")
    internship_report_url = models.CharField(max_length=500, blank=True, default="", help_text="Student submitted final internship report URL")
    weekly_progress_logs = models.JSONField(
        default=list,
        blank=True,
        help_text="Weekly milestone updates: [{'week': 1, 'milestone': '...', 'hours': 40, 'mentor_remark': '...'}]"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_job_applications'
        unique_together = ('listing', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.user.username} -> {self.listing.title} [{self.status}]"


class LearningProgram(models.Model):
    """
    PS Requirement: Industry Learning Programs
    Companies can publish training programs, certification courses, workshops,
    and mentorship initiatives to help students and faculty acquire in-demand skills.
    """
    class ProgramType(models.TextChoices):
        TRAINING_PROGRAM = 'TRAINING_PROGRAM', 'Industry Training Program'
        CERTIFICATION_COURSE = 'CERTIFICATION_COURSE', 'Certification Course'
        WORKSHOP = 'WORKSHOP', 'Hands-on Workshop'
        MENTORSHIP = 'MENTORSHIP', 'Mentorship Initiative'
        GUEST_LECTURE = 'GUEST_LECTURE', 'Executive Guest Lecture'
        INNOVATION_CHALLENGE = 'INNOVATION_CHALLENGE', 'Innovation Challenge / Hackathon'

    class Mode(models.TextChoices):
        ONLINE = 'ONLINE', 'Online'
        OFFLINE = 'OFFLINE', 'Offline / On-Campus'
        HYBRID = 'HYBRID', 'Hybrid'

    class TargetAudience(models.TextChoices):
        STUDENT = 'STUDENT', 'Students & Candidates'
        FACULTY = 'FACULTY', 'Academicians & Faculty'
        ALL = 'ALL', 'Students & Faculty'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='learning_programs')
    title = models.CharField(max_length=255)
    program_type = models.CharField(max_length=30, choices=ProgramType.choices, default=ProgramType.WORKSHOP)
    target_audience = models.CharField(max_length=20, choices=TargetAudience.choices, default=TargetAudience.ALL)
    description = models.TextField(help_text="Detailed syllabus, prerequisites, and learning outcomes")
    skills_covered = models.JSONField(default=list, help_text="e.g. ['Cloud Architecture', 'EV Powertrain', 'Financial Modeling']")
    instructor_or_mentor = models.CharField(max_length=200, blank=True, help_text="Name & title of industry leader or mentor")
    duration = models.CharField(max_length=100, help_text="e.g. 4 Weeks, 2 Days, 40 Hours")
    mode = models.CharField(max_length=20, choices=Mode.choices, default=Mode.ONLINE)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    is_certified = models.BooleanField(default=True, help_text="Awards recognized industry certificate upon completion")
    branding_banner_url = models.CharField(max_length=500, blank=True, default="")
    
    enrolled_students = models.ManyToManyField('students.StudentProfile', blank=True, related_name='enrolled_learning_programs')
    enrolled_faculty = models.ManyToManyField('institutions.FacultyProfile', blank=True, related_name='enrolled_learning_programs')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_learning_programs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.company.name} [{self.program_type}]"

