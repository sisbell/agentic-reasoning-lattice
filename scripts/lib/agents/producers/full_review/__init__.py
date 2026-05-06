"""Full-review agent package.

Public surface:
- FullReviewAgent — Agent class fired by the full-review trigger.
  One cycle per fire; the runner handles refinement re-firing.
- run_full_review — legacy multi-cycle wrapper. Now a thin adapter
  over the runner: drives `full_review` and `claim_revise` triggers
  until quiescence. Used by `scripts/claim-full-review.py`.
"""

from __future__ import annotations

from .agent import FULL_MODEL, FullReviewAgent


__all__ = [
    "FULL_MODEL",
    "FullReviewAgent",
    "run_full_review",
]


def run_full_review(asn_num, *, max_cycles: int = 8) -> str:
    """Legacy multi-cycle wrapper: drive full_review + claim_revise
    triggers until quiescence. Returns "quiescent" / "not_quiescent" /
    "failed".

    Wraps the runner-driven path — the previous internal cycle loop
    inside this wrapper retired when claim_revise was lifted to a
    predicate-fired Agent class. The runner walks both triggers until
    every comment.revise on the ASN's claims is closed and the
    ASN's review coverage is current.
    """
    from lib.runner import asn, run_until_quiescent
    from lib.triggers import claim_findings, claim_revise, full_review

    result = run_until_quiescent(
        triggers=[full_review, claim_findings, claim_revise],
        scope=asn(asn_num),
        max_iterations=max_cycles,
    )
    if result.errors:
        return "failed"
    return "quiescent" if result.quiescent else "not_quiescent"
