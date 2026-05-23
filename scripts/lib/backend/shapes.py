"""Link-shape registry — the substrate's alphabet.

Each link type has a fixed F/G cardinality convention. This module
declares those conventions in one place: a per-type mapping to a
LinkShape that records F-cardinality, G-cardinality, what G targets
(a doc address or a link address), and whether emissions are
idempotent at the active-set level.

The registry is what makes the substrate function as a predicate
language. Predicate signatures match link signatures by reading
this table; idempotency is well-defined because the existence
test for any link is templated by its shape; self-reference
(g_targets="link") is what enables retraction and resolution to
flip predicates without overwriting prior facts.

See docs/v2/predicate-substrate.md for the principles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class LinkShape:
    """Cardinality and target conventions for one family of links.

    Fields:
      f_cardinality: "empty" | "one"
      g_cardinality: "empty" | "one" | "one_or_empty" | "many"
                     "many" admits any finite count (including 1), the
                     code-side encoding of ASN-0094's `*` cardinality.
                     `citation.depends` registers at the FanOutPair
                     shape `(1, *, A_doc, A_doc, ⊤)` to carry bundled
                     multi-target emissions; legacy single-target
                     emissions remain admissible since cardinality 1
                     matches `many`.
      g_targets:     "doc" | "link"  (whether G addresses a doc or a link)
      idempotent:    True if a structurally-equivalent active link
                     causes a re-emit to no-op; False if every emit
                     creates a fresh fact (comment, resolution,
                     retraction, manages).
    """
    f_cardinality: str
    g_cardinality: str
    g_targets: str = "doc"
    idempotent: bool = True


# ─── Shape families ────────────────────────────────────────────────

# Classifier — F=∅, G=[doc]. The category-membership pattern.
CLASSIFIER = LinkShape("empty", "one")

# Attribute — F=[doc], G=[sidecar]. Doc-attached metadata documents.
ATTRIBUTE = LinkShape("one", "one")

# Citation — F=[citing], G=[cited]. Directed dep/forward/resolve.
CITATION = LinkShape("one", "one")

# FanOutPair — F=[citing], G=[cited1, cited2, ...]. ASN-0094's `(1, *,
# A_doc, A_doc, ⊤)` row. One source doc, any finite count of target
# docs in a single tuple. Registered K: `citation.depends`. Legacy
# single-target emissions remain admissible (cardinality 1 matches
# "many"). Used by the cascade-anchor pattern: each review-N doc emits
# one bundled `citation.depends` to the foundation heads it read, and
# the cascade-fresh predicate walks that link's to_set checking
# `is_head_version` per target.
FAN_OUT = LinkShape("one", "many")

# Coverage — F=[meta], G=[covered]. "Meta doc audited covered doc."
COVERAGE = LinkShape("one", "one")

# Comment — F=[review], G=[target]. NOT idempotent: each review cycle's
# comments are independent facts even when targeting the same doc.
COMMENT = LinkShape("one", "one", idempotent=False)

# Resolution — F=[by_doc], G=[comment_link]. Self-referential (G
# targets a link). NOT idempotent: each closure is its own fact.
RESOLUTION = LinkShape("one", "one", g_targets="link", idempotent=False)

# Retraction — F=[by_doc], G=[target_link]. Self-referential. NOT
# idempotent: each retraction is its own fact.
RETRACTION = LinkShape("one", "one", g_targets="link", idempotent=False)

# Provenance — F=[source], G=[derived] OR G=∅ (empty derivation
# anchor). Idempotent on (F, G).
PROVENANCE = LinkShape("one", "one_or_empty")

# Supersession — F=[old_version], G=[new_version].
SUPERSESSION = LinkShape("one", "one")

# Extends — F=[ext_note], G=[base_note].
EXTENDS = LinkShape("one", "one")

# Source — F=[ext_note], G=[origin_note].
SOURCE = LinkShape("one", "one")

# Manages — F=[agent], G=[operation_link]. Self-referential. NOT
# idempotent: each operation gets its own fresh manages emission.
MANAGES = LinkShape("one", "one", g_targets="link", idempotent=False)

# Holding — F=[agent_doc], G=[resource_addr]. The repellent-pheromone
# coordination signal: agent declares "I am currently working on this
# resource, stay out." Closed by retraction at fire end. NOT
# idempotent: each fire is a distinct hold; predicate semantics depend
# on per-fire emission identity. See docs/design-notes/stigmergic-coordination.md.
HOLDING = LinkShape("one", "one", g_targets="doc", idempotent=False)


# ─── Concrete-type → shape mapping ─────────────────────────────────
# Every type declared in lib/backend/types.py CANONICAL_POSITIONS
# (and PARENT_TYPES, where parent types have no direct emit but
# subtypes inherit the shape) must have an entry here.

SHAPES: Dict[str, LinkShape] = {
    # ── Classifiers ──
    "claim": CLASSIFIER,
    "contract.axiom": CLASSIFIER,
    "contract.corollary": CLASSIFIER,
    "contract.definition": CLASSIFIER,
    "contract.design-requirement": CLASSIFIER,
    "contract.lemma": CLASSIFIER,
    "contract.theorem": CLASSIFIER,
    "inquiry": CLASSIFIER,
    "note": CLASSIFIER,
    "campaign": CLASSIFIER,
    "agent": CLASSIFIER,
    "finding": CLASSIFIER,
    "review": CLASSIFIER,
    "review.content": CLASSIFIER,
    "review.structural": CLASSIFIER,
    "notation": CLASSIFIER,
    "consultation.questions": CLASSIFIER,
    "consultation.assessment": CLASSIFIER,
    "consultation.answer.theory": CLASSIFIER,
    "consultation.answer.evidence": CLASSIFIER,
    "transclusion.claim-statements": CLASSIFIER,
    "claims.statements": CLASSIFIER,
    "agent.scope.note": CLASSIFIER,
    "agent.scope.claim": CLASSIFIER,
    "agent.scope.inquiry": CLASSIFIER,
    "agent.scope.lattice": CLASSIFIER,
    "agent.caste.producer": CLASSIFIER,
    "agent.caste.refiner": CLASSIFIER,
    "agent.caste.scout": CLASSIFIER,
    "agent.caste.worker": CLASSIFIER,
    "promotion.out-of-scope": CLASSIFIER,
    "promotion.open-questions": CLASSIFIER,
    "patch.note": CLASSIFIER,
    "patch.claim": CLASSIFIER,
    "extract": CLASSIFIER,
    "absorb": CLASSIFIER,
    "clone": CLASSIFIER,
    "import": CLASSIFIER,
    "retired": CLASSIFIER,
    "review-mode.anti-bloat": CLASSIFIER,
    "motifs": CLASSIFIER,
    "motif": CLASSIFIER,

    # ── Attributes ──
    "name": ATTRIBUTE,
    "label": ATTRIBUTE,
    "description": ATTRIBUTE,
    "signature": ATTRIBUTE,
    "statements": ATTRIBUTE,
    "references": ATTRIBUTE,
    "motif.attribution": ATTRIBUTE,

    # ── Citations ──
    "citation.depends": FAN_OUT,
    "citation.forward": CITATION,
    "citation.resolve": CITATION,

    # ── Comments (non-idempotent) ──
    "comment.observe": COMMENT,
    "comment.revise": COMMENT,
    "comment.out-of-scope": COMMENT,
    "comment.violation": COMMENT,

    # ── Resolutions (self-ref, non-idempotent) ──
    "resolution.edit": RESOLUTION,
    "resolution.reject": RESOLUTION,

    # ── Coverage ──
    "review.coverage": COVERAGE,
    "consultation.coverage": COVERAGE,

    # ── Provenance ──
    "provenance.derivation": PROVENANCE,
    "provenance.synthesis": PROVENANCE,
    "provenance.clone": PROVENANCE,
    "provenance.extract": PROVENANCE,
    "provenance.absorb": PROVENANCE,
    "provenance.import": PROVENANCE,

    # ── Versioning + lineage ──
    "supersession": SUPERSESSION,
    "extends": EXTENDS,
    "source": SOURCE,

    # ── Self-ref non-idempotent ──
    "retraction": RETRACTION,
    "manages": MANAGES,

    # ── Coordination (repellent pheromone / advisory lock) ──
    "holding": HOLDING,

    # ── Membership ──
    "lattice": CLASSIFIER,  # F=∅, G=[doc] for lattice membership
}


# ─── Lookup ────────────────────────────────────────────────────────


def shape_for(type_: str) -> LinkShape:
    """Return the shape for a concrete link type.

    Raises ValueError if the type is not registered. For known
    queryable parents that need a subtype (e.g., bare `citation`
    when only `citation.depends` etc. are emittable), the error
    message lists the valid subtypes.
    """
    if type_ in SHAPES:
        return SHAPES[type_]

    from .types import PARENT_TYPES
    if type_ in PARENT_TYPES and subtypes_of(type_):
        valid = sorted(subtypes_of(type_))
        raise ValueError(
            f"type {type_!r} requires a subtype "
            f"(one of: {', '.join(f'{type_}.{s}' for s in valid)})"
        )

    if "." in type_:
        parent, sub = type_.split(".", 1)
        if parent in SHAPES or parent in PARENT_TYPES:
            raise ValueError(
                f"unknown subtype {sub!r} for parent {parent!r}"
            )

    raise ValueError(
        f"unknown link type: {type_!r} "
        f"(register in lib/backend/shapes.py)"
    )


# ─── Type-set queries derived from SHAPES + PARENT_TYPES ───────────


def subtypes_of(parent: str) -> frozenset:
    """Subtype suffixes for a parent type.

    Returns the set of suffix strings such that `parent.<suffix>` is a
    registered concrete type. Empty if `parent` has no subtyped
    concretes (a bare-only parent like `note` returns an empty set).
    """
    prefix = f"{parent}."
    return frozenset(
        type_[len(prefix):]
        for type_ in SHAPES
        if type_.startswith(prefix)
    )


def validate_type(type_: str) -> None:
    """Raise ValueError if `type_` is not a known type.

    Accepts:
      - concrete types registered in SHAPES (e.g., `claim`,
        `citation.depends`, `consultation.answer.theory`)
      - queryable parents in PARENT_TYPES (e.g., `citation`,
        `consultation.answer`) — usable in queries via L10
        prefix-matching even though they're not directly emittable
    """
    if type_ in SHAPES:
        return

    from .types import PARENT_TYPES
    if type_ in PARENT_TYPES:
        return  # queryable parent

    if "." in type_:
        parent, sub = type_.split(".", 1)
        if parent in SHAPES or parent in PARENT_TYPES:
            raise ValueError(
                f"unknown subtype {sub!r} for parent {parent!r}"
            )

    raise ValueError(f"unknown type: {type_!r}")
