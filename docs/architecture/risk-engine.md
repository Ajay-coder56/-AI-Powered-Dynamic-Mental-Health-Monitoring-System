# Risk Engine Architecture

**Version**: 1.0
**Phase**: 3A — AI / Risk Engine Foundation
**Date**: 2026-09-05

---

## Overview

The Risk Engine is a modular, implementation-independent framework for evaluating mental health risk from check-in assessments. It provides a stable internal interface that separates risk calculation logic from the API layer, enabling future AI/ML integration without modifying existing endpoints.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  POST /api/v1/users/{user_id}/check-ins                     │
│  (routers/users.py)                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   RiskEngineService                          │
│  (risk_engine/service.py)                                    │
│  - Holds reference to active RiskEngine                     │
│  - Delegates evaluate() calls                               │
│  - Manages engine lifecycle                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                RiskEngine Interface (ABC)                    │
│  (risk_engine/interface.py)                                  │
│  - evaluate(RiskInput) → RiskResult                         │
│  - engine_name, engine_version properties                   │
└────────────────────────┬────────────────────────────────────┘
                         │
           ┌─────────────┼─────────────────────────────┐
           ▼             ▼                             ▼
┌──────────────┐ ┌──────────────┐             ┌──────────────┐
│ Deterministic│ │  NLP Engine  │    ...       │  Multimodal  │
│   Baseline   │ │  (Phase 3B)  │             │  (Phase 3D)  │
│  (baseline.  │ │              │             │              │
│   py)        │ │  NOT YET     │             │  NOT YET     │
│              │ │  IMPLEMENTED │             │  IMPLEMENTED │
│  ACTIVE ✓    │ │              │             │              │
└──────────────┘ └──────────────┘             └──────────────┘
```

---

## Interfaces

### RiskEngine (Abstract Base Class)

```python
class RiskEngine(ABC):
    @property
    def engine_name(self) -> str: ...
    @property
    def engine_version(self) -> str: ...
    def evaluate(self, risk_input: RiskInput) -> RiskResult: ...
    def engine_id(self) -> str:  # Returns "name@version"
```

### Future Engine Interfaces

| Interface | Phase | Purpose |
|-----------|-------|---------|
| `TextAnalysisEngine` | 3B | NLP-based distress detection |
| `SpeechAnalysisEngine` | 3C | Voice/acoustic distress detection |
| `TemporalRiskEngine` | 3E | Historical trend analysis |
| `ExplainabilityEngine` | 3F | SHAP/LIME model explanations |

These are defined as abstract classes in `interface.py` but are **NOT wired into the production path**.

---

## Data Flow

### Input: RiskInput

```python
class RiskInput(BaseModel):
    # Required for baseline
    domain_scores: Dict[str, int]  # domain -> score (0-10)
    mode: CheckInMode

    # Context
    user_id: Optional[UUID]
    check_in_id: Optional[UUID]
    timestamp: Optional[datetime]
    mood: Optional[str]

    # Future (all Optional, ignored by baseline)
    text_content: Optional[str]       # Phase 3B
    transcript: Optional[str]         # Phase 3B
    voice_features: Optional[dict]    # Phase 3C
    historical_features: Optional[dict]  # Phase 3E
    legal_context: Optional[dict]
    metadata: Optional[dict]
```

### Output: RiskResult

```python
class RiskResult(BaseModel):
    risk_score: int          # 0-100
    wellbeing_score: int     # 0-100
    raw_score: int           # Sum of domain scores
    risk_level: RiskLevel    # stable|moderate|high|critical
    contributing_factors: List[str]
    engine_name: str
    engine_version: str
    confidence: Optional[float]  # None for deterministic
    component_scores: Dict[str, int]
    explanation: RiskExplanation
    timestamp: datetime
```

### Explanation: RiskExplanation

```python
class RiskExplanation(BaseModel):
    summary: str
    domain_contributions: List[DomainContribution]
    explanation_type: ExplanationType
    model_confidence: Optional[float]
    disclaimer: str
```

---

## Current Baseline Engine

**Engine ID**: `deterministic_baseline@1.0`

The `DeterministicBaselineEngine` implements the exact same algorithm as the Phase 2 `risk_calculator.py`:

- Sum domain scores (0-10 each) → raw_score (0-50)
- Normalize to risk_score and wellbeing_score (0-100)
- Map to risk_level via thresholds
- Identify contributing factors (domains ≥ 7)
- Generate deterministic explanations

**No changes** to the calculation semantics.

---

## Versioning Strategy

Engines are registered in the `EngineRegistry` with a `name@version` identifier:

```
deterministic_baseline@1.0   ← currently active
text_nlp@1.0                 ← future Phase 3B
speech@1.0                   ← future Phase 3C
multimodal@1.0               ← future Phase 3D
```

The registry allows:
- Registering multiple engines
- Listing all engines with metadata
- Selecting the active engine
- Querying by name and/or version

Version logic is centralized — not hardcoded throughout the application.

---

## Future AI Module Boundaries

| Module | Directory | Interface | Phase |
|--------|-----------|-----------|-------|
| NLP | `ai/nlp/` | `TextAnalysisEngine` | 3B |
| Speech | `ai/speech/` | `SpeechAnalysisEngine` | 3C |
| Distress/Multimodal | `ai/distress/` | `RiskEngine` (multimodal) | 3D |
| Explainability | `ai/explainability/` | `ExplainabilityEngine` | 3F |

Each module has a boundary `__init__.py` documenting its future purpose and the interface it will implement. **No fake AI is implemented.**

---

## Safety Boundaries

> **CRITICAL SAFETY NOTICE**

### What the system DOES:
- Provide a deterministic engineering baseline risk calculation
- Structure domain-level distress scores into a normalized risk framework
- Generate factual, rule-based explanations of risk scores
- Support future integration of validated AI models

### What the system DOES NOT do:
- **Risk score ≠ diagnosis** — Risk scores are engineering metrics, not psychiatric diagnoses
- **Risk level ≠ psychiatric diagnosis** — "high" or "critical" are engineering thresholds, not clinical determinations
- **Baseline score is an engineering prototype** — It has not been clinically validated
- **No clinical validation has been performed** — The system has not been validated against clinical outcomes
- **AI outputs must not be treated as autonomous clinical decisions** — All outputs require human review
- **Counsellor/human review remains necessary** — The system supports, not replaces, human judgment
- **Emergency situations must not depend exclusively on the model** — Standard emergency protocols must always take precedence

### Explicit Non-Claims:
- The system does NOT predict clinical outcomes
- The system does NOT provide psychiatric diagnoses
- The system does NOT replace professional mental health assessment
- The system does NOT claim clinical accuracy
- Dummy/placeholder data must NEVER be labeled as AI analysis results
