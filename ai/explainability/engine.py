from typing import List, Dict, Any, Optional
from ai.explainability.schemas import (
    ExplainabilityInput,
    ExplainabilityResult,
    DomainContribution,
    ModalitySummary,
    TemporalSummary
)

class DeterministicExplainabilityEngine:
    """
    Phase 3F: Explainability Engine.
    Generates deterministic human-readable decision support summaries from Phase 3D and 3E outputs.
    Does NOT calculate risk. Does NOT make clinical claims.
    """
    
    def generate_explanation(self, input_data: ExplainabilityInput) -> ExplainabilityResult:
        # 1. Domain Contributions (Baseline)
        domain_contributions = self._explain_domains(input_data.domain_scores)
        
        # 2. Modality Contributions (Fusion)
        modality_summaries, missing_modalities = self._explain_modalities(input_data.modality_contributions)
        
        # 3. Temporal Summary
        temporal_summary = self._explain_temporal(input_data.temporal_result)
        
        # 4. Reliability / Data Quality
        reliability = self._determine_reliability(input_data, temporal_summary)
        
        # 5. Human-readable Summary
        summary = self._generate_summary(
            risk_level=input_data.risk_level,
            domains=domain_contributions,
            temporal=temporal_summary,
            conflict=input_data.conflict_detected
        )
        
        # 6. Human Review Guidance
        human_review = self._generate_guidance(
            conflict=input_data.conflict_detected,
            missing=missing_modalities,
            temporal=temporal_summary
        )
        
        # Limitations (Fixed text for SIH prototype)
        limitations = (
            "This is an engineering prototype decision-support system, not a clinically validated predictive model. "
            "It does not diagnose mental illness or predict future mental-health outcomes. "
            "Multimodal signals can be noisy (e.g., speech features affected by recording conditions, "
            "NLP sentiment is not equivalent to clinical distress). Counsellor/human review remains necessary."
        )
        
        return ExplainabilityResult(
            summary=summary,
            risk_score=input_data.risk_score,
            risk_level=input_data.risk_level,
            top_contributing_factors=domain_contributions,
            modality_contributions=modality_summaries,
            missing_modalities=missing_modalities,
            conflicting_modalities=input_data.conflict_detected,
            temporal_summary=temporal_summary,
            reliability=reliability,
            human_review_note=human_review,
            limitations=limitations
        )
        
    def _explain_domains(self, domain_scores: Dict[str, int]) -> List[DomainContribution]:
        results = []
        for domain, score in domain_scores.items():
            # Domain scores are 0-10.
            if score >= 7:
                level = "High"
                reason = f"Elevated {domain.replace('_', ' ')} increased the baseline risk signal."
            elif score >= 4:
                level = "Moderate"
                reason = f"Moderate {domain.replace('_', ' ')} contributed slightly to the baseline risk signal."
            else:
                level = "Low"
                reason = f"Low {domain.replace('_', ' ')} did not significantly increase baseline risk."
                
            results.append(DomainContribution(
                domain=domain,
                score=score,
                contribution_level=level,
                reason=reason
            ))
            
        # Sort by score descending to get top contributors first
        results.sort(key=lambda x: x.score, reverse=True)
        return results
        
    def _explain_modalities(self, modality_contributions: List[dict]) -> tuple[List[ModalitySummary], List[str]]:
        summaries = []
        missing = []
        
        for mod in modality_contributions:
            name = mod.get("modality_name", "unknown")
            is_available = mod.get("is_available", False)
            
            if not is_available:
                missing.append(name)
                summaries.append(ModalitySummary(
                    modality=name,
                    availability="Unavailable",
                    contribution="None",
                    reason=f"{name.capitalize()} signal unavailable. Current assessment uses available signals."
                ))
            else:
                weight = mod.get("effective_weight", 0.0)
                if weight >= 0.5:
                    contrib = "Dominant"
                elif weight >= 0.2:
                    contrib = "Moderate"
                else:
                    contrib = "Minor"
                    
                summaries.append(ModalitySummary(
                    modality=name,
                    score=mod.get("score_normalized"),
                    confidence=mod.get("confidence"),
                    weight=weight,
                    availability="Available",
                    contribution=contrib,
                    reason=f"{name.capitalize()} signal contributed to the fused engineering score."
                ))
                
        return summaries, missing
        
    def _explain_temporal(self, temporal_result: Optional[dict]) -> Optional[TemporalSummary]:
        if not temporal_result or not temporal_result.get("available"):
            return None
            
        return TemporalSummary(
            current_risk=temporal_result.get("current_score", 0),
            trend=temporal_result.get("trend", "insufficient_data"),
            slope_per_day=temporal_result.get("slope_per_day"),
            persistence=temporal_result.get("persistence", False),
            recent_change=temporal_result.get("range", 0), # or compute delta
            early_warning_status=temporal_result.get("temporal_status", "no_signal"),
            data_quality=temporal_result.get("data_quality", "insufficient"),
            explanation=temporal_result.get("explanation", "Insufficient longitudinal data.")
        )
        
    def _determine_reliability(self, input_data: ExplainabilityInput, temporal: Optional[TemporalSummary]) -> str:
        # Based on available modalities and temporal data quality
        available_mods = sum(1 for m in input_data.modality_contributions if m.get("is_available", False))
        
        if available_mods >= 3 and temporal and temporal.data_quality in ["adequate", "strong"]:
            return "Strong — multiple recent observations and available multimodal signals support the current engineering assessment."
        elif available_mods >= 2 and temporal and temporal.data_quality != "insufficient":
            return "Adequate — assessment is supported by multiple signal sources and basic longitudinal data."
        else:
            return "Limited — assessment confidence is limited due to missing signal sources or insufficient longitudinal observations."
            
    def _generate_summary(self, risk_level: str, domains: List[DomainContribution], temporal: Optional[TemporalSummary], conflict: bool) -> str:
        top_domains = [d.domain.replace("_", " ") for d in domains if d.score >= 7]
        
        domain_text = ""
        if top_domains:
            domain_text = f", primarily influenced by elevated {', '.join(top_domains[:2])}"
            
        trend_text = ""
        if temporal and temporal.trend != "insufficient_data":
            trend_text = f", with the recent trajectory showing a {temporal.trend} trend"
            
        summary = f"Current engineering risk score is {risk_level}{domain_text}{trend_text}."
        
        if conflict:
            summary += " Available signals show disagreement across modalities."
            
        return summary
        
    def _generate_guidance(self, conflict: bool, missing: List[str], temporal: Optional[TemporalSummary]) -> str:
        guidance = []
        if conflict:
            guidance.append("Review conflicting modality signals carefully.")
        
        if temporal and temporal.trend == "worsening" and temporal.persistence:
            guidance.append("Review recent check-in history as the trajectory is persistently worsening.")
            
        if not guidance:
            guidance.append("Consider contacting the user according to applicable counselling protocol if risk is high.")
            
        return " ".join(guidance)
