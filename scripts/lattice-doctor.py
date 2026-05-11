#!/usr/bin/env python3
"""Lattice doctor — read-only substrate health check.

Runs every registered check against the active substrate, prints any
issues grouped by severity, exits 0 when no ERROR-level issues are
found and 1 otherwise. Read-only: never modifies substrate state or
working tree.

Usage:
    python scripts/lattice-doctor.py
    python scripts/lattice-doctor.py --stale-threshold 60
    python scripts/lattice-doctor.py --lattice materials

The doctor catches inconsistencies that don't crash queries but
violate protocol invariants the substrate doesn't itself enforce
— for example, a doc whose parent-map version head disagrees with
its supersession-link chain head (a real bug as of 2026-05-10
introduced when `_reattach_doc_owners` was added without parent-map
reconstruction).

Each check is implemented in `scripts/lib/doctor/<name>.py` and
returns Issue objects with `severity` (ERROR | WARNING | INFO),
`check` (short id), and `message` (human description). Add new
checks by writing the function and registering it below.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.doctor import Severity, run_checks
from lib.doctor import aggregate_anchor_coverage as anchor_coverage_check
from lib.doctor import citation_targets as citation_targets_check
from lib.doctor import claim_statements_bridge as bridge_check
from lib.doctor import holdings as holdings_check
from lib.doctor import review_coverage as review_coverage_check
from lib.doctor import trigger_agent_scope as trigger_scope_check
from lib.doctor import version_graph as version_graph_check
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


# Registry of (check_fn, name, description) — the description is
# printed once per check group, so per-issue messages stay terse.
def _build_registry(stale_threshold: int):
    return [
        (
            version_graph_check.check_version_graph,
            version_graph_check.CHECK_NAME,
            version_graph_check.CHECK_DESCRIPTION,
        ),
        (
            bridge_check.check_claim_statements_bridge,
            bridge_check.CHECK_NAME,
            bridge_check.CHECK_DESCRIPTION,
        ),
        (
            anchor_coverage_check.check_aggregate_anchor_coverage,
            anchor_coverage_check.CHECK_NAME,
            anchor_coverage_check.CHECK_DESCRIPTION,
        ),
        (
            citation_targets_check.check_citation_targets_exist,
            citation_targets_check.CHECK_NAME,
            citation_targets_check.CHECK_DESCRIPTION,
        ),
        (
            review_coverage_check.check_review_coverage,
            review_coverage_check.CHECK_NAME,
            review_coverage_check.CHECK_DESCRIPTION,
        ),
        (
            trigger_scope_check.check_trigger_agent_scope_alignment,
            trigger_scope_check.CHECK_NAME,
            trigger_scope_check.CHECK_DESCRIPTION,
        ),
        (
            lambda s: holdings_check.check_stale_holdings(s, stale_threshold),
            holdings_check.CHECK_NAME,
            holdings_check.CHECK_DESCRIPTION,
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stale-threshold", type=int, default=600,
        help="Holding-age threshold in seconds (default: 600 = 10 min).",
    )
    args = parser.parse_args()

    registry = _build_registry(args.stale_threshold)
    descriptions = {name: desc for _fn, name, desc in registry}

    with open_session(LATTICE) as session:
        issues = run_checks(session, [fn for fn, _, _ in registry])

    counts = {s: 0 for s in Severity}
    for issue in issues:
        counts[issue.severity] += 1

    for severity in (Severity.ERROR, Severity.WARNING, Severity.INFO):
        bucket = [i for i in issues if i.severity is severity]
        if not bucket:
            continue
        print(f"\n=== {severity.value} ({len(bucket)}) ===",
              file=sys.stderr, flush=True)
        # Group by check, print the description once, then one line per issue.
        by_check: dict = {}
        for issue in bucket:
            by_check.setdefault(issue.check, []).append(issue)
        for check_name, items in by_check.items():
            print(f"\n  [{check_name}] {descriptions.get(check_name, '')}",
                  file=sys.stderr, flush=True)
            for issue in items:
                print(f"    {issue.message}", flush=True)

    print(
        f"\n[DOCTOR] {counts[Severity.ERROR]} error(s) "
        f"{counts[Severity.WARNING]} warning(s) "
        f"{counts[Severity.INFO]} info",
        file=sys.stderr,
    )
    return 1 if counts[Severity.ERROR] else 0


if __name__ == "__main__":
    sys.exit(main())
