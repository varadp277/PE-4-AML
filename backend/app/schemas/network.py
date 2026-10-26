from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NetworkRowInput(BaseModel):
    duration: float = Field(default=0.0)
    protocol_type: str = Field(default="tcp")
    service: str = Field(default="http")
    flag: str = Field(default="SF")
    src_bytes: int = Field(default=100)
    dst_bytes: int = Field(default=200)
    count: int = Field(default=1)
    srv_count: int = Field(default=1)
    serror_rate: float = Field(default=0.0)
    rerror_rate: float = Field(default=0.0)
    same_srv_rate: float = Field(default=1.0)
    diff_srv_rate: float = Field(default=0.0)
    dst_host_count: int = Field(default=10)
    dst_host_srv_count: int = Field(default=10)
    dst_host_same_srv_rate: float = Field(default=1.0)
    dst_host_diff_srv_rate: float = Field(default=0.0)
    dst_host_serror_rate: float = Field(default=0.0)
    num_failed_logins: int = Field(default=0)
    logged_in: int = Field(default=1)


class NetworkRowResult(BaseModel):
    row_id: int
    protocol: str
    service: str
    flag: str
    is_attack: bool
    verdict: str # "Normal" or "Attack"
    attack_category: str # "Normal", "DoS", "Probe", "R2L", "U2R" or "Novel Anomaly"
    confidence: float
    risk_score: float # 0 - 100
    is_zero_day_anomaly: bool = False
    details: str


class NetworkScanSummary(BaseModel):
    total_records: int
    normal_count: int
    attack_count: int
    threat_percentage: float
    attack_categories_breakdown: Dict[str, int]
    protocol_breakdown: Dict[str, int]
    high_risk_alerts_created: int


class NetworkScanResponse(BaseModel):
    summary: NetworkScanSummary
    rows: List[NetworkRowResult]
    educational_notice: str = "Defensive analysis based on NSL-KDD & UNSW-NB15 benchmarking standards."
