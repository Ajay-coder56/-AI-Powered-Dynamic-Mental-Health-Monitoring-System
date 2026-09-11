from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
import json
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.models.consent_log import ConsentLog
from app.models.check_in import CheckInSession, CheckInDomain
from app.schemas.user import UserResponse
from app.schemas.consent import ConsentRequest, ConsentResponse
from app.schemas.check_in import (
    CheckInCreateRequest,
    CheckInResultResponse,
    CheckInHistoryItem,
    DomainScoreResponse,
)
from app.risk_engine.service import get_risk_engine_service
from app.risk_engine.schemas import RiskInput

router = APIRouter()


# ------------------------------------------------------------------
# Helper: fetch user or raise 404
# ------------------------------------------------------------------
async def _get_user_or_404(user_id: UUID, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ==================================================================
# STEP 2 — GET /api/v1/users/{user_id}
# ==================================================================
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a user's non-sensitive profile information."""
    user = await _get_user_or_404(user_id, db)
    return user


# ==================================================================
# STEP 3 — POST /api/v1/users/{user_id}/consent
# ==================================================================
@router.post("/{user_id}/consent", response_model=ConsentResponse, status_code=201)
async def grant_consent(
    user_id: UUID,
    body: ConsentRequest,
    db: AsyncSession = Depends(get_db),
):
    """Record explicit user consent and update the user's consent status."""
    user = await _get_user_or_404(user_id, db)

    now = datetime.now(timezone.utc)

    # Create consent log entry
    consent_log = ConsentLog(
        user_id=user.id,
        consent_type=body.consent_type,
        ip_address=body.ip_address,
        user_agent=body.user_agent,
    )
    db.add(consent_log)

    # Update user consent fields
    user.consent_given = True
    user.consent_date = now
    user.updated_at = now

    await db.commit()
    await db.refresh(consent_log)
    await db.refresh(user)

    return ConsentResponse(
        id=consent_log.id,
        user_id=consent_log.user_id,
        consent_type=consent_log.consent_type,
        created_at=consent_log.created_at,
        user_consent_given=user.consent_given,
        user_consent_date=user.consent_date,
    )


# ==================================================================
# STEP 4 & 5 — POST /api/v1/users/{user_id}/check-ins
# ==================================================================
@router.post(
    "/{user_id}/check-ins",
    response_model=CheckInResultResponse,
    status_code=201,
)
async def submit_check_in(
    user_id: UUID,
    body: CheckInCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Submit a mental-health check-in assessment and receive a deterministic risk result.

    NOTE: The risk calculation is a deterministic engineering baseline,
    NOT a clinically validated assessment.
    """
    user = await _get_user_or_404(user_id, db)

    # Verify consent
    if not user.consent_given:
        raise HTTPException(
            status_code=403,
            detail="User has not given consent. Consent is required before check-in.",
        )

    # Build standardized RiskInput for the engine
    domain_scores_dict = {ds.domain.value: ds.score for ds in body.domain_scores}

    risk_input = RiskInput(
        user_id=user.id,
        timestamp=None,  # Let the engine set it
        mode=body.mode.value,
        mood=body.mood,
        domain_scores=domain_scores_dict,
        text_content=body.text_content,
    )

    # Evaluate risk through the engine service
    risk_service = get_risk_engine_service()
    risk_result = risk_service.evaluate(risk_input)

    # Inject fusion analysis into answers for Phase 3F Explainability retrieval
    answers = body.answers or {}
    if risk_result.fusion_analysis:
        answers["fusion_analysis"] = risk_result.fusion_analysis

    # Create check-in record (same DB fields as before)
    check_in = CheckInSession(
        user_id=user.id,
        case_id=user.case_id,
        mode=body.mode.value,
        answers=answers,
        raw_score=risk_result.raw_score,
        wellbeing_score=risk_result.wellbeing_score,
        risk_level=risk_result.risk_level.value,
        mood=body.mood,
        duration_seconds=body.duration_seconds,
    )
    db.add(check_in)
    await db.flush()  # get the generated ID

    # Create domain score records
    for ds in body.domain_scores:
        domain_record = CheckInDomain(
            check_in_id=check_in.id,
            domain=ds.domain.value,
            score=ds.score,
        )
        db.add(domain_record)

    # Update case total_sessions if applicable
    if user.case_id:
        from app.models.case import Case

        case_result = await db.execute(select(Case).where(Case.id == user.case_id))
        case = case_result.scalars().first()
        if case:
            case.total_sessions = (case.total_sessions or 0) + 1
            case.risk_score = risk_result.risk_score
            case.risk_level = risk_result.risk_level.value

    await db.commit()
    await db.refresh(check_in)

    # Phase 4: Trigger Alerts Evaluation
    if user.case_id:
        try:
            from app.services.alert_service import trigger_alerts_for_case
            await trigger_alerts_for_case(db, user.case_id)
            await db.commit()
        except Exception as e:
            # We don't want alert failures to crash the check-in process
            import logging
            logging.error(f"Failed to process alerts for case {user.case_id}: {str(e)}")

    return CheckInResultResponse(
        check_in_id=check_in.id,
        raw_score=risk_result.raw_score,
        wellbeing_score=risk_result.wellbeing_score,
        risk_score=risk_result.risk_score,
        risk_level=risk_result.risk_level.value,
        mood=body.mood,
        contributing_factors=risk_result.contributing_factors,
        domain_scores=[
            DomainScoreResponse(domain=ds.domain.value, score=ds.score)
            for ds in body.domain_scores
        ],
        created_at=check_in.created_at,
        nlp_analysis=risk_result.nlp_analysis,
        speech_analysis=risk_result.speech_analysis,
        fusion_analysis=risk_result.fusion_analysis,
    )


# ==================================================================
# STEP 5.5 — POST /api/v1/users/{user_id}/voice-check-ins
# ==================================================================
@router.post(
    "/{user_id}/voice-check-ins",
    response_model=CheckInResultResponse,
    status_code=201,
)
async def submit_voice_check_in(
    user_id: UUID,
    audio_file: UploadFile = File(...),
    domain_scores: str = Form(...),
    mood: str = Form(None),
    duration_seconds: int = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Phase 3C: Submit a voice check-in assessment.
    Accepts multipart/form-data with audio and JSON domain_scores.
    """
    user = await _get_user_or_404(user_id, db)

    if not user.consent_given:
        raise HTTPException(status_code=403, detail="Consent is required before check-in.")

    # Validate audio
    if not audio_file.filename:
        raise HTTPException(status_code=400, detail="Audio file required.")
        
    audio_bytes = await audio_file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file.")
    if len(audio_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file too large (max 10MB).")

    # Parse JSON domain_scores
    try:
        domain_scores_list = json.loads(domain_scores)
        # Verify structure
        domain_scores_dict = {}
        for ds in domain_scores_list:
            if ds["score"] < 0 or ds["score"] > 10:
                raise ValueError("Score out of bounds")
            domain_scores_dict[ds["domain"]] = ds["score"]
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid domain_scores JSON: {e}")

    # Evaluate Risk
    from app.risk_engine.schemas import RiskInput
    from app.risk_engine.service import get_risk_engine_service
    risk_input = RiskInput(
        user_id=user.id,
        timestamp=None,
        mode="voice",
        mood=mood,
        domain_scores=domain_scores_dict,
        audio_bytes=audio_bytes,
    )
    risk_service = get_risk_engine_service()
    risk_result = risk_service.evaluate(risk_input)

    answers = {}
    if risk_result.fusion_analysis:
        answers["fusion_analysis"] = risk_result.fusion_analysis

    # Save CheckIn
    from app.models.check_in import CheckInSession, CheckInDomain
    check_in = CheckInSession(
        user_id=user.id,
        case_id=user.case_id,
        mode="voice",
        answers=answers,
        raw_score=risk_result.raw_score,
        wellbeing_score=risk_result.wellbeing_score,
        risk_level=risk_result.risk_level.value,
        mood=mood,
        duration_seconds=duration_seconds,
    )
    db.add(check_in)
    await db.flush()

    for domain_name, score in domain_scores_dict.items():
        db.add(CheckInDomain(check_in_id=check_in.id, domain=domain_name, score=score))

    if user.case_id:
        from app.models.case import Case
        case_result = await db.execute(select(Case).where(Case.id == user.case_id))
        case = case_result.scalars().first()
        if case:
            case.total_sessions = (case.total_sessions or 0) + 1
            case.risk_score = risk_result.risk_score
            case.risk_level = risk_result.risk_level.value

    await db.commit()
    await db.refresh(check_in)
    
    # Phase 4: Trigger Alerts Evaluation
    if user.case_id:
        try:
            from app.services.alert_service import trigger_alerts_for_case
            await trigger_alerts_for_case(db, user.case_id)
            await db.commit()
        except Exception as e:
            import logging
            logging.error(f"Failed to process alerts for case {user.case_id}: {str(e)}")
            
    # We do NOT persist the raw audio bytes or save them anywhere in DB.

    from app.schemas.check_in import DomainScoreResponse
    
    return CheckInResultResponse(
        check_in_id=check_in.id,
        raw_score=risk_result.raw_score,
        wellbeing_score=risk_result.wellbeing_score,
        risk_score=risk_result.risk_score,
        risk_level=risk_result.risk_level.value,
        mood=mood,
        contributing_factors=risk_result.contributing_factors,
        domain_scores=[DomainScoreResponse(domain=k, score=v) for k, v in domain_scores_dict.items()],
        created_at=check_in.created_at,
        nlp_analysis=risk_result.nlp_analysis,
        speech_analysis=risk_result.speech_analysis,
        fusion_analysis=risk_result.fusion_analysis,
    )


# ==================================================================
# STEP 6 — GET /api/v1/users/{user_id}/check-ins
# ==================================================================
@router.get("/{user_id}/check-ins", response_model=list[CheckInHistoryItem])
async def get_check_in_history(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a user's check-in history, newest first."""
    await _get_user_or_404(user_id, db)

    result = await db.execute(
        select(CheckInSession)
        .where(CheckInSession.user_id == user_id)
        .order_by(CheckInSession.created_at.desc())
    )
    check_ins = result.scalars().all()

    history = []
    for ci in check_ins:
        # Fetch associated domain scores
        domain_result = await db.execute(
            select(CheckInDomain).where(CheckInDomain.check_in_id == ci.id)
        )
        domains = domain_result.scalars().all()

        history.append(
            CheckInHistoryItem(
                id=ci.id,
                mode=ci.mode,
                raw_score=ci.raw_score,
                wellbeing_score=ci.wellbeing_score,
                risk_level=ci.risk_level,
                mood=ci.mood,
                duration_seconds=ci.duration_seconds,
                created_at=ci.created_at,
                domain_scores=[
                    DomainScoreResponse(domain=d.domain, score=d.score)
                    for d in domains
                ],
            )
        )

    return history

# ==================================================================
@router.get("/{user_id}/risk/trajectory")
async def get_risk_trajectory(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve deterministic temporal risk trajectory (Phase 3E).
    Consumes historical fused risk scores (100 - wellbeing_score) to compute
    longitudinal early-warning signals and trend features.
    """
    await _get_user_or_404(user_id, db)
    
    # We need historical observations, order doesn't matter for the query since TemporalEngine sorts them
    # But filtering for non-null wellbeing_score is essential for fused score derivation.
    result = await db.execute(
        select(CheckInSession)
        .where(CheckInSession.user_id == user_id, CheckInSession.wellbeing_score.isnot(None))
    )
    check_ins = result.scalars().all()
    
    from ai.distress import TemporalObservation, TemporalInput, TemporalRiskEngine
    
    observations = []
    for ci in check_ins:
        if ci.created_at and ci.risk_level:
            fused_score = 100 - ci.wellbeing_score
            observations.append(
                TemporalObservation(
                    timestamp=ci.created_at,
                    risk_score=fused_score,
                    risk_level=ci.risk_level
                )
            )
            
    temporal_input = TemporalInput(
        user_id=str(user_id),
        observations=observations
    )
    
    temporal_engine = TemporalRiskEngine()
    result = temporal_engine.analyze(temporal_input)
    
    # Return as dict using model_dump
    return result.model_dump()
