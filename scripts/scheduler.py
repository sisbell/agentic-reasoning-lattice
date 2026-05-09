#!/usr/bin/env python3
"""Scheduler — meta-runner across a set of ASNs.

Walks the full trigger registry against each requested ASN's source
note, repeating until no ASN in the set fires anything in a complete
outer pass. The outer fixed-point handles cross-ASN cascade — when
ASN-34's emission flips a predicate in ASN-36, the next outer pass
walks ASN-36 and the agent fires.

This is single-process, in-process dispatch. Multi-process topology
(supervisor + per-ASN workers) is a future arc; this is the
stepping-stone version with the same semantics.

Operator interventions (`claim_decompose`, `note_patch`, etc.) are
not in the trigger registry — they're separate one-shot CLIs.
Operator runs them as needed; the scheduler picks up the resulting
substrate state on its next outer pass.

Usage:
    python scripts/scheduler.py 34 36 40
    python scripts/scheduler.py 34 36 --max-outer 6 --max-inner 50

Args:
    ASN_LABELS — one or more ASN numbers (`34`, `0034`, `ASN-0034`).

Flags:
    --max-outer N  — cap on outer fixed-point iterations (default 20)
    --max-inner N  — cap on per-ASN runner passes (default 100)
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


def _registry_triggers() -> list[Trigger]:
    """Every Trigger instance exported by `lib.triggers`.

    Sorted by name for deterministic walk order. Predicates handle
    correctness; ordering only affects efficiency.
    """
    found = [
        v for v in vars(triggers_module).values()
        if isinstance(v, Trigger)
    ]
    return sorted(found, key=lambda t: t.name)


def _parse_asn(raw: str) -> str:
    """Normalize an ASN spec (`34`, `0034`, `ASN-0034`) to `ASN-NNNN`."""
    digits = re.sub(r"\D", "", raw)
    if not digits:
        raise SystemExit(f"invalid ASN: {raw!r}")
    return f"ASN-{int(digits):04d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="scheduler",
        description=(
            "Walk the full trigger registry across a set of ASNs to "
            "fixed-point quiescence. Single-process meta-runner."
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
    args = parser.parse_args()

    asn_labels = [_parse_asn(a) for a in args.asns]
    triggers = _registry_triggers()

    print(
        f"  [SCHEDULER] {len(triggers)} triggers across "
        f"{len(asn_labels)} ASNs: {', '.join(asn_labels)}",
        file=sys.stderr,
    )

    total_fires = 0
    total_errors: list[tuple[str, str, str, str]] = []
    inner_capped: set[str] = set()
    overall_start = time.time()

    for outer in range(args.max_outer):
        print(
            f"\n  [SCHEDULER] outer pass {outer + 1}",
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
            )
            elapsed = time.time() - inner_start
            print(
                f"  [SCHEDULER] {asn_label}: "
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
                f"\n  [SCHEDULER] quiescent across all ASNs after "
                f"{outer + 1} outer passes; total_fires={total_fires} "
                f"errors={len(total_errors)} ({elapsed:.0f}s)",
                file=sys.stderr,
            )
            return 0 if not total_errors else 1

    elapsed = time.time() - overall_start
    print(
        f"\n  [SCHEDULER] hit max-outer={args.max_outer} without "
        f"fixed-point quiescence; total_fires={total_fires} "
        f"errors={len(total_errors)} inner_capped={sorted(inner_capped)} "
        f"({elapsed:.0f}s)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
