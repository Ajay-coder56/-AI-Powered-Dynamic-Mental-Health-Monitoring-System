from fastapi import APIRouter
from app.schemas.alert import AlertResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def list_alerts():
    # TODO: Implement alert listing
    return []

@router.put("/{alert_id}/resolve")
async def resolve_alert(alert_id: int):
    # TODO: Implement alert resolution
    pass
