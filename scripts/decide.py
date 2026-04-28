#!/usr/bin/env python3
"""Reviser-callable CLI for closing a finding.

Invoked at the end of a revise session:

    python scripts/decide.py accept
    python scripts/decide.py reject --rationale "<one or two sentences>"

Reads context from environment variables (set by the orchestrator before
spawning the reviser):

    PROTOCOL_COMMENT_ID    — the comment link being closed
    PROTOCOL_CLAIM_PATH    — the claim md path (repo-relative)
    PROTOCOL_ASN_LABEL     — the ASN label (for rationale doc placement)

On reject, materializes the rationale document under
_store/rationales/{ASN}/{comment_id}.md and writes a resolution.reject
link binding the comment and the rationale.

Prints the new resolution link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.store import default_store
from store.decide import emit_decision


REQUIRED_ENV = ("PROTOCOL_COMMENT_ID", "PROTOCOL_CLAIM_PATH", "PROTOCOL_ASN_LABEL")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("accept")
    p_reject = sub.add_parser("reject")
    p_reject.add_argument(
        "--rationale", required=True,
        help="One or two sentences explaining why the finding was refused.",
    )
    args = parser.parse_args()

    for name in REQUIRED_ENV:
        if not os.environ.get(name):
            print(f"error: {name} env var not set", file=sys.stderr)
            return 1

    comment_id = os.environ["PROTOCOL_COMMENT_ID"]
    claim_path = os.environ["PROTOCOL_CLAIM_PATH"]
    asn_label = os.environ["PROTOCOL_ASN_LABEL"]

    store = default_store()
    try:
        try:
            link_id = emit_decision(
                store, args.action, comment_id, claim_path, asn_label,
                rationale=getattr(args, "rationale", None),
            )
        except (KeyError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        print(link_id)
    finally:
        store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
