"""
Single unified training runner for all Threat Intelligence ML models.
Executes Phishing URL, Network Intrusion, and UEBA Login pipelines sequentially,
then prints dynamic auditing summary calculated directly from real training data.
"""

import sys
import os

# Ensure backend root is in python path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from ml.train_phishing import train_phishing_pipeline
from ml.train_network import train_network_models
from ml.train_login import train_login_pipeline
from ml.metadata_manager import load_metadata


def train_all():
    print("\n" + "=" * 70)
    print("      AI-BASED THREAT INTELLIGENCE PLATFORM — MODEL TRAINING")
    print("      Defensive & Educational Cybersecurity Case Study")
    print("=" * 70 + "\n")

    # 1. Phishing detector
    print(">>> [1/3] Training Phishing URL Detection Models...")
    phishing_meta = train_phishing_pipeline()

    # 2. Network intrusion detectors (RF & Isolation Forest)
    print("\n>>> [2/3] Training Network Intrusion Detection Models...")
    train_network_models()

    # 3. UEBA login anomaly detector
    print("\n>>> [3/3] Training UEBA Login Anomaly Detection Models...")
    train_login_pipeline()

    # Global summary verification
    meta = load_metadata()
    summary = meta.get("summary", {})

    print("\n" + "=" * 70)
    print("                      TRAINING COMPLETE SUMMARY")
    print("=" * 70)
    print(f" Datasets Used (unique)     : {summary.get('total_datasets')}")
    print(f" Total Records Trained On   : {summary.get('total_records_trained_on'):,}")
    print(f" Total Models Trained       : {summary.get('total_models_trained')}")
    print(f" Timestamp                  : {summary.get('last_updated')}")
    print("=" * 70)

    for m_id, m in meta.get("models", {}).items():
        print(f"[*] {m.get('model_name')}")
        print(f"    - Algorithm : {m.get('algorithm')}")
        print(f"    - Records   : {m.get('num_records_trained')} train, {m.get('num_records_tested')} test")
        print(f"    - Features  : {m.get('num_features')}")
        print(f"    - Accuracy  : {m.get('accuracy')}")
        print(f"    - F1 Score  : {m.get('f1_score')}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    train_all()
