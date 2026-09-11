from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class AlertPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(str, Enum):
    RISK_THRESHOLD = "RISK_THRESHOLD"
    WORSENING_TRAJECTORY = "WORSENING_TRAJECTORY"
    PERSISTENT_WORSENING = "PERSISTENT_WORSENING"
    SIGNAL_CONFLICT = "SIGNAL_CONFLICT"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

class AlertEngineResult(BaseModel):
    should_alert: bool
    priority: Optional[AlertPriority] = None
    alert_type: Optional[AlertType] = None
    title: Optional[str] = None
    reason: Optional[str] = None
    recommended_actions: List[str] = Field(default_factory=list)
