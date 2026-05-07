"""Predicate factory — templated predicate generators per link shape.

Most atomic predicates are templates parameterized by a link kind:
`has_<attr>(doc)` for any attribute kind, `is_<classifier>(doc)` for
any classifier kind, etc. The shape registry already declares these
kinds; this module turns each shape's pattern into a generator that
emits the canonical predicate function.

Composite predicates (is_doc_quiescent, is_claim_confirmed, etc.)
stay hand-written — they read multiple link types and apply
non-trivial logic. The factory targets only the one-link, one-shape
existence/lookup/freshness templates.

See docs/v2/predicate-substrate.md for the principles behind shape-
parameterized predicates.
"""

from __future__ import annotations

from typing import Callable, Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


# ─── Classifier predicates ─────────────────────────────────────────


def is_classifier(kind: str) -> Callable[[Session, Address], bool]:
    """Generate `is_<kind>(doc)` for a classifier-shape link kind.

    Returns True iff an active classifier of `kind` targets `doc`.
    Equivalent to `bool(session.active_links(kind, to_set=[doc]))`.
    """
    def predicate(session: Session, doc_addr: Address) -> bool:
        return bool(session.active_links(kind, to_set=[doc_addr]))
    predicate.__name__ = f"is_{kind.replace('.', '_')}"
    predicate.__doc__ = (
        f"True iff `doc` has an active `{kind}` classifier link."
    )
    return predicate


# ─── Attribute predicates ──────────────────────────────────────────


def has_attribute(kind: str) -> Callable[[Session, Address], bool]:
    """Generate `has_<kind>(doc)` for an attribute-shape link kind.

    Returns True iff `doc` is the F of an active `kind` attribute
    link. Equivalent to `bool(session.active_links(kind,
    from_set=[doc]))`.
    """
    def predicate(session: Session, doc_addr: Address) -> bool:
        return bool(session.active_links(kind, from_set=[doc_addr]))
    predicate.__name__ = f"has_{kind}"
    predicate.__doc__ = (
        f"True iff `doc` has an active `{kind}` attribute link."
    )
    return predicate


def attribute_sidecar(
    kind: str,
) -> Callable[[Session, Address], Optional[Address]]:
    """Generate `<kind>_sidecar_of(doc)` lookup.

    Returns the sidecar address attached to `doc` via the `kind`
    attribute link, or None. If multiple active links exist (rare),
    returns the first by sibling order.
    """
    def lookup(session: Session, doc_addr: Address) -> Optional[Address]:
        links = session.active_links(kind, from_set=[doc_addr])
        for link in links:
            if link.to_set:
                return link.to_set[0]
        return None
    lookup.__name__ = f"{kind}_sidecar_of"
    lookup.__doc__ = (
        f"The `{kind}` sidecar address for `doc`, or None."
    )
    return lookup


def attribute_is_fresh(
    kind: str,
    *,
    confirmation_gate: bool = False,
) -> Callable[[Session, Address], bool]:
    """Generate `<kind>_is_fresh(doc)` chain-comparison predicate.

    True iff the `kind` sidecar's supersession chain is at least as
    long as `doc`'s chain. False when no sidecar exists (initial
    state) — the corresponding producer should fire to create it.

    `confirmation_gate=True` adds a precondition: if the doc is not
    yet confirmed (still in revise cycles), report fresh and skip
    re-fire. Used by `statements_is_fresh` to avoid extracting
    statements mid-refinement.
    """
    sidecar_lookup = attribute_sidecar(kind)

    def predicate(session: Session, doc_addr: Address) -> bool:
        if confirmation_gate:
            from lib.predicates.quiescence import is_claim_confirmed
            if not is_claim_confirmed(session, doc_addr):
                return True

        from lib.predicates.versions import supersession_chain_length
        sidecar_addr = sidecar_lookup(session, doc_addr)
        if sidecar_addr is None:
            return False
        return (
            supersession_chain_length(session, sidecar_addr)
            >= supersession_chain_length(session, doc_addr)
        )

    predicate.__name__ = f"{kind}_is_fresh"
    gate = " (with confirmation gate)" if confirmation_gate else ""
    predicate.__doc__ = (
        f"True iff `{kind}` sidecar's chain ≥ doc's chain{gate}."
    )
    return predicate


# ─── Citation predicates ───────────────────────────────────────────


def citation_outgoing(
    direction: str,
) -> Callable[[Session, Address], list]:
    """Generate `<direction>(doc)` — docs `doc` cites via citation.<direction>.

    Returns a sorted list of cited addresses. Retracted citations
    drop from the result automatically.
    """
    type_str = f"citation.{direction}"

    def lookup(session: Session, doc_addr: Address) -> list:
        out = set()
        for link in session.active_links(type_str, from_set=[doc_addr]):
            out.update(link.to_set)
        return sorted(out, key=lambda a: a.digits)

    lookup.__name__ = direction
    lookup.__doc__ = (
        f"Docs `doc` cites via `citation.{direction}` (active set)."
    )
    return lookup


def citation_incoming(
    direction: str,
) -> Callable[[Session, Address], list]:
    """Generate the reverse — docs that cite `doc` via citation.<direction>.

    Returns a sorted list of citing addresses.
    """
    type_str = f"citation.{direction}"

    def lookup(session: Session, doc_addr: Address) -> list:
        out = set()
        for link in session.active_links(type_str, to_set=[doc_addr]):
            out.update(link.from_set)
        return sorted(out, key=lambda a: a.digits)

    lookup.__name__ = f"{direction}_incoming"
    lookup.__doc__ = (
        f"Docs that cite `doc` via `citation.{direction}` (active set)."
    )
    return lookup
