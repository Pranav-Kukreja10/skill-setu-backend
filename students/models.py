from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    # Lists stored in JSONFields automatically map to native JSONB arrays in PostgreSQL
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    github_handle = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Store dynamic data auto-parsed from the resume
    skills = models.JSONField(default=list, blank=True)
    projects = models.JSONField(default=list, blank=True)
    
    # Multi-Role Fitment Score Matrix (e.g. {"BACKEND_ENGINEER": {"score": 85, "fit_level": "High Match"}})
    role_fit_matrix = models.JSONField(default=dict, blank=True)
    
    placement_status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.UNPLACED
    )
    
    overall_confidence_score = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skillsetu_student_profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'STUDENT':
        StudentProfile.objects.get_or_create(user=instance)

class TestSession(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="test_sessions")
    target_role = models.CharField(max_length=100)
    questions_data = models.JSONField(help_text="Stores the full generated test, correct answers, and rubrics")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skillsetu_test_sessions'

