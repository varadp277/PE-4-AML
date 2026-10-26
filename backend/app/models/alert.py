"""
SQLAlchemy ORM models for Threat Alerts, Scan History, and Retraining Logs.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from backend.app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    module = Column(String(50), nullable=False) # phishing, network, login
    severity = Column(String(20), nullable=False) # Low, Medium, High, Critical
    risk_score = Column(Float, nullable=False) # 0.0 - 100.0
    title = Column(String(255), nullable=False)
    details = Column(Text, nullable=True) # JSON or descriptive text
    source_identifier = Column(String(255), nullable=True) # URL, IP, user session
    is_reviewed = Column(Boolean, default=False, index=True)
    analyst_verdict = Column(String(50), nullable=True) # "Confirmed Threat", "False Positive", "Benign"
    analyst_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)


class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    module = Column(String(50), nullable=False)
    target = Column(String(255), nullable=False)
    verdict = Column(String(50), nullable=False)
    risk_score = Column(Float, nullable=False)


class RetrainLog(Base):
    __tablename__ = "retrain_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    module = Column(String(50), nullable=False)
    records_count = Column(Integer, nullable=False)
    previous_f1 = Column(Float, nullable=True)
    new_f1 = Column(Float, nullable=True)
    status = Column(String(50), default="SUCCESS")
    summary = Column(Text, nullable=True)
