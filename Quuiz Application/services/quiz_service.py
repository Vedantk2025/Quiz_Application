"""
Quiz service module.
Handles fetching questions from SQLite, validating difficulty,
selecting non-repeating random questions, and option randomization.
"""

import random
from typing import List, Dict, Optional
from utils.helpers import get_db_connection


def validate_difficulty(difficulty: str, allowed: tuple) -> bool:
    """Check if provided difficulty string is valid."""
    if not difficulty or not isinstance(difficulty, str):
        return False
    return difficulty.strip().lower() in allowed


def get_all_questions_by_difficulty(difficulty: str, db_path: Optional[str] = None) -> List[dict]:
    """Retrieve all questions for a given difficulty level from SQLite."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, question_text, option_a, option_b, option_c, option_d,
               correct_answer, difficulty, category
        FROM questions
        WHERE LOWER(difficulty) = LOWER(?)
        """,
        (difficulty,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_random_quiz_questions(difficulty: str, count: int = 10, db_path: Optional[str] = None) -> List[dict]:
    """
    Select `count` random, non-repeating questions for the given difficulty.
    Randomizes both question order and answer options.
    Returns list of question dictionaries (with correct_answer intact for backend use).
    """
    questions = get_all_questions_by_difficulty(difficulty, db_path)
    
    if not questions:
        return []
    
    # Pick min(count, available) random unique questions
    selected_count = min(count, len(questions))
    selected_questions = random.sample(questions, selected_count)
    
    # Shuffle question sequence so order is randomized
    random.shuffle(selected_questions)
    
    # Format each question with randomized options list
    formatted_questions = []
    for q in selected_questions:
        options = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
        random.shuffle(options)  # Randomize option order
        
        q_copy = dict(q)
        q_copy["options"] = options
        formatted_questions.append(q_copy)
        
    return formatted_questions


def get_questions_by_ids(question_ids: List[int], db_path: Optional[str] = None) -> List[dict]:
    """
    Retrieve questions matching a list of question IDs, maintaining the original order
    specified in question_ids.
    """
    if not question_ids:
        return []
        
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    placeholders = ",".join("?" for _ in question_ids)
    query = f"""
        SELECT id, question_text, option_a, option_b, option_c, option_d,
               correct_answer, difficulty, category
        FROM questions
        WHERE id IN ({placeholders})
    """
    cursor.execute(query, question_ids)
    rows = cursor.fetchall()
    conn.close()
    
    # Map by ID so we can preserve session order
    row_map = {row["id"]: dict(row) for row in rows}
    
    ordered_questions = []
    for qid in question_ids:
        if qid in row_map:
            ordered_questions.append(row_map[qid])
            
    return ordered_questions
