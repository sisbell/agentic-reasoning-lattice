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
from .shapes import LinkShape, shape_for, subtypes_of, validate_type
from .store import Store


# ============================================================
#  Generic typed emit primitive
# ============================================================
#
# `emit()` reads the link's shape from the registry, validates F/G
# cardinality, runs the active-set existence check (when the shape is
# idempotent), and writes the link. The semantic helpers below
# (emit_claim, emit_citation, emit_review_coverage, etc.) are thin
# wrappers that supply the type and bind F/G into named arguments.


def _validate_cardinality(shape: LinkShape, from_set, to_set) -> None:
    def check(name, expected, actual):
        if expected == "empty" and actual:
            raise ValueError(
                f"{name} must be empty for this shape; got {actual!r}"
            )
        if expected == "one" and len(actual) != 1:
            raise ValueError(
                f"{name} must have exactly one address for this shape; "
                f"got {len(actual)}"
            )
        if expected == "one_or_empty" and len(actual) > 1:
            raise ValueError(
                f"{name} must be empty or exactly one address; "
                f"got {len(actual)}"
            )
        if expected == "many" and not actual:
            raise ValueError(
                f"{name} must have at least one address for this shape; "
                f"got 0"
            )

    check("from_set", shape.f_cardinality, from_set)
    check("to_set", shape.g_cardinality, to_set)


def _default_homedoc(
    shape: LinkShape, from_set, to_set,
) -> Address:
    """Pick the canonical homedoc for a shape.

    Convention: classifier-shape links (F=∅) home in G[0]; everything
    else homes in F[0]. Callers can override by passing homedoc
    explicitly.
    """
    if shape.f_cardinality == "empty":
        return to_set[0]
    return from_set[0]


def emit(
    store: Store,
    type_: str,
    *,
    from_set: Optional[List[Address]] = None,
    to_set: Optional[List[Address]] = None,
    homedoc: Optional[Address] = None,
) -> Tuple[Link, bool]:
    """Typed substrate emit — shape-validated, idempotent by shape.

    Reads the link's shape from the registry (lib/backend/shapes.py),
    validates F/G cardinality, runs the active-set existence check
    when the shape is idempotent, and writes the link. Returns
    (link, created) — `created` is False if an active equivalent
    already existed (idempotent shapes only).
    """
    validate_type(type_)
    shape = shape_for(type_)

    f = list(from_set or ())
    g = list(to_set or ())
    _validate_cardinality(shape, f, g)

    if homedoc is None:
        homedoc = _default_homedoc(shape, f, g)

    if shape.idempotent:
        existing = active_links(
            store.state, type_,
            from_set=f or None,
            to_set=g or None,
        )
        for link in existing:
            if (tuple(link.from_set) == tuple(f)
                    and tuple(link.to_set) == tuple(g)):
                return link, False

    link = store.make_link(
        homedoc=homedoc,
        from_set=f,
        to_set=g,
        type_=type_,
    )
    return link, True


# ============================================================
#  Classifier links (F=∅, G=[doc])
# ============================================================


def emit_classifier(
    store: Store, doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File a classifier link of the given kind targeting doc.

    Idempotent on the active-classifier set — if a classifier of the
    same kind already targets doc, returns its (link, False) without
    re-emitting.
    """
    return emit(store, kind, to_set=[doc])


def emit_claim(store: Store, claim_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, claim_doc, "claim")


def emit_contract(
    store: Store, claim_doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File contract.<kind> classifier on a claim doc."""
    valid = subtypes_of("contract")
    if kind not in valid:
        raise ValueError(
            f"invalid contract kind {kind!r}; must be one of {sorted(valid)}"
        )
    return emit_classifier(store, claim_doc, f"contract.{kind}")


def emit_note(store: Store, note_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, note_doc, "note")


def emit_inquiry(store: Store, inquiry_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, inquiry_doc, "inquiry")


def emit_patch_note(store: Store, patch_doc: Address) -> Tuple[Link, bool]:
    """Classifier on a note-targeted patch doc — promoted from workspace
    into substrate by NotePatchAgent on each fire."""
    return emit_classifier(store, patch_doc, "patch.note")


def emit_patch_claim(store: Store, patch_doc: Address) -> Tuple[Link, bool]:
    """Classifier on a claim-targeted patch doc — promoted from workspace
    into substrate by ClaimPatchAgent on each fire."""
    return emit_classifier(store, patch_doc, "patch.claim")


def emit_extract(store: Store, extract_doc: Address) -> Tuple[Link, bool]:
    """Classifier on an extract spec doc — the operator's scout-output for
    a note-extract operation, promoted from workspace into substrate by
    NoteExtractAgent on each fire. Carries the extract_from /
    create_note / absorb_into / claims intent plus rationale prose."""
    return emit_classifier(store, extract_doc, "extract")


def emit_absorb(store: Store, absorb_doc: Address) -> Tuple[Link, bool]:
    """Classifier on an absorb spec doc — the operator's scout-output for
    a note-absorb operation, promoted from workspace into substrate by
    NoteAbsorbAgent on each fire. Carries the operator's intent
    (which extension to absorb) plus rationale prose justifying merge
    readiness."""
    return emit_classifier(store, absorb_doc, "absorb")


def emit_clone(store: Store, clone_doc: Address) -> Tuple[Link, bool]:
    """Classifier on a clone spec doc — the operator's scout-output for
    a note-clone operation, promoted from workspace into substrate by
    NoteCloneAgent on each fire. Carries the operator's intent
    (clone_from / create_note) plus rationale prose. Distinct from
    `provenance.clone`, which carries the origin → clone lineage."""
    return emit_classifier(store, clone_doc, "clone")


def emit_import(store: Store, import_doc: Address) -> Tuple[Link, bool]:
    """Classifier on an import spec doc — the operator's scout-output for
    a note-import operation, promoted from workspace into substrate by
    NoteImportAgent on each fire. Carries the operator's intent
    (source_doc / create_note / title / depends) plus rationale prose.
    Distinct from `provenance.import`, which carries the spec → new-note
    audit edge."""
    return emit_classifier(store, import_doc, "import")


def emit_campaign(store: Store, campaign_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, campaign_doc, "campaign")


def emit_review(store: Store, review_doc: Address) -> Tuple[Link, bool]:
    return emit_classifier(store, review_doc, "review")


def emit_review_content(
    store: Store, review_doc: Address,
) -> Tuple[Link, bool]:
    """Classify a review doc as content review (LLM-authored critique).

    Distinguished from review.structural so predicates can filter by
    the kind of analysis the review captures. Producers (claim_review,
    full_review, cone_review) emit this on the review docs they author.
    """
    return emit_classifier(store, review_doc, "review.content")


def emit_review_structural(
    store: Store, audit_doc: Address,
) -> Tuple[Link, bool]:
    """Classify an audit doc as structural review (validator outcomes).

    Same review.coverage shape as review.content, different working
    surface — the audit body carries validator-rule outcomes rather
    than LLM prose. Emitted by the structural-audit scout.
    """
    return emit_classifier(store, audit_doc, "review.structural")


def emit_review_coverage(
    store: Store, review_meta: Address, covered: Address,
) -> Tuple[Link, bool]:
    """Record that `covered` is within `review_meta`'s coverage.

    Idempotent on (review_meta, covered). Forms the substrate join
    between reviews and the docs they covered — read by the
    confirmation predicate today, by coverage / staleness predicates
    later. See docs/hypergraph-protocol/review-coverage.md.
    """
    return emit(
        store, "review.coverage",
        from_set=[review_meta], to_set=[covered],
    )


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
    valid = subtypes_of("promotion")
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
    (superseded, succeeding).

    Reading: walk outgoing supersession from any address to find what
    replaces it. The head version is the address with no outgoing
    supersession link.
    """
    return emit(
        store, "supersession",
        from_set=[superseded], to_set=[succeeding],
    )


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


def emit_review_mode_anti_bloat(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    """Tag a note for anti-bloat-augmented review.

    Classifier-shape link (F=∅, G=[doc]). When present, NoteReviewAgent
    appends the anti-bloat block (note_review_anti_bloat.md) to the
    standard review prompt, adding forward-reference accretion patterns
    to the reviewer's flag list. Idempotent on the active set; retract
    via `emit_retraction` to remove the tag.
    """
    return emit_classifier(store, doc, "review-mode.anti-bloat")


def emit_extends(
    store: Store, ext_note: Address, base_note: Address,
) -> Tuple[Link, bool]:
    """Declare that `ext_note` is an extension of `base_note`.

    F=[ext_note], G=[base_note]. Idempotent on (ext, base). Reverse-
    walked by find-extensions queries ("what extends ASN-NNNN?").
    """
    return emit(store, "extends", from_set=[ext_note], to_set=[base_note])


def emit_source(
    store: Store, ext_note: Address, origin_note: Address,
) -> Tuple[Link, bool]:
    """Declare that `ext_note` was extracted from `origin_note`.

    F=[ext_note], G=[origin_note]. Idempotent on (ext, origin). For an
    extension carved from multiple origins, emit one source link per
    origin.
    """
    return emit(store, "source", from_set=[ext_note], to_set=[origin_note])


def emit_transclusion(
    store: Store, transclusion_doc: Address, kind: str,
) -> Tuple[Link, bool]:
    """File a `transclusion.<kind>` runtime tag on a doc.

    Marks the doc as rendered-on-read; the kind selects which renderer
    (registered via lib/lattice/render.py) supplies content. The tag
    is a read-mechanism flag, not a structural classifier — predicates
    and substrate walks should NOT branch on its presence.
    """
    valid = subtypes_of("transclusion")
    if kind not in valid:
        raise ValueError(
            f"invalid transclusion kind {kind!r}; must be one of {sorted(valid)}"
        )
    return emit_classifier(store, transclusion_doc, f"transclusion.{kind}")


def emit_claims_statements(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    """File `claims.statements` classifier — the substrate identity of an
    ASN-level statements aggregate.

    Distinct from `transclusion.<kind>` (render-mode tag): the
    classifier announces what the doc IS (statements assembled from
    claims), independent of how its content is materialized. Cascade
    consumers cite via this identity; the version chain on the
    underlying address advances when the aggregate's content changes.
    """
    return emit_classifier(store, doc, "claims.statements")


def emit_consultation_questions(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, doc, "consultation.questions")


def emit_consultation_answer(
    store: Store, doc: Address, role: str,
) -> Tuple[Link, bool]:
    """File a `consultation.answer.<role>` classifier on a Q/A answer doc.

    role ∈ {theory, evidence} — closed set tied to the channel's
    structural role. Channel name (Nelson, Gregory, Maxwell-1867…) is
    not in substrate; it's recoverable from the campaign binding.
    Reading via the parent type `consultation.answer` matches both
    subtypes via L10 prefix-matching.
    """
    valid = {"theory", "evidence"}
    if role not in valid:
        raise ValueError(
            f"invalid consultation.answer role {role!r}; "
            f"must be one of {sorted(valid)}"
        )
    return emit_classifier(store, doc, f"consultation.answer.{role}")


def emit_consultation_assessment(
    store: Store, doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, doc, "consultation.assessment")


def emit_consultation_coverage(
    store: Store, source: Address, finding: Address,
) -> Tuple[Link, bool]:
    """Record that a consultation doc (assessment or answer) is about a
    specific finding. F=[source], G=[finding]. Idempotent on
    (source, finding). Same shape as `review.coverage`.

    Lets future predicates and queries answer "is this finding covered
    by a consultation?" and "what answers exist for this finding?"
    via substrate, instead of relying on filename conventions.
    """
    return emit(
        store, "consultation.coverage",
        from_set=[source], to_set=[finding],
    )


# ============================================================
#  Attribute links (F=[doc], G=[sidecar])
# ============================================================


def emit_attribute_link(
    store: Store, doc: Address, kind: str, sidecar: Address,
) -> Tuple[Link, bool]:
    """File an attribute link from doc to its sidecar (label, name,
    description, signature, statements). Pure substrate primitive:
    takes addresses, emits the link. Idempotent on the active-
    attribute set.
    """
    from .schema import VALID_ATTRIBUTE_KINDS
    if kind not in VALID_ATTRIBUTE_KINDS:
        raise ValueError(
            f"invalid attribute kind {kind!r}; must be one of "
            f"{sorted(VALID_ATTRIBUTE_KINDS)}"
        )
    return emit(store, kind, from_set=[doc], to_set=[sidecar])


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
    valid = subtypes_of("citation")
    if direction not in valid:
        raise ValueError(
            f"invalid citation direction {direction!r}; "
            f"must be one of {sorted(valid)}"
        )
    return emit(
        store, f"citation.{direction}",
        from_set=[citing], to_set=[cited],
    )


def emit_citation_bundle(
    store: Store,
    citing: Address,
    cited: List[Address],
    *,
    direction: str = "depends",
) -> Tuple[Link, bool]:
    """File a bundled citation link with multiple targets in to_set.

    Only valid for citation subtypes registered at FanOutPair
    (`citation.depends`). One source doc, any positive count of cited
    docs in a single tuple. Used by the cascade-anchor pattern: a
    review-N doc emits one bundled `citation.depends` recording the
    foundation heads it read.

    Empty `cited` raises (FanOutPair's `c_G = *` admits any natural
    number but emitting zero targets carries no information; callers
    should skip the emission entirely if the dep list is empty).
    """
    valid = subtypes_of("citation")
    if direction not in valid:
        raise ValueError(
            f"invalid citation direction {direction!r}; "
            f"must be one of {sorted(valid)}"
        )
    if not cited:
        raise ValueError(
            "emit_citation_bundle requires at least one cited address"
        )
    return emit(
        store, f"citation.{direction}",
        from_set=[citing], to_set=list(cited),
    )


# ============================================================
#  Retraction (F=[doc], G=[link being nullified])
# ============================================================


def emit_retraction(
    store: Store,
    by_doc: Address,
    target_link: Address,
) -> Link:
    """File a retraction link nullifying target_link.

    F=[by_doc], G=[target_link]. NOT idempotent — each retraction is
    its own fact (the shape's idempotent=False).
    """
    link, _ = emit(
        store, "retraction",
        from_set=[by_doc], to_set=[target_link],
    )
    return link


# ============================================================
#  Provenance (F=[source], G=[derived])
# ============================================================


def emit_derivation(
    store: Store, source_doc: Address, derived_doc: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.derivation` link source → derived.

    Idempotent on (source, derived).
    """
    return emit(
        store, "provenance.derivation",
        from_set=[source_doc], to_set=[derived_doc],
    )


def emit_empty_derivation(
    store: Store, source_doc: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.derivation` link from source to the empty set.

    Structural meaning: "this source was decomposed/derived-from, and
    produced no derivatives." Used by the claim_findings producer
    when a review is decomposed into zero per-finding substrate
    (CONVERGED-verdict reviews); anchors the "decompose ran" fact in
    substrate without a verb-flag classifier. Predicate
    `is_review_decomposed` reads any outbound `provenance.derivation`
    from a review, so this empty-G shape is the zero-findings
    counterpart to the non-zero F=[source], G=[derived] shape.

    Idempotent on (source, ∅) — re-emit returns the existing link.
    """
    return emit(
        store, "provenance.derivation",
        from_set=[source_doc], to_set=[],
    )


def emit_provenance_clone(
    store: Store, origin_note: Address, clone_note: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.clone` link from origin to clone.

    Records that `clone_note` is a whole-note copy of `origin_note`.
    Idempotent on (origin, clone). Used by note-clone for cheap
    experiments that preserve the origin's expensive consultation
    on the new ASN.

    Distinct from `emit_clone`, which is the spec-doc classifier
    helper.
    """
    return emit(
        store, "provenance.clone",
        from_set=[origin_note], to_set=[clone_note],
    )


def emit_provenance_extract(
    store: Store, extract_doc: Address, new_note: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.extract` link from the extract spec doc to the
    new note it produced. Records the audit fact: this extract operation
    (described by spec_doc) produced this new note.

    Idempotent on (spec_doc, new_note). Pairs with the `extract`
    classifier on the spec doc; together they make the operator's
    scout-output and the producer's identity grant a closed audit
    trail.
    """
    return emit(
        store, "provenance.extract",
        from_set=[extract_doc], to_set=[new_note],
    )


def emit_provenance_import(
    store: Store, import_doc: Address, new_note: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.import` link from the import spec doc to the
    new note it produced. Records the audit fact: this import operation
    (described by spec_doc) lifted an external doc into the note set
    as this new note.

    The source doc itself stays in place outside the docuverse and is
    NOT registered in substrate — its path is recorded only in the
    spec doc's frontmatter `source_doc:` field.

    Idempotent on (spec_doc, new_note). Pairs with the `import`
    classifier on the spec doc.
    """
    return emit(
        store, "provenance.import",
        from_set=[import_doc], to_set=[new_note],
    )


def emit_provenance_absorb(
    store: Store, absorb_doc: Address, base_note: Address,
) -> Tuple[Link, bool]:
    """File a `provenance.absorb` link from the absorb spec doc to the
    base note it merged content into. Records the audit fact: this
    absorb operation (described by spec_doc) integrated extension
    material into this base.

    Idempotent on (spec_doc, base_note). Pairs with the `absorb`
    classifier on the spec doc; together they close the audit trail
    of operator intent → integration outcome.
    """
    return emit(
        store, "provenance.absorb",
        from_set=[absorb_doc], to_set=[base_note],
    )


def emit_synthesis(
    store: Store, inquiry_doc: Address, note_doc: Address,
) -> Tuple[Link, bool]:
    return emit(
        store, "provenance.synthesis",
        from_set=[inquiry_doc], to_set=[note_doc],
    )


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
    independent facts). The shape's idempotent=False ensures the
    generic emit() always writes a fresh link.
    """
    valid = subtypes_of("comment")
    if kind not in valid:
        raise ValueError(
            f"invalid comment kind {kind!r}; must be one of {sorted(valid)}"
        )
    link, _ = emit(
        store, f"comment.{kind}",
        from_set=[review_doc], to_set=[target_doc],
    )
    return link


def emit_resolution(
    store: Store,
    by_doc: Address,
    comment: Address,
    *,
    kind: str = "edit",
) -> Link:
    """File a resolution.<kind> link closing a comment.

    F=[by_doc], G=[comment_link_addr]. Self-referential (G targets a
    link). NOT idempotent — each closure is its own fact.
    """
    valid = subtypes_of("resolution")
    if kind not in valid:
        raise ValueError(
            f"invalid resolution kind {kind!r}; must be one of {sorted(valid)}"
        )
    link, _ = emit(
        store, f"resolution.{kind}",
        from_set=[by_doc], to_set=[comment],
    )
    return link


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
    fresh manages emission marking who's responsible for it. The
    shape's idempotent=False ensures the generic emit() always
    writes a fresh link.
    """
    link, _ = emit(
        store, "manages",
        from_set=[agent_doc], to_set=[operation_link],
    )
    return link


# ============================================================
#  Coordination (repellent pheromone / advisory lock)
# ============================================================


def emit_holding(
    store: Store, agent_doc: Address, resource: Address,
) -> Link:
    """File a `holding` link from `agent_doc` to `resource`.

    Repellent-pheromone semantic: agent declares "I am currently
    working on this resource, stay out." Other agents check via
    `is_held` (or extended quiescence predicates) and yield.

    Closed by retraction at fire end. NOT idempotent — each fire is
    a distinct hold; the shape's idempotent=False ensures the generic
    emit() writes a fresh link every call.

    See docs/design-notes/stigmergic-coordination.md.
    """
    link, _ = emit(
        store, "holding",
        from_set=[agent_doc], to_set=[resource],
    )
    return link


def emit_agent_scope(
    store: Store, agent_doc: Address, scope_type: str,
) -> Tuple[Link, bool]:
    """Classify an agent doc with its hold-scope declaration.

    `scope_type` is one of `"note"`, `"claim"`, `"inquiry"`,
    `"lattice"`. The classifier subtype (`agent.scope.<type>`) is filed
    on the agent doc; the agent base class reads this at fire time to
    decide what resource to hold.

    Idempotent — re-classifying with the same scope is a no-op.
    """
    if scope_type not in {"note", "claim", "inquiry", "lattice"}:
        raise ValueError(
            f"unknown scope_type {scope_type!r}; "
            f"must be one of 'note', 'claim', 'inquiry', 'lattice'"
        )
    return emit_classifier(store, agent_doc, f"agent.scope.{scope_type}")


def emit_agent_caste(
    store: Store, agent_doc: Address, caste: str,
) -> Tuple[Link, bool]:
    """Classify an agent doc with its caste declaration.

    `caste` is one of `"producer"`, `"refiner"`, `"scout"`, or
    `"worker"`. The classifier subtype (`agent.caste.<value>`) is
    filed on the agent doc; predicates and tooling that filter agents
    by caste read this from substrate.

    Idempotent — re-classifying with the same caste is a no-op.
    """
    if caste not in {"producer", "refiner", "scout", "worker"}:
        raise ValueError(
            f"unknown caste {caste!r}; "
            f"must be one of 'producer', 'refiner', 'scout', 'worker'"
        )
    return emit_classifier(store, agent_doc, f"agent.caste.{caste}")



# ============================================================
#  Notation (lattice-wide singleton)
# ============================================================


def emit_notation(
    store: Store, notation_doc: Address,
) -> Tuple[Link, bool]:
    return emit_classifier(store, notation_doc, "notation")
