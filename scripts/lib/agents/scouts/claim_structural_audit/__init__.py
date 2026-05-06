"""Claim structural-audit scout — emits validator findings to substrate.

The first scout-caste agent in the system. Detects structural
violations (via the claim-validate.py validator) and emits per-finding
substrate so the structural-fix refiner can close them via existing
resolution machinery.
"""

from .agent import ClaimStructuralAuditAgent

__all__ = ["ClaimStructuralAuditAgent"]
