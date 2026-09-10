from django.db import models
from accounts.models import User

class Institution(models.Model):
    class InstitutionType(models.TextChoices):
        UNIVERSITY = "UNIVERSITY", "University"
        COLLEGE = "COLLEGE", "Autonomous College"
        INSTITUTE = "INSTITUTE", "National Institute / IIT / NIT / IIIT"
        POLYTECHNIC = "POLYTECHNIC", "Polytechnic / Vocational Institute"

    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text="AISHE code or institutional code")
    institution_type = models.CharField(
        max_length=30,
        choices=InstitutionType.choices,
        default=InstitutionType.COLLEGE
    )
    state = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    website = models.URLField(max_length=500, blank=True, null=True)
    nirf_rank = models.IntegerField(blank=True, null=True, help_text="NIRF ranking rank (if ranked)")
    is_verified = models.BooleanField(default=True)
    branding_logo_url = models.URLField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="departments"
    )
    name = models.CharField(max_length=150, help_text="e.g. Computer Science & Engineering, Finance & Commerce")
    code = models.CharField(max_length=20, blank=True, default="")
    head_of_department = models.CharField(max_length=150, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["institution", "name"]
        unique_together = ("institution", "name")

    def __str__(self):
        return f"{self.name} - {self.institution.name}"


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="faculty_profile"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_members"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_members"
    )
    designation = models.CharField(
        max_length=150,
        default="Placement Officer",
        help_text="e.g. Training & Placement Officer (TPO), HOD, Dean"
    )
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, default="")
    is_institution_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        inst_name = self.institution.name if self.institution else "Unassigned"
        return f"{self.user.username} ({self.designation} at {inst_name})"
