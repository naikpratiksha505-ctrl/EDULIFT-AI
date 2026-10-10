"""
EduLift AI - Flask Application & Security Tests
Tests end-to-end user workflows, route protections, role permissions,
data isolation, input validation, and goal/snapshot/intervention persistence.
"""

import os
import unittest
import tempfile
from app import app
import database as db
from seed_data import seed_database
from werkzeug.security import check_password_hash


class TestFlaskApplication(unittest.TestCase):
    def setUp(self):
        # Configure test environment
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

        # Seed temporary database
        seed_database(self.temp_db_path)

        # Set environment override
        os.environ["DATABASE_PATH"] = self.temp_db_path
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key-123"
        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except PermissionError:
                pass

    # 1. Health Check
    def test_health_check_endpoint(self):
        """Verify /health endpoint returns 200 with database and model status."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["database_connected"])

    # 2. Authentication & Password Hashing
    def test_password_hashing(self):
        """Verify demo passwords are stored as secure hashes, not plain text."""
        student_user = db.get_user_by_username("student_demo", self.temp_db_path)
        self.assertNotEqual(student_user["password_hash"], "Password123!")
        self.assertTrue(check_password_hash(student_user["password_hash"], "Password123!"))

    def test_login_success_student(self):
        """Verify successful student login redirects to student dashboard."""
        response = self.client.post("/login", data={
            "username": "student_demo",
            "password": "Password123!"
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/student", response.headers["Location"])

    def test_login_success_faculty(self):
        """Verify successful faculty login redirects to faculty dashboard."""
        response = self.client.post("/login", data={
            "username": "faculty_demo",
            "password": "Password123!"
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/faculty", response.headers["Location"])

    def test_login_invalid_password(self):
        """Verify invalid password returns error status and remains on login."""
        response = self.client.post("/login", data={
            "username": "student_demo",
            "password": "WrongPassword!"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid username or password", response.data)

    def test_logout(self):
        """Verify logout clears session and redirects to landing."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
            sess["role"] = "student"

        response = self.client.get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")

        with self.client.session_transaction() as sess:
            self.assertNotIn("user_id", sess)

    # 3. Route Protection & Role Permissions
    def test_unauthenticated_access_redirects(self):
        """Verify unauthenticated users cannot access student or faculty dashboards."""
        res_student = self.client.get("/student", follow_redirects=False)
        self.assertEqual(res_student.status_code, 302)
        self.assertIn("/login", res_student.headers["Location"])

        res_faculty = self.client.get("/faculty", follow_redirects=False)
        self.assertEqual(res_faculty.status_code, 302)
        self.assertIn("/login", res_faculty.headers["Location"])

    def test_student_cannot_access_faculty_routes(self):
        """Verify student cannot access faculty dashboard."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
            sess["username"] = "student_demo"
            sess["role"] = "student"
            sess["full_name"] = "Aarav Sharma"

        res = self.client.get("/faculty", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/student", res.headers["Location"])

    def test_faculty_cannot_access_student_routes(self):
        """Verify faculty cannot access student dashboard."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "faculty_demo"
            sess["role"] = "faculty"
            sess["full_name"] = "Dr. Sunita Rao"

        res = self.client.get("/student", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/faculty", res.headers["Location"])

    # 4. Student Features (Goal creation, toggle, snapshot)
    def test_student_goal_creation_and_toggle(self):
        """Verify student can create and toggle their study goal."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
            sess["username"] = "student_demo"
            sess["role"] = "student"
            sess["full_name"] = "Aarav Sharma"

        # Create Goal
        res_create = self.client.post("/student/goals/create", data={
            "title": "Solve 10 Calculus Integrals",
            "target_date": "2026-10-15"
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)

        # Check in DB
        goals = db.get_student_goals(1, self.temp_db_path)
        matching = [g for g in goals if g["title"] == "Solve 10 Calculus Integrals"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["is_completed"], 0)

        # Toggle Goal
        goal_id = matching[0]["id"]
        res_toggle = self.client.post(f"/student/goals/{goal_id}/toggle", follow_redirects=True)
        self.assertEqual(res_toggle.status_code, 200)

        # Verify updated
        updated_goals = db.get_student_goals(1, self.temp_db_path)
        updated_match = [g for g in updated_goals if g["id"] == goal_id][0]
        self.assertEqual(updated_match["is_completed"], 1)

    def test_student_progress_snapshot(self):
        """Verify student can take an official progress snapshot."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
            sess["username"] = "student_demo"
            sess["role"] = "student"
            sess["full_name"] = "Aarav Sharma"

        res = self.client.post("/student/snapshot", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        snapshots = db.get_student_snapshots(1, self.temp_db_path)
        user_captured = [s for s in snapshots if s["is_seed"] == 0]
        self.assertGreater(len(user_captured), 0)
        self.assertGreater(user_captured[0]["attendance_pct"], 0)

    # 5. Faculty Permissions & Validation (Attendance & Assessment)
    def test_faculty_attendance_validation(self):
        """Verify attendance validation rejects attended > total."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "faculty_demo"
            sess["role"] = "faculty"
            sess["full_name"] = "Dr. Sunita Rao"

        # Try invalid attendance (attended 50 out of 40)
        res = self.client.post("/faculty/student/1/attendance/update", data={
            "subject_id": 1,
            "attended_classes": 50,
            "total_classes": 40,
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Attended classes must be between 0 and total classes", res.data)

    def test_faculty_assessment_score_validation(self):
        """Verify assessment validation rejects score > max_score."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "faculty_demo"
            sess["role"] = "faculty"
            sess["full_name"] = "Dr. Sunita Rao"

        res = self.client.post("/faculty/student/1/assessment/add", data={
            "subject_id": 1,
            "assessment_name": "Invalid Test",
            "score": 150,
            "max_score": 100,
            "date_recorded": "2026-10-09"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"valid assessment name and score within range", res.data)

    def test_faculty_intervention_creation_and_update(self):
        """Verify faculty can create and update student interventions."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "faculty_demo"
            sess["role"] = "faculty"
            sess["full_name"] = "Dr. Sunita Rao"

        # Create intervention
        res_create = self.client.post("/faculty/student/1/intervention/add", data={
            "indicator_reason": "Low attendance in Math lectures",
            "suggested_action": "Peer mentor assigned for weekly review",
            "faculty_notes": "Aarav agreed to attend tutorial sessions",
            "follow_up_date": "2026-10-20",
            "status": "In progress"
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)
        self.assertIn(b"Supportive intervention recorded successfully", res_create.data)

        # Verify in DB
        invs = db.get_student_interventions(1, self.temp_db_path)
        matching = [i for i in invs if i["indicator_reason"] == "Low attendance in Math lectures"]
        self.assertEqual(len(matching), 1)

        # Update intervention
        inv_id = matching[0]["id"]
        res_update = self.client.post(f"/faculty/intervention/{inv_id}/update", data={
            "student_id": 1,
            "status": "Completed",
            "follow_up_date": "2026-10-20",
            "outcome_notes": "Student attended all tutorials and improved attendance."
        }, follow_redirects=True)
        self.assertEqual(res_update.status_code, 200)

        # Verify update persisted
        updated_invs = db.get_student_interventions(1, self.temp_db_path)
        updated_item = [i for i in updated_invs if i["id"] == inv_id][0]
        self.assertEqual(updated_item["status"], "Completed")
        self.assertEqual(updated_item["outcome_notes"], "Student attended all tutorials and improved attendance.")


if __name__ == "__main__":
    unittest.main()
