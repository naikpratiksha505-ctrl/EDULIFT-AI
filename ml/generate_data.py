"""
EduLift AI - Machine Learning Demonstration: Synthetic Data Generator
Generates reproducible fictional student data for training a demonstration ML model.
Uses fixed random seed and transparent, documented synthetic rules.
"""

import os
import numpy as np
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "synthetic_students.csv")


def generate_synthetic_data(num_samples: int = 500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic academic records for demonstration purposes.

    Features:
    - attendance_pct: Attendance percentage (45% to 100%)
    - previous_marks_avg: Historical average score (35% to 98%)
    - assignment_completion_rate: Ratio of completed assignments (0.3 to 1.0)
    - recent_trend: Change between last two assessment marks (-15 to +15)

    Synthetic Target 'needs_support':
    1 if student would likely benefit from faculty check-in / intervention, 0 otherwise.
    Rule: Strong risk if attendance < 75% AND marks < 65%, OR trend <= -6.0 with moderate marks,
          with 5% simulated noise to mirror real educational distributions.
    """
    np.random.seed(random_seed)

    # 1. Attendance percentage
    attendance = np.clip(np.random.normal(loc=78, scale=12, size=num_samples), 45.0, 100.0)

    # 2. Previous marks average
    marks = np.clip(np.random.normal(loc=72, scale=14, size=num_samples), 35.0, 98.0)

    # 3. Assignment completion rate (percentage between 30% and 100%)
    assignments = np.clip(np.random.normal(loc=82, scale=12, size=num_samples), 30.0, 100.0)

    # 4. Recent assessment trend (delta in marks between consecutive tests)
    trend = np.clip(np.random.normal(loc=0.5, scale=6.0, size=num_samples), -15.0, 15.0)

    # Documented synthetic logic for demo
    # We assign higher probability of needing support when attendance is low,
    # marks are low, assignments are missed, or trend dropped sharply.
    score_metric = (
        (75.0 - attendance) * 0.05 +
        (65.0 - marks) * 0.04 +
        (75.0 - assignments) * 0.03 +
        (-trend) * 0.06
    )

    # Sigmoid probability
    probabilities = 1.0 / (1.0 + np.exp(-score_metric))

    # Add slight random perturbation (5% noise) for realistic variation
    noise = np.random.uniform(-0.05, 0.05, size=num_samples)
    final_probs = np.clip(probabilities + noise, 0.0, 1.0)

    targets = (final_probs >= 0.50).astype(int)

    df = pd.DataFrame({
        "attendance_pct": np.round(attendance, 1),
        "previous_marks_avg": np.round(marks, 1),
        "assignment_completion_rate": np.round(assignments, 1),
        "recent_trend": np.round(trend, 1),
        "needs_support": targets,
    })

    return df


def save_dataset(filepath: str = DATA_PATH, num_samples: int = 500) -> str:
    """Generate and save the synthetic dataset to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = generate_synthetic_data(num_samples=num_samples, random_seed=42)
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} synthetic records and saved to: {filepath}")
    return filepath


if __name__ == "__main__":
    save_dataset()
