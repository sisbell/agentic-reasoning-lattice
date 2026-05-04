"""Convergence-protocol decision helper — accept/reject revise comments.

Files a `resolution` link closing a `comment.revise`. On accept,
files `resolution.edit` (the comment is closed because the prose
was edited). On reject, writes the reviser's rationale to a
rationale doc and files `resolution.reject` referencing both the
comment and the rationale.

Pass 2 of the binding work split this from `lib/backend/emit.py`:
the bundled `emit_decision` there did both the rationale-document
write and the link emission in one call. Now the two operations
are explicit:

    1. session.update_document(rationale_path, body)  — FEBE write
    2. session.make_link(...)                         — substrate link

This is claim-convergence-protocol-specific (resolution.edit /
resolution.reject are the protocol's vocabulary for closing
revise comments) and so lives here, not in lib/backend/.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session


def emit_decision(
    session: Session,
    action: str,
    comment_addr: Address,
    claim_addr: Address,
    asn_label: str,
    rationale: Optional[str] = None,
) -> Link:
    """Emit the resolution link for a reviser's accept/reject decision.

    action: 'accept' or 'reject'
    comment_addr: address of the comment being closed
    claim_addr: address of the doc the resolution applies to
    asn_label: ASN label (for rationale doc placement on reject)
    rationale: required when action == 'reject'

    On accept: emits resolution.edit (F=[claim], G=[comment]).
    On reject: composes two explicit operations:
      1. session.update_document(rationale_path, body) — FEBE write
      2. session.make_link(...)                        — resolution.reject

    The rationale doc lives at
    `_docuverse/documents/rationale/<asn>/<comment_addr>.md`.
    """
    from lib.shared.paths import RATIONALE_DIR

    if action == "accept":
        return session.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr],
            type_="resolution",
            subtype="edit",
        )

    if action == "reject":
        if not rationale:
            raise ValueError("reject requires rationale text")
        # Compute rationale path (lattice-relative for update_document)
        target_dir = Path(RATIONALE_DIR) / asn_label
        rationale_path = target_dir / f"{comment_addr}.md"
        body = rationale + "\n"
        lattice_root = session.store.lattice_dir.resolve()
        rationale_rel = str(rationale_path.resolve().relative_to(lattice_root))

        # 1. Document write (FEBE)
        session.update_document(rationale_rel, body)

        # 2. Substrate link emission
        rationale_addr = session.register_path(rationale_rel)
        return session.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr, rationale_addr],
            type_="resolution",
            subtype="reject",
        )

    raise ValueError(f"unknown action: {action!r}")
