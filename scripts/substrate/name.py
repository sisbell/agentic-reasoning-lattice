#!/usr/bin/env python3
"""Reviser-callable CLI to set a claim's canonical name.

    python scripts/substrate/name.py --label T0 --to CarrierSetDefinition

The label identifies the claim; the script resolves it to the
canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var, writes `<stem>.name.md` next to the
claim md (edit-in-place), and emits the substrate `name` link.
Idempotent.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import claim_doc_path
from store.attributes import emit_attribute
from store.store import default_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--label", required=True,
        help="Label of the claim being named (e.g., T0).",
    )
    parser.add_argument(
        "--to", required=True,
        help="The canonical name string (e.g., CarrierSetDefinition).",
    )
    args = parser.parse_args()

    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    claim_path = claim_doc_path(asn_label, args.label)

    store = default_store()
    try:
        try:
            link_id, created = emit_attribute(
                store, claim_path, "name", args.to,
            )
        except ValueError as e:
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
