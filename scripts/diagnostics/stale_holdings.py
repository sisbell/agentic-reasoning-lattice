#!/usr/bin/env python3
"""Report active `holding` links open longer than a threshold —
observability for stuck agent fires.

When an agent acquires a `holding` on a resource and crashes (or is
killed) mid-fire, the retraction never lands and the holding stays
active. Future agent fires that gate on `is_held` skip indefinitely
on the affected resource. This diagnostic surfaces those stuck
holdings so the operator can investigate or manually retract.

Usage:
    # Operator-facing report (verbose: prints when clean too)
    python3 scripts/diagnostics/stale_holdings.py
    python3 scripts/diagnostics/stale_holdings.py --threshold 600

    # Runner-facing check (silent when clean, loud banner when stuck)
    python3 scripts/diagnostics/stale_holdings.py --quiet

    # Retract a specific orphan holding
    python3 scripts/diagnostics/stale_holdings.py --retract <holding_addr>

Exits 0 in all observation modes (this is observability, not an error
condition). `--retract` exits 1 if the target holding can't be found.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import emit_retraction
from lib.predicates.agents import stale_holdings
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


def _format_age(seconds: int) -> str:
    """Human-readable duration: '14h 32m' / '45m' / '12s'."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    return f"{hours}h {minutes % 60:02d}m"


def _resolve_label(session, addr) -> str:
    """Render an address as repo-relative path if known, else raw."""
    try:
        path = session.store.path_for_addr(addr)
    except Exception:
        path = None
    return path if path else str(addr)


_WIDTH = 64


def _bline(text: str) -> str:
    """Render one banner inner line, padded to _WIDTH between ║ chars."""
    return f"  ║{text.ljust(_WIDTH)}║"


def _print_banner(session, stuck, threshold: int, now: int) -> None:
    """Loud banner for cycle-start use. Repeats every outer cycle until
    the operator retracts the orphans — that's the "loud" part."""
    bar = "═" * _WIDTH
    print("", file=sys.stderr)
    print(f"  ╔{bar}╗", file=sys.stderr)
    header = (
        f"  STUCK HOLDINGS — {len(stuck)} orphan(s) "
        f"open >{_format_age(threshold)}"
    )
    print(_bline(header), file=sys.stderr)
    print(f"  ╠{bar}╣", file=sys.stderr)
    for link in stuck:
        resource = link.to_set[0] if link.to_set else None
        age = now - link.ts if link.ts is not None else 0
        label = _resolve_label(session, resource) if resource else "?"
        if len(label) > 38:
            label = "..." + label[-35:]
        print(_bline(f"  {label}  held {_format_age(age)} ago"),
              file=sys.stderr)
    print(_bline(""), file=sys.stderr)
    print(_bline("  Resources blocked until holdings retracted. Investigate."),
          file=sys.stderr)
    print(_bline(""), file=sys.stderr)
    print(_bline("  Retract:"), file=sys.stderr)
    for link in stuck:
        cmd = (
            f"    scripts/diagnostics/stale_holdings.py "
            f"--retract {link.addr}"
        )
        if len(cmd) > _WIDTH:
            # Address is long; split onto its own line.
            print(_bline(
                "    scripts/diagnostics/stale_holdings.py --retract \\"
            ), file=sys.stderr)
            print(_bline(f"      {link.addr}"), file=sys.stderr)
        else:
            print(_bline(cmd), file=sys.stderr)
    print(f"  ╚{bar}╝", file=sys.stderr)
    print("", file=sys.stderr)


def _retract(session, target_addr: Address) -> int:
    """Emit a retraction for a single holding. Returns exit code."""
    try:
        link = session.get_link(target_addr)
    except KeyError:
        print(
            f"  [STALE-HOLDINGS] holding {target_addr} not found",
            file=sys.stderr,
        )
        return 1

    # Sanity-check that this really is a holding link
    type_set = getattr(link, "type_set", []) or []
    if not any("holding" in str(t) or t.endswith(".35") for t in type_set):
        print(
            f"  [STALE-HOLDINGS] {target_addr} is not a holding link "
            f"(type_set={type_set})",
            file=sys.stderr,
        )
        return 1

    if not link.from_set:
        print(
            f"  [STALE-HOLDINGS] holding {target_addr} has no from_set; "
            f"cannot determine agent_doc for retraction",
            file=sys.stderr,
        )
        return 1
    agent_doc = link.from_set[0]
    retraction = emit_retraction(session.store, agent_doc, target_addr)
    session.commit()
    print(
        f"  [STALE-HOLDINGS] retracted {target_addr} via {retraction.addr}",
        file=sys.stderr,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold", type=int, default=8100,
        help="Age threshold in seconds (default: 8100 = 135 minutes, "
             "safely above the 120-minute subprocess timeout).",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Silent when no stale holdings found. Use from the runner; "
             "operator-facing manual invocations should omit.",
    )
    parser.add_argument(
        "--retract",
        help="Retract the given holding address (manual recovery from "
             "an orphan). Skips threshold check — operator-authorized.",
    )
    args = parser.parse_args()

    with open_session(LATTICE) as session:
        if args.retract:
            return _retract(session, Address(args.retract))

        now = int(time.time())
        stuck = stale_holdings(session, args.threshold)

        if not stuck:
            if not args.quiet:
                print(
                    f"  [STALE-HOLDINGS] none open "
                    f">{_format_age(args.threshold)}",
                    file=sys.stderr,
                )
            return 0

        _print_banner(session, stuck, args.threshold, now)
        return 0


if __name__ == "__main__":
    sys.exit(main())
