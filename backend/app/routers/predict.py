"""
Prediction router for Phishing URLs, Network Intrusions, and UEBA Login Anomalies.
Defensive cybersecurity analytics with automated alert generation.
"""

import io
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.alert import Alert, ScanRecord
from backend.app.schemas.login import LoginEventRequest, LoginScanResponse
from backend.app.schemas.network import NetworkRowInput, NetworkScanResponse, NetworkScanSummary, NetworkRowResult
from backend.app.schemas.url import URLScanRequest, URLScanResponse
from backend.ml.features import explain_url_risk, extract_url_features
from backend.ml.train_phishing import build_feature_dataframe
from backend.ml.train_login import extract_login_features, SAFE_COUNTRIES

router = APIRouter(prefix="/predict", tags=["Threat Detection"])

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models_saved")
PHISHING_MODEL_PATH = os.path.join(MODELS_DIR, "phishing_model.joblib")
NETWORK_RF_PATH = os.path.join(MODELS_DIR, "network_rf_model.joblib")
NETWORK_ISO_PATH = os.path.join(MODELS_DIR, "network_isolation_forest.joblib")
LOGIN_MODEL_PATH = os.path.join(MODELS_DIR, "login_isolation_forest.joblib")

# Cache loaded models in memory
_models_cache: Dict[str, Any] = {}


def get_cached_model(key: str, path: str):
    if key not in _models_cache:
        if not os.path.exists(path):
            raise HTTPException(
                status_code=503,
                detail=f"Model artifact not found at {path}. Run `python backend/ml/train_all.py` first."
            )
        _models_cache[key] = joblib.load(path)
    return _models_cache[key]


def invalidate_model_cache(key: str):
    _models_cache.pop(key, None)


# ==============================================================================
# 1. Phishing URL Scanner
# ==============================================================================
@router.post("/url", response_model=URLScanResponse)
def scan_url(payload: URLScanRequest, db: Session = Depends(get_db)):
    url = payload.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Invalid empty URL.")

    bundle = get_cached_model("phishing", PHISHING_MODEL_PATH)
    model = bundle["model"]
    feature_names = bundle["feature_names"]
    algorithm = bundle.get("algorithm", "Classifier")

    # Extract features
    raw_feats = extract_url_features(url)
    matched_kws = raw_feats.pop("_matched_keywords", [])

    # Prepare vector matching exact training feature names
    X_df = pd.DataFrame([raw_feats])
    for col in feature_names:
        if col not in X_df.columns:
            X_df[col] = 0
    X = X_df[feature_names].values

    # Inference
    prob_phishing = float(model.predict_proba(X)[0][1])
    is_phishing = prob_phishing >= 0.5

    if prob_phishing >= 0.75:
        verdict = "Phishing"
        risk_score = round(prob_phishing * 100, 1)
        severity = "Critical" if prob_phishing > 0.9 else "High"
    elif prob_phishing >= 0.40:
        verdict = "Suspicious"
        risk_score = round(prob_phishing * 100, 1)
        severity = "Medium"
    else:
        verdict = "Safe"
        risk_score = round(prob_phishing * 100, 1)
        severity = "Low"

    # Re-insert matched keywords for explanation generator
    raw_feats["_matched_keywords"] = matched_kws
    reasons = explain_url_risk(raw_feats, confidence=prob_phishing, is_phishing=is_phishing)
    raw_feats.pop("_matched_keywords", None)

    # Record scan history
    scan_log = ScanRecord(
        module="phishing",
        target=url[:250],
        verdict=verdict,
        risk_score=risk_score
    )
    db.add(scan_log)

    # Create Alert if Suspicious or Phishing
    alert_created = False
    alert_id = None
    if verdict in ["Suspicious", "Phishing"]:
        alert = Alert(
            module="phishing",
            severity=severity,
            risk_score=risk_score,
            title=f"Potential Phishing URL Detected: {url[:60]}...",
            details=json.dumps({
                "url": url,
                "confidence": round(prob_phishing, 4),
                "algorithm": algorithm,
                "top_reasons": [r["factor"] for r in reasons[:3]]
            }),
            source_identifier=url[:250],
            is_reviewed=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        alert_created = True
        alert_id = alert.id
    else:
        db.commit()

    return URLScanResponse(
        url=url,
        verdict=verdict,
        risk_score=risk_score,
        confidence=round(prob_phishing, 4),
        model_used=algorithm,
        reasons=reasons,
        features_extracted=raw_feats,
        alert_created=alert_created,
        alert_id=alert_id
    )


# ==============================================================================
# 2. Network Intrusion Detector (CSV Upload or JSON Rows)
# ==============================================================================
@router.post("/network", response_model=NetworkScanResponse)
async def scan_network(
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    rf_bundle = get_cached_model("network_rf", NETWORK_RF_PATH)
    iso_bundle = get_cached_model("network_iso", NETWORK_ISO_PATH)

    rf_model = rf_bundle["model"]
    iso_model = iso_bundle["model"]
    encoder = rf_bundle["encoder"]
    scaler = rf_bundle["scaler"]
    categorical_cols = rf_bundle["categorical_cols"]
    numeric_cols = rf_bundle["numeric_cols"]

    if file is None or not file.filename:
        # If no file was uploaded, use default test sample records for demonstration
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data", "raw", "nsl_kdd_sample_test.csv"
        )
        if os.path.exists(sample_path) and os.path.getsize(sample_path) > 0:
            df = pd.read_csv(sample_path).head(40)
        else:
            # Fallback demonstration rows if raw data folder is empty or absent
            fallback_rows = [
                {
                    "duration": 0, "protocol_type": "tcp", "service": "http", "flag": "SF",
                    "src_bytes": 181, "dst_bytes": 5450, "count": 8, "srv_count": 8,
                    "serror_rate": 0.0, "rerror_rate": 0.0, "same_srv_rate": 1.0,
                    "diff_srv_rate": 0.0, "dst_host_count": 9, "dst_host_srv_count": 9,
                    "dst_host_same_srv_rate": 1.0, "dst_host_diff_srv_rate": 0.0,
                    "dst_host_serror_rate": 0.0, "num_failed_logins": 0, "logged_in": 1
                }
            ] * 20
            df = pd.DataFrame(fallback_rows)
    else:
        MAX_UPLOAD_SIZE = int(4.5 * 1024 * 1024) # 4.5 MB serverless payload limit
        content = await file.read()
        if len(content) > MAX_UPLOAD_SIZE:
            size_mb = round(len(content) / (1024 * 1024), 2)
            raise HTTPException(
                status_code=413,
                detail=f"Uploaded CSV ({size_mb} MB) exceeds the 4.5 MB serverless upload limit. Please upload a smaller file under 4.5 MB."
            )
        try:
            df = pd.read_csv(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty. Please provide network telemetry records.")

    # Ensure required columns are present with sensible defaults
    for col in categorical_cols:
        if col not in df.columns:
            df[col] = "tcp" if col == "protocol_type" else ("http" if col == "service" else "SF")
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0

    # Transformations
    X_cat = encoder.transform(df[categorical_cols])
    X_num = scaler.transform(df[numeric_cols])
    X = np.hstack([X_num, X_cat])

    # Supervised predictions (RF)
    rf_preds = rf_model.predict(X)
    rf_probs = rf_model.predict_proba(X)[:, 1]

    # Unsupervised Anomaly Detection (Isolation Forest)
    iso_raw = iso_model.predict(X) # -1 is anomaly
    iso_scores = -iso_model.score_samples(X)

    results: List[NetworkRowResult] = []
    cat_counts: Dict[str, int] = {}
    proto_counts: Dict[str, int] = {}
    attacks = 0
    normals = 0
    alerts_created_count = 0

    attack_categories_pool = ["DoS (Neptune/Smurf)", "Probe (Portsweep/Satan)", "R2L (Unauthorized Access)", "U2R (Buffer Overflow)"]

    for idx, row in df.iterrows():
        is_attack = bool(rf_preds[idx] == 1)
        prob = float(rf_probs[idx])
        is_zero_day = bool(iso_raw[idx] == -1)

        protocol = str(row.get("protocol_type", "tcp"))
        service = str(row.get("service", "http"))
        flag = str(row.get("flag", "SF"))

        proto_counts[protocol] = proto_counts.get(protocol, 0) + 1

        if is_attack:
            attacks += 1
            # Infer realistic category based on signature
            if row.get("count", 0) > 100 or flag == "S0":
                cat = "DoS (Traffic Flooding)"
            elif flag in ["REJ", "RSTR", "SH"] or row.get("diff_srv_rate", 0) > 0.5:
                cat = "Probe (Port/Vulnerability Scanning)"
            elif row.get("num_failed_logins", 0) > 0:
                cat = "R2L (Brute Force / Password Attack)"
            else:
                cat = "Generic Exploits / Malware Traffic"

            risk_score = round(max(prob * 100, 75.0), 1)
            verdict = "Attack"
            details = f"Intrusion signature identified: {cat}. Protocol: {protocol}, Service: {service}, Flag: {flag}."
        elif is_zero_day:
            attacks += 1
            cat = "Zero-Day Anomaly (Novel Pattern)"
            risk_score = 68.5
            verdict = "Attack"
            details = f"Unsupervised Isolation Forest detected statistical outlier outside baseline network manifold (Anomaly score: {round(float(iso_scores[idx]), 3)})."
        else:
            normals += 1
            cat = "Normal Traffic"
            risk_score = round(prob * 100, 1)
            verdict = "Normal"
            details = f"Benign traffic flow verified ({protocol}/{service}). Conforms to normal enterprise baseline."

        cat_counts[cat] = cat_counts.get(cat, 0) + 1

        results.append(NetworkRowResult(
            row_id=int(idx + 1),
            protocol=protocol,
            service=service,
            flag=flag,
            is_attack=(verdict == "Attack"),
            verdict=verdict,
            attack_category=cat,
            confidence=round(prob if is_attack else (1.0 - prob), 3),
            risk_score=risk_score,
            is_zero_day_anomaly=is_zero_day,
            details=details
        ))

        # Log High Risk Alerts to DB (up to top 5 representative alerts per batch)
        if verdict == "Attack" and alerts_created_count < 5:
            alert = Alert(
                module="network",
                severity="Critical" if risk_score > 85 else "High",
                risk_score=risk_score,
                title=f"Network Intrusion: {cat} ({protocol.upper()}/{service})",
                details=json.dumps({
                    "row_id": int(idx + 1),
                    "protocol": protocol,
                    "service": service,
                    "flag": flag,
                    "src_bytes": int(row.get("src_bytes", 0)),
                    "dst_bytes": int(row.get("dst_bytes", 0)),
                    "category": cat
                }),
                source_identifier=f"{protocol.upper()}://{service}:{row.get('count', 1)}conns",
                is_reviewed=False
            )
            db.add(alert)
            alerts_created_count += 1

    # Record overall scan
    db.add(ScanRecord(
        module="network",
        target=f"CSV Batch ({len(df)} records)",
        verdict=f"{attacks} Attacks / {normals} Normal",
        risk_score=round((attacks / max(1, len(df))) * 100, 1)
    ))
    db.commit()

    summary = NetworkScanSummary(
        total_records=len(df),
        normal_count=normals,
        attack_count=attacks,
        threat_percentage=round((attacks / max(1, len(df))) * 100, 1),
        attack_categories_breakdown=cat_counts,
        protocol_breakdown=proto_counts,
        high_risk_alerts_created=alerts_created_count
    )

    return NetworkScanResponse(summary=summary, rows=results)


# ==============================================================================
# 3. Login Anomaly Detector (UEBA)
# ==============================================================================
@router.post("/login", response_model=LoginScanResponse)
def scan_login(event: LoginEventRequest, db: Session = Depends(get_db)):
    bundle = get_cached_model("login_iso", LOGIN_MODEL_PATH)
    iso_model = bundle["model"]
    scaler = bundle["scaler"]
    feature_names = bundle["feature_names"]

    # Parse timestamp
    if event.timestamp:
        try:
            dt = datetime.fromisoformat(event.timestamp)
        except Exception:
            dt = datetime.utcnow()
    else:
        dt = datetime.utcnow()

    hour = dt.hour
    is_weekend = 1 if dt.weekday() >= 5 else 0
    is_off_hours = 1 if (hour < 7 or hour > 19) else 0
    failed_attempts = event.failed_attempts
    is_foreign = 1 if event.login_country not in SAFE_COUNTRIES else 0
    is_untrusted_device = 1 if any(t in event.device.lower() for t in ["tor", "emulator", "rooted", "python", "curl", "unknown"]) else 0
    burst_penalty = 1 if failed_attempts >= 3 else 0

    vector = np.array([[
        hour,
        is_off_hours,
        is_weekend,
        failed_attempts,
        is_foreign,
        is_untrusted_device,
        burst_penalty
    ]], dtype=float)

    X_scaled = scaler.transform(vector)
    iso_pred = iso_model.predict(X_scaled)[0] # -1 = anomaly, 1 = normal
    raw_score = float(-iso_model.score_samples(X_scaled)[0])

    is_anomaly = (iso_pred == -1) or (failed_attempts >= 5) or (is_foreign == 1 and is_off_hours == 1)

    reasons = []
    if is_foreign:
        reasons.append(f"Geographic Risk: Login originated from unexpected country ({event.login_city}, {event.login_country})")
    if is_off_hours:
        reasons.append(f"Temporal Anomaly: Authentication requested at {hour:02d}:00 outside standard corporate business hours")
    if failed_attempts >= 3:
        reasons.append(f"Brute-Force Velocity: High failed password attempts ({failed_attempts} attempts)")
    if is_untrusted_device:
        reasons.append(f"Device Integrity Warning: Non-standard/anomalous client environment ({event.device})")

    if not reasons and not is_anomaly:
        reasons.append("Standard login aligned with baseline corporate behavioral profile.")

    # Risk score calculation
    if is_anomaly:
        risk_score = round(min(98.0, 50.0 + (raw_score * 40) + (failed_attempts * 6) + (20 if is_foreign else 0)), 1)
        verdict = "Anomalous Login"
        severity = "Critical" if risk_score > 85 else "High"
    else:
        risk_score = round(max(5.0, raw_score * 20 + failed_attempts * 4), 1)
        verdict = "Normal"
        severity = "Low"

    session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"

    # Log scan
    db.add(ScanRecord(
        module="login",
        target=f"{event.username} ({event.login_city})",
        verdict=verdict,
        risk_score=risk_score
    ))

    # Create Alert if Anomalous
    alert_created = False
    alert_id = None
    if is_anomaly:
        alert = Alert(
            module="login",
            severity=severity,
            risk_score=risk_score,
            title=f"UEBA Anomaly: Suspicious Authentication for {event.username}",
            details=json.dumps({
                "username": event.username,
                "role": event.role,
                "city": event.login_city,
                "country": event.login_country,
                "ip": event.ip_address,
                "device": event.device,
                "failed_attempts": failed_attempts,
                "reasons": reasons
            }),
            source_identifier=f"{event.username} @ {event.ip_address}",
            is_reviewed=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        alert_created = True
        alert_id = alert.id
    else:
        db.commit()

    return LoginScanResponse(
        session_id=session_id,
        username=event.username,
        verdict=verdict,
        is_anomaly=is_anomaly,
        risk_score=risk_score,
        anomaly_score=round(raw_score, 4),
        reasons=reasons,
        alert_created=alert_created,
        alert_id=alert_id
    )
