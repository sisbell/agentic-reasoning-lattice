"""Canonical link-type registry (per docs/hypergraph-protocol/link-types.md).

Per ASN-0043 L8 (TypeByAddress), every link's type endset is a set of
addresses pointing into a registry document. Subtype hierarchies are
recoverable by tumbler-prefix matching (L10).

Each type has a canonical position in the registry doc's link
subspace. The structural prefix is `<registry-doc>.1.0.2`:
  - <registry-doc> — the registry doc address (zeros=2)
  - .1            — first version of that doc (extends doc field)
  - .0            — separator into element field
  - .2            — link subspace identifier (s_L)
A type's full address appends its position digits to that prefix.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .addressing import Address

# Canonical leaf-type positions (relative to the registry-doc + .1.0.2 prefix).
# Source: docs/hypergraph-protocol/link-types.md §4.
CANONICAL_POSITIONS: Dict[str, Tuple[int, ...]] = {
    "claim": (1,),
    "contract.axiom": (2, 1),
    "contract.corollary": (2, 2),
    "contract.definition": (2, 3),
    "contract.design-requirement": (2, 4),
    "contract.lemma": (2, 5),
    "contract.theorem": (2, 6),
    "inquiry": (3,),
    "note": (4,),
    "campaign": (5,),
    "agent": (6,),
    "finding": (7,),
    "review": (8,),
    "review.coverage": (8, 1),
    "review.content": (8, 2),
    "review.structural": (8, 3),
    "signature": (9,),
    "notation": (10,),
    "consultation.questions": (11, 1),
    "consultation.assessment": (11, 2),
    "consultation.answer.theory": (11, 3, 1),
    "consultation.answer.evidence": (11, 3, 2),
    "consultation.coverage": (11, 4),
    "name": (12,),
    "label": (13,),
    "description": (14,),
    "citation.depends": (15, 1),
    "citation.forward": (15, 2),
    "citation.resolve": (15, 3),
    "comment.observe": (16, 1),
    "comment.revise": (16, 2),
    "comment.out-of-scope": (16, 3),
    "comment.violation": (16, 4),
    "resolution.edit": (17, 1),
    "resolution.reject": (17, 2),
    "retraction": (18,),
    "provenance.derivation": (19, 1),
    "provenance.synthesis": (19, 2),
    "provenance.clone": (19, 3),
    "manages": (20,),
    "lattice": (21,),
    "transclusion.claim-statements": (22, 1),
    "supersession": (23,),
    "statements": (24,),
    "retired": (25,),
    "extends": (26,),
    "source": (27,),
    "promotion.out-of-scope": (28, 1),
    "promotion.open-questions": (28, 2),
    "references": (29,),
    "patch.note": (30, 1),
    "patch.claim": (30, 2),
    "extract": (31,),
    "absorb": (32,),
    "clone": (33,),
    "claims.statements": (34, 1),
    "holding": (35,),
    "agent.scope.note": (6, 1, 1),
    "agent.scope.claim": (6, 1, 2),
    "agent.scope.inquiry": (6, 1, 3),
}

# Parent-type positions for hierarchical queries (per L10): a query at
# the parent address matches every subtype that extends it.
PARENT_TYPES: Dict[str, Tuple[int, ...]] = {
    "contract": (2,),
    "consultation": (11,),
    "consultation.answer": (11, 3),  # parent of role-bearing subtypes;
                                     # also the address of legacy bare
                                     # answer links
    "citation": (15,),
    "comment": (16,),
    "resolution": (17,),
    "provenance": (19,),
    "transclusion": (22,),
    "promotion": (28,),
    "patch": (30,),
    "claims": (34,),
    "agent.scope": (6, 1),
}

# Types whose endset shape is Classifier (F=∅, G=[doc]). When State.create_doc
# is called with one of these as `kind`, it emits the corresponding classifier
# link. Source: link-types.md §3.
CLASSIFIER_TYPES: frozenset = frozenset({
    "claim",
    "contract.axiom",
    "contract.corollary",
    "contract.definition",
    "contract.design-requirement",
    "contract.lemma",
    "contract.theorem",
    "inquiry",
    "note",
    "campaign",
    "agent",
    "finding",
    "review",
    "review.content",
    "review.structural",
    "notation",
    "consultation.questions",
    "consultation.assessment",
    "consultation.answer",
    "transclusion.claim-statements",
    "promotion.out-of-scope",
    "promotion.open-questions",
    "patch.note",
    "patch.claim",
    "extract",
    "absorb",
    "clone",
    "claims.statements",
    "agent.scope.note",
    "agent.scope.claim",
    "agent.scope.inquiry",
})


def _structural_prefix(registry_doc: Address) -> Tuple[int, ...]:
    """Per link-types.md §4: <registry-doc>.1.0.2."""
    return registry_doc.digits + (1, 0, 2)


class TypeRegistry:
    """Resolves type names to/from tumbler addresses anchored at a
    designated registry document.

    Type addresses are computed from CANONICAL_POSITIONS / PARENT_TYPES;
    the registry doesn't itself allocate them — per L9 (TypeGhostPermission)
    type addresses can be ghosts. This class is the coordination point
    that fixes which name maps to which position.
    """

    def __init__(self, registry_doc: Address) -> None:
        self.registry_doc = registry_doc
        self._prefix = _structural_prefix(registry_doc)
        self._addr_to_name: Dict[Address, str] = {}
        for name, position in CANONICAL_POSITIONS.items():
            self._addr_to_name[self._build(position)] = name
        for name, position in PARENT_TYPES.items():
            self._addr_to_name[self._build(position)] = name

    def _build(self, position: Tuple[int, ...]) -> Address:
        return Address(self._prefix + position)

    def address_for(self, name: str) -> Address:
        if name in CANONICAL_POSITIONS:
            return self._build(CANONICAL_POSITIONS[name])
        if name in PARENT_TYPES:
            return self._build(PARENT_TYPES[name])
        raise KeyError(f"unknown link type: {name!r}")

    def name_for(self, addr: Address) -> Optional[str]:
        return self._addr_to_name.get(addr)

    def is_known(self, name: str) -> bool:
        return name in CANONICAL_POSITIONS or name in PARENT_TYPES
