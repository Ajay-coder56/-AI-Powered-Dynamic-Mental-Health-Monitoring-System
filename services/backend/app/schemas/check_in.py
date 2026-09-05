from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

# ---------- Enums matching PostgreSQL ----------

class CheckInMode(str, Enum):
    questionnaire = "questionnaire"
    voice = "voice"

class DomainName(str, Enum):
    mood = "mood"
    sleep = "sleep"
    safety = "safety"
    social_support = "social_support"
    legal_anxiety = "legal_anxiety"

# ---------- Request schemas ----------

class DomainScore(BaseModel):
    """Individual domain assessment score (0-10)."""
    domain: DomainName
    score: int

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: int) -> int:
        if not 0 <= v <= 10:
            raise ValueError("Domain score must be between 0 and 10")
        return v

class CheckInCreateRequest(BaseModel):
    """Request body for submitting a check-in assessment."""
    mode: CheckInMode = CheckInMode.questionnaire
    mood: Optional[str] = None
    answers: Optional[Dict[str, Any]] = None
    domain_scores: List[DomainScore]
    duration_seconds: Optional[int] = None
    text_content: Optional[str] = None

    @field_validator("domain_scores")
    @classmethod
    def validate_domain_scores(cls, v: List[DomainScore]) -> List[DomainScore]:
        if len(v) == 0:
            raise ValueError("At least one domain score is required")
        domains_seen = set()
        for ds in v:
            if ds.domain in domains_seen:
                raise ValueError(f"Duplicate domain: {ds.domain}")
            domains_seen.add(ds.domain)
        return v

# ---------- Response schemas ----------

class DomainScoreResponse(BaseModel):
    domain: str
    score: int

    model_config = ConfigDict(from_attributes=True)

class CheckInResultResponse(BaseModel):
    """Result of a check-in including deterministic risk assessment.

    NOTE: This is an engineering/demo baseline risk calculation.
    It is NOT a clinically validated assessment.
    """
    check_in_id: UUID
    raw_score: int
    wellbeing_score: int
    risk_score: int
    risk_level: str
    mood: Optional[str] = None
    contributing_factors: List[str]
    domain_scores: List[DomainScoreResponse]
    created_at: datetime
    disclaimer: str = (
        "This is a deterministic engineering baseline. "
        "It is NOT a clinically validated diagnosis or prediction."
    )
    nlp_analysis: Optional[Dict[str, Any]] = None
    speech_analysis: Optional[Dict[str, Any]] = None
    fusion_analysis: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class CheckInHistoryItem(BaseModel):
    """Single item in check-in history list."""
    id: UUID
    mode: str
    raw_score: Optional[int] = None
    wellbeing_score: Optional[int] = None
    risk_level: Optional[str] = None
    mood: Optional[str] = None
    duration_seconds: Optional[int] = None
    created_at: datetime
    domain_scores: List[DomainScoreResponse] = []

    model_config = ConfigDict(from_attributes=True)
