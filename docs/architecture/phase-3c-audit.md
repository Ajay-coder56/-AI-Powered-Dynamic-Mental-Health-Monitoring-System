# Phase 3C Audit — Speech Engine

**Date**: 2026-09-05
**Phase**: 3C — Speech / Voice Analysis

## Audit Findings

1. **Frontend**: `VoiceCheckIn.tsx` previously simulated a timer but did not record actual audio. It submitted a dummy JSON payload to the standard check-in endpoint.
2. **Backend**: No multipart upload endpoint existed for check-ins.
3. **Environment**: Did not have audio processing tools installed. `ffmpeg` binary was missing from the OS, so using `av` (PyAV) for decoding was necessary.
4. **Integration**: `RiskEngineService` cleanly supported extensions. `SpeechAnalysisEngine` contract was defined but needed audio bytes support.

## Plan
Implement Option A: Acoustic Features using `librosa` and `av`, alongside a new `POST /api/v1/users/{id}/voice-check-ins` endpoint, fully replacing the mock frontend with `MediaRecorder`.
