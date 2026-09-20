"""
Quiz feature unit and integration tests (Feature Set B).
Tests difficulty validation, question randomization, scoring, and submit flow.
"""

import time
import unittest
from app import create_app
from config import TestingConfig
from database.seed import init_database
from services.quiz_service import (
    validate_difficulty,
    get_all_questions_by_difficulty,
    get_random_quiz_questions
)
from services.scoring_service import calculate_quiz_results


class QuizTestCase(unittest.TestCase):
    """Test quiz business logic and endpoints."""

    def setUp(self):
        # Initialize test database
        init_database(TestingConfig.DATABASE_PATH)
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_validate_difficulty(self):
        """Test difficulty validation logic."""
        allowed = ("easy", "medium", "hard")
        self.assertTrue(validate_difficulty("easy", allowed))
        self.assertTrue(validate_difficulty("Medium", allowed))
        self.assertTrue(validate_difficulty("HARD ", allowed))
        self.assertFalse(validate_difficulty("impossible", allowed))
        self.assertFalse(validate_difficulty("", allowed))
        self.assertFalse(validate_difficulty(None, allowed))

    def test_questions_retrieval_by_difficulty(self):
        """Verify questions from database match the chosen difficulty."""
        for diff in ("easy", "medium", "hard"):
            questions = get_all_questions_by_difficulty(diff, TestingConfig.DATABASE_PATH)
            self.assertGreaterEqual(len(questions), 10, f"Expected at least 10 questions for {diff}")
            for q in questions:
                self.assertEqual(q["difficulty"].lower(), diff)

    def test_random_question_selection_no_duplicates(self):
        """Verify random question selection is non-repeating."""
        count = 5
        questions = get_random_quiz_questions("easy", count=count, db_path=TestingConfig.DATABASE_PATH)
        self.assertEqual(len(questions), count)

        # Ensure all selected question IDs are unique
        q_ids = [q["id"] for q in questions]
        self.assertEqual(len(q_ids), len(set(q_ids)), "Questions must not contain duplicate IDs")

        # Verify options are shuffled and valid
        for q in questions:
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["correct_answer"], q["options"])

    def test_scoring_service_calculation(self):
        """Test scoring calculations: correct (+1), incorrect (0), unanswered (0)."""
        sample_questions = [
            {"id": 1, "question_text": "Q1", "correct_answer": "Python", "category": "General"},
            {"id": 2, "question_text": "Q2", "correct_answer": "def", "category": "General"},
            {"id": 3, "question_text": "Q3", "correct_answer": "len()", "category": "General"},
            {"id": 4, "question_text": "Q4", "correct_answer": "list", "category": "General"},
        ]

        # User answered Q1 correctly, Q2 incorrectly, Q3 unanswered, Q4 correctly
        user_answers = {
            "1": "Python",  # Correct (+1)
            "2": "function",  # Incorrect (0)
            # "3" omitted -> Unanswered (0)
            "4": "list"  # Correct (+1)
        }

        result = calculate_quiz_results(
            questions=sample_questions,
            user_answers=user_answers,
            time_taken=25,
            difficulty="easy",
            db_path=TestingConfig.DATABASE_PATH
        )

        self.assertEqual(result["total_questions"], 4)
        self.assertEqual(result["correct_answers"], 2)
        self.assertEqual(result["incorrect_answers"], 1)
        self.assertEqual(result["unanswered"], 1)
        self.assertEqual(result["score"], 2)
        self.assertEqual(result["percentage"], 50.0)
        self.assertEqual(result["time_taken"], 25)
        self.assertEqual(result["feedback"]["tier"], "average")

    def test_scoring_empty_questions_safe(self):
        """Ensure score calculation handles division by zero safely."""
        result = calculate_quiz_results(
            questions=[],
            user_answers={},
            time_taken=0,
            difficulty="easy",
            db_path=TestingConfig.DATABASE_PATH
        )
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_start_quiz_flow(self):
        """Test starting quiz via POST /start-quiz."""
        # Valid difficulty starts quiz and redirects to /quiz
        response = self.client.post("/start-quiz", data={"difficulty": "medium"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/quiz"))

        # Session should contain quiz state
        with self.client.session_transaction() as sess:
            self.assertTrue(sess["quiz_in_progress"])
            self.assertEqual(sess["difficulty"], "medium")
            self.assertEqual(len(sess["question_ids"]), self.app.config["QUIZ_QUESTION_COUNT"])

    def test_start_quiz_invalid_difficulty(self):
        """Test invalid difficulty is rejected and redirects to home."""
        response = self.client.post("/start-quiz", data={"difficulty": "invalid_tier"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please select a valid difficulty level", response.data)

    def test_submit_quiz_flow(self):
        """Test full quiz submit flow and final result view."""
        # 1. Start quiz
        self.client.post("/start-quiz", data={"difficulty": "easy"})

        with self.client.session_transaction() as sess:
            q_ids = sess["question_ids"]

        # 2. Submit form answers
        form_data = {
            f"answer_{q_ids[0]}": "SomeAnswer",
        }
        response = self.client.post("/submit-quiz", data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/result"))

        # 3. View result page
        result_page = self.client.get("/result")
        self.assertEqual(result_page.status_code, 200)
        self.assertIn(b"Quiz Results", result_page.data)
        self.assertIn(b"Detailed Question Review", result_page.data)
        self.assertIn(b"Restart Quiz", result_page.data)


if __name__ == "__main__":
    unittest.main()
