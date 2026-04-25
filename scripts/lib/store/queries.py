"""Convergence query helpers for the Claim Convergence Protocol.

Read-only logic composed entirely over `Store.find_links`. The protocol
predicate (per docs/protocols/claim-convergence-protocol-v2.md):

    For every document with a `claim` classifier, every `comment.revise`
    link targeting that claim has a matching `resolution` link.

Helpers below evaluate that predicate at lattice and per-claim scope, plus
expose the unresolved-comment listing for diagnostic callers.
"""


def has_resolution(store, comment_id):
    """True iff any resolution link targets this comment id."""
    return bool(store.find_links(to_set=[comment_id], type_set=["resolution"]))


def all_claim_paths(store):
    """Every document path classified as a claim. Sorted for determinism."""
    paths = set()
    for link in store.find_links(type_set=["claim"]):
        paths.update(link["to_set"])
    return sorted(paths)


def unresolved_revise_comments(store, claim_path=None):
    """Every comment.revise link without a matching resolution.

    If claim_path is given, scopes to comments targeting that claim.
    Otherwise spans the whole graph.
    """
    revises = store.find_links(
        to_set=[claim_path] if claim_path else None,
        type_set=["comment.revise"],
    )
    return [c for c in revises if not has_resolution(store, c["id"])]


def is_claim_converged(store, claim_path):
    """The protocol predicate, restricted to one claim."""
    return not unresolved_revise_comments(store, claim_path)


def is_converged(store):
    """The protocol predicate at lattice scope.

    Vacuously true on an empty graph — coverage (have reviews actually
    happened?) is the choreography's responsibility, not the predicate's.
    """
    return not unresolved_revise_comments(store)


def current_contract_kind(store, claim_md_path):
    """Return the contract subtype string for a claim, or None.

    Picks the most recently-created `contract.<kind>` classifier link
    targeting the claim. Links are permanent — multiple classifiers may
    accumulate over time; the latest by `ts` is the current kind.
    Returns the bare subtype, e.g., "axiom", "theorem", "corollary".
    """
    if not claim_md_path:
        return None
    links = store.find_links(to_set=[claim_md_path], type_set=["contract"])
    if not links:
        return None
    latest = max(links, key=lambda l: l["ts"])
    type_str = latest["type_set"][0]
    if "." in type_str:
        return type_str.split(".", 1)[1]
    return None
