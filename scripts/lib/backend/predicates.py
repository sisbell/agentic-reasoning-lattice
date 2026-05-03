"""Substrate predicates over the tumbler-keyed link store.

Read-only logic over `State.find_links`. Ported from the legacy
`scripts/lib/store/queries.py` with one substantive change: identity
is by tumbler address (`Address`), not filesystem path string.

## The convergence predicate (per docs/protocols/claim-convergence-protocol.md)

    For every document with a `claim` classifier, every active
    `comment.revise` link targeting that claim has a matching active
    `resolution` link.

A link is *active* if no `retraction` link nullifies it. Retracted
revises drop out of the predicate; retracted resolutions stop
satisfying it. Predicates here implement that protocol over the new
substrate.

## Alignment predicates

Version-bearing addresses (VER3) make alignment questions like "does
the head version of claim D have an active description link?" reduce
to a single substrate query: `find_links(from_set=[head], type_="description")`.
When the claim revises (D → D.1), the existing description link still
points at D — the predicate returns False for D.1 until claim-describe
runs against it.
"""

from __future__ import annotations

from typing import List, Optional, Set

from .addressing import Address
from .links import Link
from .state import State


# ============================================================
#  active-vs-retracted helpers
# ============================================================


def retracted_link_addrs(state: State) -> Set[Address]:
    """Set of link addresses that have been retracted.

    A retraction is a `retraction`-typed link whose to_set contains
    the address of the link being nullified.
    """
    out: Set[Address] = set()
    for r in state.find_links(type_="retraction"):
        out.update(r.to_set)
    return out


def active_links(
    state: State,
    type_: str,
    from_set: Optional[List[Address]] = None,
    to_set: Optional[List[Address]] = None,
) -> List[Link]:
    """Links of the given type whose addresses haven't been retracted."""
    retracted = retracted_link_addrs(state)
    candidates = state.find_links(from_set=from_set, to_set=to_set, type_=type_)
    return [link for link in candidates if link.addr not in retracted]


# ============================================================
#  convergence predicates (load-bearing for the protocol)
# ============================================================


def has_resolution(
    state: State,
    comment_addr: Address,
    *,
    _retracted: Optional[Set[Address]] = None,
) -> bool:
    """True iff at least one active `resolution` link targets this comment.

    Substrate convention (matches legacy and migrated data): the
    resolution link has `from_set=[revised_doc]`, `to_set=[comment_addr]`.
    The catalog's stated F/G order is the opposite — to be reconciled
    later; this predicate matches the data we actually have.

    `_retracted` is an optional pre-computed set of retracted link
    addresses; callers iterating over many comments pass it once to
    avoid re-querying.
    """
    retracted = retracted_link_addrs(state) if _retracted is None else _retracted
    for r in state.find_links(to_set=[comment_addr], type_="resolution"):
        if r.addr not in retracted:
            return True
    return False


def unresolved_revise_comments(
    state: State,
    doc_addr: Optional[Address] = None,
) -> List[Link]:
    """Every active `comment.revise` link without an active resolution.

    Retracted revises are excluded (the retraction nullifies the
    complaint). A resolution that has itself been retracted does not
    satisfy the predicate. If `doc_addr` is given, scopes to comments
    targeting that doc; otherwise spans the whole substrate.

    This is the load-bearing predicate for the convergence model —
    every "is the lattice done?" question reduces to this set being
    empty over the appropriate scope.
    """
    retracted = retracted_link_addrs(state)
    revises = state.find_links(
        to_set=[doc_addr] if doc_addr is not None else None,
        type_="comment.revise",
    )
    return [
        c for c in revises
        if c.addr not in retracted
        and not has_resolution(state, c.addr, _retracted=retracted)
    ]


def is_doc_converged(state: State, doc_addr: Address) -> bool:
    """The protocol predicate, restricted to one document."""
    return not unresolved_revise_comments(state, doc_addr)


# Doc-neutral alias matching the legacy queries.py pattern.
is_claim_converged = is_doc_converged


def is_converged(state: State) -> bool:
    """The protocol predicate at lattice scope.

    Vacuously true on an empty graph — coverage (have reviews actually
    happened?) is choreography's responsibility, not the predicate's.
    """
    return not unresolved_revise_comments(state)


# ============================================================
#  classifier enumeration
# ============================================================


def all_claim_addrs(state: State) -> List[Address]:
    """Every doc classified as a claim. Sorted for determinism."""
    out: Set[Address] = set()
    for link in state.find_links(type_="claim"):
        out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)

def current_contract_kind(state: State, claim_addr: Address) -> Optional[str]:
    """Most recent `contract.<kind>` classifier targeting the claim.

    Returns the bare subtype string ("axiom", "theorem", etc.) or None.
    Links are permanent; multiple classifiers may accumulate over time;
    the latest in emission order is the current kind. Type-name lookup
    via the registry's reverse map.
    """
    links = state.find_links(to_set=[claim_addr], type_="contract")
    if not links:
        return None
    # Order in LinkStore preserves emission order; take the last
    latest = links[-1]
    if not latest.type_set:
        return None
    name = state.types.name_for(latest.type_set[0])
    if name and "." in name:
        return name.split(".", 1)[1]
    return None


def all_classified(state: State, kind: str) -> List[Address]:
    """Every doc with a classifier link of the given kind. Sorted."""
    out: Set[Address] = set()
    for link in state.find_links(type_=kind):
        # Classifier shape: F=∅, G=[doc]
        if not link.from_set:
            out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


# ============================================================
#  alignment predicates (enabled by version-bearing addresses)
# ============================================================


def has_description(state: State, doc_addr: Address) -> bool:
    """True iff the doc is the F of an active `description` attribute link.

    Per VER3, the description is pinned to a specific doc version. When
    the doc revises (D → D.1), this returns False for D.1 until
    claim-describe runs against it.
    """
    return bool(active_links(state, "description", from_set=[doc_addr]))


def description_sidecar_of(state: State, doc_addr: Address) -> Optional[Address]:
    """The description sidecar's address for this doc, or None.

    If multiple active description links exist (rare — usually 1:1),
    returns the first by sibling order.
    """
    links = active_links(state, "description", from_set=[doc_addr])
    for link in links:
        if link.to_set:
            return link.to_set[0]
    return None


def has_signature(state: State, doc_addr: Address) -> bool:
    """True iff the doc has an active `signature` attribute link."""
    return bool(active_links(state, "signature", from_set=[doc_addr]))


def signature_sidecar_of(state: State, doc_addr: Address) -> Optional[Address]:
    links = active_links(state, "signature", from_set=[doc_addr])
    for link in links:
        if link.to_set:
            return link.to_set[0]
    return None


def has_name(state: State, doc_addr: Address) -> bool:
    return bool(active_links(state, "name", from_set=[doc_addr]))


def has_label(state: State, doc_addr: Address) -> bool:
    return bool(active_links(state, "label", from_set=[doc_addr]))


# ============================================================
#  version-chain helpers (over the parent map)
# ============================================================


def version_children(state: State, doc_addr: Address) -> List[Address]:
    """Immediate version-children of this doc, sorted by sibling order."""
    return sorted(
        (a for a, p in state.parent.items() if p == doc_addr),
        key=lambda a: a.digits,
    )


def version_head(state: State, doc_addr: Address) -> Address:
    """Walk forward to the deepest descendant in the linear chain.

    At each level, picks the highest-numbered sibling. Branches
    (versions of an earlier version that aren't the latest) are not
    followed.
    """
    cur = doc_addr
    while True:
        children = version_children(state, cur)
        if not children:
            return cur
        cur = children[-1]


def is_head_version(state: State, doc_addr: Address) -> bool:
    return not version_children(state, doc_addr)


# ============================================================
#  citation graph
# ============================================================


def depends(state: State, doc_addr: Address) -> List[Address]:
    """Docs this doc depends on (active `citation.depends` from doc)."""
    out: Set[Address] = set()
    for link in active_links(state, "citation.depends", from_set=[doc_addr]):
        out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


def dependents(state: State, doc_addr: Address) -> List[Address]:
    """Docs that depend on this doc (active `citation.depends` to doc)."""
    out: Set[Address] = set()
    for link in active_links(state, "citation.depends", to_set=[doc_addr]):
        out.update(link.from_set)
    return sorted(out, key=lambda a: a.digits)
