from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import User
from students.models import IndustrySector, StudentProfile, Notification
from recruiters.models import Company, RecruiterProfile, JobListing, JobApplication, LearningProgram
from institutions.models import FacultyProfile, Institution, Department
from recruiters.search import index_job_listing
from students.search import index_student_profile

class Command(BaseCommand):
    help = "Seeds enterprise partner companies, recruiter identities, faculty opportunities, learning programs, and verified internship records"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[-] Seeding enterprise partner companies, recruiters, faculty opportunities, and learning programs..."))

        it_sector, _ = IndustrySector.objects.get_or_create(name="Information Technology", defaults={"description": "Software, Cloud, and AI"})
        mech_sector, _ = IndustrySector.objects.get_or_create(name="Mechanical Engineering", defaults={"description": "Automotive, Robotics, and Manufacturing"})
        fin_sector, _ = IndustrySector.objects.get_or_create(name="Finance & Banking", defaults={"description": "FinTech, Trading, and Investment Banking"})

        # 1. COMPANIES
        companies_data = [
            {
                "name": "Google India",
                "registration_number": "CIN-U72900KA2003PTC033028",
                "is_verified": True,
                "website": "https://careers.google.com",
                "industry": it_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
                "description": "Global leader in search, cloud computing, artificial intelligence, and hyperscale systems.",
                "headquarters": "Bengaluru, Karnataka, India"
            },
            {
                "name": "Tata Motors",
                "registration_number": "CIN-L28920MH1945PLC004520",
                "is_verified": True,
                "website": "https://www.tatamotors.com",
                "industry": mech_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Tata_logo.svg",
                "description": "Pioneering commercial and electric vehicle engineering, battery management, and CAD simulation.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Morgan Stanley",
                "registration_number": "CIN-U67120MH1993FTC072704",
                "is_verified": True,
                "website": "https://www.morganstanley.com/careers",
                "industry": fin_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Morgan_Stanley_Logo_1.svg",
                "description": "Multinational investment bank and financial services firm leading quantitative trading and risk analytics.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Microsoft India",
                "registration_number": "CIN-U72200DL1990PTC041040",
                "is_verified": True,
                "website": "https://careers.microsoft.com",
                "industry": it_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg",
                "description": "Worldwide leader in software, cloud infrastructure, AI models, and enterprise platforms.",
                "headquarters": "Hyderabad, Telangana, India"
            },
            {
                "name": "Larsen & Toubro",
                "registration_number": "CIN-L99999MH1946PLC004768",
                "is_verified": True,
                "website": "https://www.larsentoubro.com",
                "industry": mech_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/e/e5/L%26T.png",
                "description": "Indian multinational engaged in EPC projects, smart infrastructure, and high-tech defense engineering.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Zerodha Broking",
                "registration_number": "CIN-U65990KA2018PTC116578",
                "is_verified": True,
                "website": "https://zerodha.com",
                "industry": fin_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Zerodha_logo.svg/320px-Zerodha_logo.svg.png",
                "description": "India's largest retail stock broker and FinTech innovator pioneering low-latency trading infrastructure.",
                "headquarters": "Bengaluru, Karnataka, India"
            }
        ]

        companies = {}
        for cdata in companies_data:
            comp, created = Company.objects.update_or_create(
                name=cdata["name"],
                defaults=cdata
            )
            companies[comp.name] = comp
            status = "Created" if created else "Updated"
            self.stdout.write(f"  [Company] {comp.name} ({status}, Verified: {comp.is_verified})")

        # 2. RECRUITERS
        recruiters_data = [
            {
                "username": "recruiter_google",
                "email": "talent@google.example",
                "company": companies["Google India"],
                "designation": "Senior Technical Staffing Specialist",
                "department": "Core Systems Infrastructure"
            },
            {
                "username": "recruiter_tata",
                "email": "careers@tatamotors.example",
                "company": companies["Tata Motors"],
                "designation": "Head of University Relations & Talent",
                "department": "Electric Mobility Division"
            },
            {
                "username": "recruiter_morgan",
                "email": "quant.hiring@morganstanley.example",
                "company": companies["Morgan Stanley"],
                "designation": "Director of Quantitative Recruitment",
                "department": "Institutional Equities"
            },
            {
                "username": "recruiter_microsoft",
                "email": "india.talent@microsoft.example",
                "company": companies["Microsoft India"],
                "designation": "Principal University Talent Lead",
                "department": "Azure Core & AI"
            },
            {
                "username": "recruiter_lnt",
                "email": "hr@larsentoubro.example",
                "company": companies["Larsen & Toubro"],
                "designation": "Head of Academic Collaborations",
                "department": "Engineering R&D"
            },
            {
                "username": "recruiter_zerodha",
                "email": "careers@zerodha.example",
                "company": companies["Zerodha Broking"],
                "designation": "Lead Engineering Recruiter",
                "department": "Trading Tech & Infrastructure"
            }
        ]

        recruiters = {}
        for rdata in recruiters_data:
            u, _ = User.objects.get_or_create(
                username=rdata["username"],
                defaults={
                    "email": rdata["email"],
                    "role": User.Role.RECRUITER,
                    "first_name": rdata["username"].split('_')[1].capitalize(),
                    "last_name": "Lead"
                }
            )
            u.set_password("password123")
            u.save()
            rp, _ = RecruiterProfile.objects.update_or_create(
                user=u,
                defaults={
                    "company": rdata["company"],
                    "designation": rdata["designation"],
                    "department": rdata["department"],
                    "is_company_admin": True,
                    "contact_phone": "+91 98000 11223"
                }
            )
            recruiters[rdata["company"].name] = rp
            self.stdout.write(f"  [Recruiter] {u.username} -> {rdata['company'].name} (password123)")

        # 3. JOB LISTINGS (STUDENT & FACULTY COVERAGE)
        listings_data = [
            # 3.1 Student Full-Time & Internships
            {
                "company": companies["Google India"],
                "recruiter": recruiters["Google India"],
                "title": "Backend Systems Engineer",
                "role_type": JobListing.RoleType.FULL_TIME,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "22 - 28 LPA",
                "location": "Bengaluru, Karnataka (Hybrid)",
                "tenure": "Permanent",
                "open_positions": 4,
                "required_skills": ["python", "django", "postgresql", "docker", "redis", "rest api"],
                "eligibility_criteria": {"min_cgpa": 7.5, "eligible_branches": ["Computer Science", "Information Technology"]},
                "description": "Architect high-throughput backend services, resilient relational schemas, and containerized microservices."
            },
            {
                "company": companies["Google India"],
                "recruiter": recruiters["Google India"],
                "title": "Frontend Engineering Intern",
                "role_type": JobListing.RoleType.INTERNSHIP,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 50,00,000/year (INR 50,000/month)",
                "location": "Bengaluru, Karnataka",
                "tenure": "6 Months",
                "open_positions": 3,
                "required_skills": ["react", "typescript", "tailwind", "nextjs"],
                "eligibility_criteria": {"min_cgpa": 7.0},
                "is_diversity_drive": True,
                "target_gender": "FEMALE_ONLY",
                "dei_initiatives": ["Women in Tech Accelerated Track", "Google Women Techmakers Mentorship", "Equal Opportunity Employer"],
                "description": "Build dynamic, accessible web interfaces utilizing React, TypeScript, and modern component systems."
            },
            {
                "company": companies["Microsoft India"],
                "recruiter": recruiters["Microsoft India"],
                "title": "Cloud & AI Diversity Associate",
                "role_type": JobListing.RoleType.FULL_TIME,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "18 - 24 LPA",
                "location": "Hyderabad, Telangana (Hybrid)",
                "tenure": "Permanent",
                "open_positions": 5,
                "required_skills": ["azure", "python", "cloud architecture", "machine learning", "docker"],
                "eligibility_criteria": {"min_cgpa": 7.5},
                "is_diversity_drive": True,
                "target_gender": "FEMALE_ONLY",
                "dei_initiatives": ["TechSaksham Pipeline Program", "Executive Sponsorship for Women Engineers", "Inclusive Maternity & Childcare Benefits"],
                "description": "Accelerated cloud engineering program for female engineers to build planetary-scale Azure and Generative AI microservices."
            },
            {
                "company": companies["Tata Motors"],
                "recruiter": recruiters["Tata Motors"],
                "title": "Autonomous Robotics & CAD Engineer",
                "role_type": JobListing.RoleType.FULL_TIME,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "12 - 16 LPA",
                "location": "Pune, Maharashtra",
                "tenure": "Permanent",
                "open_positions": 2,
                "required_skills": ["cad", "solidworks", "ansys", "robotics", "matlab"],
                "eligibility_criteria": {"min_cgpa": 7.0, "eligible_branches": ["Mechanical Engineering", "Mechatronics"]},
                "description": "Perform mechanical simulation, kinematic stress analysis, and structural CAD modeling for electric vehicle platforms."
            },
            {
                "company": companies["Morgan Stanley"],
                "recruiter": recruiters["Morgan Stanley"],
                "title": "Quantitative Financial Analyst",
                "role_type": JobListing.RoleType.FULL_TIME,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "24 - 30 LPA",
                "location": "Mumbai, Maharashtra",
                "tenure": "Permanent",
                "open_positions": 2,
                "required_skills": ["python", "financial modeling", "sql", "excel", "statistics"],
                "eligibility_criteria": {"min_cgpa": 8.0, "eligible_branches": ["Computer Science", "Finance", "Mathematics"]},
                "is_diversity_drive": True,
                "target_gender": "PREFER_DIVERSITY",
                "dei_initiatives": ["Women in Quant Finance Network", "Global Diversity Exchange", "Career Returnship Support"],
                "description": "Develop algorithmic trading strategies, backtesting infrastructure, and statistical risk models."
            },
            {
                "company": companies["Zerodha Broking"],
                "recruiter": recruiters["Zerodha Broking"],
                "title": "Financial Engineering & Trading Systems Intern",
                "role_type": JobListing.RoleType.INTERNSHIP,
                "target_audience": JobListing.TargetAudience.STUDENT,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 45,000/month",
                "location": "Bengaluru, Karnataka (Remote)",
                "is_remote": True,
                "tenure": "6 Months",
                "open_positions": 3,
                "required_skills": ["python", "sql", "quantitative analysis", "financial modeling"],
                "eligibility_criteria": {"min_cgpa": 7.0},
                "description": "Work on order routing engines, market data streams, and quantitative financial models."
            },

            # 3.2 PS Requirement: Faculty Internships, FDPs & Collaborative Research
            {
                "company": companies["Google India"],
                "recruiter": recruiters["Google India"],
                "title": "Google Cloud Distributed Systems Faculty Fellowship",
                "role_type": JobListing.RoleType.FACULTY_INTERNSHIP,
                "target_audience": JobListing.TargetAudience.FACULTY,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 1,20,000/month Honorarium",
                "location": "Bengaluru, Karnataka (Hybrid)",
                "tenure": "8 Weeks (Summer)",
                "open_positions": 5,
                "required_skills": ["cloud architecture", "distributed systems", "kubernetes", "microservices"],
                "eligibility_criteria": {"min_designation": "Assistant Professor / Associate Professor", "departments": ["CSE", "IT"]},
                "description": "Immersion residency for university faculty to gain real-world industry experience in hyperscale cloud architectures and integrate findings into academic curricula."
            },
            {
                "company": companies["Tata Motors"],
                "recruiter": recruiters["Tata Motors"],
                "title": "Tata Motors EV Powertrain & Battery Management FDP",
                "role_type": JobListing.RoleType.FDP,
                "target_audience": JobListing.TargetAudience.FACULTY,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "Fully Sponsored + Certificate",
                "location": "Pune, Maharashtra",
                "tenure": "2 Weeks Intensive",
                "open_positions": 20,
                "required_skills": ["ev powertrain", "battery management", "matlab", "thermal analysis"],
                "eligibility_criteria": {"target_audience": "Academicians & Faculty in Mechanical, Electrical, and Automobile Engineering"},
                "description": "AICTE-recognized Faculty Development Program exploring EV battery thermal runaway prevention, regenerative braking, and powertrain simulation."
            },
            {
                "company": companies["Larsen & Toubro"],
                "recruiter": recruiters["Larsen & Toubro"],
                "title": "L&T Advanced Structural Dynamics & Industrial Training",
                "role_type": JobListing.RoleType.INDUSTRIAL_TRAINING,
                "target_audience": JobListing.TargetAudience.FACULTY,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 60,000 Stipend + Certification",
                "location": "Chennai, Tamil Nadu",
                "tenure": "4 Weeks",
                "open_positions": 8,
                "required_skills": ["structural engineering", "cad", "ansys", "civil engineering"],
                "eligibility_criteria": {"eligible_faculty": ["Civil", "Mechanical", "Structural Engineering"]},
                "description": "Industrial training residency providing hands-on practical exposure on mega-scale infrastructure projects and seismic structural analysis."
            },
            {
                "company": companies["Microsoft India"],
                "recruiter": recruiters["Microsoft India"],
                "title": "Microsoft AI for Sustainable Supply Chains Research Project",
                "role_type": JobListing.RoleType.RESEARCH_PROJECT,
                "target_audience": JobListing.TargetAudience.FACULTY,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 15,00,000 Research Grant",
                "location": "Hyderabad / Remote",
                "tenure": "1 Year Collaborative Grant",
                "open_positions": 2,
                "required_skills": ["machine learning", "deep learning", "python", "supply chain optimization"],
                "eligibility_criteria": {"qualification": "Ph.D. in Computer Science / Operations Research with published papers"},
                "description": "Joint academic-industry collaborative research initiative developing foundational AI algorithms for carbon-neutral logistics and resilient supply networks."
            },
            {
                "company": companies["Microsoft India"],
                "recruiter": recruiters["Microsoft India"],
                "title": "Microsoft GenAI & Autonomous Agents Innovation Challenge",
                "role_type": JobListing.RoleType.INNOVATION_CHALLENGE,
                "target_audience": JobListing.TargetAudience.ALL,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 10,00,000 Cash Prizes + Direct Interviews",
                "location": "Online / All India",
                "is_remote": True,
                "tenure": "48-Hour Hackathon + 2-Week Mentorship",
                "open_positions": 50,
                "required_skills": ["python", "generative ai", "llm", "rag", "docker"],
                "eligibility_criteria": {"open_to": "Students, Freshers, and Academic Teams across all Indian Universities"},
                "description": "National hackathon challenging participants to construct multi-agent AI systems for solving socio-economic challenges in health, agriculture, and education."
            }
        ]

        seeded_listings = {}
        for ldata in listings_data:
            listing, created = JobListing.objects.update_or_create(
                company=ldata["company"],
                title=ldata["title"],
                defaults=ldata
            )
            index_job_listing(listing)
            seeded_listings[listing.title] = listing
            self.stdout.write(f"  [Listing] '{listing.title}' ({listing.role_type}) -> Vector indexed.")

        # 4. INDUSTRY LEARNING PROGRAMS (PS REQUIREMENT)
        now = timezone.now()
        programs_data = [
            {
                "company": companies["Google India"],
                "title": "Google Cloud Architecture & Kubernetes Production Systems",
                "program_type": LearningProgram.ProgramType.TRAINING_PROGRAM,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Comprehensive 6-week curriculum covering cloud-native deployment, microservices reliability, and zero-trust security.",
                "skills_covered": ["Cloud Architecture", "Kubernetes", "Docker", "GCP", "Microservices"],
                "instructor_or_mentor": "Sundeep Rao, Principal Google Cloud Architect",
                "duration": "6 Weeks (40 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=20),
                "start_date": now + timedelta(days=25),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Tata Motors"],
                "title": "Advanced Electric Mobility & Battery Pack Engineering Workshop",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Hands-on engineering workshop demonstrating BMS telemetry, regenerative brake simulation, and battery pack design.",
                "skills_covered": ["EV Powertrain", "Battery Management", "CAD", "MATLAB", "SolidWorks"],
                "instructor_or_mentor": "Anil Deshmukh, Chief Technical Specialist - EV Powertrains",
                "duration": "2 Weeks (16 Hours)",
                "mode": LearningProgram.Mode.HYBRID,
                "registration_deadline": now + timedelta(days=15),
                "start_date": now + timedelta(days=18),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1558441719-8b489c63f7bc?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Microsoft India"],
                "title": "Azure AI & Enterprise LLM Applications Certification Track",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Industry certification track on building retrieval-augmented generation (RAG) pipelines and fine-tuning enterprise LLMs.",
                "skills_covered": ["Generative AI", "Azure OpenAI", "Python", "Vector Databases", "Prompt Engineering"],
                "instructor_or_mentor": "Dr. Meenakshi Sundaram, Partner AI Scientist, Microsoft",
                "duration": "4 Weeks",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=30),
                "start_date": now + timedelta(days=35),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Zerodha Broking"],
                "title": "Algorithmic Quantitative Trading & High-Frequency Systems Fellowship",
                "program_type": LearningProgram.ProgramType.MENTORSHIP,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Selective 8-week mentorship program paired with senior algorithmic traders to develop backtesting strategies on live market data.",
                "skills_covered": ["Financial Modeling", "Python", "Quantitative Analysis", "Algorithms", "SQL"],
                "instructor_or_mentor": "Kailash Nadh, CTO Zerodha",
                "duration": "8 Weeks",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=10),
                "start_date": now + timedelta(days=14),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80"
            }
        ]

        seeded_programs = {}
        for pdata in programs_data:
            prog, created = LearningProgram.objects.update_or_create(
                company=pdata["company"],
                title=pdata["title"],
                defaults=pdata
            )
            seeded_programs[prog.title] = prog
            self.stdout.write(f"  [LearningProgram] '{prog.title}' ({prog.program_type})")

        # 5. CANDIDATE DIGITAL PORTFOLIO & INTERNSHIP PROGRESS SEEDING
        alex_user = User.objects.filter(username="alex_dev").first()
        if alex_user:
            profile, _ = StudentProfile.objects.get_or_create(user=alex_user)
            
            # Enrich Alex's profile with full Digital Portfolio
            profile.institution = "Chitkara University, Punjab"
            profile.department = "Computer Science & Engineering"
            profile.degree = "B.Tech in Computer Science"
            profile.cgpa = 9.32
            profile.graduation_year = 2026
            profile.github_url = "https://github.com/alexdev99"
            profile.linkedin_url = "https://linkedin.com/in/alex-developer-verified"
            profile.portfolio_url = "https://alexdev.engineer"
            profile.placement_status = StudentProfile.PlacementStatus.PLACED
            profile.is_verified = True
            profile.overall_confidence_score = 88.0

            # Verified Certifications
            profile.certifications = [
                {
                    "name": "AWS Certified Solutions Architect - Associate",
                    "issuer": "Amazon Web Services",
                    "issue_year": 2024,
                    "credential_url": "https://aws.amazon.com/verification/AWS-PSA-9912",
                    "skills_covered": ["Python", "Cloud Architecture", "Docker", "PostgreSQL"]
                },
                {
                    "name": "Certified Kubernetes Administrator (CKA)",
                    "issuer": "Cloud Native Computing Foundation (CNCF)",
                    "issue_year": 2024,
                    "credential_url": "https://cncf.io/verify/CKA-88214-ALEX",
                    "skills_covered": ["Kubernetes", "Docker", "Microservices"]
                }
            ]

            # Verified Projects
            profile.projects = [
                {
                    "title": "High-Throughput Distributed Task Processing Queue",
                    "technologies": ["Python", "Django", "PostgreSQL", "Redis", "Docker"],
                    "description": "Engineered an asynchronous task broker handling 10,000+ jobs/sec with exponential backoff and persistent state tracking in PostgreSQL."
                },
                {
                    "title": "Low-Latency Market Order Book Simulator",
                    "technologies": ["Python", "C++", "FastAPI", "WebSockets"],
                    "description": "Constructed a price-time priority matching engine simulating L2 order book events with sub-millisecond tick execution."
                }
            ]

            # Completed Internships in Portfolio
            profile.internships = [
                {
                    "company": "Google India",
                    "role": "Backend Systems Intern",
                    "duration": "6 Months (Jan 2024 - Jun 2024)",
                    "mentor_name": "Dr. Arvind Varma",
                    "mentor_designation": "Principal Distributed Systems Architect, Google India",
                    "mentor_feedback": "Alex performed at the level of a senior L4 engineer. He designed and deployed a zero-copy gRPC RPC layer that reduced inter-service latency by 34%. Highly recommended for any systems team.",
                    "mentor_rating": 5.0,
                    "certificate_url": "https://skillsetu.cert.in/verify/GOOGLE-INTERN-2024-9841",
                    "report_url": "https://skillsetu.docs.in/reports/alex-google-internship-final.pdf",
                    "completed_at": "2024-06-30T18:00:00Z"
                }
            ]

            # Verified Achievements & Honors (SIH, IEEE, Academic)
            profile.achievements = [
                {
                    "title": "Smart India Hackathon (SIH) 2024 Finalist",
                    "issuer": "Ministry of Education & AICTE",
                    "year": 2024,
                    "description": "1st Runner Up nationally in the Artificial Intelligence category for building an autonomous skill-gap diagnostic platform.",
                    "proof_url": "https://sih.gov.in/certificates/2024/SIH-AI-RUNNER-UP-ALEX"
                },
                {
                    "title": "IEEE International Conference Cloud Computing - Published Author",
                    "issuer": "IEEE Computer Society",
                    "year": 2024,
                    "description": "Published research paper: 'Resilient Microservices with Asynchronous Backpressure and Zero-Copy IPC'.",
                    "proof_url": "https://ieeexplore.ieee.org/document/10488219"
                },
                {
                    "title": "Dean's Academic Excellence Honor Roll",
                    "issuer": "Chitkara University",
                    "year": 2023,
                    "description": "Awarded Top 1% Academic Distinction in Computer Science for outstanding semester GPA.",
                    "proof_url": "https://chitkara.edu.in/merit/2023/alex-dean-award"
                }
            ]

            # Academic Semester Transcripts
            profile.academic_records = [
                {"semester": 1, "sgpa": 8.90, "credits": 24},
                {"semester": 2, "sgpa": 9.15, "credits": 26},
                {"semester": 3, "sgpa": 9.20, "credits": 24},
                {"semester": 4, "sgpa": 9.40, "credits": 25},
                {"semester": 5, "sgpa": 9.35, "credits": 24},
                {"semester": 6, "sgpa": 9.50, "credits": 26}
            ]

            profile.save()
            index_student_profile(profile)
            self.stdout.write(self.style.SUCCESS(f"  [Student Portfolio] Alex Dev's Digital Portfolio updated with certifications, internships, achievements & transcripts."))

            # 5.1 Link Applications
            # App 1: Google Backend Systems Engineer (Completed Internship)
            google_listing = seeded_listings.get("Backend Systems Engineer")
            if google_listing:
                app_g, _ = JobApplication.objects.update_or_create(
                    listing=google_listing,
                    student=profile,
                    defaults={
                        "status": JobApplication.ApplicationStatus.OFFERED,
                        "match_score": 0.94,
                        "recruiter_notes": "Outstanding technical performance across all viva rounds and architectural challenges. Immediate hire recommendation.",
                        "internship_status": JobApplication.InternshipStatus.COMPLETED,
                        "mentor_name": "Dr. Arvind Varma",
                        "mentor_designation": "Principal Distributed Systems Architect",
                        "mentor_feedback": "Alex performed at the level of an L4 systems engineer. He designed and deployed a zero-copy gRPC RPC layer that reduced inter-service latency by 34%.",
                        "mentor_rating": 5.0,
                        "completion_certificate_url": "https://skillsetu.cert.in/verify/GOOGLE-INTERN-2024-9841",
                        "internship_report_url": "https://skillsetu.docs.in/reports/alex-google-internship-final.pdf",
                        "weekly_progress_logs": [
                            {"week": 1, "milestone": "Onboarding, repository setup, dev environment containerization", "hours": 40, "logged_at": "2024-01-12T17:00:00Z"},
                            {"week": 2, "milestone": "Benchmarked legacy REST pipeline latency; identified serialization bottlenecks", "hours": 42, "logged_at": "2024-01-19T17:00:00Z"},
                            {"week": 3, "milestone": "Designed Protobuf schema and high-throughput streaming RPC contracts", "hours": 40, "logged_at": "2024-01-26T17:00:00Z"},
                            {"week": 4, "milestone": "Implemented zero-copy serialization driver in Python & C++ bindings", "hours": 45, "logged_at": "2024-02-02T17:00:00Z"},
                            {"week": 5, "milestone": "Stress-tested microservice cluster with 25,000 req/sec load generator", "hours": 40, "logged_at": "2024-02-09T17:00:00Z"},
                            {"week": 6, "milestone": "Configured Prometheus telemetry, Grafana dashboards, and latency alerting", "hours": 40, "logged_at": "2024-02-16T17:00:00Z"},
                            {"week": 7, "milestone": "Canary deployment in staging; verified 34% p99 latency reduction", "hours": 40, "logged_at": "2024-02-23T17:00:00Z"},
                            {"week": 8, "milestone": "Production rollout, engineering documentation, and handover demo", "hours": 40, "logged_at": "2024-03-01T17:00:00Z"}
                        ]
                    }
                )
                self.stdout.write(f"  [Application] Alex -> Google ({app_g.status}, Internship: {app_g.internship_status}, 5.0/5.0)")

            # App 2: Tata Motors Autonomous Robotics (In-Progress Internship)
            tata_listing = seeded_listings.get("Autonomous Robotics & CAD Engineer")
            if tata_listing:
                app_t, _ = JobApplication.objects.update_or_create(
                    listing=tata_listing,
                    student=profile,
                    defaults={
                        "status": JobApplication.ApplicationStatus.INTERVIEW,
                        "match_score": 0.82,
                        "recruiter_notes": "Very strong software foundation; cross-training in CAN bus telemetry protocols.",
                        "internship_status": JobApplication.InternshipStatus.IN_PROGRESS,
                        "mentor_name": "Sneha Kulkarni",
                        "mentor_designation": "Director of Engineering, Tata Motors",
                        "mentor_feedback": "Demonstrating high diligence in real-time telemetry stream ingestion and BMS sensor calibration.",
                        "mentor_rating": 4.8,
                        "weekly_progress_logs": [
                            {"week": 1, "milestone": "Setup CAN bus emulation testbed and telemetry ingestion listener", "hours": 40, "deliverables_url": "https://github.com/alexdev99/canbus-telemetry", "logged_at": "2024-09-01T17:00:00Z"},
                            {"week": 2, "milestone": "Integrated Kalman filter for noisy sensor smoothing in vehicle simulation", "hours": 40, "deliverables_url": "https://github.com/alexdev99/kalman-filter-sim", "logged_at": "2024-09-08T17:00:00Z"}
                        ]
                    }
                )
                self.stdout.write(f"  [Application] Alex -> Tata Motors ({app_t.status}, Internship: {app_t.internship_status})")

            # Enroll Alex in Google Learning Program
            g_program = seeded_programs.get("Google Cloud Architecture & Kubernetes Production Systems")
            if g_program:
                g_program.enrolled_students.add(profile)
                self.stdout.write(f"  [Enrollment] Alex -> {g_program.title}")

        # 6. FACULTY COLLABORATION SEEDING (DR. RAMESH IYER & FACULTY DEAN)
        iyer_user = User.objects.filter(username="dr_iyer").first() or User.objects.filter(username="faculty_dean").first()
        if iyer_user:
            faculty_prof, _ = FacultyProfile.objects.get_or_create(user=iyer_user)

            # Enroll Faculty in Tata Motors Workshop
            t_program = seeded_programs.get("Advanced Electric Mobility & Battery Pack Engineering Workshop")
            if t_program:
                t_program.enrolled_faculty.add(faculty_prof)
                self.stdout.write(f"  [Faculty Enrollment] {iyer_user.username} -> {t_program.title}")

            # Notify Recruiter about Faculty FDP Application
            tata_fdp = seeded_listings.get("Tata Motors EV Powertrain & Battery Management FDP")
            if tata_fdp and tata_fdp.recruiter:
                Notification.objects.get_or_create(
                    user=tata_fdp.recruiter.user,
                    title=f"Faculty FDP Application: {tata_fdp.title}",
                    defaults={
                        "message": f"Prof. {iyer_user.first_name} {iyer_user.last_name} ({faculty_prof.designation} at Indian Institute of Technology Bombay) submitted an application for '{tata_fdp.title}'. Statement of Purpose: 'Looking to incorporate electric powertrain simulation into our university laboratory.'",
                        "notification_type": Notification.NotificationType.APPLICATION_REVIEW,
                        "related_listing_id": tata_fdp.id
                    }
                )
                self.stdout.write(f"  [Faculty Notification] {iyer_user.username} FDP application registered for Tata Motors.")

        self.stdout.write(self.style.SUCCESS("[OK] Successfully seeded realistic enterprise partner ecosystem, faculty opportunities, learning programs & digital portfolio records!"))
