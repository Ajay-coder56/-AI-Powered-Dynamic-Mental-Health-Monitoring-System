"""
AI / NLP Module — Natural Language Processing for distress analysis.

Phase: 3B

This module provides text analysis capabilities for identifying distress
signals in free-text responses and voice transcripts. It implements the
TextAnalysisEngine interface defined in app.risk_engine.interface.

Capabilities (Phase 3B):
- Multilingual sentiment analysis (XLM-RoBERTa)
- Derivation of an NLP distress signal from negative sentiment
- Safe fallback when NLP fails or text is missing
- No clinical diagnoses; engineering prototypes only.
"""

from ai.nlp.schemas import TextAnalysisInput, TextAnalysisResult
from ai.nlp.engine import MultilingualSentimentEngine
from ai.nlp.config import config, NLPConfig

NOT_IMPLEMENTED = False
PHASE = "3B"
ENGINE_INTERFACE = "TextAnalysisEngine"

__all__ = [
    "TextAnalysisInput",
    "TextAnalysisResult",
    "MultilingualSentimentEngine",
    "config",
    "NLPConfig"
]
