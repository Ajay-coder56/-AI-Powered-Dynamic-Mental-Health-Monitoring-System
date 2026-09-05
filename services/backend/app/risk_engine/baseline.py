"""
Deterministic Baseline Risk Engine — wraps the verified Phase 2 risk calculator.

This engine implements the exact same algorithm as the original risk_calculator.py:
- Domains: mood, sleep, safety, social_support, legal_anxiety (each 0-10)
- Raw score: sum of all domain scores (max 50)
- Risk score: normalized to 0-100 (higher = more risk)
- Wellbeing score: inverted, normalized to 0-100 (higher = better)
- Thresholds: 0-12 stable, 13-24 moderate, 25-37 high, 38-50 critical
- Contributing factors: domains scoring >= 7

DISCLAIMER:
This is a deterministic engineering baseline. It is NOT a clinically validated
assessment, diagnosis, or prediction tool. No clinical validation has been
performed. AI outputs must not be treated as autonomous clinical decisions.
Counsellor/human review remains necessary.
"""

from datetime import datetime
from typing import List, Tuple

from app.risk_engine.interface import RiskEngine
from app.risk_engine.schemas import (
    DomainContribution,
    ExplanationType,
    RiskExplanation,
    RiskInput,
    RiskLevel,
    RiskResult,
)

# ======================================================================
# Constants — identical to the original risk_calculator.py
# ======================================================================

CONTRIBUTING_FACTOR_THRESHOLD = 7

DOMAIN_LABELS = {
    "mood": "low mood / emotional distress",
    "sleep": "sleep difficulty",
    "safety": "safety concern",
    "social_support": "social withdrawal / low support",
    "legal_anxiety": "legal anxiety",
}

RISK_THRESHOLDS: List[Tuple[int, str]] = [
    (12, "stable"),
    (24, "moderate"),
    (37, "high"),
    (50, "critical"),
]


class DeterministicBaselineEngine(RiskEngine):
    """
    Deterministic baseline risk engine.

    Implements the exact same algorithm as the Phase 2 risk_calculator.py.
    This is the default and currently active engine.

    Engine ID: deterministic_baseline@1.0
    """

    @property
    def engine_name(self) -> str:
        return "deterministic_baseline"

    @property
    def engine_version(self) -> str:
        return "1.0"

    def evaluate(self, risk_input: RiskInput) -> RiskResult:
        """
        Evaluate risk using the deterministic baseline algorithm.

        The calculation is identical to the original calculate_risk() function:
        1. Sum all domain scores -> raw_score
        2. Normalize to 0-100 -> risk_score, wellbeing_score
        3. Map raw_score to risk_level via thresholds
        4. Identify contributing factors (domains >= 7)
        5. Generate deterministic explanation
        """
        domain_scores = risk_input.domain_scores

        # --- Core calculation (identical to risk_calculator.py) ---

        raw_score = sum(domain_scores.values())
        max_possible = len(domain_scores) * 10

        if max_possible > 0:
            wellbeing_score = round(((max_possible - raw_score) / max_possible) * 100)
            risk_score = round((raw_score / max_possible) * 100)
        else:
            wellbeing_score = 100
            risk_score = 0

        # Clamp
        wellbeing_score = max(0, min(100, wellbeing_score))
        risk_score = max(0, min(100, risk_score))

        # Determine risk level from raw_score
        risk_level_str = "critical"  # default if above all thresholds
        for threshold, level in RISK_THRESHOLDS:
            if raw_score <= threshold:
                risk_level_str = level
                break

        # Identify contributing factors (sorted by score descending, same as original)
        contributing_factors: List[str] = []
        for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
            if score >= CONTRIBUTING_FACTOR_THRESHOLD:
                label = DOMAIN_LABELS.get(domain, domain)
                contributing_factors.append(label)

        # --- Explanation generation ---

        domain_contributions = self._build_domain_contributions(domain_scores)
        explanation = self._build_explanation(
            domain_contributions=domain_contributions,
            risk_level_str=risk_level_str,
            contributing_factors=contributing_factors,
        )

        # --- Assemble result ---

        return RiskResult(
            risk_score=risk_score,
            wellbeing_score=wellbeing_score,
            raw_score=raw_score,
            risk_level=RiskLevel(risk_level_str),
            contributing_factors=contributing_factors,
            engine_name=self.engine_name,
            engine_version=self.engine_version,
            confidence=None,  # Deterministic — no probabilistic confidence
            component_scores={domain: score for domain, score in domain_scores.items()},
            explanation=explanation,
            timestamp=risk_input.timestamp or datetime.utcnow(),
        )

    def _build_domain_contributions(
        self, domain_scores: dict[str, int]
    ) -> List[DomainContribution]:
        """Build per-domain contribution details for the explanation."""
        contributions = []
        for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
            label = DOMAIN_LABELS.get(domain, domain)
            is_contributing = score >= CONTRIBUTING_FACTOR_THRESHOLD

            if is_contributing:
                detail = (
                    f"{label.capitalize()} scored {score}/10, which is at or above "
                    f"the contributing-factor threshold of {CONTRIBUTING_FACTOR_THRESHOLD}."
                )
            else:
                detail = f"{label.capitalize()} scored {score}/10."

            contributions.append(
                DomainContribution(
                    domain=domain,
                    score=score,
                    max_score=10,
                    label=label,
                    is_contributing_factor=is_contributing,
                    detail=detail,
                )
            )
        return contributions

    def _build_explanation(
        self,
        domain_contributions: List[DomainContribution],
        risk_level_str: str,
        contributing_factors: List[str],
    ) -> RiskExplanation:
        """Build a deterministic, factual explanation from the input data."""
        if contributing_factors:
            factors_text = ", ".join(contributing_factors)
            summary = (
                f"Deterministic baseline assessment: risk level is '{risk_level_str}'. "
                f"Contributing factors: {factors_text}. "
                f"This is an engineering baseline, not a clinical assessment."
            )
        else:
            summary = (
                f"Deterministic baseline assessment: risk level is '{risk_level_str}'. "
                f"No individual domain reached the contributing-factor threshold "
                f"of {CONTRIBUTING_FACTOR_THRESHOLD}/10. "
                f"This is an engineering baseline, not a clinical assessment."
            )

        return RiskExplanation(
            summary=summary,
            domain_contributions=domain_contributions,
            explanation_type=ExplanationType.deterministic_baseline,
            model_confidence=None,
        )
