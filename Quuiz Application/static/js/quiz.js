/**
 * Quiz Application Client Logic (Feature Set B)
 * Handles countdown timer, question switching, answer state preservation,
 * question navigator dots, progress bar, and automatic/manual submission.
 */

document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Elements ---
    const quizForm = document.getElementById("quizForm");
    if (!quizForm) return; // Not on quiz page

    const cards = document.querySelectorAll(".question-card");
    const totalQuestions = cards.length;
    const currentNumEl = document.getElementById("currentQuestionNumber");
    const progressBar = document.getElementById("quizProgressBar");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitQuizBtn");
    const answeredCounter = document.getElementById("answeredCounter");
    const navDots = document.querySelectorAll(".nav-dot");
    
    // Timer Elements
    const timerBadge = document.getElementById("timerBadge");
    const timerCountdown = document.getElementById("timerCountdown");
    
    // Unanswered Modal Elements
    const modal = document.getElementById("unansweredModal");
    const modalCount = document.getElementById("unansweredModalCount");
    const cancelModalBtn = document.getElementById("cancelModalBtn");
    const confirmSubmitBtn = document.getElementById("confirmSubmitBtn");

    let currentIndex = 0;
    let isSubmitting = false;

    // =========================================================================
    // 1. COUNTDOWN TIMER
    // =========================================================================
    let remainingTime = parseInt(timerBadge.getAttribute("data-remaining"), 10) || 60;

    function updateTimerDisplay() {
        timerCountdown.textContent = `${remainingTime}s`;

        // Warning state (< 15s)
        if (remainingTime <= 15 && remainingTime > 5) {
            timerBadge.classList.add("timer-warning");
            timerBadge.classList.remove("timer-critical");
        } else if (remainingTime <= 5) {
            timerBadge.classList.remove("timer-warning");
            timerBadge.classList.add("timer-critical");
        } else {
            timerBadge.classList.remove("timer-warning", "timer-critical");
        }
    }

    updateTimerDisplay();

    const timerInterval = setInterval(() => {
        remainingTime -= 1;
        
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            timerCountdown.textContent = "0s";
            handleAutoSubmit("Time expired! Automatically submitting your quiz...");
        } else {
            updateTimerDisplay();
        }
    }, 1000);

    function handleAutoSubmit(reason) {
        if (isSubmitting) return;
        isSubmitting = true;
        
        // Disable interactive inputs
        document.querySelectorAll("input[type='radio']").forEach(r => r.disabled = true);
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = "Time Up! Submitting...";
        }
        
        // Hide modal if open
        if (modal) modal.style.display = "none";
        
        // Auto-submit the form
        quizForm.submit();
    }

    // =========================================================================
    // 2. QUESTION NAVIGATION & PROGRESS
    // =========================================================================
    function showQuestion(index) {
        if (index < 0 || index >= totalQuestions) return;
        currentIndex = index;

        // Show active card, hide others
        cards.forEach((card, i) => {
            if (i === currentIndex) {
                card.classList.add("active-question");
            } else {
                card.classList.remove("active-question");
            }
        });

        // Update Question Tracker
        if (currentNumEl) currentNumEl.textContent = currentIndex + 1;

        // Update Progress Bar
        if (progressBar) {
            const pct = Math.round(((currentIndex + 1) / totalQuestions) * 100);
            progressBar.style.width = `${pct}%`;
        }

        // Update Nav Dots active state
        navDots.forEach((dot, i) => {
            if (i === currentIndex) {
                dot.classList.add("active");
            } else {
                dot.classList.remove("active");
            }
        });

        // Update Previous / Next Buttons
        if (prevBtn) prevBtn.disabled = (currentIndex === 0);
        
        // On last question, show Submit prominently
        if (nextBtn) {
            if (currentIndex === totalQuestions - 1) {
                nextBtn.style.display = "none";
                submitBtn.style.display = "inline-flex";
            } else {
                nextBtn.style.display = "inline-flex";
                // Keep submit button visible at all times or secondary
                submitBtn.style.display = "inline-flex";
            }
        }
    }

    // Previous & Next click events
    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            if (currentIndex > 0) showQuestion(currentIndex - 1);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            if (currentIndex < totalQuestions - 1) showQuestion(currentIndex + 1);
        });
    }

    // Nav Dots direct jump
    navDots.forEach(dot => {
        dot.addEventListener("click", () => {
            const targetIdx = parseInt(dot.getAttribute("data-index"), 10);
            showQuestion(targetIdx);
        });
    });

    // =========================================================================
    // 3. ANSWER SELECTION & TRACKING
    // =========================================================================
    const radios = document.querySelectorAll(".quiz-radio");

    function updateAnsweredStats() {
        const answeredQids = new Set();
        radios.forEach(radio => {
            if (radio.checked) {
                const qid = radio.getAttribute("data-question-id");
                answeredQids.add(qid);
                const dot = document.getElementById(`navDot-${qid}`);
                if (dot) dot.classList.add("answered");
            }
        });

        const answeredCount = answeredQids.size;
        if (answeredCounter) {
            answeredCounter.textContent = `${answeredCount} of ${totalQuestions} answered`;
        }

        return answeredCount;
    }

    radios.forEach(radio => {
        radio.addEventListener("change", () => {
            updateAnsweredStats();
        });
    });

    // Initial check in case of browser-cached form values
    updateAnsweredStats();
    showQuestion(0);

    // =========================================================================
    // 4. SUBMISSION & UNANSWERED MODAL CONFIRMATION
    // =========================================================================
    quizForm.addEventListener("submit", (e) => {
        if (isSubmitting) return; // Prevent double submit

        const answeredCount = updateAnsweredStats();
        const unansweredCount = totalQuestions - answeredCount;

        // If there are unanswered questions and not confirmed yet, show modal
        if (unansweredCount > 0 && !quizForm.dataset.confirmed) {
            e.preventDefault();
            if (modalCount) modalCount.textContent = unansweredCount;
            if (modal) modal.style.display = "flex";
            return;
        }

        // Mark as submitting
        isSubmitting = true;
        clearInterval(timerInterval);
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = "Submitting Quiz...";
        }
    });

    // Modal actions
    if (cancelModalBtn) {
        cancelModalBtn.addEventListener("click", () => {
            if (modal) modal.style.display = "none";
        });
    }

    if (confirmSubmitBtn) {
        confirmSubmitBtn.addEventListener("click", () => {
            if (modal) modal.style.display = "none";
            quizForm.dataset.confirmed = "true";
            quizForm.requestSubmit ? quizForm.requestSubmit() : quizForm.submit();
        });
    }
});
