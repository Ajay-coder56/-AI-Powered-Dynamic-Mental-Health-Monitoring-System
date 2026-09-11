from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

class AlertBase(BaseModel):
    severity: str
    type: str
    title: str
    message: str
    ai_explanation: Optional[str] = None
    recommended_actions: Optional[List[str]] = None

class AlertResponse(AlertBase):
    id: uuid.UUID
    case_id: uuid.UUID
    created_at: datetime
    resolved_at: Optional[datetime] = None
    is_read: bool
    is_resolved: bool
    resolved_by: Optional[uuid.UUID] = None
    
    class Config:
        from_attributes = True

