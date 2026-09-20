import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "bca-college-quiz-app-secret-key-2026")
    
    # Path to SQLite database
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        str(BASE_DIR / "database" / "quiz.db")
    )
    
    # Quiz Settings (Feature Set B)
    QUIZ_QUESTION_COUNT = int(os.environ.get("QUIZ_QUESTION_COUNT", 10))
    QUIZ_TIME_LIMIT = int(os.environ.get("QUIZ_TIME_LIMIT", 60))  # seconds
    TIME_GRACE_PERIOD = int(os.environ.get("TIME_GRACE_PERIOD", 5))  # network latency grace in seconds
    
    # Allowed difficulty levels
    ALLOWED_DIFFICULTIES = ("easy", "medium", "hard")
    
    # Scoring rules
    MARKS_CORRECT = 1
    MARKS_INCORRECT = 0
    MARKS_UNANSWERED = 0


class TestingConfig(Config):
    """Configuration for automated test suite."""
    TESTING = True
    DATABASE_PATH = str(BASE_DIR / "database" / "test_quiz.db")
    QUIZ_QUESTION_COUNT = 5
    QUIZ_TIME_LIMIT = 10
    TIME_GRACE_PERIOD = 2
