#!/usr/bin/env python3
"""Note-scheduler — meta-runner for the note review/consult/revise cycle.

Walks `note_review`, `note_consult`, `note_revise`, and `note_statements`
against each requested ASN's source note, repeating until no ASN in the
set fires anything in a complete outer pass. Narrower sibling of
`scheduler.py`, which walks the full registry.

`note_statements` carries a `confirmation_gate=True` predicate — it
stays quiescent during active revise cycles and fires only at the N+1
boundary (no open revises + latest review CONVERGED). The scheduler
runs it alongside the cycle so the statements sidecar refreshes
automatically once the cycle settles.

Same outer fixed-point semantics: cross-ASN cascade is handled by the
outer loop. Predicates handle ordering within the inner pass.

Usage:
    python scripts/note-scheduler.py 40
    python scripts/note-scheduler.py 34 36 40 --max-outer 6
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import triggers as triggers_module
from lib.runner import Scope, Trigger, run_until_quiescent


NOTE_CYCLE_TRIGGER_NAMES = (
    "note_review", "note_consult", "note_revise", "note_statements",
)


def _note_cycle_triggers() -> list[Trigger]:
    """Resolve the note-cycle triggers from the registry.

    note_statements has a `confirmation_gate=True` predicate: it stays
    quiescent during active revise cycles and fires once the cycle
    settles (no open revises + latest review CONVERGED). Including it
    in the same outer loop lets the scheduler walk past the N+1
    boundary without operator intervention.
    """
    found = []
    for name in NOTE_CYCLE_TRIGGER_NAMES:
        trig = getattr(triggers_module, name, None)
        if not isinstance(trig, Trigger):
            raise SystemExit(
                f"trigger {name!r} not found in lib.triggers registry"
            )
        found.append(trig)
    return found


def _parse_asn(raw: str) -> str:
    from lib.lattice.labels import format_label
    digits = re.sub(r"\D", "", raw)
    if not digits:
        raise SystemExit(f"invalid ASN: {raw!r}")
    return format_label(int(digits))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="note-scheduler",
        description=(
            "Walk the note review/consult/revise cycle across a set "
            "of ASNs to fixed-point quiescence."
        ),
    )
    parser.add_argument(
        "asns", nargs="+", metavar="ASN",
        help="One or more ASN numbers (e.g., 34 36 40)",
    )
    parser.add_argument(
        "--max-outer", type=int, default=20,
        help="Cap on outer fixed-point iterations (default 20)",
    )
    parser.add_argument(
        "--max-inner", type=int, default=100,
        help="Cap on per-ASN runner passes (default 100)",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the per-fire auto-commit (default: commit after each fire).",
    )
    args = parser.parse_args()

    asn_labels = [_parse_asn(a) for a in args.asns]
    triggers = _note_cycle_triggers()

    print(
        f"  [NOTE-SCHED] {len(triggers)} triggers across "
        f"{len(asn_labels)} ASNs: {', '.join(asn_labels)}",
        file=sys.stderr,
    )

    total_fires = 0
    total_errors: list[tuple[str, str, str, str]] = []
    inner_capped: set[str] = set()
    overall_start = time.time()

    for outer in range(args.max_outer):
        print(
            f"\n  [NOTE-SCHED] outer pass {outer + 1}",
            file=sys.stderr,
        )
        fired_any = False
        for asn_label in asn_labels:
            scope = Scope(asn_label=asn_label)
            inner_start = time.time()
            result = run_until_quiescent(
                triggers=triggers,
                scope=scope,
                max_iterations=args.max_inner,
                auto_commit=not args.no_commit,
            )
            elapsed = time.time() - inner_start
            print(
                f"  [NOTE-SCHED] {asn_label}: "
                f"iters={result.iterations} fires={len(result.fires)} "
                f"errors={len(result.errors)} "
                f"quiescent={result.quiescent} ({elapsed:.0f}s)",
                file=sys.stderr,
            )
            total_fires += len(result.fires)
            for trig_name, addr, exc in result.errors:
                total_errors.append((asn_label, trig_name, addr, exc))
            if result.fires:
                fired_any = True
            if not result.quiescent:
                inner_capped.add(asn_label)
                fired_any = True
        if not fired_any:
            elapsed = time.time() - overall_start
            print(
                f"\n  [NOTE-SCHED] quiescent across all ASNs after "
                f"{outer + 1} outer passes; total_fires={total_fires} "
                f"errors={len(total_errors)} ({elapsed:.0f}s)",
                file=sys.stderr,
            )
            return 0 if not total_errors else 1

    elapsed = time.time() - overall_start
    print(
        f"\n  [NOTE-SCHED] hit max-outer={args.max_outer} without "
        f"fixed-point quiescence; total_fires={total_fires} "
        f"errors={len(total_errors)} inner_capped={sorted(inner_capped)} "
        f"({elapsed:.0f}s)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
