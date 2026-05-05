"""Schema constants — types, subtypes, validation, file suffixes.

Mirrors `scripts/lib/store/schema.py` for the tumbler substrate.
The constants describe the catalog at the SCHEMA level (string
identifiers); the type *addresses* live in TypeRegistry.
"""

from __future__ import annotations

VALID_TYPES = frozenset({
    # Protocol-defined doc kinds
    "claim", "note", "review", "finding",
    "contract", "citation", "comment", "resolution",
    # Discovery / consultation
    "inquiry", "campaign", "consultation",
    # Provenance — operation-produced-output audit links
    "provenance",
    # Substrate-owned (general-purpose document primitives)
    "retraction", "label", "name", "description", "signature", "notation",
    "statements",
    # Agent module
    "agent", "manages",
    # Lattice membership relation (added in spec-faithful refactor)
    "lattice",
    # Transclusion — runtime tag (NOT a structural classifier) marking
    # a doc whose content is rendered by a registered Python function
    # at read time. Native to Xanadu's protocol there; here it's a
    # read-mechanism flag, not a substrate predicate target. Always
    # carries a sub-kind.
    "transclusion",
    # Supersession — version-replacement declaration (per LM 4/52-4/53).
    # F=[old_version], G=[new_version]. Reading: walk outgoing supersession
    # from any address to find what replaces it; head = no outgoing
    # supersession link.
    "supersession",
    # Retired — lifecycle marker on a doc. Classifier-shape (F=∅, G=[doc]).
    # Presence = doc is retired (out of active lattice). Retraction
    # revives. State transitions are real substrate facts; no toggling.
    "retired",
    # Extension lineage — directional link between two notes.
    # extends: F=[ext_note], G=[base_note]. The new ASN extends the base
    # (builds on top of it; base claims are foundation for ext claims).
    # source: F=[ext_note], G=[origin_note(s)]. The new ASN's claims were
    # extracted from the origin note(s) during a maturation operation.
    "extends",
    "source",
    # Promotion — classifier on a report doc that records the LLM's
    # promote/decline decisions for a source ASN. Always carries a
    # subtype distinguishing the input flow:
    #   promotion.out-of-scope   — OUT_OF_SCOPE sections from reviews
    #   promotion.open-questions — Open Questions section in the note
    "promotion",
})

VALID_SUBTYPES = {
    "contract": frozenset({
        "axiom", "definition", "theorem", "corollary", "lemma",
        "consequence", "design-requirement",
    }),
    "comment": frozenset({"revise", "observe", "out-of-scope"}),
    "resolution": frozenset({"edit", "reject"}),
    "citation": frozenset({"depends", "forward", "resolve"}),
    "consultation": frozenset({"questions", "answer", "assessment"}),
    "provenance": frozenset({
        "synthesis",   # consultation: inquiry → note
        "derivation",  # decomposition: note → claim, aggregate-review → finding
        "extract",     # maturation: existing notes → new foundation
        "absorb",      # maturation: note A material → note B
        "reset",       # maturation: hard-reset cascade marker
    }),
    "review": frozenset({
        "coverage",  # review meta → covered doc; structural audit fact:
                     # this doc was within this review's coverage. Used by
                     # is_claim_confirmed and future coverage / staleness
                     # predicates.
    }),
    "transclusion": frozenset({
        "claim-statements",  # per-ASN assembled view of derived claims
                             # + their descriptions; rendered live from
                             # substrate state.
    }),
    "promotion": frozenset({"out-of-scope", "open-questions"}),
}

# Types that must always carry a subtype — bare parent writes are invalid.
REQUIRES_SUBTYPE = frozenset({"citation", "transclusion", "promotion"})

# File suffixes for attribute sidecars (used by file-walking helpers
# that distinguish claim body markdown from sidecars).
VALID_ATTRIBUTE_KINDS = frozenset({
    "label", "name", "description", "signature", "statements",
})
ATTRIBUTE_SUFFIXES = tuple(f".{k}.md" for k in sorted(VALID_ATTRIBUTE_KINDS))


def validate_type(type_str: str) -> None:
    """Raise ValueError if type_str is not a known parent or parent.subtype."""
    if "." in type_str:
        parent, sub = type_str.split(".", 1)
        if parent not in VALID_TYPES:
            raise ValueError(f"unknown parent type: {parent!r}")
        valid_subs = VALID_SUBTYPES.get(parent, frozenset())
        if sub not in valid_subs:
            raise ValueError(f"unknown subtype {sub!r} for parent {parent!r}")
    else:
        if type_str not in VALID_TYPES:
            raise ValueError(f"unknown type: {type_str!r}")
        if type_str in REQUIRES_SUBTYPE:
            valid = sorted(VALID_SUBTYPES.get(type_str, frozenset()))
            raise ValueError(
                f"type {type_str!r} requires a subtype "
                f"(one of: {', '.join(f'{type_str}.{s}' for s in valid)})"
            )
