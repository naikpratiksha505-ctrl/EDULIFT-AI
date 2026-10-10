"""
EduLift AI - Database Seeder
Populates 6 distinct, highly realistic student demo accounts and 1 faculty account.
Each student represents a distinct academic archetype:
  1. Aarav Sharma (student_demo) - Mixed profile with recent Math dip
  2. Priya Patel (priya_demo)    - High Performer / Star Student (95% att, 93% marks)
  3. Rohan Verma (rohan_demo)    - High Support Needed / Compounding Obstacles (64% att, 55% marks)
  4. Ananya Iyer (ananya_demo)   - Consistent & Steady Achiever (88% att, 82% marks)
  5. Vikram Singh (vikram_demo)  - Self-Directed / Theory Attendance Gap (74% att, 77% marks)
  6. Sneha Kulkarni (sneha_demo) - Rapid Improver / Comeback Student (85% att, soaring marks)
"""

import json
from datetime import date, timedelta
from werkzeug.security import generate_password_hash
from database import init_db, get_connection


def seed_database(db_path: str = None) -> None:
    """Populate database with fictional demo accounts and variant academic records."""
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    print("Seeding EduLift AI database with 6 diverse student personas...")

    # Shared demo password hash (Password123!)
    demo_password_hash = generate_password_hash("Password123!")

    # 1. Create Cohort
    cursor.execute("""
        INSERT OR IGNORE INTO cohorts (id, name, description)
        VALUES (1, 'B.Tech AIML - 2026 (Section A)', 'First-Year Artificial Intelligence & Machine Learning cohort')
    """)

    # 2. Create Users
    # Faculty Account
    cursor.execute("""
        INSERT INTO users (id, username, password_hash, role, full_name, email)
        VALUES (1, 'faculty_demo', ?, 'faculty', 'Dr. Sunita Rao', 'sunita.rao@campus.edu')
        ON CONFLICT(id) DO UPDATE SET
            username=excluded.username,
            password_hash=excluded.password_hash,
            full_name=excluded.full_name,
            email=excluded.email
    """, (demo_password_hash,))

    # 6 Student Demo Users
    students_data = [
        (2, "student_demo", "Aarav Sharma", "aarav.sharma@student.edu", "26AIML042"),
        (3, "priya_demo",   "Priya Patel",   "priya.patel@student.edu",   "26AIML015"),
        (4, "rohan_demo",   "Rohan Verma",   "rohan.verma@student.edu",   "26AIML028"),
        (5, "ananya_demo",  "Ananya Iyer",   "ananya.iyer@student.edu",   "26AIML033"),
        (6, "vikram_demo",  "Vikram Singh",  "vikram.singh@student.edu",  "26AIML049"),
        (7, "sneha_demo",   "Sneha Kulkarni","sneha.kulkarni@student.edu","26AIML058"),
    ]

    for uid, uname, name, email, roll in students_data:
        cursor.execute("""
            INSERT INTO users (id, username, password_hash, role, full_name, email)
            VALUES (?, ?, ?, 'student', ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username=excluded.username,
                password_hash=excluded.password_hash,
                full_name=excluded.full_name,
                email=excluded.email
        """, (uid, uname, demo_password_hash, name, email))

    # 3. Assign Faculty to Cohort
    cursor.execute("""
        INSERT OR IGNORE INTO faculty_cohorts (user_id, cohort_id)
        VALUES (1, 1)
    """)

    # 4. Create Student Profiles
    for pid, (uid, uname, name, email, roll) in enumerate(students_data, start=1):
        cursor.execute("""
            INSERT INTO student_profiles (id, user_id, roll_number, cohort_id, semester, branch)
            VALUES (?, ?, ?, 1, 1, 'AI & Data Science')
            ON CONFLICT(id) DO UPDATE SET
                user_id=excluded.user_id,
                roll_number=excluded.roll_number
        """, (pid, uid, roll))

    # 5. Create Subjects
    subjects = [
        (1, 1, "MA101", "Mathematics for AI", 4),
        (2, 1, "CS101", "Programming with Python", 4),
        (3, 1, "AI101", "Introduction to Artificial Intelligence", 3),
        (4, 1, "CS102", "Digital Logic & Architecture", 3),
        (5, 1, "HS101", "Technical Communication", 2),
    ]

    for sub_id, cid, code, name, credits in subjects:
        cursor.execute("""
            INSERT INTO subjects (id, cohort_id, code, name, credits)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                cohort_id=excluded.cohort_id,
                code=excluded.code,
                name=excluded.name,
                credits=excluded.credits
        """, (sub_id, cid, code, name, credits))

    # 6. Seed Attendance Records (Varied across profiles)
    # Total classes = 42 for each subject
    today_str = date.today().isoformat()
    attendance_data = [
        # Student 1: Aarav (Mixed / Math Dip -> 80.0% overall)
        (1, 1, 42, 29),  # 69.0%
        (1, 2, 42, 38),  # 90.5%
        (1, 3, 42, 32),  # 76.2%
        (1, 4, 42, 30),  # 71.4%
        (1, 5, 42, 39),  # 92.8%

        # Student 2: Priya (Star Student -> 95.7% overall)
        (2, 1, 42, 40),  # 95.2%
        (2, 2, 42, 41),  # 97.6%
        (2, 3, 42, 39),  # 92.8%
        (2, 4, 42, 40),  # 95.2%
        (2, 5, 42, 41),  # 97.6%

        # Student 3: Rohan (High Support Needed -> 63.8% overall)
        (3, 1, 42, 25),  # 59.5%
        (3, 2, 42, 28),  # 66.7%
        (3, 3, 42, 24),  # 57.1%
        (3, 4, 42, 27),  # 64.3%
        (3, 5, 42, 30),  # 71.4%

        # Student 4: Ananya (Steady Consistent -> 88.1% overall)
        (4, 1, 42, 37),  # 88.1%
        (4, 2, 42, 38),  # 90.5%
        (4, 3, 42, 36),  # 85.7%
        (4, 4, 42, 36),  # 85.7%
        (4, 5, 42, 38),  # 90.5%

        # Student 5: Vikram (Theory Gap / Lab Strong -> 74.8% overall)
        (5, 1, 42, 28),  # 66.7% (8am lecture)
        (5, 2, 42, 37),  # 88.1% (practical lab)
        (5, 3, 42, 30),  # 71.4%
        (5, 4, 42, 27),  # 64.3%
        (5, 5, 42, 35),  # 83.3%

        # Student 6: Sneha (Rapid Improver -> 84.8% overall)
        (6, 1, 42, 35),  # 83.3%
        (6, 2, 42, 37),  # 88.1%
        (6, 3, 42, 34),  # 81.0%
        (6, 4, 42, 35),  # 83.3%
        (6, 5, 42, 37),  # 88.1%
    ]

    for sid, sub_id, total, attended in attendance_data:
        cursor.execute("""
            INSERT OR REPLACE INTO attendance (student_id, subject_id, total_classes, attended_classes, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (sid, sub_id, total, attended, today_str))

    # 7. Seed Assessment Marks (Showing contrasting trends)
    d1 = (date.today() - timedelta(days=42)).isoformat()
    d2 = (date.today() - timedelta(days=26)).isoformat()
    d3 = (date.today() - timedelta(days=9)).isoformat()

    # Clear previous marks to allow fresh variance
    cursor.execute("DELETE FROM assessment_marks")

    assessments = [
        # Student 1: Aarav (Math dip from 78 to 70 to 58, strong Python 85->88->92)
        (1, 1, "Quiz 1", 78, 100, d1),
        (1, 1, "Midterm Exam", 70, 100, d2),
        (1, 1, "Assignment 1", 58, 100, d3),
        (1, 2, "Quiz 1", 85, 100, d1),
        (1, 2, "Midterm Exam", 88, 100, d2),
        (1, 2, "Lab Project", 92, 100, d3),
        (1, 3, "Quiz 1", 74, 100, d1),
        (1, 3, "Midterm Exam", 76, 100, d2),
        (1, 4, "Quiz 1", 68, 100, d1),
        (1, 4, "Midterm Exam", 64, 100, d2),
        (1, 5, "Presentation", 85, 100, d2),

        # Student 2: Priya (Star Student: consistently 90-98%)
        (2, 1, "Quiz 1", 94, 100, d1),
        (2, 1, "Midterm Exam", 92, 100, d2),
        (2, 1, "Assignment 1", 96, 100, d3),
        (2, 2, "Quiz 1", 96, 100, d1),
        (2, 2, "Midterm Exam", 98, 100, d2),
        (2, 2, "Lab Project", 95, 100, d3),
        (2, 3, "Quiz 1", 90, 100, d1),
        (2, 3, "Midterm Exam", 93, 100, d2),
        (2, 4, "Quiz 1", 89, 100, d1),
        (2, 4, "Midterm Exam", 91, 100, d2),
        (2, 5, "Presentation", 95, 100, d2),

        # Student 3: Rohan (Downward Trend: 62 -> 56 -> 48 in Math; 64 -> 56 -> 50 in Python)
        (3, 1, "Quiz 1", 62, 100, d1),
        (3, 1, "Midterm Exam", 54, 100, d2),
        (3, 1, "Assignment 1", 46, 100, d3),
        (3, 2, "Quiz 1", 64, 100, d1),
        (3, 2, "Midterm Exam", 56, 100, d2),
        (3, 2, "Lab Project", 50, 100, d3),
        (3, 3, "Quiz 1", 55, 100, d1),
        (3, 3, "Midterm Exam", 51, 100, d2),
        (3, 4, "Quiz 1", 58, 100, d1),
        (3, 4, "Midterm Exam", 52, 100, d2),
        (3, 5, "Presentation", 64, 100, d2),

        # Student 4: Ananya (Steady Consistency: 80-86% across the board)
        (4, 1, "Quiz 1", 82, 100, d1),
        (4, 1, "Midterm Exam", 80, 100, d2),
        (4, 1, "Assignment 1", 84, 100, d3),
        (4, 2, "Quiz 1", 84, 100, d1),
        (4, 2, "Midterm Exam", 85, 100, d2),
        (4, 2, "Lab Project", 86, 100, d3),
        (4, 3, "Quiz 1", 78, 100, d1),
        (4, 3, "Midterm Exam", 81, 100, d2),
        (4, 4, "Quiz 1", 79, 100, d1),
        (4, 4, "Midterm Exam", 82, 100, d2),
        (4, 5, "Presentation", 86, 100, d2),

        # Student 5: Vikram (Solid scores despite missing morning lectures: 72-88%)
        (5, 1, "Quiz 1", 76, 100, d1),
        (5, 1, "Midterm Exam", 74, 100, d2),
        (5, 1, "Assignment 1", 75, 100, d3),
        (5, 2, "Quiz 1", 86, 100, d1),
        (5, 2, "Midterm Exam", 84, 100, d2),
        (5, 2, "Lab Project", 88, 100, d3),
        (5, 3, "Quiz 1", 72, 100, d1),
        (5, 3, "Midterm Exam", 75, 100, d2),
        (5, 4, "Quiz 1", 70, 100, d1),
        (5, 4, "Midterm Exam", 68, 100, d2),
        (5, 5, "Presentation", 80, 100, d2),

        # Student 6: Sneha (The Comeback Student: soaring from 54->68->84 in Math!)
        (6, 1, "Quiz 1", 54, 100, d1),
        (6, 1, "Midterm Exam", 68, 100, d2),
        (6, 1, "Assignment 1", 84, 100, d3),
        (6, 2, "Quiz 1", 60, 100, d1),
        (6, 2, "Midterm Exam", 75, 100, d2),
        (6, 2, "Lab Project", 88, 100, d3),
        (6, 3, "Quiz 1", 62, 100, d1),
        (6, 3, "Midterm Exam", 78, 100, d2),
        (6, 4, "Quiz 1", 58, 100, d1),
        (6, 4, "Midterm Exam", 74, 100, d2),
        (6, 5, "Presentation", 82, 100, d2),
    ]

    for sid, sub_id, name, score, max_score, dt in assessments:
        cursor.execute("""
            INSERT INTO assessment_marks (student_id, subject_id, assessment_name, score, max_score, date_recorded)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sid, sub_id, name, score, max_score, dt))

    # 8. Seed Study Goals for All 6 Students
    cursor.execute("DELETE FROM study_goals")
    study_goals = [
        # Aarav (2 done, 2 pending)
        (1, "Complete Python Week 4 Practice Problems", "Solve 5 recursion and list comprehension exercises", (date.today() + timedelta(days=2)).isoformat(), 1),
        (1, "Review Linear Algebra Eigenvalues", "Re-read Chapter 4 notes and solve Quiz 1 makeup questions", (date.today() + timedelta(days=4)).isoformat(), 1),
        (1, "Clarify Math Assignment 1 with Instructor", "Visit Dr. Sunita during office hours on Thursday", (date.today() + timedelta(days=3)).isoformat(), 0),
        (1, "Build Digital Logic Circuit Simulation", "Complete Logisim lab for CS102 multiplexers", (date.today() + timedelta(days=7)).isoformat(), 0),

        # Priya (4 done, 1 pending)
        (2, "Implement A* Pathfinding Visualizer in Python", "Build interactive grid search script", (date.today() - timedelta(days=3)).isoformat(), 1),
        (2, "Complete Multivariable Calculus Problem Set", "Finish vector gradient proof exercises", (date.today() - timedelta(days=5)).isoformat(), 1),
        (2, "Peer Tutor 2 Classmates on Boolean Algebra", "Help review Karnaugh maps before midterm", (date.today() - timedelta(days=1)).isoformat(), 1),
        (2, "Prepare Slides for AI Ethics Symposium", "Draft 5 slides on fairness in machine learning", (date.today() + timedelta(days=1)).isoformat(), 1),
        (2, "Read Research Paper on Convolutional Neural Networks", "Study LeNet and AlexNet architecture", (date.today() + timedelta(days=6)).isoformat(), 0),

        # Rohan (1 done, 4 pending - struggling to keep up)
        (3, "Attempt Math Assignment 1 Revision", "Review problems 1 to 4 with peer tutor", (date.today() - timedelta(days=2)).isoformat(), 1),
        (3, "Review Python Loop Basics & Lists", "Catch up on week 3 syntax practice", (date.today() + timedelta(days=1)).isoformat(), 0),
        (3, "Meet Dr. Sunita for Mentoring Consultation", "Discuss attendance makeup options", (date.today() + timedelta(days=2)).isoformat(), 0),
        (3, "Submit Makeup Lab for Digital Logic", "Breadboard circuit assignment", (date.today() + timedelta(days=4)).isoformat(), 0),
        (3, "Organize Chapter 1-3 Summary Notes", "Consolidate lecture handouts", (date.today() + timedelta(days=5)).isoformat(), 0),

        # Ananya (3 done, 1 pending - steady)
        (4, "Complete Python OOP Inheritance Worksheet", "Classes and polymorphism exercises", (date.today() - timedelta(days=4)).isoformat(), 1),
        (4, "Review AI Heuristic Search Formulations", "Manhattan distance vs Euclidean", (date.today() - timedelta(days=2)).isoformat(), 1),
        (4, "Prepare Flashcards for CS102 Micro-operations", "ALU control signals review", (date.today() - timedelta(days=1)).isoformat(), 1),
        (4, "Solve 3 Past Exam Papers in Linear Algebra", "Focus on matrix transformation questions", (date.today() + timedelta(days=4)).isoformat(), 0),

        # Vikram (2 done, 2 pending - self directed)
        (5, "Watch Recorded Lectures for Missed 8 AM Math", "Modules 5 & 6 on differential equations", (date.today() - timedelta(days=2)).isoformat(), 1),
        (5, "Complete Logisim Multiplexer Circuit Lab", "Simulate 4-to-1 MUX", (date.today() - timedelta(days=3)).isoformat(), 1),
        (5, "Submit Python Data Structures Lab Report", "File I/O performance benchmarks", (date.today() + timedelta(days=3)).isoformat(), 0),
        (5, "Coordinate Bus Route Transit Timing", "Adjust morning transit schedule", (date.today() + timedelta(days=5)).isoformat(), 0),

        # Sneha (3 done, 1 pending - rapid comeback)
        (6, "Clear Foundational Doubts in Matrix Algebra", "Solved 10 practice problems with tutor", (date.today() - timedelta(days=6)).isoformat(), 1),
        (6, "Complete Python Functions & Decorators Track", "Completed all HackerRank basic modules", (date.today() - timedelta(days=3)).isoformat(), 1),
        (6, "Attend Math Tutorial Makeup Session", "Attended Thursday problem clinic", (date.today() - timedelta(days=1)).isoformat(), 1),
        (6, "Prepare for Upcoming AI Search Midterm 2", "Review BFS, DFS, and heuristic graphs", (date.today() + timedelta(days=5)).isoformat(), 0),
    ]

    for sid, title, desc, target_dt, completed in study_goals:
        cursor.execute("""
            INSERT INTO study_goals (student_id, title, description, target_date, is_completed)
            VALUES (?, ?, ?, ?, ?)
        """, (sid, title, desc, target_dt, completed))

    # 9. Seed Study Planner Tasks for All Students
    cursor.execute("DELETE FROM study_tasks")
    tasks = [
        # Aarav (student 1)
        (1, 1, "Math for AI: Matrix Operations Review", "Monday", "18:00", 45, "High", 1),
        (1, 2, "Programming with Python: File I/O & Functions", "Tuesday", "18:00", 45, "Medium", 1),
        (1, 3, "Intro to AI: State Space Search Summary", "Wednesday", "19:00", 45, "Medium", 0),
        (1, 1, "Math for AI: Problem Set 2 Practice", "Thursday", "18:00", 45, "High", 0),
        (1, 4, "Digital Logic: Karnaugh Map Simplification", "Friday", "17:00", 45, "Medium", 0),

        # Priya (student 2 - highly disciplined)
        (2, 2, "Python: Advanced Algorithms & Dynamic Programming", "Monday", "17:00", 45, "High", 1),
        (2, 1, "Math for AI: Vector Spaces & Inner Products", "Tuesday", "17:00", 45, "High", 1),
        (2, 3, "Intro to AI: Neural Network Forward Propagation", "Wednesday", "17:00", 45, "Medium", 1),
        (2, 4, "Digital Logic: Finite State Machine Design", "Thursday", "18:00", 45, "Medium", 1),
        (2, 3, "AI Ethics: Reading Seminal Fairness Papers", "Friday", "18:00", 45, "Low", 0),

        # Rohan (student 3 - remedial plan)
        (3, 1, "Math for AI: Remedial Matrix Multiplication", "Monday", "19:00", 45, "High", 1),
        (3, 2, "Python: Practice 5 Basic Syntax Tasks", "Tuesday", "19:00", 45, "High", 0),
        (3, 3, "Intro to AI: Review Lecture 3 & 4 Slides", "Thursday", "19:00", 45, "Medium", 0),

        # Ananya (student 4 - balanced)
        (4, 1, "Math for AI: Eigenvalues & Vector Spaces", "Monday", "18:00", 45, "Medium", 1),
        (4, 2, "Python: Class Design & Exceptions", "Wednesday", "18:00", 45, "Medium", 1),
        (4, 3, "Intro to AI: A* and Greedy Search Formulations", "Friday", "18:00", 45, "Medium", 0),
        (4, 4, "Digital Logic: Flip-Flops & Registers", "Saturday", "11:00", 45, "Low", 0),

        # Vikram (student 5 - lecture catchup)
        (5, 1, "Math for AI: Review Recorded 8 AM Lecture Notes", "Tuesday", "18:00", 45, "High", 1),
        (5, 4, "Digital Logic: Logic Gate Simulations", "Thursday", "18:00", 45, "Medium", 0),
        (5, 2, "Python: Practice API & JSON Parsing", "Saturday", "10:00", 45, "Medium", 0),

        # Sneha (student 6 - momentum builder)
        (6, 1, "Math for AI: Practice Midterm Exam Problems", "Monday", "18:00", 45, "High", 1),
        (6, 2, "Python: Advanced Functions & Decorators", "Wednesday", "18:00", 45, "High", 1),
        (6, 3, "Intro to AI: Review Classification Algorithms", "Friday", "18:00", 45, "Medium", 0),
        (6, 4, "Digital Logic: Instruction Cycle & Assembly", "Saturday", "16:00", 45, "Medium", 0),
    ]

    for sid, sub_id, title, day, start_time, duration, prio, comp in tasks:
        cursor.execute("""
            INSERT INTO study_tasks (student_id, subject_id, title, day_of_week, start_time, duration_minutes, priority, is_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, sub_id, title, day, start_time, duration, prio, comp))

    # 10. Seed Historical Progress Snapshots for All 6 Students
    cursor.execute("DELETE FROM progress_snapshots")
    snapshots = [
        # Aarav (student 1: subtle decline in Math)
        (1, 84.5, 79.0, 1, 3, json.dumps({"Math": 78.0, "Python": 85.0, "AI": 74.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 10:00:00"),
        (1, 82.0, 77.5, 2, 2, json.dumps({"Math": 74.0, "Python": 88.0, "AI": 75.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 15:30:00"),

        # Priya (student 2: steady excellence)
        (2, 96.0, 91.5, 2, 3, json.dumps({"Math": 94.0, "Python": 96.0, "AI": 90.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 09:30:00"),
        (2, 95.7, 93.8, 4, 1, json.dumps({"Math": 95.0, "Python": 97.0, "AI": 92.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 11:00:00"),

        # Rohan (student 3: noticeable decline)
        (3, 71.0, 62.0, 0, 4, json.dumps({"Math": 62.0, "Python": 64.0, "AI": 55.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 14:15:00"),
        (3, 66.5, 57.5, 1, 4, json.dumps({"Math": 54.0, "Python": 56.0, "AI": 51.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 16:45:00"),

        # Ananya (student 4: plateau / steady)
        (4, 87.5, 81.0, 1, 3, json.dumps({"Math": 82.0, "Python": 84.0, "AI": 78.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 10:00:00"),
        (4, 88.1, 82.7, 3, 1, json.dumps({"Math": 82.0, "Python": 85.0, "AI": 80.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 14:00:00"),

        # Vikram (student 5: attendance slipped from 78% to 74.8%, marks held steady)
        (5, 78.5, 76.0, 1, 3, json.dumps({"Math": 76.0, "Python": 86.0, "AI": 72.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 11:30:00"),
        (5, 74.8, 76.8, 2, 2, json.dumps({"Math": 75.0, "Python": 87.0, "AI": 74.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 12:15:00"),

        # Sneha (student 6: dramatic comeback curve!)
        (6, 78.0, 58.5, 1, 3, json.dumps({"Math": 54.0, "Python": 60.0, "AI": 62.0}), 1, (date.today() - timedelta(days=21)).isoformat() + " 13:00:00"),
        (6, 82.5, 67.0, 2, 2, json.dumps({"Math": 68.0, "Python": 75.0, "AI": 78.0}), 1, (date.today() - timedelta(days=7)).isoformat() + " 15:45:00"),
    ]

    for sid, att, avg_m, comp_g, pend_g, bdown, is_sd, created_at in snapshots:
        cursor.execute("""
            INSERT INTO progress_snapshots
            (student_id, attendance_pct, avg_marks, completed_goals, pending_goals, subject_breakdown_json, is_seed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, att, avg_m, comp_g, pend_g, bdown, is_sd, created_at))

    # 11. Seed Faculty Interventions
    cursor.execute("DELETE FROM faculty_interventions")
    interventions = [
        (
            1, 1,
            "Attendance decreased below 75% in Mathematics for AI",
            "Peer study buddy pairing & faculty office hour consultation",
            "Noticed Aarav missed two Tuesday morning sessions due to transit delays. Advised on lecture recording resources.",
            (date.today() + timedelta(days=5)).isoformat(),
            "In progress",
            "Aarav agreed to review recorded modules and attend Thursday tutorial."
        ),
        (
            3, 1,
            "Attendance dropped below 65% with downward score trends across core subjects",
            "Comprehensive 1-on-1 counseling, remedial question bank, and peer tutoring pair",
            "Reached out to Rohan to provide guidance on core foundational math and python concepts.",
            (date.today() + timedelta(days=4)).isoformat(),
            "In progress",
            "Diagnostic quiz scheduled; peer buddy assigned."
        ),
        (
            5, 1,
            "Morning transit delays causing attendance gap in 8 AM theory classes",
            "Lecture recording access and transportation route coordination",
            "Vikram is performing well in exams (77%) but missing attendance benchmarks due to morning bus schedule.",
            (date.today() - timedelta(days=4)).isoformat(),
            "Completed",
            "Student adjusted commute; accessing lecture recordings regularly."
        ),
        (
            6, 1,
            "Early semester exam difficulty in foundational mathematics",
            "Remedial problem clinic and study schedule calibration",
            "Sneha attended Thursday tutorial and worked through extra problem sheets.",
            (date.today() - timedelta(days=2)).isoformat(),
            "Completed",
            "Remarkable turnaround: score surged from 54% to 84% on recent assignment!"
        ),
    ]

    for sid, fid, reason, act, notes, f_date, stat, out_notes in interventions:
        cursor.execute("""
            INSERT INTO faculty_interventions
            (student_id, faculty_id, indicator_reason, suggested_action, faculty_notes, follow_up_date, status, outcome_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, fid, reason, act, notes, f_date, stat, out_notes))

    conn.commit()
    conn.close()
    print("Database seeding completed successfully for all 6 student personas.")


if __name__ == "__main__":
    seed_database()
