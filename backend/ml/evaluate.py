"""
Model evaluation suite for the AI Threat Intelligence Platform.
Computes Confusion Matrices, Classification Reports, and ROC Curves,
and saves visual evaluation artifacts into models_saved/plots/.
"""

import os
import sys
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from ml.features import extract_url_features
from ml.train_phishing import build_feature_dataframe
from ml.train_login import extract_login_features

PLOTS_DIR = os.path.join(BACKEND_DIR, "models_saved", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def evaluate_phishing():
    print("\n--- Evaluating Phishing URL Detector ---")
    model_path = os.path.join(BACKEND_DIR, "models_saved", "phishing_model.joblib")
    data_path = os.path.join(BACKEND_DIR, "data", "raw", "phishing_sample.csv")

    if not os.path.exists(model_path):
        print("Phishing model not trained yet. Run train_all.py first.")
        return

    bundle = joblib.load(model_path)
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    df = pd.read_csv(data_path)
    X_df = build_feature_dataframe(df)
    X = X_df[feature_names].values
    y = df["label"].values

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    print(classification_report(y, preds, target_names=["Legitimate", "Phishing"]))
    cm = confusion_matrix(y, preds)

    # Plot Confusion Matrix and ROC Curve
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Confusion matrix
    cax = axes[0].matshow(cm, cmap=plt.cm.Blues, alpha=0.8)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            axes[0].text(x=j, y=i, s=cm[i, j], va="center", ha="center", size="xx-large")
    axes[0].set_xlabel("Predicted Label")
    axes[0].set_ylabel("True Label")
    axes[0].set_xticklabels(["", "Legit", "Phishing"])
    axes[0].set_yticklabels(["", "Legit", "Phishing"])
    axes[0].set_title(f"Phishing Detection Confusion Matrix\n({bundle['algorithm']})")

    # ROC curve
    fpr, tpr, _ = roc_curve(y, probs)
    roc_auc = auc(fpr, tpr)
    axes[1].plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})")
    axes[1].plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].set_title("ROC Curve — Phishing Detector")
    axes[1].legend(loc="lower right")

    plt.tight_layout()
    plot_file = os.path.join(PLOTS_DIR, "phishing_evaluation.png")
    plt.savefig(plot_file, dpi=150)
    plt.close()
    print(f"Saved evaluation plot to: {plot_file}")


def evaluate_network():
    print("\n--- Evaluating Network Intrusion Classifier ---")
    model_path = os.path.join(BACKEND_DIR, "models_saved", "network_rf_model.joblib")
    test_path = os.path.join(BACKEND_DIR, "data", "raw", "nsl_kdd_sample_test.csv")

    if not os.path.exists(model_path):
        print("Network model not trained yet. Run train_all.py first.")
        return

    bundle = joblib.load(model_path)
    rf = bundle["model"]
    encoder = bundle["encoder"]
    scaler = bundle["scaler"]
    categorical_cols = bundle["categorical_cols"]
    numeric_cols = bundle["numeric_cols"]

    test_df = pd.read_csv(test_path)
    X_test_cat = encoder.transform(test_df[categorical_cols])
    X_test_num = scaler.transform(test_df[numeric_cols])
    X_test = np.hstack([X_test_num, X_test_cat])
    y_test = test_df["is_attack"].values

    preds = rf.predict(X_test)
    probs = rf.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, preds, target_names=["Normal", "Attack"]))
    cm = confusion_matrix(y_test, preds)

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].matshow(cm, cmap=plt.cm.Greens, alpha=0.8)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            axes[0].text(x=j, y=i, s=cm[i, j], va="center", ha="center", size="xx-large")
    axes[0].set_xlabel("Predicted Label")
    axes[0].set_ylabel("True Label")
    axes[0].set_xticklabels(["", "Normal", "Attack"])
    axes[0].set_yticklabels(["", "Normal", "Attack"])
    axes[0].set_title("Network Intrusion Confusion Matrix\n(NSL-KDD Test Set)")

    fpr, tpr, _ = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)
    axes[1].plot(fpr, tpr, color="teal", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})")
    axes[1].plot([0, 1], [0, 1], color="gray", lw=2, linestyle="--")
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].set_title("ROC Curve — Network Intrusion (RF)")
    axes[1].legend(loc="lower right")

    plt.tight_layout()
    plot_file = os.path.join(PLOTS_DIR, "network_evaluation.png")
    plt.savefig(plot_file, dpi=150)
    plt.close()
    print(f"Saved evaluation plot to: {plot_file}")


def evaluate_all():
    print("=" * 60)
    print(">>> Running Threat Intelligence ML Evaluation Suite")
    print("=" * 60)
    evaluate_phishing()
    evaluate_network()
    print("\n[+] All evaluation plots generated successfully in models_saved/plots/")


if __name__ == "__main__":
    evaluate_all()
