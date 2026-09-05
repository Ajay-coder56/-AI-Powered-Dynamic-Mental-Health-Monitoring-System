from pydantic import BaseModel
from datetime import datetime
from typing import List

class AlertBase(BaseModel):
    severity: str
    type: str
    title: str
    patient_name: str
    message: str
    ai_explanation: str
    actions: List[str]

class AlertResponse(AlertBase):
    id: int
    case_id: int
    time: datetime
    is_read: bool
    is_resolved: bool
    class Config:
        from_attributes = True
