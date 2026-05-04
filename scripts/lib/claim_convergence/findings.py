"""Claim-convergence finding recording — review meta doc + per-finding docs.

Two helpers:

- `emit_meta(session, ...)` — writes the aggregate review document
  (<reviews_dir>/<asn>/review-N.md) and emits the `review` classifier
  on it.
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
from lib.backend.links import Link
from lib.lattice.findings import record_one_finding
from lib.protocols.febe.protocol import Session


def emit_meta(
    session: Session,
    asn_label: str,
    review_num: int,
    *,
    title: str,
    timestamp: str,
    scope: str,
    verdict: str,
    findings_summary: str,
    emitted_findings: list,
    elapsed_seconds: float,
    reviews_dir,
    covered_addrs: list[Address] | None = None,
) -> Link:
    """Write the aggregate review doc and emit the `review` classifier.

    Path: <reviews_dir>/<asn_label>/review-<N>.md.

    The aggregate is the reviewer's full output; per-finding bodies
    live separately (written by record_findings).

    `covered_addrs`, when provided, records via `review.coverage`
    links which docs were within this review's coverage (the
    structural audit fact). The `is_claim_confirmed` predicate
    consults these links to find the most recent review covering a
    given doc; coverage / staleness predicates will use them too.
    Omit when scope is not relevant (legacy callers).
    """
    from lib.backend.emit import emit_review_coverage

    reviews_root = Path(reviews_dir)
    review_stem = f"review-{review_num}"
    asn_dir = reviews_root / asn_label
    meta_path = asn_dir / f"{review_stem}.md"

    lines = [
        f"# {title}",
        "",
        f"*{timestamp}*",
        "",
        f"**Scope:** {scope}",
        f"**Verdict:** {verdict}",
        f"**Findings:** {findings_summary}",
        f"**Elapsed:** {elapsed_seconds:.0f}s",
    ]
    if emitted_findings:
        lines.extend(["", "## Findings", ""])
        for ef in emitted_findings:
            finding_filename = Path(ef["finding_path"]).name
            cls = ef.get("cls", "REVISE")
            title_text = ef.get("title", "(untitled)")
            lines.append(f"- {finding_filename} — {title_text} *({cls})*")
    body = "\n".join(lines) + "\n"

    lattice_root = session.store.lattice_dir.resolve()
    meta_rel = str(meta_path.resolve().relative_to(lattice_root))

    session.update_document(meta_rel, body)
    meta_addr = session.register_path(meta_rel)
    link, _ = emit_review(session.store, meta_addr)

    if covered_addrs:
        for covered in covered_addrs:
            emit_review_coverage(session.store, meta_addr, covered)

    return link


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
