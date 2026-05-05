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


def emit_review_coverage(
    store: Store, review_meta: Address, covered: Address,
) -> Tuple[Link, bool]:
    """Record that `covered` is within `review_meta`'s coverage.

    Idempotent on (review_meta, covered). Forms the substrate join
    between reviews and the docs they covered — read by the
    confirmation predicate today, by coverage / staleness predicates
    later. See docs/hypergraph-protocol/review-coverage.md.
    """
    existing = active_links(
        store.state, "review.coverage",
        from_set=[review_meta], to_set=[covered],
    )
    if existing:
        return existing[0], False
    link = store.make_link(
        homedoc=review_meta,
        from_set=[review_meta], to_set=[covered],
        type_="review.coverage",
    )
    return link, True


def emit_finding(store: Store, finding_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, finding_doc, "finding")


def emit_promotion(
    store: Store, promotion_doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File a `promotion.<kind>` classifier on a report doc.

    Distinguishes the input flow that produced the report:
      out-of-scope    — items from review OUT_OF_SCOPE sections
      open-questions  — items from the note's Open Questions section
    """
    valid = VALID_SUBTYPES["promotion"]
    if kind not in valid:
        raise ValueError(
            f"invalid promotion kind {kind!r}; must be one of {sorted(valid)}"
        )
    return emit_classifier(store, promotion_doc, f"promotion.{kind}")


def emit_supersession(
    store: Store, superseded: Address, succeeding: Address,
) -> Tuple[Link, bool]:
    """Declare that `succeeding` supersedes `superseded`.

    Per LM 4/52-4/53: a supersession link records "this version
    replaces that one." F=[superseded], G=[succeeding]. Idempotent on
    (superseded, succeeding) — if the same edge already exists active,
    returns it without re-emitting.

    Reading: walk outgoing supersession from any address to find what
    replaces it. The head version is the address with no outgoing
    supersession link.
    """
    existing = active_links(
        store.state, "supersession",
        from_set=[superseded], to_set=[succeeding],
    )
    if existing:
        return existing[0], False
    link = store.make_link(
        homedoc=superseded,
        from_set=[superseded], to_set=[succeeding],
        type_="supersession",
    )
    return link, True


def emit_retired(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    """Mark a doc as retired (lifecycle: out of active lattice).

    Classifier-shape link (F=∅, G=[doc]). Idempotent on the active
    set — re-emitting returns the existing link without re-emitting.
    Reviving the doc is a `retraction` on this link (standard
    substrate primitive); each transition is a real fact, not a
    toggled state.
    """
    return emit_classifier(store, doc, "retired")


def emit_extends(
    store: Store, ext_note: Address, base_note: Address,
) -> Tuple[Link, bool]:
    """Declare that `ext_note` is an extension of `base_note`.

    F=[ext_note], G=[base_note]. Idempotent on (ext, base) — re-emitting
    returns the existing link. Reverse-walked by find-extensions queries
    ("what extends ASN-NNNN?").
    """
    existing = active_links(
        store.state, "extends",
        from_set=[ext_note], to_set=[base_note],
    )
    if existing:
        return existing[0], False
    link = store.make_link(
        homedoc=ext_note,
        from_set=[ext_note], to_set=[base_note],
        type_="extends",
    )
    return link, True


def emit_source(
    store: Store, ext_note: Address, origin_note: Address,
) -> Tuple[Link, bool]:
    """Declare that `ext_note` was extracted from `origin_note`.

    F=[ext_note], G=[origin_note]. Idempotent on (ext, origin). For an
    extension carved from multiple origins, emit one source link per
    origin.
    """
    existing = active_links(
        store.state, "source",
        from_set=[ext_note], to_set=[origin_note],
    )
    if existing:
        return existing[0], False
    link = store.make_link(
        homedoc=ext_note,
        from_set=[ext_note], to_set=[origin_note],
        type_="source",
    )
    return link, True


def emit_transclusion(
    store: Store, transclusion_doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File a `transclusion.<kind>` runtime tag on a doc.

    Marks the doc as rendered-on-read; the kind selects which renderer
    (registered via lib/lattice/render.py) supplies content. The tag
    is a read-mechanism flag, not a structural classifier — predicates
    and substrate walks should NOT branch on its presence.
    """
    valid = VALID_SUBTYPES["transclusion"]
    if kind not in valid:
        raise ValueError(
            f"invalid transclusion kind {kind!r}; must be one of {sorted(valid)}"
        )
    return emit_classifier(store, transclusion_doc, f"transclusion.{kind}")


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
    """File an attribute link from doc to its sidecar (label, name,
    description, signature, statements). Pure substrate primitive:
    takes addresses, emits the link. Idempotent on the active-
    attribute set. Homedoc = doc (the link's source).
    """
    from .schema import VALID_ATTRIBUTE_KINDS
    if kind not in VALID_ATTRIBUTE_KINDS:
        raise ValueError(
            f"invalid attribute kind {kind!r}; must be one of "
            f"{sorted(VALID_ATTRIBUTE_KINDS)}"
        )
    existing = active_links(store.state, kind, from_set=[doc], to_set=[sidecar])
    for link in existing:
        if link.from_set == (doc,) and link.to_set == (sidecar,):
            return link, False
    link = store.make_link(
        homedoc=doc, from_set=[doc], to_set=[sidecar], type_=kind,
    )
    return link, True


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


def emit_clone(
    store: Store, origin_note: Address, clone_note: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.clone` link from origin to clone.

    Records that `clone_note` is a whole-note copy of `origin_note`.
    Idempotent on (origin, clone). Used by note-clone for cheap
    experiments that preserve the origin's expensive consultation
    on the new ASN.
    """
    existing = active_links(
        store.state,
        "provenance.clone",
        from_set=[origin_note],
        to_set=[clone_note],
    )
    for link in existing:
        if (link.from_set == (origin_note,)
                and link.to_set == (clone_note,)):
            return link, False
    link = store.make_link(
        homedoc=origin_note,
        from_set=[origin_note],
        to_set=[clone_note],
        type_="provenance.clone",
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
#  Notation (lattice-wide singleton)
# ============================================================


def emit_notation(
    store: Store, notation_doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, notation_doc, "notation")
