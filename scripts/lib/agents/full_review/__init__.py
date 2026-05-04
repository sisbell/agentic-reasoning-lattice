"""Full-review agent package.

Public surface:
- FullReviewAgent — Agent class fired by the full-review trigger.
  One cycle per fire; the runner handles convergence re-firing.
- run_full_review — legacy multi-cycle wrapper. Used by the
  `claim-full-review.py` CLI for direct invocation.
"""

from __future__ import annotations

import sys

from lib.predicates import is_asn_confirmed
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE

from .agent import FULL_MODEL, FullReviewAgent


__all__ = [
    "FULL_MODEL",
    "FullReviewAgent",
    "run_full_review",
]


def run_full_review(
    asn_num, *, max_cycles: int = 8, model: str = FULL_MODEL,
) -> str:
    """Legacy multi-cycle wrapper: drive FullReviewAgent until confirmed
    or max_cycles hit. Returns "converged" / "not_converged" / "failed".

    Used by the manual CLI entry point. Mirrors run_cone_review's
    structure: each cycle re-opens the session so the agent's
    substrate writes become visible.

    No `dry_run`: undo via `git reset --hard HEAD~N`.
    """
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [run_full_review] ASN-{asn_num:04d} not found",
              file=sys.stderr)
        return "failed"

    agent = FullReviewAgent()
    session = open_session(LATTICE)

    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        print(f"  [run_full_review] note not in substrate: {note_rel}",
              file=sys.stderr)
        return "failed"

    for _ in range(max_cycles):
        if is_asn_confirmed(session, note_addr):
            return "converged"
        result = agent(session, note_addr)
        if not result.success and result.detail.startswith("gate-failed"):
            return "failed"
        # Re-open so agent's substrate writes are visible.
        session = open_session(LATTICE)
        note_addr = (
            session.store.path_to_addr.get(
                session.get_path_for_addr(note_addr) or "",
                note_addr,
            )
        )

    if is_asn_confirmed(session, note_addr):
        return "converged"
    return "not_converged"
