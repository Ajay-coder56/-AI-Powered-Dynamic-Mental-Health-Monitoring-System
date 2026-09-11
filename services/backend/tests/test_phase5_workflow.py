import pytest
from httpx import AsyncClient
import uuid
from app.models.case import Case
from app.models.alert import Alert
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_end_to_end_workflow(client: AsyncClient, async_session_maker):
    resp = await client.post('/api/v1/auth/login', data={'username': 'dr.meera.iyer@wcd.gov.in', 'password': 'password123'})
    token = resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    case_id_str = f'CASE-WF-{uuid.uuid4().hex[:6].upper()}'
    async with async_session_maker() as db_session:
        from app.models.counsellor import Counsellor
        c_res = await db_session.execute(select(Counsellor).where(Counsellor.email == 'dr.meera.iyer@wcd.gov.in'))
        counsellor = c_res.scalars().first()
        
        case = Case(case_number=case_id_str, counsellor_id=counsellor.id, case_type='Civil', status='active')
        db_session.add(case)
        await db_session.commit()
        
        alert = Alert(case_id=case.id, severity='high', type='TEST', title='Test Alert', message='Workflow test', is_read=False, is_resolved=False)
        db_session.add(alert)
        await db_session.commit()
        
        alert_id = str(alert.id)
    
    assert (await client.get('/api/v1/dashboard/summary', headers=headers)).status_code == 200
    assert (await client.get(f'/api/v1/cases/{case_id_str}/analytics', headers=headers)).status_code == 200
    assert (await client.post(f'/api/v1/cases/{case_id_str}/notes', json={'content': 'E2E Test Note'}, headers=headers)).status_code == 200
    assert (await client.post(f'/api/v1/alerts/{alert_id}/acknowledge', headers=headers)).status_code == 200
    assert (await client.post(f'/api/v1/alerts/{alert_id}/resolve', headers=headers)).status_code == 200
