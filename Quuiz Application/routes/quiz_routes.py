"""
Quiz routes blueprint.
Handles home page, quiz initialization, displaying active quiz,
restarting quiz session, and system health checks.
"""

import time
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash, jsonify
from services.quiz_service import (
    validate_difficulty,
    get_random_quiz_questions,
    get_questions_by_ids
)
from utils.helpers import sanitize_question_for_client

quiz_bp = Blueprint("quiz_bp", __name__)


@quiz_bp.route("/", methods=["GET"])
def index():
    """Render the landing / home page with difficulty selection and quiz instructions."""
    # Check if a quiz is already in progress and inform the user
    in_progress = session.get("quiz_in_progress", False)
    return render_template(
        "index.html",
        quiz_in_progress=in_progress,
        question_count=current_app.config.get("QUIZ_QUESTION_COUNT", 10),
        time_limit=current_app.config.get("QUIZ_TIME_LIMIT", 60)
    )


@quiz_bp.route("/start-quiz", methods=["POST"])
def start_quiz():
    """
    Validate difficulty, query database for random questions,
    initialize the session state, and redirect to the quiz view.
    """
    difficulty = request.form.get("difficulty", "").strip().lower()
    allowed = current_app.config.get("ALLOWED_DIFFICULTIES", ("easy", "medium", "hard"))
    
    # 1. Validate difficulty
    if not validate_difficulty(difficulty, allowed):
        flash("Please select a valid difficulty level (Easy, Medium, or Hard) to start.", "warning")
        return redirect(url_for("quiz_bp.index"))
        
    question_count = current_app.config.get("QUIZ_QUESTION_COUNT", 10)
    time_limit = current_app.config.get("QUIZ_TIME_LIMIT", 60)
    
    # 2. Fetch random questions from database
    questions = get_random_quiz_questions(difficulty, count=question_count)
    
    if not questions or len(questions) == 0:
        flash(f"No questions are currently available for '{difficulty.capitalize()}' difficulty. Please run the database seed script.", "danger")
        return redirect(url_for("quiz_bp.index"))
        
    # 3. Setup session data (store start timestamp for tamper-resistant timer)
    session.clear()
    session["difficulty"] = difficulty
    session["question_ids"] = [q["id"] for q in questions]
    # Store shuffled options mapping per question id for consistent display
    session["shuffled_options"] = {str(q["id"]): q["options"] for q in questions}
    session["quiz_start_time"] = time.time()
    session["time_limit"] = time_limit
    session["quiz_in_progress"] = True
    
    return redirect(url_for("quiz_bp.quiz"))


@quiz_bp.route("/quiz", methods=["GET"])
def quiz():
    """
    Render active quiz interface with one-at-a-time or stepped navigation,
    timer display, and question cards.
    """
    # Verify active quiz session
    if not session.get("quiz_in_progress") or not session.get("question_ids"):
        flash("No active quiz session found. Please choose a difficulty to start a new quiz.", "info")
        return redirect(url_for("quiz_bp.index"))
        
    start_time = session.get("quiz_start_time", time.time())
    time_limit = session.get("time_limit", current_app.config.get("QUIZ_TIME_LIMIT", 60))
    elapsed = time.time() - start_time
    remaining_time = max(0, int(time_limit - elapsed))
    
    # Retrieve questions by stored session IDs
    question_ids = session.get("question_ids", [])
    raw_questions = get_questions_by_ids(question_ids)
    
    # Restore randomized options and sanitize to avoid leaking answers
    shuffled_options = session.get("shuffled_options", {})
    client_questions = []
    
    for q in raw_questions:
        q_safe = sanitize_question_for_client(q)
        qid_str = str(q["id"])
        # Use session-saved randomized options if available, otherwise original options
        if qid_str in shuffled_options:
            q_safe["options"] = shuffled_options[qid_str]
        else:
            q_safe["options"] = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
        client_questions.append(q_safe)
        
    difficulty = session.get("difficulty", "medium").capitalize()
    
    return render_template(
        "quiz.html",
        questions=client_questions,
        total_questions=len(client_questions),
        difficulty=difficulty,
        time_limit=time_limit,
        remaining_time=remaining_time
    )


@quiz_bp.route("/restart", methods=["GET"])
def restart():
    """Clear current quiz session and return to home page for a fresh attempt."""
    session.clear()
    flash("Quiz reset. Select your difficulty to begin a new attempt.", "info")
    return redirect(url_for("quiz_bp.index"))


@quiz_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint returning application status."""
    return jsonify({"status": "ok", "app": "Python Quiz Application Feature Set B"}), 200
