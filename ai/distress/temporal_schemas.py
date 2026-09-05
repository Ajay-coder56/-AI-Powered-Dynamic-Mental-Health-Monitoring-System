from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class TemporalObservation(BaseModel):
    timestamp: datetime
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str

class TemporalInput(BaseModel):
    user_id: str
    observations: List[TemporalObservation]

class TemporalRiskResult(BaseModel):
    available: bool = Field(..., description="Whether sufficient history exists for temporal analysis")
    observation_count: int
    analysis_window_days: Optional[float] = None
    
    # Deterministic Features
    current_score: Optional[int] = None
    previous_score: Optional[int] = None
    mean_score: Optional[int] = None
    minimum_score: Optional[int] = None
    maximum_score: Optional[int] = None
    range: Optional[int] = None
    slope_per_day: Optional[float] = None
    
    # Categorical logic
    trend: str = Field(..., description="improving, stable, worsening, insufficient_data")
    persistence: Optional[bool] = None
    
    # Engineering output
    early_warning_score: Optional[int] = Field(None, ge=0, le=100)
    temporal_status: str = Field(..., description="no_signal, watch, elevated, strong, unavailable")
    data_quality: str = Field(..., description="insufficient, limited, adequate, strong")
    
    # Human readable
    explanation: str
    limitations: str = (
        "Phase 3E provides a deterministic longitudinal engineering signal based on observed "
        "historical trends. It is not a clinically validated predictive model and must not "
        "be interpreted as a diagnosis or guaranteed forecast of future mental-health outcomes."
    )
