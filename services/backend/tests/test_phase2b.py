"""
Phase 2B Tests: Core Victim Data Flow

Tests cover:
- User retrieval (valid, not found)
- Consent (valid, unknown user, repeated)
- Check-in (valid, unknown user, no consent, invalid payload, persistence)
- Deterministic risk calculator (low, moderate, high, critical, contributing factors)
- Check-in history (empty, multiple, newest-first ordering)
"""

import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.asyncio

# ----------------------------------------------------------------
# Known seeded user IDs from 001_demo_data.sql
# ----------------------------------------------------------------
PRIYA_ID = "11111111-1111-1111-1111-111111111111"
UNKNOWN_ID = "ffffffff-ffff-ffff-ffff-ffffffffffff"


# ==================================================================
# USER RETRIEVAL TESTS
# ==================================================================

async def test_get_user_success(client: AsyncClient):
    """GET /api/v1/users/{user_id} with a known seeded user."""
    response = await client.get(f"/api/v1/users/{PRIYA_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Priya Sharma"
    assert data["id"] == PRIYA_ID
    # Phone should NOT be in response
    assert "phone" not in data


async def test_get_user_not_found(client: AsyncClient):
    """GET /api/v1/users/{user_id} with a non-existent user."""
    response = await client.get(f"/api/v1/users/{UNKNOWN_ID}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# ==================================================================
# CONSENT TESTS
# ==================================================================

async def test_consent_success(client: AsyncClient):
    """POST /api/v1/users/{user_id}/consent with a valid user."""
    response = await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == PRIYA_ID
    assert data["consent_type"] == "data_collection_and_assessment"
    assert data["user_consent_given"] is True
    assert data["user_consent_date"] is not None


async def test_consent_unknown_user(client: AsyncClient):
    """POST /api/v1/users/{user_id}/consent with an unknown user."""
    response = await client.post(
        f"/api/v1/users/{UNKNOWN_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_consent_repeated(client: AsyncClient):
    """POST /api/v1/users/{user_id}/consent twice — should succeed both times.
    Each call creates a new consent_log entry, reflecting re-consent."""
    # First consent
    r1 = await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )
    assert r1.status_code == 201

    # Second consent (re-consent)
    r2 = await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )
    assert r2.status_code == 201
    # Both are valid, each creates a separate log
    assert r1.json()["id"] != r2.json()["id"]


# ==================================================================
# CHECK-IN TESTS
# ==================================================================

VALID_CHECK_IN_PAYLOAD = {
    "mode": "questionnaire",
    "mood": "anxious",
    "domain_scores": [
        {"domain": "mood", "score": 6},
        {"domain": "sleep", "score": 8},
        {"domain": "safety", "score": 3},
        {"domain": "social_support", "score": 5},
        {"domain": "legal_anxiety", "score": 7},
    ],
    "duration_seconds": 120,
}


async def test_checkin_success(client: AsyncClient):
    """POST /api/v1/users/{user_id}/check-ins with consent given."""
    # Ensure consent is given first
    await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )

    response = await client.post(
        f"/api/v1/users/{PRIYA_ID}/check-ins",
        json=VALID_CHECK_IN_PAYLOAD,
    )
    assert response.status_code == 201
    data = response.json()
    assert "check_in_id" in data
    assert data["risk_level"] in ("stable", "moderate", "high", "critical")
    assert 0 <= data["risk_score"] <= 100
    assert 0 <= data["wellbeing_score"] <= 100
    assert isinstance(data["contributing_factors"], list)
    assert len(data["domain_scores"]) == 5
    assert "disclaimer" in data


async def test_checkin_unknown_user(client: AsyncClient):
    """POST /api/v1/users/{user_id}/check-ins with unknown user."""
    response = await client.post(
        f"/api/v1/users/{UNKNOWN_ID}/check-ins",
        json=VALID_CHECK_IN_PAYLOAD,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_checkin_without_consent(client: AsyncClient, async_session_maker):
    """POST /api/v1/users/{user_id}/check-ins without consent -> 403."""
    # Use Kavitha who hasn't consented (reset her consent to be safe)
    kavitha_id = "22222222-2222-2222-2222-222222222222"
    from sqlalchemy import update
    from app.models.user import User

    async with async_session_maker() as session:
        await session.execute(
            update(User)
            .where(User.id == UUID(kavitha_id))
            .values(consent_given=False, consent_date=None)
        )
        await session.commit()

    response = await client.post(
        f"/api/v1/users/{kavitha_id}/check-ins",
        json=VALID_CHECK_IN_PAYLOAD,
    )
    assert response.status_code == 403
    assert "consent" in response.json()["detail"].lower()


async def test_checkin_invalid_payload(client: AsyncClient):
    """POST /api/v1/users/{user_id}/check-ins with invalid data."""
    # Ensure consent
    await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )

    # Missing domain_scores
    response = await client.post(
        f"/api/v1/users/{PRIYA_ID}/check-ins",
        json={"mode": "questionnaire"},
    )
    assert response.status_code == 422


async def test_checkin_invalid_domain_score(client: AsyncClient):
    """POST /api/v1/users/{user_id}/check-ins with out-of-range domain score."""
    await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )

    response = await client.post(
        f"/api/v1/users/{PRIYA_ID}/check-ins",
        json={
            "mode": "questionnaire",
            "domain_scores": [{"domain": "mood", "score": 15}],
        },
    )
    assert response.status_code == 422


async def test_checkin_domain_persistence(client: AsyncClient):
    """Verify check-in and domain scores persist to the database."""
    await client.post(
        f"/api/v1/users/{PRIYA_ID}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )

    response = await client.post(
        f"/api/v1/users/{PRIYA_ID}/check-ins",
        json=VALID_CHECK_IN_PAYLOAD,
    )
    assert response.status_code == 201
    check_in_id = response.json()["check_in_id"]

    # Verify we can retrieve it from history
    history = await client.get(f"/api/v1/users/{PRIYA_ID}/check-ins")
    assert history.status_code == 200
    data = history.json()
    assert any(item["id"] == check_in_id for item in data)

    matched = next(item for item in data if item["id"] == check_in_id)
    assert len(matched["domain_scores"]) == 5


# ==================================================================
# RISK CALCULATOR TESTS (unit-level, via the service module)
# ==================================================================

async def test_risk_low():
    """All domains low -> stable risk."""
    from app.services.risk_calculator import calculate_risk

    result = calculate_risk({
        "mood": 1, "sleep": 2, "safety": 0, "social_support": 1, "legal_anxiety": 2,
    })
    assert result["risk_level"] == "stable"
    assert result["risk_score"] <= 25
    assert result["wellbeing_score"] >= 75
    assert result["contributing_factors"] == []


async def test_risk_moderate():
    """Mixed domain scores -> moderate risk."""
    from app.services.risk_calculator import calculate_risk

    result = calculate_risk({
        "mood": 5, "sleep": 4, "safety": 3, "social_support": 4, "legal_anxiety": 5,
    })
    assert result["risk_level"] == "moderate"


async def test_risk_high():
    """High scores -> high risk."""
    from app.services.risk_calculator import calculate_risk

    result = calculate_risk({
        "mood": 7, "sleep": 8, "safety": 5, "social_support": 6, "legal_anxiety": 7,
    })
    assert result["risk_level"] == "high"
    assert "sleep difficulty" in result["contributing_factors"]
    assert "low mood / emotional distress" in result["contributing_factors"]
    assert "legal anxiety" in result["contributing_factors"]


async def test_risk_critical():
    """Maximum scores -> critical risk."""
    from app.services.risk_calculator import calculate_risk

    result = calculate_risk({
        "mood": 9, "sleep": 8, "safety": 8, "social_support": 7, "legal_anxiety": 9,
    })
    assert result["risk_level"] == "critical"
    assert result["risk_score"] >= 75
    assert len(result["contributing_factors"]) >= 3


async def test_risk_contributing_factors():
    """Contributing factors only include domains >= threshold."""
    from app.services.risk_calculator import calculate_risk

    result = calculate_risk({
        "mood": 2, "sleep": 9, "safety": 1, "social_support": 0, "legal_anxiety": 8,
    })
    assert "sleep difficulty" in result["contributing_factors"]
    assert "legal anxiety" in result["contributing_factors"]
    assert "low mood / emotional distress" not in result["contributing_factors"]


# ==================================================================
# CHECK-IN HISTORY TESTS
# ==================================================================

async def test_history_empty(client: AsyncClient):
    """GET /api/v1/users/{user_id}/check-ins for user with no check-ins."""
    # Use Lakshmi who likely has no check-ins yet
    lakshmi_id = "33333333-3333-3333-3333-333333333333"
    response = await client.get(f"/api/v1/users/{lakshmi_id}/check-ins")
    assert response.status_code == 200
    assert response.json() == []


async def test_history_multiple_newest_first(client: AsyncClient):
    """GET /api/v1/users/{user_id}/check-ins returns multiple, newest first."""
    # Use Sunita for isolation
    sunita_id = "44444444-4444-4444-4444-444444444444"

    # Give consent
    await client.post(
        f"/api/v1/users/{sunita_id}/consent",
        json={"consent_type": "data_collection_and_assessment"},
    )

    # Submit two check-ins
    payload_1 = {
        "mode": "questionnaire",
        "mood": "calm",
        "domain_scores": [
            {"domain": "mood", "score": 2},
            {"domain": "sleep", "score": 1},
            {"domain": "safety", "score": 1},
            {"domain": "social_support", "score": 2},
            {"domain": "legal_anxiety", "score": 1},
        ],
    }
    payload_2 = {
        "mode": "questionnaire",
        "mood": "stressed",
        "domain_scores": [
            {"domain": "mood", "score": 7},
            {"domain": "sleep", "score": 6},
            {"domain": "safety", "score": 5},
            {"domain": "social_support", "score": 4},
            {"domain": "legal_anxiety", "score": 8},
        ],
    }

    r1 = await client.post(f"/api/v1/users/{sunita_id}/check-ins", json=payload_1)
    assert r1.status_code == 201

    r2 = await client.post(f"/api/v1/users/{sunita_id}/check-ins", json=payload_2)
    assert r2.status_code == 201

    # Fetch history
    response = await client.get(f"/api/v1/users/{sunita_id}/check-ins")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

    # Verify newest first
    timestamps = [item["created_at"] for item in data]
    assert timestamps == sorted(timestamps, reverse=True)
