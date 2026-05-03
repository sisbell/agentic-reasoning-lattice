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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import claim_doc_path, LATTICE
from lib.backend.store import default_store
from lib.backend.emit import emit_retraction
from lib.backend.populate import build_doc_label_index
from lib.backend.predicates import active_links


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

    store = default_store(LATTICE)
    label_index = build_doc_label_index(store, claim_path)
    if args.to not in label_index:
        print(f"error: unknown label {args.to!r}", file=sys.stderr)
        return 1
    citing_addr = store.path_to_addr.get(claim_path)
    if citing_addr is None:
        print(f"error: claim {claim_path!r} not in substrate", file=sys.stderr)
        return 1
    cited_addr = label_index[args.to]
    type_str = f"citation.{args.direction}"
    candidates = active_links(
        store.state, type_str, from_set=[citing_addr], to_set=[cited_addr],
    )
    if not candidates:
        print(f"error: no active {type_str} from {args.from_label} to {args.to}",
              file=sys.stderr)
        return 1
    if len(candidates) > 1:
        print(f"error: ambiguous — {len(candidates)} active {type_str} links",
              file=sys.stderr)
        return 1
    target_link = candidates[0]
    retraction = emit_retraction(store, citing_addr, target_link.addr)
    print(retraction.addr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
