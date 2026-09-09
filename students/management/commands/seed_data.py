from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import StudentProfile

class Command(BaseCommand):
    help = "Seeds the database with sample students and profiles matching Phase 2 schema"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing student profiles and non-admin users...")
        StudentProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating sample student accounts and profiles...")
        
        sample_students = [
            {
                "username": "alex_dev",
                "email": "alex@university.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543210",
                "github_handle": "alexdev99",
                "bio": "Auto-extracted 4 skills and 1 project.",
                "skills": ["Python", "Django", "PostgreSQL", "Git"],
                "projects": [
                    {
                        "title": "E-Commerce REST API",
                        "technologies": ["Python", "Django", "PostgreSQL"],
                        "description": "Designed a secure and normalized database structure with complete JWT authentication routing."
                    }
                ],
                "role_fit_matrix": {
                    "Backend Engineer": {
                        "score": 85,
                        "fit_level": "High Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": None
                    },
                    "CAD Design Engineer": {
                        "score": 10,
                        "fit_level": "Low Match",
                        "sector": "Mechanical Engineering",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "overall_confidence_score": 0.0,
                "is_verified": False
            },
            {
                "username": "priya_s",
                "email": "priya@college.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543211",
                "github_handle": "priyacodes",
                "bio": "Auto-extracted 5 skills and 1 project.",
                "skills": ["React", "JavaScript", "Tailwind CSS", "Vite", "HTML5"],
                "projects": [
                    {
                        "title": "Portfolio Workspace",
                        "technologies": ["React", "Vite", "Tailwind CSS"],
                        "description": "Built a beautiful, responsive single-page application with optimized component states."
                    }
                ],
                "role_fit_matrix": {
                    "Frontend Engineer": {
                        "score": 90,
                        "fit_level": "High Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": None
                    },
                    "Financial Analyst": {
                        "score": 15,
                        "fit_level": "Low Match",
                        "sector": "Finance & Commerce",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "overall_confidence_score": 0.0,
                "is_verified": False
            }
        ]

        for s_data in sample_students:
            # 1. This triggers create_student_profile signal in the background
            user = User.objects.create_user(
                username=s_data["username"],
                email=s_data["email"],
                password=s_data["password"],
                role=s_data["role"],
                phone_number=s_data["phone_number"]
            )
            
            # 2. Safely retrieve the profile created by the signal and update its fields
            profile, created = StudentProfile.objects.get_or_create(user=user)
            profile.github_handle = s_data["github_handle"]
            profile.bio = s_data["bio"]
            profile.skills = s_data["skills"]
            profile.projects = s_data["projects"]
            profile.role_fit_matrix = s_data["role_fit_matrix"]
            profile.placement_status = s_data["placement_status"]
            profile.overall_confidence_score = s_data["overall_confidence_score"]
            profile.is_verified = s_data["is_verified"]
            profile.save()
            
            self.stdout.write(f"Successfully created user & profile for: {user.username}")

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with Phase 2 test profiles!"))
