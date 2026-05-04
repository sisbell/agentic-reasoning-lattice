"""Cone-review agent package.

Public surface:
- ConeReviewAgent — Agent class fired by the cone-review trigger.
  One cycle per fire; the runner handles the multi-cycle convergence.
- run_cone_review — legacy multi-cycle wrapper. Kept while
  full-review (which has not migrated to triggers yet) still calls
  it. New code should use the trigger / agent directly.
"""

from __future__ import annotations

import sys

from lib.protocols.febe.session import open_session
from lib.predicates import is_claim_confirmed
from lib.shared.paths import LATTICE

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
    """Legacy multi-cycle wrapper: drive ConeReviewAgent until confirmed
    or max_cycles hit. Returns "converged" / "not_converged" / "failed".

    Used by full-review's cone-fallback dispatch. Once full-review
    migrates to the trigger model, this wrapper retires.

    No `dry_run`: undo via `git reset --hard HEAD~N`. Faux-dry semantics
    leak side effects (raw output files, session re-opens, partial
    substrate writes); the git reset path is honest about cost and
    captures every artifact we care about.
    """
    agent = ConeReviewAgent()
    session = open_session(LATTICE)

    from lib.lattice.labels import build_cross_asn_label_index
    label_index = build_cross_asn_label_index(session.store)
    apex_addr = label_index.get(apex_label)
    if apex_addr is None:
        print(
            f"  [run_cone_review] no addr for {apex_label}",
            file=sys.stderr,
        )
        return "failed"

    for cycle in range(max_cycles):
        if is_claim_confirmed(session, apex_addr):
            return "converged"
        result = agent(session, apex_addr)
        if not result.success and result.detail.startswith("gate-failed"):
            return "failed"
        # Re-open session: the agent's substrate writes are now visible.
        session = open_session(LATTICE)
        apex_addr = (
            session.store.path_to_addr.get(
                session.get_path_for_addr(apex_addr) or "",
                apex_addr,
            )
        )

    if is_claim_confirmed(session, apex_addr):
        return "converged"
    return "not_converged"
