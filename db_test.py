import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe"


async def test_conn():
    engine = create_async_engine(DATABASE_URL)

    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )

            tables = [row[0] for row in result]

            print("DB_CONNECTION: SUCCESS")
            print(f"TABLES_FOUND: {tables}")

    except Exception as e:
        print("DB_CONNECTION: FAILED")
        print(type(e).__name__)
        print(e)

    finally:
        await engine.dispose()


asyncio.run(test_conn())