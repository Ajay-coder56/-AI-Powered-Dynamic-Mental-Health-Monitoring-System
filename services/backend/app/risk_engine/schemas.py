"""
Risk Engine Schemas — Standardized input/output models for risk evaluation.

These Pydantic models define the data contract between the API layer and
any risk engine implementation. They are implementation-independent.

DISCLAIMER: Risk scores produced by this system are engineering baselines.
They are NOT clinically validated diagnoses or predictions.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


# ---------- Enums ----------

class RiskLevel(str, Enum):
    """Risk levels matching the PostgreSQL risk_level_enum."""
    stable = "stable"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class CheckInMode(str, Enum):
    """Check-in modes matching the PostgreSQL check_in_mode_enum."""
    questionnaire = "questionnaire"
    voice = "voice"


class ExplanationType(str, Enum):
    """Type of explanation generation method."""
    deterministic_baseline = "deterministic_baseline"
    model_based = "model_based"
    hybrid = "hybrid"


# ---------- Valid domains ----------

VALID_DOMAINS = frozenset({"mood", "sleep", "safety", "social_support", "legal_anxiety"})


# ---------- Input ----------

class RiskInput(BaseModel):
    """
    Standardized input for any risk engine evaluation.

    Current baseline requires only: domain_scores, mode.
    Future AI fields are all Optional and ignored by the baseline engine.
    """

    # --- Required for baseline ---
    domain_scores: Dict[str, int] = Field(
        ...,
        description="Domain name -> distress score (0-10). "
                    "Valid domains: mood, sleep, safety, social_support, legal_anxiety.",
    )
    mode: CheckInMode = CheckInMode.questionnaire

    # --- Context (used by baseline if present) ---
    user_id: Optional[UUID] = None
    check_in_id: Optional[UUID] = None
    timestamp: Optional[datetime] = None
    mood: Optional[str] = None

    # --- Future NLP fields (Phase 3B) ---
    text_content: Optional[str] = Field(
        None, description="Optional text content from the user (e.g. journal entry, transcript)"
    )
    transcript: Optional[str] = Field(
        None, description="Optional transcript of a voice check-in"
    )
    audio_bytes: Optional[bytes] = Field(
        None, description="Raw audio bytes for Phase 3C voice check-ins"
    )

    # --- Future speech fields (Phase 3C) ---
    voice_features: Optional[Dict[str, Any]] = Field(
        None,
        description="Extracted voice/acoustic features for speech analysis.",
    )

    # --- Future temporal fields (Phase 3E) ---
    historical_features: Optional[Dict[str, Any]] = Field(
        None,
        description="Historical risk data for trend analysis.",
    )

    # --- Future contextual fields ---
    legal_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Legal/case context for contextual risk adjustment.",
    )

    # --- Extensibility ---
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Arbitrary metadata for future use.",
    )

    @field_validator("domain_scores")
    @classmethod
    def validate_domain_scores(cls, v: Dict[str, int]) -> Dict[str, int]:
        if not v:
            raise ValueError("domain_scores must not be empty")

        for domain, score in v.items():
            if domain not in VALID_DOMAINS:
                raise ValueError(
                    f"Invalid domain '{domain}'. "
                    f"Valid domains: {sorted(VALID_DOMAINS)}"
                )
            if not isinstance(score, int):
                raise ValueError(
                    f"Domain score for '{domain}' must be an integer, "
                    f"got {type(score).__name__}"
                )
            if not 0 <= score <= 10:
                raise ValueError(
                    f"Domain score for '{domain}' must be 0-10, got {score}"
                )

        return v


# ---------- Explanation ----------

class DomainContribution(BaseModel):
    """Individual domain's contribution to the risk assessment."""
    domain: str
    score: int
    max_score: int = 10
    label: str
    is_contributing_factor: bool
    detail: str


class RiskExplanation(BaseModel):
    """
    Structured explanation of a risk assessment result.

    For the baseline engine, explanations are deterministic and derived
    directly from the input domain scores. Future engines may provide
    SHAP/LIME-style explanations.

    DISCLAIMER: Explanations are engineering artifacts, not clinical interpretations.
    """
    model_config = {"protected_namespaces": ()}
    summary: str
    domain_contributions: List[DomainContribution]
    explanation_type: ExplanationType = ExplanationType.deterministic_baseline
    model_confidence: Optional[float] = Field(
        None,
        description="Model confidence score (0.0-1.0). Null for deterministic baseline.",
    )
    disclaimer: str = (
        "This explanation is generated by a deterministic engineering baseline. "
        "It is NOT a clinical interpretation, diagnosis, or prediction. "
        "No clinical validation has been performed."
    )


# ---------- Output ----------

class RiskResult(BaseModel):
    """
    Standardized output from any risk engine evaluation.

    This model is implementation-independent. The API layer consumes this
    regardless of whether the result came from deterministic rules, NLP,
    speech analysis, or a multimodal model.

    DISCLAIMER: Risk scores are engineering baselines, NOT clinical assessments.
    """

    # --- Core scores ---
    risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100 (higher = more risk)")
    wellbeing_score: int = Field(..., ge=0, le=100, description="Wellbeing score 0-100 (higher = better)")
    raw_score: int = Field(..., ge=0, description="Raw sum of domain scores")
    risk_level: RiskLevel

    # --- Factors ---
    contributing_factors: List[str] = Field(
        default_factory=list,
        description="Human-readable labels of domains scoring >= threshold.",
    )

    # --- Engine metadata ---
    engine_name: str
    engine_version: str
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Engine confidence (0.0-1.0). Null for deterministic baseline.",
    )

    # --- Component detail ---
    component_scores: Dict[str, int] = Field(
        default_factory=dict,
        description="Per-domain scores echoed from input.",
    )

    # --- Explanation ---
    explanation: RiskExplanation

    # --- Timing ---
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())

    # --- Phase 3B Additions ---
    nlp_analysis: Optional[Dict[str, Any]] = Field(
        None,
        description="NLP analysis result if text_content was provided."
    )

    # --- Phase 3C Additions ---
    speech_analysis: Optional[Dict[str, Any]] = Field(
        None,
        description="Speech analysis result if audio_bytes were provided."
    )

    # --- Phase 3D Additions ---
    fusion_analysis: Optional[Dict[str, Any]] = Field(
        None,
        description="Multimodal fusion analysis result."
    )
