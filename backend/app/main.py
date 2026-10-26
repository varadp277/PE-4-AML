"""
FastAPI application entry point for the AI Threat Intelligence Platform.
Defensive cybersecurity case study and automated threat detection system.
"""

import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.database import Base, SessionLocal, engine
from backend.app.models.alert import Alert, ScanRecord
from backend.app.routers import alerts, dashboard, models_info, predict, retrain

# Ensure database tables exist
Base.metadata.create_all(bind=engine)


def seed_initial_demo_alerts():
    """Seed a few realistic historical alerts so dashboard charts display rich data immediately."""
    db = SessionLocal()
    try:
        count = db.query(Alert).count()
        if count == 0:
            now = datetime.utcnow()
            initial_alerts = [
                Alert(
                    timestamp=now - timedelta(hours=2, minutes=15),
                    module="phishing",
                    severity="Critical",
                    risk_score=94.5,
                    title="Credential Phishing: Target Brand Spoofing (PayPal)",
                    details=json.dumps({
                        "url": "http://secure.paypal-verification.auth-portal99.xyz/login.php",
                        "confidence": 0.945,
                        "algorithm": "XGBoost Classifier",
                        "top_reasons": ["Hyphenated Domain Structure", "Multiple Subdomains", "Unencrypted (HTTP)"]
                    }),
                    source_identifier="http://secure.paypal-verification.auth-portal99.xyz/login.php",
                    is_reviewed=False
                ),
                Alert(
                    timestamp=now - timedelta(hours=5, minutes=40),
                    module="network",
                    severity="Critical",
                    risk_score=96.0,
                    title="Network Intrusion: DoS (Traffic Flooding via ICMP/TCP)",
                    details=json.dumps({
                        "protocol": "tcp",
                        "service": "private",
                        "flag": "S0",
                        "category": "DoS (Traffic Flooding)",
                        "src_bytes": 0,
                        "dst_bytes": 0
                    }),
                    source_identifier="TCP://private:450conns",
                    is_reviewed=True,
                    analyst_verdict="Confirmed Threat",
                    analyst_notes="Identified syn flood attack pattern matching known Neptune signature.",
                    reviewed_at=now - timedelta(hours=4)
                ),
                Alert(
                    timestamp=now - timedelta(hours=9, minutes=10),
                    module="login",
                    severity="High",
                    risk_score=87.2,
                    title="UEBA Anomaly: Impossible Travel Authentication (alice.security)",
                    details=json.dumps({
                        "username": "alice.security",
                        "city": "Moscow",
                        "country": "Russia",
                        "ip": "185.120.45.67",
                        "failed_attempts": 3,
                        "reasons": ["Geographic Risk: Login originated from Russia", "Temporal Anomaly: 03:00 AM off-hours"]
                    }),
                    source_identifier="alice.security @ 185.120.45.67",
                    is_reviewed=False
                ),
                Alert(
                    timestamp=now - timedelta(days=1, hours=4),
                    module="phishing",
                    severity="High",
                    risk_score=81.0,
                    title="Suspected Deceptive Domain: Micro-Banking Portal",
                    details=json.dumps({
                        "url": "http://192.168.1.105/bankofamerica/secure-login.cgi",
                        "confidence": 0.81,
                        "algorithm": "XGBoost Classifier",
                        "top_reasons": ["IP Address in Hostname", "Security Keywords"]
                    }),
                    source_identifier="http://192.168.1.105/bankofamerica/secure-login.cgi",
                    is_reviewed=True,
                    analyst_verdict="Confirmed Threat",
                    analyst_notes="Suspicious phishing host using naked IP address.",
                    reviewed_at=now - timedelta(days=1)
                ),
                Alert(
                    timestamp=now - timedelta(days=2, hours=1),
                    module="network",
                    severity="Medium",
                    risk_score=68.5,
                    title="Zero-Day Network Anomaly (Statistical Outlier Detected)",
                    details=json.dumps({
                        "protocol": "udp",
                        "service": "other",
                        "flag": "SF",
                        "category": "Zero-Day Anomaly (Novel Pattern)"
                    }),
                    source_identifier="UDP://other:1conn",
                    is_reviewed=False
                )
            ]
            for a in initial_alerts:
                db.add(a)
                db.add(ScanRecord(
                    timestamp=a.timestamp,
                    module=a.module,
                    target=a.source_identifier or "Telemetry Stream",
                    verdict="Threat Detected",
                    risk_score=a.risk_score
                ))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    seed_initial_demo_alerts()
    yield
    # Shutdown


app = FastAPI(
    title="AI Threat Intelligence Platform API",
    description="Automated Cyber Threat Detection Platform for Defensive Cybersecurity Research.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["*"], # Permissive for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(predict.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)
app.include_router(models_info.router)
app.include_router(retrain.router)

# Mount static plots directory for viewing confusion matrices & ROC curves directly
plots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models_saved", "plots")
if os.path.exists(plots_dir):
    app.mount("/static/plots", StaticFiles(directory=plots_dir), name="plots")


@app.get("/")
def root():
    return {
        "platform": "AI-Based Threat Intelligence Platform",
        "purpose": "Educational and defensive cybersecurity case study",
        "version": "1.0.0",
        "docs_url": "/docs",
        "modules": [
            "Phishing URL Detector (/predict/url)",
            "Network Intrusion Detector (/predict/network)",
            "UEBA Login Anomaly Detector (/predict/login)",
            "Threat Dashboard (/dashboard/stats)",
            "Analyst Feedback & Alerts (/alerts)",
            "Model & Dataset Transparency (/models/info)",
            "Model Retraining Feedback Loop (/retrain)"
        ],
        "disclaimer": "Defensive use only. Do not use for offensive operations or live production security without human oversight."
    }
