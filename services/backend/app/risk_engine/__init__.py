"""
Risk Engine Package — AI / Risk Engine Foundation (Phase 3A).

This package provides a clean, production-oriented Risk Engine architecture
that supports the current deterministic baseline risk calculation and allows
future integration of NLP, speech, temporal, and multimodal AI engines
without requiring major rewrites of the existing API, database, or frontend.

Architecture:
    API Route
        ↓
    RiskEngineService (service.py)
        ↓
    RiskEngine Interface (interface.py)
        ↓
    DeterministicBaselineEngine (baseline.py)
        ↓
    Standardized RiskResult (schemas.py)

DISCLAIMER:
This system provides engineering baseline risk calculations.
It is NOT a clinically validated assessment, diagnosis, or prediction tool.
No clinical validation has been performed. Risk scores do not constitute
psychiatric diagnoses. AI outputs must not be treated as autonomous clinical
decisions. Counsellor/human review remains necessary. Emergency situations
must not depend exclusively on the model.
"""

from app.risk_engine.baseline import DeterministicBaselineEngine
from app.risk_engine.interface import RiskEngine
from app.risk_engine.registry import EngineRegistry
from app.risk_engine.schemas import RiskInput, RiskResult, RiskExplanation
from app.risk_engine.service import RiskEngineService, get_risk_engine_service

__all__ = [
    "DeterministicBaselineEngine",
    "EngineRegistry",
    "RiskEngine",
    "RiskEngineService",
    "RiskExplanation",
    "RiskInput",
    "RiskResult",
    "get_risk_engine_service",
]
