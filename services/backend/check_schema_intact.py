import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def check():
    engine = create_async_engine("postgresql+asyncpg://mindsafe_admin:changeme_dev_only@localhost:5432/mindsafe")
    async with engine.connect() as conn:
        r = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
        tables = [row[0] for row in r.fetchall()]
        print("Tables:", tables)
        
        r = await conn.execute(text("SELECT t.typname FROM pg_type t JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace WHERE n.nspname = 'public' AND t.typtype = 'e' ORDER BY t.typname"))
        enums = [row[0] for row in r.fetchall()]
        print("Enums:", enums)
        
        for t in ["counsellors", "users", "cases", "alerts", "hearings"]:
            r = await conn.execute(text(f"SELECT count(*) FROM {t}"))
            print(f"{t}: {r.scalar()} rows")
    await engine.dispose()

asyncio.run(check())
