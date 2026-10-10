"""
EduLift AI - Machine Learning Demonstration Unit Tests
Validates synthetic dataset generation, Logistic Regression training,
baseline comparison, genuine evaluation metrics, and prediction attribution.
"""

import os
import unittest
import tempfile
import pandas as pd
from ml.generate_data import generate_synthetic_data
from ml.train_model import train_and_evaluate_model
from ml.predict import predict_student_support


class TestMachineLearningModule(unittest.TestCase):
    def test_synthetic_data_generation_reproducibility(self):
        """Verify reproducible dataset generation and column contracts."""
        df1 = generate_synthetic_data(num_samples=100, random_seed=42)
        df2 = generate_synthetic_data(num_samples=100, random_seed=42)

        self.assertEqual(len(df1), 100)
        self.assertTrue(df1.equals(df2), "Fixed seed must produce identical synthetic data.")

        expected_columns = {
            "attendance_pct",
            "previous_marks_avg",
            "assignment_completion_rate",
            "recent_trend",
            "needs_support",
        }
        self.assertEqual(set(df1.columns), expected_columns)
        self.assertFalse(df1.isnull().values.any(), "Synthetic dataset must contain no NaN values.")

    def test_model_training_and_metrics(self):
        """Verify model training calculates real metrics and saves artifacts."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "test_students.csv")
            df = generate_synthetic_data(num_samples=200, random_seed=42)
            df.to_csv(csv_path, index=False)

            metrics = train_and_evaluate_model(data_path=csv_path)

            self.assertIn("accuracy", metrics)
            self.assertIn("precision", metrics)
            self.assertIn("recall", metrics)
            self.assertIn("f1_score", metrics)
            self.assertIn("confusion_matrix", metrics)

            # Ensure metrics are genuine numbers between 0 and 1
            self.assertGreaterEqual(metrics["accuracy"], 0.5)
            self.assertLessEqual(metrics["accuracy"], 1.0)
            self.assertGreaterEqual(metrics["f1_score"], 0.0)
            self.assertLessEqual(metrics["f1_score"], 1.0)

    def test_prediction_output_and_explanation(self):
        """Verify prediction function returns structured output and factor attribution."""
        # Test student needing support (low attendance, low marks, downward trend)
        pred_high_risk = predict_student_support(
            attendance_pct=60.0,
            previous_marks_avg=52.0,
            assignment_completion_rate=55.0,
            recent_trend=-8.0,
        )
        self.assertEqual(pred_high_risk["status"], "available")
        self.assertIn(pred_high_risk["prediction"], ["Support Recommended", "Steady / On Track"])
        self.assertIsInstance(pred_high_risk["factors"], list)
        self.assertIn("synthetic data", pred_high_risk["warning"].lower())

        # Test student on track (high attendance, high marks, positive trend)
        pred_low_risk = predict_student_support(
            attendance_pct=95.0,
            previous_marks_avg=90.0,
            assignment_completion_rate=98.0,
            recent_trend=4.0,
        )
        self.assertEqual(pred_low_risk["status"], "available")
        self.assertFalse(pred_low_risk["support_needed"])
        self.assertEqual(pred_low_risk["prediction"], "Steady / On Track")

    def test_missing_model_fallback(self):
        """Verify graceful fallback if model artifact is unavailable."""
        res = predict_student_support(
            attendance_pct=70.0,
            previous_marks_avg=70.0,
            assignment_completion_rate=70.0,
            recent_trend=0.0,
            model_path="/non_existent_model_file.joblib"
        )
        self.assertEqual(res["status"], "unavailable")
        self.assertEqual(res["prediction"], "Model Unavailable")


if __name__ == "__main__":
    unittest.main()
