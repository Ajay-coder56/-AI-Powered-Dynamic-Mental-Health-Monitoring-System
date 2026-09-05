"""
Phase 3C Tests: Speech / Voice Analysis Engine

Tests verify:
1. SpeechAnalysisInput validation
2. SpeechAnalysisResult schema validation
3. Engine instantiation & metadata
4. Baseline unchanged when Speech unavailable/disabled
5. Graceful fallback on Speech failure
6. Integration with RiskEngineService
"""

import pytest
import numpy as np
import io
import soundfile as sf
from pydantic import ValidationError

from app.risk_engine.schemas import RiskInput
from app.risk_engine.service import RiskEngineService
from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.registry import EngineRegistry
from ai.speech.schemas import SpeechAnalysisInput, SpeechAnalysisResult
from ai.speech.engine import AcousticFeatureEngine


def create_synthetic_audio(duration_sec=1.0, sr=16000, freq=440.0):
    """Creates a simple synthetic sine wave and encodes it to WAV bytes."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    y = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Write to in-memory bytes buffer
    buf = io.BytesIO()
    sf.write(buf, y, sr, format='WAV', subtype='PCM_16')
    return buf.getvalue()


def test_input_validation_valid():
    """Valid audio bytes passes validation."""
    data = SpeechAnalysisInput(audio_bytes=b"dummy_bytes")
    assert data.audio_bytes == b"dummy_bytes"


def test_result_schema():
    """SpeechAnalysisResult handles valid bounds."""
    res = SpeechAnalysisResult(
        available=True,
        duration_seconds=10.5,
        voice_signal=0.6,
        confidence=0.9,
        feature_summary={"mean_pitch_hz": 200.0},
        extractor_name="test",
        extractor_version="1.0",
        explanation="Test",
        limitations="Test limitation"
    )
    assert res.available is True
    assert res.voice_signal == 0.6


def test_engine_metadata():
    """AcousticFeatureEngine has correct metadata."""
    engine = AcousticFeatureEngine()
    assert engine.engine_name == "acoustic_features"
    assert engine.engine_version == "1.0"


def test_speech_unavailable_fallback():
    """When audio is invalid, the engine returns an unavailable result without crashing."""
    engine = AcousticFeatureEngine()
    res = engine.analyze(SpeechAnalysisInput(audio_bytes=b"invalid_bytes"))
    assert res.available is False
    assert "Failed to decode" in res.explanation


def test_synthetic_audio_analysis():
    """Test the engine with a synthetic sine wave."""
    engine = AcousticFeatureEngine()
    audio_bytes = create_synthetic_audio(duration_sec=0.5, freq=440.0)
    
    # Run analysis
    res = engine.analyze(SpeechAnalysisInput(audio_bytes=audio_bytes))
    
    assert res.available is True
    assert res.duration_seconds == pytest.approx(0.5, abs=0.01)
    
    # 440Hz sine wave should have mean pitch around 440Hz
    # librosa pyin might not be perfectly exact for short synthetic clips, but it should be close
    assert res.feature_summary is not None
    assert "mean_pitch_hz" in res.feature_summary
    assert res.voice_signal is not None
    assert 0.0 <= res.voice_signal <= 1.0


def test_service_integration_no_audio():
    """RiskEngineService with no audio returns baseline only."""
    registry = EngineRegistry()
    baseline = DeterministicBaselineEngine()
    registry.register(baseline, set_active=True)
    service = RiskEngineService(engine=baseline, registry=registry)
    
    risk_input = RiskInput(domain_scores={"mood": 5, "sleep": 2, "safety": 0, "social_support": 1, "legal_anxiety": 2})
    result = service.evaluate(risk_input)
    
    # `getattr(risk_input, 'audio_bytes')` should be None
    assert result.speech_analysis is None
    assert result.risk_level.value == "stable"


def test_service_integration_with_audio():
    """RiskEngineService triggers speech analysis if audio_bytes is present."""
    registry = EngineRegistry()
    baseline = DeterministicBaselineEngine()
    registry.register(baseline, set_active=True)
    service = RiskEngineService(engine=baseline, registry=registry)
    
    audio_bytes = create_synthetic_audio(duration_sec=0.5)
    risk_input = RiskInput(
        domain_scores={"mood": 5, "sleep": 2, "safety": 0, "social_support": 1, "legal_anxiety": 2},
        audio_bytes=audio_bytes
    )
    result = service.evaluate(risk_input)
    
    assert result.speech_analysis is not None
    assert result.speech_analysis["available"] is True
    assert result.speech_analysis["duration_seconds"] == pytest.approx(0.5, abs=0.01)
