# AI Roadmap — MindSafe

**Project**: SIH 2026 — AI Mental Health Monitoring System
**Problem Statement ID**: 26094
**Date**: 2026-09-05

---

## Phased AI Integration Strategy

```
Phase 3A ─── Risk Engine Foundation           ← CURRENT
    │
    ▼
Phase 3B ─── NLP / Text Analysis
    │
    ▼
Phase 3C ─── Speech / Voice Analysis
    │
    ▼
Phase 3D ─── Multimodal Risk Engine
    │
    ▼
Phase 3E ─── Temporal / Dynamic Risk
    │
    ▼
Phase 3F ─── Explainability
    │
    ▼
Phase 3G ─── Alerts / Early Warning
```

---

## Phase 3A — Risk Engine Foundation ✓

**Status**: COMPLETE

**Goal**: Create a clean, production-oriented Risk Engine architecture that allows future AI integration without major rewrites.

**Deliverables**:
- Abstract `RiskEngine` interface
- Standardized `RiskInput` / `RiskResult` schemas
- `DeterministicBaselineEngine` wrapping verified Phase 2 algorithm
- `RiskEngineService` separating engine from API layer
- `EngineRegistry` for versioning and metadata
- Explainability foundation (`RiskExplanation`)
- Future AI engine interface contracts
- AI module boundary definitions
- Safety documentation
- Phase 3A test suite

**Prerequisites**: Phase 2 (A+B+C) complete and verified.

---

## Phase 3B — NLP / Text Analysis ✓

**Status**: COMPLETE

**Goal**: Add natural language processing for analyzing free-text responses and voice transcripts for distress signals.

**Planned Work**:
- Implement `TextAnalysisEngine` interface
- Multilingual text analysis (Hindi, English, regional languages)
- IndicBERT-based distress/sentiment detection
- Keyword and phrase extraction for risk indicators
- Integration with `RiskInput.text_content` and `RiskInput.transcript` fields

**Interface**: `TextAnalysisEngine` (defined in `risk_engine/interface.py`)
**Module**: `ai/nlp/`

**Prerequisites**: Phase 3A complete. Multilingual training data available.

---

## Phase 3C — Speech / Voice Analysis ✓

**Status**: COMPLETE

**Goal**: Analyze voice/audio characteristics to produce a structured, explainable acoustic voice signal.

**Planned Work**:
- Implement `SpeechAnalysisEngine` interface
- Voice feature extraction (pitch, energy, pauses, speaking rate)
- IndicWhisper / Wav2Vec2-based speech processing
- OpenSMILE acoustic feature extraction
- Integration with `RiskInput.voice_features` field

**Interface**: `SpeechAnalysisEngine` (defined in `risk_engine/interface.py`)
**Module**: `ai/speech/`

**Prerequisites**: Phase 3A complete. Audio capture pipeline available.

---

## Phase 3D — Multimodal Fusion Layer ✓

**Status**: COMPLETE

**Goal**: Synthesize Baseline, NLP, and Speech signals into a unified RiskResult.

**Planned Work**:
- Developed dynamic fusion engine weighting modalities (60/20/20 baseline focus).
- Handled missing modalities (renormalization) & low confidence signals.
- Preserved 100% backward compatibility for risk levels & existing APIs.
- Register as alternative engine in `EngineRegistry`

**Module**: `ai/distress/`

**Prerequisites**: Phase 3B and 3C functional.

---

## Phase 3E — Temporal Risk Engine ✓

**Status**: COMPLETE

**Goal**: Analyze historical risk progression over time.

**Planned Work**:
- Developed independent temporal trend analysis module.
- Incorporated configurable analysis windows (7–14 days).
- Implemented deterministic slope and persistence/spike logic.
- Calculated deterministic early-warning engineering score.
- Kept strictly separate from clinical claims or alerting loops.

**Module**: `ai/distress/`

**Interface**: `TemporalRiskEngine` (defined in `risk_engine/interface.py`)

**Prerequisites**: Phase 3D complete. Sufficient historical check-in data.

---

## Phase 3F — Explainability & Decision Support ✓

**Status**: COMPLETE

**Goal**: Provide transparent, human-readable explanations of risk assessments for counsellors.

**Planned Work**:
- Replaced SHAP/LIME placeholders with a robust deterministic rule-based explainability engine.
- Implemented human-readable baseline domain contributions.
- Surfaced modality fusion logic, missing modalities, and signal conflicts.
- Connected longitudinal temporal explanations.
- Created `GET /api/v1/cases/{case_id}/explanation` counsellor API.
- Rebuilt frontend `CaseDetailPage` to consume and display AI decision support.
- Maintained strict non-clinical engineering claims.

**Interface**: `ExplainabilityEngine` (defined in `risk_engine/interface.py`)
**Module**: `ai/explainability/`

**Prerequisites**: Phase 3D complete. AI models producing non-trivial outputs.

**Note**: The Phase 3A deterministic baseline already provides rule-based explanations via `RiskExplanation`. Phase 3F extends this to AI model outputs.

---

## Phase 4 — Intervention & Alerts ✓

**Status**: COMPLETE

**Goal**: Transform AI insights into an actionable triage workflow for counsellors.

**Planned Work**:
- Developed `AlertEngine` with deterministic thresholds.
- Connected Alerts to Explainability and Temporal outputs.
- Deduplication rule prevents repeated spamming.
- Added API endpoints for viewing, acknowledging, and resolving alerts.
- Enforced strict case-level authorization (`Depends(get_current_counsellor)`).
- Human-in-the-loop: Counsellor decides intervention, AI does not act automatically.
- Case notes API implemented.

**Module**: `ai/alerts/` table and router
- Dashboard integration for real-time monitoring

**Prerequisites**: Phase 3E complete. Alert routing infrastructure available.

**Critical Safety Note**: Automated alerts must NEVER replace human judgment. All alerts require counsellor review. Emergency situations must follow standard emergency protocols regardless of model output.

---

## Cross-Cutting Concerns

### Clinical Validation
- No phase claims clinical validation
- Each phase requires explicit validation protocol before production use
- All outputs labeled as "engineering baseline" or "non-clinical prototype" until validated

### Data Privacy
- All AI processing must comply with data protection requirements
- Voice recordings and transcripts require explicit consent
- Model outputs should be auditable

### Model Governance
- Engine versioning via `EngineRegistry`
- A/B testing capability via multiple registered engines
- Rollback support via engine selection
- No model deployed without documented evaluation metrics
