import pytest
from datetime import datetime, timezone, timedelta
from ai.distress import TemporalObservation, TemporalInput, TemporalRiskEngine

def build_obs(days_ago: int, score: int) -> TemporalObservation:
    t = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return TemporalObservation(timestamp=t, risk_score=score, risk_level="test")

def test_zero_observations():
    engine = TemporalRiskEngine()
    result = engine.analyze(TemporalInput(user_id="test", observations=[]))
    assert not result.available
    assert result.observation_count == 0
    assert result.data_quality == "insufficient"
    assert result.temporal_status == "unavailable"

def test_one_observation():
    engine = TemporalRiskEngine()
    obs = build_obs(0, 50)
    result = engine.analyze(TemporalInput(user_id="test", observations=[obs]))
    assert not result.available
    assert result.observation_count == 1
    assert result.current_score == 50
    assert result.trend == "insufficient_data"

def test_stable_trajectory():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 40)
    obs2 = build_obs(2, 41)
    obs3 = build_obs(1, 40)
    obs4 = build_obs(0, 42)
    
    result = engine.analyze(TemporalInput(user_id="test", observations=[obs1, obs2, obs3, obs4]))
    assert result.available
    assert result.observation_count == 4
    assert result.trend == "stable"
    assert not result.persistence
    assert result.temporal_status in ["no_signal", "watch"]
    assert "stable" in result.explanation

def test_worsening_trajectory():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 30)
    obs2 = build_obs(2, 38)
    obs3 = build_obs(1, 47)
    obs4 = build_obs(0, 58)
    
    result = engine.analyze(TemporalInput(user_id="test", observations=[obs1, obs2, obs3, obs4]))
    assert result.available
    assert result.trend == "worsening"
    assert result.persistence is True
    assert result.temporal_status in ["elevated", "strong"]
    assert "persistent worsening" in result.explanation

def test_improving_trajectory():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 70)
    obs2 = build_obs(2, 60)
    obs3 = build_obs(1, 48)
    obs4 = build_obs(0, 35)
    
    result = engine.analyze(TemporalInput(user_id="test", observations=[obs1, obs2, obs3, obs4]))
    assert result.available
    assert result.trend == "improving"
    assert not result.persistence
    assert result.temporal_status in ["no_signal", "watch"]
    assert "improving" in result.explanation

def test_single_spike():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 35)
    obs2 = build_obs(2, 38)
    obs3 = build_obs(1, 75)
    obs4 = build_obs(0, 39)
    
    result = engine.analyze(TemporalInput(user_id='test', observations=[obs1, obs2, obs3, obs4]))
    assert not result.persistence
    assert 'persistent worsening' not in result.explanation

def test_single_spike_end():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 35)
    obs2 = build_obs(2, 36)
    obs3 = build_obs(1, 37)
    obs4 = build_obs(0, 75)
    
    result = engine.analyze(TemporalInput(user_id='test', observations=[obs1, obs2, obs3, obs4]))
    assert result.trend == 'worsening'
    assert result.persistence

def test_irregular_time():
    engine = TemporalRiskEngine()
    obs1 = build_obs(5, 40)
    obs2 = build_obs(3, 50)
    obs3 = build_obs(0, 65)
    
    result = engine.analyze(TemporalInput(user_id='test', observations=[obs1, obs2, obs3]))
    assert result.available
    assert result.observation_count == 3
    assert result.analysis_window_days == 5.0
    assert result.slope_per_day == pytest.approx(5.0)

def test_duplicate_timestamps():
    engine = TemporalRiskEngine()
    obs1 = build_obs(3, 30)
    obs2 = build_obs(3, 40)
    
    result = engine.analyze(TemporalInput(user_id='test', observations=[obs1, obs2]))
    assert result.observation_count == 1

@pytest.mark.asyncio
async def test_api_trajectory(client):
    from httpx import AsyncClient
    from tests.test_phase2b import PRIYA_ID
    
    response = await client.get(f'/api/v1/users/{PRIYA_ID}/risk/trajectory')
    assert response.status_code == 200
    data = response.json()
    assert 'available' in data
    assert 'trend' in data
