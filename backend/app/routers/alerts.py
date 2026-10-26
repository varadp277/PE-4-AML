"""
Alerts management and analyst review workflow router.
Enables threat triage, marking alerts as reviewed, and capturing ground-truth feedback.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.alert import Alert
from backend.app.schemas.alert import AlertItem, AlertReviewRequest

router = APIRouter(prefix="/alerts", tags=["Threat Alerts & Analyst Review"])


@router.get("", response_model=List[AlertItem])
def list_alerts(
    module: Optional[str] = Query(None, description="Filter by module: phishing, network, login"),
    severity: Optional[str] = Query(None, description="Filter by severity: Low, Medium, High, Critical"),
    is_reviewed: Optional[bool] = Query(None, description="Filter by review status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)

    if module:
        query = query.filter(Alert.module == module.lower())
    if severity:
        query = query.filter(Alert.severity == severity.capitalize())
    if is_reviewed is not None:
        query = query.filter(Alert.is_reviewed == is_reviewed)

    alerts = query.order_by(desc(Alert.timestamp)).offset(offset).limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertItem)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found.")
    return alert


@router.patch("/{alert_id}/review", response_model=AlertItem)
def review_alert(
    alert_id: int,
    payload: AlertReviewRequest,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found.")

    alert.is_reviewed = True
    alert.analyst_verdict = payload.analyst_verdict
    alert.analyst_notes = payload.analyst_notes
    alert.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(alert)
    return alert
