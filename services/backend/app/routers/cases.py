from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import uuid

from app.database import get_db
from app.dependencies import get_current_counsellor
from app.models.case import Case
from app.models.user import User
from app.models.check_in import CheckInSession, CheckInDomain
from app.schemas.case import CaseResponse
from ai.explainability.schemas import ExplainabilityResult, ExplainabilityInput
from ai.explainability.engine import DeterministicExplainabilityEngine
from ai.distress import TemporalRiskEngine, TemporalInput, TemporalObservation

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_cases(
    db: AsyncSession = Depends(get_db),
    counsellor=Depends(get_current_counsellor)
):
    """List cases assigned to the counsellor."""
    result = await db.execute(
        select(Case)
        .where(Case.counsellor_id == counsellor.id)
    )
    cases = result.scalars().all()
    
    # We will return dictionaries matching what the frontend expects
    out = []
    for c in cases:
        out.append({
            "id": c.case_number,
            "patientName": "Patient", # Masked for privacy
            "riskLevel": c.risk_level.capitalize() if c.risk_level else "Stable",
            "riskScore": c.risk_score if c.risk_score else 0,
            "trend": c.trend if c.trend else "stable",
            "nextSession": c.next_hearing_date.isoformat() if c.next_hearing_date else None,
            "streak": c.streak,
            "status": c.status
        })
    return out

@router.get("/{case_id}/explanation", response_model=ExplainabilityResult)
async def get_case_explanation(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    counsellor=Depends(get_current_counsellor)
):
    """
    Provide explainability decision support for a given case.
    Requires counsellor authentication.
    """
    # 1. Fetch case
    result = await db.execute(
        select(Case).where(Case.case_number == case_id)
    )
    case_obj = result.scalars().first()
    
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")
        
    if case_obj.counsellor_id != counsellor.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this case")
        
    # 2. Fetch user's check-ins
    ci_result = await db.execute(
        select(CheckInSession)
        .where(CheckInSession.case_id == case_obj.id, CheckInSession.wellbeing_score.isnot(None))
        .order_by(CheckInSession.created_at.desc())
    )
    check_ins = ci_result.scalars().all()
    
    if not check_ins:
        raise HTTPException(status_code=404, detail="No check-ins available for this case")
        
    latest_ci = check_ins[0]
    
    # 3. Fetch domain scores for latest check-in
    dom_result = await db.execute(
        select(CheckInDomain).where(CheckInDomain.check_in_id == latest_ci.id)
    )
    domains = dom_result.scalars().all()
    domain_dict = {d.domain: d.score for d in domains}
    
    # 4. Extract Modalities from answers if saved, otherwise reconstruct baseline
    modality_contributions = []
    conflict_detected = False
    
    if latest_ci.answers and isinstance(latest_ci.answers, dict) and "fusion_analysis" in latest_ci.answers:
        fusion = latest_ci.answers["fusion_analysis"]
        modality_contributions = fusion.get("modality_contributions", [])
        conflict_detected = fusion.get("conflict_detected", False)
    else:
        # Fallback to only baseline
        modality_contributions = [
            {
                "modality_name": "baseline",
                "is_available": True,
                "score_normalized": (100 - latest_ci.wellbeing_score) if latest_ci.wellbeing_score else 0,
                "confidence": 1.0,
                "effective_weight": 1.0
            },
            {"modality_name": "nlp", "is_available": False},
            {"modality_name": "speech", "is_available": False}
        ]
        
    # 5. Temporal Analysis (Phase 3E)
    observations = []
    for ci in reversed(check_ins): # chronological order
        fused_score = 100 - ci.wellbeing_score
        observations.append(
            TemporalObservation(
                timestamp=ci.created_at,
                risk_score=fused_score,
                risk_level=ci.risk_level
            )
        )
        
    temporal_input = TemporalInput(
        user_id=str(case_obj.victim_id),
        observations=observations
    )
    temporal_engine = TemporalRiskEngine()
    temporal_result = temporal_engine.analyze(temporal_input).model_dump()
    
    # 6. Explainability Engine
    explain_input = ExplainabilityInput(
        risk_score=(100 - latest_ci.wellbeing_score) if latest_ci.wellbeing_score else 0,
        risk_level=latest_ci.risk_level or "stable",
        wellbeing_score=latest_ci.wellbeing_score or 100,
        domain_scores=domain_dict,
        modality_contributions=modality_contributions,
        conflict_detected=conflict_detected,
        temporal_result=temporal_result
    )
    
    engine = DeterministicExplainabilityEngine()
    explanation = engine.generate_explanation(explain_input)
    
    return explanation
