import pytest
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
from datetime import datetime

from ai.alerts.engine import DeterministicAlertEngine
from ai.alerts.schemas import AlertPriority, AlertType, AlertEngineResult
from ai.explainability.schemas import ExplainabilityResult, TemporalSummary
from app.models.alert import Alert

# ---------------------------------------------------------------------------
# 1. Alert Engine Unit Tests
# ---------------------------------------------------------------------------

def _make_explain(risk_score: int, conflict: bool = False, temporal: Optional[TemporalSummary] = None, reliability="Strong") -> ExplainabilityResult:
    return ExplainabilityResult(
        summary="Test explanation",
        risk_score=risk_score,
        risk_level="high" if risk_score >= 60 else "stable",
        top_contributing_factors=[],
        modality_contributions=[],
        missing_modalities=[],
        conflicting_modalities=conflict,
        temporal_summary=temporal,
        reliability=reliability,
        human_review_note="Note",
        limitations="Limitations"
    )

def test_rule_a_critical():
    engine = DeterministicAlertEngine()
    res = engine.evaluate(_make_explain(80))
    assert res.should_alert is True
    assert res.priority == AlertPriority.CRITICAL
    assert res.alert_type == AlertType.RISK_THRESHOLD

def test_rule_b_high():
    engine = DeterministicAlertEngine()
    res = engine.evaluate(_make_explain(60))
    assert res.should_alert is True
    assert res.priority == AlertPriority.HIGH
    assert res.alert_type == AlertType.RISK_THRESHOLD

def test_rule_e_persistent_worsening():
    engine = DeterministicAlertEngine()
    ts = TemporalSummary(current_risk=40, trend="worsening", persistence=True, early_warning_status="elevated", data_quality="adequate", explanation="")
    res = engine.evaluate(_make_explain(40, temporal=ts))
    assert res.should_alert is True
    assert res.priority == AlertPriority.HIGH
    assert res.alert_type == AlertType.PERSISTENT_WORSENING

def test_rule_c_worsening():
    engine = DeterministicAlertEngine()
    ts = TemporalSummary(current_risk=40, trend="worsening", persistence=False, early_warning_status="elevated", data_quality="adequate", explanation="")
    res = engine.evaluate(_make_explain(40, temporal=ts))
    assert res.should_alert is True
    assert res.priority == AlertPriority.MEDIUM
    assert res.alert_type == AlertType.WORSENING_TRAJECTORY

def test_rule_f_conflict():
    engine = DeterministicAlertEngine()
    res = engine.evaluate(_make_explain(30, conflict=True))
    assert res.should_alert is True
    assert res.priority == AlertPriority.MEDIUM
    assert res.alert_type == AlertType.SIGNAL_CONFLICT

def test_rule_g_insufficient():
    engine = DeterministicAlertEngine()
    res = engine.evaluate(_make_explain(30, reliability="Insufficient data."))
    assert res.should_alert is True
    assert res.priority == AlertPriority.LOW
    assert res.alert_type == AlertType.INSUFFICIENT_DATA

def test_no_alert_condition():
    engine = DeterministicAlertEngine()
    ts = TemporalSummary(current_risk=30, trend="improving", persistence=False, early_warning_status="none", data_quality="adequate", explanation="")
    res = engine.evaluate(_make_explain(30, temporal=ts))
    assert res.should_alert is False


# ---------------------------------------------------------------------------
# 2. Alert API / Service Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_api_rejects_unauthenticated(client):
    res = await client.get("/api/v1/alerts/")
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_api_rejects_invalid_token(client):
    res = await client.get("/api/v1/alerts/", headers={"Authorization": "Bearer fake"})
    assert res.status_code == 401
