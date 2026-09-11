import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Text, Uuid, Enum as SAEnum, text
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from app.database import Base

alert_severity_enum = ENUM('low', 'moderate', 'high', 'critical', name='alert_severity_enum', create_type=False)

class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=True)
    severity: Mapped[str] = mapped_column(alert_severity_enum, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    ai_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_actions = mapped_column(JSONB, nullable=True)
    is_read: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    is_resolved: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("counsellors.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
