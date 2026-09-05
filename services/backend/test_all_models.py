import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.counsellor import Counsellor
from app.models.user import User
from app.models.case import Case
from app.models.alert import Alert
from app.models.case_note import CaseNote
from app.models.check_in import CheckInSession, CheckInDomain
from app.models.consent_log import ConsentLog
from app.models.hearing import Hearing
from app.models.notification import Notification

DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"

async def test_all():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    models = [
        ("Counsellor", Counsellor),
        ("User", User),
        ("Case", Case),
        ("Alert", Alert),
        ("CaseNote", CaseNote),
        ("CheckInSession", CheckInSession),
        ("CheckInDomain", CheckInDomain),
        ("ConsentLog", ConsentLog),
        ("Hearing", Hearing),
        ("Notification", Notification)
    ]
    
    try:
        async with async_session() as session:
            for name, model in models:
                try:
                    result = await session.execute(select(model).limit(1))
                    record = result.scalars().first()
                    if record:
                        print(f"[SUCCESS] {name} - ID Type: {type(record.id)}")
                    else:
                        print(f"[NO RECORD] {name} - (Query succeeded, but table is empty)")
                except Exception as e:
                    print(f"[FAILED] {name} - {type(e).__name__}: {e}")
                    # Rollback the session so subsequent queries can continue
                    await session.rollback()
    except Exception as e:
        print(f"CRASHED: {type(e).__name__} - {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_all())
