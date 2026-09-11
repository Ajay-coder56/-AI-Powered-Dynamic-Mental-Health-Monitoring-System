from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import uuid

from app.database import get_db
from app.dependencies import get_current_counsellor
from app.models.alert import Alert
from app.models.case import Case
from app.schemas.alert import AlertResponse

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    db: AsyncSession = Depends(get_db),
    counsellor = Depends(get_current_counsellor)
):
    """List all alerts for cases assigned to this counsellor."""
    # Join with cases to ensure they belong to this counsellor
    result = await db.execute(
        select(Alert)
        .join(Case, Alert.case_id == Case.id)
        .where(Case.counsellor_id == counsellor.id)
        .order_by(Alert.created_at.desc())
    )
    alerts = result.scalars().all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    counsellor = Depends(get_current_counsellor)
):
    result = await db.execute(
        select(Alert)
        .join(Case, Alert.case_id == Case.id)
        .where(Alert.id == alert_id, Case.counsellor_id == counsellor.id)
    )
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found or unauthorized")
    return alert

@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    counsellor = Depends(get_current_counsellor)
):
    """Mark alert as read/acknowledged"""
    result = await db.execute(
        select(Alert)
        .join(Case, Alert.case_id == Case.id)
        .where(Alert.id == alert_id, Case.counsellor_id == counsellor.id)
    )
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found or unauthorized")
        
    alert.is_read = True
    await db.commit()
    return {"status": "success", "message": "Alert acknowledged"}

@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    counsellor = Depends(get_current_counsellor)
):
    """Mark alert as resolved by this counsellor"""
    result = await db.execute(
        select(Alert)
        .join(Case, Alert.case_id == Case.id)
        .where(Alert.id == alert_id, Case.counsellor_id == counsellor.id)
    )
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found or unauthorized")
        
    if alert.is_resolved:
        raise HTTPException(status_code=400, detail="Alert is already resolved")
        
    alert.is_resolved = True
    alert.resolved_by = counsellor.id
    from datetime import datetime
    import pytz
    alert.resolved_at = datetime.now(pytz.utc)
    
    await db.commit()
    return {"status": "success", "message": "Alert resolved"}

@router.post("/{alert_id}/dismiss")
async def dismiss_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    counsellor = Depends(get_current_counsellor)
):
    """Mark alert as resolved (dismissed)"""
    return await resolve_alert(alert_id, db, counsellor)
