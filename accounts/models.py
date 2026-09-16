from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student / Candidate'
        CANDIDATE = 'CANDIDATE', 'Candidate / Job Seeker'
        RECRUITER = 'RECRUITER', 'Industry Recruiter'
        ACADEMIA = 'ACADEMIA', 'Academia Representative'
        ADMIN = 'ADMIN', 'System Administrator'

    class AuthProvider(models.TextChoices):
        LOCAL = 'LOCAL', 'Email & Password'
        GOOGLE = 'GOOGLE', 'Google OAuth2'
        GITHUB = 'GITHUB', 'GitHub OAuth2'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Role classification to dictate portal workspace access"
    )
    auth_provider = models.CharField(
        max_length=20,
        choices=AuthProvider.choices,
        default=AuthProvider.LOCAL,
        help_text="Authentication identity provider"
    )
    provider_id = models.CharField(max_length=255, blank=True, null=True, help_text="External OAuth2 subject/user ID")
    avatar_url = models.URLField(max_length=500, blank=True, null=True, help_text="Profile picture from OAuth provider")
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_student(self) -> bool:
        return self.role in [self.Role.STUDENT, self.Role.CANDIDATE]

    def is_candidate(self) -> bool:
        return self.role in [self.Role.STUDENT, self.Role.CANDIDATE]

    def is_recruiter(self) -> bool:
        return self.role == self.Role.RECRUITER

    def is_academia(self) -> bool:
        return self.role == self.Role.ACADEMIA

    class Meta:
        db_table = 'skillsetu_users'
