from typing import Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class TextAnalysisInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Free-text to analyze")
    language: Optional[str] = Field(None, description="ISO 639-1 code if known")
    user_id: Optional[UUID] = None
    check_in_id: Optional[UUID] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict] = None

class TextAnalysisResult(BaseModel):
    available: bool = Field(..., description="Whether NLP analysis was successfully run")
    language_detected: Optional[str] = None
    distress_signal: Optional[float] = Field(None, ge=0.0, le=1.0, description="0.0 = no distress, 1.0 = high distress language")
    sentiment_label: Optional[str] = None
    sentiment_scores: Optional[Dict[str, float]] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    model_name: str
    model_version: str
    inference_time_ms: Optional[float] = None
    explanation: str
    limitations: str
    disclaimer: str = (
        "This is an NLP distress signal based on negative sentiment probability. "
        "It is an engineering prototype and NOT a clinical diagnosis."
    )
