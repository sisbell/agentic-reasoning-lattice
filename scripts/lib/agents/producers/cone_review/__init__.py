"""Cone-review agent package.

Public surface:
- ConeReviewAgent — Agent class fired by the cone-review trigger.
  One cycle per fire; the runner handles the multi-cycle refinement.
- run_cone_review — legacy multi-cycle wrapper. Now a thin adapter
  over the runner: drives `cone_review` and `claim_revise` triggers
  until quiescence. Kept for the manual CLI entry point
  (`scripts/claim-full-review.py --cone <label>`).
"""

from __future__ import annotations

import sys

from .agent import CONE_MODEL, ConeReviewAgent
from .scope import assemble_cone, transitive_same_asn_deps
from .sync import sync_claim_citations


__all__ = [
    "ConeReviewAgent",
    "assemble_cone",
    "run_cone_review",
    "sync_claim_citations",
    "transitive_same_asn_deps",
]


def run_cone_review(
    asn_num, apex_label, dep_labels, *,
    max_cycles: int = 8, model: str = CONE_MODEL,
) -> str:
    """Legacy multi-cycle wrapper: drive cone_review + claim_revise
    triggers until quiescence. Returns "quiescent" / "not_quiescent" /
    "failed".

    Wraps the runner-driven path — the previous internal cycle loop
    inside this wrapper retired when claim_revise was lifted to a
    predicate-fired Agent class. The runner walks both triggers until
    every comment.revise on the apex is closed and the apex's review
    coverage is current.

    `apex_label` and `dep_labels` are not used in the new shape; the
    runner derives the cone from substrate (transitive deps walked
    inside ConeReviewAgent.run()). Kept in the signature for
    backwards compatibility with callers.
    """
    from lib.runner import Scope, run_force_pass
    from lib.triggers import claim_revise, cone_review

    scope = Scope(
        asn_label=f"ASN-{asn_num:04d}",
        labels=frozenset({apex_label}),
    )
    result = run_force_pass(
        triggers=[cone_review, claim_revise], scope=scope,
    )
    if result.errors:
        return "failed"
    return "quiescent" if result.quiescent else "not_quiescent"
