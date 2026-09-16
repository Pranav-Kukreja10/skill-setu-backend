from django.core.management.base import BaseCommand
from students.models import IndustrySector, JobBenchmark

class Command(BaseCommand):
    help = "Seeds database with multi-department industry standards"

    def handle(self, *args, **options):
        self.stdout.write("Clearing previous benchmarks...")
        JobBenchmark.objects.all().delete()
        IndustrySector.objects.all().delete()

        # Define 3 departments
        it_sector = IndustrySector.objects.create(name="Information Technology", description="Software Development and Cloud Engineering")
        mech_sector = IndustrySector.objects.create(name="Mechanical Engineering", description="Industrial CAD, Fluid Mechanics, and Aerospace Systems")
        finance_sector = IndustrySector.objects.create(name="Finance & Commerce", description="Accounting, Corporate Finance, and Banking Analytics")

        # 1. Seed Software Engineering Benchmark
        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer",
            core_skills=["python", "django", "fastapi", "postgresql", "sql", "flask", "c"],
            methodology_skills=["rest api", "mvc", "docker", "gunicorn", "jwt", "quality assurance"],
            tooling_skills=["git", "trello", "jira", "postman"]
        )

        # 2. Seed Mechanical Design Benchmark
        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="CAD Design Engineer",
            core_skills=["autocad", "solidworks", "catia", "ansys", "thermodynamics", "fluid mechanics"],
            methodology_skills=["gd&t", "fea", "geometric dimensioning", "stress analysis"],
            tooling_skills=["matlab", "msc nasran", "fusion 360"]
        )

        # 3. Seed Finance Analyst Benchmark
        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Financial Analyst",
            core_skills=["accounting", "valuation", "corporate finance", "excel", "tableau", "statistics"],
            methodology_skills=["dcf", "financial modeling", "portfolio management", "trend analysis"],
            tooling_skills=["powerbi", "ms office", "bloomberg terminal"]
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded multi-department job benchmarks!"))
