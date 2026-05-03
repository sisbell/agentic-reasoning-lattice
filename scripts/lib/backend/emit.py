"""Semantic emit_* helpers — substrate writes with domain semantics.

Mirrors and consolidates the legacy `scripts/lib/store/emit.py`,
`cite.py`, `classify.py`, `attributes.py`, `retract.py`, `notation.py`,
`agent.py`, `decide.py` modules. All operate on tumbler addresses
(`Address`) via a `Store`.

Each helper:
- Validates the kind/subtype against the catalog (via schema.py)
- Checks active-link idempotency where applicable (skip if already
  filed, ignoring retracted history)
- Emits via Store.make_link, returning (link, created) — the legacy
  pattern lets callers know whether they wrote a fresh fact or hit
  an existing one
"""

from __future__ import annotations

from typing import List, Optional, Tuple

# Re-export Optional for the helper

from .addressing import Address
from .links import Link
from .predicates import active_links
from .schema import REQUIRES_SUBTYPE, VALID_SUBTYPES, validate_type
from .store import Store


# ============================================================
#  Classifier links (F=∅, G=[doc])
# ============================================================


def emit_classifier(
    store: Store, doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File a classifier link of the given kind targeting doc.

    Idempotent on the active-classifier set — if a classifier of the
    same kind already targets doc, returns its (link, False) without
    re-emitting. The classifier link is homed in doc per spec
    convention (F=∅, so homedoc = G[0]).
    """
    validate_type(kind)
    existing = active_links(store.state, kind, to_set=[doc])
    for link in existing:
        if not link.from_set and link.to_set == (doc,):
            return link, False
    link = store.make_link(
        homedoc=doc, from_set=[], to_set=[doc], type_=kind,
    )
    return link, True


def emit_claim(store: Store, claim_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, claim_doc, "claim")


def emit_contract(
    store: Store, claim_doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File contract.<kind> classifier on a claim doc."""
    valid = VALID_SUBTYPES["contract"]
    if kind not in valid:
        raise ValueError(
            f"invalid contract kind {kind!r}; must be one of {sorted(valid)}"
        )
    return emit_classifier(store, claim_doc, f"contract.{kind}")


def emit_note(store: Store, note_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, note_doc, "note")


def emit_inquiry(store: Store, inquiry_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, inquiry_doc, "inquiry")


def emit_campaign(store: Store, campaign_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, campaign_doc, "campaign")


def emit_review(store: Store, review_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, review_doc, "review")


def emit_finding(store: Store, finding_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, finding_doc, "finding")


def emit_consultation_questions(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, doc, "consultation.questions")


def emit_consultation_answer(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, doc, "consultation.answer")


def emit_consultation_assessment(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, doc, "consultation.assessment")


# ============================================================
#  Attribute links (F=[doc], G=[sidecar])
# ============================================================


def emit_attribute_link(
    store: Store, doc: Address, kind: str, sidecar: Address,
) -> Tuple[Link, bool]:
    """File a name/label/description/signature attribute link from
    doc to its sidecar. Pure substrate primitive: takes addresses,
    emits the link. Idempotent on the active-attribute set.
    Homedoc = doc (the link's source).
    """
    valid = {"label", "name", "description", "signature"}
    if kind not in valid:
        raise ValueError(
            f"invalid attribute kind {kind!r}; must be one of {sorted(valid)}"
        )
    existing = active_links(store.state, kind, from_set=[doc], to_set=[sidecar])
    for link in existing:
        if link.from_set == (doc,) and link.to_set == (sidecar,):
            return link, False
    link = store.make_link(
        homedoc=doc, from_set=[doc], to_set=[sidecar], type_=kind,
    )
    return link, True


def emit_attribute(
    store: Store, claim_md_path, kind: str, value: str, lattice_root=None,
) -> Tuple[Link, bool]:
    """Write the sidecar with `value` (edit-in-place) and emit the
    attribute link from claim_md to its sidecar. Mirrors the legacy
    lib.store.attributes.emit_attribute signature.

    `claim_md_path` may be lattice-relative or absolute. The sidecar
    path is derived as `<claim_dir>/<stem>.<kind>.md`. Both docs are
    registered in the path map (allocated fresh tumblers if new).
    """
    from pathlib import Path
    valid = {"label", "name", "description", "signature"}
    if kind not in valid:
        raise ValueError(
            f"invalid attribute kind {kind!r}; must be one of {sorted(valid)}"
        )
    root = Path(lattice_root) if lattice_root else store.lattice_dir
    claim_md = Path(claim_md_path)
    if not claim_md.is_absolute():
        claim_md = (root / claim_md).resolve()
    else:
        claim_md = claim_md.resolve()
    stem = claim_md.stem
    sidecar_abs = claim_md.parent / f"{stem}.{kind}.md"

    if kind == "description":
        body = value if value.endswith("\n") else value + "\n"
    else:
        body = value.rstrip("\n") + "\n"
    if not sidecar_abs.exists() or sidecar_abs.read_text() != body:
        sidecar_abs.parent.mkdir(parents=True, exist_ok=True)
        sidecar_abs.write_text(body)

    root_resolved = root.resolve()
    claim_rel = str(claim_md.relative_to(root_resolved))
    sidecar_rel = str(sidecar_abs.relative_to(root_resolved))
    claim_addr = store.register_path(claim_rel)
    sidecar_addr = store.register_path(sidecar_rel)
    return emit_attribute_link(store, claim_addr, kind, sidecar_addr)


def emit_signature(
    store: Store, claim_doc: Address, sidecar: Address,
) -> Tuple[Link, bool]:
    return emit_attribute_link(store, claim_doc, "signature", sidecar)


def emit_name(
    store: Store, doc: Address, sidecar: Address,
) -> Tuple[Link, bool]:
    return emit_attribute_link(store, doc, "name", sidecar)


def emit_label(
    store: Store, doc: Address, sidecar: Address,
) -> Tuple[Link, bool]:
    return emit_attribute_link(store, doc, "label", sidecar)


def emit_description(
    store: Store, doc: Address, sidecar: Address,
) -> Tuple[Link, bool]:
    return emit_attribute_link(store, doc, "description", sidecar)


# ============================================================
#  Citation relations (F=[citing], G=[cited])
# ============================================================


def emit_citation(
    store: Store,
    citing: Address,
    cited: Address,
    *,
    direction: str = "depends",
) -> Tuple[Link, bool]:
    """File a citation link of the given direction from citing to cited.

    direction ∈ {depends, forward, resolve}. Idempotent on the active
    citation set; a previously-retracted citation does not satisfy
    idempotency (re-emitting after retraction creates a fresh active
    link, since the caller is expressing the citation is currently
    wanted).
    """
    valid = VALID_SUBTYPES["citation"]
    if direction not in valid:
        raise ValueError(
            f"invalid citation direction {direction!r}; "
            f"must be one of {sorted(valid)}"
        )
    type_str = f"citation.{direction}"
    existing = active_links(
        store.state, type_str, from_set=[citing], to_set=[cited],
    )
    for link in existing:
        if link.from_set == (citing,) and link.to_set == (cited,):
            return link, False
    link = store.make_link(
        homedoc=citing,
        from_set=[citing],
        to_set=[cited],
        type_=type_str,
    )
    return link, True


# ============================================================
#  Retraction (F=[doc], G=[link being nullified])
# ============================================================


def emit_retraction(
    store: Store,
    by_doc: Address,
    target_link: Address,
) -> Link:
    """File a retraction link nullifying target_link.

    Convention (matches legacy substrate): F=[by_doc], G=[target_link],
    homedoc=by_doc. The catalog's stated F=∅ shape will be reconciled
    later; this emits in the form the substrate has.
    """
    return store.make_link(
        homedoc=by_doc,
        from_set=[by_doc],
        to_set=[target_link],
        type_="retraction",
    )


# ============================================================
#  Provenance (F=[source], G=[derived])
# ============================================================


def emit_derivation(
    store: Store, source_doc: Address, derived_doc: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.derivation` link source → derived.

    Idempotent on (source, derived).
    """
    existing = active_links(
        store.state,
        "provenance.derivation",
        from_set=[source_doc],
        to_set=[derived_doc],
    )
    for link in existing:
        if (link.from_set == (source_doc,)
                and link.to_set == (derived_doc,)):
            return link, False
    link = store.make_link(
        homedoc=source_doc,
        from_set=[source_doc],
        to_set=[derived_doc],
        type_="provenance.derivation",
    )
    return link, True


def emit_synthesis(
    store: Store, inquiry_doc: Address, note_doc: Address,
) -> Tuple[Link, bool]:
    existing = active_links(
        store.state,
        "provenance.synthesis",
        from_set=[inquiry_doc],
        to_set=[note_doc],
    )
    for link in existing:
        if (link.from_set == (inquiry_doc,)
                and link.to_set == (note_doc,)):
            return link, False
    link = store.make_link(
        homedoc=inquiry_doc,
        from_set=[inquiry_doc],
        to_set=[note_doc],
        type_="provenance.synthesis",
    )
    return link, True


# ============================================================
#  Comment / resolution (review feedback)
# ============================================================


def emit_comment(
    store: Store,
    review_doc: Address,
    target_doc: Address,
    *,
    kind: str = "revise",
) -> Link:
    """File a comment.<kind> link from review doc to target.

    Comments are not idempotent (each review cycle's comments are
    independent facts).
    """
    valid = VALID_SUBTYPES["comment"]
    if kind not in valid:
        raise ValueError(
            f"invalid comment kind {kind!r}; must be one of {sorted(valid)}"
        )
    return store.make_link(
        homedoc=review_doc,
        from_set=[review_doc],
        to_set=[target_doc],
        type_=f"comment.{kind}",
    )


def emit_resolution(
    store: Store,
    by_doc: Address,
    comment: Address,
    *,
    kind: str = "edit",
) -> Link:
    """File a resolution.<kind> link closing a comment.

    Substrate convention (matches legacy + migrated data): F=[by_doc]
    (the doc that was revised, or the rationale doc on rejection),
    G=[comment_addr]. homedoc=by_doc.
    """
    valid = VALID_SUBTYPES["resolution"]
    if kind not in valid:
        raise ValueError(
            f"invalid resolution kind {kind!r}; must be one of {sorted(valid)}"
        )
    return store.make_link(
        homedoc=by_doc,
        from_set=[by_doc],
        to_set=[comment],
        type_=f"resolution.{kind}",
    )


# ============================================================
#  Decision (accept/reject a comment finding)
# ============================================================


def emit_decision(
    store: Store,
    action: str,
    comment_addr: Address,
    claim_addr: Address,
    asn_label: str,
    rationale: Optional[str] = None,
) -> Link:
    """Emit the resolution link for a reviser's accept/reject decision.

    Mirrors lib.store.decide.emit_decision.

    action: 'accept' or 'reject'
    comment_addr: address of the comment being closed
    claim_addr: address of the doc the resolution applies to
    asn_label: ASN label (for rationale doc placement on reject)
    rationale: required when action == 'reject'

    On accept: emits resolution.edit (F=[claim], G=[comment]).
    On reject: writes rationale doc to disk, registers it in path map,
    emits resolution.reject (F=[claim], G=[comment, rationale_doc]).
    """
    from pathlib import Path
    from lib.shared.paths import RATIONALE_DIR

    if action == "accept":
        return store.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr],
            type_="resolution.edit",
        )

    if action == "reject":
        if not rationale:
            raise ValueError("reject requires rationale text")
        target_dir = Path(RATIONALE_DIR) / asn_label
        target_dir.mkdir(parents=True, exist_ok=True)
        rationale_path = target_dir / f"{comment_addr}.md"
        rationale_path.write_text(rationale + "\n")
        rationale_rel = str(
            rationale_path.resolve().relative_to(store.lattice_dir.resolve())
        )
        rationale_addr = store.register_path(rationale_rel)
        return store.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr, rationale_addr],
            type_="resolution.reject",
        )

    raise ValueError(f"unknown action: {action!r}")


# ============================================================
#  Agent attribution
# ============================================================


def emit_agent(
    store: Store, agent_doc: Address,
) -> Tuple[Link, bool]:
    """Classifier marking a doc as an agent. Idempotent."""
    return emit_classifier(store, agent_doc, "agent")


def emit_manages(
    store: Store, agent_doc: Address, operation_link: Address,
) -> Link:
    """File a `manages` attribution link from agent to operation_link.

    Manages links are NOT idempotent — each operation gets its own
    fresh manages emission marking who's responsible for it.
    """
    return store.make_link(
        homedoc=agent_doc,
        from_set=[agent_doc],
        to_set=[operation_link],
        type_="manages",
    )


# ============================================================
#  Claim findings + review meta
# ============================================================


def emit_meta(
    store: Store,
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
    """Write the aggregate review doc to <reviews_dir>/<asn>/review-N.md
    and emit the `review` classifier on it.

    Mirrors lib.store.emit.emit_meta. The aggregate is the reviewer's
    full output; per-finding bodies live separately (written by
    emit_findings).
    """
    from pathlib import Path
    reviews_root = Path(reviews_dir)
    review_stem = f"review-{review_num}"
    asn_dir = reviews_root / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
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
    meta_path.write_text("\n".join(lines) + "\n")

    meta_rel = str(meta_path.resolve().relative_to(store.lattice_dir.resolve()))
    meta_addr = store.register_path(meta_rel)
    link, _ = emit_review(store, meta_addr)
    return link


def emit_findings(
    store: Store,
    review_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    label_index: dict,
    findings_dir,
):
    """Materialize each claim-side finding as a doc and emit its substrate
    facts. Mirrors lib.store.emit.emit_findings.

    `findings` is a list of (title, cls, body). For each:
      - resolve target claim via body's `**ASN**: <label>` (or
        `**Foundation**:` fallback)
      - materialize <findings_dir>/<asn>/<review_stem>/<n>.md
      - emit `finding` classifier on the per-finding doc
      - emit `comment.{revise|observe}` from finding doc to target claim
      - emit `provenance.derivation` from aggregate review to finding

    label_index: {label_string: claim_doc_addr}
    """
    from pathlib import Path
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    out_dir.mkdir(parents=True, exist_ok=True)

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
        finding_path.write_text(body)
        finding_rel = str(finding_path.resolve().relative_to(
            store.lattice_dir.resolve()
        ))
        finding_addr = store.register_path(finding_rel)

        emit_finding(store, finding_addr)

        cls_normalized = cls.upper() if cls else "REVISE"
        if cls_normalized not in {"REVISE", "OBSERVE"}:
            cls_normalized = "REVISE"
        comment = emit_comment(
            store, finding_addr, claim_addr,
            kind=cls_normalized.lower(),
        )

        emit_derivation(store, review_addr, finding_addr)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment.addr,
            "claim_path": store.path_for_addr(claim_addr),
            "finding_path": finding_rel,
        })

    return results


def _extract_target_label(body: str, label_index: dict) -> Optional[str]:
    """Parse a finding body for an ASN/Foundation label that resolves
    in label_index. Returns the label string or None.
    """
    import re
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
#  Note findings (per-finding doc materialization)
# ============================================================


def emit_note_findings(
    store: Store,
    note_addr: Address,
    aggregate_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    findings_dir,
):
    """Materialize each note-review finding as a doc and emit its substrate
    facts.

    Mirrors legacy `lib.store.emit.emit_note_findings`. For each
    (title, cls, body) in `findings`:
      - write body to <findings_dir>/<asn_label>/<review_stem>/<n>.md
      - register the finding doc's path → tumbler
      - emit `finding` classifier on the per-finding doc
      - emit `comment.{revise|out-of-scope}` from finding doc to note
      - emit `provenance.derivation` from aggregate review to finding

    Returns list of {title, cls, comment_id, note_path, finding_path} dicts.
    """
    from pathlib import Path
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    out_dir.mkdir(parents=True, exist_ok=True)

    note_rel = store.path_for_addr(note_addr)
    results = []
    for n, (title, cls, body) in enumerate(findings):
        finding_path = out_dir / f"{n}.md"
        finding_path.write_text(body)
        finding_rel = str(finding_path.resolve().relative_to(
            store.lattice_dir.resolve()
        ))
        finding_addr = store.register_path(finding_rel)

        emit_finding(store, finding_addr)

        cls_normalized = (cls or "REVISE").upper()
        if cls_normalized == "OUT_OF_SCOPE":
            comment_kind = "out-of-scope"
        else:
            comment_kind = "revise"

        comment = emit_comment(
            store, finding_addr, note_addr, kind=comment_kind,
        )

        emit_derivation(store, aggregate_addr, finding_addr)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment.addr,
            "note_path": note_rel,
            "finding_path": finding_rel,
        })

    return results


# ============================================================
#  Notation (lattice-wide singleton)
# ============================================================


def emit_notation(
    store: Store, notation_doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, notation_doc, "notation")
