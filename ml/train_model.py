"""
EduLift AI - Machine Learning Demonstration: Model Training
Trains a Logistic Regression classifier on synthetic student data.
Compares performance against a dummy baseline classifier.
Saves model artifacts with scikit-learn metrics.
"""

import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Relative paths
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "synthetic_students.csv")
MODEL_PATH = os.path.join(BASE_DIR, "student_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "model_metrics.json")


def train_and_evaluate_model(data_path: str = DATA_PATH):
    """
    Train Logistic Regression model, compute real evaluation metrics,
    compare with baseline, and save artifacts.
    """
    if not os.path.exists(data_path):
        from generate_data import save_dataset
        save_dataset(data_path)

    df = pd.read_csv(data_path)

    feature_cols = [
        "attendance_pct",
        "previous_marks_avg",
        "assignment_completion_rate",
        "recent_trend",
    ]
    target_col = "needs_support"

    X = df[feature_cols]
    y = df[target_col]

    # Split: 80% train, 20% test, fixed random seed for reproducible results
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Standardize feature scales
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Baseline Model (Dummy Classifier - Most Frequent class)
    baseline_model = DummyClassifier(strategy="most_frequent")
    baseline_model.fit(X_train, y_train)
    baseline_preds = baseline_model.predict(X_test)

    baseline_acc = float(accuracy_score(y_test, baseline_preds))
    baseline_f1 = float(f1_score(y_test, baseline_preds, zero_division=0))

    # 2. Logistic Regression Model
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    lr_preds = lr_model.predict(X_test_scaled)

    # Calculate genuine metrics on test set
    accuracy = float(accuracy_score(y_test, lr_preds))
    precision = float(precision_score(y_test, lr_preds, zero_division=0))
    recall = float(recall_score(y_test, lr_preds, zero_division=0))
    f1 = float(f1_score(y_test, lr_preds, zero_division=0))
    cm = confusion_matrix(y_test, lr_preds).tolist()

    feature_weights = dict(zip(feature_cols, [float(c) for c in lr_model.coef_[0]]))

    metrics = {
        "model_type": "Logistic Regression",
        "features": feature_cols,
        "sample_size_total": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "baseline_accuracy": round(baseline_acc, 4),
        "baseline_f1": round(baseline_f1, 4),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "feature_weights": feature_weights,
        "intercept": float(lr_model.intercept_[0]),
    }

    # Save model bundle
    artifact = {
        "model": lr_model,
        "scaler": scaler,
        "features": feature_cols,
        "metrics": metrics,
    }
    joblib.dump(artifact, MODEL_PATH)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("=" * 60)
    print("EduLift AI - Model Training Results")
    print("=" * 60)
    print(f"Dataset Size: {len(df)} rows")
    print(f"Baseline Accuracy (Most Frequent): {baseline_acc:.2%}")
    print(f"Logistic Regression Accuracy:     {accuracy:.2%}")
    print(f"Precision:                         {precision:.2%}")
    print(f"Recall:                            {recall:.2%}")
    print(f"F1 Score:                          {f1:.2%}")
    print("Confusion Matrix [[TN, FP], [FN, TP]]:", cm)
    print("Feature Coefficients:", feature_weights)
    print("=" * 60)
    print(f"Artifact successfully saved to {MODEL_PATH}")

    return metrics


if __name__ == "__main__":
    train_and_evaluate_model()
