"""
Phase 3B Tests: NLP / Text Analysis Engine

Tests verify:
1. TextAnalysisInput validation
2. TextAnalysisResult schema validation
3. Engine instantiation & metadata
4. Baseline unchanged when NLP unavailable/disabled
5. Graceful fallback on NLP failure
6. Integration with RiskEngineService
"""

import pytest
from pydantic import ValidationError

from app.schemas.check_in import CheckInCreateRequest, DomainScore
from app.risk_engine.schemas import RiskInput
from app.risk_engine.service import RiskEngineService
from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.registry import EngineRegistry
from ai.nlp.schemas import TextAnalysisInput, TextAnalysisResult
from ai.nlp.engine import MultilingualSentimentEngine


def test_input_validation_valid():
    """Valid text passes validation."""
    data = TextAnalysisInput(text="I am feeling sad today", language="en")
    assert data.text == "I am feeling sad today"
    assert data.language == "en"

def test_input_validation_empty():
    """Empty text is rejected."""
    with pytest.raises(ValidationError):
        TextAnalysisInput(text="")

def test_input_validation_too_long():
    """Extremely long text is rejected by Pydantic (max_length=2000)."""
    with pytest.raises(ValidationError):
        TextAnalysisInput(text="a" * 2001)

def test_result_schema():
    """TextAnalysisResult handles valid bounds."""
    res = TextAnalysisResult(
        available=True,
        language_detected="hi",
        distress_signal=0.85,
        sentiment_label="negative",
        sentiment_scores={"negative": 0.85, "neutral": 0.1, "positive": 0.05},
        confidence=0.85,
        model_name="test_model",
        model_version="1.0",
        explanation="Test explanation",
        limitations="Test limitation",
    )
    assert res.available is True
    assert res.distress_signal == 0.85

def test_engine_metadata():
    """MultilingualSentimentEngine has correct metadata."""
    engine = MultilingualSentimentEngine()
    assert engine.engine_name == "text_nlp"
    assert "1.0" in engine.engine_version

def test_nlp_unavailable_fallback():
    """When text is empty, the engine returns an unavailable result without crashing."""
    engine = MultilingualSentimentEngine()
    # Bypass pydantic validation for the test to see how engine handles empty
    # internally (e.g., if called directly bypassing schemas)
    res = engine.analyze(TextAnalysisInput(text="   "))
    assert res.available is False
    assert "empty" in res.explanation.lower()

def test_service_integration_no_text():
    """RiskEngineService with no text returns baseline only."""
    registry = EngineRegistry()
    baseline = DeterministicBaselineEngine()
    registry.register(baseline, set_active=True)
    service = RiskEngineService(engine=baseline, registry=registry)
    
    risk_input = RiskInput(domain_scores={"mood": 5, "sleep": 2, "safety": 0, "social_support": 1, "legal_anxiety": 2})
    result = service.evaluate(risk_input)
    
    assert result.nlp_analysis is None
    assert result.risk_level.value == "stable"

def test_check_in_request_optional_text():
    """CheckInCreateRequest accepts optional text_content."""
    req = CheckInCreateRequest(
        domain_scores=[DomainScore(domain="mood", score=5)],
        text_content="I feel anxious."
    )
    assert req.text_content == "I feel anxious."
    
    req2 = CheckInCreateRequest(
        domain_scores=[DomainScore(domain="mood", score=5)]
    )
    assert req2.text_content is None
