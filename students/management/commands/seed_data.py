from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import StudentProfile

class Command(BaseCommand):
    help = "Seeds the database with sample students and profiles for testing"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing student profiles and non-admin users...")
        StudentProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating sample student accounts...")
        
        sample_students = [
            {
                "username": "alex_dev",
                "email": "alex@university.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543210",
                "github_handle": "alexdev99",
                "bio": "Full-stack developer interested in Django and React backend architectures.",
                "skills": ["Python", "Django", "PostgreSQL", "Docker"],
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "github_score": 85.5
            },
            {
                "username": "priya_s",
                "email": "priya@college.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543211",
                "github_handle": "priyacodes",
                "bio": "Frontend engineer passionate about designing beautiful user experiences with React and Tailwind CSS.",
                "skills": ["React", "JavaScript", "Tailwind CSS", "TypeScript", "HTML"],
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "github_score": 92.0
            },
            {
                "username": "rohan_m",
                "email": "rohan@academia.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543212",
                "github_handle": "rohan-ml",
                "bio": "Machine Learning engineer specialized in pandas, numpy, and python-driven API development.",
                "skills": ["Python", "numpy", "pandas", "Scikit-Learn", "Django"],
                "placement_status": StudentProfile.PlacementStatus.PLACED,
                "github_score": 78.2
            }
        ]

        for s_data in sample_students:
            user = User.objects.create_user(
                username=s_data["username"],
                email=s_data["email"],
                password=s_data["password"],
                role=s_data["role"],
                phone_number=s_data["phone_number"]
            )
            # Student profiles are linked to the user accounts
            StudentProfile.objects.create(
                user=user,
                github_handle=s_data["github_handle"],
                bio=s_data["bio"],
                skills=s_data["skills"],
                placement_status=s_data["placement_status"],
                github_score=s_data["github_score"]
            )
            self.stdout.write(f"Successfully created: {user.username} (Role: {user.role})")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with test dataset!"))
