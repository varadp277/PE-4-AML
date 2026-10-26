from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl


class URLScanRequest(BaseModel):
    url: str = Field(..., description="URL to analyze for phishing threats", min_length=3)


class RiskReason(BaseModel):
    factor: str
    impact: str # Info, Low, Medium, High
    description: str


class URLScanResponse(BaseModel):
    url: str
    verdict: str # Safe, Suspicious, Phishing
    risk_score: float # 0 to 100
    confidence: float # 0.0 to 1.0
    model_used: str
    reasons: List[RiskReason]
    features_extracted: Dict[str, Any]
    alert_created: bool = False
    alert_id: Optional[int] = None
    educational_notice: str = "Defensive analysis for educational cybersecurity case study."
