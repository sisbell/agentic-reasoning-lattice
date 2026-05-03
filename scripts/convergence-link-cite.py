#!/usr/bin/env python3
"""Reviser-callable CLI to add a citation link.

Invoked when the reviser adds a dependency:

    python scripts/convergence-link-cite.py --from <label> --to <label>

Both arguments are claim labels — never paths. The script resolves the
from-label to its canonical doc address via the claim path convention
(`_docuverse/documents/claim/<asn>/<label>.md`) keyed off the
`PROTOCOL_ASN_LABEL` env var the orchestrator sets, and resolves the
to-label via the substrate's cross-ASN label index (deps may target
foundations in upstream ASNs). Idempotent on (from, to).

Prints the citation link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import claim_doc_path, LATTICE
from lib.agent import default_store
from lib.backend.emit import emit_citation
from lib.lattice.labels import build_doc_label_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from", dest="from_label", required=True,
        help="Label of the claim citing FROM (e.g., NAT-addbound).",
    )
    parser.add_argument(
        "--to", required=True,
        help="Label of the dependency being cited (e.g., T0, NAT-closure).",
    )
    parser.add_argument(
        "--direction", choices=("depends", "forward"), default="depends",
        help="Direction of the citation: depends (backward, default) or "
             "forward (this claim names a downstream claim it does not "
             "depend on).",
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
    citing_addr = store.register_path(claim_path)
    cited_addr = label_index[args.to]
    link, created = emit_citation(
        store, citing_addr, cited_addr, direction=args.direction,
    )
    print(link.addr)
    if not created:
        print("(already exists)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
