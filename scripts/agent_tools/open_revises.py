#!/usr/bin/env python3
"""List unresolved revise comments for a note.

Output (one line per open revise, tab-separated):
    <comment_id>\t<title>

If no open revises, prints nothing and exits 0.

Usage:
    python3 scripts/agent_tools/open_revises.py <asn>
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.note_convergence.revise import collect_open_revises
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE
from lib.store.store import default_store


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asn")
    args = ap.parse_args()

    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"ERROR: ASN not found: {args.asn}", file=sys.stderr)
        sys.exit(1)

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
    with default_store() as store:
        items = collect_open_revises(store, note_rel)

    for comment_id, title, _body in items:
        print(f"{comment_id}\t{title}")


if __name__ == "__main__":
    main()
