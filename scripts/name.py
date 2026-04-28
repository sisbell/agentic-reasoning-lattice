#!/usr/bin/env python3
"""Reviser-callable CLI to set a claim's canonical name.

Usage:

    PROTOCOL_DOC_PATH=lattices/.../T0.md python scripts/name.py --to CarrierSetDefinition

Writes `<stem>.name.md` next to the claim md (edit-in-place if it
already exists) and emits a `name` link from the claim md to the
sibling doc. Idempotent.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.attributes import emit_attribute
from store.store import default_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--to", required=True,
        help="The canonical name (e.g., CarrierSetDefinition).",
    )
    args = parser.parse_args()

    claim_path = os.environ.get("PROTOCOL_DOC_PATH")
    if not claim_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1

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
