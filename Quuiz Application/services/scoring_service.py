"""
Scoring service module.
Evaluates user answers against database records, calculates score,
computes percentages and statistics, and records results into SQLite.
"""

from typing import List, Dict, Any, Optional
from utils.helpers import get_db_connection, get_performance_feedback


def calculate_quiz_results(
    questions: List[dict],
    user_answers: Dict[str, str],
    time_taken: int,
    difficulty: str,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate full quiz results, generate question review details,
    and save the attempt record to the database.
    
    :param questions: List of question dictionaries from DB (including correct_answer)
    :param user_answers: Dict mapping question ID (as string) to selected answer string
    :param time_taken: Elapsed time in seconds
    :param difficulty: Quiz difficulty string ('easy', 'medium', 'hard')
    :param db_path: Optional path to SQLite DB
    :return: Comprehensive result dictionary
    """
    total_questions = len(questions)
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    review_list = []
    
    for q in questions:
        qid_str = str(q["id"])
        selected_answer = user_answers.get(qid_str)
        
        # Clean answer string if present
        if selected_answer is not None:
            selected_answer = selected_answer.strip()
            if not selected_answer:
                selected_answer = None
                
        correct_answer = q["correct_answer"].strip()
        
        if selected_answer is None:
            unanswered_count += 1
            status = "unanswered"
            is_correct = False
            display_user_ans = "Not Answered"
        elif selected_answer.lower() == correct_answer.lower():
            correct_count += 1
            status = "correct"
            is_correct = True
            display_user_ans = selected_answer
        else:
            incorrect_count += 1
            status = "incorrect"
            is_correct = False
            display_user_ans = selected_answer
            
        review_list.append({
            "id": q["id"],
            "question_text": q["question_text"],
            "category": q.get("category", "General"),
            "user_answer": display_user_ans,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "status": status
        })
        
    score = correct_count * 1
    max_score = total_questions * 1
    
    # Calculate percentage safely
    percentage = round((score / total_questions) * 100, 1) if total_questions > 0 else 0.0
    
    # Get performance feedback tier & message
    feedback = get_performance_feedback(percentage)
    
    # Persist quiz result to SQLite
    record_id = None
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO quiz_results (
                difficulty, total_questions, correct_answers, incorrect_answers,
                unanswered, score, percentage, time_taken
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                difficulty,
                total_questions,
                correct_count,
                incorrect_count,
                unanswered_count,
                score,
                percentage,
                time_taken
            )
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
    except Exception as e:
        # If DB write fails, score calculation still succeeds
        print(f"[WARNING] Could not save quiz result to database: {e}")
        
    return {
        "result_id": record_id,
        "difficulty": difficulty.capitalize(),
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "incorrect_answers": incorrect_count,
        "unanswered": unanswered_count,
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
        "time_taken": time_taken,
        "feedback": feedback,
        "review": review_list
    }
