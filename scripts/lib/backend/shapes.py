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
      g_cardinality: "empty" | "one" | "one_or_empty"
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
    "promotion.out-of-scope": CLASSIFIER,
    "promotion.open-questions": CLASSIFIER,
    "patch.note": CLASSIFIER,
    "patch.claim": CLASSIFIER,
    "extract": CLASSIFIER,
    "absorb": CLASSIFIER,
    "clone": CLASSIFIER,
    "retired": CLASSIFIER,

    # ── Attributes ──
    "name": ATTRIBUTE,
    "label": ATTRIBUTE,
    "description": ATTRIBUTE,
    "signature": ATTRIBUTE,
    "statements": ATTRIBUTE,
    "references": ATTRIBUTE,

    # ── Citations ──
    "citation.depends": CITATION,
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

    # ── Versioning + lineage ──
    "supersession": SUPERSESSION,
    "extends": EXTENDS,
    "source": SOURCE,

    # ── Self-ref non-idempotent ──
    "retraction": RETRACTION,
    "manages": MANAGES,

    # ── Membership ──
    "lattice": CLASSIFIER,  # F=∅, G=[doc] for lattice membership
}


# ─── Lookup ────────────────────────────────────────────────────────


def shape_for(type_: str) -> LinkShape:
    """Return the shape for a concrete link type.

    Raises KeyError if the type is not registered. Subtyped names
    must be registered as concrete entries (e.g., `citation.depends`,
    not bare `citation`).
    """
    try:
        return SHAPES[type_]
    except KeyError:
        raise KeyError(
            f"unknown link type: {type_!r} "
            f"(register in lib/backend/shapes.py)"
        )
