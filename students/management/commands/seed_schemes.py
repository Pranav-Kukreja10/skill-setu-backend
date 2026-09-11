from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from students.models import GovernmentScheme

class Command(BaseCommand):
    help = "Seeds authentic multi-domain government schemes and corporate DEI affirmative action initiatives."

    def handle(self, *args, **options):
        now = timezone.now()

        schemes_data = [
            # 1. Engineering & Technology
            {
                "title": "AICTE Pragati Scholarship for Girls 2025-2026",
                "sponsoring_agency": "All India Council for Technical Education (AICTE), Ministry of Education, GoI",
                "domain": GovernmentScheme.Domain.TECH,
                "scheme_type": GovernmentScheme.SchemeType.SCHOLARSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 50,000 per annum + College Tuition Reimbursement",
                "description": (
                    "Flagship Government of India initiative to empower female students pursuing technical education. "
                    "Open to female candidates admitted to the 1st year or 2nd year (lateral entry) of AICTE-approved degree programs. "
                    "Covers college tuition, books, computers, equipment, and certified software tools."
                ),
                "eligible_degrees": ["B.Tech", "B.E.", "BCA", "MCA", "B.Sc Computer Science", "M.Tech"],
                "min_cgpa": 6.5,
                "application_deadline": now + timedelta(days=60),
                "official_portal_url": "https://scholarships.gov.in/aicte-pragati",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "emerald"
            },
            {
                "title": "TechSaksham Initiative for Women in Technology",
                "sponsoring_agency": "Microsoft India & SAP India (Joint National AICTE Partnership)",
                "domain": GovernmentScheme.Domain.TECH,
                "scheme_type": GovernmentScheme.SchemeType.MENTORSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "Free Industry Cloud & AI Certification + 1-on-1 Corporate Mentorship",
                "description": (
                    "Joint corporate initiative between Microsoft and SAP India designed to equip 60,000+ female students "
                    "with foundational skills in Cloud Computing, Artificial Intelligence, and Enterprise Application Development. "
                    "Includes hands-on hackathons, technical project reviews, and direct interview waivers."
                ),
                "eligible_degrees": ["B.Tech", "B.E.", "BCA", "MCA", "B.Sc", "M.Tech"],
                "min_cgpa": 7.0,
                "application_deadline": now + timedelta(days=45),
                "official_portal_url": "https://techsaksham.in",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "blue"
            },
            {
                "title": "Amazon WOW (Women of the World) SDE Intern & FTE Hiring",
                "sponsoring_agency": "Amazon India",
                "domain": GovernmentScheme.Domain.TECH,
                "scheme_type": GovernmentScheme.SchemeType.INTERNSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 1,10,000/month Stipend + Full-Time SDE Conversion Track",
                "description": (
                    "Targeted affirmative action and talent incubation program designed to bridge gender disparity in software engineering. "
                    "Provides mentorship, coding bootcamps, and direct interview opportunities for female engineering students "
                    "across India for 6-month Software Development Engineer (SDE) internships."
                ),
                "eligible_degrees": ["B.Tech", "B.E.", "MCA", "M.Tech"],
                "min_cgpa": 7.5,
                "application_deadline": now + timedelta(days=30),
                "official_portal_url": "https://amazonwowindia.splashthat.com",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "amber"
            },
            {
                "title": "Adobe India Women-in-Technology (WIT) Scholarship",
                "sponsoring_agency": "Adobe Research India",
                "domain": GovernmentScheme.Domain.TECH,
                "scheme_type": GovernmentScheme.SchemeType.SCHOLARSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "$10,000 Financial Grant + Summer Research Internship at Adobe",
                "description": (
                    "Global prestigious scholarship created to encourage outstanding female university students in Computing "
                    "and Design. Covers tuition fees, an opportunity to intern at Adobe Research Labs in Bengaluru, and fully funded "
                    "travel to the annual Grace Hopper Celebration."
                ),
                "eligible_degrees": ["B.Tech", "B.E.", "M.Tech", "MCA", "B.Des"],
                "min_cgpa": 8.0,
                "application_deadline": now + timedelta(days=75),
                "official_portal_url": "https://research.adobe.com/scholarship/women-in-technology/",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "rose"
            },

            # 2. Commerce, Banking & Finance
            {
                "title": "ICICI Bank DNA (Diversity Nurturing Academy) Career Fellowship",
                "sponsoring_agency": "ICICI Bank Ltd.",
                "domain": GovernmentScheme.Domain.FINANCE,
                "scheme_type": GovernmentScheme.SchemeType.INTERNSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 45,000/month Stipend + Investment Banking Mentorship",
                "description": (
                    "Affirmative action talent accelerator designed to cultivate women leaders in retail banking, "
                    "wealth management, equity research, and commercial credit. Female students undergo practical training "
                    "on financial modeling, statutory compliance, and corporate client relationship building."
                ),
                "eligible_degrees": ["B.Com", "M.Com", "BBA", "MBA", "CA Inter", "CMA"],
                "min_cgpa": 7.0,
                "application_deadline": now + timedelta(days=50),
                "official_portal_url": "https://www.icicicareers.com/diversity-academy",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "indigo"
            },
            {
                "title": "SEBI & NISM Women in Capital Markets Research Grant",
                "sponsoring_agency": "Securities and Exchange Board of India (SEBI) & NISM",
                "domain": GovernmentScheme.Domain.FINANCE,
                "scheme_type": GovernmentScheme.SchemeType.RESEARCH_GRANT,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 60,000 Research Grant + NISM Regulatory Certification Waiver",
                "description": (
                    "National research initiative encouraging female commerce and economics scholars to produce high-impact "
                    "papers on algorithmic market microstructure, ESG disclosure frameworks, and retail investor protection."
                ),
                "eligible_degrees": ["B.Com", "M.Com", "MBA", "B.Sc Economics"],
                "min_cgpa": 7.5,
                "application_deadline": now + timedelta(days=90),
                "official_portal_url": "https://www.nism.ac.in/women-in-capital-markets",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "cyan"
            },

            # 3. Business Administration & Management
            {
                "title": "Tata Affirmative Action Women Leadership Initiative",
                "sponsoring_agency": "Tata Sons & Tata Group Companies",
                "domain": GovernmentScheme.Domain.MANAGEMENT,
                "scheme_type": GovernmentScheme.SchemeType.MENTORSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 75,000 Merit Award + Executive Mentorship with Tata CXOs",
                "description": (
                    "Prestigious pan-Tata initiative identifying high-potential female students across management, human resources, "
                    "and supply chain disciplines. Fellows are paired with senior Tata leaders and assigned high-visibility strategic deliverables."
                ),
                "eligible_degrees": ["BBA", "MBA", "PGDM", "B.Com"],
                "min_cgpa": 7.5,
                "application_deadline": now + timedelta(days=40),
                "official_portal_url": "https://www.tata.com/careers/women-in-leadership",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "blue"
            },
            {
                "title": "P&G Lead With Diversity Fellowship",
                "sponsoring_agency": "Procter & Gamble India",
                "domain": GovernmentScheme.Domain.MANAGEMENT,
                "scheme_type": GovernmentScheme.SchemeType.INTERNSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 80,000/month Stipend + Brand Management Summer Residency",
                "description": (
                    "Dedicated female leadership accelerator focused on real-world brand operations, consumer market research, "
                    "and supply chain logistics. Top performers receive pre-placement offers (PPO) for management trainee positions."
                ),
                "eligible_degrees": ["BBA", "MBA", "PGDM"],
                "min_cgpa": 7.0,
                "application_deadline": now + timedelta(days=35),
                "official_portal_url": "https://www.pgcareers.com/diversity-fellowship-india",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "teal"
            },

            # 4. Design & Creative Arts
            {
                "title": "Adobe Design Circle Global UI/UX Scholarship",
                "sponsoring_agency": "Adobe Inc. & Design Leaders Council",
                "domain": GovernmentScheme.Domain.DESIGN,
                "scheme_type": GovernmentScheme.SchemeType.SCHOLARSHIP,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "$25,000 Global Tuition Grant + Design Studio Mentorship",
                "description": (
                    "International scholarship initiative dedicated to supporting underrepresented female product designers, "
                    "UX researchers, and design systems engineers. Includes annual software licenses, portfolio reviews from world-renowned "
                    "creative directors, and career placement support."
                ),
                "eligible_degrees": ["B.Des", "M.Des", "B.Tech", "Fine Arts"],
                "min_cgpa": 6.8,
                "application_deadline": now + timedelta(days=80),
                "official_portal_url": "https://www.adobe.com/design-circle/scholarship",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "fuchsia"
            },
            {
                "title": "Women in Animation & Digital Arts (WADA) India Grant",
                "sponsoring_agency": "National Media & Creative Arts Council",
                "domain": GovernmentScheme.Domain.DESIGN,
                "scheme_type": GovernmentScheme.SchemeType.RESEARCH_GRANT,
                "target_gender": GovernmentScheme.TargetGender.FEMALE_ONLY,
                "benefit_summary": "INR 50,000 Equipment Grant + Free Figma Organization & Adobe CC License",
                "description": (
                    "Affirmative action grant providing computing hardware, graphic tablets, and professional design software "
                    "to talented female designers in interactive media, 3D simulation, and user experience design."
                ),
                "eligible_degrees": ["B.Des", "M.Des", "BCA", "B.Tech"],
                "min_cgpa": 6.5,
                "application_deadline": now + timedelta(days=55),
                "official_portal_url": "https://wada-india.org/grants",
                "status": GovernmentScheme.SchemeStatus.ACTIVE,
                "badge_color": "purple"
            }
        ]

        count = 0
        for item in schemes_data:
            scheme, created = GovernmentScheme.objects.update_or_create(
                title=item["title"],
                defaults=item
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} multi-domain government & DEI schemes!"))
