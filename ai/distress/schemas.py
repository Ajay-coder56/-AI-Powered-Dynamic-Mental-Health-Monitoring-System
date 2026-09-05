from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class FusionInput(BaseModel):
    baseline_score: float = Field(..., ge=0, le=100)
    nlp_signal: Optional[float] = Field(None, ge=0, le=100)
    speech_signal: Optional[float] = Field(None, ge=0, le=100)
    
    baseline_confidence: float = Field(1.0, ge=0, le=1.0)
    nlp_confidence: Optional[float] = Field(None, ge=0, le=1.0)
    speech_confidence: Optional[float] = Field(None, ge=0, le=1.0)
    
    nlp_available: bool = False
    speech_available: bool = False

class ModalityContribution(BaseModel):
    score: float
    weight: float
    contribution: float
    confidence: float
    available: bool

class FusionResult(BaseModel):
    fused_risk_score: int = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0.0, le=1.0)
    modality_contributions: Dict[str, ModalityContribution]
    modalities_used: List[str]
    modalities_missing: List[str]
    conflict_detected: bool
    explanation: str
    limitations: str = (
        "Phase 3D fusion is an engineering prototype and is not clinically validated. "
        "The resulting score must not be interpreted as a diagnosis or medical prediction."
    )
