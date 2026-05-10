#!/usr/bin/env python3
"""Report active `holding` links that have been open longer than a
threshold — observability for stuck agent fires.

When an agent acquires a `holding` on a resource and crashes (or is
killed) mid-fire, the retraction never lands and the holding stays
active. Future agent fires that gate on `is_held` skip indefinitely
on the affected resource. This diagnostic surfaces those stuck
holdings so the operator can investigate or manually retract.

Usage:
    python3 scripts/diagnostics/stale_holdings.py
    python3 scripts/diagnostics/stale_holdings.py --threshold 600
    python3 scripts/diagnostics/stale_holdings.py --threshold 60 --lattice materials

Output: one line per stale holding —

    HOLDING <addr>  agent=<agent_addr>  resource=<resource_addr>  age=<seconds>s

Exits 0 whether or not stale holdings were found (this is
observability, not an error condition). Operator decides whether to
investigate or manually retract.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.predicates.agents import stale_holdings
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold", type=int, default=600,
        help="Age threshold in seconds (default: 600 = 10 minutes).",
    )
    args = parser.parse_args()

    now = int(time.time())
    with open_session(LATTICE) as session:
        stuck = stale_holdings(session, args.threshold)

    if not stuck:
        print(
            f"  [STALE-HOLDINGS] none open >{args.threshold}s",
            file=sys.stderr,
        )
        return 0

    print(
        f"  [STALE-HOLDINGS] {len(stuck)} holding(s) open >{args.threshold}s:",
        file=sys.stderr,
    )
    for link in stuck:
        agent = link.from_set[0] if link.from_set else None
        resource = link.to_set[0] if link.to_set else None
        age = now - link.ts if link.ts is not None else None
        print(
            f"HOLDING {link.addr}  "
            f"agent={agent}  resource={resource}  "
            f"age={age}s"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
