"""
Unit tests for URL feature extraction and explainability.
"""

import pytest
from backend.ml.features import calculate_entropy, explain_url_risk, extract_url_features


def test_legitimate_url_features():
    url = "https://www.google.com/search?q=cybersecurity"
    feats = extract_url_features(url)

    assert feats["is_https"] == 1
    assert feats["has_ip"] == 0
    assert feats["has_at_symbol"] == 0
    assert feats["num_subdomains"] <= 1
    assert feats["digit_ratio"] >= 0.0


def test_phishing_url_features_detection():
    # Phishing URL containing multiple suspicious indicators
    phishing_url = "http://192.168.1.1/paypal/login-verification/secure/update?auth=true&token=123"
    feats = extract_url_features(phishing_url)

    assert feats["is_https"] == 0
    assert feats["has_ip"] == 1
    assert feats["has_suspicious_keyword"] == 1
    assert feats["suspicious_keyword_count"] >= 3
    assert "login" in feats["_matched_keywords"]
    assert "verify" in feats["_matched_keywords"] or "verification" in feats["_matched_keywords"]

    reasons = explain_url_risk(feats, confidence=0.92, is_phishing=True)
    factors = [r["factor"] for r in reasons]
    assert any("IP Address" in f for f in factors)
    assert any("Unencrypted" in f for f in factors)


def test_entropy_calculation():
    # Low entropy (repetitive)
    low_ent = calculate_entropy("aaaaaaa")
    # High entropy (random alphanumeric)
    high_ent = calculate_entropy("a8Z9v!kL#2pQ9x1")

    assert low_ent < 1.0
    assert high_ent > 3.0
