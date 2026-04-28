#!/usr/bin/env python3
"""Reviser-callable CLI to add a citation link.

Invoked when the reviser adds a dependency:

    python scripts/cite.py --to <label>

Reads `PROTOCOL_DOC_PATH` from environment (set by `revise.py` for the
claim being revised). The label is resolved via the cross-ASN label
index. Idempotent — re-running with the same args is a no-op.

Prints the citation link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.store import default_store
from store.cite import emit_citation
from store.populate import build_cross_asn_label_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--to", required=True,
        help="The dependency label to cite (e.g., T0, NAT-closure).",
    )
    args = parser.parse_args()

    claim_path = os.environ.get("PROTOCOL_DOC_PATH")
    if not claim_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1

    store = default_store()
    try:
        try:
            label_index = build_cross_asn_label_index(store=store)
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
