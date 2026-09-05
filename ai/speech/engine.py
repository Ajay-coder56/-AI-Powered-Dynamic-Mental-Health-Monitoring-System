import io
import logging
import time
import numpy as np
from typing import Optional, Tuple

from app.risk_engine.interface import SpeechAnalysisEngine
from ai.speech.schemas import SpeechAnalysisInput, SpeechAnalysisResult

logger = logging.getLogger(__name__)

class AcousticFeatureEngine(SpeechAnalysisEngine):
    """
    Speech engine that extracts pure acoustic features using librosa and PyAV.
    Derives an engineering 'voice_signal' from pitch variability and RMS energy.
    """
    
    @property
    def engine_name(self) -> str:
        return "acoustic_features"
        
    @property
    def engine_version(self) -> str:
        return "1.0"
        
    def engine_id(self) -> str:
        return f"{self.engine_name}@{self.engine_version}"

    def _decode_audio(self, audio_bytes: bytes) -> Tuple[Optional[np.ndarray], Optional[int]]:
        """Decode raw audio bytes (e.g. webm) into a numpy array (mono) using PyAV."""
        try:
            import av
        except ImportError:
            logger.error("PyAV not installed")
            return None, None

        try:
            container = av.open(io.BytesIO(audio_bytes))
            stream = container.streams.audio[0]
            
            samples = []
            sample_rate = stream.rate
            
            for frame in container.decode(stream):
                # convert to numpy array (channels, samples)
                arr = frame.to_ndarray()
                if arr.ndim > 1:
                    # convert to mono by averaging channels
                    arr = np.mean(arr, axis=0)
                samples.append(arr)
                
            if not samples:
                return None, None
                
            waveform = np.concatenate(samples)
            
            # Simple normalization (-1 to 1)
            max_val = np.max(np.abs(waveform))
            if max_val > 0:
                waveform = waveform / max_val
                
            return waveform, sample_rate
            
        except Exception as e:
            logger.error(f"Audio decoding failed: {e}")
            return None, None

    def analyze_voice(self, voice_features: dict) -> dict:
        """Internal interface matching the Phase 3A ABC."""
        # We expect voice_features to contain the raw bytes for Phase 3C
        audio_bytes = voice_features.get("audio_bytes")
        if not audio_bytes:
            return self._build_unavailable("No audio bytes provided").model_dump()
            
        input_data = SpeechAnalysisInput(audio_bytes=audio_bytes)
        result = self.analyze(input_data)
        return result.model_dump()

    def analyze(self, input_data: SpeechAnalysisInput) -> SpeechAnalysisResult:
        """Extract acoustic features and construct voice signal."""
        start_time = time.time()
        
        try:
            import librosa
        except ImportError:
            return self._build_unavailable("librosa not installed")

        if len(input_data.audio_bytes) > 10 * 1024 * 1024:
            return self._build_unavailable("Audio size exceeds 10MB limit")

        waveform, sr = self._decode_audio(input_data.audio_bytes)
        if waveform is None or sr is None:
            return self._build_unavailable("Failed to decode audio or unsupported format")
            
        duration = len(waveform) / sr
        if duration == 0:
            return self._build_unavailable("Audio duration is 0 seconds")
        
        if duration > 180:
             return self._build_unavailable("Audio duration exceeds 180 seconds")

        try:
            # 1. Pitch / Fundamental frequency (F0)
            f0, voiced_flag, voiced_probs = librosa.pyin(
                waveform, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr
            )
            f0_valid = f0[voiced_flag]
            mean_pitch = float(np.mean(f0_valid)) if len(f0_valid) > 0 else 0.0
            pitch_std = float(np.std(f0_valid)) if len(f0_valid) > 0 else 0.0
            
            # 2. RMS Energy
            rms = librosa.feature.rms(y=waveform)
            mean_energy = float(np.mean(rms))
            
            # 3. Construct "voice_signal" (Engineering prototype)
            # High pitch variability and very low mean energy can loosely correlate with certain distress types.
            # This is NOT clinical. It's a deterministic normalized proxy.
            
            # Normalize pitch variability (assume 50Hz is high variance)
            norm_pitch_var = min(pitch_std / 50.0, 1.0)
            
            # Normalize energy (assume 0.1 is normal, lower is more "distressed" / flat affect)
            norm_energy_inv = max(0.0, 1.0 - (mean_energy / 0.1))
            
            voice_signal = (norm_pitch_var * 0.4) + (norm_energy_inv * 0.6)
            voice_signal = float(np.clip(voice_signal, 0.0, 1.0))

            feature_summary = {
                "mean_pitch_hz": mean_pitch,
                "pitch_std_hz": pitch_std,
                "mean_rms_energy": mean_energy
            }

            return SpeechAnalysisResult(
                available=True,
                duration_seconds=float(duration),
                voice_signal=voice_signal,
                confidence=float(np.mean(voiced_probs)) if len(voiced_probs) > 0 else 0.0,
                feature_summary=feature_summary,
                extractor_name=self.engine_name,
                extractor_version=self.engine_version,
                explanation=(
                    f"Extracted features from {duration:.1f}s audio. "
                    f"Mean pitch: {mean_pitch:.1f} Hz, Energy: {mean_energy:.3f}. "
                    f"Derived voice distress signal: {voice_signal:.2f}."
                ),
                limitations="Signal is based on basic acoustic heuristics (energy and pitch variability)."
            )

        except Exception as e:
            logger.error(f"Speech analysis failed: {e}")
            return self._build_unavailable(f"Feature extraction failed: {str(e)}")

    def _build_unavailable(self, reason: str) -> SpeechAnalysisResult:
        return SpeechAnalysisResult(
            available=False,
            extractor_name=self.engine_name,
            extractor_version=self.engine_version,
            explanation=f"Voice analysis unavailable: {reason}",
            limitations="Analysis skipped."
        )
