"""
EduLift AI - Main Flask Application
An AI-Powered Student Analytics & Success Platform for First-Year B.Tech AIML.
Provides role-protected portals for students and faculty with rule-based recommendations,
interactive study planner, and scikit-learn ML demonstration.
"""

import os
import json
from datetime import date
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    abort,
)
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Import internal modules
import database as db
from recommendations import analyze_student_academic_health
from planner import generate_study_schedule
from ml.predict import predict_student_support, MODEL_PATH

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "edulift-dev-secret-key-2026")
app.config["TEMPLATES_AUTO_RELOAD"] = True


# -------------------------------------------------------------
# Authentication & Authorization Decorators
# -------------------------------------------------------------

def login_required(f):
    """Ensure user is authenticated in the current session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role: str):
    """Enforce that the logged-in user matches the specified role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please sign in to access this page.", "warning")
                return redirect(url_for("login"))
            if session.get("role") != required_role:
                flash("Access denied: You do not have permission for that section.", "danger")
                if session.get("role") == "student":
                    return redirect(url_for("student_dashboard"))
                return redirect(url_for("faculty_dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# -------------------------------------------------------------
# Public & Authentication Routes
# -------------------------------------------------------------

@app.route("/")
def landing():
    """Professional landing page showcasing EduLift AI."""
    if "user_id" in session:
        if session.get("role") == "student":
            return redirect(url_for("student_dashboard"))
        return redirect(url_for("faculty_dashboard"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user sign in for students and faculty."""
    if "user_id" in session:
        if session.get("role") == "student":
            return redirect(url_for("student_dashboard"))
        return redirect(url_for("faculty_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.", "warning")
            return render_template("login.html"), 400

        user = db.get_user_by_username(username)

        if user and check_password_hash(user["password_hash"], password):
            # Store necessary session data
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]

            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] == "student":
                return redirect(url_for("student_dashboard"))
            return redirect(url_for("faculty_dashboard"))
        else:
            flash("Invalid username or password. Please verify credentials.", "danger")
            return render_template("login.html"), 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Sign out the current user and clear session."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("landing"))


@app.route("/health")
def health_check():
    """Application health check endpoint for monitoring."""
    db_ok = False
    try:
        conn = db.get_connection()
        conn.execute("SELECT 1").fetchone()
        conn.close()
        db_ok = True
    except Exception:
        db_ok = False

    model_ok = os.path.exists(MODEL_PATH)

    status = "healthy" if db_ok else "unhealthy"
    return jsonify({
        "status": status,
        "database_connected": db_ok,
        "ml_model_present": model_ok,
        "app": "EduLift AI",
        "version": "1.0.0",
    }), (200 if db_ok else 503)


# -------------------------------------------------------------
# Student Routes
# -------------------------------------------------------------

@app.route("/student")
@login_required
@role_required("student")
def student_dashboard():
    """Student academic dashboard showing stats, charts, AI recommendations, and goals."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    if not profile:
        flash("Student profile not found. Please contact administration.", "danger")
        return redirect(url_for("logout"))

    student_id = profile["id"]

    # 1. Academic Summaries
    att_summary = db.get_student_attendance_summary(student_id)
    marks_summary = db.get_student_marks_summary(student_id)

    # 2. Rule-Based Academic Recommendations
    rec_analysis = analyze_student_academic_health(att_summary, marks_summary)

    # 3. Machine Learning Demonstration Prediction
    # Calculate trend from recent 2 assessments
    recent = marks_summary["recent_assessments"]
    recent_trend = 0.0
    if len(recent) >= 2:
        recent_trend = (recent[0]["score"] * 100.0 / recent[0]["max_score"]) - (recent[1]["score"] * 100.0 / recent[1]["max_score"])

    # Compute assignment/quiz completion rate estimate based on records
    assgn_rate = min(100.0, max(50.0, att_summary["overall_percentage"] * 1.05))

    ml_prediction = predict_student_support(
        attendance_pct=att_summary["overall_percentage"],
        previous_marks_avg=marks_summary["overall_average"],
        assignment_completion_rate=assgn_rate,
        recent_trend=round(recent_trend, 1),
    )

    # 4. Prepare Chart.js chronological assessment marks data
    chronological = list(reversed(recent))
    chart_labels = [f"{m['subject_code']}: {m['assessment_name']}" for m in chronological]
    chart_scores = [round(m["score"] * 100.0 / m["max_score"], 1) for m in chronological]

    marks_chart_json = json.dumps({
        "labels": chart_labels,
        "scores": chart_scores,
    })

    # 5. Combined Subject Rows (merging attendance and score stats)
    att_map = {r["subject_id"]: r for r in att_summary["records"]}
    subject_rows = []
    for stat in marks_summary["subject_stats"]:
        sub_id = stat["subject_id"]
        att_rec = att_map.get(sub_id)
        attended = att_rec["attended_classes"] if att_rec else 0
        total = att_rec["total_classes"] if att_rec else 0
        att_pct = round(attended * 100.0 / total, 1) if total > 0 else 0.0
        avg_score = round(stat["avg_score_pct"], 1) if stat["avg_score_pct"] is not None else None

        subject_rows.append({
            "name": stat["subject_name"],
            "code": stat["subject_code"],
            "attended": attended,
            "total": total,
            "att_pct": att_pct,
            "avg_score": avg_score,
        })

    # 6. Study Goals & Snapshots
    goals = db.get_student_goals(student_id)
    completed_goals = sum(1 for g in goals if g["is_completed"])
    pending_goals = len(goals) - completed_goals
    snapshots = db.get_student_snapshots(student_id)

    return render_template(
        "student_dashboard.html",
        active_page="student_dashboard",
        profile=profile,
        attendance_summary=att_summary,
        marks_summary=marks_summary,
        rec_analysis=rec_analysis,
        ml_prediction=ml_prediction,
        marks_chart_json=marks_chart_json,
        subject_rows=subject_rows,
        goals=goals,
        completed_goals_count=completed_goals,
        pending_goals_count=pending_goals,
        total_goals_count=len(goals),
        snapshots=snapshots,
    )


@app.route("/student/goals/create", methods=["POST"])
@login_required
@role_required("student")
def create_goal():
    """Create a new study goal for the logged-in student."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    title = request.form.get("title", "").strip()
    target_date = request.form.get("target_date", "").strip() or None

    if not title:
        flash("Goal title cannot be empty.", "warning")
        return redirect(url_for("student_dashboard"))

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO study_goals (student_id, title, target_date, is_completed)
        VALUES (?, ?, ?, 0)
    """, (profile["id"], title, target_date))
    conn.commit()
    conn.close()

    flash("New study goal added successfully!", "success")
    return redirect(url_for("student_dashboard"))


@app.route("/student/goals/<int:goal_id>/toggle", methods=["POST"])
@login_required
@role_required("student")
def toggle_goal(goal_id: int):
    """Toggle a goal's completion status with ownership check."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    conn = db.get_connection()
    goal = conn.execute("SELECT * FROM study_goals WHERE id = ? AND student_id = ?", (goal_id, profile["id"])).fetchone()

    if not goal:
        conn.close()
        flash("Goal not found or unauthorized.", "danger")
        return redirect(url_for("student_dashboard"))

    new_status = 0 if goal["is_completed"] == 1 else 1
    conn.execute("UPDATE study_goals SET is_completed = ? WHERE id = ?", (new_status, goal_id))
    conn.commit()
    conn.close()

    flash("Goal updated!", "info")
    return redirect(url_for("student_dashboard"))


@app.route("/student/snapshot", methods=["POST"])
@login_required
@role_required("student")
def create_snapshot():
    """Record an official point-in-time progress snapshot."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    student_id = profile["id"]

    att_summary = db.get_student_attendance_summary(student_id)
    marks_summary = db.get_student_marks_summary(student_id)
    goals = db.get_student_goals(student_id)

    completed_g = sum(1 for g in goals if g["is_completed"])
    pending_g = len(goals) - completed_g

    breakdown = {s["subject_name"]: round(s["avg_score_pct"], 1) if s["avg_score_pct"] else None for s in marks_summary["subject_stats"]}

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO progress_snapshots (student_id, attendance_pct, avg_marks, completed_goals, pending_goals, subject_breakdown_json, is_seed)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        student_id,
        att_summary["overall_percentage"],
        marks_summary["overall_average"],
        completed_g,
        pending_g,
        json.dumps(breakdown),
    ))
    conn.commit()
    conn.close()

    flash("Current progress snapshot captured successfully!", "success")
    return redirect(url_for("student_dashboard"))


@app.route("/student/study-planner")
@login_required
@role_required("student")
def study_planner():
    """Weekly study planner view."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    tasks = db.get_student_tasks(profile["id"])

    conn = db.get_connection()
    subjects = conn.execute("SELECT * FROM subjects WHERE cohort_id = ? ORDER BY name", (profile["cohort_id"],)).fetchall()
    conn.close()

    return render_template(
        "study_planner.html",
        active_page="study_planner",
        profile=profile,
        tasks=tasks,
        subjects=subjects,
    )


@app.route("/student/study-planner/generate", methods=["POST"])
@login_required
@role_required("student")
def generate_schedule():
    """Generate suggested weekly timetable using simple Python logic."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    student_id = profile["id"]

    try:
        hours = float(request.form.get("available_hours", 8))
    except ValueError:
        hours = 8.0

    priority_sub_id = request.form.get("priority_subject_id", "")
    priority_sub_id = int(priority_sub_id) if priority_sub_id.isdigit() else None

    conn = db.get_connection()
    subjects = [dict(s) for s in conn.execute("SELECT * FROM subjects WHERE cohort_id = ? ORDER BY name", (profile["cohort_id"],)).fetchall()]

    upcoming = []
    if priority_sub_id:
        upcoming.append({"subject_id": priority_sub_id})

    suggested = generate_study_schedule(subjects, hours, upcoming)

    # Insert suggested tasks
    for task in suggested:
        conn.execute("""
            INSERT INTO study_tasks (student_id, subject_id, title, day_of_week, start_time, duration_minutes, priority, is_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            student_id,
            task["subject_id"],
            task["title"],
            task["day_of_week"],
            task["start_time"],
            task["duration_minutes"],
            task["priority"],
        ))

    conn.commit()
    conn.close()

    flash(f"Generated {len(suggested)} study sessions for your weekly planner!", "success")
    return redirect(url_for("study_planner"))


@app.route("/student/study-planner/task/create", methods=["POST"])
@login_required
@role_required("student")
def create_task():
    """Create a manual study task."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    title = request.form.get("title", "").strip()
    sub_id = request.form.get("subject_id", "")
    sub_id = int(sub_id) if sub_id.isdigit() else None
    day = request.form.get("day_of_week", "Monday")
    start_time = request.form.get("start_time", "18:00")
    priority = request.form.get("priority", "Medium")

    try:
        duration = int(request.form.get("duration_minutes", 45))
    except ValueError:
        duration = 45

    if not title:
        flash("Task title cannot be empty.", "warning")
        return redirect(url_for("study_planner"))

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO study_tasks (student_id, subject_id, title, day_of_week, start_time, duration_minutes, priority, is_completed)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    """, (profile["id"], sub_id, title, day, start_time, duration, priority))
    conn.commit()
    conn.close()

    flash("Study task scheduled!", "success")
    return redirect(url_for("study_planner"))


@app.route("/student/study-planner/task/<int:task_id>/toggle", methods=["POST"])
@login_required
@role_required("student")
def toggle_task(task_id: int):
    """Toggle completion status for a study task."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    conn = db.get_connection()
    task = conn.execute("SELECT * FROM study_tasks WHERE id = ? AND student_id = ?", (task_id, profile["id"])).fetchone()

    if not task:
        conn.close()
        flash("Task not found or unauthorized.", "danger")
        return redirect(url_for("study_planner"))

    new_val = 0 if task["is_completed"] == 1 else 1
    conn.execute("UPDATE study_tasks SET is_completed = ? WHERE id = ?", (new_val, task_id))
    conn.commit()
    conn.close()

    return redirect(url_for("study_planner"))


@app.route("/student/study-planner/task/<int:task_id>/delete", methods=["POST"])
@login_required
@role_required("student")
def delete_task(task_id: int):
    """Delete a study task with student ownership check."""
    profile = db.get_student_profile_by_user_id(session["user_id"])
    conn = db.get_connection()
    conn.execute("DELETE FROM study_tasks WHERE id = ? AND student_id = ?", (task_id, profile["id"]))
    conn.commit()
    conn.close()

    flash("Task removed from schedule.", "info")
    return redirect(url_for("study_planner"))


# -------------------------------------------------------------
# Faculty Routes
# -------------------------------------------------------------

@app.route("/faculty")
@login_required
@role_required("faculty")
def faculty_dashboard():
    """Faculty cohort overview dashboard."""
    faculty_user = db.get_user_by_id(session["user_id"])
    cohorts = db.get_faculty_cohorts(session["user_id"])

    if not cohorts:
        flash("No assigned cohorts found for your faculty account.", "warning")
        return render_template("faculty_dashboard.html", active_page="faculty_dashboard", cohort=None, total_students=0)

    # Use first assigned cohort for primary view
    cohort = cohorts[0]
    students = db.get_cohort_students(cohort["id"])

    # Compute aggregate metrics across cohort
    student_roster = []
    support_alerts = []
    total_att_sum = 0.0
    total_marks_sum = 0.0

    for s in students:
        sid = s["id"]
        att = db.get_student_attendance_summary(sid)
        marks = db.get_student_marks_summary(sid)
        rec_data = analyze_student_academic_health(att, marks)

        att_pct = att["overall_percentage"]
        avg_m = marks["overall_average"]

        total_att_sum += att_pct
        total_marks_sum += avg_m

        has_support_flag = rec_data["indicator_count"] > 0
        if has_support_flag:
            reasons = rec_data["indicators"]
            primary_reason = reasons[0] if reasons else "Attendance or marks below recommended guidelines"
            support_alerts.append({
                "student_id": sid,
                "student_name": s["full_name"],
                "roll_number": s["roll_number"],
                "supportive_message": f"This student may benefit from a check-in because {primary_reason.lower()}.",
                "reason": "; ".join(reasons),
            })

        student_roster.append({
            "student_id": sid,
            "roll_number": s["roll_number"],
            "full_name": s["full_name"],
            "attendance_pct": att_pct,
            "avg_marks": avg_m,
            "support_flag": has_support_flag,
        })

    num_students = len(students)
    cohort_avg_att = round(total_att_sum / num_students, 1) if num_students > 0 else 0.0
    cohort_avg_marks = round(total_marks_sum / num_students, 1) if num_students > 0 else 0.0

    # Cohort Subject Averages for Chart.js
    conn = db.get_connection()
    sub_rows = conn.execute("""
        SELECT s.name as subject_name,
               AVG(am.score * 100.0 / am.max_score) as avg_score
        FROM subjects s
        LEFT JOIN assessment_marks am ON am.subject_id = s.id
        WHERE s.cohort_id = ?
        GROUP BY s.id, s.name
        ORDER BY s.name
    """, (cohort["id"],)).fetchall()

    cohort_interventions = conn.execute("""
        SELECT fi.*, u.full_name as student_name, sp.roll_number
        FROM faculty_interventions fi
        JOIN student_profiles sp ON fi.student_id = sp.id
        JOIN users u ON sp.user_id = u.id
        WHERE sp.cohort_id = ?
        ORDER BY fi.created_at DESC
    """, (cohort["id"],)).fetchall()
    conn.close()

    cohort_chart_json = json.dumps({
        "labels": [r["subject_name"] for r in sub_rows],
        "averages": [round(r["avg_score"], 1) if r["avg_score"] is not None else 0.0 for r in sub_rows],
    })

    active_interventions = sum(1 for i in cohort_interventions if i["status"] in ("Planned", "In progress"))

    # Load ML metrics for preview card
    metrics_path = os.path.join(os.path.dirname(__file__), "ml", "model_metrics.json")
    ml_metrics = None
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r") as f:
                ml_metrics = json.load(f)
        except Exception:
            ml_metrics = None

    return render_template(
        "faculty_dashboard.html",
        active_page="faculty_dashboard",
        faculty_user=faculty_user,
        cohort=cohort,
        total_students=num_students,
        cohort_avg_attendance=cohort_avg_att,
        cohort_avg_marks=cohort_avg_marks,
        student_roster=student_roster,
        support_alerts=support_alerts,
        cohort_chart_json=cohort_chart_json,
        cohort_interventions=cohort_interventions,
        active_interventions_count=active_interventions,
        ml_metrics=ml_metrics,
    )


@app.route("/faculty/student/<int:student_id>")
@login_required
@role_required("faculty")
def faculty_student_detail(student_id: int):
    """Detailed student academic & intervention profile for authorized faculty."""
    # Enforce strict cohort-based authorization
    if not db.faculty_can_access_student(session["user_id"], student_id):
        abort(403, description="Access forbidden: This student is not in your assigned cohort.")

    student = db.get_student_profile_by_id(student_id)
    if not student:
        abort(404, description="Student profile not found.")

    att_summary = db.get_student_attendance_summary(student_id)
    marks_summary = db.get_student_marks_summary(student_id)
    rec_analysis = analyze_student_academic_health(att_summary, marks_summary)
    interventions = db.get_student_interventions(student_id)
    snapshots = db.get_student_snapshots(student_id)

    conn = db.get_connection()
    subjects = conn.execute("SELECT * FROM subjects WHERE cohort_id = ? ORDER BY name", (student["cohort_id"],)).fetchall()
    conn.close()

    # ML prediction for student
    recent = marks_summary["recent_assessments"]
    recent_trend = 0.0
    if len(recent) >= 2:
        recent_trend = (recent[0]["score"] * 100.0 / recent[0]["max_score"]) - (recent[1]["score"] * 100.0 / recent[1]["max_score"])
    assgn_rate = min(100.0, max(50.0, att_summary["overall_percentage"] * 1.05))

    ml_prediction = predict_student_support(
        attendance_pct=att_summary["overall_percentage"],
        previous_marks_avg=marks_summary["overall_average"],
        assignment_completion_rate=assgn_rate,
        recent_trend=round(recent_trend, 1),
    )

    return render_template(
        "student_detail.html",
        active_page="faculty_dashboard",
        student=student,
        attendance_summary=att_summary,
        marks_summary=marks_summary,
        rec_analysis=rec_analysis,
        interventions=interventions,
        snapshots=snapshots,
        subjects=subjects,
        ml_prediction=ml_prediction,
        today_str=date.today().isoformat(),
    )


@app.route("/faculty/student/<int:student_id>/attendance/update", methods=["POST"])
@login_required
@role_required("faculty")
def faculty_update_attendance(student_id: int):
    """Update authorized attendance entries."""
    if not db.faculty_can_access_student(session["user_id"], student_id):
        abort(403)

    try:
        subject_id = int(request.form.get("subject_id"))
        attended = int(request.form.get("attended_classes"))
        total = int(request.form.get("total_classes"))
    except (ValueError, TypeError):
        flash("Invalid attendance numerical values.", "danger")
        return redirect(url_for("faculty_student_detail", student_id=student_id))

    if attended < 0 or total <= 0 or attended > total:
        flash("Attended classes must be between 0 and total classes.", "warning")
        return redirect(url_for("faculty_student_detail", student_id=student_id))

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO attendance (student_id, subject_id, total_classes, attended_classes, last_updated)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id, subject_id) DO UPDATE SET
            total_classes = excluded.total_classes,
            attended_classes = excluded.attended_classes,
            last_updated = excluded.last_updated
    """, (student_id, subject_id, total, attended, date.today().isoformat()))
    conn.commit()
    conn.close()

    flash("Attendance record updated successfully.", "success")
    return redirect(url_for("faculty_student_detail", student_id=student_id))


@app.route("/faculty/student/<int:student_id>/assessment/add", methods=["POST"])
@login_required
@role_required("faculty")
def faculty_add_assessment(student_id: int):
    """Record an assessment score for an authorized student."""
    if not db.faculty_can_access_student(session["user_id"], student_id):
        abort(403)

    try:
        subject_id = int(request.form.get("subject_id"))
        score = float(request.form.get("score"))
        max_score = float(request.form.get("max_score", 100))
    except (ValueError, TypeError):
        flash("Invalid score entered.", "danger")
        return redirect(url_for("faculty_student_detail", student_id=student_id))

    name = request.form.get("assessment_name", "").strip()
    date_rec = request.form.get("date_recorded", "").strip() or date.today().isoformat()

    if not name or score < 0 or max_score <= 0 or score > max_score:
        flash("Please provide a valid assessment name and score within range.", "warning")
        return redirect(url_for("faculty_student_detail", student_id=student_id))

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO assessment_marks (student_id, subject_id, assessment_name, score, max_score, date_recorded)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, subject_id, name, score, max_score, date_rec))
    conn.commit()
    conn.close()

    flash("Assessment result recorded successfully.", "success")
    return redirect(url_for("faculty_student_detail", student_id=student_id))


@app.route("/faculty/student/<int:student_id>/intervention/add", methods=["POST"])
@login_required
@role_required("faculty")
def faculty_add_intervention(student_id: int):
    """Add a supportive intervention / check-in plan for a student."""
    if not db.faculty_can_access_student(session["user_id"], student_id):
        abort(403)

    reason = request.form.get("indicator_reason", "").strip()
    action = request.form.get("suggested_action", "").strip()
    notes = request.form.get("faculty_notes", "").strip()
    follow_up = request.form.get("follow_up_date", "").strip() or None
    status = request.form.get("status", "Planned")

    if not reason or not action:
        flash("Both indicator reason and suggested action are required.", "warning")
        return redirect(url_for("faculty_student_detail", student_id=student_id))

    if status not in ("Planned", "In progress", "Completed", "Dismissed"):
        status = "Planned"

    conn = db.get_connection()
    conn.execute("""
        INSERT INTO faculty_interventions
        (student_id, faculty_id, indicator_reason, suggested_action, faculty_notes, follow_up_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_id, session["user_id"], reason, action, notes, follow_up, status))
    conn.commit()
    conn.close()

    flash("Supportive intervention recorded successfully.", "success")
    return redirect(url_for("faculty_student_detail", student_id=student_id))


@app.route("/faculty/intervention/<int:intervention_id>/update", methods=["POST"])
@login_required
@role_required("faculty")
def faculty_update_intervention(intervention_id: int):
    """Update status, follow-up date, or outcome notes of an existing intervention."""
    student_id = request.form.get("student_id")
    status = request.form.get("status", "Planned")
    follow_up = request.form.get("follow_up_date", "").strip() or None
    outcome_notes = request.form.get("outcome_notes", "").strip() or None

    if status not in ("Planned", "In progress", "Completed", "Dismissed"):
        status = "Planned"

    conn = db.get_connection()
    inv = conn.execute("SELECT * FROM faculty_interventions WHERE id = ?", (intervention_id,)).fetchone()

    if not inv or not db.faculty_can_access_student(session["user_id"], inv["student_id"]):
        conn.close()
        abort(403)

    conn.execute("""
        UPDATE faculty_interventions
        SET status = ?, follow_up_date = ?, outcome_notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, follow_up, outcome_notes, intervention_id))
    conn.commit()
    conn.close()

    flash("Intervention status updated.", "info")
    target_sid = student_id if student_id else inv["student_id"]
    return redirect(url_for("faculty_student_detail", student_id=target_sid))


# -------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------

@app.errorhandler(403)
def forbidden_error(error):
    return render_template("base.html", content=f"<div class='alert alert-danger'><h3>403 Forbidden</h3><p>{error.description or 'You do not have permission to view this resource.'}</p><a href='/' class='btn btn-outline'>Return Home</a></div>"), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template("base.html", content=f"<div class='alert alert-warning'><h3>404 Not Found</h3><p>{error.description or 'The requested resource was not found.'}</p><a href='/' class='btn btn-outline'>Return Home</a></div>"), 404


# -------------------------------------------------------------
# Main Application Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":
    # Ensure database initialized on startup
    db.init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting EduLift AI application on http://0.0.0.0:{port} (Local: http://localhost:{port})")
    app.run(host="0.0.0.0", port=port, debug=False)
