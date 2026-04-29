"""Library: emit a resolution.edit or resolution.reject link.

Called from `scripts/convergence-resolution.py` (the agent-callable CLI). Separated from
the CLI so tests exercise the logic directly without subprocess overhead.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import RATIONALE_DIR, LATTICE


def emit_decision(store, action, comment_id, claim_path, asn_label,
                  rationale=None, rationale_dir=None, lattice=None):
    """Emit the resolution link for the reviser's decision.

    action: 'accept' or 'reject'
    comment_id: link id of the comment being closed
    claim_path: lattice-relative md path of the claim
    asn_label: ASN label (for rationale doc placement)
    rationale: required if action == 'reject'
    rationale_dir, lattice: testing overrides

    Returns the new resolution link id.
    Raises KeyError if comment_id doesn't exist; ValueError on bad action
    or missing rationale on reject.
    """
    if store.get(comment_id) is None:
        raise KeyError(f"comment id {comment_id} not in store")

    if action == "accept":
        return store.make_link(
            from_set=[claim_path],
            to_set=[comment_id],
            type_set=["resolution.edit"],
        )

    if action == "reject":
        if not rationale:
            raise ValueError("reject requires rationale text")
        rdir = Path(rationale_dir) if rationale_dir else Path(RATIONALE_DIR)
        lat = Path(lattice) if lattice else Path(LATTICE)
        target_dir = rdir / asn_label
        target_dir.mkdir(parents=True, exist_ok=True)
        rationale_path = target_dir / f"{comment_id}.md"
        rationale_path.write_text(rationale + "\n")
        rationale_rel = str(rationale_path.resolve().relative_to(lat.resolve()))
        return store.make_link(
            from_set=[],
            to_set=[comment_id, rationale_rel],
            type_set=["resolution.reject"],
        )

    raise ValueError(f"unknown action: {action!r}")
