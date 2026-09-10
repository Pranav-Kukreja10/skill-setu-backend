from django.test import SimpleTestCase
from datetime import datetime
from institutions.schemas import (
    InstitutionOut,
    DepartmentOut,
    FacultyProfileOut,
    PlacementOverviewOut,
    SkillGapAnalysisOut,
    SkillDeficitItemOut,
    InDemandSkillsOut
)

class InstitutionSchemaUnitTests(SimpleTestCase):
    """
    Validates Pydantic schema contracts for Institutions, Faculty Profiles,
    and Institutional Placement reporting.
    """

    def test_institution_and_department_schema(self):
        dept = DepartmentOut(
            id=1,
            name="Computer Science & Engineering",
            code="CSE",
            head_of_department="Dr. Ananth Kumar",
            created_at=datetime.now()
        )
        self.assertEqual(dept.code, "CSE")

        inst = InstitutionOut(
            id=1,
            name="National Institute of Technology, Karnataka",
            code="AISHE-U-0237",
            institution_type="INSTITUTE",
            state="Karnataka",
            city="Surathkal",
            website="https://www.nitk.ac.in",
            nirf_rank=12,
            is_verified=True,
            departments=[dept],
            created_at=datetime.now()
        )
        self.assertEqual(inst.nirf_rank, 12)
        self.assertEqual(len(inst.departments), 1)

    def test_placement_overview_schema(self):
        overview = PlacementOverviewOut(
            total_students=100,
            placed_students=78,
            unplaced_students=22,
            placement_rate_percentage=78.0,
            total_companies=15,
            total_job_openings=25,
            total_applications=140,
            offers_extended=80,
            shortlisted_candidates=95,
            interview_pipeline_count=85
        )
        self.assertEqual(overview.placement_rate_percentage, 78.0)
        self.assertEqual(overview.placed_students, 78)

    def test_skill_gap_analysis_schema(self):
        item = SkillDeficitItemOut(
            skill="Django",
            market_demand_count=10,
            market_demand_percentage=50.0,
            student_supply_count=2,
            student_supply_percentage=10.0,
            deficit_percentage=40.0,
            average_student_proficiency=72.5
        )
        gap_report = SkillGapAnalysisOut(
            department="Computer Science",
            total_students=20,
            total_active_postings=20,
            deficit_skills=[item],
            faculty_recommendations=["Integrate hands-on Django lab"]
        )
        self.assertEqual(gap_report.deficit_skills[0].deficit_percentage, 40.0)
        self.assertEqual(len(gap_report.faculty_recommendations), 1)

    def test_learning_program_and_faculty_collaboration_schema(self):
        from recruiters.schemas import LearningProgramOut
        from institutions.schemas import FacultyOpportunityApplyIn

        program = LearningProgramOut(
            id=1,
            company_id=1,
            company_name="Google India",
            title="Google Cloud Architecture & Kubernetes Production Systems",
            program_type="TRAINING_PROGRAM",
            target_audience="ALL",
            description="Production cloud engineering curriculum",
            skills_covered=["Cloud", "Kubernetes"],
            duration="6 Weeks",
            mode="ONLINE",
            is_certified=True,
            created_at=datetime.now()
        )
        self.assertEqual(program.company_name, "Google India")
        self.assertTrue(program.is_certified)

        apply_in = FacultyOpportunityApplyIn(
            statement_of_purpose="Integrating EV battery management into academic syllabus.",
            research_areas=["Battery Management", "Thermal Dynamics"]
        )
        self.assertEqual(len(apply_in.research_areas), 2)
        self.assertIn("Battery Management", apply_in.research_areas)

