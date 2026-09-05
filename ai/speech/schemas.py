from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SpeechAnalysisInput(BaseModel):
    """Input for speech analysis containing the raw audio bytes."""
    audio_bytes: bytes
    filename: Optional[str] = None
    content_type: Optional[str] = None
    language: Optional[str] = None

class SpeechAnalysisResult(BaseModel):
    """Output of speech analysis."""
    available: bool = Field(..., description="Whether voice analysis succeeded")
    duration_seconds: Optional[float] = None
    voice_signal: Optional[float] = Field(None, ge=0.0, le=1.0, description="Normalized distress signal based on acoustic features")
    confidence: Optional[float] = None
    feature_summary: Optional[Dict[str, float]] = None
    extractor_name: str
    extractor_version: str
    explanation: str
    limitations: str
    disclaimer: str = (
        "This is an engineering prototype signal based on acoustic features. "
        "It is NOT a clinically validated biomarker or diagnosis."
    )
