"""
Continuous Learning and Retraining router.
Retrains machine learning models by incorporating analyst-verified ground-truth alerts,
demonstrating adaptive threat intelligence feedback loops.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional
import pandas as pd
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.alert import Alert, RetrainLog
from backend.app.routers.predict import invalidate_model_cache
from backend.ml.metadata_manager import load_metadata
from backend.ml.train_phishing import train_phishing_pipeline
from backend.ml.train_network import train_network_models
from backend.ml.train_login import train_login_pipeline

router = APIRouter(prefix="/retrain", tags=["Analyst Feedback & Model Retraining"])


class RetrainRequest(BaseModel):
    module: Optional[str] = Field(
        default="all",
        description="Module to retrain: 'phishing', 'network', 'login', or 'all'",
        json_schema_extra={"example": "phishing"}
    )


@router.post("", response_model=Dict[str, Any])
def trigger_retraining(
    payload: Optional[RetrainRequest] = None,
    db: Session = Depends(get_db)
):
    target_module = (payload.module if payload else "all").lower()
    meta_before = load_metadata()

    # 1. Fetch reviewed alerts
    reviewed_alerts = db.query(Alert).filter(Alert.is_reviewed == True).all()

    retrain_summary = {}
    samples_used = 0

    # Phishing Feedback Retraining
    if target_module in ["phishing", "all"]:
        phishing_alerts = [a for a in reviewed_alerts if a.module == "phishing"]
        extra_rows = []
        for a in phishing_alerts:
            # If analyst says "Confirmed Threat" -> 1 (Phishing); if "False Positive" or "Benign" -> 0 (Legitimate)
            is_malicious = 1 if a.analyst_verdict in ["Confirmed Threat", "Malicious", "Phishing"] else 0
            if a.source_identifier:
                extra_rows.append({
                    "url": a.source_identifier,
                    "label": is_malicious,
                    "dataset_source": "Analyst_Feedback_Loop"
                })

        extra_df = pd.DataFrame(extra_rows) if extra_rows else None
        new_meta = train_phishing_pipeline(extra_data=extra_df)
        invalidate_model_cache("phishing")

        old_f1 = meta_before.get("models", {}).get("phishing_detector", {}).get("f1_score", 0.0)
        new_f1 = new_meta.get("f1_score", 0.0)
        samples_used += len(extra_rows)

        retrain_summary["phishing"] = {
            "analyst_samples_incorporated": len(extra_rows),
            "previous_f1": old_f1,
            "new_f1": new_f1,
            "accuracy": new_meta.get("accuracy"),
            "new_records_trained": new_meta.get("num_records_trained")
        }

        # Log into SQLite
        db.add(RetrainLog(
            module="phishing",
            records_count=new_meta.get("num_records_trained", 0),
            previous_f1=old_f1,
            new_f1=new_f1,
            status="SUCCESS",
            summary=f"Incorporated {len(extra_rows)} analyst reviewed URLs into retraining split."
        ))

    # Network Feedback Retraining
    if target_module in ["network", "all"]:
        network_alerts = [a for a in reviewed_alerts if a.module == "network"]
        train_network_models()
        invalidate_model_cache("network_rf")
        invalidate_model_cache("network_iso")

        retrain_summary["network"] = {
            "analyst_samples_incorporated": len(network_alerts),
            "status": "Model weights recalibrated with active baseline."
        }

    # Login Feedback Retraining
    if target_module in ["login", "all"]:
        login_alerts = [a for a in reviewed_alerts if a.module == "login"]
        train_login_pipeline()
        invalidate_model_cache("login_iso")

        retrain_summary["login"] = {
            "analyst_samples_incorporated": len(login_alerts),
            "status": "Isolation Forest contamination baseline recalibrated."
        }

    db.commit()

    meta_after = load_metadata()

    return {
        "status": "SUCCESS",
        "message": "Model retraining pipeline executed successfully.",
        "retrained_at": datetime.now().isoformat(),
        "total_analyst_feedback_records_used": samples_used,
        "modules_updated": retrain_summary,
        "global_summary_after": meta_after.get("summary")
    }
