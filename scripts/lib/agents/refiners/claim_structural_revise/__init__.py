"""Claim structural-revise agent — refiner for structural-violation findings.

Public surface:
- ClaimStructuralReviseAgent — Agent class fired by the claim-structural-revise
  trigger. One fire = one claim's structural quiescence work; reads unresolved
  comment.violation findings emitted by the structural-audit scout, applies
  per-rule fixes, emits resolution.<kind> per closed comment.
- fix_structural_rule — LLM-call helper used by the agent.
"""

from .agent import ClaimStructuralReviseAgent
from .helpers import StructuralRuleFixResult, fix_structural_rule

__all__ = [
    "ClaimStructuralReviseAgent",
    "StructuralRuleFixResult",
    "fix_structural_rule",
]
