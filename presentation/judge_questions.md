# EduLift AI — Judge Questions & Honest Answers

This document prepares the team to answer common technical, ethical, and design questions transparently during hackathon judging.

---

### Q1: "Why did you build this with Flask, SQLite, and vanilla HTML/JS instead of React, Next.js, or FastAPI?"
**Honest Answer:**
"As first-year B.Tech AIML students, our priority was building a reliable, explainable, and production-tested application where every layer is understandable. Flask with SQLite allowed us to implement secure server-side sessions, strict role-based access controls, and parameterized queries without unnecessary framework overhead. Vanilla JavaScript and Chart.js ensure fast load times and zero build-step complexity, making the system easy to audit and deploy in educational environments."

---

### Q2: "Is your machine learning model trained on real student records?"
**Honest Answer:**
"No. Our demonstration model is trained on 500 synthetic records generated with Python and numpy using a fixed seed (`seed=42`). Using real student records without Institutional Review Board (IRB) approval, student consent, and strict privacy clearances would be unethical. We explicitly display an advisory banner in the dashboard stating that predictions are synthetic demonstrations and must never be used for high-stakes or disciplinary decisions."

---

### Q3: "What algorithm is used for the ML demonstration, and how does it perform against a baseline?"
**Honest Answer:**
"We used scikit-learn's `LogisticRegression` with feature standardization (`StandardScaler`). We split the dataset 80/20 into training and testing sets.
* Baseline Model (Dummy Classifier picking the most frequent class): ~81.0% accuracy.
* Our Model: ~94.0% accuracy, 93.3% precision, 73.7% recall, and an F1 score of 82.4%.
More importantly, we extract the model coefficients to explain to the student exactly how attendance, prior marks, assignment completion, and recent momentum influenced the outcome."

---

### Q4: "What happens if the ML model fails or the file is missing?"
**Honest Answer:**
"EduLift AI is architected for graceful degradation. If the model artifact (`student_model.joblib`) is missing or fails to load, the dashboard continues functioning completely normally using our rule-based recommendation engine. The ML section displays an informative advisory message with instructions on how to train the model, ensuring students and faculty are never blocked."

---

### Q5: "How do you protect student privacy and prevent unauthorized data access?"
**Honest Answer:**
"We enforce security strictly on the backend:
1. **Password Security:** Passwords are never stored in plaintext; we use scrypt-based password hashing with Werkzeug.
2. **Session Authentication:** Route access requires valid session cookies signed with a server secret key.
3. **Student Isolation:** The student dashboard queries data exclusively using the logged-in student's `session['user_id']`. A student cannot access another student's data by tampering with query parameters or URLs.
4. **Cohort Isolation:** Faculty access is verified through a cohort mapping table (`faculty_cohorts`). If a faculty member attempts to inspect or edit a student outside their cohort, the server returns an HTTP 403 Forbidden error."

---

### Q6: "Doesn't flagging students risk demotivating them?"
**Honest Answer:**
"That exact concern drove our design philosophy. EduLift AI is explicitly built around *constructive improvement* rather than deficit labeling. We do not use words like 'At-Risk' or 'Failing.' Instead, our system uses phrases like 'Support Opportunity' and 'Focus Area.' Every observation comes with a clear reason, the supporting academic evidence, and an actionable next step such as pairing with a peer or attending office hours."

---

### Q7: "How is the weekly study planner schedule generated?"
**Honest Answer:**
"The study planner uses deterministic Python scheduling logic. Given a student's available hours (e.g., 8 hours/week), it calculates the number of 45-minute focused blocks. It distributes these across weekdays with built-in 15-minute breaks, automatically prioritizing subjects where upcoming assessments or exams are scheduled, ensuring a balanced workload without burnout."

---

### Q8: "Did you run tests to verify the application?"
**Honest Answer:**
"Yes. We wrote an automated test suite containing 23 tests across three test modules (`test_database.py`, `test_ml.py`, and `test_app.py`) using Python's built-in `unittest` framework. All 23 tests pass cleanly against isolated temporary databases, verifying health checks, route protections, input validation, snapshot creation, and ML reproducibility."
