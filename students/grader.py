import os
import json
import base64
import requests
import math

class ResilientGrader:
    """
    Grades student screening tests using local memory for MCQs
    and Gemini Cloud APIs with strict rubrics for open-ended Vivas.
    Includes time-wise decay weighting on MCQ answers.
    """

    @staticmethod
    def get_token_questions(session_token: str) -> list:
        """
        Decodes the base64 session token. 
        Note: This is deprecated now that we use secure, database-backed sessions!
        """
        try:
            clean_token = session_token.strip().replace("\n", "").replace("\r", "").strip('"').strip("'")
            padding_needed = len(clean_token) % 4
            if padding_needed:
                clean_token += '=' * (4 - padding_needed)
                
            decoded_bytes = base64.b64decode(clean_token.encode())
            decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
            return json.loads(decoded_text, strict=False).get("questions", [])
        except Exception as e:
            raise ValueError(f"Invalid or corrupted session token. Details: {str(e)}")

    @staticmethod
    def evaluate_test_submission(submitted_answers: list, original_questions: list, resume_rating: float) -> dict:
        """
        Grades the test submission using questions retrieved directly from the database.
        - MCQs: Evaluated instantly in-memory with custom Time-Decay multipliers.
        - Vivas: Evaluated via Gemini API with structured feedback.
        """
        total_mcq_score = 0
        mcq_count = 0
        viva_score_sum = 0
        viva_count = 0
        
        detailed_feedback = []

        for q in original_questions:
            q_id = q["id"]
            # Find the matching submitted answer
            sub_ans = next((item for item in submitted_answers if item["id"] == q_id), None)
            student_answer_text = sub_ans["answer_text"].strip() if sub_ans else ""
            
            # Extract time taken parameter (default to 15 seconds if not provided)
            time_taken = sub_ans.get("time_taken_seconds", 15) if sub_ans else 15

            if q["type"] == "MCQ":
                mcq_count += 1
                is_correct = (student_answer_text.lower().strip() == q["correct_answer"].lower().strip())
                
                if is_correct:
                    # Apply Linear Time-Decay Multiplier
                    if time_taken <= 15:
                        multiplier = 1.0
                    elif time_taken >= 60:
                        multiplier = 0.7
                    else:
                        # Decays linearly from 1.0 down to 0.7 between 15s and 60s
                        multiplier = 1.0 - 0.3 * ((time_taken - 15) / 45)
                    
                    score = int(100 * multiplier)
                    feedback_msg = f"Correct answer! Answered in {time_taken}s (Speed Multiplier: {multiplier:.2f}x)."
                else:
                    score = 0
                    feedback_msg = "Incorrect answer."

                total_mcq_score += score
                
                detailed_feedback.append({
                    "id": q_id,
                    "question_text": q["question_text"],
                    "type": "MCQ",
                    "student_answer": student_answer_text,
                    "score": score,
                    "feedback": f"Correct answer: {q['correct_answer']}. {q['explanation']} | {feedback_msg}"
                })

            elif q["type"] == "VIVA":
                viva_count += 1
                # Trigger Gemini grading engine for open-ended Viva answers
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
        
        # Weighted Cognitive Score: 30% MCQ (with Time-Decay), 70% Viva (Reasoning-focused)
        cognitive_score = (0.3 * final_mcq_avg) + (0.7 * final_viva_avg)

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
        """
        Task 3: Response Grading. Routed strictly to gemini-3.1-flash-lite.
        """
        if not student_answer:
            return 0, "No answer submitted."

        api_key = os.getenv("GEMINI_API_KEY")
        # Read from .env, default to our verified gemini-3.1-flash-lite model
        model = os.getenv("MODEL_GRADER", "gemini-3.1-flash-lite")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in your .env configuration.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        system_prompt = (
            "You are a strict and objective domain-expert examiner. Grade the candidate's answer to the "
            "viva question based on the provided expert grading rubric across their field of study or professional domain. "
            "You must score the answer strictly on a scale of 0 to 100.\n\n"
            "Use these explicit rubric anchors:\n"
            "- Score 90-100: Excellent answer. Mentions core concepts, specific methodologies/tools/metrics, and practical trade-offs.\n"
            "- Score 50-80: Acceptable answer. Understands the basic concepts but lacks specific operational or practical details.\n"
            "- Score 10-40: Weak answer. Vague, superficial mentions of keywords with no real domain comprehension.\n"
            "- Score 0: Irrelevant, empty, or plagiarized answer.\n\n"
            "You must return ONLY a structured JSON object matching this exact schema:\n"
            "{\n"
            "  \"score\": 85,\n"
            "  \"feedback\": \"Detailed, objective 2-sentence feedback explaining why this score was awarded.\"\n"
            "}"
        )

        user_content = (
            f"Question: {question}\n"
            f"Candidate Answer: {student_answer}\n"
            f"Grading Rubric Anchor: {rubric}"
        )

        response_schema = {
            "type": "OBJECT",
            "properties": {
                "score": {"type": "INTEGER"},
                "feedback": {"type": "STRING"}
            },
            "required": ["score", "feedback"]
        }

        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nCandidate Submission:\n{user_content}"}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema,
                "temperature": 0.1
            }
        }

        try:
            # Set timeout to 120 seconds to completely eliminate any free-tier connection drops
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result_json = response.json()
            text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
            content = json.loads(text_response)
            
            return int(content["score"]), content["feedback"]
        except Exception as e:
            return 50, f"Automatic grading service temporarily timed out. Fallback default applied: {str(e)}"
