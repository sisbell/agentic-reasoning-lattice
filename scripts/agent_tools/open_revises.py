#!/usr/bin/env python3
"""List unresolved revise comments for a note.

Output (one line per open revise, tab-separated):
    <comment_id>\t<title>

If no open revises, prints nothing and exits 0.

Usage:
    python3 scripts/agent_tools/open_revises.py <asn>
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.claim_convergence.predicates import unresolved_revise_comments
from lib.backend.store import Store
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asn")
    args = ap.parse_args()

    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"ERROR: ASN not found: {args.asn}", file=sys.stderr)
        sys.exit(1)

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
    store = Store(LATTICE)
    note_addr = store.addr_for_path(note_rel)

    for c in unresolved_revise_comments(store.state, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        finding_rel = store.path_for_addr(finding_addr)
        if not finding_rel:
            continue
        finding_full = LATTICE / finding_rel
        if not finding_full.exists():
            print(f"  [SKIP] finding doc missing: {finding_rel}",
                  file=sys.stderr)
            continue
        body = finding_full.read_text().strip()
        first_line = body.splitlines()[0] if body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"
        print(f"{c.addr}\t{title}")


if __name__ == "__main__":
    main()
