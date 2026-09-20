"""
Database initialization and seeding script.
Creates database tables and inserts 48 questions (16 per difficulty level).
Can be run standalone: python database/seed.py
"""

import os
import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "quiz.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Sample Questions (Feature Set B)
# Tuple structure: (question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty, category)
SEED_QUESTIONS = [
    # ==================== EASY QUESTIONS (16) ====================
    (
        "Which language is used to create a Flask web backend?",
        "Python", "Java", "C++", "PHP",
        "Python",
        "easy", "Programming"
    ),
    (
        "What is the correct file extension for Python source files?",
        ".pyt", ".pt", ".py", ".python",
        ".py",
        "easy", "Programming"
    ),
    (
        "Which keyword is used to define a function in Python?",
        "function", "def", "fun", "define",
        "def",
        "easy", "Programming"
    ),
    (
        "What data type is the result of expression 3 + 2.5 in Python?",
        "int", "float", "complex", "str",
        "float",
        "easy", "Programming"
    ),
    (
        "Which character is used to start single-line comments in Python?",
        "//", "/*", "#", "--",
        "#",
        "easy", "Programming"
    ),
    (
        "Which built-in function returns the number of items in a list?",
        "count()", "size()", "length()", "len()",
        "len()",
        "easy", "Programming"
    ),
    (
        "What will type([1, 2, 3]) return in Python?",
        "<class 'tuple'>", "<class 'list'>", "<class 'set'>", "<class 'array'>",
        "<class 'list'>",
        "easy", "Programming"
    ),
    (
        "Which SQL keyword is used to retrieve data from a database table?",
        "SELECT", "GET", "FETCH", "EXTRACT",
        "SELECT",
        "easy", "Database"
    ),
    (
        "Which HTTP method is typically used to request data from a web server?",
        "POST", "GET", "PUT", "DELETE",
        "GET",
        "easy", "Web Development"
    ),
    (
        "In HTML, which tag is used to create an unordered bullet list?",
        "<ol>", "<li>", "<ul>", "<list>",
        "<ul>",
        "easy", "Web Development"
    ),
    (
        "Which Python statement is used to exit a loop immediately?",
        "stop", "exit", "pass", "break",
        "break",
        "easy", "Programming"
    ),
    (
        "What is the boolean evaluation of an empty list [] in Python?",
        "True", "False", "None", "Error",
        "False",
        "easy", "Programming"
    ),
    (
        "Which operator is used to compare equality of two values in Python?",
        "=", "==", "===", "equals",
        "==",
        "easy", "Programming"
    ),
    (
        "What does CSS stand for in web development?",
        "Computer Style Sheets", "Creative Style System", "Cascading Style Sheets", "Colorful Style Sheets",
        "Cascading Style Sheets",
        "easy", "Web Development"
    ),
    (
        "Which built-in Python data structure stores unordered key-value pairs?",
        "List", "Dictionary", "Tuple", "Set",
        "Dictionary",
        "easy", "Programming"
    ),
    (
        "Which keyword is used to import external modules in Python?",
        "include", "require", "import", "using",
        "import",
        "easy", "Programming"
    ),

    # ==================== MEDIUM QUESTIONS (16) ====================
    (
        "What is the primary purpose of Flask's render_template function?",
        "To compile Python to C", "To render Jinja2 HTML templates", "To execute SQL queries", "To create session cookies",
        "To render Jinja2 HTML templates",
        "medium", "Web Development"
    ),
    (
        "Which of the following built-in Python data structures is immutable?",
        "List", "Dictionary", "Tuple", "Set",
        "Tuple",
        "medium", "Programming"
    ),
    (
        "What will list(range(2, 8, 2)) evaluate to in Python?",
        "[2, 4, 6, 8]", "[2, 4, 6]", "[2, 3, 4, 5, 6, 7]", "[4, 6, 8]",
        "[2, 4, 6]",
        "medium", "Programming"
    ),
    (
        "In SQLite, which constraint ensures all values in a specific column are distinct?",
        "NOT NULL", "CHECK", "UNIQUE", "DEFAULT",
        "UNIQUE",
        "medium", "Database"
    ),
    (
        "Which HTTP status code represents an 'Internal Server Error'?",
        "404", "403", "500", "502",
        "500",
        "medium", "Web Development"
    ),
    (
        "What does the Python zip() function do when passed two lists?",
        "Concatenates them into one", "Pairs corresponding elements as tuples", "Calculates intersection", "Compresses file size",
        "Pairs corresponding elements as tuples",
        "medium", "Programming"
    ),
    (
        "How is client session data stored by default in standard Flask applications?",
        "In a local SQLite database", "Cryptographically signed browser cookies", "In server RAM memory", "In Redis cache",
        "Cryptographically signed browser cookies",
        "medium", "Web Development"
    ),
    (
        "What does {'a': 1, 'b': 2}.get('c', 0) return in Python?",
        "None", "KeyError exception", "0", "False",
        "0",
        "medium", "Programming"
    ),
    (
        "Which SQL clause is used to filter records after an aggregate GROUP BY operation?",
        "WHERE", "HAVING", "FILTER", "ORDER BY",
        "HAVING",
        "medium", "Database"
    ),
    (
        "Which Python block is always executed regardless of whether an exception occurred?",
        "try", "except", "else", "finally",
        "finally",
        "medium", "Programming"
    ),
    (
        "What is the average time complexity of key lookup in a Python dictionary?",
        "O(n)", "O(log n)", "O(1)", "O(n^2)",
        "O(1)",
        "medium", "Data Structures"
    ),
    (
        "Which Flask decorator is used to associate a view function with a specific URL route?",
        "@app.route()", "@app.url()", "@app.endpoint()", "@app.view()",
        "@app.route()",
        "medium", "Web Development"
    ),
    (
        "What is the output of list(map(lambda x: x**2, [1, 2, 3])) in Python?",
        "[1, 4, 9]", "[2, 4, 6]", "[1, 2, 3]", "[1, 8, 27]",
        "[1, 4, 9]",
        "medium", "Programming"
    ),
    (
        "What is the default port used when running a local Flask development server?",
        "80", "8080", "5000", "3000",
        "5000",
        "medium", "Web Development"
    ),
    (
        "In SQLite, which SQL command removes all rows from a table without deleting the table structure?",
        "DROP TABLE", "DELETE FROM table_name", "TRUNCATE SCHEMA", "REMOVE ALL",
        "DELETE FROM table_name",
        "medium", "Database"
    ),
    (
        "Which HTTP status code signifies that a resource was successfully created on the server?",
        "200 OK", "201 Created", "204 No Content", "301 Moved",
        "201 Created",
        "medium", "Web Development"
    ),

    # ==================== HARD QUESTIONS (16) ====================
    (
        "In Python multiple inheritance, which algorithm determines the Method Resolution Order (MRO)?",
        "Depth-First Search", "Breadth-First Search", "C3 Linearization", "Dijkstra Algorithm",
        "C3 Linearization",
        "hard", "Programming"
    ),
    (
        "What does isinstance(True, int) evaluate to in Python?",
        "True", "False", "TypeError", "ValueError",
        "True",
        "hard", "Programming"
    ),
    (
        "What is the consequence of defining def func(item, container=[]) in Python?",
        "A new list is created every call", "The same list persists across calls", "A syntax error is raised", "The list becomes read-only",
        "The same list persists across calls",
        "hard", "Programming"
    ),
    (
        "Which Flask context variable is used to store request-scoped data accessible throughout the request?",
        "session", "g", "request.context", "flask.cache",
        "g",
        "hard", "Web Development"
    ),
    (
        "In SQLite, which command must be executed per connection to enforce foreign key constraints?",
        "SET FOREIGN_KEYS = 1", "PRAGMA foreign_keys = ON;", "ALTER TABLE ENFORCE KEYS", "ENABLE CONSTRAINT",
        "PRAGMA foreign_keys = ON;",
        "hard", "Database"
    ),
    (
        "What is the primary benefit of declaring __slots__ in a Python class?",
        "Enables operator overloading", "Reduces memory overhead by eliminating __dict__", "Prevents class inheritance", "Enforces static type checking",
        "Reduces memory overhead by eliminating __dict__",
        "hard", "Programming"
    ),
    (
        "Which WSGI production HTTP server is standard for deploying Flask applications on Unix systems?",
        "Gunicorn", "Node.js", "Kestrel", "Webpack",
        "Gunicorn",
        "hard", "Web Development"
    ),
    (
        "Why is @functools.wraps commonly applied when writing custom Python decorators?",
        "To speed up execution", "To preserve function name, docstring, and metadata", "To enforce type annotations", "To catch unhandled exceptions",
        "To preserve function name, docstring, and metadata",
        "hard", "Programming"
    ),
    (
        "Which ACID transaction isolation level prevents dirty reads, non-repeatable reads, and phantom reads?",
        "Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable",
        "Serializable",
        "hard", "Database"
    ),
    (
        "What does the expression (x for x in range(5)) construct in Python?",
        "A list comprehension", "A generator expression", "A tuple generator", "A set comprehension",
        "A generator expression",
        "hard", "Programming"
    ),
    (
        "What architectural pattern does Flask's Blueprint feature implement?",
        "Microservices Architecture", "Modular Application / Factory Pattern", "Active Record Pattern", "Observer Pattern",
        "Modular Application / Factory Pattern",
        "hard", "Web Development"
    ),
    (
        "What does CPython's Global Interpreter Lock (GIL) primarily enforce?",
        "Single-threaded OS processes", "Only one thread executes Python bytecode at a time", "Database write locking", "Garbage collection freeze",
        "Only one thread executes Python bytecode at a time",
        "hard", "Computer Science"
    ),
    (
        "In SQLite, which specialized index structure provides optimal performance for multi-dimensional spatial queries?",
        "B-Tree", "Hash Index", "R-Tree", "Inverted Index",
        "R-Tree",
        "hard", "Database"
    ),
    (
        "What will sorted([10, 5, 20, 15], key=lambda x: -x) return in Python?",
        "[5, 10, 15, 20]", "[20, 15, 10, 5]", "[-20, -15, -10, -5]", "TypeError",
        "[20, 15, 10, 5]",
        "hard", "Programming"
    ),
    (
        "Which HTTP header directive helps mitigate Cross-Site Request Forgery (CSRF) in modern browsers?",
        "Content-Security-Policy", "X-Frame-Options", "SameSite attribute in Set-Cookie", "Access-Control-Allow-Origin",
        "SameSite attribute in Set-Cookie",
        "hard", "Web Development"
    ),
    (
        "What does Python's sys.intern() do for strings?",
        "Translates strings into bytecode", "Ensures identical strings share the exact same memory address", "Encrypts strings using SHA-256", "Converts Unicode to ASCII",
        "Ensures identical strings share the exact same memory address",
        "hard", "Computer Science"
    ),
]


def init_database(db_path=DB_PATH):
    """Create tables using schema.sql and seed questions."""
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 1. Execute schema.sql
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    
    # 2. Check existing count
    cursor.execute("SELECT COUNT(*) FROM questions")
    existing_count = cursor.fetchone()[0]
    
    if existing_count == 0:
        cursor.executemany(
            """
            INSERT INTO questions (
                question_text, option_a, option_b, option_c, option_d,
                correct_answer, difficulty, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            SEED_QUESTIONS
        )
        conn.commit()
        print(f"[SUCCESS] Database initialized and seeded with {len(SEED_QUESTIONS)} questions.")
    else:
        print(f"[INFO] Database already contains {existing_count} questions. Skipping seed.")
        
    # Count per difficulty
    for diff in ("easy", "medium", "hard"):
        cursor.execute("SELECT COUNT(*) FROM questions WHERE difficulty = ?", (diff,))
        count = cursor.fetchone()[0]
        print(f"  - Difficulty '{diff.capitalize()}': {count} questions")
        
    conn.close()


if __name__ == "__main__":
    init_database()
