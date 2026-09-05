import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, Uuid, text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from app.database import Base

# PostgreSQL enum types (already exist in the database — DO NOT recreate)
check_in_mode_enum = ENUM('questionnaire', 'voice', name='check_in_mode_enum', create_type=False)
risk_level_enum = ENUM('stable', 'moderate', 'high', 'critical', name='risk_level_enum', create_type=False)
domain_enum = ENUM('mood', 'sleep', 'safety', 'social_support', 'legal_anxiety', name='domain_enum', create_type=False)

class CheckInSession(Base):
    __tablename__ = "check_ins"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=True)
    mode: Mapped[str] = mapped_column(check_in_mode_enum, nullable=False)
    answers = mapped_column(JSONB, nullable=True)
    raw_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    wellbeing_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[Optional[str]] = mapped_column(risk_level_enum, nullable=True)
    mood: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class CheckInDomain(Base):
    __tablename__ = "check_in_domains"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_in_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("check_ins.id", ondelete="CASCADE"), nullable=True)
    domain: Mapped[str] = mapped_column(domain_enum, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
