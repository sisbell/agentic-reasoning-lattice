"""Note-convergence finding helper — per-finding doc materialization.

Pass 2 split this from `lib/backend/emit.py` where it bundled
filesystem writes with substrate link emissions. Now the document
write and the link emission are visibly separate calls.

For each finding (title, cls, body):
  1. session.update_document(<findings_dir>/<asn>/<review_stem>/<n>.md)
  2. emit_finding classifier on the per-finding doc
  3. emit comment.{revise|out-of-scope} from finding doc to note
  4. emit provenance.derivation from aggregate review to finding

Atomicity story: operations are not transactional; partial failure
recoverable via reconciliation. See
docs/hypergraph-protocol/error-handling.md.
"""

from __future__ import annotations

from pathlib import Path

from lib.backend.addressing import Address
from lib.backend.emit import emit_comment, emit_derivation, emit_finding
from lib.febe.protocol import Session


def emit_note_findings(
    session: Session,
    note_addr: Address,
    aggregate_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    findings_dir,
):
    """Materialize each note-review finding as a doc and emit substrate
    facts.

    `findings` is a list of (title, cls, body). For each:
      1. session.update_document(<findings_dir>/<asn>/<review_stem>/<n>.md)
      2. emit_finding classifier on the per-finding doc
      3. emit comment.{revise|out-of-scope} from finding doc to note
      4. emit provenance.derivation from aggregate review to finding

    Returns list of {title, cls, comment_id, note_path, finding_path}.
    """
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    lattice_root = session.store.lattice_dir.resolve()

    note_rel = session.get_path_for_addr(note_addr)
    results = []
    for n, (title, cls, body) in enumerate(findings):
        finding_path = out_dir / f"{n}.md"
        finding_rel = str(finding_path.resolve().relative_to(lattice_root))

        # 1. Document write
        session.update_document(finding_rel, body)

        # 2. Substrate facts
        finding_addr = session.register_path(finding_rel)
        emit_finding(session.store, finding_addr)

        cls_normalized = (cls or "REVISE").upper()
        if cls_normalized == "OUT_OF_SCOPE":
            comment_kind = "out-of-scope"
        else:
            comment_kind = "revise"

        comment = emit_comment(
            session.store, finding_addr, note_addr, kind=comment_kind,
        )

        emit_derivation(session.store, aggregate_addr, finding_addr)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment.addr,
            "note_path": note_rel,
            "finding_path": finding_rel,
        })

    return results
