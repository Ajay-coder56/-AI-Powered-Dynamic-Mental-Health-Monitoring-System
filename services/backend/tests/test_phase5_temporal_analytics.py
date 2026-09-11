import pytest
from httpx import AsyncClient
from sqlalchemy.future import select
from app.models.case import Case
from app.models.check_in import CheckInSession
import uuid

@pytest.mark.asyncio
async def test_case_analytics_api(client: AsyncClient, async_session_maker):
    resp = await client.post('/api/v1/auth/login', data={'username': 'dr.meera.iyer@wcd.gov.in', 'password': 'password123'})
    token = resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    async with async_session_maker() as db_session:
        from app.models.counsellor import Counsellor
        c_res = await db_session.execute(select(Counsellor).where(Counsellor.email == 'dr.meera.iyer@wcd.gov.in'))
        counsellor = c_res.scalars().first()
        
        case_id_str = f'CASE-{uuid.uuid4().hex[:6].upper()}'
        case = Case(case_number=case_id_str, counsellor_id=counsellor.id, case_type='Domestic Violence', risk_score=75, risk_level='high', status='active')
        db_session.add(case)
        await db_session.commit()
        
        ci1 = CheckInSession(case_id=case.id, mode='questionnaire', wellbeing_score=50, risk_level='moderate')
        db_session.add(ci1)
        await db_session.commit()
        
        ci2 = CheckInSession(case_id=case.id, mode='questionnaire', wellbeing_score=25, risk_level='high')
        db_session.add(ci2)
        await db_session.commit()
    
    response = await client.get(f'/api/v1/cases/{case_id_str}/analytics', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['latest_score'] == 75
    assert data['delta'] == 25
