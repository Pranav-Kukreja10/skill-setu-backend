from django.db import models
from django.conf import settings
from pgvector.django import VectorField

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
    contact_phone = models.CharField(max_length=30, blank=True)
    is_company_admin = models.BooleanField(default=False, help_text="Authorizes editing company verification, website, branding")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_recruiter_profiles'

    def __str__(self):
        comp = self.company.name if self.company else "Independent"
        return f"{self.user.username} ({self.designation} at {comp})"

class JobListing(models.Model):
    class RoleType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full-Time'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        CONTRACT = 'CONTRACT', 'Contract'

    class ListingStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'
        CLOSED = 'CLOSED', 'Closed'

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
    title = models.CharField(max_length=255, help_text="e.g. Junior Backend Engineer, Robotics Intern")
    role_type = models.CharField(max_length=20, choices=RoleType.choices, default=RoleType.FULL_TIME)
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.DRAFT)
    
    stipend_or_ctc = models.CharField(max_length=100, help_text="e.g. INR 40,000/month or 12 - 16 LPA")
    location = models.CharField(max_length=255, help_text="e.g. Bengaluru, Remote, Pune (Hybrid)")
    is_remote = models.BooleanField(default=False, help_text="Flag indicating remote work option")
    application_deadline = models.DateTimeField(null=True, blank=True, help_text="Last date to submit applications")
    tenure = models.CharField(max_length=100, blank=True, help_text="e.g. 6 Months, Permanent")
    open_positions = models.IntegerField(default=1)
    
    # Skills and requirements
    required_skills = models.JSONField(default=list, help_text="Standardized or raw skill requirements e.g. ['python', 'django', 'postgresql']")
    eligibility_criteria = models.JSONField(
        default=dict,
        blank=True,
        help_text="Arbitrary rules e.g. {'min_cgpa': 7.5, 'branches': ['CSE', 'IT'], 'min_confidence_score': 60}"
    )
    description = models.TextField(help_text="Detailed job description, responsibilities, and perks")
    
    # Denormalized NLP search corpus & 384-dim BGE dense embedding
    search_corpus = models.TextField(blank=True, default='')
    embedding = VectorField(dimensions=384, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_job_listings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company.name} ({self.status})"

class JobApplication(models.Model):
    class ApplicationStatus(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW = 'INTERVIEW', 'Interview'
        OFFERED = 'OFFERED', 'Offered'
        REJECTED = 'REJECTED', 'Rejected'

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skillsetu_job_applications'
        unique_together = ('listing', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.user.username} -> {self.listing.title} [{self.status}]"
