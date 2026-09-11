from django.core.management.base import BaseCommand
from institutions.models import Institution, Department

INSTITUTIONS_CATALOG = [
    # --- 23 INDIAN INSTITUTES OF TECHNOLOGY (IITs) ---
    {"name": "Indian Institute of Technology (IIT) Madras", "code": "IITM", "type": "INSTITUTE", "city": "Chennai", "state": "Tamil Nadu", "rank": 1},
    {"name": "Indian Institute of Technology (IIT) Delhi", "code": "IITD", "type": "INSTITUTE", "city": "New Delhi", "state": "Delhi", "rank": 2},
    {"name": "Indian Institute of Technology (IIT) Bombay", "code": "IITB", "type": "INSTITUTE", "city": "Mumbai", "state": "Maharashtra", "rank": 3},
    {"name": "Indian Institute of Technology (IIT) Kanpur", "code": "IITK", "type": "INSTITUTE", "city": "Kanpur", "state": "Uttar Pradesh", "rank": 4},
    {"name": "Indian Institute of Technology (IIT) Kharagpur", "code": "IITKGP", "type": "INSTITUTE", "city": "Kharagpur", "state": "West Bengal", "rank": 5},
    {"name": "Indian Institute of Technology (IIT) Roorkee", "code": "IITR", "type": "INSTITUTE", "city": "Roorkee", "state": "Uttarakhand", "rank": 6},
    {"name": "Indian Institute of Technology (IIT) Guwahati", "code": "IITG", "type": "INSTITUTE", "city": "Guwahati", "state": "Assam", "rank": 7},
    {"name": "Indian Institute of Technology (IIT) Hyderabad", "code": "IITH", "type": "INSTITUTE", "city": "Sangareddy", "state": "Telangana", "rank": 8},
    {"name": "Indian Institute of Technology (BHU) Varanasi", "code": "IIT-BHU", "type": "INSTITUTE", "city": "Varanasi", "state": "Uttar Pradesh", "rank": 10},
    {"name": "Indian Institute of Technology (IIT) Indore", "code": "IITI", "type": "INSTITUTE", "city": "Indore", "state": "Madhya Pradesh", "rank": 13},
    {"name": "Indian Institute of Technology (ISM) Dhanbad", "code": "IIT-ISM", "type": "INSTITUTE", "city": "Dhanbad", "state": "Jharkhand", "rank": 15},
    {"name": "Indian Institute of Technology (IIT) Ropar", "code": "IITRPR", "type": "INSTITUTE", "city": "Rupnagar", "state": "Punjab", "rank": 22},
    {"name": "Indian Institute of Technology (IIT) Mandi", "code": "IIT-MANDI", "type": "INSTITUTE", "city": "Mandi", "state": "Himachal Pradesh", "rank": 33},
    {"name": "Indian Institute of Technology (IIT) Gandhinagar", "code": "IITGN", "type": "INSTITUTE", "city": "Gandhinagar", "state": "Gujarat", "rank": 18},
    {"name": "Indian Institute of Technology (IIT) Jodhpur", "code": "IITJ", "type": "INSTITUTE", "city": "Jodhpur", "state": "Rajasthan", "rank": 30},
    {"name": "Indian Institute of Technology (IIT) Patna", "code": "IITP", "type": "INSTITUTE", "city": "Patna", "state": "Bihar", "rank": 41},
    {"name": "Indian Institute of Technology (IIT) Bhubaneswar", "code": "IITBBS", "type": "INSTITUTE", "city": "Bhubaneswar", "state": "Odisha", "rank": 47},
    {"name": "Indian Institute of Technology (IIT) Tirupati", "code": "IITTP", "type": "INSTITUTE", "city": "Tirupati", "state": "Andhra Pradesh", "rank": 59},
    {"name": "Indian Institute of Technology (IIT) Palakkad", "code": "IITPKD", "type": "INSTITUTE", "city": "Palakkad", "state": "Kerala", "rank": 69},
    {"name": "Indian Institute of Technology (IIT) Goa", "code": "IITGOA", "type": "INSTITUTE", "city": "Ponda", "state": "Goa", "rank": 75},
    {"name": "Indian Institute of Technology (IIT) Dharwad", "code": "IITDH", "type": "INSTITUTE", "city": "Dharwad", "state": "Karnataka", "rank": 85},
    {"name": "Indian Institute of Technology (IIT) Bhilai", "code": "IITBHILAI", "type": "INSTITUTE", "city": "Bhilai", "state": "Chhattisgarh", "rank": 81},
    {"name": "Indian Institute of Technology (IIT) Jammu", "code": "IITJAMMU", "type": "INSTITUTE", "city": "Jammu", "state": "Jammu and Kashmir", "rank": 67},

    # --- TOP 31 NATIONAL INSTITUTES OF TECHNOLOGY (NITs) ---
    {"name": "National Institute of Technology (NIT) Tiruchirappalli", "code": "NITT", "type": "INSTITUTE", "city": "Tiruchirappalli", "state": "Tamil Nadu", "rank": 9},
    {"name": "National Institute of Technology (NIT) Karnataka, Surathkal", "code": "NITK", "type": "INSTITUTE", "city": "Surathkal", "state": "Karnataka", "rank": 12},
    {"name": "National Institute of Technology (NIT) Rourkela", "code": "NITRKL", "type": "INSTITUTE", "city": "Rourkela", "state": "Odisha", "rank": 16},
    {"name": "National Institute of Technology (NIT) Warangal", "code": "NITW", "type": "INSTITUTE", "city": "Warangal", "state": "Telangana", "rank": 21},
    {"name": "National Institute of Technology (NIT) Calicut", "code": "NITC", "type": "INSTITUTE", "city": "Kozhikode", "state": "Kerala", "rank": 23},
    {"name": "Visvesvaraya National Institute of Technology (VNIT) Nagpur", "code": "VNIT", "type": "INSTITUTE", "city": "Nagpur", "state": "Maharashtra", "rank": 41},
    {"name": "Malaviya National Institute of Technology (MNIT) Jaipur", "code": "MNIT", "type": "INSTITUTE", "city": "Jaipur", "state": "Rajasthan", "rank": 37},
    {"name": "Motilal Nehru National Institute of Technology (MNNIT) Allahabad", "code": "MNNIT", "type": "INSTITUTE", "city": "Prayagraj", "state": "Uttar Pradesh", "rank": 49},
    {"name": "Sardar Vallabhbhai National Institute of Technology (SVNIT) Surat", "code": "SVNIT", "type": "INSTITUTE", "city": "Surat", "state": "Gujarat", "rank": 65},
    {"name": "Maulana Azad National Institute of Technology (MANIT) Bhopal", "code": "MANIT", "type": "INSTITUTE", "city": "Bhopal", "state": "Madhya Pradesh", "rank": 80},
    {"name": "National Institute of Technology (NIT) Kurukshetra", "code": "NITKKR", "type": "INSTITUTE", "city": "Kurukshetra", "state": "Haryana", "rank": 58},
    {"name": "National Institute of Technology (NIT) Durgapur", "code": "NITDGP", "type": "INSTITUTE", "city": "Durgapur", "state": "West Bengal", "rank": 43},
    {"name": "National Institute of Technology (NIT) Silchar", "code": "NITS", "type": "INSTITUTE", "city": "Silchar", "state": "Assam", "rank": 40},
    {"name": "Dr. B. R. Ambedkar National Institute of Technology (NIT) Jalandhar", "code": "NITJ", "type": "INSTITUTE", "city": "Jalandhar", "state": "Punjab", "rank": 46},
    {"name": "National Institute of Technology (NIT) Meghalaya", "code": "NITM", "type": "INSTITUTE", "city": "Shillong", "state": "Meghalaya", "rank": 72},
    {"name": "National Institute of Technology (NIT) Patna", "code": "NITP", "type": "INSTITUTE", "city": "Patna", "state": "Bihar", "rank": 56},
    {"name": "National Institute of Technology (NIT) Raipur", "code": "NITRR", "type": "INSTITUTE", "city": "Raipur", "state": "Chhattisgarh", "rank": 70},
    {"name": "National Institute of Technology (NIT) Srinagar", "code": "NITSRI", "type": "INSTITUTE", "city": "Srinagar", "state": "Jammu and Kashmir", "rank": 82},
    {"name": "National Institute of Technology (NIT) Agartala", "code": "NITA", "type": "INSTITUTE", "city": "Agartala", "state": "Tripura", "rank": 91},
    {"name": "National Institute of Technology (NIT) Goa", "code": "NITGOA", "type": "INSTITUTE", "city": "Farmagudi", "state": "Goa", "rank": 90},
    {"name": "National Institute of Technology (NIT) Jamshedpur", "code": "NITJSR", "type": "INSTITUTE", "city": "Jamshedpur", "state": "Jharkhand", "rank": 101},
    {"name": "National Institute of Technology (NIT) Hamirpur", "code": "NITH", "type": "INSTITUTE", "city": "Hamirpur", "state": "Himachal Pradesh", "rank": 128},

    # --- INDIAN INSTITUTES OF INFORMATION TECHNOLOGY (IIITs) ---
    {"name": "International Institute of Information Technology (IIIT) Hyderabad", "code": "IIITH", "type": "INSTITUTE", "city": "Hyderabad", "state": "Telangana", "rank": 55},
    {"name": "International Institute of Information Technology (IIIT) Bangalore", "code": "IIITB", "type": "INSTITUTE", "city": "Bengaluru", "state": "Karnataka", "rank": 74},
    {"name": "Indraprastha Institute of Information Technology (IIIT) Delhi", "code": "IIITD", "type": "INSTITUTE", "city": "New Delhi", "state": "Delhi", "rank": 75},
    {"name": "Indian Institute of Information Technology (IIIT) Allahabad", "code": "IIITA", "type": "INSTITUTE", "city": "Prayagraj", "state": "Uttar Pradesh", "rank": 89},
    {"name": "Atal Bihari Vajpayee Indian Institute of Information Technology (IIITM) Gwalior", "code": "IIITMG", "type": "INSTITUTE", "city": "Gwalior", "state": "Madhya Pradesh", "rank": 88},
    {"name": "Indian Institute of Information Technology (IIIT) Lucknow", "code": "IIITL", "type": "INSTITUTE", "city": "Lucknow", "state": "Uttar Pradesh", "rank": 120},
    {"name": "Indian Institute of Information Technology (IIIT) Pune", "code": "IIITP", "type": "INSTITUTE", "city": "Pune", "state": "Maharashtra", "rank": 130},
    {"name": "Indian Institute of Information Technology (IIIT) Sri City", "code": "IIITS", "type": "INSTITUTE", "city": "Chittoor", "state": "Andhra Pradesh", "rank": 135},
    {"name": "Indian Institute of Information Technology (IIIT) Vadodara", "code": "IIITV", "type": "INSTITUTE", "city": "Gandhinagar", "state": "Gujarat", "rank": 140},

    # --- INDIAN INSTITUTES OF MANAGEMENT (IIMs) ---
    {"name": "Indian Institute of Management (IIM) Ahmedabad", "code": "IIMA", "type": "INSTITUTE", "city": "Ahmedabad", "state": "Gujarat", "rank": 1},
    {"name": "Indian Institute of Management (IIM) Bangalore", "code": "IIMB", "type": "INSTITUTE", "city": "Bengaluru", "state": "Karnataka", "rank": 2},
    {"name": "Indian Institute of Management (IIM) Calcutta", "code": "IIMC", "type": "INSTITUTE", "city": "Kolkata", "state": "West Bengal", "rank": 3},
    {"name": "Indian Institute of Management (IIM) Lucknow", "code": "IIML", "type": "INSTITUTE", "city": "Lucknow", "state": "Uttar Pradesh", "rank": 4},
    {"name": "Indian Institute of Management (IIM) Kozhikode", "code": "IIMK", "type": "INSTITUTE", "city": "Kozhikode", "state": "Kerala", "rank": 5},
    {"name": "Indian Institute of Management (IIM) Indore", "code": "IIMI", "type": "INSTITUTE", "city": "Indore", "state": "Madhya Pradesh", "rank": 8},
    {"name": "Indian Institute of Management (IIM) Mumbai (formerly NITIE)", "code": "IIMM", "type": "INSTITUTE", "city": "Mumbai", "state": "Maharashtra", "rank": 7},
    {"name": "Indian Institute of Management (IIM) Shillong", "code": "IIMS", "type": "INSTITUTE", "city": "Shillong", "state": "Meghalaya", "rank": 26},
    {"name": "Indian Institute of Management (IIM) Rohtak", "code": "IIMR", "type": "INSTITUTE", "city": "Rohtak", "state": "Haryana", "rank": 12},
    {"name": "Indian Institute of Management (IIM) Ranchi", "code": "IIMRNC", "type": "INSTITUTE", "city": "Ranchi", "state": "Jharkhand", "rank": 17},
    {"name": "Indian Institute of Management (IIM) Raipur", "code": "IIMRPR", "type": "INSTITUTE", "city": "Raipur", "state": "Chhattisgarh", "rank": 14},

    # --- APEX SCIENCE & RESEARCH INSTITUTES ---
    {"name": "Indian Institute of Science (IISc) Bangalore", "code": "IISC", "type": "INSTITUTE", "city": "Bengaluru", "state": "Karnataka", "rank": 1},
    {"name": "Tata Institute of Fundamental Research (TIFR) Mumbai", "code": "TIFR", "type": "INSTITUTE", "city": "Mumbai", "state": "Maharashtra", "rank": 25},
    {"name": "Indian Statistical Institute (ISI) Kolkata", "code": "ISI-KOL", "type": "INSTITUTE", "city": "Kolkata", "state": "West Bengal", "rank": 35},
    {"name": "Indian Institute of Science Education and Research (IISER) Pune", "code": "IISER-PUNE", "type": "INSTITUTE", "city": "Pune", "state": "Maharashtra", "rank": 27},
    {"name": "Indian Institute of Science Education and Research (IISER) Mohali", "code": "IISER-MOHALI", "type": "INSTITUTE", "city": "Mohali", "state": "Punjab", "rank": 50},

    # --- NATIONAL INSTITUTES OF FASHION TECHNOLOGY (NIFTs) ---
    {"name": "National Institute of Fashion Technology (NIFT) New Delhi", "code": "NIFT-DELHI", "type": "INSTITUTE", "city": "New Delhi", "state": "Delhi", "rank": 1},
    {"name": "National Institute of Fashion Technology (NIFT) Mumbai", "code": "NIFT-MUMBAI", "type": "INSTITUTE", "city": "Mumbai", "state": "Maharashtra", "rank": 2},
    {"name": "National Institute of Fashion Technology (NIFT) Bengaluru", "code": "NIFT-BLR", "type": "INSTITUTE", "city": "Bengaluru", "state": "Karnataka", "rank": 3},
    {"name": "National Institute of Fashion Technology (NIFT) Kolkata", "code": "NIFT-KOL", "type": "INSTITUTE", "city": "Kolkata", "state": "West Bengal", "rank": 5},
    {"name": "National Institute of Fashion Technology (NIFT) Chennai", "code": "NIFT-CHN", "type": "INSTITUTE", "city": "Chennai", "state": "Tamil Nadu", "rank": 6},
    {"name": "National Institute of Fashion Technology (NIFT) Gandhinagar", "code": "NIFT-GN", "type": "INSTITUTE", "city": "Gandhinagar", "state": "Gujarat", "rank": 7},
    {"name": "National Institute of Fashion Technology (NIFT) Hyderabad", "code": "NIFT-HYD", "type": "INSTITUTE", "city": "Hyderabad", "state": "Telangana", "rank": 4},
    {"name": "National Institute of Fashion Technology (NIFT) Patna", "code": "NIFT-PATNA", "type": "INSTITUTE", "city": "Patna", "state": "Bihar", "rank": 11},

    # --- PREMIER CENTRAL & STATE UNIVERSITIES ---
    {"name": "University of Delhi (Delhi University / DU)", "code": "DU", "type": "UNIVERSITY", "city": "New Delhi", "state": "Delhi", "rank": 11},
    {"name": "Shri Ram College of Commerce (SRCC), Delhi University", "code": "SRCC-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 11},
    {"name": "St. Stephen's College, Delhi University", "code": "STEPHENS-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 14},
    {"name": "Hindu College, Delhi University", "code": "HINDU-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 1},
    {"name": "Hansraj College, Delhi University", "code": "HANSRAJ-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 12},
    {"name": "Miranda House, Delhi University", "code": "MIRANDA-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 2},
    {"name": "Lady Shri Ram College for Women (LSR), Delhi University", "code": "LSR-DU", "type": "COLLEGE", "city": "New Delhi", "state": "Delhi", "rank": 9},
    {"name": "Jawaharlal Nehru University (JNU)", "code": "JNU", "type": "UNIVERSITY", "city": "New Delhi", "state": "Delhi", "rank": 2},
    {"name": "Banaras Hindu University (BHU)", "code": "BHU", "type": "UNIVERSITY", "city": "Varanasi", "state": "Uttar Pradesh", "rank": 5},
    {"name": "Jamia Millia Islamia", "code": "JMI", "type": "UNIVERSITY", "city": "New Delhi", "state": "Delhi", "rank": 3},
    {"name": "Aligarh Muslim University (AMU)", "code": "AMU", "type": "UNIVERSITY", "city": "Aligarh", "state": "Uttar Pradesh", "rank": 9},
    {"name": "University of Hyderabad", "code": "UOH", "type": "UNIVERSITY", "city": "Hyderabad", "state": "Telangana", "rank": 10},
    {"name": "Jadavpur University", "code": "JU", "type": "UNIVERSITY", "city": "Kolkata", "state": "West Bengal", "rank": 4},
    {"name": "Anna University", "code": "ANNA-UNIV", "type": "UNIVERSITY", "city": "Chennai", "state": "Tamil Nadu", "rank": 14},
    {"name": "University of Calcutta", "code": "CAL-UNIV", "type": "UNIVERSITY", "city": "Kolkata", "state": "West Bengal", "rank": 12},
    {"name": "Savitribai Phule Pune University", "code": "SPPU", "type": "UNIVERSITY", "city": "Pune", "state": "Maharashtra", "rank": 19},
    {"name": "University of Mumbai", "code": "MU", "type": "UNIVERSITY", "city": "Mumbai", "state": "Maharashtra", "rank": 56},
    {"name": "Panjab University", "code": "PU-CHD", "type": "UNIVERSITY", "city": "Chandigarh", "state": "Punjab", "rank": 25},
    {"name": "Delhi Technological University (DTU, formerly DCE)", "code": "DTU", "type": "UNIVERSITY", "city": "New Delhi", "state": "Delhi", "rank": 29},
    {"name": "Netaji Subhas University of Technology (NSUT)", "code": "NSUT", "type": "UNIVERSITY", "city": "New Delhi", "state": "Delhi", "rank": 60},

    # --- TOP AUTONOMOUS & PRIVATE UNIVERSITIES ---
    {"name": "Birla Institute of Technology and Science (BITS) Pilani", "code": "BITS-PILANI", "type": "UNIVERSITY", "city": "Pilani", "state": "Rajasthan", "rank": 20},
    {"name": "BITS Pilani (K. K. Birla Goa Campus)", "code": "BITS-GOA", "type": "UNIVERSITY", "city": "Zuarinagar", "state": "Goa", "rank": 20},
    {"name": "BITS Pilani (Hyderabad Campus)", "code": "BITS-HYD", "type": "UNIVERSITY", "city": "Hyderabad", "state": "Telangana", "rank": 20},
    {"name": "Vellore Institute of Technology (VIT) Vellore", "code": "VIT", "type": "UNIVERSITY", "city": "Vellore", "state": "Tamil Nadu", "rank": 11},
    {"name": "Manipal Academy of Higher Education (MAHE) Manipal", "code": "MAHE", "type": "UNIVERSITY", "city": "Manipal", "state": "Karnataka", "rank": 6},
    {"name": "Thapar Institute of Engineering and Technology", "code": "TIET", "type": "UNIVERSITY", "city": "Patiala", "state": "Punjab", "rank": 22},
    {"name": "Chitkara University, Punjab & Himachal Pradesh", "code": "CHITKARA", "type": "UNIVERSITY", "city": "Rajpura", "state": "Punjab", "rank": 101},
    {"name": "Amity University, Noida", "code": "AMITY", "type": "UNIVERSITY", "city": "Noida", "state": "Uttar Pradesh", "rank": 35},
    {"name": "SRM Institute of Science and Technology, Chennai", "code": "SRM", "type": "UNIVERSITY", "city": "Kattankulathur", "state": "Tamil Nadu", "rank": 18},
    {"name": "Chandigarh University, Mohali", "code": "CU-MOHALI", "type": "UNIVERSITY", "city": "Gharuan", "state": "Punjab", "rank": 45},
    {"name": "Ashoka University, Sonipat", "code": "ASHOKA", "type": "UNIVERSITY", "city": "Sonipat", "state": "Haryana", "rank": 88},
    {"name": "Shiv Nadar University, Greater Noida", "code": "SNU", "type": "UNIVERSITY", "city": "Greater Noida", "state": "Uttar Pradesh", "rank": 62},
    {"name": "Symbiosis International University, Pune", "code": "SIU", "type": "UNIVERSITY", "city": "Pune", "state": "Maharashtra", "rank": 32},
    {"name": "Christ (Deemed to be University), Bengaluru", "code": "CHRIST", "type": "UNIVERSITY", "city": "Bengaluru", "state": "Karnataka", "rank": 67},

    # --- TOP COMMERCE, ARTS & LAW INSTITUTIONS ---
    {"name": "St. Xavier's College, Kolkata", "code": "SXC-KOL", "type": "COLLEGE", "city": "Kolkata", "state": "West Bengal", "rank": 5},
    {"name": "Loyola College, Chennai", "code": "LOYOLA-CHN", "type": "COLLEGE", "city": "Chennai", "state": "Tamil Nadu", "rank": 7},
    {"name": "National Law School of India University (NLSIU) Bengaluru", "code": "NLSIU", "type": "UNIVERSITY", "city": "Bengaluru", "state": "Karnataka", "rank": 1},
    {"name": "NALSAR University of Law, Hyderabad", "code": "NALSAR", "type": "UNIVERSITY", "city": "Hyderabad", "state": "Telangana", "rank": 3},
]

DEFAULT_DEPARTMENTS = [
    {"name": "Computer Science & Engineering", "code": "CSE"},
    {"name": "Information Technology", "code": "IT"},
    {"name": "Electronics & Communication Engineering", "code": "ECE"},
    {"name": "Mechanical Engineering", "code": "ME"},
    {"name": "Electrical & Electronics Engineering", "code": "EEE"},
    {"name": "Commerce, Accounts & Finance", "code": "CAF"},
    {"name": "Business Administration & Management", "code": "BAM"},
    {"name": "Design, UI/UX & Creative Arts", "code": "DES"},
    {"name": "Data Science & Artificial Intelligence", "code": "AI-DS"},
]

class Command(BaseCommand):
    help = "Seeds comprehensive catalog of top Indian higher-education institutions (IITs, NITs, IIITs, IIMs, NIFTs, Universities)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding comprehensive Indian higher-education institutions catalog..."))

        created_count = 0
        updated_count = 0

        for item in INSTITUTIONS_CATALOG:
            inst, created = Institution.objects.update_or_create(
                name=item["name"],
                defaults={
                    "code": item["code"],
                    "institution_type": item["type"],
                    "city": item["city"],
                    "state": item["state"],
                    "nirf_rank": item.get("rank"),
                    "is_verified": True
                }
            )

            # Auto-link standard foundational departments
            for dept_info in DEFAULT_DEPARTMENTS:
                Department.objects.get_or_create(
                    institution=inst,
                    name=dept_info["name"],
                    defaults={"code": dept_info["code"]}
                )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {len(INSTITUTIONS_CATALOG)} institutions! "
            f"(Created: {created_count}, Updated: {updated_count})"
        ))
