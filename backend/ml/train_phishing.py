"""
Training pipeline for Phishing URL Detection.
Compares Random Forest and XGBoost, selecting the champion model based on F1-score.
Defensive cybersecurity analytics.
"""

import os
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from .features import extract_url_features
from .metadata_manager import save_model_metadata

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "phishing_sample.csv")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models_saved")
MODEL_OUT = os.path.join(MODELS_DIR, "phishing_model.joblib")


def build_feature_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Extract tabular features from URL strings."""
    feature_rows = []
    for url in df["url"]:
        feats = extract_url_features(str(url))
        feats.pop("_matched_keywords", None)
        feature_rows.append(feats)
    feature_df = pd.DataFrame(feature_rows)
    return feature_df


def train_phishing_pipeline(extra_data: pd.DataFrame = None):
    print("=" * 60)
    print(">>> Starting Phishing URL Model Training Pipeline")
    print(f"Loading dataset from: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    if extra_data is not None and not extra_data.empty:
        print(f"Integrating {len(extra_data)} analyst-reviewed feedback samples into training set...")
        df = pd.concat([df, extra_data], ignore_index=True).drop_duplicates(subset=["url"])

    print(f"Dataset total records: {len(df)}")
    print(f"Phishing distribution: {df['label'].value_counts().to_dict()}")

    X_df = build_feature_dataframe(df)
    y = df["label"].values
    feature_names = list(X_df.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_df.values, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train records: {len(X_train)} | Test records: {len(X_test)} | Features: {len(feature_names)}")

    # 1. Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, class_weight="balanced")
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    rf_probs = rf.predict_proba(X_test)[:, 1]
    rf_f1 = f1_score(y_test, rf_preds)
    rf_acc = accuracy_score(y_test, rf_preds)

    # 2. Train XGBoost
    xgb = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="logloss")
    xgb.fit(X_train, y_train)
    xgb_preds = xgb.predict(X_test)
    xgb_probs = xgb.predict_proba(X_test)[:, 1]
    xgb_f1 = f1_score(y_test, xgb_preds)
    xgb_acc = accuracy_score(y_test, xgb_preds)

    print(f"[Model 1] Random Forest -> Accuracy: {rf_acc:.4f}, F1: {rf_f1:.4f}")
    print(f"[Model 2] XGBoost       -> Accuracy: {xgb_acc:.4f}, F1: {xgb_f1:.4f}")

    # Select champion by F1 score
    if xgb_f1 >= rf_f1:
        champion = xgb
        algo_name = "XGBoost Classifier"
        chosen_preds = xgb_preds
        chosen_probs = xgb_probs
        champion_f1 = xgb_f1
    else:
        champion = rf
        algo_name = "Random Forest Classifier"
        chosen_preds = rf_preds
        chosen_probs = rf_probs
        champion_f1 = rf_f1

    print(f"[+] Champion Model Selected: {algo_name} (F1: {champion_f1:.4f})")

    # Evaluate champion
    accuracy = float(accuracy_score(y_test, chosen_preds))
    precision = float(precision_score(y_test, chosen_preds, zero_division=0))
    recall = float(recall_score(y_test, chosen_preds, zero_division=0))
    f1 = float(f1_score(y_test, chosen_preds, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, chosen_probs))
    cm = confusion_matrix(y_test, chosen_preds).tolist()

    # Save model artifact bundle
    artifact = {
        "model": champion,
        "feature_names": feature_names,
        "algorithm": algo_name,
        "version": 1 if extra_data is None else 2
    }
    joblib.dump(artifact, MODEL_OUT)
    print(f"Champion model serialized to: {MODEL_OUT}")

    # Save dynamic metadata computed from real training session
    meta_info = {
        "model_id": "phishing_detector",
        "model_name": "Phishing URL Detector",
        "algorithm": algo_name,
        "dataset_name": "UCI Phishing Websites Dataset Sample",
        "dataset_source_link": "https://archive.ics.uci.edu/dataset/327/phishing+websites",
        "num_records_trained": int(len(X_train)),
        "num_records_tested": int(len(X_test)),
        "total_records": int(len(df)),
        "num_features": int(len(feature_names)),
        "feature_names": feature_names,
        "train_test_split": "80% Train / 20% Test (Stratified)",
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "confusion_matrix": cm,
        "trained_at": datetime.now().isoformat(),
        "is_retrained": extra_data is not None and not extra_data.empty,
        "retrained_samples_count": len(extra_data) if extra_data is not None else 0
    }
    save_model_metadata("phishing_detector", meta_info)
    print("Metadata updated successfully.")
    return meta_info


if __name__ == "__main__":
    train_phishing_pipeline()
