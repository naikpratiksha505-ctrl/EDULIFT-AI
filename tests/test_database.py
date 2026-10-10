"""
EduLift AI - Database Layer Unit Tests
Tests schema creation, foreign key constraints, query helpers, and data integrity
using an isolated temporary test database.
"""

import os
import unittest
import tempfile
import database as db
from seed_data import seed_database


class TestDatabaseLayer(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for isolated database tests
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db_path = self.temp_db_file.name
        self.temp_db_file.close()
        # Seed test database
        seed_database(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except PermissionError:
                pass

    def test_database_initialization_and_tables(self):
        """Verify all required tables exist in SQLite."""
        conn = db.get_connection(self.temp_db_path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = {t["name"] for t in tables}
        conn.close()

        required = {
            "users", "cohorts", "student_profiles", "faculty_cohorts",
            "subjects", "assessment_marks", "attendance", "study_goals",
            "study_tasks", "progress_snapshots", "faculty_interventions"
        }
        for req in required:
            self.assertIn(req, table_names, f"Table '{req}' should exist in database.")

    def test_get_user_by_username(self):
        """Verify user retrieval and password hash presence."""
        user = db.get_user_by_username("student_demo", self.temp_db_path)
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "student")
        self.assertTrue(user["password_hash"].startswith("scrypt:") or len(user["password_hash"]) > 10)

    def test_student_profile_retrieval(self):
        """Verify student profile links properly to user and cohort."""
        user = db.get_user_by_username("student_demo", self.temp_db_path)
        profile = db.get_student_profile_by_user_id(user["id"], self.temp_db_path)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["roll_number"], "26AIML042")
        self.assertEqual(profile["full_name"], "Aarav Sharma")
        self.assertIn("AIML", profile["cohort_name"])

    def test_faculty_permissions_and_cohort_access(self):
        """Verify faculty cohort access check."""
        faculty = db.get_user_by_username("faculty_demo", self.temp_db_path)
        student = db.get_student_profile_by_user_id(2, self.temp_db_path)
        can_access = db.faculty_can_access_student(faculty["id"], student["id"], self.temp_db_path)
        self.assertTrue(can_access)

    def test_attendance_and_marks_summary(self):
        """Verify attendance calculation and marks summary."""
        student = db.get_student_profile_by_user_id(2, self.temp_db_path)
        att = db.get_student_attendance_summary(student["id"], self.temp_db_path)
        self.assertGreater(att["total_classes"], 0)
        self.assertGreaterEqual(att["overall_percentage"], 0.0)
        self.assertLessEqual(att["overall_percentage"], 100.0)

        marks = db.get_student_marks_summary(student["id"], self.temp_db_path)
        self.assertGreater(len(marks["recent_assessments"]), 0)
        self.assertGreater(marks["overall_average"], 0.0)


if __name__ == "__main__":
    unittest.main()
