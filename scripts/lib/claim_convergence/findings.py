"""Claim-convergence finding recording — review doc + per-finding docs.

Two helpers:

- `emit_review_doc(session, ...)` — writes the LLM's review output
  verbatim to the docuverse review path and emits the `review`
  classifier + `review.coverage` links on it.
- `record_findings(session, ...)` — for each finding, parses the
  target claim from the body, then delegates the doc-write + substrate
  emissions to record_one_finding.

Atomicity story: see lib/lattice/findings.py.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from lib.backend.addressing import Address
from lib.backend.emit import emit_review
from lib.lattice.findings import record_one_finding
from lib.protocols.febe.protocol import Session
from lib.shared.paths import review_aggregate_path


def emit_review_doc(
    session: Session,
    asn_label: str,
    review_num: int,
    *,
    body: str,
    covered_addrs: list[Address] | None = None,
) -> tuple[Address, Path]:
    """Persist the LLM's review output as a substrate-citizen document.

    The body is the reviewer's full output verbatim — narrative,
    findings, verdict. Per-finding bodies are also extracted to their
    own docs by record_findings (so revise gets clean per-finding
    input); this document is the audit trail.

    `covered_addrs`, when provided, records via `review.coverage`
    links which docs were within this review's coverage. The
    `is_claim_confirmed` predicate consults these links to find the
    most recent review covering a given doc.

    Returns `(review_addr, review_path)`.
    """
    from lib.backend.emit import emit_review_coverage

    review_path = review_aggregate_path(asn_label, review_num, kind="claim")
    lattice_root = session.store.lattice_dir.resolve()
    review_rel = str(review_path.resolve().relative_to(lattice_root))

    session.update_document(review_rel, body)
    review_addr = session.register_path(review_rel)
    emit_review(session.store, review_addr)

    if covered_addrs:
        for covered in covered_addrs:
            emit_review_coverage(session.store, review_addr, covered)

    return review_addr, review_path


def record_findings(
    session: Session,
    review_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    label_index: dict,
    findings_dir,
):
    """Materialize per-finding docs and emit their substrate facts.

    `findings` is a list of (title, cls, body). For each finding, parses
    the target claim label out of the body (`**ASN**: <label>` or
    `**Foundation**: <label>`), maps cls (REVISE | OBSERVE) to a
    comment kind, and delegates to record_one_finding.

    label_index: {label_string: claim_doc_addr}.
    """
    out_dir = Path(findings_dir) / asn_label / review_stem
    lattice_root = session.store.lattice_dir.resolve()

    results = []
    for n, (title, cls, body) in enumerate(findings):
        target_label = _extract_target_label(body, label_index)
        if target_label is None:
            import sys as _sys
            print(
                f"  [emit] skipping finding {n} '{title}' — "
                f"no parseable target label",
                file=_sys.stderr,
            )
            continue
        claim_addr = label_index[target_label]

        finding_rel = str(
            (out_dir / f"{n}.md").resolve().relative_to(lattice_root)
        )

        cls_normalized = cls.upper() if cls else "REVISE"
        if cls_normalized not in {"REVISE", "OBSERVE"}:
            cls_normalized = "REVISE"

        _, comment = record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=body,
            target_addr=claim_addr,
            review_addr=review_addr,
            comment_kind=cls_normalized.lower(),
        )

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment.addr,
            "claim_path": session.get_path_for_addr(claim_addr),
            "finding_path": finding_rel,
        })

    return results


def _extract_target_label(body: str, label_index: dict) -> Optional[str]:
    """Parse a finding body for an ASN/Foundation label that resolves
    in label_index. Returns the label string or None.
    """
    for header in ("ASN", "Foundation"):
        m = re.search(
            rf"\*\*{header}\*\*\s*[:\-]\s*([A-Za-z0-9_./\\-]+)",
            body,
        )
        if m:
            label = m.group(1).strip()
            if label in label_index:
                return label
    return None
