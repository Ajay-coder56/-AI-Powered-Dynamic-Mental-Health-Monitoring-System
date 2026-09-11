import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.alert import Alert
from ai.explainability.schemas import ExplainabilityResult
from ai.alerts.engine import DeterministicAlertEngine

class AlertService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = DeterministicAlertEngine()

    async def evaluate_and_create_alert(self, case_id: uuid.UUID, explainability: ExplainabilityResult) -> Optional[Alert]:
        """
        Evaluate explainability data against deterministic alert rules.
        If an alert should be created, deduplicate against existing open alerts,
        and persist to the database.
        """
        result = self.engine.evaluate(explainability)
        
        if not result.should_alert:
            return None
            
        # Deduplication rule: same case + same type + not resolved
        existing_result = await self.db.execute(
            select(Alert)
            .where(
                Alert.case_id == case_id,
                Alert.type == result.alert_type.value,
                Alert.is_resolved == False
            )
        )
        existing_alert = existing_result.scalars().first()
        
        if existing_alert:
            # If we already have an open alert of this type, we can optionally update its message
            # For this MVP, we avoid spamming and just return the existing alert without duplicating.
            return existing_alert
            
        # Create new alert
        new_alert = Alert(
            case_id=case_id,
            severity=result.priority.value,
            type=result.alert_type.value,
            title=result.title,
            message=result.reason,
            ai_explanation=explainability.summary,
            recommended_actions=result.recommended_actions,
            is_read=False,
            is_resolved=False
        )
        
        self.db.add(new_alert)
        await self.db.flush()
        
        # In a full system, we might trigger a NotificationService here
        # e.g., NotificationService.send_counsellor_notification(new_alert)
        
        return new_alert

async def trigger_alerts_for_case(db: AsyncSession, case_id: uuid.UUID):
    """
    Called after a new check-in is saved. Pulls the latest check-in,
    generates the explainability result, and evaluates alerts.
    """
    from app.models.check_in import CheckInSession, CheckInDomain
    from ai.distress import TemporalRiskEngine, TemporalInput, TemporalObservation
    from ai.explainability.schemas import ExplainabilityInput
    
    # 1. Fetch user's check-ins
    ci_result = await db.execute(
        select(CheckInSession)
        .where(CheckInSession.case_id == case_id, CheckInSession.wellbeing_score.isnot(None))
        .order_by(CheckInSession.created_at.desc())
    )
    check_ins = ci_result.scalars().all()
    if not check_ins:
        return None
        
    latest_ci = check_ins[0]
    
    # 2. Fetch domain scores
    dom_result = await db.execute(
        select(CheckInDomain).where(CheckInDomain.check_in_id == latest_ci.id)
    )
    domains = dom_result.scalars().all()
    domain_dict = {d.domain: d.score for d in domains}
    
    # 3. Extract Modalities
    modality_contributions = []
    conflict_detected = False
    if latest_ci.answers and isinstance(latest_ci.answers, dict) and "fusion_analysis" in latest_ci.answers:
        fusion = latest_ci.answers["fusion_analysis"]
        modality_contributions = fusion.get("modality_contributions", [])
        conflict_detected = fusion.get("conflict_detected", False)
    else:
        modality_contributions = [
            {"modality_name": "baseline", "is_available": True, "score_normalized": (100 - latest_ci.wellbeing_score) if latest_ci.wellbeing_score else 0, "confidence": 1.0, "effective_weight": 1.0},
            {"modality_name": "nlp", "is_available": False},
            {"modality_name": "speech", "is_available": False}
        ]
        
    # 4. Temporal Analysis
    observations = []
    # Needs a fallback if victim_id/user_id isn't directly on case object, but we have it on latest_ci
    user_id_str = str(latest_ci.user_id) 
    for ci in reversed(check_ins):
        fused_score = 100 - ci.wellbeing_score
        observations.append(
            TemporalObservation(
                timestamp=ci.created_at,
                risk_score=fused_score,
                risk_level=ci.risk_level
            )
        )
        
    temporal_input = TemporalInput(user_id=user_id_str, observations=observations)
    temporal_engine = TemporalRiskEngine()
    temporal_result = temporal_engine.analyze(temporal_input).model_dump()
    
    # 5. Explainability
    explain_input = ExplainabilityInput(
        risk_score=(100 - latest_ci.wellbeing_score) if latest_ci.wellbeing_score else 0,
        risk_level=latest_ci.risk_level or "stable",
        wellbeing_score=latest_ci.wellbeing_score or 100,
        domain_scores=domain_dict,
        modality_contributions=modality_contributions,
        conflict_detected=conflict_detected,
        temporal_result=temporal_result
    )
    
    engine = DeterministicAlertEngine()
    explanation_engine = __import__("ai.explainability.engine").explainability.engine.DeterministicExplainabilityEngine()
    explanation = explanation_engine.generate_explanation(explain_input)
    
    # 6. Evaluate Alert
    service = AlertService(db)
    return await service.evaluate_and_create_alert(case_id, explanation)

def get_alert_service(db: AsyncSession) -> AlertService:
    return AlertService(db)
