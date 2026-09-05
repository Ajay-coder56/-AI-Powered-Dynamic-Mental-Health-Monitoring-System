"""
Risk Engine Interface — Abstract base classes for risk evaluation.

This module defines the contract that all risk engine implementations must follow.
The API layer depends only on these interfaces, never on concrete implementations.

DISCLAIMER: This is an engineering framework. Risk scores are NOT clinical diagnoses.
No clinical validation has been performed. Counsellor/human review remains necessary.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.risk_engine.schemas import RiskInput, RiskResult


class RiskEngine(ABC):
    """
    Abstract base class for all risk engine implementations.

    Every risk engine must:
    1. Accept a standardized RiskInput
    2. Return a standardized RiskResult
    3. Provide engine name and version metadata

    The API layer calls evaluate() through a RiskEngineService and never
    needs to know which concrete engine produced the result.
    """

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Unique identifier for this engine (e.g. 'deterministic_baseline')."""
        ...

    @property
    @abstractmethod
    def engine_version(self) -> str:
        """Semantic version string (e.g. '1.0')."""
        ...

    @abstractmethod
    def evaluate(self, risk_input: RiskInput) -> RiskResult:
        """
        Evaluate risk from a standardized input.

        Args:
            risk_input: Validated RiskInput containing domain scores and
                        optional future AI fields.

        Returns:
            RiskResult with scores, level, contributing factors,
            engine metadata, and explanation.
        """
        ...

    def engine_id(self) -> str:
        """Return a combined engine identifier: name@version."""
        return f"{self.engine_name}@{self.engine_version}"


# ======================================================================
# Future AI Engine Contracts
# These are NOT wired into the production path.
# They define the interface future Phase 3B/3C/3D modules will implement.
# ======================================================================

class TextAnalysisEngine(ABC):
    """
    Contract for NLP-based text analysis engines (Phase 3B).

    Will analyze free-text responses and transcripts for distress signals.
    NOT IMPLEMENTED — placeholder interface only.
    """

    @property
    @abstractmethod
    def engine_name(self) -> str: ...

    @property
    @abstractmethod
    def engine_version(self) -> str: ...

    @abstractmethod
    def analyze_text(self, text: str, language: Optional[str] = None) -> dict:
        """Analyze text for distress indicators. Returns raw analysis dict."""
        ...


class SpeechAnalysisEngine(ABC):
    """
    Contract for speech/voice analysis engines (Phase 3C).

    Will analyze voice features (pitch, energy, pauses) for distress signals.
    NOT IMPLEMENTED — placeholder interface only.
    """

    @property
    @abstractmethod
    def engine_name(self) -> str: ...

    @property
    @abstractmethod
    def engine_version(self) -> str: ...

    @abstractmethod
    def analyze_voice(self, voice_features: dict) -> dict:
        """Analyze voice features for distress indicators. Returns raw analysis dict."""
        ...


class TemporalRiskEngine(ABC):
    """
    Contract for temporal/historical risk analysis engines (Phase 3E).

    Will analyze risk trends over time for early warning detection.
    NOT IMPLEMENTED — placeholder interface only.
    """

    @property
    @abstractmethod
    def engine_name(self) -> str: ...

    @property
    @abstractmethod
    def engine_version(self) -> str: ...

    @abstractmethod
    def analyze_trend(self, historical_features: dict) -> dict:
        """Analyze historical risk data for trend detection. Returns raw analysis dict."""
        ...


class ExplainabilityEngine(ABC):
    """
    Contract for explainability engines (Phase 3F).

    Will provide SHAP/LIME-style explanations for AI model outputs.
    NOT IMPLEMENTED — placeholder interface only.
    """

    @property
    @abstractmethod
    def engine_name(self) -> str: ...

    @property
    @abstractmethod
    def engine_version(self) -> str: ...

    @abstractmethod
    def explain(self, risk_result: RiskResult, risk_input: RiskInput) -> dict:
        """Generate model explanation for a given risk result. Returns explanation dict."""
        ...
