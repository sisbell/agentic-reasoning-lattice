#!/usr/bin/env python3
"""Reviser-callable CLI to set a claim's prose description.

Usage:

    PROTOCOL_DOC_PATH=lattices/.../T0.md python scripts/substrate/description.py \\
        --to "Defines the carrier set ℕ for tumbler addresses."

For multi-line descriptions, use --from-file to read the body from a
file (or `-` for stdin):

    PROTOCOL_DOC_PATH=... python scripts/substrate/description.py --from-file desc.md
    cat desc.md | PROTOCOL_DOC_PATH=... python scripts/substrate/description.py --from-file -

Writes `<stem>.description.md` next to the claim md (edit-in-place if
it already exists) and emits a `description` link from the claim md to
the sibling doc. Idempotent.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from store.attributes import emit_attribute
from store.store import default_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--to", help="The description string (single-line).",
    )
    group.add_argument(
        "--from-file", dest="from_file",
        help="Path to a file containing the description body, or '-' for stdin.",
    )
    args = parser.parse_args()

    claim_path = os.environ.get("PROTOCOL_DOC_PATH")
    if not claim_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1

    if args.from_file:
        if args.from_file == "-":
            body = sys.stdin.read()
        else:
            try:
                body = Path(args.from_file).read_text()
            except OSError as e:
                print(f"error: cannot read {args.from_file}: {e}", file=sys.stderr)
                return 1
    else:
        body = args.to

    store = default_store()
    try:
        try:
            link_id, created = emit_attribute(
                store, claim_path, "description", body,
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
