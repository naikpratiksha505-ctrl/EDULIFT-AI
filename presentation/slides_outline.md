# EduLift AI — Presentation Slides Outline

## Slide 1: Title Slide
* **Title:** EduLift AI — AI-Powered Student Analytics and Success Platform
* **Tagline:** Every Student Deserves a Chance to Succeed.
* **Presenters:** First-Year B.Tech AIML Student Team
* **Event:** College Innovation Hackathon 2026

## Slide 2: The Problem & Context
* **Context:** The transition from secondary school to first-year university is academically rigorous and fast-paced.
* **The Challenge:** Students encounter unexpected difficulties in attendance, foundational subjects (Linear Algebra, Programming), and study habits.
* **Consequence:** Dips compound quietly until midterms or finals, resulting in academic probation or withdrawal.

## Slide 3: Existing Gaps in College Portals
* **Passive Recording:** Systems log grades and absentees without diagnostic analysis.
* **Siloed Communication:** Faculty and students lack a shared constructive support plan.
* **Negative Stigmatization:** Alerts are often punitive ("at-risk list") rather than encouraging.

## Slide 4: Our Solution — EduLift AI
* **Mission:** Early, constructive, and ethical academic support.
* **Two Integrated Portals:**
  * **Student Portal:** Diagnostic feedback, goal tracking, and smart weekly study planning.
  * **Faculty Portal:** Cohort analytics, support alerts, and intervention lifecycle management.

## Slide 5: Core Features Walkthrough
* **Attendance & Mark Tracking:** Chronological Chart.js trends and subject-wise averages.
* **Supportive AI Recommendations:** 4-part explanations (Observation, Root Cause, Academic Evidence, Actionable Next Step).
* **Weekly Study Planner:** Automated session generation (45m study + 15m rest) calibrated to student availability and upcoming tests.
* **Milestone Snapshots:** Point-in-time progress audits.

## Slide 6: Faculty Mentorship & Interventions
* **Cohort-Scoped Access:** Faculty only see their assigned batches.
* **Intervention Tracking:** Structured check-in records with lifecycle statuses: *Planned*, *In progress*, *Completed*, *Dismissed*.
* **Constructive Framing:** Supportive alerts ("This student may benefit from a check-in...") replace stigmatizing flags.

## Slide 7: AI & Machine Learning Demonstration
* **Dual Approach:** Deterministic rules + scikit-learn Logistic Regression.
* **Synthetic Data Generation:** 500 samples with fixed seed (`random_seed=42`) for reproducibility.
* **Transparent Evaluation:**
  * Baseline (Most Frequent Class): ~81.0%
  * Logistic Regression: ~94.0% accuracy, 93.3% precision, 82.4% F1 score.
* **Factor Attribution:** Coefficients explain which features contributed to the advisory result.

## Slide 8: Privacy, Ethics & Security
* **Data Isolation:** Students can only view their own profile; direct URL tampering is blocked server-side.
* **Cohort Protection:** Faculty access is strictly verified by cohort assignment via foreign keys.
* **Password Security:** Scrypt password hashing with Werkzeug.
* **Ethical Advisory Notice:** Clear warning displayed: *"Demonstration uses synthetic data and is not validated for real students. Predictions are advisory and must not be used for disciplinary decisions."*

## Slide 9: Technology Stack
* **Frontend:** Clean Semantic HTML5, Custom Responsive CSS (Navy & Teal theme), Vanilla JS, Chart.js.
* **Backend:** Python 3, Flask framework, Werkzeug security.
* **Database:** SQLite3 with foreign keys and parameterized SQL queries.
* **ML:** pandas, numpy, scikit-learn, joblib.
* **Offline-Ready:** Bundled local assets with zero external API dependencies.

## Slide 10: Future Scope & Roadmap
* **LMS Integration:** Webhook connections to Moodle/Canvas for real-time quiz updates.
* **Peer Tutoring Exchange:** Matching students excelling in a subject with peers seeking study partners.
* **Longitudinal Studies:** Ethically validated predictive models calibrated with institutional ethics committee approval.
* **Mobile Companion App:** Lightweight offline-first mobile interface.
