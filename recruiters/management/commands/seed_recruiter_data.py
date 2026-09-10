from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import IndustrySector, StudentProfile
from recruiters.models import Company, RecruiterProfile, JobListing, JobApplication
from recruiters.search import index_job_listing

class Command(BaseCommand):
    help = "Seeds enterprise partner companies, recruiter identities, and verified job & internship postings"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[-] Seeding recruiter companies, listings, and applications..."))

        it_sector = IndustrySector.objects.filter(name__icontains="Information").first()
        mech_sector = IndustrySector.objects.filter(name__icontains="Mechanical").first()
        fin_sector = IndustrySector.objects.filter(name__icontains="Finance").first()

        # 1. COMPANIES
        companies_data = [
            {
                "name": "Google India",
                "registration_number": "CIN-U72900KA2003PTC033028",
                "is_verified": True,
                "website": "https://careers.google.com",
                "industry": it_sector,
                "branding_logo_url": "https://logo.clearbit.com/google.com",
                "description": "Global leader in search, cloud platforms, AI, and distributed systems engineering.",
                "headquarters": "Bengaluru, Karnataka, India"
            },
            {
                "name": "Tata Motors",
                "registration_number": "CIN-L28920MH1945PLC004520",
                "is_verified": True,
                "website": "https://www.tatamotors.com",
                "industry": mech_sector,
                "branding_logo_url": "https://logo.clearbit.com/tatamotors.com",
                "description": "Pioneering commercial and electric automotive engineering with advanced simulation and CAD design.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Morgan Stanley",
                "registration_number": "CIN-U67120MH1993FTC072704",
                "is_verified": True,
                "website": "https://www.morganstanley.com/careers",
                "industry": fin_sector,
                "branding_logo_url": "https://logo.clearbit.com/morganstanley.com",
                "description": "Multinational investment bank and financial services firm leading algorithmic quantitative trading.",
                "headquarters": "Mumbai, Maharashtra, India"
            }
        ]

        companies = {}
        for cdata in companies_data:
            comp, created = Company.objects.update_or_create(
                name=cdata["name"],
                defaults=cdata
            )
            companies[comp.name] = comp
            self.stdout.write(f"  [Company] {comp.name} (Verified: {comp.is_verified})")

        # 2. RECRUITERS
        recruiters_data = [
            {
                "username": "recruiter_google",
                "email": "talent@google.example",
                "company": companies["Google India"],
                "designation": "Senior Technical Recruiter",
                "department": "Core Infrastructure"
            },
            {
                "username": "recruiter_tata",
                "email": "careers@tatamotors.example",
                "company": companies["Tata Motors"],
                "designation": "Head of Campus Talent",
                "department": "Automotive R&D"
            },
            {
                "username": "recruiter_morgan",
                "email": "quant.hiring@morganstanley.example",
                "company": companies["Morgan Stanley"],
                "designation": "Director of Quantitative Recruitment",
                "department": "Institutional Securities"
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
                    "last_name": "Recruiter"
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

        # 2.1 FACULTY / ACADEMIA
        faculty_user, _ = User.objects.get_or_create(
            username="faculty_dean",
            defaults={
                "email": "dean@university.edu",
                "role": User.Role.ACADEMIA,
                "first_name": "Ramesh",
                "last_name": "Sharma",
                "phone_number": "+919811122334"
            }
        )
        faculty_user.set_password("password123")
        faculty_user.save()
        self.stdout.write(f"  [Faculty/Academia] {faculty_user.username} -> University Placement Cell (password123)")

        # 3. JOB LISTINGS
        listings_data = [
            {
                "company": companies["Google India"],
                "recruiter": recruiters["Google India"],
                "title": "Backend Systems Engineer",
                "role_type": JobListing.RoleType.FULL_TIME,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "22 - 28 LPA",
                "location": "Bengaluru, Karnataka (Hybrid)",
                "tenure": "Permanent",
                "open_positions": 4,
                "required_skills": ["python", "django", "postgresql", "docker", "redis"],
                "eligibility_criteria": {"min_cgpa": 7.5, "eligible_branches": ["Computer Science", "Information Technology"]},
                "description": "Architect high-throughput backend services, resilient relational schemas, and containerized microservices."
            },
            {
                "company": companies["Google India"],
                "recruiter": recruiters["Google India"],
                "title": "Frontend Engineering Intern",
                "role_type": JobListing.RoleType.INTERNSHIP,
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "INR 50,000/month",
                "location": "Bengaluru, Karnataka",
                "tenure": "6 Months",
                "open_positions": 3,
                "required_skills": ["react", "typescript", "tailwind", "nextjs"],
                "eligibility_criteria": {"min_cgpa": 7.0},
                "description": "Build dynamic, accessible web interfaces utilizing React, TypeScript, and modern component systems."
            },
            {
                "company": companies["Tata Motors"],
                "recruiter": recruiters["Tata Motors"],
                "title": "Autonomous Robotics & CAD Engineer",
                "role_type": JobListing.RoleType.FULL_TIME,
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
                "status": JobListing.ListingStatus.PUBLISHED,
                "stipend_or_ctc": "24 - 30 LPA",
                "location": "Mumbai, Maharashtra",
                "tenure": "Permanent",
                "open_positions": 2,
                "required_skills": ["python", "financial modeling", "sql", "excel", "statistics"],
                "eligibility_criteria": {"min_cgpa": 8.0, "eligible_branches": ["Computer Science", "Finance", "Mathematics"]},
                "description": "Develop algorithmic trading strategies, backtesting infrastructure, and statistical risk models."
            }
        ]

        for ldata in listings_data:
            listing, created = JobListing.objects.update_or_create(
                company=ldata["company"],
                title=ldata["title"],
                defaults=ldata
            )
            # Generate pgvector 384-dim dense embedding
            index_job_listing(listing)
            self.stdout.write(f"  [Listing] '{listing.title}' ({listing.stipend_or_ctc}) -> Vector indexed.")

        self.stdout.write(self.style.SUCCESS("[OK] Successfully seeded enterprise partner companies, recruiters, and vector-indexed listings."))

