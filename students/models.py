from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from pgvector.django import VectorField, HnswIndex

class IndustrySector(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. IT, Mechanical, Finance")
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'skillsetu_industry_sectors'
        
    def __str__(self):
        return self.name

class JobBenchmark(models.Model):
    sector = models.ForeignKey(IndustrySector, on_delete=models.CASCADE, related_name="benchmarks")
    role_title = models.CharField(max_length=100, unique=True, help_text="e.g. Backend Engineer, CAD Designer")
    
    # Required skills lists mapped directly to native JSONB fields in PostgreSQL
    core_skills = models.JSONField(default=list, help_text="List of mandatory core skills")
    methodology_skills = models.JSONField(default=list, help_text="List of methodology/architectural practices")
    tooling_skills = models.JSONField(default=list, help_text="List of tools/software utilities")

    class Meta:
        db_table = 'skillsetu_job_benchmarks'

    def __str__(self):
        return f"{self.role_title} ({self.sector.name})"

class StudentProfile(models.Model):
    class PlacementStatus(models.TextChoices):
        UNPLACED = 'UNPLACED', 'Unplaced'
        PLACED = 'PLACED', 'Placed'
        OPEN_TO_INTERN = 'OPEN_TO_INTERN', 'Open to Internships'

    class Gender(models.TextChoices):
        FEMALE = 'FEMALE', 'Female'
        MALE = 'MALE', 'Male'
        NON_BINARY = 'NON_BINARY', 'Non-Binary'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    github_handle = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Demographic attributes for affirmative action & government scheme matching
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
        blank=True,
        help_text="Self-identified gender for demographic opportunity matching and affirmative action schemes"
    )

    # Granular profile personalisation & notification preferences
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Granular feature and notification toggles: notifications, features, and privacy preferences"
    )
    
    # Store multi-dimensional skills with AI-graded evidence weights
    skills_matrix = models.JSONField(default=dict, blank=True)
    projects = models.JSONField(default=list, blank=True)
    
    # Multi-Role Fitment Score Matrix (e.g. {"Backend Engineer": {"score": 85, "fit_level": "High Match"}})
    role_fit_matrix = models.JSONField(default=dict, blank=True)
    
    placement_status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.UNPLACED
    )
    
    # Target job roles candidate is seeking (e.g. ['Backend Engineer', 'DevOps Engineer'])
    target_roles = models.JSONField(default=list, blank=True, help_text="Target job roles candidate is seeking")
    
    # Data Provenance: Preserved un-normalized raw string identifiers extracted directly from candidate resume
    raw_extracted_skills = models.JSONField(default=list, blank=True, help_text="Preserved raw resume string identifiers")
    
    # Institutional attributes for academic faculty reporting
    institution = models.CharField(max_length=255, blank=True, default='', help_text="College or University name")
    department = models.CharField(max_length=150, blank=True, default='', help_text="Academic department/branch (e.g. Computer Science, Mechanical)")
    degree = models.CharField(max_length=100, blank=True, default='', help_text="Academic degree e.g. B.Tech, B.S., M.S.")
    cgpa = models.FloatField(null=True, blank=True, help_text="Cumulative Grade Point Average (0.0 - 10.0)")
    graduation_year = models.IntegerField(null=True, blank=True, help_text="Graduation Year e.g. 2026")

    # Candidate professional experience & current designation
    current_designation = models.CharField(max_length=150, blank=True, default='', help_text="Current or most recent professional role (e.g. Senior Accountant, UI Designer)")
    experience_years = models.FloatField(default=0.0, blank=True, help_text="Total years of work experience (0 for students/freshers)")

    # Social & portfolio URLs
    github_url = models.URLField(max_length=500, blank=True, default='', help_text="GitHub profile URL")
    linkedin_url = models.URLField(max_length=500, blank=True, default='', help_text="LinkedIn profile URL")
    portfolio_url = models.URLField(max_length=500, blank=True, default='', help_text="Personal portfolio or website URL")

    # Structured industry certifications & credentials
    certifications = models.JSONField(
        default=list,
        blank=True,
        help_text="Industry certifications: [{'name': '...', 'issuer': '...', 'issue_year': 2024, 'credential_url': '...', 'skills_covered': []}]"
    )

    # Structured 4-tier skill categorization (technical_skills, frameworks, tools, soft_skills)
    skills_categorized = models.JSONField(
        default=dict,
        blank=True,
        help_text="Categorized skills: {'technical_skills': [], 'frameworks': [], 'tools': [], 'soft_skills': []}"
    )

    # PS Requirement: Digital Portfolio - Verified Internships & Experience
    internships = models.JSONField(
        default=list,
        blank=True,
        help_text="Completed internships: [{'company': '...', 'role': '...', 'duration': '...', 'mentor_feedback': '...', 'mentor_rating': 4.5, 'certificate_url': '...'}]"
    )

    # PS Requirement: Digital Portfolio - Verified Achievements & Honors
    achievements = models.JSONField(
        default=list,
        blank=True,
        help_text="Hackathons, awards, honors, publications: [{'title': '...', 'issuer': '...', 'year': 2024, 'description': '...'}]"
    )

    # PS Requirement: Academic Records & Transcripts
    academic_records = models.JSONField(
        default=list,
        blank=True,
        help_text="Semester GPA records & academic transcripts: [{'semester': 1, 'sgpa': 8.8, 'credits': 24}]"
    )
    
    overall_confidence_score = models.FloatField(default=0.0)
    profile_strength_score = models.FloatField(default=0.0, blank=True, help_text="Calculated profile strength score (0-100) based on 45/30/15/10 industry weighting")
    is_verified = models.BooleanField(default=False)
    
    # Denormalized text corpus & 384-dim BGE dense embedding for hybrid search
    search_corpus = models.TextField(blank=True, default='')
    embedding = VectorField(dimensions=384, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skillsetu_student_profiles'
        indexes = [
            HnswIndex(
                name='student_profile_hnsw_idx',
                fields=['embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops'],
            ),
        ]

    def get_preferences(self) -> dict:
        defaults = {
            "notifications": {
                "opportunity_alerts": True,
                "deadline_reminders": True,
                "scheme_alerts": True,
                "application_status_updates": True,
            },
            "features": {
                "show_affirmative_action_schemes": True,
                "show_diversity_job_badges": True,
                "smart_roadmap_recommendations": True,
                "reverse_matching_radar": True,
            },
            "privacy": {
                "participate_in_diversity_hiring": True,
                "share_profile_with_verified_recruiters": True,
            }
        }
        current = self.preferences or {}
        merged = {}
        for section, sec_defaults in defaults.items():
            merged[section] = {**sec_defaults, **current.get(section, {})}
        return merged

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        STATUS_CHANGE = 'STATUS_CHANGE', 'Status Change'
        INTERVIEW_SCHEDULED = 'INTERVIEW_SCHEDULED', 'Interview Scheduled'
        NEW_OPPORTUNITY = 'NEW_OPPORTUNITY', 'New Opportunity'
        DEADLINE_APPROACHING = 'DEADLINE_APPROACHING', 'Deadline Approaching'
        APPLICATION_REVIEW = 'APPLICATION_REVIEW', 'Application Review'
        NEW_SCHEME = 'NEW_SCHEME', 'New Government / Diversity Scheme'
        SYSTEM = 'SYSTEM', 'System Alert'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=35,
        choices=NotificationType.choices,
        default=NotificationType.STATUS_CHANGE
    )
    related_application_id = models.IntegerField(null=True, blank=True)
    related_listing_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skillsetu_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} [{self.notification_type}]"


class GovernmentScheme(models.Model):
    """
    Universal Multi-Domain Government & Affirmative Action Schemes
    Empowers candidates (especially women in STEM, finance, management, design)
    with direct portal access, verified grants, scholarships, and corporate DEI initiatives.
    """
    class Domain(models.TextChoices):
        TECH = 'TECH', 'Engineering & Technology'
        FINANCE = 'FINANCE', 'Commerce & Finance'
        MANAGEMENT = 'MANAGEMENT', 'Management & Business'
        DESIGN = 'DESIGN', 'Design & Creative Arts'
        ALL = 'ALL', 'Cross-Domain / Universal'

    class SchemeType(models.TextChoices):
        SCHOLARSHIP = 'SCHOLARSHIP', 'Scholarship & Financial Aid'
        INTERNSHIP = 'INTERNSHIP', 'Corporate Diversity Internship'
        MENTORSHIP = 'MENTORSHIP', 'Mentorship & Upskilling'
        RESEARCH_GRANT = 'RESEARCH_GRANT', 'Research Grant / Fellowship'
        INNOVATION_CHALLENGE = 'INNOVATION_CHALLENGE', 'Innovation Challenge / Hackathon'

    class TargetGender(models.TextChoices):
        FEMALE_ONLY = 'FEMALE_ONLY', 'Women / Female Candidates'
        ALL = 'ALL', 'All Eligible Candidates'

    class SchemeStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active / Open for Application'
        UPCOMING = 'UPCOMING', 'Upcoming'
        EXPIRED = 'EXPIRED', 'Application Closed'

    title = models.CharField(max_length=255)
    sponsoring_agency = models.CharField(max_length=255, help_text="e.g. AICTE / Ministry of Education, Amazon India, ICICI Bank")
    domain = models.CharField(max_length=30, choices=Domain.choices, default=Domain.ALL)
    scheme_type = models.CharField(max_length=30, choices=SchemeType.choices, default=SchemeType.SCHOLARSHIP)
    target_gender = models.CharField(max_length=20, choices=TargetGender.choices, default=TargetGender.FEMALE_ONLY)
    benefit_summary = models.CharField(max_length=255, help_text="e.g. INR 50,000/year + Tuition Waiver")
    description = models.TextField(help_text="Full program guidelines, eligibility, and deliverables")
    eligible_degrees = models.JSONField(default=list, blank=True, help_text="e.g. ['B.Tech', 'BCA', 'B.Com', 'MBA', 'B.Des']")
    min_cgpa = models.FloatField(null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    official_portal_url = models.URLField(max_length=500, help_text="Official portal or registration URL")
    status = models.CharField(max_length=20, choices=SchemeStatus.choices, default=SchemeStatus.ACTIVE)
    badge_color = models.CharField(max_length=30, default="purple", help_text="UI badge accent color")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_government_schemes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.domain}] ({self.status})"

class TestSession(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="test_sessions")
    target_role = models.CharField(max_length=100)
    questions_data = models.JSONField(help_text="Stores the full generated test, correct answers, and rubrics")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skillsetu_test_sessions'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role in ['STUDENT', 'CANDIDATE']:
        StudentProfile.objects.get_or_create(user=instance)
