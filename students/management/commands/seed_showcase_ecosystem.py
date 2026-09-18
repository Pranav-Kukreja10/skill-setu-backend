from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache

from accounts.models import User
from students.models import IndustrySector, StudentProfile, Notification, GovernmentScheme
from recruiters.models import Company, RecruiterProfile, JobListing, JobApplication, LearningProgram
from institutions.models import Institution, Department, FacultyProfile
from students.search import index_student_profile
from recruiters.search import index_job_listing

class Command(BaseCommand):
    help = "Seeds comprehensive, interconnected multi-sector ecosystem for SIH showcase."

    def handle(self, *args, **options):
        self.stdout.write("Flushing existing transactional data...")
        try:
            cache.clear()
        except Exception:
            pass

        Notification.objects.all().delete()
        JobApplication.objects.all().delete()
        JobListing.objects.all().delete()
        LearningProgram.objects.all().delete()
        FacultyProfile.objects.all().delete()
        RecruiterProfile.objects.all().delete()
        StudentProfile.objects.all().delete()
        Company.objects.all().delete()
        GovernmentScheme.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        now = timezone.now()

        it_sec, _ = IndustrySector.objects.get_or_create(
            name="Information Technology & Software Engineering",
            defaults={"description": "Fullstack, Cloud, Distributed Systems and AI"}
        )
        mech_sec, _ = IndustrySector.objects.get_or_create(
            name="Mechanical & Automotive Engineering",
            defaults={"description": "Robotics, EV Powertrain, CAD and Automation"}
        )
        fin_sec, _ = IndustrySector.objects.get_or_create(
            name="Finance, Banking & FinTech",
            defaults={"description": "Quantitative Finance, Trading Systems, Taxation and Valuation"}
        )
        design_sec, _ = IndustrySector.objects.get_or_create(
            name="Design, Creative Arts & UI/UX",
            defaults={"description": "Design Systems, Product Interaction, Accessibility and Prototyping"}
        )
        pharma_sec, _ = IndustrySector.objects.get_or_create(
            name="Pharmacy & Pharmaceutical Sciences",
            defaults={"description": "Formulation & Development, Drug Regulatory Affairs, Pharmacovigilance"}
        )

        iitb, _ = Institution.objects.get_or_create(
            name="Indian Institute of Technology (IIT) Bombay",
            defaults={
                "code": "IITB",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "city": "Mumbai",
                "state": "Maharashtra",
                "nirf_rank": 3,
                "is_verified": True
            }
        )
        nits, _ = Institution.objects.get_or_create(
            name="National Institute of Technology (NIT) Karnataka, Surathkal",
            defaults={
                "code": "NITK",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "city": "Surathkal",
                "state": "Karnataka",
                "nirf_rank": 12,
                "is_verified": True
            }
        )
        du_srcc, _ = Institution.objects.get_or_create(
            name="Shri Ram College of Commerce, Delhi University",
            defaults={
                "code": "DU-SRCC",
                "institution_type": Institution.InstitutionType.COLLEGE,
                "city": "New Delhi",
                "state": "Delhi",
                "nirf_rank": 1,
                "is_verified": True
            }
        )
        nid, _ = Institution.objects.get_or_create(
            name="National Institute of Design (NID) Ahmedabad",
            defaults={
                "code": "NID-AMD",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "city": "Ahmedabad",
                "state": "Gujarat",
                "nirf_rank": 1,
                "is_verified": True
            }
        )
        chitkara, _ = Institution.objects.get_or_create(
            name="Chitkara University, Punjab",
            defaults={
                "code": "CU-PB",
                "institution_type": Institution.InstitutionType.UNIVERSITY,
                "city": "Rajpura",
                "state": "Punjab",
                "nirf_rank": 40,
                "is_verified": True
            }
        )
        bits, _ = Institution.objects.get_or_create(
            name="Birla Institute of Technology and Science (BITS) Pilani",
            defaults={
                "code": "BITS-PILANI",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "city": "Pilani",
                "state": "Rajasthan",
                "nirf_rank": 20,
                "is_verified": True
            }
        )
        dtu, _ = Institution.objects.get_or_create(
            name="Delhi Technological University (DTU)",
            defaults={
                "code": "DTU-DELHI",
                "institution_type": Institution.InstitutionType.UNIVERSITY,
                "city": "New Delhi",
                "state": "Delhi",
                "nirf_rank": 29,
                "is_verified": True
            }
        )
        dept_bits_cse, _ = Department.objects.get_or_create(
            institution=bits,
            name="Computer Science & Engineering",
            defaults={"code": "CSE", "head_of_department": "Dr. Shan Balasubramaniam"}
        )
        dept_dtu_cse, _ = Department.objects.get_or_create(
            institution=dtu,
            name="Computer Science & Engineering",
            defaults={"code": "CSE", "head_of_department": "Dr. Rajeev Kumar"}
        )

        dept_iitb_cse, _ = Department.objects.get_or_create(
            institution=iitb,
            name="Computer Science & Engineering",
            defaults={"code": "CSE", "head_of_department": "Dr. Ramesh Iyer"}
        )
        dept_iitb_mech, _ = Department.objects.get_or_create(
            institution=iitb,
            name="Mechanical Engineering",
            defaults={"code": "ME", "head_of_department": "Dr. Sneha Kulkarni"}
        )
        dept_nits_cse, _ = Department.objects.get_or_create(
            institution=nits,
            name="Computer Science & Engineering",
            defaults={"code": "CSE", "head_of_department": "Dr. Suresh Rao"}
        )
        dept_du_fin, _ = Department.objects.get_or_create(
            institution=du_srcc,
            name="Commerce & Financial Studies",
            defaults={"code": "CFS", "head_of_department": "Dr. Meenakshi Sharma"}
        )
        dept_nid_ux, _ = Department.objects.get_or_create(
            institution=nid,
            name="Interaction & UI/UX Design",
            defaults={"code": "UXD", "head_of_department": "Prof. Aditi Rao"}
        )
        dept_cu_cse, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Computer Science & Engineering",
            defaults={"code": "CSE", "head_of_department": "Dr. Aman Deep"}
        )
        dept_cu_ece, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Electronics & Communication Engineering",
            defaults={"code": "ECE", "head_of_department": "Dr. Sandeep Arora"}
        )
        dept_cu_mech, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Mechanical Engineering",
            defaults={"code": "MECH", "head_of_department": "Dr. Gurwinder Singh"}
        )
        dept_cu_civil, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Civil Engineering",
            defaults={"code": "CIVIL", "head_of_department": "Dr. Pankaj Kumar"}
        )
        dept_cu_cbs, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara Business School",
            defaults={"code": "CBS", "head_of_department": "Dr. Babita Singla"}
        )
        dept_cu_cds, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara Design School",
            defaults={"code": "CDS", "head_of_department": "Prof. Nitin Dutt"}
        )
        dept_cu_pharm, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara College of Pharmacy",
            defaults={"code": "CCP", "head_of_department": "Dr. Sandeep Sharma"}
        )
        dept_cu_health, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara School of Health Sciences",
            defaults={"code": "CSHS", "head_of_department": "Dr. Sonika Bakshi"}
        )
        dept_cu_arch, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara School of Planning & Architecture",
            defaults={"code": "CSPA", "head_of_department": "Prof. I.J.S. Bakshi"}
        )
        dept_cu_hotel, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara College of Hotel Management",
            defaults={"code": "CCHM", "head_of_department": "Chef Amit Sood"}
        )
        dept_cu_mass, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara School of Mass Communication",
            defaults={"code": "CSMC", "head_of_department": "Dr. Ashutosh Mishra"}
        )
        dept_cu_law, _ = Department.objects.get_or_create(
            institution=chitkara,
            name="Chitkara Law School",
            defaults={"code": "CLS", "head_of_department": "Dr. Jasneet Kaur"}
        )

        comp_google = Company.objects.create(
            name="Google India",
            registration_number="CIN-U72900KA2003PTC033028",
            is_verified=True,
            website="https://careers.google.com",
            industry=it_sec,
            description="Global leader in search, cloud platforms, artificial intelligence, and hyperscale systems.",
            headquarters="Bengaluru, Karnataka, India"
        )
        comp_tata = Company.objects.create(
            name="Tata Motors",
            registration_number="CIN-L28920MH1945PLC004520",
            is_verified=True,
            website="https://www.tatamotors.com",
            industry=mech_sec,
            description="Pioneering commercial and electric vehicle mobility, battery telemetry, and robotics.",
            headquarters="Mumbai, Maharashtra, India"
        )
        comp_microsoft = Company.objects.create(
            name="Microsoft India",
            registration_number="CIN-U72200DL1990PTC041040",
            is_verified=True,
            website="https://careers.microsoft.com",
            industry=it_sec,
            description="Global technology corporation engineering planetary cloud infrastructure, AI models, and developer tools.",
            headquarters="Hyderabad, Telangana, India"
        )
        comp_morgan = Company.objects.create(
            name="Morgan Stanley",
            registration_number="CIN-U67120MH1993FTC072704",
            is_verified=True,
            website="https://www.morganstanley.com",
            industry=fin_sec,
            description="Global investment bank and financial services firm leading quantitative trading and risk analytics.",
            headquarters="Mumbai, Maharashtra, India"
        )
        comp_zerodha = Company.objects.create(
            name="Zerodha Broking",
            registration_number="CIN-U65990KA2018PTC116578",
            is_verified=True,
            website="https://zerodha.com",
            industry=fin_sec,
            description="India's largest retail stock broker and FinTech innovator pioneering low-latency trading infrastructure.",
            headquarters="Bengaluru, Karnataka, India"
        )
        comp_sunpharma = Company.objects.create(
            name="Sun Pharmaceutical Industries",
            registration_number="CIN-L24230GJ1993PLC019050",
            is_verified=True,
            website="https://www.sunpharma.com",
            industry=pharma_sec,
            description="Global specialty pharmaceutical company leading drug formulation research, regulatory compliance, and generic therapeutics.",
            headquarters="Mumbai, Maharashtra, India"
        )

        u_rec_google = User.objects.create_user(
            username="vikram_malhotra",
            email="vikram.malhotra@google.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Vikram",
            last_name="Malhotra",
            phone_number="+919811122334",
            is_email_verified=True
        )
        rp_google = RecruiterProfile.objects.create(
            user=u_rec_google,
            company=comp_google,
            designation="Principal University Talent Lead",
            department="Core Infrastructure & Engineering",
            is_company_admin=True,
            contact_phone="+919811122334"
        )

        u_rec_google_ai = User.objects.create_user(
            username="neha_gupta",
            email="neha.gupta@google.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Neha",
            last_name="Gupta",
            phone_number="+919811122335",
            is_email_verified=True
        )
        rp_google_ai = RecruiterProfile.objects.create(
            user=u_rec_google_ai,
            company=comp_google,
            designation="AI & Cloud Campus Talent Partner",
            department="Google Cloud AI",
            is_company_admin=False,
            contact_phone="+919811122335"
        )

        u_rec_tata = User.objects.create_user(
            username="priya_nair",
            email="priya.nair@tatamotors.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Priya",
            last_name="Nair",
            phone_number="+919822233445",
            is_email_verified=True
        )
        rp_tata = RecruiterProfile.objects.create(
            user=u_rec_tata,
            company=comp_tata,
            designation="Head of University Relations & Talent",
            department="Electric Mobility Division",
            is_company_admin=True,
            contact_phone="+919822233445"
        )

        u_rec_ms = User.objects.create_user(
            username="arjun_kapoor",
            email="arjun.kapoor@microsoft.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Arjun",
            last_name="Kapoor",
            phone_number="+919833344556",
            is_email_verified=True
        )
        rp_ms = RecruiterProfile.objects.create(
            user=u_rec_ms,
            company=comp_microsoft,
            designation="Principal University Recruiting Lead",
            department="Azure Cloud & AI",
            is_company_admin=True,
            contact_phone="+919833344556"
        )

        u_rec_morgan = User.objects.create_user(
            username="anita_desai",
            email="anita.desai@morganstanley.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Anita",
            last_name="Desai",
            phone_number="+919844455667",
            is_email_verified=True
        )
        rp_morgan = RecruiterProfile.objects.create(
            user=u_rec_morgan,
            company=comp_morgan,
            designation="Director of Quantitative Recruitment",
            department="Institutional Equities & Quant Analytics",
            is_company_admin=True,
            contact_phone="+919844455667"
        )

        u_rec_zerodha = User.objects.create_user(
            username="kailash_hr",
            email="kailash.hr@zerodha.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Kailash",
            last_name="Nadh",
            phone_number="+919855566778",
            is_email_verified=True
        )
        rp_zerodha = RecruiterProfile.objects.create(
            user=u_rec_zerodha,
            company=comp_zerodha,
            designation="Lead Engineering Recruiter",
            department="Trading Tech & Core Systems",
            is_company_admin=True,
            contact_phone="+919855566778"
        )

        u_rec_pharma = User.objects.create_user(
            username="dr_kavita_nair",
            email="kavita.nair@sunpharma.com",
            password="password123",
            role=User.Role.RECRUITER,
            first_name="Kavita",
            last_name="Nair",
            phone_number="+919855566779",
            is_email_verified=True
        )
        rp_pharma = RecruiterProfile.objects.create(
            user=u_rec_pharma,
            company=comp_sunpharma,
            designation="Director of Scientific Talent Acquisition",
            department="Global Regulatory & Clinical Formulation",
            is_company_admin=True,
            contact_phone="+919855566779"
        )

        u_faculty_iitb = User.objects.create_user(
            username="dr_iyer",
            email="dr.iyer@iitb.ac.in",
            password="password123",
            role=User.Role.ACADEMIA,
            first_name="Ramesh",
            last_name="Iyer",
            phone_number="+919866677889",
            is_email_verified=True
        )
        fp_iitb = FacultyProfile.objects.create(
            user=u_faculty_iitb,
            institution=iitb,
            department=dept_iitb_cse,
            employee_id="IITB-FAC-8812",
            designation="Professor & Dean of Corporate Relations",
            is_institution_admin=True,
            contact_phone="+919866677889"
        )

        u_faculty_du = User.objects.create_user(
            username="dr_meenakshi",
            email="dr.meenakshi@du.ac.in",
            password="password123",
            role=User.Role.ACADEMIA,
            first_name="Meenakshi",
            last_name="Sharma",
            phone_number="+919877788990",
            is_email_verified=True
        )
        fp_du = FacultyProfile.objects.create(
            user=u_faculty_du,
            institution=du_srcc,
            department=dept_du_fin,
            employee_id="DU-FAC-9921",
            designation="Professor & Head of Department",
            is_institution_admin=True,
            contact_phone="+919877788990"
        )

        u_faculty_nid = User.objects.create_user(
            username="prof_aditi",
            email="prof.aditi@nid.ac.in",
            password="password123",
            role=User.Role.ACADEMIA,
            first_name="Aditi",
            last_name="Rao",
            phone_number="+919888899001",
            is_email_verified=True
        )
        fp_nid = FacultyProfile.objects.create(
            user=u_faculty_nid,
            institution=nid,
            department=dept_nid_ux,
            employee_id="NID-FAC-4410",
            designation="Associate Professor of Interaction Architecture",
            is_institution_admin=True,
            contact_phone="+919888899001"
        )

        u_faculty_chitkara = User.objects.create_user(
            username="dr_babita",
            email="dr.babita@chitkara.edu.in",
            password="password123",
            role=User.Role.ACADEMIA,
            first_name="Babita",
            last_name="Singla",
            phone_number="+919899900112",
            is_email_verified=True
        )
        fp_chitkara = FacultyProfile.objects.create(
            user=u_faculty_chitkara,
            institution=chitkara,
            department=dept_cu_cbs,
            employee_id="CU-FAC-1008",
            designation="Dean & Professor of Management Studies",
            is_institution_admin=True,
            contact_phone="+919899900112"
        )

        l_google_backend = JobListing.objects.create(
            company=comp_google,
            recruiter=rp_google,
            title="Backend Systems Engineer",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="24 - 32 LPA",
            location="Bengaluru, Karnataka (Hybrid)",
            tenure="Permanent",
            open_positions=4,
            required_skills=["python", "django", "postgresql", "docker", "redis", "rest api"],
            eligibility_criteria={"min_cgpa": 7.5, "eligible_branches": ["Computer Science", "Information Technology"]},
            description="Architect high-throughput backend services, resilient relational schemas, and containerized microservices in Python.",
            application_deadline=now + timedelta(days=45)
        )
        index_job_listing(l_google_backend)

        l_google_frontend = JobListing.objects.create(
            company=comp_google,
            recruiter=rp_google_ai,
            title="Frontend Engineering Intern",
            role_type=JobListing.RoleType.INTERNSHIP,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="INR 50,000 / month",
            location="Bengaluru, Karnataka",
            tenure="6 Months",
            open_positions=3,
            required_skills=["react", "typescript", "tailwind", "nextjs", "figma"],
            eligibility_criteria={"min_cgpa": 7.0},
            is_diversity_drive=True,
            target_gender="FEMALE_ONLY",
            dei_initiatives=["Google Women Techmakers", "Accelerated Conversion Pipeline"],
            description="Design and implement dynamic, accessible web interfaces utilizing React, TypeScript, and modern component systems.",
            application_deadline=now + timedelta(days=30)
        )
        index_job_listing(l_google_frontend)

        l_ms_cloud_dei = JobListing.objects.create(
            company=comp_microsoft,
            recruiter=rp_ms,
            title="Cloud & AI Diversity Associate",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="18 - 25 LPA",
            location="Hyderabad, Telangana (Hybrid)",
            tenure="Permanent",
            open_positions=6,
            required_skills=["azure", "python", "cloud architecture", "machine learning", "docker"],
            eligibility_criteria={"min_cgpa": 7.5},
            is_diversity_drive=True,
            target_gender="FEMALE_ONLY",
            dei_initiatives=["TechSaksham National Pipeline", "Executive Mentorship for Women in Tech"],
            description="Accelerated engineering track for female engineers to build scalable Azure cloud architectures and GenAI microservices.",
            application_deadline=now + timedelta(days=25)
        )
        index_job_listing(l_ms_cloud_dei)

        l_tata_robotics = JobListing.objects.create(
            company=comp_tata,
            recruiter=rp_tata,
            title="Autonomous Robotics & CAD Engineer",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="14 - 18 LPA",
            location="Pune, Maharashtra",
            tenure="Permanent",
            open_positions=3,
            required_skills=["cad", "solidworks", "ansys", "robotics", "python"],
            eligibility_criteria={"min_cgpa": 7.0, "eligible_branches": ["Mechanical", "Mechatronics", "Computer Science"]},
            description="Perform structural CAD modeling, kinematic stress simulation, and telemetry protocol integration for electric vehicles.",
            application_deadline=now + timedelta(days=35)
        )
        index_job_listing(l_tata_robotics)

        l_morgan_quant = JobListing.objects.create(
            company=comp_morgan,
            recruiter=rp_morgan,
            title="Quantitative Financial Analyst",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="25 - 32 LPA",
            location="Mumbai, Maharashtra",
            tenure="Permanent",
            open_positions=2,
            required_skills=["excel", "financial modeling", "dcf", "valuation", "python", "sql"],
            eligibility_criteria={"min_cgpa": 8.0, "eligible_branches": ["Commerce", "Finance", "Computer Science"]},
            is_diversity_drive=True,
            target_gender="PREFER_DIVERSITY",
            description="Construct financial models, valuation projections, and algorithmic risk telemetry for institutional equities.",
            application_deadline=now + timedelta(days=20)
        )
        index_job_listing(l_morgan_quant)

        l_zerodha_intern = JobListing.objects.create(
            company=comp_zerodha,
            recruiter=rp_zerodha,
            title="Trading Systems & FinTech Intern",
            role_type=JobListing.RoleType.INTERNSHIP,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="INR 45,000 / month",
            location="Bengaluru, Karnataka (Remote)",
            is_remote=True,
            tenure="6 Months",
            open_positions=4,
            required_skills=["python", "sql", "quantitative analysis", "financial modeling"],
            eligibility_criteria={"min_cgpa": 7.0},
            description="Develop low-latency market data streams, order routing listeners, and algorithmic financial pipelines.",
            application_deadline=now + timedelta(days=15)
        )
        index_job_listing(l_zerodha_intern)

        l_google_faculty = JobListing.objects.create(
            company=comp_google,
            recruiter=rp_google,
            title="Google Cloud Distributed Systems Faculty Fellowship",
            role_type=JobListing.RoleType.FACULTY_INTERNSHIP,
            target_audience=JobListing.TargetAudience.FACULTY,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="INR 1,20,000 / month Honorarium",
            location="Bengaluru, Karnataka (Hybrid)",
            tenure="8 Weeks (Summer)",
            open_positions=5,
            required_skills=["cloud architecture", "distributed systems", "kubernetes", "microservices"],
            eligibility_criteria={"min_designation": "Assistant Professor / Associate Professor", "departments": ["CSE", "IT"]},
            description="Immersion residency for university faculty to gain real-world industry experience in hyperscale cloud architectures.",
            application_deadline=now + timedelta(days=50)
        )
        index_job_listing(l_google_faculty)

        l_tata_fdp = JobListing.objects.create(
            company=comp_tata,
            recruiter=rp_tata,
            title="Tata Motors EV Powertrain & Battery Management FDP",
            role_type=JobListing.RoleType.FDP,
            target_audience=JobListing.TargetAudience.FACULTY,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="Fully Sponsored + AICTE Certification",
            location="Pune, Maharashtra",
            tenure="2 Weeks Intensive",
            open_positions=25,
            required_skills=["ev powertrain", "battery management", "matlab", "thermal analysis"],
            eligibility_criteria={"target_audience": "Academicians & Faculty in Mechanical, Electrical, and Automotive Engineering"},
            description="AICTE-recognized Faculty Development Program exploring EV battery thermal runaway prevention, regenerative braking, and powertrain simulation.",
            application_deadline=now + timedelta(days=40)
        )
        index_job_listing(l_tata_fdp)

        l_ms_hackathon = JobListing.objects.create(
            company=comp_microsoft,
            recruiter=rp_ms,
            title="Microsoft GenAI & Autonomous Agents Innovation Challenge",
            role_type=JobListing.RoleType.INNOVATION_CHALLENGE,
            target_audience=JobListing.TargetAudience.ALL,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="INR 10,00,000 Cash Prizes + Direct Interviews",
            location="Online / All India",
            is_remote=True,
            tenure="48-Hour Hackathon + 2-Week Mentorship",
            open_positions=50,
            required_skills=["python", "generative ai", "llm", "rag", "docker"],
            eligibility_criteria={"open_to": "Students, Freshers, and Academic Teams across all Indian Universities"},
            description="National hackathon challenging participants to construct multi-agent AI systems for socio-economic challenges.",
            application_deadline=now + timedelta(days=18)
        )
        index_job_listing(l_ms_hackathon)

        l_tata_ev = JobListing.objects.create(
            company=comp_tata,
            recruiter=rp_tata,
            title="Electric Vehicle Powertrain Specialist",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="16 - 22 LPA",
            location="Pune, Maharashtra",
            tenure="Permanent",
            open_positions=4,
            required_skills=["ev powertrain", "battery management", "cad", "solidworks", "matlab", "robotics"],
            eligibility_criteria={"min_cgpa": 7.5, "eligible_branches": ["Mechanical", "Automotive", "Mechatronics"]},
            description="Design high-voltage EV battery pack packaging, regenerative braking telemetry, and powertrain thermal integration.",
            application_deadline=now + timedelta(days=40)
        )
        index_job_listing(l_tata_ev)

        l_google_ux = JobListing.objects.create(
            company=comp_google,
            recruiter=rp_google_ai,
            title="UI/UX Product Systems Designer",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="20 - 28 LPA",
            location="Bengaluru, Karnataka (Hybrid)",
            tenure="Permanent",
            open_positions=3,
            required_skills=["figma", "design systems", "wireframing", "user research", "wcag accessibility"],
            eligibility_criteria={"min_cgpa": 7.5},
            description="Lead multi-platform design systems, interaction tokens, accessibility guidelines, and usability prototyping.",
            application_deadline=now + timedelta(days=35)
        )
        index_job_listing(l_google_ux)

        l_pharma_reg = JobListing.objects.create(
            company=comp_sunpharma,
            recruiter=rp_pharma,
            title="Drug Regulatory Affairs & Formulation Specialist",
            role_type=JobListing.RoleType.FULL_TIME,
            target_audience=JobListing.TargetAudience.STUDENT,
            status=JobListing.ListingStatus.PUBLISHED,
            stipend_or_ctc="12 - 16 LPA",
            location="Mumbai, Maharashtra",
            tenure="Permanent",
            open_positions=5,
            required_skills=["formulation development", "drug regulatory affairs", "pharmacovigilance", "hplc", "gmp compliance"],
            eligibility_criteria={"min_cgpa": 7.5, "eligible_degrees": ["B.Pharm", "M.Pharm", "Pharm.D"]},
            description="Spearhead dossiers preparation for US FDA / EMA regulatory filings, formulation scale-up, and analytical validations.",
            application_deadline=now + timedelta(days=45)
        )
        index_job_listing(l_pharma_reg)

        p_google_k8s = LearningProgram.objects.create(
            company=comp_google,
            title="Google Cloud Architecture & Kubernetes Production Systems",
            program_type=LearningProgram.ProgramType.TRAINING_PROGRAM,
            target_audience=LearningProgram.TargetAudience.ALL,
            description="Comprehensive 6-week curriculum covering cloud-native deployment, microservices reliability, and zero-trust security.",
            skills_covered=["Cloud Architecture", "Kubernetes", "Docker", "GCP", "Microservices"],
            instructor_or_mentor="Sundeep Rao, Principal Google Cloud Architect",
            duration="6 Weeks (40 Hours)",
            mode=LearningProgram.Mode.ONLINE,
            registration_deadline=now + timedelta(days=20),
            start_date=now + timedelta(days=25),
            is_certified=True,
            branding_banner_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80"
        )

        p_tata_ev = LearningProgram.objects.create(
            company=comp_tata,
            title="Advanced Electric Mobility & Battery Pack Engineering Workshop",
            program_type=LearningProgram.ProgramType.WORKSHOP,
            target_audience=LearningProgram.TargetAudience.ALL,
            description="Hands-on engineering workshop demonstrating BMS telemetry, regenerative brake simulation, and battery pack design.",
            skills_covered=["EV Powertrain", "Battery Management", "CAD", "MATLAB", "SolidWorks"],
            instructor_or_mentor="Anil Deshmukh, Chief Technical Specialist - EV Powertrains",
            duration="2 Weeks (16 Hours)",
            mode=LearningProgram.Mode.HYBRID,
            registration_deadline=now + timedelta(days=15),
            start_date=now + timedelta(days=18),
            is_certified=True,
            branding_banner_url="https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80"
        )

        p_ms_ai = LearningProgram.objects.create(
            company=comp_microsoft,
            title="Azure AI & Enterprise LLM Applications Certification Track",
            program_type=LearningProgram.ProgramType.CERTIFICATION_COURSE,
            target_audience=LearningProgram.TargetAudience.ALL,
            description="Industry certification track on building retrieval-augmented generation (RAG) pipelines and fine-tuning enterprise LLMs.",
            skills_covered=["Generative AI", "Azure OpenAI", "Python", "Vector Databases", "Prompt Engineering"],
            instructor_or_mentor="Dr. Meenakshi Sundaram, Partner AI Scientist, Microsoft",
            duration="4 Weeks",
            mode=LearningProgram.Mode.ONLINE,
            registration_deadline=now + timedelta(days=30),
            start_date=now + timedelta(days=35),
            is_certified=True,
            branding_banner_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80"
        )

        sch_pragati = GovernmentScheme.objects.create(
            title="AICTE Pragati Scholarship for Girls 2025-2026",
            sponsoring_agency="All India Council for Technical Education (AICTE), Ministry of Education, GoI",
            domain=GovernmentScheme.Domain.TECH,
            scheme_type=GovernmentScheme.SchemeType.SCHOLARSHIP,
            target_gender=GovernmentScheme.TargetGender.FEMALE_ONLY,
            benefit_summary="INR 50,000 per annum + College Tuition Reimbursement",
            description="Flagship Government of India initiative to empower female students pursuing technical education.",
            eligible_degrees=["B.Tech", "B.E.", "BCA", "MCA", "M.Tech"],
            min_cgpa=6.5,
            application_deadline=now + timedelta(days=60),
            official_portal_url="https://scholarships.gov.in/aicte-pragati",
            status=GovernmentScheme.SchemeStatus.ACTIVE,
            badge_color="emerald"
        )

        sch_techsaksham = GovernmentScheme.objects.create(
            title="TechSaksham Initiative for Women in Technology",
            sponsoring_agency="Microsoft India & SAP India (Joint National AICTE Partnership)",
            domain=GovernmentScheme.Domain.TECH,
            scheme_type=GovernmentScheme.SchemeType.MENTORSHIP,
            target_gender=GovernmentScheme.TargetGender.FEMALE_ONLY,
            benefit_summary="Free Industry Cloud & AI Certification + 1-on-1 Corporate Mentorship",
            description="Joint corporate initiative between Microsoft and SAP India equipping female students with Cloud and AI skills.",
            eligible_degrees=["B.Tech", "B.E.", "BCA", "MCA", "M.Tech"],
            min_cgpa=7.0,
            application_deadline=now + timedelta(days=45),
            official_portal_url="https://techsaksham.in",
            status=GovernmentScheme.SchemeStatus.ACTIVE,
            badge_color="blue"
        )

        sch_sebi = GovernmentScheme.objects.create(
            title="SEBI & NISM Women in Capital Markets Research Grant",
            sponsoring_agency="Securities and Exchange Board of India (SEBI) & NISM",
            domain=GovernmentScheme.Domain.FINANCE,
            scheme_type=GovernmentScheme.SchemeType.RESEARCH_GRANT,
            target_gender=GovernmentScheme.TargetGender.FEMALE_ONLY,
            benefit_summary="INR 2,50,000 Research Grant + Direct SEBI Internship Interview",
            description="National regulatory grant encouraging female finance scholars to conduct empirical market microstructure research.",
            eligible_degrees=["B.Com", "M.Com", "MBA", "CFA", "Economics"],
            min_cgpa=7.5,
            application_deadline=now + timedelta(days=40),
            official_portal_url="https://nism.ac.in/women-in-markets",
            status=GovernmentScheme.SchemeStatus.ACTIVE,
            badge_color="violet"
        )

        u_rahul = User.objects.create_user(
            username="rahul_sharma",
            email="rahul.sharma@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Rahul",
            last_name="Sharma",
            phone_number="+919876543210",
            is_email_verified=True
        )
        sp_rahul, _ = StudentProfile.objects.update_or_create(
            user=u_rahul,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Computer Science & Engineering",
                "degree": "B.Tech in Computer Science",
                "cgpa": 9.42,
                "graduation_year": 2026,
                "github_handle": "rahulsharma-dev",
                "linkedin_url": "https://linkedin.com/in/rahul-sharma-verified",
                "portfolio_url": "https://rahulsharma.engineer",
                "placement_status": StudentProfile.PlacementStatus.PLACED,
                "is_verified": True,
                "overall_confidence_score": 88.0,
                "gender": StudentProfile.Gender.MALE,
                "apaar_id": "APAAR-2024-CU-8819",
                "abc_id": "ABC-7712-9934",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Backend Systems Engineer", "Distributed Systems Engineer", "Cloud Architect"],
                "skills_matrix": {
                    "python": {"weight": 90, "project_evidence": 92, "experience_recency": 86, "is_certified": True, "credential_bonus": 1.15},
                    "django": {"weight": 86, "project_evidence": 88, "experience_recency": 82, "is_certified": False},
                    "postgresql": {"weight": 85, "project_evidence": 86, "experience_recency": 84, "is_certified": True, "credential_bonus": 1.15},
                    "docker": {"weight": 82, "project_evidence": 84, "experience_recency": 80, "is_certified": True, "credential_bonus": 1.15},
                    "redis": {"weight": 80, "project_evidence": 82, "experience_recency": 78, "is_certified": False},
                    "rest api": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": False},
                    "git": {"weight": 84, "project_evidence": 85, "experience_recency": 82, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Python", "PostgreSQL", "Redis", "REST API"],
                    "frameworks": ["Django", "Microservices Architecture", "Zero-Copy RPC"],
                    "tools": ["Docker", "Git", "Kubernetes", "Linux"],
                    "soft_skills": ["Systems Reasoning", "Technical Mentorship", "Agile Communication"]
                },
                "certifications": [
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
                        "credential_url": "https://cncf.io/verify/CKA-88214-RAHUL",
                        "skills_covered": ["Kubernetes", "Docker", "Microservices"]
                    }
                ],
                "projects": [
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
                ],
                "internships": [
                    {
                        "company": "Google India",
                        "role": "Backend Systems Intern",
                        "duration": "6 Months (Jan 2024 - Jun 2024)",
                        "mentor_name": "Dr. Arvind Varma",
                        "mentor_designation": "Principal Distributed Systems Architect, Google India",
                        "mentor_feedback": "Rahul performed at the level of a senior systems engineer. He designed and deployed a zero-copy gRPC RPC layer that reduced inter-service latency by 34%. Highly recommended for any planetary systems team.",
                        "mentor_rating": 5.0,
                        "certificate_url": "https://skillsetu.cert.in/verify/GOOGLE-INTERN-2024-9841",
                        "report_url": "https://skillsetu.docs.in/reports/rahul-google-internship-final.pdf",
                        "completed_at": "2024-06-30T18:00:00Z"
                    }
                ],
                "achievements": [
                    {
                        "title": "Smart India Hackathon (SIH) 2024 Finalist",
                        "issuer": "Ministry of Education & AICTE",
                        "year": 2024,
                        "description": "1st Runner Up nationally in the Artificial Intelligence category for building an autonomous skill-gap diagnostic platform.",
                        "proof_url": "https://sih.gov.in/certificates/2024/SIH-AI-RUNNER-UP-RAHUL"
                    },
                    {
                        "title": "Dean's Academic Excellence Honor Roll",
                        "issuer": "IIT Bombay",
                        "year": 2023,
                        "description": "Awarded Top 1% Academic Distinction in Computer Science for outstanding semester GPA.",
                        "proof_url": "https://iitb.ac.in/merit/2023/rahul-dean-award"
                    }
                ],
                "academic_records": [
                    {"semester": 1, "sgpa": 9.10, "credits": 24},
                    {"semester": 2, "sgpa": 9.35, "credits": 26},
                    {"semester": 3, "sgpa": 9.40, "credits": 24},
                    {"semester": 4, "sgpa": 9.50, "credits": 25},
                    {"semester": 5, "sgpa": 9.45, "credits": 24},
                    {"semester": 6, "sgpa": 9.60, "credits": 26}
                ]
            }
        )
        index_student_profile(sp_rahul)

        app_rahul_google = JobApplication.objects.create(
            listing=l_google_backend,
            student=sp_rahul,
            status=JobApplication.ApplicationStatus.INTERVIEW,
            match_score=0.95,
            interview_date=now + timedelta(days=4, hours=4),
            recruiter_notes="Round 2 Technical Architecture & Distributed Systems interview scheduled with Google Systems Engineering team.",
            internship_status=JobApplication.InternshipStatus.NOT_STARTED,
            status_history=[
                {"status": "APPLIED", "timestamp": (now - timedelta(days=10)).isoformat(), "note": "Applied directly with verified skills matrix."},
                {"status": "UNDER_REVIEW", "timestamp": (now - timedelta(days=7)).isoformat(), "note": "Passed initial resume screening."},
                {"status": "SHORTLISTED", "timestamp": (now - timedelta(days=4)).isoformat(), "note": "Shortlisted based on 95% match and verified skills."},
                {"status": "INTERVIEW", "timestamp": (now - timedelta(days=1)).isoformat(), "interview_date": (now + timedelta(days=4, hours=4)).isoformat(), "note": "Round 2 Technical Architecture & Distributed Systems interview scheduled with Google Systems Engineering team."}
            ]
        )

        app_rahul_tata = JobApplication.objects.create(
            listing=l_tata_robotics,
            student=sp_rahul,
            status=JobApplication.ApplicationStatus.INTERVIEW,
            match_score=0.82,
            interview_date=now + timedelta(days=3),
            recruiter_notes="Strong software foundations; evaluating telemetry listener pipeline and CAN bus bridge.",
            internship_status=JobApplication.InternshipStatus.IN_PROGRESS,
            mentor_name="Priya Nair",
            mentor_designation="Head of University Relations & Talent",
            mentor_feedback="Demonstrating high diligence in real-time telemetry stream ingestion.",
            mentor_rating=4.8,
            weekly_progress_logs=[
                {"week": 1, "milestone": "Setup CAN bus emulation testbed and telemetry ingestion listener", "hours": 40}
            ]
        )

        Notification.objects.create(
            user=u_rahul,
            title="Interview Scheduled: Google India",
            message="Your Round 2 Technical Architecture interview for Backend Systems Engineer is scheduled for Friday at 11:00 AM IST.",
            notification_type=Notification.NotificationType.INTERVIEW_SCHEDULED,
            related_application_id=app_rahul_google.id,
            related_listing_id=l_google_backend.id,
            is_read=False
        )
        Notification.objects.create(
            user=u_rahul,
            title="Interview Scheduled: Tata Motors",
            message="Your technical interview for Autonomous Robotics & CAD Engineer is scheduled for Monday at 10:30 AM IST.",
            notification_type=Notification.NotificationType.INTERVIEW_SCHEDULED,
            related_application_id=app_rahul_tata.id,
            related_listing_id=l_tata_robotics.id,
            is_read=False
        )

        p_google_k8s.enrolled_students.add(sp_rahul)

        u_sneha = User.objects.create_user(
            username="sneha_reddy",
            email="sneha.reddy@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Sneha",
            last_name="Reddy",
            phone_number="+919876543211",
            is_email_verified=True
        )
        sp_sneha, _ = StudentProfile.objects.update_or_create(
            user=u_sneha,
            defaults={
                "institution": "National Institute of Technology (NIT) Karnataka, Surathkal",
                "department": "Computer Science & Engineering",
                "degree": "B.Tech in Computer Science",
                "cgpa": 9.15,
                "graduation_year": 2026,
                "github_handle": "snehareddy-cloud",
                "linkedin_url": "https://linkedin.com/in/sneha-reddy-cloud",
                "portfolio_url": "https://snehareddy.dev",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 85.0,
                "gender": StudentProfile.Gender.FEMALE,
                "apaar_id": "APAAR-2024-NITK-4421",
                "abc_id": "ABC-8812-3341",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Cloud & AI Associate", "Azure Solutions Architect", "Machine Learning Engineer"],
                "skills_matrix": {
                    "python": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": True, "credential_bonus": 1.15},
                    "azure": {"weight": 86, "project_evidence": 88, "experience_recency": 82, "is_certified": True, "credential_bonus": 1.15},
                    "cloud architecture": {"weight": 84, "project_evidence": 85, "experience_recency": 80, "is_certified": True, "credential_bonus": 1.15},
                    "machine learning": {"weight": 82, "project_evidence": 84, "experience_recency": 78, "is_certified": False},
                    "docker": {"weight": 80, "project_evidence": 82, "experience_recency": 76, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Python", "Azure Cloud", "Machine Learning", "Docker"],
                    "frameworks": ["Cloud-Native Microservices", "Scikit-Learn", "FastAPI"],
                    "tools": ["Azure Portal", "Git", "Docker Compose", "Postman"],
                    "soft_skills": ["Cross-functional Leadership", "Analytical Synthesis", "Presentation"]
                },
                "certifications": [
                    {
                        "name": "Microsoft Certified: Azure Solutions Architect Expert",
                        "issuer": "Microsoft",
                        "issue_year": 2024,
                        "credential_url": "https://learn.microsoft.com/verify/AZ-305-SNEHA",
                        "skills_covered": ["Azure", "Cloud Architecture", "Docker"]
                    }
                ],
                "projects": [
                    {
                        "title": "Automated Satellite Crop Health Classification",
                        "technologies": ["Python", "Azure ML", "PyTorch", "Docker"],
                        "description": "Built multi-spectral satellite imagery classification model deployed on Azure Kubernetes Service."
                    }
                ]
            }
        )
        index_student_profile(sp_sneha)

        app_sneha_ms = JobApplication.objects.create(
            listing=l_ms_cloud_dei,
            student=sp_sneha,
            status=JobApplication.ApplicationStatus.INTERVIEW,
            match_score=0.92,
            interview_date=now + timedelta(days=2),
            recruiter_notes="Outstanding technical portfolio; verified Azure Solutions Architect credential."
        )

        app_sneha_google = JobApplication.objects.create(
            listing=l_google_frontend,
            student=sp_sneha,
            status=JobApplication.ApplicationStatus.SHORTLISTED,
            match_score=0.88,
            recruiter_notes="Strong engineering profile; advanced to technical screen."
        )

        Notification.objects.create(
            user=u_sneha,
            title="Interview Invite: Microsoft India",
            message="Your technical interview for the Cloud & AI Diversity Associate role is scheduled for Tuesday at 2:00 PM IST.",
            notification_type=Notification.NotificationType.INTERVIEW_SCHEDULED,
            related_application_id=app_sneha_ms.id,
            related_listing_id=l_ms_cloud_dei.id,
            is_read=False
        )
        Notification.objects.create(
            user=u_sneha,
            title="100% Eligible: AICTE Pragati Scholarship for Girls",
            message="Your profile has matched 100% eligibility criteria for the AICTE Pragati Scholarship for Girls (INR 50,000 / year).",
            notification_type=Notification.NotificationType.NEW_SCHEME,
            is_read=False
        )
        Notification.objects.create(
            user=u_sneha,
            title="Shortlisted by Google India",
            message="Google India has shortlisted your application for Frontend Engineering Intern.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_sneha_google.id,
            related_listing_id=l_google_frontend.id,
            is_read=True
        )

        p_ms_ai.enrolled_students.add(sp_sneha)

        u_ananya = User.objects.create_user(
            username="ananya_patel",
            email="ananya.patel@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Ananya",
            last_name="Patel",
            phone_number="+919876543212",
            is_email_verified=True
        )
        sp_ananya, _ = StudentProfile.objects.update_or_create(
            user=u_ananya,
            defaults={
                "institution": "Shri Ram College of Commerce, Delhi University",
                "department": "Commerce & Financial Studies",
                "degree": "B.Com (Honours) in Financial Analysis",
                "cgpa": 9.20,
                "graduation_year": 2025,
                "github_handle": "ananyafinance",
                "linkedin_url": "https://linkedin.com/in/ananya-patel-fin",
                "portfolio_url": "https://ananyapatel.finance",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 86.0,
                "gender": StudentProfile.Gender.FEMALE,
                "apaar_id": "APAAR-2024-DU-9912",
                "abc_id": "ABC-4412-8877",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Quantitative Financial Analyst", "Valuation Analyst", "Investment Banking Associate"],
                "skills_matrix": {
                    "excel": {"weight": 95, "project_evidence": 96, "experience_recency": 92, "is_certified": True, "credential_bonus": 1.15},
                    "financial modeling": {"weight": 90, "project_evidence": 92, "experience_recency": 88, "is_certified": True, "credential_bonus": 1.15},
                    "dcf": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": True, "credential_bonus": 1.15},
                    "valuation": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": False},
                    "tally": {"weight": 84, "project_evidence": 85, "experience_recency": 82, "is_certified": False},
                    "gst": {"weight": 82, "project_evidence": 84, "experience_recency": 80, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Excel", "Financial Modeling", "DCF Valuation", "Tally Prime", "GST Compliance"],
                    "frameworks": ["GAAP/Ind AS Reporting", "Capital Asset Pricing Model (CAPM)", "3-Statement Projections"],
                    "tools": ["MS Excel", "Tally Prime", "Tableau", "QuickBooks"],
                    "soft_skills": ["Financial Rigor", "Stakeholder Communication", "Due Diligence"]
                },
                "certifications": [
                    {
                        "name": "NSE Certified Market Professional (NCMP)",
                        "issuer": "National Stock Exchange of India",
                        "issue_year": 2024,
                        "credential_url": "https://nseindia.com/verify/NCMP-8819-ANANYA",
                        "skills_covered": ["Financial Modeling", "Valuation", "Excel"]
                    }
                ],
                "projects": [
                    {
                        "title": "Public SaaS Company DCF Valuation Model",
                        "technologies": ["Excel", "Financial Modeling", "Valuation", "DCF"],
                        "description": "Constructed a 3-statement financial model and 5-year discounted cash flow forecasting with sensitivity analysis."
                    }
                ]
            }
        )
        index_student_profile(sp_ananya)

        app_ananya_morgan = JobApplication.objects.create(
            listing=l_morgan_quant,
            student=sp_ananya,
            status=JobApplication.ApplicationStatus.SHORTLISTED,
            match_score=0.94,
            recruiter_notes="Strong DCF modeling foundation and verified NCMP credential."
        )

        app_ananya_zerodha = JobApplication.objects.create(
            listing=l_zerodha_intern,
            student=sp_ananya,
            status=JobApplication.ApplicationStatus.UNDER_REVIEW,
            match_score=0.86,
            recruiter_notes="Reviewing quantitative analysis background."
        )

        Notification.objects.create(
            user=u_ananya,
            title="Shortlisted: Morgan Stanley",
            message="Morgan Stanley has moved your application for Quantitative Financial Analyst to Shortlisted.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_ananya_morgan.id,
            related_listing_id=l_morgan_quant.id,
            is_read=False
        )
        Notification.objects.create(
            user=u_ananya,
            title="New Grant Alert: SEBI & NISM Research Grant",
            message="You are eligible for the SEBI & NISM Women in Capital Markets Research Grant (INR 2,50,000).",
            notification_type=Notification.NotificationType.NEW_SCHEME,
            is_read=False
        )

        u_priya = User.objects.create_user(
            username="priya_roy",
            email="priya.roy@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Priya",
            last_name="Roy",
            phone_number="+919876543213",
            is_email_verified=True
        )
        sp_priya, _ = StudentProfile.objects.update_or_create(
            user=u_priya,
            defaults={
                "institution": "National Institute of Design (NID) Ahmedabad",
                "department": "Interaction & UI/UX Design",
                "degree": "B.Des in UI/UX Design",
                "cgpa": 8.85,
                "graduation_year": 2025,
                "github_handle": "priyaroy-design",
                "linkedin_url": "https://linkedin.com/in/priya-roy-design",
                "portfolio_url": "https://priyaroy.design",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": False,
                "overall_confidence_score": 0.0,
                "gender": StudentProfile.Gender.FEMALE,
                "apaar_id": "APAAR-2024-NID-3319",
                "abc_id": "ABC-9912-7722",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["UI/UX Designer", "Product Designer", "Design Systems Lead"],
                "skills_matrix": {
                    "figma": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": False},
                    "ui/ux": {"weight": 86, "project_evidence": 88, "experience_recency": 82, "is_certified": False},
                    "design systems": {"weight": 84, "project_evidence": 85, "experience_recency": 80, "is_certified": False},
                    "wireframing": {"weight": 82, "project_evidence": 84, "experience_recency": 78, "is_certified": False},
                    "prototyping": {"weight": 80, "project_evidence": 82, "experience_recency": 76, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Figma", "UI/UX", "Design Systems", "Prototyping", "Wireframing"],
                    "frameworks": ["Atomic Design", "Design Thinking", "WCAG 2.1 Accessibility"],
                    "tools": ["Figma", "Adobe Creative Suite", "Miro", "Principle"],
                    "soft_skills": ["User Empathy", "Design Critique", "User Research"]
                },
                "projects": [
                    {
                        "title": "Accessible Healthcare Telemedicine Mobile App",
                        "technologies": ["Figma", "Design Systems", "UI/UX"],
                        "description": "Conducted 25 user interviews and built a 50-screen design system conforming to WCAG 2.1 AAA contrast standards."
                    }
                ]
            }
        )
        index_student_profile(sp_priya)

        app_priya_google = JobApplication.objects.create(
            listing=l_google_frontend,
            student=sp_priya,
            status=JobApplication.ApplicationStatus.UNDER_REVIEW,
            match_score=0.68,
            recruiter_notes="Design portfolio received; pending cognitive test verification."
        )

        Notification.objects.create(
            user=u_priya,
            title="Application Placed Under Review",
            message="Google India has placed your application for Frontend Engineering Intern under review.",
            notification_type=Notification.NotificationType.APPLICATION_REVIEW,
            related_application_id=app_priya_google.id,
            is_read=False
        )

        u_aarav = User.objects.create_user(
            username="aarav_verma",
            email="aarav.verma@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Aarav",
            last_name="Verma",
            phone_number="+919876543214",
            is_email_verified=True
        )
        sp_aarav, _ = StudentProfile.objects.update_or_create(
            user=u_aarav,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Computer Science & Engineering",
                "degree": "B.Tech in Computer Science",
                "cgpa": 7.20,
                "graduation_year": 2026,
                "current_designation": "Junior Python Developer",
                "target_roles": ["Junior Python Developer", "Software Trainee"],
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "is_verified": False,
                "overall_confidence_score": 0.0,
                "gender": StudentProfile.Gender.MALE,
                "skills_matrix": {},
                "skills_categorized": {
                    "technical_skills": [],
                    "frameworks": [],
                    "tools": [],
                    "soft_skills": ["Eager to Learn", "Team Collaboration"]
                },
                "projects": []
            }
        )
        index_student_profile(sp_aarav)

        app_aarav_zerodha = JobApplication.objects.create(
            listing=l_zerodha_intern,
            student=sp_aarav,
            status=JobApplication.ApplicationStatus.APPLIED,
            match_score=0.28,
            recruiter_notes="Foundational candidate application received via designated career pathway."
        )

        Notification.objects.create(
            user=u_aarav,
            title="Application Submitted: Zerodha Broking",
            message="Your application for Trading Systems & FinTech Intern has been submitted.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_aarav_zerodha.id,
            is_read=False
        )
        Notification.objects.create(
            user=u_aarav,
            title="Unlock 80%+ Match Ceilings",
            message="You are currently at Foundational Aspirant tier (capped at 35%). Complete your 5-minute Adaptive Skill Assessment to unlock high match tiers.",
            notification_type=Notification.NotificationType.SYSTEM,
            is_read=False
        )

        u_karan = User.objects.create_user(
            username="karan_mehra",
            email="karan.mehra@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Karan",
            last_name="Mehra",
            phone_number="+919876543215",
            is_email_verified=True
        )
        sp_karan, _ = StudentProfile.objects.update_or_create(
            user=u_karan,
            defaults={
                "institution": "Birla Institute of Technology and Science (BITS) Pilani",
                "department": "Computer Science & Engineering",
                "degree": "B.E. in Computer Science",
                "cgpa": 8.45,
                "graduation_year": 2026,
                "github_handle": "karan-mehra",
                "linkedin_url": "https://linkedin.com/in/karan-mehra-bits",
                "portfolio_url": "https://karanmehra.tech",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 74.0,
                "gender": StudentProfile.Gender.MALE,
                "apaar_id": "APAAR-2024-BITS-9921",
                "abc_id": "ABC-6612-4433",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Backend Systems Engineer", "Python Developer"],
                "skills_matrix": {
                    "python": {"weight": 78, "project_evidence": 80, "experience_recency": 75, "is_certified": True, "credential_bonus": 1.15},
                    "django": {"weight": 74, "project_evidence": 75, "experience_recency": 72, "is_certified": False},
                    "postgresql": {"weight": 75, "project_evidence": 76, "experience_recency": 74, "is_certified": False},
                    "docker": {"weight": 70, "project_evidence": 72, "experience_recency": 68, "is_certified": False},
                    "redis": {"weight": 68, "project_evidence": 70, "experience_recency": 65, "is_certified": False},
                    "rest api": {"weight": 76, "project_evidence": 78, "experience_recency": 74, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Python", "PostgreSQL", "REST API", "Redis"],
                    "frameworks": ["Django", "AsyncIO"],
                    "tools": ["Docker", "Git", "Postman"],
                    "soft_skills": ["Teamwork", "Problem Solving"]
                },
                "certifications": [
                    {
                        "name": "AWS Certified Cloud Practitioner",
                        "issuer": "Amazon Web Services",
                        "issue_year": 2024,
                        "credential_url": "https://aws.amazon.com/verification/CLF-C02-KARAN",
                        "skills_covered": ["Python", "Cloud Architecture"]
                    }
                ],
                "projects": [
                    {
                        "title": "Asynchronous Task Processing Queue with Redis",
                        "technologies": ["Python", "Django", "Redis", "Docker"],
                        "description": "Implemented background task distribution queue handling scheduled email reminders and data exports."
                    }
                ]
            }
        )
        index_student_profile(sp_karan)

        app_karan_google = JobApplication.objects.create(
            listing=l_google_backend,
            student=sp_karan,
            status=JobApplication.ApplicationStatus.SHORTLISTED,
            match_score=0.76,
            recruiter_notes="Solid mid-tier backend candidate with verified Python fundamentals."
        )

        Notification.objects.create(
            user=u_karan,
            title="Application Shortlisted by Google India",
            message="Your application for Backend Systems Engineer has been shortlisted for technical rounds.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_karan_google.id,
            is_read=False
        )

        u_abhinav = User.objects.create_user(
            username="abhinav_kashyap",
            email="abhinav.kashyap@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Abhinav",
            last_name="Kashyap",
            phone_number="+919876543216",
            is_email_verified=True
        )
        sp_abhinav, _ = StudentProfile.objects.update_or_create(
            user=u_abhinav,
            defaults={
                "institution": "Delhi Technological University (DTU)",
                "department": "Computer Science & Engineering",
                "degree": "B.Tech in Information Technology",
                "cgpa": 7.80,
                "graduation_year": 2025,
                "github_handle": "abhinav-kashyap",
                "linkedin_url": "https://linkedin.com/in/abhinav-kashyap-dtu",
                "portfolio_url": "https://abhinavkashyap.dev",
                "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                "is_verified": False,
                "overall_confidence_score": 34.8,
                "gender": StudentProfile.Gender.MALE,
                "apaar_id": "APAAR-2024-DTU-7711",
                "abc_id": "ABC-5512-2288",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Backend Systems Engineer"],
                "skills_matrix": {
                    "python": {"weight": 95, "project_evidence": 96, "experience_recency": 94, "is_certified": False},
                    "django": {"weight": 92, "project_evidence": 93, "experience_recency": 90, "is_certified": False},
                    "postgresql": {"weight": 90, "project_evidence": 91, "experience_recency": 88, "is_certified": False},
                    "docker": {"weight": 88, "project_evidence": 89, "experience_recency": 86, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Python", "PostgreSQL"],
                    "frameworks": ["Django"],
                    "tools": ["Docker"],
                    "soft_skills": ["Communication"]
                },
                "projects": [
                    {
                        "title": "Basic Blog Engine",
                        "technologies": ["Python", "Django"],
                        "description": "Created basic CRUD application."
                    }
                ]
            }
        )
        index_student_profile(sp_abhinav)

        app_abhinav_google = JobApplication.objects.create(
            listing=l_google_backend,
            student=sp_abhinav,
            status=JobApplication.ApplicationStatus.REJECTED,
            match_score=0.38,
            recruiter_notes="System Anti-Cheat Alert: Significant discrepancy detected between resume claims (95%) and cognitive validation (48%). Square-root penalty applied."
        )

        Notification.objects.create(
            user=u_abhinav,
            title="Verification Audit: Retest Recommended",
            message="Discrepancy detected between resume claims and proctored assessment. Retest recommended to recalibrate match confidence score.",
            notification_type=Notification.NotificationType.SYSTEM,
            is_read=False
        )

        u_harpreet = User.objects.create_user(
            username="harpreet_singh",
            email="harpreet.singh@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Harpreet",
            last_name="Singh",
            phone_number="+919876543217",
            is_email_verified=True
        )
        sp_harpreet, _ = StudentProfile.objects.update_or_create(
            user=u_harpreet,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Mechanical Engineering",
                "degree": "B.E. in Mechanical Engineering (Automotive & EV)",
                "cgpa": 8.85,
                "graduation_year": 2026,
                "github_handle": "harpreet-ev",
                "linkedin_url": "https://linkedin.com/in/harpreet-singh-ev",
                "portfolio_url": "https://harpreet-ev.portfolio",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 85.5,
                "gender": StudentProfile.Gender.MALE,
                "apaar_id": "APAAR-2024-CU-5522",
                "abc_id": "ABC-8812-3344",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["EV Powertrain Engineer", "Automotive Systems Engineer", "Robotics Engineer"],
                "skills_matrix": {
                    "ev powertrain": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": True, "credential_bonus": 1.15},
                    "battery management": {"weight": 86, "project_evidence": 88, "experience_recency": 84, "is_certified": True, "credential_bonus": 1.15},
                    "cad": {"weight": 84, "project_evidence": 86, "experience_recency": 82, "is_certified": False},
                    "solidworks": {"weight": 85, "project_evidence": 87, "experience_recency": 83, "is_certified": False},
                    "matlab": {"weight": 82, "project_evidence": 84, "experience_recency": 80, "is_certified": False},
                    "robotics": {"weight": 80, "project_evidence": 82, "experience_recency": 78, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["EV Powertrain", "Battery Management", "Robotics"],
                    "frameworks": ["CAN Bus Telemetry", "Thermal Modeling"],
                    "tools": ["SolidWorks", "MATLAB Simulink", "ANSYS", "AutoCAD"],
                    "soft_skills": ["Analytical Thinking", "Cross-disciplinary Engineering"]
                },
                "certifications": [
                    {
                        "name": "Certified EV Battery Systems Specialist",
                        "issuer": "Automotive Skills Development Council (ASDC)",
                        "issue_year": 2024,
                        "credential_url": "https://asdc.org.in/verify/EV-BMS-HARPREET",
                        "skills_covered": ["EV Powertrain", "Battery Management"]
                    }
                ],
                "projects": [
                    {
                        "title": "48V Regenerative Braking and Battery Pack Simulation",
                        "technologies": ["MATLAB", "SolidWorks", "Simulink", "EV Powertrain"],
                        "description": "Modeled thermal dissipation and state-of-charge efficiency for 48V electric vehicle battery packs."
                    }
                ]
            }
        )
        index_student_profile(sp_harpreet)

        app_harpreet_tata = JobApplication.objects.create(
            listing=l_tata_ev,
            student=sp_harpreet,
            status=JobApplication.ApplicationStatus.INTERVIEW,
            match_score=0.93,
            recruiter_notes="Candidate demonstrated outstanding mastery of high-voltage battery thermal management. Technical interview scheduled."
        )

        p_tata_ev.enrolled_students.add(sp_harpreet)

        Notification.objects.create(
            user=u_harpreet,
            title="Interview Scheduled: Tata Motors",
            message="Your technical interview for Electric Vehicle Powertrain Specialist is scheduled for Thursday at 2:00 PM IST.",
            notification_type=Notification.NotificationType.INTERVIEW_SCHEDULED,
            related_application_id=app_harpreet_tata.id,
            is_read=False
        )

        u_simran = User.objects.create_user(
            username="simran_kaur",
            email="simran.kaur@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Simran",
            last_name="Kaur",
            phone_number="+919876543218",
            is_email_verified=True
        )
        sp_simran, _ = StudentProfile.objects.update_or_create(
            user=u_simran,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Chitkara Design School",
                "degree": "B.Des in UI/UX & Interaction Design",
                "cgpa": 9.05,
                "graduation_year": 2026,
                "github_handle": "simran-design",
                "linkedin_url": "https://linkedin.com/in/simran-kaur-design",
                "portfolio_url": "https://simrankaur.design",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 83.5,
                "gender": StudentProfile.Gender.FEMALE,
                "apaar_id": "APAAR-2024-CU-7766",
                "abc_id": "ABC-9912-1144",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Product Designer", "UI/UX Designer", "Design Systems Lead"],
                "skills_matrix": {
                    "figma": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": True, "credential_bonus": 1.15},
                    "design systems": {"weight": 86, "project_evidence": 88, "experience_recency": 84, "is_certified": False},
                    "wireframing": {"weight": 85, "project_evidence": 87, "experience_recency": 83, "is_certified": False},
                    "user research": {"weight": 82, "project_evidence": 84, "experience_recency": 80, "is_certified": False},
                    "wcag accessibility": {"weight": 80, "project_evidence": 82, "experience_recency": 78, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["Figma", "UI/UX", "Design Systems", "Wireframing"],
                    "frameworks": ["Design Tokens", "Material You", "WCAG 2.2 AAA"],
                    "tools": ["Figma", "FigJam", "Adobe XD", "Principle"],
                    "soft_skills": ["Visual Storytelling", "Design System Governance", "User Empathy"]
                },
                "certifications": [
                    {
                        "name": "Google UX Design Professional Certificate",
                        "issuer": "Google Career Certificates",
                        "issue_year": 2024,
                        "credential_url": "https://coursera.org/verify/professional-cert/GOOGLE-UX-SIMRAN",
                        "skills_covered": ["Figma", "UI/UX", "User Research"]
                    }
                ],
                "projects": [
                    {
                        "title": "Chitkara Unified Campus Portal Design System",
                        "technologies": ["Figma", "Design Systems", "Tokens", "WCAG"],
                        "description": "Architected component library with 120+ responsive components, dark mode variants, and strict accessibility tokens."
                    }
                ]
            }
        )
        index_student_profile(sp_simran)

        app_simran_google = JobApplication.objects.create(
            listing=l_google_ux,
            student=sp_simran,
            status=JobApplication.ApplicationStatus.SHORTLISTED,
            match_score=0.89,
            recruiter_notes="Verified design systems portfolio with WCAG accessibility score above 95%."
        )

        Notification.objects.create(
            user=u_simran,
            title="Shortlisted by Google India",
            message="Your application for UI/UX Product Systems Designer has been shortlisted.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_simran_google.id,
            is_read=False
        )

        u_divya = User.objects.create_user(
            username="divya_oberoi",
            email="divya.oberoi@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Divya",
            last_name="Oberoi",
            phone_number="+919876543219",
            is_email_verified=True
        )
        sp_divya, _ = StudentProfile.objects.update_or_create(
            user=u_divya,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Chitkara College of Pharmacy",
                "degree": "B.Pharm in Pharmaceutical Sciences & Regulatory Affairs",
                "cgpa": 8.95,
                "graduation_year": 2025,
                "github_handle": "divya-pharma",
                "linkedin_url": "https://linkedin.com/in/divya-oberoi-pharma",
                "portfolio_url": "https://divyaoberoi.pharma",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 87.0,
                "gender": StudentProfile.Gender.FEMALE,
                "apaar_id": "APAAR-2024-CU-3388",
                "abc_id": "ABC-2212-7799",
                "nheqf_level": "LEVEL_6_0",
                "target_roles": ["Drug Regulatory Affairs Specialist", "Formulation Scientist", "Pharmacovigilance Associate"],
                "skills_matrix": {
                    "formulation development": {"weight": 88, "project_evidence": 90, "experience_recency": 85, "is_certified": True, "credential_bonus": 1.15},
                    "drug regulatory affairs": {"weight": 90, "project_evidence": 92, "experience_recency": 88, "is_certified": True, "credential_bonus": 1.15},
                    "pharmacovigilance": {"weight": 85, "project_evidence": 86, "experience_recency": 83, "is_certified": False},
                    "hplc": {"weight": 84, "project_evidence": 85, "experience_recency": 82, "is_certified": False},
                    "gmp compliance": {"weight": 88, "project_evidence": 90, "experience_recency": 86, "is_certified": True, "credential_bonus": 1.15}
                },
                "skills_categorized": {
                    "technical_skills": ["Drug Regulatory Affairs", "Formulation Development", "HPLC Assay", "Pharmacovigilance"],
                    "frameworks": ["ICH Q8/Q9/Q10 Quality Guidelines", "US FDA eCTD Modules", "WHO GMP"],
                    "tools": ["Empower HPLC Software", "TrackWise", "MasterControl QMS"],
                    "soft_skills": ["Regulatory Writing", "Analytical Diligence", "Audit Readiness"]
                },
                "certifications": [
                    {
                        "name": "Certified Regulatory Affairs Professional (RAC)",
                        "issuer": "Regulatory Affairs Professionals Society (RAPS)",
                        "issue_year": 2024,
                        "credential_url": "https://raps.org/verify/RAC-DIVYA-2024",
                        "skills_covered": ["Drug Regulatory Affairs", "GMP Compliance"]
                    }
                ],
                "projects": [
                    {
                        "title": "eCTD Module 3 Dossier Preparation for Oral Solid Dosage Form",
                        "technologies": ["eCTD", "Formulation Development", "GMP"],
                        "description": "Authored complete stability protocol and chemistry manufacturing controls documentation conforming to ICH standards."
                    }
                ]
            }
        )
        index_student_profile(sp_divya)

        app_divya_sun = JobApplication.objects.create(
            listing=l_pharma_reg,
            student=sp_divya,
            status=JobApplication.ApplicationStatus.SHORTLISTED,
            match_score=0.92,
            recruiter_notes="Strong knowledge of US FDA eCTD dossiers preparation and GMP standards."
        )

        Notification.objects.create(
            user=u_divya,
            title="Shortlisted: Sun Pharmaceutical Industries",
            message="Your application for Drug Regulatory Affairs & Formulation Specialist has been shortlisted for technical evaluation.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_divya_sun.id,
            is_read=False
        )

        u_rohan = User.objects.create_user(
            username="rohan_kapoor",
            email="rohan.kapoor@skillsetu.in",
            password="password123",
            role=User.Role.STUDENT,
            first_name="Rohan",
            last_name="Kapoor",
            phone_number="+919876543220",
            is_email_verified=True
        )
        sp_rohan, _ = StudentProfile.objects.update_or_create(
            user=u_rohan,
            defaults={
                "institution": "Chitkara University, Punjab",
                "department": "Chitkara Business School",
                "degree": "MBA in Business Analytics & Operations",
                "cgpa": 8.70,
                "graduation_year": 2025,
                "github_handle": "rohan-analytics",
                "linkedin_url": "https://linkedin.com/in/rohan-kapoor-mba",
                "portfolio_url": "https://rohankapoor.biz",
                "placement_status": StudentProfile.PlacementStatus.OPEN_TO_INTERN,
                "is_verified": True,
                "overall_confidence_score": 82.0,
                "gender": StudentProfile.Gender.MALE,
                "apaar_id": "APAAR-2024-CU-1199",
                "abc_id": "ABC-3312-8855",
                "nheqf_level": "LEVEL_6_5",
                "target_roles": ["Business Analyst", "Product Operations Analyst", "Operations Manager"],
                "skills_matrix": {
                    "business analysis": {"weight": 86, "project_evidence": 88, "experience_recency": 83, "is_certified": False},
                    "market research": {"weight": 82, "project_evidence": 84, "experience_recency": 80, "is_certified": False},
                    "tableau": {"weight": 85, "project_evidence": 87, "experience_recency": 83, "is_certified": True, "credential_bonus": 1.15},
                    "sql": {"weight": 84, "project_evidence": 85, "experience_recency": 82, "is_certified": False},
                    "scrum": {"weight": 80, "project_evidence": 82, "experience_recency": 78, "is_certified": False},
                    "financial modeling": {"weight": 78, "project_evidence": 80, "experience_recency": 76, "is_certified": False}
                },
                "skills_categorized": {
                    "technical_skills": ["SQL", "Tableau", "Business Analysis", "Financial Modeling"],
                    "frameworks": ["Agile Scrum", "SWOT Analysis", "Root Cause Analysis (5 Whys)"],
                    "tools": ["Tableau Desktop", "Jira", "Excel Power Query", "Confluence"],
                    "soft_skills": ["Executive Stakeholder Presentation", "Process Optimization", "Requirements Elicitation"]
                },
                "certifications": [
                    {
                        "name": "Tableau Desktop Certified Associate",
                        "issuer": "Salesforce / Tableau",
                        "issue_year": 2024,
                        "credential_url": "https://tableau.com/verify/TABLEAU-ROHAN-2024",
                        "skills_covered": ["Tableau", "SQL", "Business Analysis"]
                    }
                ],
                "projects": [
                    {
                        "title": "Enterprise Retail Supply Chain Bottleneck Diagnostic",
                        "technologies": ["Tableau", "SQL", "Business Analysis"],
                        "description": "Constructed end-to-end telemetry dashboard tracking warehouse inventory turnover and order delivery SLA variances."
                    }
                ]
            }
        )
        index_student_profile(sp_rohan)

        app_rohan_zerodha = JobApplication.objects.create(
            listing=l_zerodha_intern,
            student=sp_rohan,
            status=JobApplication.ApplicationStatus.UNDER_REVIEW,
            match_score=0.84,
            recruiter_notes="Analytics portfolio under review for product operations track."
        )

        Notification.objects.create(
            user=u_rohan,
            title="Application Under Review: Zerodha Broking",
            message="Your application for Trading Systems & FinTech Intern has been marked under review.",
            notification_type=Notification.NotificationType.STATUS_CHANGE,
            related_application_id=app_rohan_zerodha.id,
            is_read=False
        )

        Notification.objects.create(
            user=u_faculty_iitb,
            title="Faculty Fellowship Application Confirmed",
            message="Your expression of interest for the Google Cloud Distributed Systems Faculty Fellowship has been submitted.",
            notification_type=Notification.NotificationType.APPLICATION_REVIEW,
            related_listing_id=l_google_faculty.id,
            is_read=False
        )
        p_tata_ev.enrolled_faculty.add(fp_iitb)

        Notification.objects.create(
            user=u_rec_google,
            title="New Application: Rahul Sharma (Offer Pending Acceptance)",
            message="Rahul Sharma has achieved a 95% Verified Match Score for Backend Systems Engineer.",
            notification_type=Notification.NotificationType.APPLICATION_REVIEW,
            related_application_id=app_rahul_google.id,
            related_listing_id=l_google_backend.id,
            is_read=False
        )
        Notification.objects.create(
            user=u_rec_ms,
            title="Upcoming Interview: Sneha Reddy",
            message="Technical screening with Sneha Reddy for Cloud & AI Diversity Associate is scheduled for Tuesday.",
            notification_type=Notification.NotificationType.INTERVIEW_SCHEDULED,
            related_application_id=app_sneha_ms.id,
            related_listing_id=l_ms_cloud_dei.id,
            is_read=False
        )

        self.stdout.write(self.style.SUCCESS("Master SIH prototype showcase ecosystem seeded successfully with 100% interconnected dynamic relationships!"))
