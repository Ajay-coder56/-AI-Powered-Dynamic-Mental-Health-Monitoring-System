import pytest
from httpx import AsyncClient
import uuid
from app.models.case import Case
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_dashboard_summary_api(client: AsyncClient, async_session_maker):
    resp = await client.post('/api/v1/auth/login', data={'username': 'dr.meera.iyer@wcd.gov.in', 'password': 'password123'})
    token = resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    async with async_session_maker() as db_session:
        from app.models.counsellor import Counsellor
        c_res = await db_session.execute(select(Counsellor).where(Counsellor.email == 'dr.meera.iyer@wcd.gov.in'))
        counsellor = c_res.scalars().first()
        
        case = Case(case_number=f'CASE-{uuid.uuid4().hex[:6].upper()}', counsellor_id=counsellor.id, case_type='Civil', status='active', trend='worsening')
        db_session.add(case)
        await db_session.commit()
        
    response = await client.get('/api/v1/dashboard/summary', headers=headers)
    assert response.status_code == 200
    assert response.json()['cases_worsening'] >= 1
