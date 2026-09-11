import pytest
from httpx import AsyncClient
from app.models.case import Case
from app.models.counsellor import Counsellor
from app.security import get_password_hash
import uuid
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_idor_case_analytics(client: AsyncClient, async_session_maker):
    resp = await client.post('/api/v1/auth/login', data={'username': 'dr.meera.iyer@wcd.gov.in', 'password': 'password123'})
    token = resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    other_counsellor_id = uuid.uuid4()
    other_case_id = f'CASE-{uuid.uuid4().hex[:6].upper()}'
    async with async_session_maker() as db_session:
        other_counsellor = Counsellor(
            id=other_counsellor_id,
            email=f'other-{uuid.uuid4().hex[:6]}@test.gov.in',
            password_hash=get_password_hash('testpassword'),
            name='Other Counsellor',
        )
        db_session.add(other_counsellor)
        await db_session.flush()
        case = Case(case_number=other_case_id, counsellor_id=other_counsellor_id, case_type='Criminal', status='active')
        db_session.add(case)
        await db_session.commit()
    
    response = await client.get(f'/api/v1/cases/{other_case_id}/analytics', headers=headers)
    assert response.status_code == 403
