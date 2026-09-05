"""
Phase 3D Tests: Multimodal Fusion Layer
"""
import pytest
from app.risk_engine.schemas import RiskInput
from app.risk_engine.service import RiskEngineService
from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.registry import EngineRegistry

from ai.distress.schemas import FusionInput
from ai.distress.fusion import MultimodalFusionEngine
from ai.distress.config import config

def test_fusion_engine_baseline_only():
    engine = MultimodalFusionEngine()
    
    fusion_input = FusionInput(
        baseline_score=50.0,
        baseline_confidence=1.0,
        nlp_available=False,
        speech_available=False
    )
    
    result = engine.fuse(fusion_input)
    assert result.fused_risk_score == 50
    assert result.confidence == pytest.approx(1.0)
    assert "baseline" in result.modalities_used
    assert "nlp" in result.modalities_missing
    assert "speech" in result.modalities_missing
    assert not result.conflict_detected
    assert "Optional text and voice signals were unavailable." in result.explanation

def test_fusion_engine_all_modalities():
    engine = MultimodalFusionEngine()
    
    # Weights: baseline 0.6, nlp 0.2, speech 0.2
    # Baseline: 50 * 0.6 = 30
    # NLP: 80 * 0.2 = 16
    # Speech: 60 * 0.2 = 12
    # Sum = 58
    
    fusion_input = FusionInput(
        baseline_score=50.0,
        baseline_confidence=1.0,
        nlp_signal=80.0,
        nlp_confidence=1.0,
        nlp_available=True,
        speech_signal=60.0,
        speech_confidence=1.0,
        speech_available=True
    )
    
    result = engine.fuse(fusion_input)
    assert result.fused_risk_score == 58
    assert result.confidence == pytest.approx(1.0)
    assert not result.conflict_detected

def test_fusion_engine_missing_nlp():
    engine = MultimodalFusionEngine()
    
    # Baseline: 0.6 / 0.8 = 0.75 weight
    # Speech: 0.2 / 0.8 = 0.25 weight
    # 50 * 0.75 = 37.5
    # 60 * 0.25 = 15
    # Sum = 52.5 -> 52 or 53 depending on round
    
    fusion_input = FusionInput(
        baseline_score=50.0,
        baseline_confidence=1.0,
        nlp_available=False,
        speech_signal=60.0,
        speech_confidence=1.0,
        speech_available=True
    )
    
    result = engine.fuse(fusion_input)
    assert result.fused_risk_score == 52
    assert result.confidence == pytest.approx(1.0)
    assert not result.conflict_detected
    
def test_fusion_engine_low_confidence():
    engine = MultimodalFusionEngine()
    
    # Baseline weight: 0.6 * 1.0 = 0.6
    # NLP weight: 0.2 * 0.5 = 0.1
    # Speech weight: 0.2 * 0.0 = 0.0
    # Total effective weight = 0.7
    # Normalized weights: Baseline 0.6/0.7 = 0.857, NLP 0.1/0.7 = 0.143, Speech 0
    
    # Baseline score = 50 * 0.857 = 42.85
    # NLP score = 80 * 0.143 = 11.44
    # Speech score = 60 * 0 = 0
    # Total = 54.29 -> 54
    # Confidence: 1.0 * 0.857 + 0.5 * 0.143 = 0.928
    
    fusion_input = FusionInput(
        baseline_score=50.0,
        baseline_confidence=1.0,
        nlp_signal=80.0,
        nlp_confidence=0.5,
        nlp_available=True,
        speech_signal=60.0,
        speech_confidence=0.0,
        speech_available=True
    )
    
    result = engine.fuse(fusion_input)
    assert result.fused_risk_score == 54
    assert round(result.confidence, 2) == 0.93

def test_fusion_engine_conflict_detected():
    engine = MultimodalFusionEngine()
    
    fusion_input = FusionInput(
        baseline_score=20.0,
        baseline_confidence=1.0,
        nlp_signal=80.0,
        nlp_confidence=1.0,
        nlp_available=True,
        speech_available=False
    )
    
    result = engine.fuse(fusion_input)
    assert result.conflict_detected is True
    assert "meaningful disagreement" in result.explanation

def test_risk_engine_service_integration():
    registry = EngineRegistry()
    baseline = DeterministicBaselineEngine()
    registry.register(baseline, set_active=True)
    service = RiskEngineService(engine=baseline, registry=registry)
    
    # Max risk score = 25 / 50 = 50 risk_score
    risk_input = RiskInput(
        domain_scores={"mood": 5, "sleep": 5, "safety": 5, "social_support": 5, "legal_anxiety": 5}
    )
    result = service.evaluate(risk_input)
    
    assert result.risk_score == 50
    assert result.fusion_analysis is not None
    assert result.fusion_analysis["fused_risk_score"] == 50
    assert "baseline" in result.fusion_analysis["modalities_used"]
    assert result.risk_level.value == "high"  # 50 falls in high (25-74 mapped from 0-100) Wait, threshold mapped to 0-100: <=24 stable, <=48 moderate, <=74 high, else critical.
