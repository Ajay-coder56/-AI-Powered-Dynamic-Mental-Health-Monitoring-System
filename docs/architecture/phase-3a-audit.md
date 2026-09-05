# Phase 3A Audit — Current System Analysis

**Date**: 2026-09-05
**Phase**: 3A — AI / Risk Engine Foundation
**Status**: Pre-implementation audit

---

## Current Architecture Overview

```
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────────┐
│  React App  │────>│  Node Gateway │────>│  FastAPI Backend │────>│ PostgreSQL │
│ (apps/web)  │     │ (api-gateway) │     │ (services/      │     │ (mindsafe) │
│             │     │               │     │  backend)        │     │            │
└─────────────┘     └───────────────┘     └─────────────────┘     └────────────┘
```

### Backend Stack
- **Framework**: FastAPI 0.111.0
- **ORM**: SQLAlchemy 2.0.30 (async)
- **Database**: PostgreSQL via asyncpg
- **Validation**: Pydantic 2.7.2
- **Auth**: JWT via python-jose, bcrypt

---

## Current Risk Calculation Flow

```
POST /api/v1/users/{user_id}/check-ins
        │
        ▼
routers/users.py::submit_check_in()
        │
        ├── Validate user exists (404 if not)
        ├── Verify consent (403 if not)
        ├── Build domain_scores dict from request
        │
        ▼
services/risk_calculator.py::calculate_risk(domain_scores)
        │
        ├── Sum domain scores → raw_score (0-50)
        ├── Normalize → risk_score (0-100), wellbeing_score (0-100)
        ├── Map to risk_level via thresholds
        ├── Identify contributing factors (score >= 7)
        │
        ▼
Return dict: {raw_score, wellbeing_score, risk_score, risk_level, contributing_factors}
        │
        ▼
Store in check_ins table + check_in_domains table
Update case.risk_score / case.risk_level if applicable
Return CheckInResultResponse to client
```

### Algorithm Details

| Parameter | Value |
|-----------|-------|
| Domains | mood, sleep, safety, social_support, legal_anxiety |
| Domain range | 0-10 (0 = no distress, 10 = max distress) |
| Raw score | Sum of all domain scores (max 50) |
| Risk score | `round((raw / max) * 100)` |
| Wellbeing score | `round(((max - raw) / max) * 100)` |
| Stable threshold | raw_score 0-12 |
| Moderate threshold | raw_score 13-24 |
| High threshold | raw_score 25-37 |
| Critical threshold | raw_score 38-50 |
| Contributing factor | domain score >= 7 |

---

## Relevant Files

### Risk Calculation
| File | Purpose |
|------|---------|
| `services/backend/app/services/risk_calculator.py` | Core deterministic risk algorithm |
| `services/backend/app/services/scoring_service.py` | **DEAD CODE** — returns hardcoded 50, never used |

### Models
| File | Purpose |
|------|---------|
| `services/backend/app/models/check_in.py` | CheckInSession, CheckInDomain ORM models |
| `services/backend/app/models/user.py` | User model with consent fields |
| `services/backend/app/models/case.py` | Case model with risk_score, risk_level |

### Schemas
| File | Purpose |
|------|---------|
| `services/backend/app/schemas/check_in.py` | Request/response Pydantic models |

### Routers
| File | Purpose |
|------|---------|
| `services/backend/app/routers/users.py` | Check-in submit + history endpoints |

### Tests
| File | Test Count | Purpose |
|------|-----------|---------|
| `services/backend/tests/test_auth.py` | 8 | Authentication flow |
| `services/backend/tests/test_phase2b.py` | 18 | Victim data flow + risk calculator |

### AI Placeholders
| Directory | Content |
|-----------|---------|
| `ai/nlp/` | Empty directory |
| `ai/speech/` | Empty directory |
| `ai/distress/` | Empty directory |
| `ai/explainability/` | Empty directory |

---

## Dependencies

```
fastapi==0.111.0
uvicorn==0.30.1
sqlalchemy==2.0.30
alembic==1.13.1
pydantic==2.7.2
pydantic-settings==2.3.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
asyncpg==0.29.0
pytest, pytest-asyncio, httpx, bcrypt
```

---

## Technical Debt

1. **`scoring_service.py`** — Dead code returning hardcoded `50`, never imported.
2. **Risk calculation inline** — `calculate_risk()` is imported and called directly in the router with no abstraction layer.
3. **No engine interface** — No way to swap risk implementations without changing the router.
4. **No explainability** — No structured explanation of risk results.
5. **No engine versioning** — No metadata about which algorithm produced a result.
6. **No future AI boundaries** — Empty `ai/` directories with no interface contracts.

---

## Risks

1. **Router coupling** — Risk calculation is directly coupled to the API route. Any change to the algorithm requires modifying router code.
2. **No A/B testing support** — Cannot run multiple engines side-by-side.
3. **No explanation auditability** — No record of why a risk score was assigned.

---

## Recommended Phase 3A Changes

1. Create `risk_engine/` package with abstract interface, schemas, baseline engine, service, and registry.
2. Wrap existing `calculate_risk()` in `DeterministicBaselineEngine` with identical semantics.
3. Minimal router modification — swap direct call for engine service call.
4. Add standardized `RiskInput`/`RiskResult` schemas with future-proof optional fields.
5. Add explainability foundation with deterministic explanations.
6. Add engine versioning via `EngineRegistry`.
7. Create AI module boundary `__init__.py` files with interface documentation.
8. Add Phase 3A unit tests verifying parity with Phase 2.
9. Create architecture documentation.
10. **Do NOT** modify database schema, authentication, or frontend.
