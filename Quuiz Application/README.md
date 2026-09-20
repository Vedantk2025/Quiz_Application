# Quiz Application — Feature Set B

A complete, responsive, and secure web-based **Quiz Application** built with **Python**, **Flask**, and **SQLite**. Developed as a BCA 3rd-semester college assignment demonstrating core Python programming, web routing, server-side session management, relational database integration, and clean frontend design.

---

## 🌟 Features (Feature Set B)

The application implements all 5 required features:

1. **Difficulty Selection**
   - Three distinct difficulty tiers: **Easy**, **Medium**, and **Hard**.
   - Difficulty must be selected on the home page before starting the quiz.
   - Questions are queried dynamically from the SQLite database according to the selected tier.

2. **Random Non-Repeating Questions**
   - Questions are randomly selected from SQLite using Python's `random.sample()` algorithm.
   - Zero question repetition within any single quiz attempt.
   - Configurable question count (default: **10 questions** per attempt).
   - Randomizes question sequence and answer option placement.
   - Every new quiz attempt receives a unique question set or ordering.

3. **Anti-Tamper Visible Countdown Timer**
   - Visible countdown timer on the quiz screen (default: **60 seconds** for 10 questions).
   - Configurable via `config.py` (`QUIZ_TIME_LIMIT`).
   - Counts down smoothly every second; alerts with warning color (< 15s) and pulsing red (< 5s).
   - **Server-Side Security**: The backend records the quiz start timestamp (`time.time()`) in the encrypted Flask session. Refreshing or manipulating the client browser does **not** reset or grant extra time.
   - Automatically submits the quiz when time expires.

4. **Robust Backend Score Calculation**
   - **Scoring Rules**:
     - Correct Answer: **+1 mark**
     - Incorrect Answer: **0 marks**
     - Unanswered Question: **0 marks**
   - Displays: Total Questions, Correct Answers, Incorrect Answers, Unanswered Questions, Score, and Percentage.
   - All scoring and comparisons are performed securely on the Python backend; never trusted from JavaScript.

5. **Final Result & Detailed Review**
   - Comprehensive score card showing final score, maximum score, percentage, and time taken.
   - Encouraging performance feedback tier:
     - **80% – 100%**: *Excellent performance!*
     - **60% – 79%**: *Good performance!*
     - **40% – 59%**: *Keep practicing!*
     - **0% – 39%**: *Keep learning and try again!*
   - Question-by-Question review section displaying:
     - Question text
     - User's selected answer
     - Correct answer
     - Status badges (✓ Correct, ✗ Incorrect, ⊘ Unanswered)
   - **Restart Quiz** and **Back to Home** buttons.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12+, Flask 3.1+
- **Database**: SQLite 3 (using Python's built-in `sqlite3` module)
- **Frontend**: HTML5, Vanilla CSS3 (custom responsive glassmorphism theme), Vanilla JavaScript (ES6)
- **Templating**: Jinja2
- **Testing**: Python standard library `unittest`

---

## 📁 Project Structure

```
d:/Quuiz Application/
├── app.py                     # Main Flask entry point and application factory
├── config.py                  # App configuration, quiz settings, and timeouts
├── requirements.txt           # Minimal Python dependencies (Flask)
├── .env.example               # Environment variables template
├── .gitignore                 # Files and folders to ignore in Git
├── README.md                  # Complete project documentation & viva guide
│
├── database/
│   ├── schema.sql             # SQL DDL for questions and quiz_results tables
│   ├── seed.py                # Standalone DB seeder with 48 sample questions
│   └── quiz.db                # SQLite database file
│
├── routes/
│   ├── __init__.py
│   ├── quiz_routes.py         # Routes: /, /start-quiz, /quiz, /restart, /health
│   └── result_routes.py       # Routes: /submit-quiz, /result
│
├── services/
│   ├── __init__.py
│   ├── quiz_service.py        # Question retrieval, random sampling & option shuffling
│   └── scoring_service.py     # Answer evaluation, scoring & result persistence
│
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Database connector & performance tier calculations
│
├── templates/
│   ├── base.html              # Base Jinja2 layout (header, footer, meta)
│   ├── index.html             # Home page with difficulty selector cards
│   ├── quiz.html              # Question carousel, countdown timer & progress
│   ├── result.html            # Final score card, stats grid & question review
│   └── error.html             # Friendly error pages (400, 404, 500)
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom responsive CSS with dark theme
│   └── js/
│       └── quiz.js            # Client timer, question navigation & submit guard
│
└── tests/
    ├── __init__.py
    ├── test_app.py            # Route status, app initialization & 404 tests
    ├── test_quiz.py           # Business logic, difficulty & scoring tests
    └── verify_workflow.py     # Automated end-to-end testing script
```

---

## 🚀 Getting Started

### 1. Prerequisites
Verify Python 3 is installed on your machine:
```bash
python --version
```
*(Any version Python 3.10, 3.11, 3.12, or 3.13 is supported).*

### 2. Setup Virtual Environment

**On Windows (PowerShell or Command Prompt):**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
Run the seed script to create the SQLite database tables and insert 48 questions (16 per difficulty):
```bash
python database/seed.py
```
*Output confirmation:*
```
[SUCCESS] Database initialized and seeded with 48 questions.
  - Difficulty 'Easy': 16 questions
  - Difficulty 'Medium': 16 questions
  - Difficulty 'Hard': 16 questions
```

### 4. Run Application
Start the Flask development server:
```bash
python app.py
```

### 5. Access in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the complete test suite:
```powershell
.\venv\Scripts\python -m unittest discover -s tests -p "test_*.py" -v
```

Run the end-to-end live workflow verification:
```powershell
.\venv\Scripts\python tests/verify_workflow.py
```
*All 13 unit tests and 8 end-to-end integration tests pass.*

---

## 🎓 College Viva & Practical Exam Explanation Guide

During your viva examination, you can explain the core architecture using these key points:

### 1. How does Flask handle state across requests?
- HTTP is stateless by nature. We use **Flask Sessions** (`from flask import session`) backed by cryptographically signed browser cookies (`SECRET_KEY`).
- When a user starts a quiz (`/start-quiz`), we save `session['question_ids']`, `session['difficulty']`, and `session['quiz_start_time']`.

### 2. How does the Anti-Cheat Timer work?
- While JavaScript updates the visual countdown timer every 1000ms, the server never relies on the client's clock for scoring.
- The server stores `session['quiz_start_time'] = time.time()`.
- Upon submission (`/submit-quiz`), the server calculates `elapsed = time.time() - session['quiz_start_time']`.
- If a user refreshes the page, the server computes `remaining = time_limit - elapsed`. Therefore, refreshing the page does not grant any extra time.

### 3. How does Random Question Selection work?
- In `services/quiz_service.py`, we query questions matching the chosen difficulty from SQLite.
- We use Python's `random.sample(questions, count)` to guarantee $N$ unique questions without replacement.
- We also shuffle the four answer options `[option_a, option_b, option_c, option_d]` so option positions vary per attempt.

### 4. How is the score calculated and validated?
- The client form submits user answers in the format `answer_<question_id> = <selected_option_text>`.
- In `services/scoring_service.py`, the backend fetches the original question records from the SQLite database by ID.
- It iterates through each question, checks whether an answer was provided, and compares it against the authoritative `correct_answer`.
- The user's score is never sent from or calculated in JavaScript, ensuring security.

### 5. Database Schema & SQL Constraints
- SQLite tables are defined in `database/schema.sql`:
  - `questions` table enforces `CHECK(difficulty IN ('easy', 'medium', 'hard'))`.
  - `quiz_results` table stores the history of completed quizzes with `CURRENT_TIMESTAMP`.
- Queries use parameterized SQL (`cursor.execute(..., (val,))`) to prevent SQL Injection vulnerabilities.

---

## 📄 License
Created for academic assignment purposes. Free to use and extend.
