#!/usr/bin/env python3
"""Reviser-callable CLI for closing a finding.

Invoked at the end of a revise session:

    python scripts/agent_tools/convergence-link-resolution.py accept
    python scripts/agent_tools/convergence-link-resolution.py reject \\
        --rationale "<one or two sentences>"

When a single revise session closes multiple findings (note convergence
sets up env once and the agent iterates), the comment id can be passed
per call:

    python scripts/agent_tools/convergence-link-resolution.py accept --comment-id l_abc123

Otherwise reads context from environment variables (set by the
orchestrator before spawning the reviser):

    PROTOCOL_COMMENT_ID    — the comment link being closed
    PROTOCOL_ASN_LABEL     — the ASN label (for rationale doc placement)

The doc the resolution applies to is derived by reading the comment's
`to_set` from the substrate; callers do not pass a path string. On
reject, materializes the rationale document under
_docuverse/documents/rationale/{ASN}/{comment_id}.md and writes a
resolution.reject link binding the comment and the rationale.

Prints the new resolution link id on success; exits non-zero on error.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import LATTICE, RATIONALE_DIR
from lib.protocols.febe.session import open_session
from lib.backend.addressing import Address


def emit_decision(session, action, comment_addr, claim_addr, asn_label,
                  rationale=None):
    """File the resolution link closing a revise comment.

    accept → resolution.edit (F=[claim], G=[comment]).
    reject → writes rationale to <RATIONALE_DIR>/<asn>/<comment>.md, then
             emits resolution.reject (F=[claim], G=[comment, rationale]).
    """
    if action == "accept":
        return session.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr],
            type_="resolution",
            subtype="edit",
        )

    if action == "reject":
        if not rationale:
            raise ValueError("reject requires rationale text")
        rationale_path = Path(RATIONALE_DIR) / asn_label / f"{comment_addr}.md"
        lattice_root = session.store.lattice_dir.resolve()
        rationale_rel = str(rationale_path.resolve().relative_to(lattice_root))
        session.update_document(rationale_rel, rationale + "\n")
        rationale_addr = session.register_path(rationale_rel)
        return session.make_link(
            homedoc=claim_addr,
            from_set=[claim_addr],
            to_set=[comment_addr, rationale_addr],
            type_="resolution",
            subtype="reject",
        )

    raise ValueError(f"unknown action: {action!r}")


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
    asn_label = os.environ.get("PROTOCOL_ASN_LABEL")
    if not comment_id:
        print("error: --comment-id or PROTOCOL_COMMENT_ID required", file=sys.stderr)
        return 1
    if not asn_label:
        print("error: PROTOCOL_ASN_LABEL env var not set", file=sys.stderr)
        return 1

    session = open_session(LATTICE)
    # Comment id is a tumbler-address string in the new substrate.
    try:
        comment_addr = Address(comment_id)
    except (ValueError, TypeError) as e:
        print(f"error: invalid comment id {comment_id!r}: {e}",
              file=sys.stderr)
        return 1
    try:
        comment = session.get_link(comment_addr)
    except KeyError:
        print(f"error: comment {comment_id} not found in substrate",
              file=sys.stderr)
        return 1
    if not comment.to_set:
        print(f"error: comment {comment_id} has empty to_set",
              file=sys.stderr)
        return 1
    claim_addr = comment.to_set[0]

    try:
        link = emit_decision(
            session, args.action, comment_addr, claim_addr, asn_label,
            rationale=getattr(args, "rationale", None),
        )
    except (KeyError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    # An accept means an edit happened. Bump the claim's version
    # marker (LM 4/52-4/53) so downstream predicates can detect that
    # claim-derived attributes (description, etc.) are stale relative
    # to the new revision.
    if args.action == "accept":
        session.register_version(claim_addr)

    print(link.addr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
