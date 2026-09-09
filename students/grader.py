import os
import json
import requests
import math

class ResilientGrader:
    """
    Grades student screening tests using local memory for MCQs
    and Gemini Cloud APIs with strict rubrics for open-ended Vivas.
    """

    @staticmethod
    def evaluate_test_submission(submitted_answers: list, original_questions: list, resume_rating: float) -> dict:
        """
        Grades the test submission using questions retrieved directly from the database.
        No base64 decoding or character-set corruption risks!
        """
        total_mcq_score = 0
        mcq_count = 0
        viva_score_sum = 0
        viva_count = 0
        
        detailed_feedback = []

        for q in original_questions:
            q_id = q["id"]
            sub_ans = next((item for item in submitted_answers if item["id"] == q_id), None)
            student_answer_text = sub_ans["answer_text"].strip() if sub_ans else ""

            if q["type"] == "MCQ":
                mcq_count += 1
                is_correct = (student_answer_text.lower().strip() == q["correct_answer"].lower().strip())
                score = 100 if is_correct else 0
                total_mcq_score += score
                
                detailed_feedback.append({
                    "id": q_id,
                    "question_text": q["question_text"],
                    "type": "MCQ",
                    "student_answer": student_answer_text,
                    "score": score,
                    "feedback": f"Correct answer: {q['correct_answer']}. {q['explanation']}"
                })

            elif q["type"] == "VIVA":
                viva_count += 1
                viva_score, evaluation_feedback = ResilientGrader._grade_viva_via_gemini(
                    question=q["question_text"],
                    student_answer=student_answer_text,
                    rubric=q["explanation"]
                )
                viva_score_sum += viva_score
                
                detailed_feedback.append({
                    "id": q_id,
                    "question_text": q["question_text"],
                    "type": "VIVA",
                    "student_answer": student_answer_text,
                    "score": viva_score,
                    "feedback": evaluation_feedback
                })

        final_mcq_avg = total_mcq_score / mcq_count if mcq_count > 0 else 0
        final_viva_avg = viva_score_sum / viva_count if viva_count > 0 else 0
        
        cognitive_score = (0.4 * final_mcq_avg) + (0.6 * final_viva_avg)

        # Apply Capped Root Confidence Score (CS) Formula
        gap = max(0, resume_rating - cognitive_score)
        penalty_coefficient = 0.4
        penalty = penalty_coefficient * math.sqrt(gap / 100.0)
        confidence_score = int(cognitive_score * (1 - penalty))

        return {
            "cognitive_score": int(cognitive_score),
            "mcq_average": int(final_mcq_avg),
            "viva_average": int(final_viva_avg),
            "confidence_score": min(max(0, confidence_score), 100),
            "feedback_log": detailed_feedback
        }

    @staticmethod
    def _grade_viva_via_gemini(question: str, student_answer: str, rubric: str) -> tuple:
        if not student_answer:
            return 0, "No answer submitted."

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        system_prompt = (
            "You are a strict and objective technical examiner. Grade the candidate's answer to the "
            "viva question based on the provided expert grading rubric. "
            "You must score the answer strictly on a scale of 0 to 100.\n\n"
            "Use these explicit rubric anchors:\n"
            "- Score 90-100: Excellent answer. Mentions core concepts, specific tools/architectures, and real engineering trade-offs.\n"
            "- Score 50-80: Acceptable answer. Understands the basic concepts but lacks implementation metrics or deep details.\n"
            "- Score 10-40: Weak answer. Vague, superficial mentions of keywords with no real technical comprehension.\n"
            "- Score 0: Irrelevant, empty, or plagiarized answer.\n\n"
            "You must return ONLY a structured JSON object matching this exact schema:\n"
            "{\n  \"score\": 85,\n  \"feedback\": \"Detailed, objective 2-sentence feedback explaining why this score was awarded.\"\n}"
        )

        user_content = f"Question: {question}\nCandidate Answer: {student_answer}\nGrading Rubric Anchor: {rubric}"

        response_schema = {
            "type": "OBJECT",
            "properties": {
                "score": {"type": "INTEGER"},
                "feedback": {"type": "STRING"}
            },
            "required": ["score", "feedback"]
        }

        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nCandidate Submission:\n{user_content}"}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
                "temperature": 0.1
            }
        }

        # Model Pool for Round-Robin Grading
        pool = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
        
        try:
            # Try Model 1
            url1 = f"https://generativelanguage.googleapis.com/v1beta/models/{pool[0]}:generateContent?key={api_key}"
            response = requests.post(url1, json=payload, timeout=15)
            
            # Fallback to Model 2 on rate limit
            if response.status_code == 429:
                url2 = f"https://generativelanguage.googleapis.com/v1beta/models/{pool[1]}:generateContent?key={api_key}"
                response = requests.post(url2, json=payload, timeout=15)
                
            response.raise_for_status()
            
            result_json = response.json()
            text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
            content = json.loads(text_response, strict=False)
            
            return int(content["score"]), content["feedback"]
        except Exception as e:
            return 50, f"Automatic grading service temporarily timed out. Fallback default applied: {str(e)}"
