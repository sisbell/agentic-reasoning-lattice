#!/usr/bin/env python3
"""Motif dispatch — fire MotifDispatchAgent on a specific motif.

Reads the motif + its attribution sidecar, determines case 1/2/STANDALONE
mechanically, and emits operational specs into substrate. Currently
implements Case 1 (patches) only.

Usage:
    python scripts/motif-dispatch.py motif-0001
    python scripts/motif-dispatch.py motif-0003 --model opus --effort high

Eventually predicate-fired by the runner; this CLI exists for now
to test in isolation before trigger wiring.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.motif_dispatch import MotifDispatchAgent
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE, MOTIF_DIR, WORKSPACE


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "motif_label",
        help="Motif filename stem (e.g. motif-0001) or full path",
    )
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="high")
    parser.add_argument("--lattice", default=None)
    args = parser.parse_args()

    label = args.motif_label
    if "/" in label or label.endswith(".md"):
        motif_path = Path(label)
    else:
        motif_path = MOTIF_DIR / f"{label}.md"
    if not motif_path.exists():
        print(f"  motif not found at {motif_path}", file=sys.stderr)
        return 1

    rel = str(motif_path.resolve().relative_to(WORKSPACE.resolve()))
    agent = MotifDispatchAgent(model=args.model, effort=args.effort)
    with open_session(LATTICE) as session:
        motif_addr = session.store.path_to_addr.get(rel)
        if motif_addr is None:
            print(f"  motif not registered in substrate: {rel}",
                  file=sys.stderr)
            return 1
        result = agent(session, motif_addr)

    print(
        f"  [MOTIF-DISPATCH] success={result.success}  "
        f"detail={result.detail}",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
