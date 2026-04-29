#!/usr/bin/env python3
"""Reviser-callable CLI for closing a finding.

Invoked at the end of a revise session:

    python scripts/convergence-link-resolution.py accept
    python scripts/convergence-link-resolution.py reject --rationale "<one or two sentences>"

When a single revise session closes multiple findings (note convergence
sets up env once and the agent iterates), the comment id can be passed
per call:

    python scripts/convergence-link-resolution.py accept --comment-id l_abc123

Otherwise reads context from environment variables (set by the
orchestrator before spawning the reviser):

    PROTOCOL_COMMENT_ID    — the comment link being closed
    PROTOCOL_DOC_PATH      — the doc md path (lattice-relative)
    PROTOCOL_ASN_LABEL     — the ASN label (for rationale doc placement)

On reject, materializes the rationale document under
_docuverse/documents/rationale/{ASN}/{comment_id}.md and writes a resolution.reject
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--comment-id", dest="comment_id",
        help="Comment link id to close (overrides PROTOCOL_COMMENT_ID env).",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("accept")
    p_reject = sub.add_parser("reject")
    p_reject.add_argument(
        "--rationale", required=True,
        help="One or two sentences explaining why the finding was refused.",
    )
    args = parser.parse_args()

    comment_id = args.comment_id or os.environ.get("PROTOCOL_COMMENT_ID")
    doc_path = os.environ.get("PROTOCOL_DOC_PATH")
    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not comment_id:
        print("error: --comment-id or PROTOCOL_COMMENT_ID required", file=sys.stderr)
        return 1
    if not doc_path:
        print("error: PROTOCOL_DOC_PATH env var not set", file=sys.stderr)
        return 1
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    store = default_store()
    try:
        try:
            link_id = emit_decision(
                store, args.action, comment_id, doc_path, asn_label,
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
