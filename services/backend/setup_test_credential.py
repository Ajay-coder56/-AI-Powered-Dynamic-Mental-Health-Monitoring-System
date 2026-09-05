import asyncio
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from app.models.counsellor import Counsellor

DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"

async def setup_test_credential():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Hash "password123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(b"password123", salt).decode("utf-8")
    
    try:
        async with async_session() as session:
            await session.execute(
                update(Counsellor)
                .where(Counsellor.email == 'dr.meera.iyer@wcd.gov.in')
                .values(password_hash=hashed)
            )
            await session.commit()
            print("Successfully updated dr.meera.iyer@wcd.gov.in with test password: password123")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(setup_test_credential())
