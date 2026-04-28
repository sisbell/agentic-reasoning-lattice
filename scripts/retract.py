#!/usr/bin/env python3
"""Reviser-callable CLI to retract a citation link.

Invoked when the reviser removes a dependency from a claim's md
*Depends:* section because the proof no longer uses it:

    python scripts/retract.py --to <label>

Reads `PROTOCOL_DOC_PATH` from environment (set by the protocol
runner for the claim being revised). The label is resolved via the
cross-ASN label index. The CLI looks up the existing citation from
PROTOCOL_DOC_PATH to the labeled claim and files a retraction
pointing at that specific citation link's id.

Idempotent — re-running with the same args is a no-op. The substrate
is append-only; retraction does not delete the citation.

Prints the retraction link id on success; exits non-zero on error
(unknown label, no citation found, multiple citations).
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.store import default_store
from store.retract import emit_retraction
from store.populate import build_doc_label_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--to", required=True,
        help="The dependency label whose citation should be retracted "
             "(e.g., NAT-cancel, T0).",
    )
    args = parser.parse_args()

    claim_path = os.environ.get("PROTOCOL_DOC_PATH")
    if not claim_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1

    store = default_store()
    try:
        try:
            label_index = build_doc_label_index(store, claim_path)
            link_id, created = emit_retraction(
                store, claim_path, args.to, label_index,
            )
        except (KeyError, ValueError) as e:
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
