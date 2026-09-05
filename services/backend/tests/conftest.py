import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import app

DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"

from sqlalchemy.pool import NullPool

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(DATABASE_URL, poolclass=NullPool)

@pytest.fixture(scope="session")
def async_session_maker(engine):
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from app.database import get_db

@pytest_asyncio.fixture
async def client(async_session_maker):
    async def override_get_db():
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()
