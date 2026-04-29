"""Library: emit a contract.<kind> classifier link for a claim.

Called from `scripts/claim-classify.py` (the reviser-callable CLI). Separated
from the CLI so tests exercise the logic directly.

Reviser tooling parallel: `convergence-cite.py` adds citation,
`convergence-resolution.py` adds resolution, `claim-classify.py` adds
contract.<kind>. All three are explicit substrate writes the reviser
performs as part of completing its work.
"""

from lib.store.schema import VALID_SUBTYPES


def emit_classifier(store, claim_path, kind):
    """Add a contract.<kind> classifier link targeting claim_path.

    `kind` must be one of: axiom, definition, theorem, lemma, corollary,
    consequence, design-requirement.

    Idempotent: if a classifier with the same kind targeting the same claim
    already exists, returns its id with created=False without calling
    make_link.

    Returns (link_id, created_bool).
    Raises ValueError if kind is not a valid contract subtype.
    """
    valid_kinds = VALID_SUBTYPES["contract"]
    if kind not in valid_kinds:
        raise ValueError(
            f"invalid contract kind {kind!r}; must be one of "
            f"{sorted(valid_kinds)}"
        )

    type_str = f"contract.{kind}"
    candidates = store.find_links(to_set=[claim_path], type_set=[type_str])
    for link in candidates:
        if (link["from_set"] == []
                and link["to_set"] == [claim_path]
                and link["type_set"] == [type_str]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[],
        to_set=[claim_path],
        type_set=[type_str],
    )
    return link_id, True
