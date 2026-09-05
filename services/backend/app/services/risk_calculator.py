"""
Deterministic baseline risk calculator for mental health check-in assessments.

IMPORTANT DISCLAIMER:
This module provides a deterministic engineering/demo baseline risk calculation.
It is NOT a clinically validated assessment, diagnosis, or prediction tool.
It is designed to be easily replaceable with a future AI/ML model.

Algorithm:
- Accepts domain scores (0-10) across 5 domains: mood, sleep, safety, social_support, legal_anxiety
- Computes a raw_score (sum of all domain scores, higher = more distress)
- Derives a wellbeing_score (inverted, 0-100, higher = better)
- Maps to a risk_level using the PostgreSQL risk_level_enum: stable, moderate, high, critical
- Identifies contributing factors (domains scoring >= 7)

Domain score semantics (0-10):
  0 = no distress in this domain
  10 = maximum distress in this domain

Risk thresholds (on raw_score, max 50 with 5 domains):
  0-12:  stable   (wellbeing 76-100)
  13-24: moderate (wellbeing 52-75)
  25-37: high     (wellbeing 26-51)
  38-50: critical (wellbeing 0-25)
"""

from typing import List, Tuple

# Domain distress threshold for contributing factor identification
CONTRIBUTING_FACTOR_THRESHOLD = 7

# Human-readable domain labels
DOMAIN_LABELS = {
    "mood": "low mood / emotional distress",
    "sleep": "sleep difficulty",
    "safety": "safety concern",
    "social_support": "social withdrawal / low support",
    "legal_anxiety": "legal anxiety",
}

# Risk thresholds based on raw_score (sum of domain scores, max 50)
RISK_THRESHOLDS = [
    (12, "stable"),
    (24, "moderate"),
    (37, "high"),
    (50, "critical"),
]


def calculate_risk(domain_scores: dict[str, int]) -> dict:
    """
    Calculate deterministic risk from domain scores.

    Args:
        domain_scores: dict mapping domain name -> score (0-10).
                       e.g. {"mood": 6, "sleep": 8, "safety": 3, ...}

    Returns:
        dict with keys:
            raw_score: int (sum of domain scores)
            wellbeing_score: int (0-100, higher = better)
            risk_score: int (0-100, higher = more risk)
            risk_level: str (stable/moderate/high/critical)
            contributing_factors: list[str]
    """
    # Compute raw score (sum of distress, higher = worse)
    raw_score = sum(domain_scores.values())
    max_possible = len(domain_scores) * 10

    # Wellbeing score: invert so higher = better, normalize to 0-100
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
    risk_level = "critical"  # default if above all thresholds
    for threshold, level in RISK_THRESHOLDS:
        if raw_score <= threshold:
            risk_level = level
            break

    # Identify contributing factors
    contributing_factors = []
    for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
        if score >= CONTRIBUTING_FACTOR_THRESHOLD:
            label = DOMAIN_LABELS.get(domain, domain)
            contributing_factors.append(label)

    return {
        "raw_score": raw_score,
        "wellbeing_score": wellbeing_score,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "contributing_factors": contributing_factors,
    }
