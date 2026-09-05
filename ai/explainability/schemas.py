from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DomainContribution(BaseModel):
    domain: str
    score: int = Field(description="Score out of 10")
    contribution_level: str = Field(description="High, Moderate, Low")
    reason: str

class ModalitySummary(BaseModel):
    modality: str
    score: Optional[int] = None
    confidence: Optional[float] = None
    weight: Optional[float] = None
    availability: str = Field(description="Available, Unavailable")
    contribution: str = Field(description="Dominant, Moderate, Minor, None")
    reason: str

class TemporalSummary(BaseModel):
    current_risk: int
    trend: str
    slope_per_day: Optional[float] = None
    persistence: bool
    recent_change: Optional[int] = None
    early_warning_status: str
    data_quality: str
    explanation: str

class ExplainabilityInput(BaseModel):
    risk_score: int
    risk_level: str
    wellbeing_score: int
    domain_scores: Dict[str, int]
    modality_contributions: List[dict] # From Phase 3D ModalityContribution
    conflict_detected: bool
    temporal_result: Optional[dict] = None # From Phase 3E TemporalRiskResult
    
class ExplainabilityResult(BaseModel):
    summary: str
    risk_score: int
    risk_level: str
    top_contributing_factors: List[DomainContribution]
    modality_contributions: List[ModalitySummary]
    missing_modalities: List[str]
    conflicting_modalities: bool
    temporal_summary: Optional[TemporalSummary] = None
    reliability: str
    human_review_note: str
    limitations: str
