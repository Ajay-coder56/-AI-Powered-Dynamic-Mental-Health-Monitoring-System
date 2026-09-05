from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CaseBase(BaseModel):
    name: str
    age: int
    phone: str
    language: str
    city: str
    case_type: str
    court: Optional[str] = None
    next_hearing: Optional[datetime] = None

class CaseCreate(CaseBase):
    pass

class CaseResponse(CaseBase):
    id: int
    case_id: str
    risk_score: int
    risk_level: str
    last_check_in: Optional[datetime]
    status: str
    counsellor_id: Optional[int]
    streak: int
    sessions: int
    trend: str
    class Config:
        from_attributes = True
