#!/usr/bin/env python3
"""Reviser-callable CLI to add a contract.<kind> classifier link.

Invoked when the reviser creates a new claim and needs to record what
kind of contract it is (axiom, theorem, definition, etc.):

    python scripts/claim-link-contract.py --kind axiom

Reads `PROTOCOL_DOC_PATH` from environment (set by `revise.py` for the
claim being revised — but for new-claim creation, the reviser sets it
to the new claim's md path before calling). Idempotent — re-running
with the same args is a no-op.

Prints the classifier link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.store import default_store
from store.classify import emit_classifier
from store.schema import VALID_SUBTYPES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kind", required=True,
        choices=sorted(VALID_SUBTYPES["contract"]),
        help="Contract kind classifier for the claim.",
    )
    args = parser.parse_args()

    claim_path = os.environ.get("PROTOCOL_DOC_PATH")
    if not claim_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1

    store = default_store()
    try:
        try:
            link_id, created = emit_classifier(store, claim_path, args.kind)
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
