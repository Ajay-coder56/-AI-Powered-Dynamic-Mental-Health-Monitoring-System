from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class CounsellorResponse(BaseModel):
    id: UUID
    email: str
    name: str
    title: Optional[str] = None
    city: Optional[str] = None
    is_active: bool
    created_at: datetime
    role: str = "counsellor"

    model_config = ConfigDict(from_attributes=True)
