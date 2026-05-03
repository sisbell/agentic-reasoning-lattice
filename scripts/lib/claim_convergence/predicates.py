"""Convergence-protocol predicates over the substrate.

The convergence protocol's load-bearing definition (per
`docs/protocols/claim-convergence-protocol.md`):

    For every document with a `claim` classifier, every active
    `comment.revise` link targeting that claim has a matching active
    `resolution` link.

A link is *active* if no `retraction` link nullifies it. Retracted
revises drop out of the predicate; retracted resolutions stop
satisfying it. The predicates here implement that protocol semantics
on top of substrate primitives (active_links, find_links, etc.).

These predicates know what specific link types *mean* in the
convergence protocol — `comment.revise`, `resolution`, the
revise-resolution pairing — so they're protocol code, not substrate
primitive. They live here, alongside the rest of the claim-convergence
package, rather than in `lib/backend/`.
"""

from __future__ import annotations

from typing import List, Optional, Set

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.backend.predicates import active_links, retracted_link_addrs
from lib.backend.state import State


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


def is_asn_converged(store, asn_label: str) -> bool:
    """Conjunction of `is_doc_converged` over every claim md under an ASN.

    Identifies an ASN's claim docs by walking the path map for paths
    matching `_docuverse/documents/claim/<asn_label>/*.md` and
    excluding sidecars. Vacuously true on an ASN with no matching
    claims — coverage is choreography's responsibility.

    `store` is a backend.store.Store (not a State) — needs the path
    map to recover ASN-scoped docs.
    """
    import re
    from lib.backend.schema import ATTRIBUTE_SUFFIXES
    asn_path_pattern = re.compile(
        rf"_docuverse/documents/claim/{re.escape(asn_label)}/[^/]+\.md$"
    )
    for path, addr in store.path_to_addr.items():
        if not asn_path_pattern.search(path):
            continue
        if path.endswith(ATTRIBUTE_SUFFIXES):
            continue
        if "/_" in path:
            continue
        if not is_doc_converged(store.state, addr):
            return False
    return True
