#!/usr/bin/env python3
"""Motif — operator-gated CLI that fires the MotifAgent.

Usage:
    python scripts/motif.py 34 36 40
    python scripts/motif.py 59 61 65 67 --model opus --effort high

The agent scouts the input notes for like-claim correspondences,
selects the most worthwhile motif (or rejects), and attributes it
to a base. Emissions land in substrate; nothing in workspace.

See `scripts/lib/agents/producers/motif.py` for the agent's run
semantics.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.motif import MotifAgent
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_asns", nargs="+", type=int,
        help="ASN numbers of input notes to scout for motifs",
    )
    parser.add_argument(
        "--model", "-m", default="opus", choices=["opus", "sonnet"],
    )
    parser.add_argument(
        "--effort", default="high",
        help="Thinking effort (max | high | medium | low | none)",
    )
    parser.add_argument("--lattice", default=None)  # consumed by paths.py
    args = parser.parse_args()

    agent = MotifAgent(model=args.model, effort=args.effort)
    with open_session(LATTICE) as session:
        result = agent(session, addr=None, input_asns=args.input_asns)

    print(
        f"  [MOTIF] success={result.success}  detail={result.detail}",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
