"""Library: emit a citation link from one claim to another.

Called from `scripts/convergence-link-cite.py` (the reviser-callable CLI). Separated from
the CLI so tests exercise the logic directly.
"""

from lib.store.queries import active_links


def emit_citation(store, from_claim_path, to_label, label_index, *, direction="depends"):
    """Add a citation link from from_claim_path to the claim labeled to_label.

    `label_index` maps labels to repo-relative md paths (use
    `lib.store.populate.build_cross_asn_label_index`).

    `direction` ∈ {"depends", "forward"}:
      - "depends": this claim's correctness rests on the cited claim (backward)
      - "forward": this claim names a downstream claim it does not depend on

    Idempotent against the *active* citation set: if an active citation of
    the same direction and same from/to already exists, returns its id with
    created=False. A previously-retracted citation does not satisfy
    idempotency — re-emitting after a retraction creates a fresh active
    link, since the caller is expressing that the citation is currently
    wanted.

    Returns (link_id, created_bool).
    Raises KeyError if to_label is not in label_index.
    """
    if to_label not in label_index:
        raise KeyError(f"label '{to_label}' not in label index")
    to_path = label_index[to_label]
    type_str = f"citation.{direction}"

    for link in active_links(
        store, type_str, from_set=[from_claim_path], to_set=[to_path],
    ):
        if (link["from_set"] == [from_claim_path]
                and link["to_set"] == [to_path]
                and link["type_set"] == [type_str]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[from_claim_path],
        to_set=[to_path],
        type_set=[type_str],
    )
    return link_id, True
