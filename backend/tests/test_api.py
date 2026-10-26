"""
Unit & Integration tests for FastAPI endpoints:
/predict/url, /predict/network, /predict/login, /alerts, /dashboard/stats, /models/info, /retrain.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "AI-Based Threat Intelligence Platform" in data["platform"]
    assert "disclaimer" in data


def test_predict_url_safe():
    res = client.post("/predict/url", json={"url": "https://www.wikipedia.org/wiki/Computer_security"})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["Safe", "Suspicious", "Phishing"]
    assert "confidence" in data
    assert "risk_score" in data
    assert "reasons" in data


def test_predict_url_phishing():
    res = client.post(
        "/predict/url",
        json={"url": "http://192.168.1.50/paypal-login/verify-account/auth.php"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] > 50
    assert data["verdict"] in ["Suspicious", "Phishing"]
    assert len(data["reasons"]) > 0


def test_predict_login_normal():
    res = client.post(
        "/predict/login",
        json={
            "username": "bob.developer",
            "role": "Dev",
            "timestamp": "2026-10-25T14:30:00",
            "login_city": "San Francisco",
            "login_country": "USA",
            "ip_address": "192.168.1.12",
            "device": "Linux-Workstation",
            "failed_attempts": 0
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "bob.developer"
    assert data["verdict"] in ["Normal", "Anomalous Login"]


def test_predict_login_anomaly():
    res = client.post(
        "/predict/login",
        json={
            "username": "alice.security",
            "role": "SecOps",
            "timestamp": "2026-10-25T03:00:00",
            "login_city": "Pyongyang",
            "login_country": "North Korea",
            "ip_address": "89.23.45.10",
            "device": "Tor-Browser-Exit-Node",
            "failed_attempts": 6
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_anomaly"] is True
    assert data["verdict"] == "Anomalous Login"
    assert len(data["reasons"]) > 0


def test_predict_network_default_sample():
    # Calling /predict/network without a file uses the standard test sample batch
    res = client.post("/predict/network")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert data["summary"]["total_records"] > 0
    assert "attack_count" in data["summary"]
    assert len(data["rows"]) > 0


def test_models_info():
    res = client.get("/models/info")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert data["summary"]["total_models_trained"] >= 3
    assert data["summary"]["total_records_trained_on"] > 0
    assert "models" in data
    assert "phishing_detector" in data["models"]


def test_alerts_and_review():
    # 1. Fetch alerts
    res = client.get("/alerts")
    assert res.status_code == 200
    alerts = res.json()
    assert isinstance(alerts, list)

    if alerts:
        target_id = alerts[0]["id"]
        # 2. Review alert
        review_res = client.patch(
            f"/alerts/{target_id}/review",
            json={
                "analyst_verdict": "Confirmed Threat",
                "analyst_notes": "Unit test verified incident."
            }
        )
        assert review_res.status_code == 200
        updated = review_res.json()
        assert updated["is_reviewed"] is True
        assert updated["analyst_verdict"] == "Confirmed Threat"


def test_dashboard_stats():
    res = client.get("/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert "total_scans" in data
    assert "threats_detected" in data
    assert "threats_by_module" in data
    assert "severity_breakdown" in data
    assert "threats_over_time" in data


def test_retraining_endpoint():
    res = client.post("/retrain", json={"module": "phishing"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert "modules_updated" in data
