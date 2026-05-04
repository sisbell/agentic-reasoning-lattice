"""Generate per-ASN dependency dicts from substrate citation links.

Reads each claim's classifier kind and `citation.depends` links from
the substrate, plus the ASN's foundation deps via `claim_asn_dep_ids`.

The output is a single dict per ASN containing:
  - asn:     ASN number
  - depends: list of foundation ASN numbers
  - claims:  per-claim {status, type, name, follows_from}

Public entry point: build_deps_for_asn.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import LATTICE, CLAIM_DIR
from lib.shared.claim_files import load_claim_metadata
from lib.shared.common import find_asn
from lib.shared.foundation import claim_asn_dep_ids
from lib.protocols.febe.session import open_session
from lib.lattice.labels import build_cross_asn_label_index
from lib.backend.predicates import active_links
from lib.predicates import current_contract_kind


def build_deps_for_asn(asn_num):
    """Build the per-ASN dependency dict from substrate state.

    Returns a dict {asn, depends, claims}, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    claim_dir = CLAIM_DIR / asn_label
    depends = claim_asn_dep_ids(asn_num)
    metadata = load_claim_metadata(claim_dir) if claim_dir.exists() else {}

    if not metadata:
        print(f"  [ERROR] No per-claim files found in {claim_dir}",
              file=sys.stderr)
        return None

    session = open_session(LATTICE)
    store = session.store
    cross_index = build_cross_asn_label_index(store)
    rev_index = {addr: label for label, addr in cross_index.items()}

    claims = {}
    for label, data in metadata.items():
        from_addr = cross_index.get(label)
        contract_kind = (
            current_contract_kind(session, from_addr)
            if from_addr is not None else None
        )
        prop = {"status": contract_kind or "introduced"}
        if contract_kind:
            prop["type"] = contract_kind

        if data.get("name"):
            prop["name"] = data["name"]

        if from_addr is not None:
            follows = []
            for link in active_links(
                store.state, "citation.depends", from_set=[from_addr],
            ):
                for cited_addr in link.to_set:
                    label_match = rev_index.get(cited_addr)
                    if label_match:
                        follows.append(label_match)
            if follows:
                prop["follows_from"] = follows

        claims[label] = prop

    return {
        "asn": asn_num,
        "depends": depends,
        "claims": claims,
    }
