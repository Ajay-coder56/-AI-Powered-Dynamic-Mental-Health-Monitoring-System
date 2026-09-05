import asyncio
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.counsellor import Counsellor
from app.models.user import User

DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"

async def check_db_counts():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        counsellor_count = await session.scalar(select(func.count()).select_from(Counsellor))
        user_count = await session.scalar(select(func.count()).select_from(User))
        
        print(f"Counsellors Count: {counsellor_count}")
        print(f"Users Count: {user_count}")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_db_counts())
