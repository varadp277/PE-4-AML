from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    module: str
    severity: str
    risk_score: float
    title: str
    details: Optional[str] = None
    source_identifier: Optional[str] = None
    is_reviewed: bool
    analyst_verdict: Optional[str] = None
    analyst_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None


class AlertReviewRequest(BaseModel):
    analyst_verdict: str = Field(
        ...,
        description="Confirmed Threat, False Positive, or Legitimate Exception",
        json_schema_extra={"example": "Confirmed Threat"}
    )
    analyst_notes: Optional[str] = Field(
        default="",
        description="Analyst justification or forensic notes",
        json_schema_extra={"example": "Verified domain spoofing attack targeting executive credentials."}
    )


class DashboardStatsResponse(BaseModel):
    total_scans: int
    threats_detected: int
    alerts_today: int
    average_risk_score: float
    threats_by_module: Dict[str, int]
    severity_breakdown: Dict[str, int]
    threats_over_time: List[Dict[str, Any]]
    top_risk_sources: List[Dict[str, Any]]
    recent_alerts: List[AlertItem]
