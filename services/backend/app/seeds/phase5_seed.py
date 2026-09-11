import uuid
from datetime import datetime, timedelta

from app.security import get_password_hash

from app.models.counsellor import Counsellor
from app.models.user import User
from app.models.case import Case
from app.models.check_in import CheckInSession
from app.models.alert import Alert

async def seed_demo_data(db):
    # Deterministic Seed Mechanism
    demo_counsellor_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    
    # Check if already seeded
    existing = await db.get(Counsellor, demo_counsellor_id)
    if existing:
        return # Already seeded
        
    counsellor = Counsellor(
        id=demo_counsellor_id,
        email="demo@sih.gov.in",
        password_hash=get_password_hash("password123"),
        name="Demo Counsellor",
        title="Demo Court"
    )
    db.add(counsellor)
    await db.flush()  # Flush counsellor so cases can reference it via FK
    
    # CASE A: Low/stable
    case_a_id = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    case_a = Case(
        id=case_a_id, case_number="DEMO-A", counsellor_id=demo_counsellor_id,
        case_type="Civil", risk_score=20, risk_level="stable", trend="stable", status="active"
    )
    db.add(case_a)
    
    # CASE B: Medium + short-term worsening
    case_b_id = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    case_b = Case(
        id=case_b_id, case_number="DEMO-B", counsellor_id=demo_counsellor_id,
        case_type="Family", risk_score=60, risk_level="moderate", trend="worsening", status="active"
    )
    db.add(case_b)
    
    # CASE C: High + persistent worsening
    case_c_id = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
    case_c = Case(
        id=case_c_id, case_number="DEMO-C", counsellor_id=demo_counsellor_id,
        case_type="Criminal", risk_score=85, risk_level="high", trend="worsening", status="active"
    )
    db.add(case_c)
    
    # CASE D: Critical risk
    case_d_id = uuid.UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
    case_d = Case(
        id=case_d_id, case_number="DEMO-D", counsellor_id=demo_counsellor_id,
        case_type="Domestic Violence", risk_score=95, risk_level="critical", trend="worsening", status="active"
    )
    db.add(case_d)
    
    # CASE E: Conflicting/low-quality data
    case_e_id = uuid.UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee")
    case_e = Case(
        id=case_e_id, case_number="DEMO-E", counsellor_id=demo_counsellor_id,
        case_type="Civil", risk_score=40, risk_level="moderate", trend="stable", status="active"
    )
    db.add(case_e)
    
    await db.flush()
    
    # Alerts
    # Critical alert for D
    alert_d = Alert(
        id=uuid.UUID("d1111111-1111-1111-1111-111111111111"),
        case_id=case_d_id, severity="critical", type="CRITICAL_RISK",
        title="Critical Danger", message="High imminent risk", is_read=False, is_resolved=False
    )
    db.add(alert_d)
    
    # Resolved alert for C
    alert_c = Alert(
        id=uuid.UUID("c1111111-1111-1111-1111-111111111111"),
        case_id=case_c_id, severity="high", type="HIGH_RISK",
        title="High Risk", message="Patient needs attention", is_read=True, is_resolved=True,
        resolved_by=demo_counsellor_id
    )
    db.add(alert_c)
    
    await db.commit()
