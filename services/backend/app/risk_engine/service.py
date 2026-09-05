"""
Risk Engine Service — Service layer between API routes and risk engine implementations.

This module provides the RiskEngineService that API routes call to evaluate risk.
The service delegates to the active RiskEngine implementation, ensuring the API
layer never directly depends on a specific engine.

Architecture:
    API Route -> RiskEngineService -> RiskEngine (interface) -> DeterministicBaselineEngine

Future:
    API Route -> RiskEngineService -> MultimodalRiskEngine
                                      ├── Baseline
                                      ├── NLP
                                      ├── Speech
                                      └── Temporal
"""

from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.interface import RiskEngine
from app.risk_engine.registry import EngineRegistry
from app.risk_engine.schemas import RiskInput, RiskResult


class RiskEngineService:
    """
    Service layer for risk evaluation.

    Wraps a RiskEngine implementation and provides a clean evaluate() method
    for the API layer. Manages the engine lifecycle and registry.
    """
    
    # Explicit mapping for the 0-100 fused risk score.
    # Scaled exactly from the 0-50 raw score thresholds:
    # Raw 12/50 -> 24% (stable)
    # Raw 24/50 -> 48% (moderate)
    # Raw 37/50 -> 74% (high)
    # Raw 50/50 -> 100% (critical)
    FUSED_RISK_THRESHOLDS = [
        (24, "stable"),
        (48, "moderate"),
        (74, "high"),
        (100, "critical"),
    ]

    def __init__(self, engine: RiskEngine, registry: EngineRegistry) -> None:
        self._engine = engine
        self._registry = registry

    @property
    def active_engine(self) -> RiskEngine:
        """The currently active risk engine."""
        return self._engine

    @property
    def registry(self) -> EngineRegistry:
        """The engine registry."""
        return self._registry

    def evaluate(self, risk_input: RiskInput) -> RiskResult:
        """
        Evaluate risk using the active engine.

        If text_content is present, also runs the NLP engine (Phase 3B)
        and attaches the signal to the result.

        Args:
            risk_input: Validated RiskInput.

        Returns:
            Standardized RiskResult from the active engine, with optional NLP.
        """
        # 1. Run Baseline Engine
        result = self._engine.evaluate(risk_input)

        # 2. Run Optional NLP Engine
        if risk_input.text_content:
            try:
                # Retrieve the NLP engine dynamically from registry or fallback to direct import
                try:
                    nlp_engine = self._registry.get_engine("text_nlp")
                except KeyError:
                    # If not registered explicitly, try to load it
                    from ai.nlp.engine import MultilingualSentimentEngine
                    nlp_engine = MultilingualSentimentEngine()
                    self._registry.register(nlp_engine, set_active=False)

                # Run NLP
                nlp_dict = nlp_engine.analyze_text(risk_input.text_content)
                result.nlp_analysis = nlp_dict
            except Exception as e:
                # Failsafe: if NLP crashes completely, baseline still survives
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"NLP Engine hard failure: {e}")
                result.nlp_analysis = {
                    "available": False,
                    "explanation": f"NLP hard failure: {e}",
                    "limitations": "Analysis skipped."
                }

        # 3. Run Optional Speech Engine
        if getattr(risk_input, 'audio_bytes', None):
            try:
                try:
                    speech_engine = self._registry.get_engine("acoustic_features")
                except KeyError:
                    from ai.speech.engine import AcousticFeatureEngine
                    speech_engine = AcousticFeatureEngine()
                    self._registry.register(speech_engine, set_active=False)

                # Run speech analysis
                speech_dict = speech_engine.analyze_voice({"audio_bytes": risk_input.audio_bytes})
                result.speech_analysis = speech_dict
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Speech Engine hard failure: {e}")
                result.speech_analysis = {
                    "available": False,
                    "explanation": f"Speech hard failure: {e}",
                    "limitations": "Analysis skipped."
                }

        # 4. Multimodal Fusion Engine (Phase 3D)
        from ai.distress.schemas import FusionInput
        from ai.distress.fusion import MultimodalFusionEngine
        
        # Extract variables for fusion
        baseline_score = float(result.risk_score)
        baseline_confidence = 1.0  # Deterministic baseline is considered 100% reliable for its weight
        
        nlp_available = False
        nlp_signal = None
        nlp_confidence = None
        
        if result.nlp_analysis and result.nlp_analysis.get("available") is True:
            distress = result.nlp_analysis.get("distress_signal")
            if distress is not None:
                nlp_signal = float(distress) * 100.0  # Normalize to 0-100
                nlp_confidence = result.nlp_analysis.get("confidence", 1.0)
                nlp_available = True
                
        speech_available = False
        speech_signal = None
        speech_confidence = None
        
        if result.speech_analysis and result.speech_analysis.get("available") is True:
            distress = result.speech_analysis.get("voice_signal")
            if distress is not None:
                speech_signal = float(distress) * 100.0  # Normalize to 0-100
                speech_confidence = result.speech_analysis.get("confidence", 1.0)
                speech_available = True
                
        fusion_input = FusionInput(
            baseline_score=baseline_score,
            nlp_signal=nlp_signal,
            speech_signal=speech_signal,
            baseline_confidence=baseline_confidence,
            nlp_confidence=nlp_confidence,
            speech_confidence=speech_confidence,
            nlp_available=nlp_available,
            speech_available=speech_available
        )
        
        fusion_engine = MultimodalFusionEngine()
        fusion_result = fusion_engine.fuse(fusion_input)
        
        # 5. Update Result with Fused Values
        result.risk_score = fusion_result.fused_risk_score
        result.wellbeing_score = 100 - fusion_result.fused_risk_score
        result.confidence = fusion_result.confidence
        
        # Add fusion analysis dict (requires adding to RiskResult schema)
        result.fusion_analysis = fusion_result.model_dump()
        
        # Re-evaluate Risk Level based on fused_risk_score explicitly mapped to 0-100 thresholds.
        from app.risk_engine.schemas import RiskLevel
        
        result.risk_level = RiskLevel.critical  # Default fallback
        for threshold, level in self.FUSED_RISK_THRESHOLDS:
            if result.risk_score <= threshold:
                result.risk_level = RiskLevel(level)
                break
            
        # Update explanation with fusion context
        result.explanation.summary = fusion_result.explanation
        
        # Update contributing factors
        if "nlp" in fusion_result.modalities_used and fusion_result.modality_contributions["nlp"].contribution > 10.0:
            if "negative_sentiment_signal" not in result.contributing_factors:
                result.contributing_factors.append("negative_sentiment_signal")
                
        if "speech" in fusion_result.modalities_used and fusion_result.modality_contributions["speech"].contribution > 10.0:
            if "voice_acoustic_signal" not in result.contributing_factors:
                result.contributing_factors.append("voice_acoustic_signal")

        return result


# ======================================================================
# Factory — singleton-style service construction
# ======================================================================

_service_instance: RiskEngineService | None = None


def get_risk_engine_service() -> RiskEngineService:
    """
    Get or create the RiskEngineService singleton.

    On first call, creates the registry, registers the deterministic
    baseline engine as the active engine, and returns the service.

    Returns:
        Configured RiskEngineService instance.
    """
    global _service_instance

    if _service_instance is None:
        registry = EngineRegistry()
        baseline = DeterministicBaselineEngine()
        registry.register(baseline, set_active=True)

        _service_instance = RiskEngineService(engine=baseline, registry=registry)

    return _service_instance
