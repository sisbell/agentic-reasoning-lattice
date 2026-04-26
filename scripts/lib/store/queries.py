"""Convergence query helpers for the Claim Convergence Protocol.

Read-only logic composed entirely over `Store.find_links`. The protocol
predicate (per docs/protocols/claim-convergence-protocol.md):

    For every document with a `claim` classifier, every active
    `comment.revise` link targeting that claim has a matching active
    `resolution` link.

A link is *active* if no `retraction` link nullifies it. Retracted
revises drop out of the predicate (they no longer represent an active
complaint); retracted resolutions stop satisfying it.

Helpers below evaluate that predicate at lattice and per-claim scope, plus
expose the unresolved-comment listing for diagnostic callers.
"""


def _retracted_link_ids(store):
    """Set of link ids that have been retracted.

    A retraction is a link of type `"retraction"` whose to_set holds
    the link id of the link being nullified.
    """
    ids = set()
    for r in store.find_links(type_set=["retraction"]):
        if r["type_set"] == ["retraction"]:
            ids.update(r["to_set"])
    return ids


def has_resolution(store, comment_id, _retracted=None):
    """True iff any active resolution link targets this comment id.

    `_retracted` is an optional pre-computed set of retracted link ids;
    callers iterating over many comments pass it once to avoid re-querying.
    """
    retracted = _retracted_link_ids(store) if _retracted is None else _retracted
    return any(
        r["id"] not in retracted
        for r in store.find_links(to_set=[comment_id], type_set=["resolution"])
    )


def active_links(store, type_str, from_set=None, to_set=None):
    """Return links of `type_str` that have not been retracted.

    Filters LIKE-match results to exact `type_str` to avoid pulling in
    unrelated subtypes (e.g., a query for "citation" would otherwise
    match any future "citation.*" subtype via SQL LIKE).

    Use this in place of `store.find_links(type_set=[type_str], ...)`
    wherever the consumer wants the "active" set, ignoring retracted
    history.
    """
    retracted = _retracted_link_ids(store)
    candidates = store.find_links(
        from_set=from_set, to_set=to_set, type_set=[type_str],
    )
    return [
        link for link in candidates
        if link["type_set"] == [type_str]
        and link["id"] not in retracted
    ]


def all_claim_paths(store):
    """Every document path classified as a claim. Sorted for determinism."""
    paths = set()
    for link in store.find_links(type_set=["claim"]):
        paths.update(link["to_set"])
    return sorted(paths)


def unresolved_revise_comments(store, claim_path=None):
    """Every active comment.revise link without an active resolution.

    Retracted revises are excluded (the retraction nullifies the
    complaint). A resolution that has itself been retracted does not
    satisfy the predicate. If claim_path is given, scopes to comments
    targeting that claim; otherwise spans the whole graph.
    """
    retracted = _retracted_link_ids(store)
    revises = store.find_links(
        to_set=[claim_path] if claim_path else None,
        type_set=["comment.revise"],
    )
    return [
        c for c in revises
        if c["id"] not in retracted
        and not has_resolution(store, c["id"], _retracted=retracted)
    ]


def is_claim_converged(store, claim_path):
    """The protocol predicate, restricted to one claim."""
    return not unresolved_revise_comments(store, claim_path)


def is_converged(store):
    """The protocol predicate at lattice scope.

    Vacuously true on an empty graph — coverage (have reviews actually
    happened?) is the choreography's responsibility, not the predicate's.
    """
    return not unresolved_revise_comments(store)


def is_asn_converged(store, asn_label, claim_convergence_dir=None):
    """The protocol predicate scoped to one ASN's claims.

    Conjunction of `is_claim_converged` over every claim in
    `lattices/<lattice>/claim-convergence/<asn_label>/`. Vacuously true on a
    nonexistent or empty ASN — coverage is choreography's responsibility,
    not the predicate's.
    """
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from lib.shared.paths import CLAIM_CONVERGENCE_DIR, WORKSPACE

    claim_convergence_dir = (
        Path(claim_convergence_dir) if claim_convergence_dir else CLAIM_CONVERGENCE_DIR
    )
    asn_dir = claim_convergence_dir / asn_label
    if not asn_dir.exists():
        return True
    workspace_resolved = Path(WORKSPACE).resolve()
    for yaml_path in asn_dir.glob("*.yaml"):
        if yaml_path.name.startswith("_"):
            continue
        md_path = yaml_path.with_suffix(".md")
        rel = str(md_path.resolve().relative_to(workspace_resolved))
        if not is_claim_converged(store, rel):
            return False
    return True


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
