#!/usr/bin/env python3
"""Reviser-callable CLI to set a claim's prose description.

    python scripts/substrate/description.py --label T0 \\
        --to "Defines the carrier set ℕ for tumbler addresses."

For multi-line descriptions, use --from-file to read the body from a
file (or `-` for stdin):

    python scripts/substrate/description.py --label T0 --from-file desc.md
    cat desc.md | python scripts/substrate/description.py --label T0 \\
        --from-file -

The label identifies the claim; the script resolves it to the
canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var, writes `<stem>.description.md` next
to the claim md (edit-in-place), and emits the substrate
`description` link. Idempotent.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import claim_doc_path, LATTICE
from lib.backend.emit import emit_attribute
from lib.agent import default_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--label", required=True,
        help="Label of the claim being described (e.g., T0).",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--to", help="The description string (single-line).",
    )
    group.add_argument(
        "--from-file", dest="from_file",
        help="Path to a file containing the description body, or '-' for stdin.",
    )
    args = parser.parse_args()

    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    claim_path = claim_doc_path(asn_label, args.label)

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

    store = default_store(LATTICE)
    try:
        link, created = emit_attribute(
            store, claim_path, "description", body,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(link.addr)
    if not created:
        print("(already exists)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
