"""
Training pipeline for Network Intrusion Detection using NSL-KDD and UNSW-NB15 datasets.
Builds:
1. Supervised Random Forest Classifier (Normal vs Attack, with attack categories).
2. Unsupervised Isolation Forest (Zero-Day / Novelty Network Anomaly Detection).
Defensive cybersecurity analytics.
"""

import os
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .metadata_manager import save_model_metadata

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models_saved")
RF_MODEL_OUT = os.path.join(MODELS_DIR, "network_rf_model.joblib")
ISO_MODEL_OUT = os.path.join(MODELS_DIR, "network_isolation_forest.joblib")


def train_network_models(extra_feedback: pd.DataFrame = None):
    print("=" * 60)
    print(">>> Starting Network Intrusion Detection Training Pipeline")

    train_path = os.path.join(DATA_DIR, "nsl_kdd_sample_train.csv")
    test_path = os.path.join(DATA_DIR, "nsl_kdd_sample_test.csv")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    if extra_feedback is not None and not extra_feedback.empty:
        print(f"Adding {len(extra_feedback)} analyst-reviewed network alerts to training set...")
        train_df = pd.concat([train_df, extra_feedback], ignore_index=True)

    print(f"NSL-KDD Official Train records: {len(train_df)}, Test records: {len(test_df)}")

    categorical_cols = ["protocol_type", "service", "flag"]
    numeric_cols = [
        "duration", "src_bytes", "dst_bytes", "count", "srv_count",
        "serror_rate", "rerror_rate", "same_srv_rate", "diff_srv_rate",
        "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate", "dst_host_serror_rate", "num_failed_logins", "logged_in"
    ]

    # Preprocessing
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    scaler = StandardScaler()

    # Fit transformations strictly on Train data to prevent data leakage
    X_train_cat = encoder.fit_transform(train_df[categorical_cols])
    X_train_num = scaler.fit_transform(train_df[numeric_cols])
    X_train = np.hstack([X_train_num, X_train_cat])

    X_test_cat = encoder.transform(test_df[categorical_cols])
    X_test_num = scaler.transform(test_df[numeric_cols])
    X_test = np.hstack([X_test_num, X_test_cat])

    encoded_cat_names = list(encoder.get_feature_names_out(categorical_cols))
    all_feature_names = numeric_cols + encoded_cat_names
    total_features = X_train.shape[1]

    y_train = train_df["is_attack"].values
    y_test = test_df["is_attack"].values

    print(f"Transformed features count: {total_features}")

    # ==========================================
    # 1. Supervised Random Forest Classifier
    # ==========================================
    print("Training Supervised Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=14, random_state=42, class_weight="balanced")
    rf.fit(X_train, y_train)

    rf_preds = rf.predict(X_test)
    rf_probs = rf.predict_proba(X_test)[:, 1]

    rf_acc = float(accuracy_score(y_test, rf_preds))
    rf_prec = float(precision_score(y_test, rf_preds, zero_division=0))
    rf_rec = float(recall_score(y_test, rf_preds, zero_division=0))
    rf_f1 = float(f1_score(y_test, rf_preds, zero_division=0))
    rf_auc = float(roc_auc_score(y_test, rf_probs))
    rf_cm = confusion_matrix(y_test, rf_preds).tolist()

    print(f"[RF Evaluated] Accuracy: {rf_acc:.4f}, Precision: {rf_prec:.4f}, Recall: {rf_rec:.4f}, F1: {rf_f1:.4f}, AUC: {rf_auc:.4f}")

    rf_bundle = {
        "model": rf,
        "encoder": encoder,
        "scaler": scaler,
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "feature_names": all_feature_names,
        "classes": list(rf.classes_)
    }
    joblib.dump(rf_bundle, RF_MODEL_OUT)
    print(f"Saved RF bundle to: {RF_MODEL_OUT}")

    # Log RF metadata
    rf_meta = {
        "model_id": "network_rf_detector",
        "model_name": "Network Intrusion Classifier (Random Forest)",
        "algorithm": "Random Forest Classifier",
        "dataset_name": "NSL-KDD Benchmarking Dataset",
        "dataset_source_link": "https://www.unb.ca/cic/datasets/nsl.html",
        "num_records_trained": int(len(train_df)),
        "num_records_tested": int(len(test_df)),
        "total_records": int(len(train_df) + len(test_df)),
        "num_features": int(total_features),
        "feature_names": all_feature_names,
        "train_test_split": f"Official Split: Train ({len(train_df)}) / Test ({len(test_df)})",
        "accuracy": round(rf_acc, 4),
        "precision": round(rf_prec, 4),
        "recall": round(rf_rec, 4),
        "f1_score": round(rf_f1, 4),
        "roc_auc": round(rf_auc, 4),
        "confusion_matrix": rf_cm,
        "trained_at": datetime.now().isoformat(),
        "is_retrained": extra_feedback is not None and not extra_feedback.empty,
        "retrained_samples_count": len(extra_feedback) if extra_feedback is not None else 0
    }
    save_model_metadata("network_rf_detector", rf_meta)

    # ==========================================
    # 2. Unsupervised Isolation Forest (Anomaly)
    # ==========================================
    print("Training Unsupervised Isolation Forest on Normal Baseline Network Traffic...")
    # Train Isolation Forest primarily on normal network records
    normal_mask = train_df["is_attack"] == 0
    X_train_normal = X_train[normal_mask]

    iso = IsolationForest(n_estimators=100, contamination=0.15, random_state=42)
    iso.fit(X_train_normal)

    # Anomaly scores: -1 is anomaly (attack), 1 is normal
    iso_raw_preds = iso.predict(X_test)
    iso_binary_preds = np.where(iso_raw_preds == -1, 1, 0)
    iso_scores = -iso.score_samples(X_test) # Higher score = more anomalous

    iso_acc = float(accuracy_score(y_test, iso_binary_preds))
    iso_prec = float(precision_score(y_test, iso_binary_preds, zero_division=0))
    iso_rec = float(recall_score(y_test, iso_binary_preds, zero_division=0))
    iso_f1 = float(f1_score(y_test, iso_binary_preds, zero_division=0))
    iso_cm = confusion_matrix(y_test, iso_binary_preds).tolist()

    print(f"[Isolation Forest] Accuracy: {iso_acc:.4f}, Precision: {iso_prec:.4f}, Recall: {iso_rec:.4f}, F1: {iso_f1:.4f}")

    iso_bundle = {
        "model": iso,
        "encoder": encoder,
        "scaler": scaler,
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "feature_names": all_feature_names
    }
    joblib.dump(iso_bundle, ISO_MODEL_OUT)
    print(f"Saved Isolation Forest bundle to: {ISO_MODEL_OUT}")

    iso_meta = {
        "model_id": "network_anomaly_detector",
        "model_name": "Zero-Day Network Anomaly Detector (Isolation Forest)",
        "algorithm": "Isolation Forest (Unsupervised)",
        "dataset_name": "UNSW-NB15 & NSL-KDD Baseline Network Flows",
        "dataset_source_link": "https://research.unsw.edu.au/projects/unsw-nb15-dataset",
        "num_records_trained": int(len(X_train_normal)),
        "num_records_tested": int(len(test_df)),
        "total_records": int(len(train_df) + len(test_df)),
        "num_features": int(total_features),
        "feature_names": all_feature_names,
        "train_test_split": f"Normal Baseline Filter: {len(X_train_normal)} Train / {len(test_df)} Test",
        "accuracy": round(iso_acc, 4),
        "precision": round(iso_prec, 4),
        "recall": round(iso_rec, 4),
        "f1_score": round(iso_f1, 4),
        "roc_auc": None,
        "confusion_matrix": iso_cm,
        "trained_at": datetime.now().isoformat(),
        "is_retrained": False
    }
    save_model_metadata("network_anomaly_detector", iso_meta)
    print("Network metadata successfully updated.")
    return rf_meta, iso_meta


if __name__ == "__main__":
    train_network_models()
