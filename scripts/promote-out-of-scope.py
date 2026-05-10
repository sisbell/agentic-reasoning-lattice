#!/usr/bin/env python3
"""Promote Out-of-Scope CLI — thin dispatcher for
NotePromoteOutOfScopeAgent.

Reads OUT_OF_SCOPE items from a source ASN's reviews, asks the LLM
which warrant their own ASN, creates substrate-citizen inquiry docs
per promoted item plus a `promotion.out-of-scope` audit report.

Usage:
    python scripts/promote-out-of-scope.py 34
    python scripts/promote-out-of-scope.py 34 --dry-run
    python scripts/promote-out-of-scope.py 34 --model sonnet
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.lattice.labels import format_label
from lib.agents.producers.note_promote_out_of_scope import (
    NotePromoteOutOfScopeAgent,
)
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote review out-of-scope items into new inquiry ASNs.",
    )
    parser.add_argument("asn", help="Source ASN number")
    parser.add_argument(
        "--model", "-m", default="opus", choices=["opus", "sonnet"],
    )
    parser.add_argument(
        "--effort", default="max", help="Thinking effort level",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  {format_label(asn_num)} not found", file=sys.stderr)
        return 1

    if args.dry_run:
        print(
            f"  [DRY RUN] Would promote out-of-scope items from {asn_label} "
            f"using {args.model}",
            file=sys.stderr,
        )
        return 0

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)

        agent = NotePromoteOutOfScopeAgent(
            model=args.model, effort=args.effort,
        )
        result = agent(session, note_addr)

    step_commit_asn(asn_num, f"promote(out-of-scope): {asn_label}")

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
