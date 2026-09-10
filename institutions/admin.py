from django.contrib import admin
from institutions.models import Institution, Department, FacultyProfile

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "institution_type", "state", "city", "nirf_rank", "is_verified", "created_at")
    search_fields = ("name", "code", "city", "state")
    list_filter = ("institution_type", "is_verified", "state")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "institution", "head_of_department", "created_at")
    search_fields = ("name", "code", "institution__name")
    list_filter = ("institution",)

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "designation", "institution", "department", "is_institution_admin", "created_at")
    search_fields = ("user__username", "user__email", "designation", "institution__name", "department__name")
    list_filter = ("institution", "is_institution_admin")
