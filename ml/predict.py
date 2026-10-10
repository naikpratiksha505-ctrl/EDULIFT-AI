"""
EduLift AI - Machine Learning Demonstration: Prediction & Explanation
Loads trained model and generates predictions with factor impact breakdown.
Advisory warning included to ensure ethical AI demonstration.
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "student_model.joblib")

DEMO_WARNING = (
    "This demonstration uses synthetic data and is not validated for real students. "
    "Predictions are advisory and must not be used for disciplinary or high-stakes decisions."
)

_cached_artifacts = {}


def load_model_artifact(model_path: str = MODEL_PATH):
    """Load model artifact from disk, caching by model_path."""
    global _cached_artifacts
    if model_path in _cached_artifacts:
        return _cached_artifacts[model_path]

    if not os.path.exists(model_path):
        return None

    try:
        artifact = joblib.load(model_path)
        _cached_artifacts[model_path] = artifact
        return artifact
    except Exception as e:
        print(f"Error loading model artifact: {e}")
        return None


def predict_student_support(
    attendance_pct: float,
    previous_marks_avg: float,
    assignment_completion_rate: float,
    recent_trend: float,
    model_path: str = MODEL_PATH,
) -> Dict[str, Any]:
    """
    Produce an advisory prediction and factor contributions for a student.

    Returns a structured dictionary with:
    - status: 'available' or 'unavailable'
    - prediction: 'Support Recommended' or 'Steady / On Track'
    - support_needed: bool
    - probability_pct: float
    - factors: list of explanatory factor descriptions
    - warning: advisory notice
    """
    artifact = load_model_artifact(model_path)

    if artifact is None:
        return {
            "status": "unavailable",
            "prediction": "Model Unavailable",
            "support_needed": False,
            "probability_pct": 0.0,
            "factors": [
                "The trained ML model artifact was not found.",
                "To train the model, run: python ml/train_model.py in your terminal.",
            ],
            "metrics": None,
            "warning": DEMO_WARNING,
        }

    try:
        model = artifact["model"]
        scaler = artifact["scaler"]
        metrics = artifact.get("metrics", {})
        feature_cols = artifact.get("features", [
            "attendance_pct",
            "previous_marks_avg",
            "assignment_completion_rate",
            "recent_trend",
        ])

        # Create DataFrame with exact feature names matching training
        input_df = pd.DataFrame([{
            "attendance_pct": float(attendance_pct),
            "previous_marks_avg": float(previous_marks_avg),
            "assignment_completion_rate": float(assignment_completion_rate),
            "recent_trend": float(recent_trend),
        }])[feature_cols]

        scaled_features = scaler.transform(input_df)
        prob = float(model.predict_proba(scaled_features)[0][1])
        needs_support = bool(prob >= 0.50)

        # Factor attribution: calculate contribution of each feature
        coefs = model.coef_[0]
        raw_vals = [
            float(attendance_pct),
            float(previous_marks_avg),
            float(assignment_completion_rate),
            float(recent_trend),
        ]
        benchmarks = [75.0, 65.0, 75.0, 0.0]
        units = ["%", "%", "%", " pts"]
        display_names = [
            "Attendance Level",
            "Historical Marks Average",
            "Assignment Completion",
            "Recent Mark Momentum",
        ]

        factor_explanations = []
        for name, val, coef, benchmark, unit in zip(display_names, raw_vals, coefs, benchmarks, units):
            impact_direction = "increases" if coef < 0 and val < benchmark else "decreases"
            factor_explanations.append({
                "factor": name,
                "value": f"{val}{unit}",
                "impact": f"Current value ({val}{unit}) relative to benchmark ({benchmark}{unit}) {impact_direction} support need probability.",
                "coefficient": round(float(coef), 3),
            })

        return {
            "status": "available",
            "prediction": "Support Recommended" if needs_support else "Steady / On Track",
            "support_needed": needs_support,
            "probability_pct": round(prob * 100, 1),
            "factors": factor_explanations,
            "metrics": metrics,
            "warning": DEMO_WARNING,
        }

    except Exception as ex:
        return {
            "status": "error",
            "prediction": "Prediction Error",
            "support_needed": False,
            "probability_pct": 0.0,
            "factors": [f"Encountered error during prediction: {str(ex)}"],
            "metrics": None,
            "warning": DEMO_WARNING,
        }
