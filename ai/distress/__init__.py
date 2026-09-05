"""
AI / Distress Module — Multimodal distress scoring and fusion.

Phase: 3D (NOT YET IMPLEMENTED)

This module will provide multimodal risk fusion, combining outputs from
the text analysis engine (NLP), speech analysis engine, temporal engine,
and baseline deterministic engine into a unified distress score.

Planned capabilities (Phase 3D):
- Multimodal feature fusion
- Weighted ensemble risk scoring
- Cross-modal consistency checks
- Dynamic risk score aggregation

IMPORTANT: This module is a boundary placeholder only.
No AI models, no fake outputs, no production wiring.
"""

NOT_IMPLEMENTED = False
PHASE = "3D"
ENGINE_INTERFACE = "RiskEngine (multimodal variant)"

from ai.distress.schemas import FusionInput, FusionResult, ModalityContribution
from ai.distress.config import FusionConfig, config
from ai.distress.fusion import MultimodalFusionEngine

from ai.distress.temporal_schemas import TemporalInput, TemporalRiskResult, TemporalObservation
from ai.distress.temporal_config import TemporalConfig, config as temporal_config
from ai.distress.temporal import TemporalRiskEngine

__all__ = [
    "FusionInput",
    "FusionResult",
    "ModalityContribution",
    "FusionConfig",
    "config",
    "MultimodalFusionEngine",
    "TemporalInput",
    "TemporalRiskResult",
    "TemporalObservation",
    "TemporalConfig",
    "temporal_config",
    "TemporalRiskEngine",
]
