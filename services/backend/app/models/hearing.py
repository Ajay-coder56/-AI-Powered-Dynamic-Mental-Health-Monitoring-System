import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Date, Text, Uuid
from app.database import Base

class Hearing(Base):
    __tablename__ = "hearings"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=True)
    hearing_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    hearing_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    court: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
