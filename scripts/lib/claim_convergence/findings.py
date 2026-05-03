"""Claim-convergence finding helpers — review meta doc + per-finding docs.

Pass 2 split these from `lib/backend/emit.py` where they bundled
filesystem writes with substrate link emissions. Now the document
write and the link emission are visibly separate calls.

Two helpers:

- `emit_meta(session, ...)` — writes the aggregate review document
  (<reviews_dir>/<asn>/review-N.md) and emits the `review`
  classifier on it.
- `emit_findings(session, ...)` — for each finding, writes a per-
  finding document and emits the substrate facts (finding
  classifier, comment.{revise|observe} link, provenance.derivation).

Both follow the Pass 2 pattern:
  1. session.update_document(path, body)  — FEBE doc write
  2. session.make_link(...) / emit_*(...) — substrate link

Atomicity story: operations are not transactional; partial failure
recoverable via reconciliation. See
docs/hypergraph-protocol/error-handling.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_comment, emit_derivation, emit_finding, emit_review,
)
from lib.backend.links import Link
from lib.febe.protocol import Session


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
) -> Link:
    """Write the aggregate review doc and emit the `review` classifier.

    Path: <reviews_dir>/<asn_label>/review-<N>.md.

    The aggregate is the reviewer's full output; per-finding bodies
    live separately (written by emit_findings).
    """
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

    # 1. Document write
    session.update_document(meta_rel, body)

    # 2. Substrate link emission
    meta_addr = session.register_path(meta_rel)
    link, _ = emit_review(session.store, meta_addr)
    return link


def emit_findings(
    session: Session,
    review_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    label_index: dict,
    findings_dir,
):
    """Materialize per-finding docs and emit their substrate facts.

    `findings` is a list of (title, cls, body). For each:
      1. Resolve target claim via body's `**ASN**: <label>` (or
         `**Foundation**:` fallback).
      2. session.update_document(<findings_dir>/<asn>/<review_stem>/<n>.md)
      3. emit_finding classifier; emit comment.{revise|observe} link;
         emit provenance.derivation from review to finding.

    label_index: {label_string: claim_doc_addr}
    """
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
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

        finding_path = out_dir / f"{n}.md"
        finding_rel = str(finding_path.resolve().relative_to(lattice_root))

        # 1. Document write
        session.update_document(finding_rel, body)

        # 2. Substrate facts
        finding_addr = session.register_path(finding_rel)
        emit_finding(session.store, finding_addr)

        cls_normalized = cls.upper() if cls else "REVISE"
        if cls_normalized not in {"REVISE", "OBSERVE"}:
            cls_normalized = "REVISE"
        comment = emit_comment(
            session.store, finding_addr, claim_addr,
            kind=cls_normalized.lower(),
        )

        emit_derivation(session.store, review_addr, finding_addr)

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


# ============================================================
#  Reconciliation predicates
# ============================================================

# Detect partial-failure states between document writes and link
# emissions in the finding/comment pipeline. Per
# docs/hypergraph-protocol/error-handling.md, operations are not
# transactional; callers should run reconciliation at stage
# boundaries to surface inconsistencies.

# Comment subtypes that source from a finding doc in the
# claim-convergence layer. Both target a claim document.
_CLAIM_FINDING_COMMENT_KINDS = ("comment.revise", "comment.observe")


def orphan_finding_docs(
    session: Session,
    findings_dir,
) -> list:
    """Finding files on disk with no active comment link sourcing
    from them.

    Walks `findings_dir` recursively for `*.md` files. For each,
    checks whether any active `comment.revise` or `comment.observe`
    link has the file's address in its from_set. Files with no
    comment link are orphans — partial failure left a finding doc
    but the comment that should reference it never emitted (or was
    retracted without cleaning up the file).

    Returns absolute paths, sorted.
    """
    from pathlib import Path
    scope = Path(findings_dir).resolve()
    if not scope.exists():
        return []
    lattice_root = session.store.lattice_dir.resolve()
    orphans: list = []
    for path in sorted(scope.rglob("*.md")):
        try:
            finding_rel = str(path.relative_to(lattice_root))
        except ValueError:
            continue
        finding_addr = session.get_addr_for_path(finding_rel)
        if finding_addr is None:
            orphans.append(path)
            continue
        any_link = False
        for kind in _CLAIM_FINDING_COMMENT_KINDS:
            if session.active_links(kind, from_set=[finding_addr]):
                any_link = True
                break
        if not any_link:
            orphans.append(path)
    return orphans


def dangling_finding_links(session: Session) -> list:
    """Active claim-layer comment links whose source finding doc
    is missing.

    Walks every active `comment.revise` and `comment.observe` link.
    For each, checks the from_set finding address resolves to an
    existing file. Links whose source file is missing are dangling
    — link emission succeeded but the doc write didn't (or the doc
    was deleted manually after the link was filed).

    Returns Link records (the substrate-level artifact).
    """
    lattice_root = session.store.lattice_dir.resolve()
    dangling: list = []
    for kind in _CLAIM_FINDING_COMMENT_KINDS:
        for link in session.active_links(kind):
            for finding_addr in link.from_set:
                finding_rel = session.get_path_for_addr(finding_addr)
                if finding_rel is None:
                    dangling.append(link)
                    break
                if not (lattice_root / finding_rel).exists():
                    dangling.append(link)
                    break
    return dangling
