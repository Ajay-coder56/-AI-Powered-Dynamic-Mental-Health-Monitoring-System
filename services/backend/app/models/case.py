import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, Date, Uuid, text
from sqlalchemy.dialects.postgresql import ENUM
from app.database import Base

# PostgreSQL enum types (already exist in the database — DO NOT recreate)
risk_level_enum = ENUM('stable', 'moderate', 'high', 'critical', name='risk_level_enum', create_type=False)
status_enum = ENUM('active', 'monitoring', 'resolved', name='status_enum', create_type=False)
trend_enum = ENUM('improving', 'stable', 'worsening', name='trend_enum', create_type=False)

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    case_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    victim_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    counsellor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("counsellors.id", ondelete="SET NULL"), nullable=True)
    case_type: Mapped[str] = mapped_column(String(255), nullable=False)
    court: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    risk_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[Optional[str]] = mapped_column(risk_level_enum, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(status_enum, server_default=text("'active'"))
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    next_hearing_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    streak: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    total_sessions: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    trend: Mapped[Optional[str]] = mapped_column(trend_enum, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

