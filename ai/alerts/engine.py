from ai.alerts.schemas import AlertEngineResult, AlertPriority, AlertType
from ai.explainability.schemas import ExplainabilityResult

class DeterministicAlertEngine:
    """
    Phase 4: Alert, Triage & Human-in-the-loop Engine.
    Evaluates explainability/risk outputs and deterministically generates alerts.
    Does NOT calculate risk. Does NOT make clinical claims.
    """
    
    def evaluate(self, explainability: ExplainabilityResult) -> AlertEngineResult:
        # Check conditions in order of severity (highest first)
        
        # RULE A: Critical engineering risk
        if explainability.risk_score >= 75:
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.CRITICAL,
                alert_type=AlertType.RISK_THRESHOLD,
                title="Critical Engineering Risk Detected",
                reason=f"Engineering risk score is {explainability.risk_score} (critical). Immediate counsellor review is recommended according to applicable organizational protocol.",
                recommended_actions=["Review the recent check-in history", "Contact the user according to protocol"]
            )
            
        # RULE B: High engineering risk
        if 49 <= explainability.risk_score <= 74:
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.HIGH,
                alert_type=AlertType.RISK_THRESHOLD,
                title="High Engineering Risk Detected",
                reason=f"Engineering risk score is {explainability.risk_score} (high).",
                recommended_actions=["Review the contributing factors", "Monitor for further worsening"]
            )
            
        # RULE E: Persistent worsening
        if explainability.temporal_summary and explainability.temporal_summary.trend == "worsening" and explainability.temporal_summary.persistence:
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.HIGH,
                alert_type=AlertType.PERSISTENT_WORSENING,
                title="Persistent Worsening Trajectory",
                reason="Risk remains elevated across consecutive recent observations, indicating a persistent worsening pattern that warrants counsellor review.",
                recommended_actions=["Review longitudinal trajectory", "Check if external events correlate with decline"]
            )
            
        # RULE C & D: Worsening trajectory / Strong warning
        if explainability.temporal_summary and explainability.temporal_summary.trend == "worsening":
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.MEDIUM,
                alert_type=AlertType.WORSENING_TRAJECTORY,
                title="Worsening Trend Detected",
                reason="Recent trajectory shows a worsening trend in the engineering signal.",
                recommended_actions=["Review temporal timeline"]
            )
            
        # RULE F: Conflicting signals
        if explainability.conflicting_modalities:
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.MEDIUM,
                alert_type=AlertType.SIGNAL_CONFLICT,
                title="Conflicting Signals Review Required",
                reason="Modalities conflict significantly. Human interpretation is needed.",
                recommended_actions=["Review conflicting modality signals carefully"]
            )
            
        # RULE G: Insufficient data
        if "Limited" in explainability.reliability or "Insufficient" in explainability.reliability:
            return AlertEngineResult(
                should_alert=True,
                priority=AlertPriority.LOW,
                alert_type=AlertType.INSUFFICIENT_DATA,
                title="Insufficient Data Quality",
                reason="Data quality is insufficient to form a confident assessment.",
                recommended_actions=["Encourage user to complete more assessments"]
            )
            
        return AlertEngineResult(should_alert=False)
