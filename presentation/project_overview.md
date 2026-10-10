# EduLift AI — Project Overview

## 1. Problem Statement
First-year college students often experience academic disorientation when transitioning from high school to higher education. Changes in curriculum pace, self-directed learning expectations, and unfamiliar evaluation styles frequently lead to unnoticed dips in attendance and assessment performance.

Traditional educational portals suffer from critical shortcomings:
* **Passive Record-Keeping:** Portals simply store marks without translating numbers into actionable guidance.
* **Delayed Interventions:** Faculty typically discover academic distress only at the end of the semester when remedial actions are too late.
* **Deficit-Oriented Labeling:** Students falling behind are often labeled as "at-risk" or "underperforming," which creates anxiety rather than encouragement.

## 2. Our Solution: EduLift AI
**EduLift AI** is an AI-powered student analytics and success platform designed to support students constructively throughout their semester. Rather than labeling students as failures, EduLift AI:
1. **Analyzes Multi-Factor Markers:** Monitors attendance trends, subject marks, assignment completion rates, and recent performance momentum.
2. **Generates Constructive Recommendations:** Provides rule-based and machine-learning advisories that explain *what* the observation is, *why* it appeared, the *academic evidence*, and a concrete *action* the student can take.
3. **Empowers Self-Regulation:** Provides an integrated weekly study planner and personal goal tracker that respects the student's available hours with built-in rest intervals.
4. **Enables Supportive Faculty Mentoring:** Gives faculty cohort-level visibility and a dedicated intervention management workflow to record check-ins, tutoring plans, and follow-up outcomes.

## 3. Target Users
* **First-Year Engineering & College Students:** Students seeking clarity on how their attendance and test scores correlate with success, along with realistic weekly study timetables.
* **Faculty Advisors & Mentors:** Instructors who want early indicators of student difficulty to provide proactive, compassionate support rather than post-mortem grading.
* **Academic Departments & Cohort Coordinators:** Administrators who need cohort-wide subject averages to identify challenging coursework modules.

## 4. Key Core Features
* **Role-Protected Dashboards:** Separate secure portals for students (isolated to their own records) and faculty (scoped strictly to their assigned cohorts).
* **Rule-Based Recommendation Engine:** Deterministic, transparent logic that suggests actions when attendance dips below demo thresholds or scores decrease.
* **Transparent ML Advisory Demonstration:** Scikit-learn Logistic Regression trained on reproducible synthetic data, complete with baseline comparisons, genuine evaluation metrics, and factor impact attribution.
* **Weekly Study Planner:** Algorithmically generates balanced 45-minute study sessions with 15-minute breaks, dynamically prioritizing subjects with upcoming exams.
* **Point-in-Time Progress Snapshots:** Allows students to capture and audit their academic milestones over the semester.
* **Faculty Intervention Log:** Structured tracking of mentoring check-ins with statuses: *Planned*, *In progress*, *Completed*, and *Dismissed*.

## 5. Technology Stack
* **Frontend:** HTML5, CSS3, JavaScript (ES6), Chart.js (bundled locally for offline reliability).
* **Backend:** Python 3, Flask framework.
* **Database:** SQLite3 with foreign key enforcement and parameterized queries.
* **AI & Machine Learning:** scikit-learn, pandas, numpy, joblib.
* **Testing:** Python `unittest` suite with isolated temporary test databases.
