from fastapi import APIRouter
from app.schemas.case import CaseCreate, CaseResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CaseResponse])
async def list_cases():
    # TODO: Implement case listing
    return []

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: int):
    # TODO: Implement get single case
    pass

@router.post("/", response_model=CaseResponse)
async def create_case(case: CaseCreate):
    # TODO: Implement case creation
    pass

@router.post("/{case_id}/assign")
async def assign_counsellor(case_id: int, counsellor_id: int):
    # TODO: Implement case assignment
    pass
