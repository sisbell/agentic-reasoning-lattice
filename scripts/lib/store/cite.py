"""Library: emit a citation link from one claim to another.

Called from `scripts/convergence-cite.py` (the reviser-callable CLI). Separated from
the CLI so tests exercise the logic directly.
"""


def emit_citation(store, from_claim_path, to_label, label_index):
    """Add a citation link from from_claim_path to the claim labeled to_label.

    `label_index` maps labels to repo-relative md paths (use
    `lib.store.populate.build_cross_asn_label_index`).

    Idempotent: if a citation with the same from/to already exists, returns
    its id with created=False without calling make_link.

    Returns (link_id, created_bool).
    Raises KeyError if to_label is not in label_index.
    """
    if to_label not in label_index:
        raise KeyError(f"label '{to_label}' not in label index")
    to_path = label_index[to_label]

    candidates = store.find_links(
        from_set=[from_claim_path],
        to_set=[to_path],
        type_set=["citation"],
    )
    for link in candidates:
        if (link["from_set"] == [from_claim_path]
                and link["to_set"] == [to_path]
                and link["type_set"] == ["citation"]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[from_claim_path],
        to_set=[to_path],
        type_set=["citation"],
    )
    return link_id, True
