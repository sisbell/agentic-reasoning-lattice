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
    python scripts/note-scheduler.py --dag    # all active notes, topo-sorted

`--dag` mode auto-discovers every active note (one whose body file
exists under `_docuverse/.../note/`), queries substrate for
note-to-note `citation.depends` edges, and walks the topological
order so foundations process before their dependents.
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
    "inquiry_consult",
    "note_draft",
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


def _active_notes_topo_sorted() -> list[str]:
    """Discover every active note (body file present, not substrate-retired)
    and return its ASN label list in topological order — foundations before
    their dependents per substrate `citation.depends` edges.

    "Active" = body file on disk AND the note's substrate address does not
    carry the `retired` classifier. Notes with no edges land at the end
    (stable order). Notes whose dependency target isn't itself active are
    treated as having no dep on it.
    """
    from glob import glob
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE
    from lib.backend.predicates import active_links
    from lib.predicates import is_retired

    discovered: set[str] = set()
    asn_pat = re.compile(r"(ASN-\d{4})")
    for f in glob("_docuverse/documents/**/note/ASN-*.md", recursive=True):
        if ".statements.md" in f or ".motif." in f:
            continue
        m = asn_pat.search(f)
        if m:
            discovered.add(m.group(1))
    # Also discover ASNs that have an inquiry but no note yet (pre-draft
    # state — note_draft fires on these, the cycle triggers skip cleanly
    # because their per-note scope queries yield empty).
    for f in glob("_docuverse/documents/**/inquiry/ASN-*.md", recursive=True):
        m = asn_pat.search(f)
        if m:
            discovered.add(m.group(1))

    # Filter out substrate-retired notes; collect edges via citation.depends
    with open_session(LATTICE) as session:
        state = session.store
        # Resolve each ASN to its note address and check retirement.
        # For inquiry-only ASNs (no note yet), check retirement on the
        # inquiry address — retirement is the operator's signal to the
        # walker regardless of which doc carries it.
        active: set[str] = set()
        for asn in discovered:
            note_addr = None
            for path, addr in state.path_to_addr.items():
                if f"/note/{asn}-" in path and not path.endswith(".statements.md"):
                    note_addr = addr
                    break
            if note_addr is None:
                inquiry_rel = (
                    f"_docuverse/documents/1.1/1/inquiry/{asn}.md"
                )
                inquiry_addr = state.path_to_addr.get(inquiry_rel)
                if inquiry_addr is None or not is_retired(session, inquiry_addr):
                    active.add(asn)
                continue
            if not is_retired(session, note_addr):
                active.add(asn)

        edges: dict[str, set[str]] = {a: set() for a in active}
        for link in active_links(state, "citation.depends"):
            from_asns: set[str] = set()
            to_asns: set[str] = set()
            for a in link.from_set:
                p = state.path_for_addr(a)
                if p:
                    m = asn_pat.search(p)
                    if m:
                        from_asns.add(m.group(1))
            for a in link.to_set:
                p = state.path_for_addr(a)
                if p:
                    m = asn_pat.search(p)
                    if m:
                        to_asns.add(m.group(1))
            for f in from_asns & active:
                for t in to_asns & active:
                    if f != t:
                        edges[f].add(t)

    # Kahn's algorithm — pop nodes with no remaining out-deps
    sorted_list: list[str] = []
    remaining = {a: set(edges[a]) for a in active}
    while remaining:
        # find nodes with no unresolved deps
        ready = sorted(a for a, deps in remaining.items() if not deps)
        if not ready:
            # cycle (shouldn't happen with citation.depends); break by
            # taking everything left in lexical order
            ready = sorted(remaining.keys())
        for a in ready:
            sorted_list.append(a)
            remaining.pop(a)
        # remove resolved nodes from others' dep sets
        for a in remaining:
            remaining[a] -= set(ready)
    return sorted_list


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="note-scheduler",
        description=(
            "Walk the note review/consult/revise cycle across a set "
            "of ASNs to fixed-point quiescence."
        ),
    )
    parser.add_argument(
        "asns", nargs="*", metavar="ASN",
        help="One or more ASN numbers (e.g., 34 36 40). Omit with --dag.",
    )
    parser.add_argument(
        "--dag", action="store_true",
        help=(
            "Auto-discover every active note (body file present) and "
            "process in topological order from substrate "
            "citation.depends edges. Ignores positional ASN args."
        ),
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
    parser.add_argument(
        "--partition", metavar="I/N", default=None,
        help=(
            "Process only the round-robin partition I out of N total. "
            "Requires --dag. Example: --partition 0/2 takes ASNs at "
            "topo positions 0, 2, 4, ...; --partition 1/2 takes 1, 3, 5, ...."
        ),
    )
    parser.add_argument(
        "--exclude", metavar="CLASSES", default=None,
        help=(
            "Comma-separated class labels to exclude from the walk. "
            "Any class declared in the YAML is valid (plus 'core' for the implicit-default set). "
            "Class membership is read from _workspace/asn-classes.yaml. "
            "Example: --exclude operations,protocols restricts to core."
        ),
    )
    args = parser.parse_args()

    from lib.shared.asn_classes import apply_exclude, parse_exclude_arg
    try:
        excluded_classes = parse_exclude_arg(args.exclude)
    except ValueError as exc:
        parser.error(str(exc))

    partition_index = None
    partition_total = None
    if args.partition is not None:
        try:
            partition_index, partition_total = [
                int(x) for x in args.partition.split("/", 1)
            ]
        except (ValueError, IndexError):
            parser.error(f"invalid --partition value {args.partition!r}; "
                         f"expected I/N (e.g., 0/2)")
        if partition_total < 1:
            parser.error("--partition N must be >= 1")
        if not (0 <= partition_index < partition_total):
            parser.error(f"--partition I must be in [0, {partition_total - 1}]")

    if args.dag:
        asn_labels = _active_notes_topo_sorted()
        if not asn_labels:
            print("  [NOTE-SCHED] --dag: no active notes found",
                  file=sys.stderr)
            return 0
        if excluded_classes:
            before = len(asn_labels)
            asn_labels = apply_exclude(asn_labels, excluded_classes)
            print(
                f"  [NOTE-SCHED] --exclude {','.join(sorted(excluded_classes))}: "
                f"{before} → {len(asn_labels)} ASNs",
                file=sys.stderr,
            )
        if partition_index is not None:
            asn_labels = [
                asn_labels[i] for i in range(len(asn_labels))
                if i % partition_total == partition_index
            ]
            if not asn_labels:
                print(
                    f"  [NOTE-SCHED] --partition {partition_index}/{partition_total}: "
                    f"empty partition",
                    file=sys.stderr,
                )
                return 0
    else:
        if partition_index is not None:
            parser.error("--partition requires --dag")
        if excluded_classes:
            parser.error("--exclude requires --dag")
        if not args.asns:
            parser.error("ASN(s) required, or use --dag")
        asn_labels = [_parse_asn(a) for a in args.asns]
    triggers = _note_cycle_triggers()

    # Inherited-env banner: surface CLAUDE_WORKER_INDEX, partition, and
    # CLAUDE_CONFIG_DIRS so each worker visibly logs what it inherited
    # from its spawn. Useful when debugging hot-reload of WORKERS or
    # accounts via _workspace/runner.env, or when one worker's behavior
    # diverges from another's.
    import os as _os
    worker_idx = _os.environ.get("CLAUDE_WORKER_INDEX", "(unset)")
    config_dirs = _os.environ.get("CLAUDE_CONFIG_DIRS", "(unset)")
    partition_str = (
        f"{partition_index}/{partition_total}"
        if partition_index is not None else "(none)"
    )
    print(
        f"  [NOTE-SCHED] worker_idx={worker_idx} partition={partition_str} "
        f"CLAUDE_CONFIG_DIRS={config_dirs}",
        file=sys.stderr,
    )
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
            if result.shutdown:
                elapsed = time.time() - overall_start
                print(
                    f"\n  [NOTE-SCHED] graceful shutdown after "
                    f"{len(result.fires)} fire(s) on {asn_label}; "
                    f"total_fires={total_fires} "
                    f"errors={len(total_errors)} ({elapsed:.0f}s)",
                    file=sys.stderr,
                )
                return 0 if not total_errors else 1
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
