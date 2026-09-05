import pytest
from unittest.mock import patch
from app.risk_engine.schemas import RiskInput, RiskLevel
from app.risk_engine.service import RiskEngineService
from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.registry import EngineRegistry

@pytest.fixture
def service():
    registry = EngineRegistry()
    baseline = DeterministicBaselineEngine()
    registry.register(baseline, set_active=True)
    return RiskEngineService(engine=baseline, registry=registry)

@pytest.mark.parametrize("fused_score, expected_level", [
    (0, RiskLevel.stable),      # lowest stable
    (24, RiskLevel.stable),     # highest stable
    (25, RiskLevel.moderate),   # first moderate
    (48, RiskLevel.moderate),   # highest moderate
    (49, RiskLevel.high),       # first high
    (74, RiskLevel.high),       # highest high
    (75, RiskLevel.critical),   # first critical
    (100, RiskLevel.critical),  # maximum score
])
def test_fused_risk_score_boundaries(service, fused_score, expected_level):
    """
    Tests the precise boundary mapping of the 0-100 fused_risk_score
    into the RiskLevel enum, ensuring the 0-50 raw score thresholds
    are correctly scaled and non-linearities are handled safely.
    """
    from ai.distress.schemas import FusionResult
    
    # We mock the fusion engine's output to precisely test the boundary mapping
    # in RiskEngineService, decoupling it from the baseline math.
    with patch("ai.distress.fusion.MultimodalFusionEngine.fuse") as mock_fuse:
        mock_fuse.return_value = FusionResult(
            fused_risk_score=fused_score,
            confidence=1.0,
            modality_contributions={},
            modalities_used=["baseline"],
            modalities_missing=["nlp", "speech"],
            conflict_detected=False,
            explanation="Test boundary explanation"
        )
        
        # Input doesn't matter since we mocked the fusion result
        risk_input = RiskInput(
            domain_scores={"mood": 0, "sleep": 0, "safety": 0, "social_support": 0, "legal_anxiety": 0}
        )
        
        result = service.evaluate(risk_input)
        
        assert result.risk_score == fused_score
        assert result.risk_level == expected_level

