# EduLift AI — AI-Powered Student Analytics and Success Platform

> **"Every Student Deserves a Chance to Succeed."**  
> A beginner-friendly, full-stack educational analytics platform built with Python, Flask, SQLite, and scikit-learn for first-year engineering students and faculty mentors.

---

## 🌟 What EduLift AI Does

EduLift AI bridges the gap between academic data and supportive mentorship:
* **For Students:**
  * Displays attendance percentages, subject-wise marks, and chronological performance trends using interactive Chart.js charts.
  * Generates **Supportive AI Recommendations** with 4-part explanations: what the observation is, why it appeared, the academic evidence, and an actionable next step.
  * Provides an automated **Weekly Study Planner** generating balanced 45-minute focus sessions with 15-minute breaks calibrated to available hours.
  * Tracks personal study goals and captures point-in-time **Progress Snapshots**.
  * Shows a scikit-learn **Machine Learning Advisory Demonstration** with factor attribution and clear ethical warnings.
* **For Faculty:**
  * Provides aggregate cohort statistics (cohort average attendance, average marks, subject benchmarks).
  * Highlights students who benefit from check-ins using constructive language (e.g. *"This student may benefit from a check-in because attendance has decreased."*).
  * Includes a real-time student search and filtering tool.
  * Supports correction of attendance and recording of new assessment results.
  * Manages the complete **Intervention Lifecycle**: *Planned*, *In progress*, *Completed*, and *Dismissed* with follow-up dates and notes.

---

## 📁 Project Structure

```text
edulift-ai/
│
├── app.py                     # Main Flask web application and protected routes
├── database.py                # SQLite database connection layer and query helpers
├── recommendations.py         # Rule-based academic recommendation engine
├── planner.py                 # Weekly study timetable generation algorithm
├── seed_data.py               # Repeatable seeder for demo accounts and records
├── reset_database.py          # Database reset utility (drops & reseeds tables)
├── requirements.txt           # Project Python dependencies
├── .env.example               # Environment variable configuration template
├── .gitignore                 # Git ignore rules for virtual environments & DB
├── README.md                  # Comprehensive setup and usage guide
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Core navigation layout, sidebar, and flash alerts
│   ├── index.html             # Landing page with hero banner & feature highlights
│   ├── login.html             # Sign-in portal with 1-click demo credential autofill
│   ├── student_dashboard.html # Student metrics, chart, recommendations & goals
│   ├── faculty_dashboard.html # Faculty cohort analytics, alerts & roster
│   ├── student_detail.html    # Faculty individual student profile & interventions
│   └── study_planner.html     # Automated weekly timetable generator & tasks
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern responsive styling (Navy & Teal theme)
│   └── js/
│       ├── chart.umd.min.js   # Bundled local Chart.js (runs 100% offline)
│       └── dashboard.js       # Client-side chart rendering and search filters
│
├── ml/                        # Machine Learning Demonstration
│   ├── generate_data.py       # Generates reproducible synthetic training data
│   ├── train_model.py         # Trains Logistic Regression & evaluates metrics
│   ├── predict.py             # Predicts advisory support need & feature attribution
│   ├── synthetic_students.csv # Generated dataset (500 synthetic records)
│   ├── student_model.joblib   # Trained model artifact
│   └── model_metrics.json     # Saved evaluation metrics & feature weights
│
├── tests/                     # Automated Test Suite (23 Unit Tests)
│   ├── test_app.py            # Route protection, authentication, and validation tests
│   ├── test_database.py       # SQLite schemas, foreign keys, and query tests
│   └── test_ml.py             # ML synthetic generation, training, and prediction tests
│
└── presentation/              # Hackathon Pitch & Presentation Resources
    ├── project_overview.md    # Problem, solution, features, and benefits
    ├── pitch_script.md        # 60–90 second natural pitch script
    ├── slides_outline.md      # 10-slide presentation deck structure
    ├── demo_script.md         # Step-by-step 3-5 minute live demo guide
    ├── judge_questions.md     # Anticipated judge questions & honest answers
    └── limitations_and_future_scope.md # Ethical limits & production roadmap
```

---

## ⚡ Quick Start Guide (Run in 3 Steps)

### Step 1: Install Dependencies
Make sure you have **Python 3.10+** installed.

#### Windows (PowerShell):
```powershell
python -m pip install -r requirements.txt
```

#### macOS / Linux:
```bash
python3 -m pip install -r requirements.txt
```

*(Optional: If you prefer using a virtual environment)*:
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

---

### Step 2: Initialize Database & Train ML Model

Run the seeder and training scripts:

#### Windows (PowerShell):
```powershell
python seed_data.py
python ml/generate_data.py
python ml/train_model.py
```

#### macOS / Linux:
```bash
python3 seed_data.py
python3 ml/generate_data.py
python3 ml/train_model.py
```

---

### Step 3: Start the Web Application

#### Windows (PowerShell):
```powershell
python app.py
```

#### macOS / Linux:
```bash
python3 app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000/`**

---

## 🔑 Demo Accounts & Varied Student Personas

EduLift AI comes pre-loaded with **6 distinct, realistic student personas** and **1 faculty mentor account**. Each persona features a completely different attendance level, assessment trajectory, progress bar status, and recommendation set:

| Persona & Role | Username / Alias | Password | Attendance | Avg Marks | Key Characteristics & Demo Storyline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Star Student** | `priya_demo` | `Password123!` | **95.7%** | **93.5%** | **Priya Patel:** Top performer across all subjects, high goals completion, excelling status, <3% ML support risk. |
| 🟡 **Mixed Profile** | `student_demo` | `Password123!` | **80.0%** | **76.2%** | **Aarav Sharma:** Good overall standing, but recent Math assignment dipped from 78 to 58%, triggering targeted review advice. |
| 🔴 **Needs Support** | `rohan_demo` | `Password123!` | **63.8%** | **55.6%** | **Rohan Verma:** Below 75% attendance in 4 subjects, declining test scores, 99.2% ML support alert, active faculty check-in intervention. |
| 📈 **Rapid Improver** | `sneha_demo` | `Password123!` | **84.8%** | **71.2%** | **Sneha Kulkarni:** Started with 54% in Math, soared to 84% (+30% momentum)! AI celebrates positive momentum in recommendations. |
| 🟣 **Transit / Theory Gap** | `vikram_demo` | `Password123!` | **74.8%** | **77.1%** | **Vikram Singh:** Morning 8 AM lecture commute delay (66% Math att), but scores 77% on exams. System isolates transit issue without labeling failure. |
| ⚪ **Steady Achiever** | `ananya_demo` | `Password123!` | **88.1%** | **82.5%** | **Ananya Iyer:** Highly consistent attendance and marks across every subject, balanced study timetable. |
| 🎓 **Faculty Mentor** | `faculty_demo` | `Password123!` | *Cohort Avg: 81.2%* | *Cohort Avg: 76.0%* | **Dr. Sunita Rao:** Cohort analytics, real-time student search, early support alerts, and intervention lifecycle tracker. |

> **Pro Tip for Hackathon Judges:** On the Login page (`/login`), click any of the 1-click persona buttons in the **Quick Hackathon Autofill** grid to switch instantly between these datasets!

---

## 🧪 Running the Test Suite

EduLift AI includes a comprehensive test suite using Python's built-in `unittest` runner. Tests execute against isolated temporary SQLite databases so your local data is never modified.

To run all 23 tests:

```bash
python -m unittest discover tests
```

Expected output:
```text
Ran 23 tests in ~12s
OK
```

---

## 🔄 Resetting the Database

If you want to clear your local test entries and restore the original fictional seed dataset:

```bash
python reset_database.py
```
> **Warning:** This will erase any new goals, tasks, or marks added during local testing and restore fresh seed accounts.

---

## ⚠️ Security Notice & Limitations

1. **Local Demonstration Passwords:** The demo credentials (`Password123!`) are intended solely for offline hackathon evaluations.
2. **Synthetic ML Data:** The machine learning model is trained on 500 synthetic records with fixed random seeds. Predictions are purely advisory demonstrations to highlight feature attribution and must never be used for actual disciplinary or academic decisions.
3. **Data Scope:** In production, SQLite should be upgraded to PostgreSQL with connection pooling, and session cookies replaced with campus Single Sign-On (SSO / OAuth2).

---

## 🛠️ Troubleshooting & FAQ

* **Port 5000 already in use?**
  Set a custom port in your environment or run:
  ```powershell
  $env:PORT="5050"; python app.py
  ```
* **Offline charts not rendering?**
  A complete copy of `chart.umd.min.js` is bundled in `static/js/`, so charts work 100% offline without internet access.
* **Missing ML Model banner?**
  If `ml/student_model.joblib` is deleted, the app gracefully falls back to the rule-based engine. Simply re-run `python ml/train_model.py`.
