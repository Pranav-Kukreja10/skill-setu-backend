from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import StudentProfile
from students.search import index_student_profile

class Command(BaseCommand):
    help = "Seeds the database with sample multi-sector students, rich skills_matrix, target_roles, and indexes search corpora"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing student profiles and non-admin users...")
        StudentProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating sample student accounts, profiles, target roles, and embeddings across domains...")
        
        sample_students = [
            # 1. IT - Verified Backend Engineering Candidate
            {
                "username": "alex_dev",
                "email": "alex@university.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543210",
                "github_handle": "alexdev99",
                "bio": "Backend software engineer passionate about scalable REST APIs, relational databases, and microservices in Python and Django.",
                "target_roles": ["Backend Engineer", "Python Developer", "API Engineer"],
                "skills_matrix": {
                    "python": {"weight": 88, "project_evidence": 92, "experience_recency": 82},
                    "django": {"weight": 85, "project_evidence": 88, "experience_recency": 80},
                    "postgresql": {"weight": 82, "project_evidence": 85, "experience_recency": 78},
                    "rest api": {"weight": 84, "project_evidence": 86, "experience_recency": 80},
                    "docker": {"weight": 76, "project_evidence": 78, "experience_recency": 72},
                    "git": {"weight": 80, "project_evidence": 80, "experience_recency": 80},
                    "sql": {"weight": 80, "project_evidence": 82, "experience_recency": 76}
                },
                "projects": [
                    {
                        "title": "E-Commerce REST API Engine",
                        "technologies": ["Python", "Django", "PostgreSQL", "Docker", "REST API"],
                        "description": "Architected a high-throughput relational backend with JWT auth, payment gateway integration, and Docker containerization."
                    },
                    {
                        "title": "Distributed Task Scheduler",
                        "technologies": ["Python", "PostgreSQL", "Redis"],
                        "description": "Engineered an asynchronous task worker processing queue for background transactional emails."
                    }
                ],
                "role_fit_matrix": {
                    "Backend Engineer": {
                        "score": 88,
                        "fit_level": "High Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": 85.0
                    },
                    "CAD Design Engineer": {
                        "score": 5,
                        "fit_level": "Low Match",
                        "sector": "Mechanical Engineering",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "overall_confidence_score": 85.0,
                "is_verified": True
            },

            # 2. IT - Unverified Backend Candidate (Has matching skills but 0 test verification)
            {
                "username": "kevin_unverified",
                "email": "kevin@university.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543219",
                "github_handle": "kevinpadder",
                "bio": "Self-taught programmer claiming knowledge in Python, Django, and web servers with no verified assessments yet.",
                "target_roles": ["Junior Backend Developer"],
                "skills_matrix": {
                    "python": {"weight": 80, "project_evidence": 75, "experience_recency": 70},
                    "django": {"weight": 78, "project_evidence": 72, "experience_recency": 70},
                    "postgresql": {"weight": 75, "project_evidence": 70, "experience_recency": 65}
                },
                "projects": [
                    {
                        "title": "Simple Blog API",
                        "technologies": ["Python", "Django"],
                        "description": "Created basic CRUD endpoints for a personal blog application."
                    }
                ],
                "role_fit_matrix": {
                    "Backend Engineer": {
                        "score": 75,
                        "fit_level": "Medium Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "overall_confidence_score": 0.0,
                "is_verified": False
            },

            # 3. IT - Verified Frontend Engineering Candidate
            {
                "username": "priya_s",
                "email": "priya@college.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543211",
                "github_handle": "priyacodes",
                "bio": "Frontend developer specializing in modern UI/UX design, single-page web applications with React, Vite, and responsive styling.",
                "target_roles": ["Frontend Engineer", "React Developer", "UI Engineer"],
                "skills_matrix": {
                    "react": {"weight": 90, "project_evidence": 92, "experience_recency": 88},
                    "javascript": {"weight": 88, "project_evidence": 90, "experience_recency": 85},
                    "tailwind css": {"weight": 85, "project_evidence": 88, "experience_recency": 80},
                    "vite": {"weight": 80, "project_evidence": 82, "experience_recency": 78},
                    "html5": {"weight": 85, "project_evidence": 85, "experience_recency": 85}
                },
                "projects": [
                    {
                        "title": "Interactive Analytics Dashboard",
                        "technologies": ["React", "JavaScript", "Tailwind CSS", "Vite"],
                        "description": "Designed a sleek, dark-mode real-time telemetry dashboard with dynamic chart components."
                    }
                ],
                "role_fit_matrix": {
                    "Frontend Engineer": {
                        "score": 90,
                        "fit_level": "High Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": 88.0
                    },
                    "Financial Analyst": {
                        "score": 10,
                        "fit_level": "Low Match",
                        "sector": "Finance & Commerce",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "overall_confidence_score": 88.0,
                "is_verified": True
            },

            # 4. Mechanical Engineering - Verified CAD Design Candidate
            {
                "username": "rahul_cad",
                "email": "rahul@polytechnic.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543212",
                "github_handle": "rahuldesigns",
                "bio": "Mechanical design engineer experienced in CAD 3D modeling, finite element analysis (FEA), GD&T, and aerodynamic stress simulation.",
                "target_roles": ["CAD Design Engineer", "Mechanical Engineer", "FEA Analyst"],
                "skills_matrix": {
                    "solidworks": {"weight": 92, "project_evidence": 95, "experience_recency": 88},
                    "autocad": {"weight": 88, "project_evidence": 90, "experience_recency": 85},
                    "ansys": {"weight": 84, "project_evidence": 86, "experience_recency": 80},
                    "fea": {"weight": 85, "project_evidence": 88, "experience_recency": 80},
                    "gd&t": {"weight": 78, "project_evidence": 80, "experience_recency": 75},
                    "thermodynamics": {"weight": 75, "project_evidence": 76, "experience_recency": 74}
                },
                "projects": [
                    {
                        "title": "Automotive Chassis Stress Analysis",
                        "technologies": ["SolidWorks", "ANSYS", "FEA", "GD&T"],
                        "description": "Modeled a tubular space-frame chassis and conducted finite element static structural and torsion stress tests."
                    },
                    {
                        "title": "Industrial Centrifugal Pump Design",
                        "technologies": ["AutoCAD", "SolidWorks", "Fluid Mechanics"],
                        "description": "Prepared 2D engineering drawings and 3D CAD assemblies with manufacturing tolerances."
                    }
                ],
                "role_fit_matrix": {
                    "CAD Design Engineer": {
                        "score": 92,
                        "fit_level": "High Match",
                        "sector": "Mechanical Engineering",
                        "verified_confidence_score": 90.0
                    },
                    "Backend Engineer": {
                        "score": 5,
                        "fit_level": "Low Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "overall_confidence_score": 90.0,
                "is_verified": True
            },

            # 5. Finance & Commerce - Verified Financial Analyst Candidate
            {
                "username": "ananya_fin",
                "email": "ananya@business.edu",
                "password": "password123",
                "role": User.Role.STUDENT,
                "phone_number": "+919876543213",
                "github_handle": "ananyafin",
                "bio": "Financial analyst with expertise in discounted cash flow (DCF) valuation, corporate financial modeling, equity research, and Excel spreadsheets.",
                "target_roles": ["Financial Analyst", "Valuation Associate", "Equity Research Analyst"],
                "skills_matrix": {
                    "excel": {"weight": 95, "project_evidence": 96, "experience_recency": 92},
                    "dcf": {"weight": 90, "project_evidence": 92, "experience_recency": 88},
                    "financial modeling": {"weight": 90, "project_evidence": 92, "experience_recency": 86},
                    "valuation": {"weight": 88, "project_evidence": 90, "experience_recency": 85},
                    "corporate finance": {"weight": 85, "project_evidence": 86, "experience_recency": 82},
                    "tableau": {"weight": 80, "project_evidence": 82, "experience_recency": 78}
                },
                "projects": [
                    {
                        "title": "Public SaaS Company DCF Valuation Model",
                        "technologies": ["Excel", "Financial Modeling", "Valuation", "DCF"],
                        "description": "Constructed a 3-statement financial model and 5-year discounted cash flow forecasting with sensitivity analysis."
                    },
                    {
                        "title": "Portfolio Risk & Return Analytics",
                        "technologies": ["Tableau", "Excel", "Corporate Finance"],
                        "description": "Analyzed S&P 500 capital asset pricing model (CAPM) beta and Sharpe ratios across asset classes."
                    }
                ],
                "role_fit_matrix": {
                    "Financial Analyst": {
                        "score": 94,
                        "fit_level": "High Match",
                        "sector": "Finance & Commerce",
                        "verified_confidence_score": 91.0
                    },
                    "Frontend Engineer": {
                        "score": 8,
                        "fit_level": "Low Match",
                        "sector": "Information Technology",
                        "verified_confidence_score": None
                    }
                },
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "overall_confidence_score": 91.0,
                "is_verified": True
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
            
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            profile.github_handle = s_data["github_handle"]
            profile.bio = s_data["bio"]
            profile.target_roles = s_data.get("target_roles", [])
            profile.skills_matrix = s_data["skills_matrix"]
            profile.projects = s_data["projects"]
            profile.role_fit_matrix = s_data["role_fit_matrix"]
            profile.placement_status = s_data["placement_status"]
            profile.overall_confidence_score = s_data["overall_confidence_score"]
            profile.is_verified = s_data["is_verified"]
            profile.save()

            # Generate denormalized search_corpus and dense BGE embedding at index time
            try:
                index_student_profile(profile)
                self.stdout.write(f"Indexed search corpus & BGE embedding for: {user.username}")
            except Exception as e:
                self.stderr.write(f"Could not index embedding for {user.username}: {e}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded diverse test profiles with target roles & search indices!"))
