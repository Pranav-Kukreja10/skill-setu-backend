from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Industry Recruiter'
        ACADEMIA = 'ACADEMIA', 'Academia Representative'
        ADMIN = 'ADMIN', 'System Administrator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Role classification to dictate portal workspace access"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_student(self) -> bool:
        return self.role == self.Role.STUDENT

    def is_recruiter(self) -> bool:
        return self.role == self.Role.RECRUITER

    def is_academia(self) -> bool:
        return self.role == self.Role.ACADEMIA

    class Meta:
        db_table = 'skillsetu_users'
