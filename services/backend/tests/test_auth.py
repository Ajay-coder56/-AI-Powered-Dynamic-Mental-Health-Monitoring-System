import pytest
from httpx import AsyncClient
import asyncio
from sqlalchemy import update
from app.models.counsellor import Counsellor

pytestmark = pytest.mark.asyncio

async def test_login_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", data={
        "username": "dr.meera.iyer@wcd.gov.in",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", data={
        "username": "dr.meera.iyer@wcd.gov.in",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

async def test_login_unknown_email(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", data={
        "username": "nonexistent@wcd.gov.in",
        "password": "password123"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

async def test_get_me_success(client: AsyncClient):
    # First login
    login_response = await client.post("/api/v1/auth/login", data={
        "username": "dr.meera.iyer@wcd.gov.in",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Get me
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "dr.meera.iyer@wcd.gov.in"
    assert data["name"] == "Dr. Meera Iyer"
    assert data["role"] == "counsellor"

async def test_get_me_missing_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

async def test_get_me_invalid_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.token.value"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

async def test_inactive_counsellor(client: AsyncClient, async_session_maker):
    # Temporarily make counsellor inactive
    async with async_session_maker() as session:
        await session.execute(update(Counsellor).where(Counsellor.email == "dr.meera.iyer@wcd.gov.in").values(is_active=False))
        await session.commit()
        
    try:
        response = await client.post("/api/v1/auth/login", data={
            "username": "dr.meera.iyer@wcd.gov.in",
            "password": "password123"
        })
        assert response.status_code == 403
        assert response.json()["detail"] == "Inactive counsellor"
    finally:
        # Restore active status
        async with async_session_maker() as session:
            await session.execute(update(Counsellor).where(Counsellor.email == "dr.meera.iyer@wcd.gov.in").values(is_active=True))
            await session.commit()

async def test_get_me_expired_token(client: AsyncClient):
    from app.security import create_access_token
    from datetime import timedelta
    
    # Create token expired 1 minute ago
    expired_token = create_access_token(
        subject="00000000-0000-0000-0000-000000000001",
        expires_delta=timedelta(minutes=-1)
    )
    
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
