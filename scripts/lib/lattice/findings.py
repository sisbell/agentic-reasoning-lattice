"""Review-doc + per-finding emission — shared across review domains.

Three helpers:

- `emit_review_doc(session, ...)` — writes the LLM's review output
  verbatim to the docuverse review path and emits the `review`
  classifier + `review.coverage` links on it.
- `record_findings(session, ...)` — parses each finding's target
  claim label and delegates the per-finding doc-write + link-emit
  to `record_one_finding`. Claim-finding-format-specific (regex on
  `**ASN**:` / `**Foundation**:`); a parallel parser would land here
  if note reviews adopt the same shape.
- `record_one_finding(session, ...)` — the per-finding atom: write
  the doc, emit the `finding` classifier, emit a `comment.<kind>`
  link to the target, emit `provenance.derivation` from the parent
  review. Used by both note-refinement and claim-refinement;
  targets and comment-kind sets differ but the shape is identical.

Atomicity story: operations are not transactional; partial failure
recoverable via reconciliation. See
docs/hypergraph-protocol/error-handling.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple

from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation_bundle, emit_comment, emit_derivation, emit_finding,
    emit_review_content, emit_review_coverage,
)
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session
from lib.shared.paths import review_aggregate_path


def emit_review_doc(
    session: Session,
    asn_label: str,
    review_num: int,
    *,
    body: str,
    covered_addrs: list[Address] | None = None,
    cascade_anchor_heads: list[Address] | None = None,
    kind: str = "claim",
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

    `cascade_anchor_heads`, when provided, records via a single bundled
    `citation.depends` link the foundation version_heads this review
    actually read. `is_claim_cascade_fresh` later walks this anchor and
    re-fires review if any upstream has advanced — the claim-side port
    of the note's review-anchored cascade.

    `kind` ("claim" | "cone" | "note") routes the doc to the right
    review namespace; cone reviews land under `review/cone-claims/` as
    `cone-N.md` so the convergence gates can tell them apart (see
    `is_cone_review_path`).

    Returns `(review_addr, review_path)`.
    """
    review_path = review_aggregate_path(asn_label, review_num, kind=kind)
    lattice_root = session.store.lattice_dir.resolve()
    review_rel = str(review_path.resolve().relative_to(lattice_root))

    session.update_document(review_rel, body)
    review_addr = session.register_path(review_rel)
    emit_review_content(session.store, review_addr)

    if covered_addrs:
        for covered in covered_addrs:
            emit_review_coverage(session.store, review_addr, covered)

    if cascade_anchor_heads:
        emit_citation_bundle(
            session.store, review_addr, cascade_anchor_heads,
            direction="depends",
        )

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

        # A REVISE mints a blocking `comment.revise` that the revise loop
        # must resolve to converge. Downgrade to OBSERVE (non-blocking)
        # when the loop CANNOT durably resolve it, otherwise the next
        # full-review re-flags the same defect forever (the ASN-0053
        # livelock). Two unresolvable cases:
        #   (1) the reviewer marked it non-actionable
        #       (`What needs resolving: N/A`, empty, or absent), or
        #   (2) the fix locus is not an editable claim in THIS ASN's
        #       claim dir — e.g. the frozen source note's Properties
        #       table, or a foreign-ASN foundation claim like D0
        #       (ASN-0034). `claim_revise` only edits this ASN's claim
        #       files, so it can never change those.
        if cls_normalized == "REVISE":
            reason = None
            if not _finding_actionable(body):
                reason = "non-actionable (What-needs-resolving N/A/absent)"
            elif not _target_is_editable_claim(session, claim_addr, asn_label):
                reason = "fix locus not an editable claim in this ASN"
            elif _is_missing_fc_finding(title, body) and _target_fc_exempt(
                session, claim_addr
            ):
                reason = "missing-formal-contract on an FC-exempt claim kind"
            if reason is not None:
                import sys as _sys
                print(
                    f"  [emit] finding {n} '{title}' REVISE→OBSERVE: "
                    f"{reason}",
                    file=_sys.stderr,
                )
                cls_normalized = "OBSERVE"
                body = body.rstrip() + (
                    f"\n\n**Routing**: emitted as comment.observe "
                    f"(non-blocking) — {reason}.\n"
                )

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


_NONACTIONABLE_RE = re.compile(
    r"^\s*(n/?a\b|none\b|—|-+|\(observe\))", re.IGNORECASE
)


def _finding_actionable(body: str) -> bool:
    """True iff the finding carries an actionable `What needs resolving`
    instruction. A REVISE finding the reviewer marked `N/A`, left blank,
    or omitted entirely cannot be acted on — the reviser is told to
    "apply exactly the fix described in What needs resolving," and there
    is none. Treat such findings as OBSERVE so they don't mint a
    `comment.revise` the loop can never close.
    """
    m = re.search(r"\*\*What needs resolving\*\*\s*[:\-]\s*(.*)", body)
    if not m:
        return False
    text = m.group(1).strip()
    if not text:
        return False
    return _NONACTIONABLE_RE.match(text) is None


def _target_is_editable_claim(
    session: Session, claim_addr: Address, asn_label: str
) -> bool:
    """True iff `claim_addr` is an editable claim file in THIS ASN's
    claim dir. `claim_revise` only edits `{claim_dir}/{asn_label}/*.md`,
    so findings whose target resolves to the frozen source note, a
    generated aggregate (`_statements`), or a foreign-ASN foundation
    claim (e.g. D0 in ASN-0034) cannot be durably fixed by the loop and
    must not mint a blocking `comment.revise`.
    """
    path = session.get_path_for_addr(claim_addr)
    if not path:
        return False
    return f"/claim/{asn_label}/" in path and "/_statements" not in path


_MISSING_FC_RE = re.compile(
    r"(no|missing|lacks?|absent|without)[^.\n]{0,40}formal contract"
    r"|formal contract[^.\n]{0,40}(missing|absent|not present|is absent)",
    re.IGNORECASE,
)


def _is_missing_fc_finding(title: str, body: str) -> bool:
    """True iff the finding asserts the target claim lacks a Formal
    Contract section. Matched on title + body."""
    return bool(
        _MISSING_FC_RE.search(title or "") or _MISSING_FC_RE.search(body or "")
    )


def _target_fc_exempt(session: Session, claim_addr: Address) -> bool:
    """True iff the target claim's kind never carries a Formal Contract.

    Only theorem/lemma/corollary require one (KINDS_REQUIRING_CONTRACT);
    axiom/definition/design-requirement are permanently FC-less, so a
    "missing formal contract" finding against them is a non-issue — the
    same exemption full_review's predicate applies before reviewing.
    """
    from lib.agents.producers.claim_formal_contract import (
        KINDS_REQUIRING_CONTRACT,
    )
    from lib.predicates import current_contract_kind
    kind = current_contract_kind(session, claim_addr)
    return kind is not None and kind not in KINDS_REQUIRING_CONTRACT


def _extract_target_label(body: str, label_index: dict) -> Optional[str]:
    """Parse a finding body for an ASN/Foundation label that resolves
    in label_index. Returns the label string or None.

    Matches against the KNOWN labels in label_index rather than a
    restrictive character class, so labels containing dots, parentheses,
    or non-ASCII characters (e.g. `Σ.C`, `Σ.M(d)`) resolve — the old
    `[A-Za-z0-9_./-]+` capture silently dropped every finding on those.
    The label must be what the line *starts with* (after stripping
    leading markdown markup); the longest such label wins, disambiguating
    prefixes (S8a over S8). We deliberately do NOT match a label appearing
    anywhere in the line: a whole-ASN observation that lists several
    claims (e.g. "Document order: AX-2, S1, AX-1") has no single target
    and must not be mis-routed to an arbitrary one.
    """
    for header in ("ASN", "Foundation"):
        m = re.search(rf"\*\*{header}\*\*\s*[:\-]\s*(.+)", body)
        if not m:
            continue
        rest = m.group(1).strip().lstrip("`*\"' ")
        prefix = [lbl for lbl in label_index if rest.startswith(lbl)]
        if prefix:
            return max(prefix, key=len)
    return None


def record_one_finding(
    session: Session,
    *,
    finding_path_rel: str,
    body: str,
    target_addr: Address,
    review_addr: Address,
    comment_kind: str,
) -> Tuple[Address, Link]:
    """Materialize one finding: doc write + three substrate facts.

    1. session.update_document(finding_path_rel, body)
    2. emit_finding classifier on the per-finding doc
    3. emit comment.<comment_kind> from finding doc to target
    4. emit provenance.derivation from aggregate review to finding

    Caller is responsible for resolving target_addr and mapping the
    domain-specific classification to a substrate comment kind.

    Returns (finding_addr, comment_link).
    """
    session.update_document(finding_path_rel, body)
    finding_addr = session.register_path(finding_path_rel)
    emit_finding(session.store, finding_addr)
    comment = emit_comment(
        session.store, finding_addr, target_addr, kind=comment_kind,
    )
    emit_derivation(session.store, review_addr, finding_addr)
    return finding_addr, comment
