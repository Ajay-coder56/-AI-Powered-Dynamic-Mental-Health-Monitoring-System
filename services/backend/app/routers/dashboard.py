from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_counsellor
from app.models.case import Case
from app.models.alert import Alert

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    counsellor=Depends(get_current_counsellor)
):
    # Total active cases
    cases_result = await db.execute(
        select(Case.status, Case.trend, func.count(Case.id))
        .where(Case.counsellor_id == counsellor.id)
        .group_by(Case.status, Case.trend)
    )
    cases_data = cases_result.all()
    
    total_active_cases = 0
    cases_worsening = 0
    cases_improving = 0
    cases_stable = 0
    
    for row in cases_data:
        status, trend, count = row
        if status == "active" or status == "monitoring": # Both represent active cases in terms of workload
            total_active_cases += count
            if trend == "worsening":
                cases_worsening += count
            elif trend == "improving":
                cases_improving += count
            elif trend == "stable":
                cases_stable += count

    # Alerts
    alerts_result = await db.execute(
        select(Alert.severity, Alert.is_resolved, Alert.is_read, func.count(Alert.id))
        .join(Case, Alert.case_id == Case.id)
        .where(Case.counsellor_id == counsellor.id)
        .group_by(Alert.severity, Alert.is_resolved, Alert.is_read)
    )
    alerts_data = alerts_result.all()
    
    open_alerts = 0
    critical_alerts = 0
    high_alerts = 0
    medium_alerts = 0
    low_alerts = 0
    acknowledged_alerts = 0
    resolved_alerts = 0
    
    for row in alerts_data:
        severity, is_resolved, is_read, count = row
        if is_resolved:
            resolved_alerts += count
        else:
            open_alerts += count
            if is_read:
                acknowledged_alerts += count
            if severity == "critical":
                critical_alerts += count
            elif severity == "high":
                high_alerts += count
            elif severity == "medium":
                medium_alerts += count
            elif severity == "low":
                low_alerts += count
                
    return {
        "counsellors_on_duty": 1,
        "avg_response_time": "5m",
        "total_active_cases": total_active_cases,
        "cases_worsening": cases_worsening,
        "cases_improving": cases_improving,
        "cases_stable": cases_stable,
        "open_alerts": open_alerts,
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts,
        "acknowledged_alerts": acknowledged_alerts,
        "resolved_alerts": resolved_alerts
    }
