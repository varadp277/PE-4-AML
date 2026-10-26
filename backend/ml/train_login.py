"""
UEBA Login Anomaly Detection Training Pipeline.
Uses Isolation Forest to detect credential stuffing, off-hours access, and impossible travel.
Clearly tags all records as SYNTHETIC. Defensive cybersecurity analytics.
"""

import os
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler

from .metadata_manager import save_model_metadata

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "processed", "ueba_logins_synthetic.csv"
)
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models_saved")
LOGIN_MODEL_OUT = os.path.join(MODELS_DIR, "login_isolation_forest.joblib")

SAFE_COUNTRIES = {"USA", "UK", "Canada", "Germany", "Ireland"}


def extract_login_features(df: pd.DataFrame) -> tuple:
    """Transform login session fields into numeric feature matrix."""
    feats = []
    for _, row in df.iterrows():
        hour = int(row.get("hour_of_day", 12))
        is_off_hours = 1 if (hour < 7 or hour > 19) else 0
        is_weekend = int(row.get("is_weekend", 0))
        failed_attempts = int(row.get("failed_attempts", 0))
        country = str(row.get("login_country", "USA"))
        is_foreign = 1 if country not in SAFE_COUNTRIES else 0
        device = str(row.get("device", ""))
        is_untrusted_device = 1 if any(t in device.lower() for t in ["tor", "emulator", "rooted", "python", "curl"]) else 0

        # High burst penalty
        burst_penalty = 1 if failed_attempts >= 3 else 0

        feats.append([
            hour,
            is_off_hours,
            is_weekend,
            failed_attempts,
            is_foreign,
            is_untrusted_device,
            burst_penalty
        ])

    feature_names = [
        "hour_of_day",
        "is_off_hours",
        "is_weekend",
        "failed_attempts",
        "is_foreign_country",
        "is_untrusted_device",
        "burst_failure_flag"
    ]
    return np.array(feats, dtype=float), feature_names


def train_login_pipeline(extra_feedback: pd.DataFrame = None):
    print("=" * 60)
    print(">>> Starting UEBA Login Anomaly Detection Training Pipeline")
    print(f"Loading synthetic login records from: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    if extra_feedback is not None and not extra_feedback.empty:
        print(f"Merging {len(extra_feedback)} analyst-reviewed login incidents...")
        df = pd.concat([df, extra_feedback], ignore_index=True)

    print(f"Total UEBA records: {len(df)} [All tagged: SYNTHETIC_DATASET_V1]")

    # Split: train strictly on known normal profiles (unsupervised baseline creation)
    normal_df = df[df["is_known_anomaly"] == 0]
    test_df = df.sample(n=min(400, len(df)), random_state=42)

    X_train_raw, feature_names = extract_login_features(normal_df)
    X_test_raw, _ = extract_login_features(test_df)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    print(f"Baseline Normal Training Records: {len(X_train)} | Test Validation Records: {len(X_test)}")
    print(f"Features: {feature_names}")

    # Train Isolation Forest
    iso = IsolationForest(
        n_estimators=100,
        contamination=0.08,
        max_samples="auto",
        random_state=42
    )
    iso.fit(X_train)

    # Predictions: -1 indicates anomaly, 1 indicates normal
    raw_preds = iso.predict(X_test)
    binary_preds = np.where(raw_preds == -1, 1, 0)
    y_test = test_df["is_known_anomaly"].values

    acc = float(accuracy_score(y_test, binary_preds))
    prec = float(precision_score(y_test, binary_preds, zero_division=0))
    rec = float(recall_score(y_test, binary_preds, zero_division=0))
    f1 = float(f1_score(y_test, binary_preds, zero_division=0))
    cm = confusion_matrix(y_test, binary_preds).tolist()

    print(f"[UEBA Anomaly Model] Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")

    bundle = {
        "model": iso,
        "scaler": scaler,
        "feature_names": feature_names,
        "safe_countries": list(SAFE_COUNTRIES),
        "dataset_type": "SYNTHETIC_SEEDED_UEBA_V1"
    }
    joblib.dump(bundle, LOGIN_MODEL_OUT)
    print(f"Saved UEBA model to: {LOGIN_MODEL_OUT}")

    meta = {
        "model_id": "login_anomaly_detector",
        "model_name": "UEBA Login Anomaly Detector (Isolation Forest)",
        "algorithm": "Isolation Forest (Unsupervised Anomaly Detection)",
        "dataset_name": "Synthetic Corporate Login Logs (Seeded Random UEBA Profile)",
        "dataset_source_link": "Generated defensively via Seeded Random Generator (Tagged SYNTHETIC)",
        "num_records_trained": int(len(X_train)),
        "num_records_tested": int(len(X_test)),
        "total_records": int(len(df)),
        "num_features": int(len(feature_names)),
        "feature_names": feature_names,
        "train_test_split": f"Unsupervised Baseline Split: {len(X_train)} Normal Train / {len(X_test)} Test",
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": None,
        "confusion_matrix": cm,
        "trained_at": datetime.now().isoformat(),
        "is_retrained": extra_feedback is not None and not extra_feedback.empty,
        "retrained_samples_count": len(extra_feedback) if extra_feedback is not None else 0
    }
    save_model_metadata("login_anomaly_detector", meta)
    print("UEBA metadata updated.")
    return meta


if __name__ == "__main__":
    train_login_pipeline()
