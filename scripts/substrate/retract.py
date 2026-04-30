#!/usr/bin/env python3
"""Reviser-callable CLI to retract a citation link.

Invoked when the reviser removes a dependency from a claim's md
*Depends:* section because the proof no longer uses it:

    python scripts/substrate/retract.py --from <label> --to <label>

Both arguments are claim labels. The from-label is the claim whose
Depends entry is being removed; the script resolves it to its
canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var. The to-label is the labeled dependency
whose citation should be retracted; resolved via the substrate's
cross-ASN label index. The CLI then locates the existing citation
from-claim → to-claim and files a retraction at that specific link id.

Idempotent — re-running with the same args is a no-op. The substrate
is append-only; retraction does not delete the citation.

Prints the retraction link id on success; exits non-zero on error
(unknown label, no citation found, multiple citations).
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import claim_doc_path
from store.store import default_store
from store.retract import emit_retraction
from store.populate import build_doc_label_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from", dest="from_label", required=True,
        help="Label of the claim whose citation is being retracted "
             "(e.g., NAT-addbound).",
    )
    parser.add_argument(
        "--to", required=True,
        help="The dependency label whose citation should be retracted "
             "(e.g., NAT-cancel, T0).",
    )
    parser.add_argument(
        "--direction", choices=("depends", "forward"), default="depends",
        help="Direction of the citation being retracted: depends "
             "(backward, default) or forward.",
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
            link_id, created = emit_retraction(
                store, claim_path, args.to, label_index,
                direction=args.direction,
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
