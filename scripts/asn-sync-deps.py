#!/usr/bin/env python3
"""Reconcile substrate `citation.depends` to match an inquiry's
frontmatter `depends:` field.

Target end state:
  - ONE fan-out `citation.depends` link from inquiry → dep notes
  - ZERO `citation.depends` links from the note address (legacy)

Reads inquiry frontmatter (the declarative spec), retracts any
substrate citation.depends that doesn't match the desired set, and
emits one bundled fan-out link. Idempotent — re-running on a
healthy ASN produces no changes.

Hard-fail: if any declared dep can't be resolved to a substrate note,
the tool refuses to emit a partial fan-out. Operator must fix the
spec (add the missing note, or correct the dep list).

Usage:
    python scripts/asn-sync-deps.py 97
    python scripts/asn-sync-deps.py 97 --dry-run
    python scripts/asn-sync-deps.py 88 89 90 92 --no-commit
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import DOCUVERSE_DIR, INQUIRY_DIR, LATTICE, WORKSPACE
from lib.shared.sync_deps import (
    SyncDepsError, apply_plan, plan_reconciliation,
)


def _print_plan(plan, *, dry_run: bool) -> None:
    label = format_label(plan.asn_num)
    print(
        f"  [{label}] declared depends: "
        f"{', '.join(f'ASN-{d:04d}' for d in plan.declared_deps) or '(none)'}",
        file=sys.stderr,
    )
    if plan.is_noop:
        print(f"  [{label}] already healthy (no-op)", file=sys.stderr)
        return
    if plan.keep_link is not None:
        print(
            f"  [{label}] existing fan-out matches — keeping {plan.keep_link.addr}",
            file=sys.stderr,
        )
    if plan.retract_inquiry:
        print(
            f"  [{label}] will retract {len(plan.retract_inquiry)} "
            f"inquiry-side citation.depends link(s):",
            file=sys.stderr,
        )
        for L in plan.retract_inquiry:
            print(
                f"      - {L.addr} (to_set len={len(L.to_set)})",
                file=sys.stderr,
            )
    if plan.retract_note:
        print(
            f"  [{label}] will retract {len(plan.retract_note)} "
            f"note-side citation.depends link(s) (legacy):",
            file=sys.stderr,
        )
        for L in plan.retract_note:
            print(
                f"      - {L.addr} (to_set len={len(L.to_set)})",
                file=sys.stderr,
            )
    if plan.needs_emit:
        targets = ", ".join(f"ASN-{d:04d}" for d in plan.declared_deps)
        print(
            f"  [{label}] will emit fan-out citation.depends → {targets}",
            file=sys.stderr,
        )
    if dry_run:
        print(f"  [{label}] [DRY RUN] no substrate changes", file=sys.stderr)


def _print_result(result, *, label: str) -> None:
    actions = []
    if result.retracted_inquiry:
        actions.append(f"retracted inquiry={result.retracted_inquiry}")
    if result.retracted_note:
        actions.append(f"retracted note={result.retracted_note}")
    if result.emitted:
        actions.append("emitted fan-out")
    if result.kept_existing and not actions:
        actions.append("kept existing fan-out (no-op)")
    summary = ", ".join(actions) if actions else "no changes"
    print(f"  [{label}] sync: {summary}", file=sys.stderr)


def sync(asn_num: int, *, dry_run: bool = False) -> int:
    label = format_label(asn_num)
    try:
        with open_session(LATTICE) as session:
            plan = plan_reconciliation(session, asn_num)
            _print_plan(plan, dry_run=dry_run)
            if dry_run:
                return 0
            result = apply_plan(session, plan)
            _print_result(result, label=label)
    except SyncDepsError as e:
        print(f"  [{label}] [ERROR] {e}", file=sys.stderr)
        return 1
    return 0


def _stage_for_commit(asn_nums: list[int]) -> None:
    paths = []
    for n in asn_nums:
        label = format_label(n)
        paths.append(str(
            (INQUIRY_DIR / f"{label}.md").resolve()
            .relative_to(WORKSPACE.resolve())
        ))
    paths += [
        str((DOCUVERSE_DIR / "links.jsonl").resolve()
            .relative_to(WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "paths.json").resolve()
            .relative_to(WORKSPACE.resolve())),
    ]
    subprocess.run(
        ["git", "add"] + paths,
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", nargs="+", type=int,
        help="One or more ASN numbers to reconcile",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show the reconciliation plan without writing substrate",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the post-sync commit step",
    )
    args = parser.parse_args()

    rc = 0
    for n in args.asn:
        rc = sync(n, dry_run=args.dry_run) or rc

    if rc == 0 and not args.dry_run and not args.no_commit:
        _stage_for_commit(args.asn)
        label_str = ", ".join(format_label(n) for n in args.asn)
        step_commit(
            f"sync-deps(asn): reconcile citation.depends for {label_str}",
        )

    return rc


if __name__ == "__main__":
    sys.exit(main())
