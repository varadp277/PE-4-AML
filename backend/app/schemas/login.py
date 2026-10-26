from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class LoginEventRequest(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "alice.security"})
    role: Optional[str] = Field(default="Employee", json_schema_extra={"example": "SecOps"})
    timestamp: Optional[str] = Field(default=None, json_schema_extra={"example": "2026-10-25T03:15:00"})
    login_city: str = Field(..., json_schema_extra={"example": "Pyongyang"})
    login_country: str = Field(..., json_schema_extra={"example": "North Korea"})
    ip_address: str = Field(..., json_schema_extra={"example": "185.220.101.5"})
    device: str = Field(..., json_schema_extra={"example": "Tor-Browser-Exit-Node"})
    failed_attempts: int = Field(default=0, ge=0, json_schema_extra={"example": 4})


class LoginScanResponse(BaseModel):
    session_id: str
    username: str
    verdict: str # "Normal" or "Anomalous Login"
    is_anomaly: bool
    risk_score: float # 0 - 100
    anomaly_score: float # Raw Isolation Forest negative score
    reasons: List[str]
    alert_created: bool = False
    alert_id: Optional[int] = None
    is_synthetic_evaluation: bool = True
    synthetic_notice: str = "[SYNTHETIC DATASET DEMO] - Simulated corporate login telemetry for defensive case study."
