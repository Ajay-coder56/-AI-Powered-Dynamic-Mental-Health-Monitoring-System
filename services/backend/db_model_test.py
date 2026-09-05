import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.counsellor import Counsellor
from app.models.user import User


DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"


async def test_query():
    engine = create_async_engine(DATABASE_URL)

    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    try:
        async with async_session() as session:
            result = await session.execute(
                select(Counsellor).limit(1)
            )

            counsellor = result.scalars().first()

            if counsellor:
                print(f"FOUND COUNSELLOR: {counsellor.email}")
                print(f"COUNSELLOR ID TYPE: {type(counsellor.id)}")
            else:
                print("NO COUNSELLOR FOUND")

            user_result = await session.execute(
                select(User).limit(1)
            )
            user = user_result.scalars().first()
            if user:
                print(f"FOUND USER: {user.name} ({user.phone})")
                print(f"USER ID TYPE: {type(user.id)}")
            else:
                print("NO USER FOUND")

    except Exception as e:
        print(f"CRASHED: {type(e).__name__} - {e}")

    finally:
        await engine.dispose()


asyncio.run(test_query())