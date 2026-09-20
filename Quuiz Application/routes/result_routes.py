"""
Result routes blueprint.
Handles submitting answers, backend score calculation,
preventing duplicate submissions, and rendering the final result page.
"""

import time
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from services.quiz_service import get_questions_by_ids
from services.scoring_service import calculate_quiz_results

result_bp = Blueprint("result_bp", __name__)


@result_bp.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    """
    Receive submitted answers from the quiz form, validate elapsed time,
    calculate score securely on the backend, persist result, and redirect.
    """
    # 1. Prevent duplicate submission if result is already in session
    if not session.get("quiz_in_progress") and session.get("quiz_result"):
        return redirect(url_for("result_bp.view_result"))
        
    question_ids = session.get("question_ids")
    if not question_ids:
        flash("Quiz session expired or not started. Please begin a new quiz.", "warning")
        return redirect(url_for("quiz_bp.index"))
        
    # 2. Server-side time validation
    start_time = session.get("quiz_start_time", time.time())
    time_limit = session.get("time_limit", current_app.config.get("QUIZ_TIME_LIMIT", 60))
    grace_period = current_app.config.get("TIME_GRACE_PERIOD", 5)
    
    elapsed_time = int(time.time() - start_time)
    
    # 3. Extract submitted answers
    # The form submits inputs named 'answer_<question_id>'
    user_answers = {}
    for key, val in request.form.items():
        if key.startswith("answer_"):
            qid_str = key.replace("answer_", "", 1)
            user_answers[qid_str] = val
            
    # Cap recorded time taken to time_limit
    recorded_time = min(max(1, elapsed_time), time_limit)
    
    # 4. Fetch authoritative question details from database
    questions = get_questions_by_ids(question_ids)
    difficulty = session.get("difficulty", "medium")
    
    # 5. Compute full scoring and question-by-question review
    results = calculate_quiz_results(
        questions=questions,
        user_answers=user_answers,
        time_taken=recorded_time,
        difficulty=difficulty
    )
    
    # 6. Save results to session & mark quiz as finished
    session["quiz_in_progress"] = False
    session["quiz_result"] = results
    
    return redirect(url_for("result_bp.view_result"))


@result_bp.route("/result", methods=["GET"])
def view_result():
    """Display the final score, breakdown, performance message, and review."""
    results = session.get("quiz_result")
    
    if not results:
        flash("No recent quiz result found. Please start a quiz first.", "info")
        return redirect(url_for("quiz_bp.index"))
        
    return render_template("result.html", result=results)
