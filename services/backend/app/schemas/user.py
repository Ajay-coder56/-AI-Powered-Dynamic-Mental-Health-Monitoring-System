from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    """Non-sensitive user profile response."""
    id: UUID
    name: str
    age: Optional[int] = None
    language: Optional[str] = None
    case_id: Optional[UUID] = None
    consent_given: bool = False
    consent_date: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
