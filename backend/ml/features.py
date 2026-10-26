"""
Feature engineering module for URL threat detection and explanation.
Educational and defensive cybersecurity utility.
"""

import math
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

# Common keywords heavily correlated with social engineering and credential harvesting
SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification", "secure", "security",
    "account", "banking", "update", "confirm", "wallet", "support",
    "service", "portal", "authenticate", "auth", "ebayisapi", "webscr",
    "password", "recover", "invoice", "payment", "unlock", "alert",
    "billing", "re-authenticate", "suspended", "appleid", "paypal", "meta"
]

IP_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string (higher entropy = higher randomness)."""
    if not text:
        return 0.0
    freq: Dict[str, int] = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    entropy = 0.0
    text_len = len(text)
    for count in freq.values():
        p = count / text_len
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def extract_url_features(url: str) -> Dict[str, Any]:
    """
    Extract comprehensive lexical, statistical, and structural features from a URL.
    Returns a dictionary of raw features suitable for dataframe conversion.
    """
    url_cleaned = url.strip()
    if not (url_cleaned.startswith("http://") or url_cleaned.startswith("https://") or url_cleaned.startswith("ftp://")):
        # Prepend scheme for reliable parsing if user entered domain.com/login
        parsed = urlparse("//" + url_cleaned)
        scheme = ""
    else:
        parsed = urlparse(url_cleaned)
        scheme = parsed.scheme.lower()

    netloc = parsed.netloc or ""
    path = parsed.path or ""
    query = parsed.query or ""

    # Strip port if present
    hostname = netloc.split(":")[0] if ":" in netloc else netloc

    # Hostname attributes
    is_ip = 1 if IP_PATTERN.match(hostname) else 0
    domain_parts = [p for p in hostname.split(".") if p]
    num_subdomains = max(0, len(domain_parts) - 2) if not is_ip else 0

    # Counts
    length = len(url_cleaned)
    num_dots = url_cleaned.count(".")
    num_hyphens = url_cleaned.count("-")
    num_underscores = url_cleaned.count("_")
    num_slashes = url_cleaned.count("/")
    num_question_marks = url_cleaned.count("?")
    num_equal_signs = url_cleaned.count("=")
    num_ampersands = url_cleaned.count("&")
    has_at_symbol = 1 if "@" in url_cleaned else 0
    is_https = 1 if scheme == "https" else 0

    # Digits and special characters
    digit_count = sum(c.isdigit() for c in url_cleaned)
    digit_ratio = round(digit_count / max(1, length), 4)

    special_chars = sum(not c.isalnum() for c in url_cleaned)
    special_char_ratio = round(special_chars / max(1, length), 4)

    # Suspicious keywords
    url_lower = url_cleaned.lower()
    matched_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url_lower]
    suspicious_keyword_count = len(matched_keywords)
    has_suspicious_keyword = 1 if suspicious_keyword_count > 0 else 0

    # Entropy
    entropy = calculate_entropy(url_cleaned)

    # Prefix/suffix hyphens in domain (e.g. secure-login-bank.com)
    domain_has_hyphen = 1 if "-" in hostname else 0

    return {
        "url_length": length,
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_underscores": num_underscores,
        "num_slashes": num_slashes,
        "num_subdomains": num_subdomains,
        "has_at_symbol": has_at_symbol,
        "is_https": is_https,
        "has_ip": is_ip,
        "domain_has_hyphen": domain_has_hyphen,
        "has_suspicious_keyword": has_suspicious_keyword,
        "suspicious_keyword_count": suspicious_keyword_count,
        "digit_ratio": digit_ratio,
        "special_char_ratio": special_char_ratio,
        "entropy": entropy,
        "query_length": len(query),
        "path_length": len(path),
        "_matched_keywords": matched_keywords,
    }


def explain_url_risk(features: Dict[str, Any], confidence: float, is_phishing: bool) -> List[Dict[str, str]]:
    """
    Generate human-readable explanations and risk factors based on feature extraction
    and model inference for analyst transparency.
    """
    reasons = []

    if features.get("has_ip") == 1:
        reasons.append({
            "factor": "IP Address in Hostname",
            "impact": "High",
            "description": "URL directly uses a numerical IP address instead of a standard verified domain name."
        })

    if features.get("is_https") == 0:
        reasons.append({
            "factor": "Unencrypted Connection (No HTTPS)",
            "impact": "Medium",
            "description": "Traffic is unencrypted (HTTP), exposing credentials and sensitive data in transit."
        })

    if features.get("has_at_symbol") == 1:
        reasons.append({
            "factor": "'@' Character in URL",
            "impact": "High",
            "description": "The '@' symbol in a URL can trick browser parsers to obscure the actual destination domain."
        })

    if features.get("suspicious_keyword_count", 0) > 0:
        kw_list = ", ".join(features.get("_matched_keywords", []))
        reasons.append({
            "factor": f"Suspicious Security Keywords ({kw_list})",
            "impact": "High" if features.get("suspicious_keyword_count", 0) > 1 else "Medium",
            "description": f"URL incorporates social engineering keywords: {kw_list} commonly used to imitate authentic services."
        })

    if features.get("num_subdomains", 0) >= 3:
        reasons.append({
            "factor": f"Deep Subdomain Stacking ({features.get('num_subdomains')} levels)",
            "impact": "Medium",
            "description": "Multiple subdomain levels often camouflage legitimate brand names on third-party hosts."
        })

    if features.get("url_length", 0) > 75:
        reasons.append({
            "factor": f"Abnormal URL Length ({features.get('url_length')} characters)",
            "impact": "Low",
            "description": "Extremely long URLs are frequently used to embed payloads, redirects, or hide malicious domains in address bars."
        })

    if features.get("domain_has_hyphen") == 1:
        reasons.append({
            "factor": "Hyphenated Domain Structure",
            "impact": "Low",
            "description": "Hyphens in domain names are widely used in typosquatting and deceptive mimicry."
        })

    if features.get("entropy", 0) > 4.5:
        reasons.append({
            "factor": f"High Randomness / Entropy ({features.get('entropy')})",
            "impact": "Medium",
            "description": "High character entropy suggests algorithmic domain generation (DGA) or token obfuscation."
        })

    if not reasons and not is_phishing:
        reasons.append({
            "factor": "Standard Domain & Secure Transport",
            "impact": "Info",
            "description": "URL follows recognized domain conventions with valid HTTPS and standard character distributions."
        })

    return reasons
