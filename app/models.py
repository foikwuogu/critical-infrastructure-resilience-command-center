from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

def now():
    return datetime.now(timezone.utc)

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    asset_type: Mapped[str] = mapped_column(String(40))
    zone: Mapped[str] = mapped_column(String(50))
    criticality: Mapped[int] = mapped_column(Integer)
    health: Mapped[float] = mapped_column(Float)
    failure_probability: Mapped[float] = mapped_column(Float)
    rul_hours: Mapped[float] = mapped_column(Float)
    anomaly_score: Mapped[float] = mapped_column(Float)
    crypto_algorithm: Mapped[str] = mapped_column(String(60))
    pqc_status: Mapped[str] = mapped_column(String(30))
    pqc_readiness: Mapped[float] = mapped_column(Float)
    identity_trust: Mapped[float] = mapped_column(Float)
    least_privilege: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(30), default="operational")

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    asset_id: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(30))
    severity: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    operational_impact: Mapped[float] = mapped_column(Float, default=0)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)

class ScenarioRun(Base):
    __tablename__ = "scenario_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    scenario: Mapped[str] = mapped_column(String(60))
    resilience_before: Mapped[float] = mapped_column(Float)
    resilience_after: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(Text)
