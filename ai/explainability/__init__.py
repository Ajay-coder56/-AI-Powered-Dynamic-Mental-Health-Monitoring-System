"""
AI / Explainability Module — Model explanation and interpretability.

Phase: 3F (NOT YET IMPLEMENTED)

This module will provide SHAP/LIME-style explanations for AI model outputs,
enabling counsellors to understand why a particular risk score was assigned.
It will implement the ExplainabilityEngine interface defined in
app.risk_engine.interface.

Planned capabilities (Phase 3F):
- SHAP-based feature importance
- LIME-based local explanations
- Counterfactual explanations
- Domain contribution visualization data
- Natural language explanation generation

IMPORTANT: This module is a boundary placeholder only.
No AI models, no fake outputs, no production wiring.
The current deterministic baseline already provides its own
rule-based explanations via app.risk_engine.baseline.
"""

NOT_IMPLEMENTED = True
PHASE = "3F"
ENGINE_INTERFACE = "ExplainabilityEngine"
