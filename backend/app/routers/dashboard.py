"""
Threat Intelligence Dashboard statistics and analytics aggregation router.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.alert import Alert, ScanRecord
from backend.app.schemas.alert import AlertItem, DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard Statistics"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Total Scans
    total_scans = db.query(ScanRecord).count()
    if total_scans == 0:
        total_scans = db.query(Alert).count()

    # 2. Total Threats Detected (Alerts in DB)
    threats_detected = db.query(Alert).count()

    # 3. Alerts Today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    alerts_today = db.query(Alert).filter(Alert.timestamp >= today_start).count()

    # 4. Average Risk Score
    avg_score_res = db.query(func.avg(Alert.risk_score)).scalar()
    average_risk_score = round(float(avg_score_res), 1) if avg_score_res is not None else 0.0

    # 5. Threats by Module
    module_rows = db.query(Alert.module, func.count(Alert.id)).group_by(Alert.module).all()
    threats_by_module = {
        "phishing": 0,
        "network": 0,
        "login": 0
    }
    for mod, count in module_rows:
        threats_by_module[mod] = count

    # 6. Severity Breakdown
    sev_rows = db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all()
    severity_breakdown = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
        "Critical": 0
    }
    for sev, count in sev_rows:
        if sev in severity_breakdown:
            severity_breakdown[sev] = count

    # 7. Threats over time (last 7 days trend)
    threats_over_time: List[Dict[str, Any]] = []
    for day_idx in range(6, -1, -1):
        target_day = (datetime.utcnow() - timedelta(days=day_idx)).date()
        day_start = datetime.combine(target_day, datetime.min.time())
        day_end = datetime.combine(target_day, datetime.max.time())
        count = db.query(Alert).filter(Alert.timestamp >= day_start, Alert.timestamp <= day_end).count()
        threats_over_time.append({
            "date": target_day.strftime("%b %d"),
            "threats": count,
            "phishing": db.query(Alert).filter(Alert.module == "phishing", Alert.timestamp >= day_start, Alert.timestamp <= day_end).count(),
            "network": db.query(Alert).filter(Alert.module == "network", Alert.timestamp >= day_start, Alert.timestamp <= day_end).count(),
            "login": db.query(Alert).filter(Alert.module == "login", Alert.timestamp >= day_start, Alert.timestamp <= day_end).count()
        })

    # 8. Top Risk Sources
    top_sources_query = (
        db.query(Alert.source_identifier, func.count(Alert.id), func.max(Alert.risk_score))
        .filter(Alert.source_identifier.isnot(None))
        .group_by(Alert.source_identifier)
        .order_by(desc(func.count(Alert.id)))
        .limit(5)
        .all()
    )
    top_risk_sources = [
        {
            "source": s[0],
            "count": s[1],
            "max_risk": s[2]
        }
        for s in top_sources_query
    ]

    # 9. Recent Alerts
    recent_alerts = db.query(Alert).order_by(desc(Alert.timestamp)).limit(10).all()

    return DashboardStatsResponse(
        total_scans=total_scans,
        threats_detected=threats_detected,
        alerts_today=alerts_today,
        average_risk_score=average_risk_score,
        threats_by_module=threats_by_module,
        severity_breakdown=severity_breakdown,
        threats_over_time=threats_over_time,
        top_risk_sources=top_risk_sources,
        recent_alerts=recent_alerts
    )
