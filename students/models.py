from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class StudentProfile(models.Model):
    # Link to the authentication user
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    
    github_handle = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Skill Mapping
    skills = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    
    class PlacementStatus(models.TextChoices):
        UNPLACED = 'UNPLACED', 'Unplaced'
        PLACED = 'PLACED', 'Placed'
        OPEN_TO_INTERN = 'OPEN_TO_INTERN', 'Open to Internships'

    placement_status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.UNPLACED
    )

    
    
   
    github_score = models.FloatField(default=0.0, help_text="Calculated score based on GitHub activity pipeline")

    class Meta:
        db_table = 'skillsetu_student_profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a StudentProfile record in PostgreSQL
    whenever a new User with the 'STUDENT' role is registered.
    """
    if created and instance.role == 'STUDENT':
        StudentProfile.objects.get_or_create(user=instance)