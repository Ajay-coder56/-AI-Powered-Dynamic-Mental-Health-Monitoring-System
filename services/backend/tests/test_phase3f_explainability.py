"""
Phase 3F Acceptance-Hardened Test Suite.

Tests the DeterministicExplainabilityEngine in isolation, verifying:
- all risk-level explanations (stable/moderate/high/critical)
- domain contribution logic
- modality contribution logic
- missing modality handling
- modality conflict surfacing
- temporal trajectory explanations (worsening/improving/stable/insufficient)
- data-quality classification
- score passthrough (no modification of fused score)
- limitations / non-clinical disclaimer
- counsellor endpoint authentication
- unauthorized access rejection
- JSONB fusion_analysis compatibility (with and without)
"""

import pytest
from ai.explainability.schemas import ExplainabilityInput, ExplainabilityResult
from ai.explainability.engine import DeterministicExplainabilityEngine


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _baseline_only_mods(score: int):
    """Returns modality contributions list with only baseline available."""
    return [
        {"modality_name": "baseline", "is_available": True, "score_normalized": score,
         "confidence": 1.0, "effective_weight": 1.0},
        {"modality_name": "nlp", "is_available": False},
        {"modality_name": "speech", "is_available": False},
    ]


def _all_mods(baseline: int, nlp: int, speech: int):
    """Returns all three modalities available."""
    return [
        {"modality_name": "baseline", "is_available": True, "score_normalized": baseline,
         "confidence": 1.0, "effective_weight": 0.6},
        {"modality_name": "nlp", "is_available": True, "score_normalized": nlp,
         "confidence": 0.85, "effective_weight": 0.2},
        {"modality_name": "speech", "is_available": True, "score_normalized": speech,
         "confidence": 0.80, "effective_weight": 0.2},
    ]


def _make_temporal(trend: str, available: bool = True, data_quality: str = "adequate",
                   persistence: bool = False, status: str = "no_signal",
                   current_score: int = 40):
    if not available:
        return {"available": False, "trend": "insufficient_data",
                "temporal_status": "unavailable", "data_quality": "insufficient"}
    return {
        "available": True,
        "current_score": current_score,
        "trend": trend,
        "persistence": persistence,
        "slope_per_day": 2.0 if trend == "worsening" else (-2.0 if trend == "improving" else 0.1),
        "range": 10,
        "temporal_status": status,
        "data_quality": data_quality,
        "explanation": f"Trend is {trend}.",
    }


ENGINE = DeterministicExplainabilityEngine()


# ===========================================================================
# 1-4. Risk level explanation coverage
# ===========================================================================

def test_explain_stable_risk():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=10, risk_level="stable", wellbeing_score=90,
        domain_scores={"mood": 1, "sleep": 2},
        modality_contributions=_baseline_only_mods(10),
        conflict_detected=False,
    ))
    assert result.risk_score == 10
    assert result.risk_level == "stable"
    assert "stable" in result.summary.lower()


def test_explain_moderate_risk():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=35, risk_level="moderate", wellbeing_score=65,
        domain_scores={"mood": 5, "sleep": 6, "safety": 3},
        modality_contributions=_baseline_only_mods(35),
        conflict_detected=False,
    ))
    assert result.risk_score == 35
    assert result.risk_level == "moderate"
    assert "moderate" in result.summary.lower()


def test_explain_high_risk():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=60, risk_level="high", wellbeing_score=40,
        domain_scores={"mood": 8, "sleep": 7, "legal_anxiety": 9},
        modality_contributions=_baseline_only_mods(60),
        conflict_detected=False,
    ))
    assert result.risk_score == 60
    assert result.risk_level == "high"
    assert "high" in result.summary.lower()
    # High domains should appear in summary
    assert "legal anxiety" in result.summary.lower() or "mood" in result.summary.lower()


def test_explain_critical_risk():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=90, risk_level="critical", wellbeing_score=10,
        domain_scores={"mood": 10, "sleep": 9, "safety": 10, "social_support": 8, "legal_anxiety": 10},
        modality_contributions=_baseline_only_mods(90),
        conflict_detected=False,
    ))
    assert result.risk_score == 90
    assert result.risk_level == "critical"
    assert "critical" in result.summary.lower()


# ===========================================================================
# 5. Domain contribution explanation
# ===========================================================================

def test_domain_contributions_sorted_desc():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=55, risk_level="high", wellbeing_score=45,
        domain_scores={"mood": 3, "sleep": 8, "safety": 5, "legal_anxiety": 9},
        modality_contributions=_baseline_only_mods(55),
        conflict_detected=False,
    ))
    factors = result.top_contributing_factors
    assert len(factors) == 4
    # Sorted descending by score
    assert factors[0].score >= factors[1].score >= factors[2].score >= factors[3].score
    # Top factor
    assert factors[0].domain == "legal_anxiety"
    assert factors[0].contribution_level == "High"
    assert factors[0].score == 9
    # Low factor
    low = [f for f in factors if f.domain == "mood"][0]
    assert low.contribution_level == "Low"


def test_domain_moderate_contribution():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=30, risk_level="moderate", wellbeing_score=70,
        domain_scores={"mood": 5},
        modality_contributions=_baseline_only_mods(30),
        conflict_detected=False,
    ))
    f = result.top_contributing_factors[0]
    assert f.contribution_level == "Moderate"
    assert f.score == 5


# ===========================================================================
# 6. Modality contribution explanation
# ===========================================================================

def test_modality_all_available():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=50, risk_level="high", wellbeing_score=50,
        domain_scores={"mood": 6},
        modality_contributions=_all_mods(50, 60, 55),
        conflict_detected=False,
        temporal_result=_make_temporal("stable", data_quality="adequate"),
    ))
    mods = result.modality_contributions
    assert len(mods) == 3
    assert all(m.availability == "Available" for m in mods)
    assert len(result.missing_modalities) == 0
    # Baseline has weight 0.6 -> Dominant
    baseline_mod = [m for m in mods if m.modality == "baseline"][0]
    assert baseline_mod.contribution == "Dominant"
    # NLP has weight 0.2 -> Moderate
    nlp_mod = [m for m in mods if m.modality == "nlp"][0]
    assert nlp_mod.contribution == "Moderate"


# ===========================================================================
# 7. Missing NLP
# ===========================================================================

def test_missing_nlp():
    mods = [
        {"modality_name": "baseline", "is_available": True, "score_normalized": 40,
         "confidence": 1.0, "effective_weight": 0.75},
        {"modality_name": "nlp", "is_available": False},
        {"modality_name": "speech", "is_available": True, "score_normalized": 50,
         "confidence": 0.8, "effective_weight": 0.25},
    ]
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=42, risk_level="moderate", wellbeing_score=58,
        domain_scores={"mood": 4},
        modality_contributions=mods,
        conflict_detected=False,
    ))
    assert "nlp" in result.missing_modalities
    assert "speech" not in result.missing_modalities
    nlp_m = [m for m in result.modality_contributions if m.modality == "nlp"][0]
    assert nlp_m.availability == "Unavailable"
    assert "unavailable" in nlp_m.reason.lower()


# ===========================================================================
# 8. Missing speech
# ===========================================================================

def test_missing_speech():
    mods = [
        {"modality_name": "baseline", "is_available": True, "score_normalized": 40,
         "confidence": 1.0, "effective_weight": 0.75},
        {"modality_name": "nlp", "is_available": True, "score_normalized": 30,
         "confidence": 0.9, "effective_weight": 0.25},
        {"modality_name": "speech", "is_available": False},
    ]
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=38, risk_level="moderate", wellbeing_score=62,
        domain_scores={"mood": 4},
        modality_contributions=mods,
        conflict_detected=False,
    ))
    assert "speech" in result.missing_modalities
    assert "nlp" not in result.missing_modalities


# ===========================================================================
# 9. Multiple missing modalities
# ===========================================================================

def test_multiple_missing_modalities():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=40, risk_level="moderate", wellbeing_score=60,
        domain_scores={"mood": 5},
        modality_contributions=_baseline_only_mods(40),
        conflict_detected=False,
    ))
    assert "nlp" in result.missing_modalities
    assert "speech" in result.missing_modalities
    assert len(result.missing_modalities) == 2
    assert result.reliability.startswith("Limited")


# ===========================================================================
# 10. Modality conflict
# ===========================================================================

def test_modality_conflict_surfaced():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=55, risk_level="high", wellbeing_score=45,
        domain_scores={"mood": 7},
        modality_contributions=_all_mods(80, 20, 15),
        conflict_detected=True,
        temporal_result=_make_temporal("worsening", persistence=True, status="strong"),
    ))
    assert result.conflicting_modalities is True
    assert "disagreement across modalities" in result.summary
    assert "conflicting" in result.human_review_note.lower()


# ===========================================================================
# 11. Worsening temporal trajectory
# ===========================================================================

def test_temporal_worsening():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=65, risk_level="high", wellbeing_score=35,
        domain_scores={"mood": 7},
        modality_contributions=_baseline_only_mods(65),
        conflict_detected=False,
        temporal_result=_make_temporal("worsening", persistence=True,
                                       status="elevated", current_score=65),
    ))
    assert result.temporal_summary is not None
    assert result.temporal_summary.trend == "worsening"
    assert result.temporal_summary.persistence is True
    assert "worsening" in result.summary.lower()
    assert "persistently worsening" in result.human_review_note.lower()


# ===========================================================================
# 12. Improving temporal trajectory
# ===========================================================================

def test_temporal_improving():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=30, risk_level="moderate", wellbeing_score=70,
        domain_scores={"mood": 4},
        modality_contributions=_baseline_only_mods(30),
        conflict_detected=False,
        temporal_result=_make_temporal("improving", current_score=30),
    ))
    assert result.temporal_summary is not None
    assert result.temporal_summary.trend == "improving"
    assert "improving" in result.summary.lower()


# ===========================================================================
# 13. Insufficient temporal data
# ===========================================================================

def test_temporal_insufficient():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=20, risk_level="stable", wellbeing_score=80,
        domain_scores={"mood": 2},
        modality_contributions=_baseline_only_mods(20),
        conflict_detected=False,
        temporal_result=_make_temporal("insufficient_data", available=False),
    ))
    assert result.temporal_summary is None
    # No trend text in summary since temporal unavailable
    assert "worsening" not in result.summary.lower()
    assert "improving" not in result.summary.lower()


def test_temporal_none():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=20, risk_level="stable", wellbeing_score=80,
        domain_scores={"mood": 2},
        modality_contributions=_baseline_only_mods(20),
        conflict_detected=False,
        temporal_result=None,
    ))
    assert result.temporal_summary is None


# ===========================================================================
# 14. Data quality explanation
# ===========================================================================

def test_data_quality_strong():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=40, risk_level="moderate", wellbeing_score=60,
        domain_scores={"mood": 5},
        modality_contributions=_all_mods(40, 45, 42),
        conflict_detected=False,
        temporal_result=_make_temporal("stable", data_quality="strong"),
    ))
    assert result.reliability.startswith("Strong")


def test_data_quality_adequate():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=40, risk_level="moderate", wellbeing_score=60,
        domain_scores={"mood": 5},
        modality_contributions=[
            {"modality_name": "baseline", "is_available": True, "score_normalized": 40,
             "confidence": 1.0, "effective_weight": 0.75},
            {"modality_name": "nlp", "is_available": True, "score_normalized": 45,
             "confidence": 0.9, "effective_weight": 0.25},
        ],
        conflict_detected=False,
        temporal_result=_make_temporal("stable", data_quality="limited"),
    ))
    assert result.reliability.startswith("Adequate")


def test_data_quality_limited():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=40, risk_level="moderate", wellbeing_score=60,
        domain_scores={"mood": 5},
        modality_contributions=_baseline_only_mods(40),
        conflict_detected=False,
        temporal_result=None,
    ))
    assert result.reliability.startswith("Limited")


# ===========================================================================
# 15. Explanation does NOT modify the fused risk score
# ===========================================================================

def test_score_passthrough_not_modified():
    """The engine must pass the score through unchanged — it is read-only."""
    for score in [0, 24, 25, 48, 49, 74, 75, 100]:
        result = ENGINE.generate_explanation(ExplainabilityInput(
            risk_score=score, risk_level="stable", wellbeing_score=100 - score,
            domain_scores={"mood": 3},
            modality_contributions=_baseline_only_mods(score),
            conflict_detected=False,
        ))
        assert result.risk_score == score, f"Score {score} was modified to {result.risk_score}"


# ===========================================================================
# 16. Limitations always present
# ===========================================================================

def test_limitations_always_present():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=50, risk_level="high", wellbeing_score=50,
        domain_scores={"mood": 6},
        modality_contributions=_baseline_only_mods(50),
        conflict_detected=False,
    ))
    assert "not a clinically validated predictive model" in result.limitations
    assert "diagnose mental illness" in result.limitations
    assert "Counsellor/human review remains necessary" in result.limitations


# ===========================================================================
# 17. Human review guidance
# ===========================================================================

def test_human_review_default():
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=20, risk_level="stable", wellbeing_score=80,
        domain_scores={"mood": 2},
        modality_contributions=_baseline_only_mods(20),
        conflict_detected=False,
    ))
    assert "counselling protocol" in result.human_review_note.lower()


# ===========================================================================
# 18-19. Counsellor endpoint authentication (API-level tests)
# ===========================================================================

@pytest.mark.asyncio
async def test_cases_endpoint_rejects_unauthenticated(client):
    """GET /api/v1/cases/ without token must return 401."""
    response = await client.get("/api/v1/cases/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_explanation_endpoint_rejects_unauthenticated(client):
    """GET /api/v1/cases/FAKE-001/explanation without token must return 401."""
    response = await client.get("/api/v1/cases/FAKE-001/explanation")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_explanation_endpoint_rejects_bad_token(client):
    """GET /api/v1/cases/FAKE-001/explanation with invalid token must return 401."""
    response = await client.get(
        "/api/v1/cases/FAKE-001/explanation",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    assert response.status_code == 401


# ===========================================================================
# 20. JSONB compatibility — engine handles missing fusion_analysis gracefully
# ===========================================================================

def test_jsonb_no_fusion_analysis():
    """
    Simulate an old check-in that has no fusion_analysis in its JSONB answers.
    The cases router falls back to baseline-only modality contributions.
    Test that the engine handles that fallback shape correctly.
    """
    fallback_mods = [
        {"modality_name": "baseline", "is_available": True,
         "score_normalized": 50, "confidence": 1.0, "effective_weight": 1.0},
        {"modality_name": "nlp", "is_available": False},
        {"modality_name": "speech", "is_available": False},
    ]
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=50, risk_level="high", wellbeing_score=50,
        domain_scores={"mood": 6, "sleep": 5},
        modality_contributions=fallback_mods,
        conflict_detected=False,
    ))
    assert "nlp" in result.missing_modalities
    assert "speech" in result.missing_modalities
    assert result.risk_score == 50  # not altered


def test_jsonb_with_fusion_analysis():
    """
    Simulate a new check-in that HAS fusion_analysis in its JSONB answers.
    The engine should correctly interpret the full modality set.
    """
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=55, risk_level="high", wellbeing_score=45,
        domain_scores={"mood": 7, "sleep": 6},
        modality_contributions=_all_mods(55, 60, 50),
        conflict_detected=False,
    ))
    assert len(result.missing_modalities) == 0
    assert result.risk_score == 55


def test_answers_preserved_with_fusion():
    """
    Verify the answers dict merging logic preserves original answers.
    This is a unit-level simulation of what users.py does.
    """
    original_answers = {"q1": "yes", "q2": "no"}
    fusion_analysis = {"modality_contributions": [], "conflict_detected": False}

    # Simulate the merge logic from users.py
    answers = dict(original_answers)  # copy
    answers["fusion_analysis"] = fusion_analysis

    # Original keys preserved
    assert answers["q1"] == "yes"
    assert answers["q2"] == "no"
    # Fusion added
    assert "fusion_analysis" in answers
    assert answers["fusion_analysis"]["conflict_detected"] is False


def test_answers_none_with_fusion():
    """If original answers were None, fusion_analysis still works."""
    answers = {} or {}
    fusion_analysis = {"modality_contributions": [], "conflict_detected": False}
    answers["fusion_analysis"] = fusion_analysis
    assert "fusion_analysis" in answers


# ===========================================================================
# 21. No raw audio or sensitive transcript stored
# ===========================================================================

def test_no_raw_audio_in_schema():
    """ExplainabilityInput and ExplainabilityResult must not have audio fields."""
    from ai.explainability.schemas import ExplainabilityInput, ExplainabilityResult
    input_fields = set(ExplainabilityInput.model_fields.keys())
    result_fields = set(ExplainabilityResult.model_fields.keys())
    for forbidden in ["audio", "audio_bytes", "raw_audio", "transcript", "raw_text"]:
        assert forbidden not in input_fields, f"ExplainabilityInput should not have '{forbidden}'"
        assert forbidden not in result_fields, f"ExplainabilityResult should not have '{forbidden}'"


# ===========================================================================
# 22. Phase 3E consistency — temporal summary passes through unchanged
# ===========================================================================

def test_temporal_consistency_with_phase3e():
    """The explainability temporal summary must mirror the Phase 3E output."""
    temporal_in = {
        "available": True,
        "current_score": 72,
        "trend": "worsening",
        "slope_per_day": 3.5,
        "persistence": True,
        "range": 25,
        "temporal_status": "elevated",
        "data_quality": "strong",
        "explanation": "Recent observations show elevated risk.",
    }
    result = ENGINE.generate_explanation(ExplainabilityInput(
        risk_score=72, risk_level="high", wellbeing_score=28,
        domain_scores={"mood": 8},
        modality_contributions=_baseline_only_mods(72),
        conflict_detected=False,
        temporal_result=temporal_in,
    ))
    ts = result.temporal_summary
    assert ts is not None
    assert ts.current_risk == 72
    assert ts.trend == "worsening"
    assert ts.slope_per_day == 3.5
    assert ts.persistence is True
    assert ts.early_warning_status == "elevated"
    assert ts.data_quality == "strong"
    assert ts.explanation == "Recent observations show elevated risk."
