#!/usr/bin/env python3
"""
Citation Resolve — type each claim-label reference in a claim's prose
as either depends (backward) or forward.

Reads the claim's body; Sonnet identifies label references and types
each. The orchestrator validates labels, edits the .md (insert bullets
in *Depends:* / *Forward References:*), emits substrate links
(citation.depends / citation.forward / retraction / citation.resolve /
provenance.derivation), persists the resolve doc, and commits.

Usage:
    python scripts/claim-citation-resolve.py 34
    python scripts/claim-citation-resolve.py 34 --claim NAT-card
    python scripts/claim-citation-resolve.py 34 --model sonnet
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claim_convergence.citation_resolve import (
    run_classification, run_sweep,
)


def main():
    parser = argparse.ArgumentParser(
        description="Citation Resolve — type each label reference in a claim's prose.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument(
        "--claim", metavar="LABEL",
        help="Resolve a single claim instead of the full sweep",
    )
    parser.add_argument(
        "--model", default="sonnet",
        help="Model for the resolve call (default: sonnet)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.claim:
        result = run_classification(asn_num, args.claim, model=args.model)
    else:
        result = run_sweep(asn_num, model=args.model)

    sys.exit(0 if result == "ok" else 1)


if __name__ == "__main__":
    main()
