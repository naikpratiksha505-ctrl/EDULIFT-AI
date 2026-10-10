"""
EduLift AI - Database Layer
Uses Python's built-in sqlite3 module to manage persistent data.
Includes clean tables for users, profiles, cohorts, marks, attendance,
goals, study planner tasks, snapshots, and faculty interventions.
"""

import os
import sqlite3
from typing import Optional

# Default database filename
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "edulift.db")


def get_db_path(override_path: Optional[str] = None) -> str:
    """Return the database path, allowing environment or test overrides."""
    if override_path:
        return override_path
    return os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Open a connection to the SQLite database.
    Enables foreign keys and sets row_factory to sqlite3.Row for dict-like access.
    """
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """
    Initialize all tables in the SQLite database.
    Safe to run multiple times (uses CREATE TABLE IF NOT EXISTS).
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table (Students & Faculty)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'faculty')),
            full_name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Cohorts Table (Batches/Sections)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cohorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );
    """)

    # 3. Student Profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            cohort_id INTEGER NOT NULL,
            semester INTEGER DEFAULT 1,
            branch TEXT DEFAULT 'AI & Data Science',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (cohort_id) REFERENCES cohorts (id) ON DELETE RESTRICT
        );
    """)

    # 4. Faculty Cohort Mapping
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty_cohorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cohort_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (cohort_id) REFERENCES cohorts (id) ON DELETE CASCADE,
            UNIQUE(user_id, cohort_id)
        );
    """)

    # 5. Subjects Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cohort_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            FOREIGN KEY (cohort_id) REFERENCES cohorts (id) ON DELETE CASCADE,
            UNIQUE(cohort_id, code)
        );
    """)

    # 6. Assessment Marks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            assessment_name TEXT NOT NULL,
            score REAL NOT NULL CHECK(score >= 0),
            max_score REAL NOT NULL DEFAULT 100 CHECK(max_score > 0),
            date_recorded DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES student_profiles (id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
        );
    """)

    # 7. Attendance Records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            total_classes INTEGER NOT NULL DEFAULT 0 CHECK(total_classes >= 0),
            attended_classes INTEGER NOT NULL DEFAULT 0 CHECK(attended_classes >= 0),
            last_updated DATE,
            FOREIGN KEY (student_id) REFERENCES student_profiles (id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
            UNIQUE(student_id, subject_id)
        );
    """)

    # 8. Study Goals (Personal goal tracker)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            target_date DATE,
            is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0, 1)),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 9. Study Tasks (Weekly timetable tasks generated or manually added)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER,
            title TEXT NOT NULL,
            day_of_week TEXT NOT NULL,
            start_time TEXT,
            duration_minutes INTEGER NOT NULL DEFAULT 45 CHECK(duration_minutes > 0),
            priority TEXT NOT NULL DEFAULT 'Medium' CHECK(priority IN ('High', 'Medium', 'Low')),
            is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0, 1)),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles (id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE SET NULL
        );
    """)

    # 10. Progress Snapshots (Point-in-time performance records)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_pct REAL NOT NULL,
            avg_marks REAL NOT NULL,
            completed_goals INTEGER NOT NULL DEFAULT 0,
            pending_goals INTEGER NOT NULL DEFAULT 0,
            subject_breakdown_json TEXT,
            is_seed INTEGER NOT NULL DEFAULT 0 CHECK(is_seed IN (0, 1)),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles (id) ON DELETE CASCADE
        );
    """)

    # 11. Faculty Interventions (Supportive mentoring & check-ins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty_interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            faculty_id INTEGER NOT NULL,
            indicator_reason TEXT NOT NULL,
            suggested_action TEXT NOT NULL,
            faculty_notes TEXT,
            follow_up_date DATE,
            status TEXT NOT NULL DEFAULT 'Planned' CHECK(status IN ('Planned', 'In progress', 'Completed', 'Dismissed')),
            outcome_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles (id) ON DELETE CASCADE,
            FOREIGN KEY (faculty_id) REFERENCES users (id) ON DELETE RESTRICT
        );
    """)

    conn.commit()
    conn.close()


def drop_all_tables(db_path: Optional[str] = None) -> None:
    """Drop all tables in the database to allow a clean reset."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    tables = [
        "faculty_interventions",
        "progress_snapshots",
        "study_tasks",
        "study_goals",
        "attendance",
        "assessment_marks",
        "subjects",
        "faculty_cohorts",
        "student_profiles",
        "cohorts",
        "users",
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
    conn.commit()
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.close()


# -------------------------------------------------------------
# Query Helper Functions
# -------------------------------------------------------------

def get_user_by_username(username: str, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieve user record by username, supporting convenient presentation aliases."""
    raw = username.strip().lower()
    alias_map = {
        "aarav": "student_demo",
        "aarav_demo": "student_demo",
        "priya": "priya_demo",
        "priya_patel": "priya_demo",
        "rohan": "rohan_demo",
        "rohan_verma": "rohan_demo",
        "ananya": "ananya_demo",
        "ananya_iyer": "ananya_demo",
        "vikram": "vikram_demo",
        "vikram_singh": "vikram_demo",
        "sneha": "sneha_demo",
        "sneha_kulkarni": "sneha_demo",
        "faculty": "faculty_demo",
        "sunita": "faculty_demo",
        "dr_sunita": "faculty_demo",
    }
    canonical = alias_map.get(raw, raw)
    conn = get_connection(db_path)
    user = conn.execute("SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(username) = ?", (raw, canonical)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieve user record by user ID."""
    conn = get_connection(db_path)
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def get_student_profile_by_user_id(user_id: int, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieve student profile with cohort details for a given user ID."""
    conn = get_connection(db_path)
    profile = conn.execute("""
        SELECT sp.*, u.full_name, u.email, u.username, c.name as cohort_name
        FROM student_profiles sp
        JOIN users u ON sp.user_id = u.id
        JOIN cohorts c ON sp.cohort_id = c.id
        WHERE sp.user_id = ?
    """, (user_id,)).fetchone()
    conn.close()
    return profile


def get_student_profile_by_id(student_id: int, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieve student profile with user and cohort details by student profile ID."""
    conn = get_connection(db_path)
    profile = conn.execute("""
        SELECT sp.*, u.full_name, u.email, u.username, c.name as cohort_name
        FROM student_profiles sp
        JOIN users u ON sp.user_id = u.id
        JOIN cohorts c ON sp.cohort_id = c.id
        WHERE sp.id = ?
    """, (student_id,)).fetchone()
    conn.close()
    return profile


def get_faculty_cohorts(faculty_user_id: int, db_path: Optional[str] = None) -> list:
    """Get list of cohorts assigned to a faculty member."""
    conn = get_connection(db_path)
    cohorts = conn.execute("""
        SELECT c.*
        FROM cohorts c
        JOIN faculty_cohorts fc ON c.id = fc.cohort_id
        WHERE fc.user_id = ?
        ORDER BY c.name
    """, (faculty_user_id,)).fetchall()
    conn.close()
    return cohorts


def faculty_can_access_student(faculty_user_id: int, student_id: int, db_path: Optional[str] = None) -> bool:
    """Verify that a faculty member is assigned to the cohort the student belongs to."""
    conn = get_connection(db_path)
    row = conn.execute("""
        SELECT 1
        FROM student_profiles sp
        JOIN faculty_cohorts fc ON sp.cohort_id = fc.cohort_id
        WHERE sp.id = ? AND fc.user_id = ?
    """, (student_id, faculty_user_id)).fetchone()
    conn.close()
    return row is not None


def get_cohort_students(cohort_id: int, db_path: Optional[str] = None) -> list:
    """Get all students belonging to a cohort."""
    conn = get_connection(db_path)
    students = conn.execute("""
        SELECT sp.*, u.full_name, u.email, u.username
        FROM student_profiles sp
        JOIN users u ON sp.user_id = u.id
        WHERE sp.cohort_id = ?
        ORDER BY sp.roll_number
    """, (cohort_id,)).fetchall()
    conn.close()
    return students


def get_student_attendance_records(student_id: int, db_path: Optional[str] = None) -> list:
    """Get all subject attendance records for a student."""
    conn = get_connection(db_path)
    records = conn.execute("""
        SELECT a.*, s.name as subject_name, s.code as subject_code
        FROM attendance a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.student_id = ?
        ORDER BY s.name
    """, (student_id,)).fetchall()
    conn.close()
    return records


def get_student_attendance_summary(student_id: int, db_path: Optional[str] = None) -> dict:
    """Calculate overall attendance percentage and per-subject details."""
    records = get_student_attendance_records(student_id, db_path)
    total_classes = sum(r["total_classes"] for r in records)
    attended_classes = sum(r["attended_classes"] for r in records)
    percentage = round((attended_classes / total_classes * 100), 1) if total_classes > 0 else 0.0

    return {
        "records": records,
        "total_classes": total_classes,
        "attended_classes": attended_classes,
        "overall_percentage": percentage,
    }


def get_student_marks_summary(student_id: int, db_path: Optional[str] = None) -> dict:
    """Calculate overall average marks, subject averages, and list recent assessments."""
    conn = get_connection(db_path)
    # Recent assessments
    recent = conn.execute("""
        SELECT am.*, s.name as subject_name, s.code as subject_code
        FROM assessment_marks am
        JOIN subjects s ON am.subject_id = s.id
        WHERE am.student_id = ?
        ORDER BY am.date_recorded DESC, am.id DESC
    """, (student_id,)).fetchall()

    # Subject-wise average percentage
    subject_stats = conn.execute("""
        SELECT s.id as subject_id, s.name as subject_name, s.code as subject_code,
               COUNT(am.id) as assessment_count,
               AVG(am.score * 100.0 / am.max_score) as avg_score_pct
        FROM subjects s
        JOIN student_profiles sp ON sp.cohort_id = s.cohort_id
        LEFT JOIN assessment_marks am ON am.subject_id = s.id AND am.student_id = sp.id
        WHERE sp.id = ?
        GROUP BY s.id, s.name, s.code
        ORDER BY s.name
    """, (student_id,)).fetchall()

    conn.close()

    overall_scores = [r["score"] * 100.0 / r["max_score"] for r in recent]
    overall_avg = round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else 0.0

    return {
        "recent_assessments": recent,
        "subject_stats": subject_stats,
        "overall_average": overall_avg,
    }


def get_student_goals(student_id: int, db_path: Optional[str] = None) -> list:
    """Get all study goals for a student."""
    conn = get_connection(db_path)
    goals = conn.execute("""
        SELECT * FROM study_goals
        WHERE student_id = ?
        ORDER BY is_completed ASC, created_at DESC
    """, (student_id,)).fetchall()
    conn.close()
    return goals


def get_student_tasks(student_id: int, db_path: Optional[str] = None) -> list:
    """Get weekly study planner tasks for a student."""
    conn = get_connection(db_path)
    tasks = conn.execute("""
        SELECT st.*, s.name as subject_name, s.code as subject_code
        FROM study_tasks st
        LEFT JOIN subjects s ON st.subject_id = s.id
        WHERE st.student_id = ?
        ORDER BY
            CASE st.day_of_week
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
                ELSE 8
            END,
            st.start_time ASC
    """, (student_id,)).fetchall()
    conn.close()
    return tasks


def get_student_snapshots(student_id: int, db_path: Optional[str] = None) -> list:
    """Get all historical progress snapshots for a student."""
    conn = get_connection(db_path)
    snapshots = conn.execute("""
        SELECT * FROM progress_snapshots
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (student_id,)).fetchall()
    conn.close()
    return snapshots


def get_student_interventions(student_id: int, db_path: Optional[str] = None) -> list:
    """Get all faculty interventions recorded for a student."""
    conn = get_connection(db_path)
    interventions = conn.execute("""
        SELECT fi.*, u.full_name as faculty_name
        FROM faculty_interventions fi
        JOIN users u ON fi.faculty_id = u.id
        WHERE fi.student_id = ?
        ORDER BY fi.created_at DESC
    """, (student_id,)).fetchall()
    conn.close()
    return interventions
