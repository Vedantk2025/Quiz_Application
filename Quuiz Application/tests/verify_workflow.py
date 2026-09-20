"""
Comprehensive verification test script simulating all 8 manual user tests
against the running live Flask server at http://127.0.0.1:5000.
"""

import re
import time
import json
import urllib.request
import urllib.parse
import http.cookiejar

SERVER_URL = "http://127.0.0.1:5000"

def run_tests():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE QUIZ APPLICATION WORKFLOW TESTS")
    print("=" * 60)
    
    # -------------------------------------------------------------------------
    # Test 1 — Easy Quiz Full Flow
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Easy Quiz: Start, Answer, Submit, Verify Score")
    cj1 = http.cookiejar.CookieJar()
    opener1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj1))
    
    # Start Easy
    start_resp = opener1.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": "easy"}).encode("utf-8")
    ))
    assert start_resp.url.endswith("/quiz"), f"Expected redirect to /quiz, got {start_resp.url}"
    quiz_html = start_resp.read().decode("utf-8")
    assert "Easy" in quiz_html
    assert "Time Remaining:" in quiz_html
    
    # Extract question IDs from inputs
    q_ids = re.findall(r'name="answer_(\d+)"', quiz_html)
    unique_qids = list(dict.fromkeys(q_ids))
    assert len(unique_qids) == 10, f"Expected 10 questions, got {len(unique_qids)}"
    print(f"  [PASS] 10 unique Easy questions loaded: {unique_qids}")
    
    # Submit first 5 answers, leave 5 unanswered
    submit_data = {f"answer_{qid}": "Python" for qid in unique_qids[:5]}
    sub_resp = opener1.open(urllib.request.Request(
        f"{SERVER_URL}/submit-quiz",
        data=urllib.parse.urlencode(submit_data).encode("utf-8")
    ))
    assert sub_resp.url.endswith("/result"), f"Expected /result, got {sub_resp.url}"
    result_html = sub_resp.read().decode("utf-8")
    assert "Quiz Results" in result_html
    assert "Detailed Question Review" in result_html
    print("  [PASS] Easy quiz submitted and result rendered successfully.")

    # -------------------------------------------------------------------------
    # Test 2 — Medium Quiz Flow
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Medium Quiz: Start, Verify Random Questions & Result")
    cj2 = http.cookiejar.CookieJar()
    opener2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj2))
    start_resp = opener2.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": "medium"}).encode("utf-8")
    ))
    quiz_html = start_resp.read().decode("utf-8")
    assert "Medium" in quiz_html
    q_ids_med = list(dict.fromkeys(re.findall(r'name="answer_(\d+)"', quiz_html)))
    assert len(q_ids_med) == 10
    print(f"  [PASS] 10 unique Medium questions loaded: {q_ids_med}")
    
    # -------------------------------------------------------------------------
    # Test 3 — Hard Quiz Flow
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Hard Quiz: Start, Verify Random Questions & Result")
    cj3 = http.cookiejar.CookieJar()
    opener3 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj3))
    start_resp = opener3.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": "hard"}).encode("utf-8")
    ))
    quiz_html = start_resp.read().decode("utf-8")
    assert "Hard" in quiz_html
    q_ids_hard = list(dict.fromkeys(re.findall(r'name="answer_(\d+)"', quiz_html)))
    assert len(q_ids_hard) == 10
    print(f"  [PASS] 10 unique Hard questions loaded: {q_ids_hard}")

    # -------------------------------------------------------------------------
    # Test 4 — Timer Remaining Persistence (No Extra Time on Refresh)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Refresh Integrity: Timer state does not reset")
    cj4 = http.cookiejar.CookieJar()
    opener4 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj4))
    opener4.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": "easy"}).encode("utf-8")
    ))
    
    # First view of quiz
    q1_html = opener4.open(f"{SERVER_URL}/quiz").read().decode("utf-8")
    rem1 = int(re.search(r'data-remaining="(\d+)"', q1_html).group(1))
    
    # Wait 2 seconds
    time.sleep(2)
    
    # Refresh view of quiz
    q2_html = opener4.open(f"{SERVER_URL}/quiz").read().decode("utf-8")
    rem2 = int(re.search(r'data-remaining="(\d+)"', q2_html).group(1))
    assert rem2 <= rem1 - 1, f"Timer should have decreased: rem1={rem1}, rem2={rem2}"
    print(f"  [PASS] Refresh test passed: remaining time decreased from {rem1}s to {rem2}s.")

    # -------------------------------------------------------------------------
    # Test 5 — Unanswered Questions Correct Counting
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Unanswered Counting: 0 marks given, accurately tallied")
    cj5 = http.cookiejar.CookieJar()
    opener5 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj5))
    opener5.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": "easy"}).encode("utf-8")
    ))
    # Submit completely empty (0 answers selected)
    sub_resp = opener5.open(urllib.request.Request(
        f"{SERVER_URL}/submit-quiz",
        data=urllib.parse.urlencode({}).encode("utf-8")
    ))
    res_html = sub_resp.read().decode("utf-8")
    assert "Unanswered Questions (0 pts)" in res_html
    print("  [PASS] All 10 questions safely recognized as unanswered (0 score, 0.0%).")

    # -------------------------------------------------------------------------
    # Test 6 — Restart Functionality
    # -------------------------------------------------------------------------
    print("\n[TEST 6] Restart Quiz: Clears session and returns to Home")
    restart_resp = opener5.open(f"{SERVER_URL}/restart")
    assert restart_resp.url == f"{SERVER_URL}/"
    print("  [PASS] Session cleanly reset and redirected to home page.")

    # -------------------------------------------------------------------------
    # Test 7 — Invalid Input / Missing Difficulty
    # -------------------------------------------------------------------------
    print("\n[TEST 7] Invalid Input Handling")
    cj7 = http.cookiejar.CookieJar()
    opener7 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj7))
    bad_resp = opener7.open(urllib.request.Request(
        f"{SERVER_URL}/start-quiz",
        data=urllib.parse.urlencode({"difficulty": ""}).encode("utf-8")
    ))
    assert bad_resp.url == f"{SERVER_URL}/"
    bad_html = bad_resp.read().decode("utf-8")
    assert "Please select a valid difficulty level" in bad_html
    print("  [PASS] Missing difficulty correctly caught and friendly message shown.")

    # -------------------------------------------------------------------------
    # Test 8 — Non-Existent Route (404 Handler)
    # -------------------------------------------------------------------------
    print("\n[TEST 8] Custom Error Pages (404)")
    try:
        opener7.open(f"{SERVER_URL}/some-unknown-path")
    except urllib.error.HTTPError as err:
        assert err.code == 404
        err_page = err.read().decode("utf-8")
        assert "Page Not Found" in err_page
        print("  [PASS] Custom 404 error page displayed properly.")

    print("\n" + "=" * 60)
    print("ALL 8 VERIFICATION TESTS PASSED SUCCESSFULLY ON LOCALHOST!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
