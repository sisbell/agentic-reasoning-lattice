"""Helpers translating reviewer outputs into link writes.

Each review run materializes its findings as documents under
`_workspace/findings/{kind}/{asn}/{review_stem}/{n}.md` (kind ∈
{claims, notes}) and emits comment links from those documents to their
target claims/notes, plus a `review` classifier link on the review
markdown itself.

Resolution links (the reviser's accept/reject decision) are emitted by
`scripts/convergence-link-resolution.py`, not by this module — the reviser invokes the tool
directly so its action is the protocol operation.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import LATTICE
from lib.store.queries import active_links


def emit_review(store, review_md_path):
    """Make `review` classifier link on the review markdown file."""
    return store.make_link(
        from_set=[],
        to_set=[_lattice_relative(review_md_path)],
        type_set=["review"],
    )


def emit_finding(store, finding_md_path):
    """Classify a doc as a per-finding decomposition output. Idempotent.
    Returns (link_id, created).

    A finding doc holds one comment's worth of reviewer text, extracted from
    an aggregate review doc by the convergence protocol's decomposition step.
    The doc participates separately in a `comment.<kind>` relation to the
    target it comments on, and in a `provenance.derivation` relation back to
    the aggregate review it came from."""
    return _emit_classifier(store, finding_md_path, "finding")


def emit_note(store, note_md_path):
    """Classify a doc as a note. Idempotent on active classifiers.

    Returns (link_id, created). If an active `note` classifier already
    targets this doc, returns its id with created=False. Otherwise files
    a new classifier and returns (new_id, True). Same shape as
    `emit_agent` in lib.store.agent.
    """
    return _emit_classifier(store, note_md_path, "note")


def emit_campaign(store, campaign_md_path):
    """Classify a doc as a campaign descriptor. Idempotent. Returns
    (link_id, created)."""
    return _emit_classifier(store, campaign_md_path, "campaign")


def emit_inquiry(store, inquiry_md_path):
    """Classify a doc as an inquiry. Idempotent. Returns (link_id, created)."""
    return _emit_classifier(store, inquiry_md_path, "inquiry")


def emit_consultation_questions(store, questions_md_path):
    """Classify a doc as a consultation's generated question set.
    Idempotent. Returns (link_id, created).

    The question set is the artifact of one question-generation act —
    typically `questions.md` written by decompose. Tracing the set as
    a unit (rather than per-question) preserves the generation event."""
    return _emit_classifier(store, questions_md_path, "consultation.questions")


def emit_consultation_answer(store, answer_md_path):
    """Classify a doc as one Q+A pair from a consultation. Idempotent.
    Returns (link_id, created).

    Each per-answer file (`answer-NN-<role>.md`) carries one question
    and the channel's answer; the doc is self-contained. Both draft
    and revise consultations now produce these uniformly."""
    return _emit_classifier(store, answer_md_path, "consultation.answer")


def emit_consultation_assessment(store, assessment_md_path):
    """Classify a doc as a consultation's channel-assignment record.
    Idempotent. Returns (link_id, created).

    Assessment docs are produced only by revise consultations: an LLM
    response, persisted verbatim, that decides for each REVISE finding
    which channel(s) to consult and drafts the focused question. The
    audit trail of why a finding was routed where."""
    return _emit_classifier(store, assessment_md_path, "consultation.assessment")


def emit_claim(store, claim_md_path):
    """Classify a doc as a claim. Idempotent. Returns (link_id, created).

    Filed by claim derivation per the Claim Document Contract (invariant #4):
    every claim body markdown carries exactly one active `claim` classifier
    link in the substrate."""
    return _emit_classifier(store, claim_md_path, "claim")


def emit_contract(store, claim_md_path, kind):
    """File a `contract.<kind>` classifier on the claim body markdown.
    Idempotent on (doc, kind). Returns (link_id, created).

    `kind` must be one of: axiom, definition, theorem, corollary, lemma,
    consequence, design-requirement.

    Filed by claim derivation per the Claim Document Contract (invariant #4):
    every claim body carries exactly one active `contract.<kind>` classifier
    declaring its formal status."""
    return _emit_classifier(store, claim_md_path, f"contract.{kind}")


def emit_derivation(store, from_md_path, to_md_path):
    """File a `provenance.derivation` link from a source doc to a derivation
    output doc. Idempotent on (from, to) pair. Returns (link_id, created).

    Records that the `to` doc was derived (decomposed) from the `from` doc.
    Two operations file this kind of provenance:

    - Claim derivation (note → claim): each claim's body carries exactly one
      active `provenance.derivation` link from its source note. Per the Claim
      Document Contract (invariant #13).
    - Review decomposition (aggregate review → finding): each per-finding doc
      carries one active `provenance.derivation` link from the aggregate
      review it was extracted from.

    The link persists permanently regardless of subsequent edits to either
    doc. Sibling of `provenance.synthesis` (inquiry → note) and the
    maturation provenance subtypes."""
    from_rel = _lattice_relative(from_md_path)
    to_rel = _lattice_relative(to_md_path)
    candidates = active_links(
        store, "provenance.derivation",
        from_set=[from_rel], to_set=[to_rel],
    )
    for link in candidates:
        if (link["from_set"] == [from_rel]
                and link["to_set"] == [to_rel]):
            return link["id"], False
    link_id = store.make_link(
        from_set=[from_rel], to_set=[to_rel],
        type_set=["provenance.derivation"],
    )
    return link_id, True


def emit_synthesis(store, inquiry_md_path, note_md_path):
    """File a `provenance.synthesis` link from inquiry to the produced note.
    Idempotent on active (inquiry, note) pair. Returns (link_id, created).

    The link records the consultation protocol's provenance fact: this note
    was produced by synthesizing answers from the inquiry's consultations.
    Sibling of `provenance.derivation` (note → claim) and the maturation
    provenance subtypes."""
    inquiry_rel = _lattice_relative(inquiry_md_path)
    note_rel = _lattice_relative(note_md_path)
    candidates = active_links(
        store, "provenance.synthesis",
        from_set=[inquiry_rel], to_set=[note_rel],
    )
    for link in candidates:
        if (link["from_set"] == [inquiry_rel]
                and link["to_set"] == [note_rel]):
            return link["id"], False
    link_id = store.make_link(
        from_set=[inquiry_rel], to_set=[note_rel],
        type_set=["provenance.synthesis"],
    )
    return link_id, True


def _emit_classifier(store, doc_path, type_name):
    """Shared idempotent-classifier emission used by emit_note,
    emit_campaign, emit_inquiry. Skipped types live in their own
    modules (emit_agent in lib.store.agent has its own copy)."""
    rel = _lattice_relative(doc_path)
    candidates = active_links(store, type_name, to_set=[rel])
    for link in candidates:
        if link["from_set"] == [] and link["to_set"] == [rel]:
            return link["id"], False
    link_id = store.make_link(
        from_set=[], to_set=[rel], type_set=[type_name],
    )
    return link_id, True


def emit_meta(store, asn_label, review_num, *, title, timestamp, scope,
              verdict, findings_summary, emitted_findings, elapsed_seconds,
              reviews_dir):
    """Write the review event's aggregate doc to
    `<reviews_dir>/<asn>/review-N.md` and emit the `review` classifier
    link pointing at it.

    The aggregate is the reviewer's full output — header, scope,
    verdict, finding-summary table, elapsed time. Per-finding bodies
    live separately in `<findings_dir>/<asn>/review-N/<n>.md` (written
    by `emit_findings`); the aggregate links to those filenames in its
    summary table but doesn't carry their bodies.

    Args:
      asn_label: e.g. "ASN-0034"
      review_num: integer, the review number
      title: e.g. "Cone Review — ASN-0034/T4 (cycle 1)"
      timestamp: pre-formatted timestamp string
      scope: human description, e.g. "T4 + 6 deps (cone)"
      verdict: "CONVERGED" | "REVISE" | "OBSERVE" | "FAILED"
      findings_summary: e.g. "1 REVISE, 2 OBSERVE" (or "0 findings")
      emitted_findings: list of dicts from emit_findings (each has title, cls,
                       finding_path). Used to write the summary table.
      elapsed_seconds: float, used for the Elapsed line.
      reviews_dir: kind-scoped aggregate-review root (CLAIM_REVIEWS_DIR
                   or NOTE_REVIEWS_DIR) — caller selects per protocol.

    Returns the link id of the review classifier link.
    """
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

    return emit_review(store, meta_path)


def emit_findings(store, review_md_path, findings, asn_label, review_stem,
                  label_index, findings_dir):
    """Materialize each finding as a document and emit its substrate facts.

    `findings` is the list of (title, cls, body) tuples from
    `extract_findings()`. For each:
      - resolve target claim via the body's `**ASN**: <label>` line
        (falls back to `**Foundation**:` if ASN is absent)
      - materialize a document at <findings_dir>/<asn_label>/<review_stem>/<n>.md
      - emit `finding` classifier on the per-finding doc
      - emit `comment.{revise|observe}` from the per-finding doc to the
        target claim
      - emit `provenance.derivation` from the aggregate review doc
        (`review_md_path`) to the per-finding doc

    `findings_dir` is the kind-scoped findings root (CLAIM_FINDINGS_DIR or
    NOTE_FINDINGS_DIR) — caller selects per protocol.

    Returns list of {title, cls, comment_id, claim_path, finding_path} dicts
    in input order, omitting findings whose target couldn't be resolved
    (logged to stderr).
    """
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for n, (title, cls, body) in enumerate(findings):
        target_label = _extract_target_label(body, label_index)
        if target_label is None:
            print(
                f"  [emit] skipping finding {n} '{title}' — "
                f"no parseable target label (no Foundation/ASN token "
                f"matches a known claim)",
                file=sys.stderr,
            )
            continue
        claim_path = label_index[target_label]

        finding_path = out_dir / f"{n}.md"
        finding_path.write_text(body)
        finding_rel = _lattice_relative(finding_path)

        emit_finding(store, finding_path)

        cls_normalized = cls.upper() if cls else "REVISE"
        if cls_normalized not in {"REVISE", "OBSERVE"}:
            cls_normalized = "REVISE"
        comment_type = f"comment.{cls_normalized.lower()}"

        comment_id = store.make_link(
            from_set=[finding_rel],
            to_set=[claim_path],
            type_set=[comment_type],
        )

        emit_derivation(store, review_md_path, finding_path)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment_id,
            "claim_path": claim_path,
            "finding_path": finding_rel,
        })

    return results


def emit_note_findings(store, note_md_path, aggregate_md_path, findings,
                       asn_label, review_stem, findings_dir):
    """Materialize each note-review finding as a document and emit its
    substrate facts.

    Parallels `emit_findings` for notes per the Note Convergence Protocol
    §6.5. Differences from the claim-side: the target is the note itself
    (no per-finding label routing), and class ∈ {"REVISE", "OUT_OF_SCOPE"}
    per protocol §1.

    `findings` is a list of (title, cls, body) tuples. For each:
      - materialize a document at <findings_dir>/<asn_label>/<review_stem>/<n>.md
      - emit `finding` classifier on the per-finding doc
      - emit `comment.{revise|out-of-scope}` from the per-finding doc to
        the note (the review's target)
      - emit `provenance.derivation` from `aggregate_md_path` (the
        aggregate review doc) to the per-finding doc

    Returns list of {title, cls, comment_id, note_path, finding_path} dicts
    in input order.
    """
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    out_dir.mkdir(parents=True, exist_ok=True)

    note_rel = _lattice_relative(note_md_path)
    results = []
    for n, (title, cls, body) in enumerate(findings):
        finding_path = out_dir / f"{n}.md"
        finding_path.write_text(body)
        finding_rel = _lattice_relative(finding_path)

        emit_finding(store, finding_path)

        cls_normalized = (cls or "REVISE").upper()
        if cls_normalized == "OUT_OF_SCOPE":
            comment_type = "comment.out-of-scope"
        else:
            comment_type = "comment.revise"

        comment_id = store.make_link(
            from_set=[finding_rel],
            to_set=[note_rel],
            type_set=[comment_type],
        )

        emit_derivation(store, aggregate_md_path, finding_path)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment_id,
            "note_path": note_rel,
            "finding_path": finding_rel,
        })

    return results


def _extract_target_label(body, label_index):
    """Find the target claim label from a finding body, validated against label_index.

    The reviewer's `**Foundation**:` field reliably starts with a claim label
    (e.g., "NAT-order *Consequence*", "T0 (CarrierSetDefinition)"). The
    `**ASN**:` field is typically descriptive prose. We try Foundation first,
    then ASN as fallback. From each field we tokenize and return the first
    token that's a known label.
    """
    for field in ("Foundation", "ASN"):
        m = re.search(rf"\*\*{field}\*\*:\s*(.+)", body)
        if m:
            tokens = re.findall(r"[A-Za-z][\w.-]*", m.group(1))
            for token in tokens:
                if token in label_index:
                    return token
    return None


def _lattice_relative(path):
    return str(Path(path).resolve().relative_to(Path(LATTICE).resolve()))
