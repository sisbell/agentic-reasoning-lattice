#!/usr/bin/env python3
"""Reviser-callable CLI to add a citation link.

Invoked when the reviser adds a dependency:

    python scripts/convergence-link-cite.py --from <label> --to <label>

Both arguments are claim labels — never paths. The script resolves the
from-label to its canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var the orchestrator sets, and resolves the
to-label via the substrate's cross-ASN label index (deps may target
foundations in upstream ASNs). Idempotent on (from, to).

Prints the citation link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import claim_doc_path
from store.store import default_store
from store.cite import emit_citation
from store.populate import build_doc_label_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from", dest="from_label", required=True,
        help="Label of the claim citing FROM (e.g., NAT-addbound).",
    )
    parser.add_argument(
        "--to", required=True,
        help="Label of the dependency being cited (e.g., T0, NAT-closure).",
    )
    args = parser.parse_args()

    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    claim_path = claim_doc_path(asn_label, args.from_label)

    store = default_store()
    try:
        try:
            label_index = build_doc_label_index(store, claim_path)
            link_id, created = emit_citation(
                store, claim_path, args.to, label_index,
            )
        except KeyError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        print(link_id)
        if not created:
            print("(already exists)", file=sys.stderr)
    finally:
        store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
