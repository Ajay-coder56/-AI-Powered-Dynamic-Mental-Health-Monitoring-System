import pytest
from app.seeds.phase5_seed import seed_demo_data
from app.models.case import Case
from app.models.alert import Alert
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_demo_seeding(async_session_maker):
    async with async_session_maker() as db_session:
        await seed_demo_data(db_session)
        result = await db_session.execute(select(Case).where(Case.case_number.in_(['DEMO-A', 'DEMO-B', 'DEMO-C', 'DEMO-D', 'DEMO-E'])))
        cases = result.scalars().all()
        assert len(cases) == 5
