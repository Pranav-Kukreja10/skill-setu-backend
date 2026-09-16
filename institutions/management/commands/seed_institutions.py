from django.core.management.base import BaseCommand
from accounts.models import User
from institutions.models import Institution, Department, FacultyProfile

class Command(BaseCommand):
    help = "Seeds verified institutions (Universities, IITs/NITs, Colleges), academic departments, and links faculty personas"

    def handle(self, *args, **options):
        self.stdout.write("[-] Seeding verified institutions and academic departments...")

        # 1. INSTITUTIONS
        institutions_data = [
            {
                "name": "National Institute of Technology, Karnataka",
                "code": "AISHE-U-0237",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "state": "Karnataka",
                "city": "Surathkal",
                "website": "https://www.nitk.ac.in",
                "nirf_rank": 12,
                "is_verified": True,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/NITK_Surathkal_logo.svg/1200px-NITK_Surathkal_logo.svg.png",
                "departments": [
                    {"name": "Computer Science & Engineering", "code": "CSE", "head_of_department": "Dr. Ananth Kumar"},
                    {"name": "Mechanical Engineering", "code": "MECH", "head_of_department": "Dr. P. R. Venkatesh"},
                    {"name": "Information Technology", "code": "IT", "head_of_department": "Dr. Shailesh Rao"}
                ]
            },
            {
                "name": "Indian Institute of Technology, Bombay",
                "code": "AISHE-U-0306",
                "institution_type": Institution.InstitutionType.INSTITUTE,
                "state": "Maharashtra",
                "city": "Mumbai",
                "website": "https://www.iitb.ac.in",
                "nirf_rank": 3,
                "is_verified": True,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Indian_Institute_of_Technology_Bombay_Logo.svg/1200px-Indian_Institute_of_Technology_Bombay_Logo.svg.png",
                "departments": [
                    {"name": "Computer Science & Engineering", "code": "CSE", "head_of_department": "Dr. Supratik Chakraborty"},
                    {"name": "Mechanical Engineering", "code": "ME", "head_of_department": "Dr. Sreedhara S."}
                ]
            },
            {
                "name": "Shri Ram College of Commerce, Delhi University",
                "code": "AISHE-C-19812",
                "institution_type": Institution.InstitutionType.COLLEGE,
                "state": "Delhi",
                "city": "New Delhi",
                "website": "https://www.srcc.edu",
                "nirf_rank": 1,
                "is_verified": True,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/SRCC_logo.png/220px-SRCC_logo.png",
                "departments": [
                    {"name": "Commerce & Financial Studies", "code": "COM", "head_of_department": "Dr. Simrit Kaur"},
                    {"name": "Economics & Business Analytics", "code": "ECO", "head_of_department": "Dr. Rachna Jawa"}
                ]
            },
            {
                "name": "Chitkara University, Punjab",
                "code": "AISHE-U-0374",
                "institution_type": Institution.InstitutionType.UNIVERSITY,
                "state": "Punjab",
                "city": "Rajpura / Chandigarh",
                "website": "https://www.chitkara.edu.in",
                "nirf_rank": 15,
                "is_verified": True,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Chitkara_University_logo.png/220px-Chitkara_University_logo.png",
                "departments": [
                    {"name": "Computer Science & Engineering", "code": "CSE", "head_of_department": "Dr. Ramesh Iyer"},
                    {"name": "Electronics & Communication Engineering", "code": "ECE", "head_of_department": "Dr. Sandeep Arora"},
                    {"name": "Mechanical Engineering", "code": "MECH", "head_of_department": "Dr. Gurwinder Singh"},
                    {"name": "Civil Engineering", "code": "CIVIL", "head_of_department": "Dr. Pankaj Kumar"},
                    {"name": "Chitkara Business School", "code": "CBS", "head_of_department": "Dr. Babita Singla"},
                    {"name": "Chitkara Design School", "code": "CDS", "head_of_department": "Prof. Nitin Dutt"},
                    {"name": "Chitkara College of Pharmacy", "code": "CCP", "head_of_department": "Dr. Sandeep Sharma"},
                    {"name": "Chitkara School of Health Sciences", "code": "CSHS", "head_of_department": "Dr. Sonika Bakshi"},
                    {"name": "Chitkara School of Planning & Architecture", "code": "CSPA", "head_of_department": "Prof. I.J.S. Bakshi"},
                    {"name": "Chitkara College of Hotel Management", "code": "CCHM", "head_of_department": "Chef Amit Sood"},
                    {"name": "Chitkara School of Mass Communication", "code": "CSMC", "head_of_department": "Dr. Ashutosh Mishra"},
                    {"name": "Chitkara Law School", "code": "CLS", "head_of_department": "Dr. Jasneet Kaur"}
                ]
            }
        ]

        for idata in institutions_data:
            departments_data = idata.pop("departments")
            inst, created = Institution.objects.update_or_create(
                name=idata["name"],
                defaults=idata
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"  [Institution] {inst.name} ({status}, AISHE: {inst.code})")

            for ddata in departments_data:
                dept, d_created = Department.objects.update_or_create(
                    institution=inst,
                    name=ddata["name"],
                    defaults={
                        "code": ddata["code"],
                        "head_of_department": ddata["head_of_department"]
                    }
                )
                d_status = "Created" if d_created else "Updated"
                self.stdout.write(f"    - Department: {dept.name} ({d_status})")

        # 2. FACULTY PERSONA LINKAGE
        faculty_user = User.objects.filter(username="faculty_dean").first()
        if faculty_user:
            nitk = Institution.objects.filter(name__icontains="Karnataka").first()
            cse_dept = Department.objects.filter(institution=nitk, name__icontains="Computer Science").first()

            fp, _ = FacultyProfile.objects.update_or_create(
                user=faculty_user,
                defaults={
                    "institution": nitk,
                    "department": cse_dept,
                    "designation": "Head of Training & Placement Cell",
                    "employee_id": "NITK-FAC-2018",
                    "contact_phone": "+91 98111 22334",
                    "is_institution_admin": True
                }
            )
            self.stdout.write(self.style.SUCCESS(f"  [Faculty Link] {faculty_user.username} -> {nitk.name} ({fp.designation})"))

        # 2.1 CHITKARA FACULTY PERSONA (DR. RAMESH IYER)
        chitkara = Institution.objects.filter(name__icontains="Chitkara").first()
        if chitkara:
            c_dept = Department.objects.filter(institution=chitkara, name__icontains="Computer Science").first()
            iyer_user, _ = User.objects.get_or_create(
                username="dr_iyer",
                defaults={
                    "email": "ramesh.iyer@chitkara.edu.in",
                    "role": User.Role.ACADEMIA,
                    "first_name": "Ramesh",
                    "last_name": "Iyer",
                    "phone_number": "+919876500001"
                }
            )
            iyer_user.set_password("password123")
            iyer_user.save()

            fp_t, _ = FacultyProfile.objects.update_or_create(
                user=iyer_user,
                defaults={
                    "institution": chitkara,
                    "department": c_dept,
                    "designation": "Dean of Academic Collaborations & Industry Engagement",
                    "employee_id": "CU-FAC-1042",
                    "contact_phone": "+91 98765 00001",
                    "is_institution_admin": True
                }
            )
            self.stdout.write(self.style.SUCCESS(f"  [Faculty Link] {iyer_user.username} -> {chitkara.name} ({fp_t.designation})"))

        self.stdout.write(self.style.SUCCESS("[OK] Successfully seeded verified institutions, academic departments & faculty!"))

