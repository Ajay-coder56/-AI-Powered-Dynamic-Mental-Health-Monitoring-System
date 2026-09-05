"""
Phase 3A Tests: Risk Engine Foundation

Tests verify:
1.  DeterministicBaselineEngine instantiation
2.  Valid RiskInput produces RiskResult
3.  Baseline score matches original calculate_risk() output exactly
4.  Threshold behavior preserved (stable, moderate, high, critical)
5.  Contributing factors preserved
6.  Engine metadata correct
7.  Explanation generated with domain contributions
8.  Missing optional future AI fields don't break baseline
9.  Invalid domain scores rejected
10. Invalid domain names rejected
11. Risk result values within expected ranges
12. RiskEngineService works with baseline engine
13. EngineRegistry tracks engines correctly
14. Explanation disclaimer present and non-clinical
"""

import pytest
from pydantic import ValidationError

from app.services.risk_calculator import calculate_risk
from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.interface import RiskEngine
from app.risk_engine.registry import EngineRegistry
from app.risk_engine.schemas import RiskInput, RiskResult, RiskExplanation
from app.risk_engine.service import RiskEngineService


# ======================================================================
# Test data — matches Phase 2B test vectors
# ======================================================================

LOW_SCORES = {"mood": 1, "sleep": 2, "safety": 0, "social_support": 1, "legal_anxiety": 2}
MODERATE_SCORES = {"mood": 5, "sleep": 4, "safety": 3, "social_support": 4, "legal_anxiety": 5}
HIGH_SCORES = {"mood": 7, "sleep": 8, "safety": 5, "social_support": 6, "legal_anxiety": 7}
CRITICAL_SCORES = {"mood": 9, "sleep": 8, "safety": 8, "social_support": 7, "legal_anxiety": 9}
CONTRIBUTING_SCORES = {"mood": 2, "sleep": 9, "safety": 1, "social_support": 0, "legal_anxiety": 8}


def _make_input(domain_scores: dict[str, int]) -> RiskInput:
    """Helper to create a RiskInput from domain scores."""
    return RiskInput(domain_scores=domain_scores)


# ======================================================================
# 1. Engine instantiation
# ======================================================================

def test_baseline_engine_instantiation():
    """DeterministicBaselineEngine can be instantiated and is a RiskEngine."""
    engine = DeterministicBaselineEngine()
    assert isinstance(engine, RiskEngine)
    assert isinstance(engine, DeterministicBaselineEngine)


# ======================================================================
# 2. Valid input produces valid output
# ======================================================================

def test_valid_input_produces_result():
    """Valid RiskInput produces a RiskResult with all required fields."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(LOW_SCORES))

    assert isinstance(result, RiskResult)
    assert isinstance(result.risk_score, int)
    assert isinstance(result.wellbeing_score, int)
    assert isinstance(result.raw_score, int)
    assert result.risk_level is not None
    assert isinstance(result.contributing_factors, list)
    assert isinstance(result.engine_name, str)
    assert isinstance(result.engine_version, str)
    assert isinstance(result.explanation, RiskExplanation)
    assert result.timestamp is not None


# ======================================================================
# 3. Baseline score matches original calculate_risk() exactly
# ======================================================================

@pytest.mark.parametrize(
    "scores",
    [LOW_SCORES, MODERATE_SCORES, HIGH_SCORES, CRITICAL_SCORES, CONTRIBUTING_SCORES],
    ids=["low", "moderate", "high", "critical", "contributing"],
)
def test_baseline_matches_original(scores):
    """Engine output must match the original calculate_risk() function exactly."""
    # Original Phase 2 result
    original = calculate_risk(scores)

    # New engine result
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(scores))

    assert result.raw_score == original["raw_score"]
    assert result.risk_score == original["risk_score"]
    assert result.wellbeing_score == original["wellbeing_score"]
    assert result.risk_level.value == original["risk_level"]
    assert result.contributing_factors == original["contributing_factors"]


# ======================================================================
# 4. Threshold behavior preserved
# ======================================================================

def test_threshold_stable():
    """Low scores -> stable risk level."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(LOW_SCORES))
    assert result.risk_level.value == "stable"


def test_threshold_moderate():
    """Mixed scores -> moderate risk level."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(MODERATE_SCORES))
    assert result.risk_level.value == "moderate"


def test_threshold_high():
    """High scores -> high risk level."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(HIGH_SCORES))
    assert result.risk_level.value == "high"


def test_threshold_critical():
    """Maximum scores -> critical risk level."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(CRITICAL_SCORES))
    assert result.risk_level.value == "critical"


# ======================================================================
# 5. Contributing factors preserved
# ======================================================================

def test_contributing_factors():
    """Contributing factors only include domains >= 7."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(CONTRIBUTING_SCORES))

    assert "sleep difficulty" in result.contributing_factors
    assert "legal anxiety" in result.contributing_factors
    assert "low mood / emotional distress" not in result.contributing_factors


def test_no_contributing_factors_when_all_low():
    """No contributing factors when all domains are below threshold."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(LOW_SCORES))
    assert result.contributing_factors == []


# ======================================================================
# 6. Engine metadata correct
# ======================================================================

def test_engine_metadata():
    """Engine name, version, and ID are correct."""
    engine = DeterministicBaselineEngine()
    assert engine.engine_name == "deterministic_baseline"
    assert engine.engine_version == "1.0"
    assert engine.engine_id() == "deterministic_baseline@1.0"

    result = engine.evaluate(_make_input(LOW_SCORES))
    assert result.engine_name == "deterministic_baseline"
    assert result.engine_version == "1.0"
    assert result.confidence is None  # Deterministic — no probabilistic confidence


# ======================================================================
# 7. Explanation generated
# ======================================================================

def test_explanation_generated():
    """Explanation is generated with domain contributions."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(HIGH_SCORES))

    explanation = result.explanation
    assert explanation.summary is not None
    assert len(explanation.summary) > 0
    assert len(explanation.domain_contributions) == 5  # all 5 domains
    assert explanation.explanation_type.value == "deterministic_baseline"
    assert explanation.model_confidence is None

    # Verify domain contributions contain correct info
    sleep_contrib = next(
        dc for dc in explanation.domain_contributions if dc.domain == "sleep"
    )
    assert sleep_contrib.score == 8
    assert sleep_contrib.is_contributing_factor is True
    assert sleep_contrib.max_score == 10


# ======================================================================
# 8. Missing optional future AI fields don't break baseline
# ======================================================================

def test_future_fields_optional():
    """RiskInput with no future AI fields works for baseline evaluation."""
    # Only domain_scores provided — all future fields default to None
    risk_input = RiskInput(domain_scores=LOW_SCORES)
    assert risk_input.text_content is None
    assert risk_input.transcript is None
    assert risk_input.voice_features is None
    assert risk_input.historical_features is None
    assert risk_input.legal_context is None
    assert risk_input.metadata is None

    engine = DeterministicBaselineEngine()
    result = engine.evaluate(risk_input)
    assert result.risk_level.value == "stable"


def test_future_fields_present_but_ignored():
    """RiskInput with future AI fields present — baseline ignores them."""
    risk_input = RiskInput(
        domain_scores=LOW_SCORES,
        text_content="I feel very sad and hopeless",
        transcript="Transcript text here",
        voice_features={"pitch_mean": 120.5, "energy_std": 0.3},
        historical_features={"past_risk_levels": ["stable", "moderate"]},
        legal_context={"case_type": "custody"},
        metadata={"source": "test"},
    )
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(risk_input)

    # Baseline produces same result regardless of future fields
    baseline_only = engine.evaluate(_make_input(LOW_SCORES))
    assert result.risk_score == baseline_only.risk_score
    assert result.risk_level == baseline_only.risk_level


# ======================================================================
# 9. Invalid domain scores rejected
# ======================================================================

def test_invalid_score_too_high():
    """Domain score > 10 is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RiskInput(domain_scores={"mood": 15, "sleep": 5, "safety": 3, "social_support": 2, "legal_anxiety": 1})
    assert "must be 0-10" in str(exc_info.value)


def test_invalid_score_negative():
    """Negative domain score is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RiskInput(domain_scores={"mood": -1, "sleep": 5, "safety": 3, "social_support": 2, "legal_anxiety": 1})
    assert "must be 0-10" in str(exc_info.value)


def test_empty_domain_scores():
    """Empty domain_scores is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RiskInput(domain_scores={})
    assert "must not be empty" in str(exc_info.value)


# ======================================================================
# 10. Invalid domain names rejected
# ======================================================================

def test_invalid_domain_name():
    """Unknown domain name is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RiskInput(domain_scores={"mood": 5, "nonexistent_domain": 3})
    assert "Invalid domain" in str(exc_info.value)


# ======================================================================
# 11. Risk result within expected ranges
# ======================================================================

@pytest.mark.parametrize(
    "scores",
    [LOW_SCORES, MODERATE_SCORES, HIGH_SCORES, CRITICAL_SCORES],
    ids=["low", "moderate", "high", "critical"],
)
def test_result_ranges(scores):
    """Risk and wellbeing scores are within 0-100."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(scores))

    assert 0 <= result.risk_score <= 100
    assert 0 <= result.wellbeing_score <= 100
    assert result.raw_score >= 0
    assert result.risk_level.value in ("stable", "moderate", "high", "critical")


# ======================================================================
# 12. RiskEngineService works with baseline engine
# ======================================================================

def test_service_evaluate():
    """RiskEngineService correctly delegates to the baseline engine."""
    registry = EngineRegistry()
    engine = DeterministicBaselineEngine()
    registry.register(engine, set_active=True)
    service = RiskEngineService(engine=engine, registry=registry)

    result = service.evaluate(_make_input(HIGH_SCORES))
    assert isinstance(result, RiskResult)
    assert result.risk_level.value == "high"
    assert service.active_engine is engine


# ======================================================================
# 13. EngineRegistry tracks engines correctly
# ======================================================================

def test_registry_register_and_list():
    """Registry can register engines and list them."""
    registry = EngineRegistry()
    engine = DeterministicBaselineEngine()
    registry.register(engine, set_active=True)

    engines = registry.list_engines()
    assert len(engines) == 1
    assert engines[0]["engine_name"] == "deterministic_baseline"
    assert engines[0]["engine_version"] == "1.0"
    assert engines[0]["is_active"] is True


def test_registry_get_active_engine():
    """Registry returns the active engine."""
    registry = EngineRegistry()
    engine = DeterministicBaselineEngine()
    registry.register(engine, set_active=True)

    active = registry.get_active_engine()
    assert active is engine
    assert registry.active_engine_id == "deterministic_baseline@1.0"


def test_registry_no_active_engine():
    """Registry raises RuntimeError when no active engine is set."""
    registry = EngineRegistry()
    with pytest.raises(RuntimeError, match="No active risk engine"):
        registry.get_active_engine()


def test_registry_duplicate_registration():
    """Registry rejects duplicate engine registration."""
    registry = EngineRegistry()
    engine = DeterministicBaselineEngine()
    registry.register(engine)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(engine)


def test_registry_get_engine_by_name():
    """Registry can retrieve engine by name."""
    registry = EngineRegistry()
    engine = DeterministicBaselineEngine()
    registry.register(engine)

    retrieved = registry.get_engine("deterministic_baseline")
    assert retrieved is engine


def test_registry_get_engine_not_found():
    """Registry raises KeyError for unknown engine name."""
    registry = EngineRegistry()
    with pytest.raises(KeyError, match="not_registered"):
        registry.get_engine("not_registered")


# ======================================================================
# 14. Explanation disclaimer present and non-clinical
# ======================================================================

def test_explanation_disclaimer():
    """Explanation contains non-clinical disclaimer."""
    engine = DeterministicBaselineEngine()
    result = engine.evaluate(_make_input(HIGH_SCORES))

    disclaimer = result.explanation.disclaimer
    assert "NOT" in disclaimer
    assert "clinical" in disclaimer.lower()
    assert "engineering baseline" in disclaimer.lower()
