from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ConsentRequest(BaseModel):
    """Request body for granting consent."""
    consent_type: str = "data_collection_and_assessment"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class ConsentResponse(BaseModel):
    """Response after recording consent."""
    id: UUID
    user_id: UUID
    consent_type: str
    created_at: datetime
    user_consent_given: bool
    user_consent_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
