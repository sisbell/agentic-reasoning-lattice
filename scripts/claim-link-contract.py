#!/usr/bin/env python3
"""Reviser-callable CLI to add a contract.<kind> classifier link.

Invoked when the reviser creates a new claim or reclassifies an
existing one's contract structure:

    python scripts/claim-link-contract.py --label <label> --kind axiom

The label identifies the claim; the script resolves it to the
canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var. Idempotent on (doc, kind) — re-running
with the same args is a no-op.

Prints the classifier link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import claim_doc_path, LATTICE
from lib.agent import default_store
from lib.backend.emit import emit_contract
from lib.backend.schema import VALID_SUBTYPES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--label", required=True,
        help="Label of the claim to classify (e.g., T0, NAT-zero).",
    )
    parser.add_argument(
        "--kind", required=True,
        choices=sorted(VALID_SUBTYPES["contract"]),
        help="Contract kind classifier for the claim.",
    )
    args = parser.parse_args()

    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    claim_path = claim_doc_path(asn_label, args.label)

    store = default_store(LATTICE)
    claim_addr = store.register_path(claim_path)
    try:
        link, created = emit_contract(store, claim_addr, args.kind)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(link.addr)
    if not created:
        print("(already exists)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
