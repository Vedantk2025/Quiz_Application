"""
Helper functions for the Quiz Application.
Provides reusable functions for performance messages, time calculations,
and database connections.
"""

import sqlite3
from flask import current_app


def get_db_connection(db_path=None):
    """
    Establish and return a connection to the SQLite database.
    Sets row_factory to sqlite3.Row for dictionary-like column access.
    """
    if db_path is None:
        db_path = current_app.config.get("DATABASE_PATH")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_performance_feedback(percentage: float) -> dict:
    """
    Return performance rating message and CSS badge class based on percentage.
    Ranges as specified in requirements:
      80–100% -> Excellent performance!
      60–79%  -> Good performance!
      40–59%  -> Keep practicing!
      0–39%   -> Keep learning and try again!
    """
    if percentage >= 80:
        return {
            "tier": "excellent",
            "title": "Excellent Performance!",
            "message": "Outstanding work! You have shown a strong grasp of the subject.",
            "badge_color": "success"
        }
    elif percentage >= 60:
        return {
            "tier": "good",
            "title": "Good Performance!",
            "message": "Well done! Keep practicing to push your score even higher.",
            "badge_color": "info"
        }
    elif percentage >= 40:
        return {
            "tier": "average",
            "title": "Keep Practicing!",
            "message": "Decent attempt! Review the question explanations below to improve.",
            "badge_color": "warning"
        }
    else:
        return {
            "tier": "poor",
            "title": "Keep Learning and Try Again!",
            "message": "Don't be discouraged! Review your mistakes and give it another shot.",
            "badge_color": "danger"
        }


def sanitize_question_for_client(question_row) -> dict:
    """
    Convert sqlite3.Row or dict question to a safe dictionary
    WITHOUT exposing the correct_answer to the frontend template or JavaScript.
    """
    q_dict = dict(question_row)
    # Never expose the correct_answer before the user submits!
    q_dict.pop("correct_answer", None)
    return q_dict
