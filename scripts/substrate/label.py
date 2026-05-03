#!/usr/bin/env python3
"""Reviser-callable CLI to set a claim's label.

    python scripts/substrate/label.py --label T0

The argument is both the operand (which claim) and the value (the
label string). Per substrate-module §4, a claim's label sidecar's
content equals the filename stem; for the filesystem-backed
substrate the two are identical, so the single `--label` arg
suffices.

The script resolves the label to the canonical doc address via the
claim path convention (`_docuverse/documents/claim/<asn>/<label>.md`)
keyed off the `PROTOCOL_ASN_LABEL` env var, writes
`<stem>.label.md` next to the claim md (edit-in-place if it
already exists), and emits the substrate `label` link.

Idempotent — re-running with the same args is a no-op.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import claim_doc_path, LATTICE
from lib.backend.emit import emit_attribute
from lib.backend.store import default_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--label", required=True,
        help="The claim's label (e.g., T0, NAT-cancel).",
    )
    args = parser.parse_args()

    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    claim_path = claim_doc_path(asn_label, args.label)

    store = default_store(LATTICE)
    try:
        link, created = emit_attribute(
            store, claim_path, "label", args.label,
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
