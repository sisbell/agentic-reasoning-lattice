"""Library: retract a citation link by filing a retraction that points at it.

Called from `scripts/substrate/retract.py` (the reviser-callable CLI). Separated
from the CLI so tests exercise the logic directly.

A retraction is a top-level link of type `"retraction"` whose to_set
holds the link ID of the citation being retracted (link-to-link
pointer). The substrate is append-only — retraction does not delete
the citation; it nullifies it for graph queries via the `active_links`
helper in `lib.store.queries`.
"""


def emit_retraction(store, from_claim_path, to_label, label_index, *, direction="depends"):
    """Retract the citation from from_claim_path to the claim labeled to_label.

    Looks up the existing citation link, then files a retraction whose
    to_set is the citation's link id.

    `label_index` maps labels to repo-relative md paths (use
    `lib.store.populate.build_cross_asn_label_index`).

    `direction` ∈ {"depends", "forward"} selects which directional
    citation to retract.

    Idempotent: if a retraction already targets the citation's link id,
    returns its id with created=False without calling make_link.

    Returns (link_id, created_bool).
    Raises KeyError if to_label is not in label_index.
    Raises ValueError if no citation exists from from_claim_path to the
    target, or if multiple citations exist (defensive — content-hash
    dedup currently prevents this).
    """
    if to_label not in label_index:
        raise KeyError(f"label '{to_label}' not in label index")
    to_path = label_index[to_label]
    type_str = f"citation.{direction}"

    # Find the citation to retract. find_links uses LIKE matching on type,
    # so filter to exact [type_str] to avoid pulling in unrelated subtypes.
    citations = [
        link
        for link in store.find_links(
            from_set=[from_claim_path],
            to_set=[to_path],
            type_set=[type_str],
        )
        if link["type_set"] == [type_str]
        and link["from_set"] == [from_claim_path]
        and link["to_set"] == [to_path]
    ]
    if not citations:
        raise ValueError(
            f"no citation found from {from_claim_path} to {to_label}"
        )
    if len(citations) > 1:
        raise ValueError(
            f"multiple citations from {from_claim_path} to {to_label}; "
            f"cannot retract unambiguously"
        )

    citation_id = citations[0]["id"]

    # Idempotency: is there already a retraction targeting this citation?
    existing = store.find_links(
        from_set=[from_claim_path],
        to_set=[citation_id],
        type_set=["retraction"],
    )
    for link in existing:
        if (link["type_set"] == ["retraction"]
                and link["from_set"] == [from_claim_path]
                and link["to_set"] == [citation_id]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[from_claim_path],
        to_set=[citation_id],
        type_set=["retraction"],
    )
    return link_id, True
