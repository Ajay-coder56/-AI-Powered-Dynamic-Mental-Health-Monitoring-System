from typing import Dict, List
from ai.distress.schemas import FusionInput, FusionResult, ModalityContribution
from ai.distress.config import config

class MultimodalFusionEngine:
    """
    Multimodal Risk Fusion Engine.
    Combines Baseline, NLP, and Speech signals into a unified RiskResult.
    """

    def __init__(self):
        self.weights = {
            "baseline": config.BASELINE_WEIGHT,
            "nlp": config.NLP_WEIGHT,
            "speech": config.SPEECH_WEIGHT,
        }
        self.conflict_threshold = config.CONFLICT_THRESHOLD

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        modalities = {}
        
        # 1. Gather Available Modalities
        modalities["baseline"] = {
            "score": fusion_input.baseline_score,
            "confidence": fusion_input.baseline_confidence,
            "available": True
        }
        
        modalities["nlp"] = {
            "score": fusion_input.nlp_signal if fusion_input.nlp_available else 0.0,
            "confidence": fusion_input.nlp_confidence if fusion_input.nlp_available and fusion_input.nlp_confidence is not None else 0.0,
            "available": fusion_input.nlp_available
        }
        
        modalities["speech"] = {
            "score": fusion_input.speech_signal if fusion_input.speech_available else 0.0,
            "confidence": fusion_input.speech_confidence if fusion_input.speech_available and fusion_input.speech_confidence is not None else 0.0,
            "available": fusion_input.speech_available
        }

        # 2. Calculate Effective Weights
        effective_weights = {}
        for mod, data in modalities.items():
            if data["available"]:
                effective_weights[mod] = self.weights[mod] * data["confidence"]
            else:
                effective_weights[mod] = 0.0

        total_effective_weight = sum(effective_weights.values())

        if total_effective_weight == 0:
            # Failsafe: if everything fails or has 0 confidence, strictly use baseline score.
            fused_score = fusion_input.baseline_score
            overall_confidence = 0.0
            normalized_weights = {"baseline": 1.0, "nlp": 0.0, "speech": 0.0}
        else:
            normalized_weights = {k: v / total_effective_weight for k, v in effective_weights.items()}
            
            fused_score = 0.0
            overall_confidence = 0.0
            
            for mod, data in modalities.items():
                if data["available"]:
                    fused_score += data["score"] * normalized_weights[mod]
                    overall_confidence += data["confidence"] * normalized_weights[mod]
                    
        # Clamp score
        fused_score = max(0.0, min(100.0, fused_score))
        
        # 3. Detect Conflict
        active_scores = [data["score"] for data in modalities.values() if data["available"]]
        conflict_detected = False
        if len(active_scores) > 1:
            conflict_detected = (max(active_scores) - min(active_scores)) > self.conflict_threshold
            
        # 4. Construct Contributions
        modality_contributions = {}
        for mod, data in modalities.items():
            modality_contributions[mod] = ModalityContribution(
                score=data["score"],
                weight=normalized_weights[mod],
                contribution=data["score"] * normalized_weights[mod],
                confidence=data["confidence"],
                available=data["available"]
            )
            
        modalities_used = [k for k, v in modalities.items() if v["available"]]
        modalities_missing = [k for k, v in modalities.items() if not v["available"]]
        
        # 5. Explainability
        if len(modalities_used) == 1 and "baseline" in modalities_used:
            explanation = (
                "Risk estimate is based on the questionnaire responses. "
                "Optional text and voice signals were unavailable."
            )
        elif conflict_detected:
            explanation = (
                "Questionnaire and optional behavioral signals show meaningful "
                "disagreement. The combined score should be interpreted cautiously."
            )
        else:
            explanation = (
                "Risk estimate is primarily based on the questionnaire responses, "
                "with additional contextual signals from "
            )
            additional_signals = []
            if modalities["nlp"]["available"]:
                additional_signals.append("text sentiment")
            if modalities["speech"]["available"]:
                additional_signals.append("voice acoustic features")
                
            explanation += " and ".join(additional_signals) + "."
            
        return FusionResult(
            fused_risk_score=int(round(fused_score)),
            confidence=overall_confidence,
            modality_contributions=modality_contributions,
            modalities_used=modalities_used,
            modalities_missing=modalities_missing,
            conflict_detected=conflict_detected,
            explanation=explanation
        )
