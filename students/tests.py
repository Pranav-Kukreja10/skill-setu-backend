from unittest.mock import patch
from django.test import SimpleTestCase
from students.services import (
    build_skills_matrix,
    compute_profile_strength,
)
from students.grader import ResilientGrader

class ScoringAndMathFormulasTest(SimpleTestCase):
    """
    Tests the mathematical and algorithmic integrity of Skill Setu's core scoring formulas:
    1. Skill Proficiency Weight (Ws = 0.6*Pe + 0.4*Er)
    2. Additive Credential Multiplier (Ws * 1.15)
    3. MCQ Time-Decay Multiplier (Mt)
    4. Progressive Cognitive Assessment Score (As = 0.3*MCQ + 0.7*Viva)
    5. Capped-root Plagiarism & Resume Padding Penalty (CS)
    6. Candidate Profile Strength Score (P_overall)
    """

    def test_skills_matrix_without_credentials(self):
        # Pe=80, Er=60 -> 0.6*80 + 0.4*60 = 48 + 24 = 72
        skills = [{"name": "python", "project_evidence_score": 80, "experience_recency_score": 60}]
        matrix = build_skills_matrix(skills, certifications=[])
        self.assertIn("python", matrix)
        self.assertEqual(matrix["python"]["weight"], 72)
        self.assertFalse(matrix["python"]["is_certified"])
        self.assertEqual(matrix["python"]["credential_bonus"], 1.0)

    def test_skills_matrix_with_credential_boost(self):
        # Base: 72. With +15% boost: min(100, round(72 * 1.15)) = round(82.8) = 83
        skills = [{"name": "aws", "project_evidence_score": 80, "experience_recency_score": 60}]
        certs = [{"name": "AWS Certified Solutions Architect", "skills_covered": ["AWS", "Cloud Computing"]}]
        matrix = build_skills_matrix(skills, certifications=certs)
        self.assertIn("aws", matrix)
        self.assertEqual(matrix["aws"]["weight"], 83)
        self.assertTrue(matrix["aws"]["is_certified"])
        self.assertEqual(matrix["aws"]["credential_bonus"], 1.15)

    def test_mcq_evaluation_and_time_decay(self):
        # Question 1: answered fast (10s) -> 1.0x -> score 100
        # Question 2: answered slower (40s) -> 1.0 - 0.3 * ((40-15)/45) = 1.0 - 0.1667 = 0.833 -> score 83
        original_questions = [
            {
                "id": 1,
                "type": "MCQ",
                "question_text": "What is Django?",
                "correct_answer": "Web framework",
                "explanation": "Django is a high-level Python web framework."
            },
            {
                "id": 2,
                "type": "MCQ",
                "question_text": "What is Python?",
                "correct_answer": "Programming language",
                "explanation": "Python is an interpreted language."
            }
        ]
        submitted_answers = [
            {"id": 1, "answer_text": "Web framework", "time_taken_seconds": 10},
            {"id": 2, "answer_text": "Programming language", "time_taken_seconds": 40}
        ]
        # Evaluates MCQs purely in-memory
        result = ResilientGrader.evaluate_test_submission(submitted_answers, original_questions, resume_rating=90.0)
        self.assertIn("mcq_average", result)
        self.assertGreater(result["mcq_average"], 80)
        self.assertLessEqual(result["mcq_average"], 100)

    def test_candidate_profile_strength_score(self):
        # P_overall = 0.45 * Cognitive + 0.30 * Projects + 0.15 * Certs + 0.10 * Academics
        class MockProfile:
            cgpa = 8.5
            overall_confidence_score = 80.0
            certifications = [
                {"name": "Cert A", "issuer": "AWS", "skills_covered": ["Cloud"]},
                {"name": "Cert B", "issuer": "GCP", "skills_covered": ["DevOps"]}
            ]
            skills_matrix = {
                "python": {"weight": 70, "project_evidence": 70, "experience_recency": 70}
            }

        mock_profile = MockProfile()
        # Expected:
        # Cognitive (45%): 80.0 * 0.45 = 36.0
        # Projects (30%): 70.0 * 0.30 = 21.0
        # Certs (15%): 2 certs -> 85.0 * 0.15 = 12.75
        # Academics (10%): 8.5 * 10 = 85.0 * 0.10 = 8.5
        # Total = 36.0 + 21.0 + 12.75 + 8.5 = 78.25
        score, breakdown = compute_profile_strength(mock_profile)
        self.assertAlmostEqual(score, 78.25, places=2)

    def test_digital_portfolio_and_internship_schemas(self):
        from students.schemas import (
            StudentPortfolioOutSchema,
            MilestoneLogCreateIn,
            ActiveInternshipDetailOut
        )
        milestone = MilestoneLogCreateIn(
            week_number=1,
            milestone_summary="Implemented zero-copy serialization driver",
            hours_logged=40,
            deliverables_url="https://github.com/alexdev99/driver"
        )
        self.assertEqual(milestone.week_number, 1)
        self.assertEqual(milestone.hours_logged, 40)

        internship = ActiveInternshipDetailOut(
            application_id=1,
            listing_id=10,
            title="Backend Systems Intern",
            company_name="Google India",
            location="Bengaluru",
            stipend_or_ctc="INR 50,000/month",
            role_type="INTERNSHIP",
            internship_status="IN_PROGRESS",
            mentor_name="Dr. Arvind Varma",
            mentor_rating=5.0,
            weekly_progress_logs=[milestone.dict()]
        )
        self.assertEqual(internship.mentor_rating, 5.0)
        self.assertEqual(len(internship.weekly_progress_logs), 1)

        portfolio = StudentPortfolioOutSchema(
            id=1,
            username="alex_dev",
            email="alex@university.edu",
            overall_confidence_score=85.0,
            profile_strength_score=82.5,
            placement_status="PLACED",
            is_verified=True,
            certifications=[{"name": "AWS PSA", "issuer": "AWS"}],
            achievements=[{"title": "SIH 2024 Finalist", "year": 2024}],
            academic_records=[{"semester": 1, "sgpa": 9.2, "credits": 24}],
            active_internships=[internship.dict()]
        )
        self.assertEqual(portfolio.username, "alex_dev")
        self.assertEqual(len(portfolio.achievements), 1)
        self.assertEqual(portfolio.achievements[0]["title"], "SIH 2024 Finalist")

    @patch.object(ResilientGrader, "_grade_viva_via_gemini")
    def test_retest_and_fault_acknowledgment_on_grading_failure(self, mock_grade_viva):
        """
        Guarantees that on external AI viva grading failures:
        - NEVER award unearned/free scores (cognitive_score=0, viva_avg=0, confidence_score=0)
        - Transparently acknowledges the fault on our side
        - Retest is mandated and required
        """
        mock_grade_viva.return_value = (None, "Oops! Service disruption on our end.")

        original_questions = [
            {
                "id": 1,
                "type": "MCQ",
                "question_text": "What is Python?",
                "correct_answer": "Language",
                "explanation": "Interpreted language"
            },
            {
                "id": 2,
                "type": "VIVA",
                "question_text": "Explain CAP Theorem in distributed databases.",
                "explanation": "Consistency, Availability, Partition tolerance trade-offs"
            }
        ]
        submitted_answers = [
            {"id": 1, "answer_text": "Language", "time_taken_seconds": 10},
            {"id": 2, "answer_text": "Network partitions require choosing between consistency and availability.", "time_taken_seconds": 45}
        ]

        result = ResilientGrader.evaluate_test_submission(submitted_answers, original_questions, resume_rating=85.0)

        self.assertFalse(result["success"])
        self.assertTrue(result["retest_required"])
        self.assertTrue(result["fault_acknowledged"])
        self.assertEqual(result["cognitive_score"], 0)
        self.assertEqual(result["viva_average"], 0)
        self.assertEqual(result["confidence_score"], 0)
        self.assertIn("unexpected interruption on our end", result["message"])

    def test_preferences_schema_defaults_and_personalization(self):
        from students.schemas import (
            StudentPreferencesSchema,
            StudentPreferencesUpdateIn,
        )
        prefs = StudentPreferencesSchema()
        self.assertTrue(prefs.notifications.opportunity_alerts)
        self.assertTrue(prefs.notifications.scheme_alerts)
        self.assertTrue(prefs.features.show_affirmative_action_schemes)
        self.assertTrue(prefs.features.show_diversity_job_badges)
        self.assertTrue(prefs.privacy.participate_in_diversity_hiring)

        update_payload = StudentPreferencesUpdateIn(
            notifications={"scheme_alerts": False},
            features={"show_affirmative_action_schemes": False}
        )
        self.assertFalse(update_payload.notifications["scheme_alerts"])
        self.assertFalse(update_payload.features["show_affirmative_action_schemes"])

    def test_multi_domain_government_schemes_schema(self):
        from students.schemas import GovernmentSchemeOutSchema
        from datetime import datetime

        scheme = GovernmentSchemeOutSchema(
            id=1,
            title="AICTE Pragati Scholarship for Girls",
            sponsoring_agency="AICTE / Ministry of Education",
            domain="TECH",
            scheme_type="SCHOLARSHIP",
            target_gender="FEMALE_ONLY",
            benefit_summary="INR 50,000/year",
            description="Government scholarship for female technical students.",
            eligible_degrees=["B.Tech", "MCA"],
            min_cgpa=6.5,
            application_deadline=datetime(2026, 12, 31),
            official_portal_url="https://scholarships.gov.in",
            status="ACTIVE",
            badge_color="emerald",
            is_eligible=True,
            match_reasons=["Eligible: Female candidate in B.Tech"],
            created_at=datetime(2026, 1, 1)
        )
        self.assertEqual(scheme.domain, "TECH")
        self.assertTrue(scheme.is_eligible)
        self.assertEqual(scheme.badge_color, "emerald")

    def test_dei_job_discovery_schema(self):
        from students.schemas import JobDiscoveryItemOut
        from datetime import datetime

        item = JobDiscoveryItemOut(
            id=101,
            title="Cloud & AI Diversity Associate",
            company_id=1,
            company_name="Microsoft India",
            role_type="FULL_TIME",
            location="Bengaluru",
            is_remote=True,
            stipend_or_ctc="18 - 24 LPA",
            open_positions=5,
            required_skills=["azure", "python"],
            description="Diversity accelerator for women engineers.",
            is_diversity_drive=True,
            target_gender="FEMALE_ONLY",
            dei_initiatives=["TechSaksham Partner", "Executive Mentoring"],
            created_at=datetime(2026, 1, 1)
        )
        self.assertTrue(item.is_diversity_drive)
        self.assertEqual(item.target_gender, "FEMALE_ONLY")
        self.assertEqual(len(item.dei_initiatives), 2)



