#!/usr/bin/env python3
"""Claim-scheduler — meta-runner for the claim review/revise cycle.

Walks the claim-side triggers against each requested ASN's derived
claim set, repeating until no ASN in the set fires anything in a
complete outer pass. Sibling of `note-scheduler.py`; same outer
fixed-point semantics, different trigger surface.

Trigger surface:
  - Construction (post-decompose, in case cascade re-triggers):
    claim_contract, claim_formal_contract, claim_describe,
    claim_signature_resolve, claim_citation_resolve
  - Review/revise cycle:
    full_review, cone_review, claim_findings, claim_revise
  - Structural validate-gate:
    claim_structural_audit, claim_structural_revise
  - Cascade refresh:
    claim_describe_refresh, claim_signature_refresh,
    claims_statements_refresh

Per-fire auto-commit, file-based shutdown sentinel, and DAG-honoring
partition all behave exactly as in note-scheduler.py.

Usage:
    python scripts/claim-scheduler.py 36
    python scripts/claim-scheduler.py 34 36 --max-outer 6
    python scripts/claim-scheduler.py --dag    # all decomposed ASNs

`--dag` mode auto-discovers every ASN with at least one per-claim
file under `_docuverse/.../claim/ASN-NNNN/`, queries substrate for
note-to-note `citation.depends` edges (claims inherit their source
note's deps for ordering), and walks the topological order so
foundations process before their dependents.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import triggers as triggers_module
from lib.runner import (
    Scope, Trigger, compute_active_ready_partition, run_until_quiescent,
)


CLAIM_CYCLE_TRIGGER_NAMES = (
    # Construction (re-fires if cascade-fresh marks any sidecar stale)
    "claim_contract",
    "claim_formal_contract",
    "claim_describe",
    "claim_signature_resolve",
    "claim_citation_resolve",
    # Review/revise cycle
    "full_review",
    "cone_review",
    "claim_findings",
    "claim_revise",
    # Structural gate
    "claim_structural_audit",
    "claim_structural_revise",
    # Cascade refresh
    "claim_describe_refresh",
    "claim_signature_refresh",
    "claims_statements_refresh",
)


def _claim_cycle_triggers() -> list[Trigger]:
    """Resolve the claim-cycle triggers from the registry."""
    found = []
    for name in CLAIM_CYCLE_TRIGGER_NAMES:
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


def _decomposed_asns_topo_sorted() -> list[str]:
    """Discover every ASN with at least one per-claim file and return
    its label list in topological order — foundations before dependents
    per substrate `citation.depends` edges on the source notes.

    "Decomposed" = at least one `claim/ASN-NNNN/<label>.md` file exists
    on disk (excluding `_statements.md` aggregate and per-sidecar files
    like `<label>.description.md`, `<label>.signature.md`, etc.). Notes
    whose source note is substrate-retired are excluded.
    """
    from glob import glob
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE
    from lib.backend.predicates import active_links
    from lib.predicates import is_retired

    discovered: set[str] = set()
    asn_pat = re.compile(r"(ASN-\d{4})")
    # Sidecar suffixes that should NOT count as "a claim file" — they
    # ride alongside the main per-claim md and are produced by
    # construction triggers, not by decompose itself.
    sidecar_suffixes = (
        ".description.md", ".signature.md", ".references.md",
        ".label.md", ".name.md", ".contract.md",
    )
    for f in glob(
        "_docuverse/documents/**/claim/ASN-*/*.md", recursive=True,
    ):
        if f.endswith("_statements.md"):
            continue
        if any(f.endswith(suf) for suf in sidecar_suffixes):
            continue
        m = asn_pat.search(f)
        if m:
            discovered.add(m.group(1))

    # Filter out ASNs whose source note is substrate-retired, then
    # collect note-to-note edges via citation.depends for the topo sort.
    with open_session(LATTICE) as session:
        state = session.store
        active: set[str] = set()
        for asn in discovered:
            note_addr = None
            for path, addr in state.path_to_addr.items():
                if (
                    f"/note/{asn}-" in path
                    and not path.endswith(".statements.md")
                ):
                    note_addr = addr
                    break
            # If there's no source note (claim-only ASN — unusual), keep
            # it active. The triggers' scope queries will skip cleanly
            # if the note's absence makes them inapplicable.
            if note_addr is None or not is_retired(session, note_addr):
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

    # Kahn's algorithm — same as note-scheduler.
    sorted_list: list[str] = []
    remaining = {a: set(edges[a]) for a in active}
    while remaining:
        ready = sorted(a for a, deps in remaining.items() if not deps)
        if not ready:
            ready = sorted(remaining.keys())
        for a in ready:
            sorted_list.append(a)
            remaining.pop(a)
        for a in remaining:
            remaining[a] -= set(ready)
    return sorted_list


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="claim-scheduler",
        description=(
            "Walk the claim review/revise cycle across a set of ASNs "
            "to fixed-point quiescence."
        ),
    )
    parser.add_argument(
        "asns", nargs="*", metavar="ASN",
        help="One or more ASN numbers (e.g., 34 36). Omit with --dag.",
    )
    parser.add_argument(
        "--dag", action="store_true",
        help=(
            "Auto-discover every decomposed ASN (per-claim files present) "
            "and process in topological order from substrate "
            "citation.depends edges. Ignores positional ASN args."
        ),
    )
    parser.add_argument(
        "--max-outer", type=int, default=20,
        help="Cap on outer fixed-point iterations (default 20)",
    )
    parser.add_argument(
        "--empty-partition-wait", type=int, default=300,
        help=(
            "Seconds to sleep when this worker's partition is empty but "
            "peer workers have ready ASNs. Doesn't count toward "
            "--max-outer (default 300)."
        ),
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
            "Requires --dag."
        ),
    )
    parser.add_argument(
        "--exclude", metavar="CLASSES", default=None,
        help=(
            "Comma-separated class labels to exclude from the walk. "
            "Class membership is read from _workspace/asn-classes.yaml."
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
        asn_labels = _decomposed_asns_topo_sorted()
        if not asn_labels:
            print(
                "  [CLAIM-SCHED] --dag: no decomposed ASNs found "
                "(no per-claim files on disk yet)",
                file=sys.stderr,
            )
            return 0
        if excluded_classes:
            before = len(asn_labels)
            asn_labels = apply_exclude(asn_labels, excluded_classes)
            print(
                f"  [CLAIM-SCHED] --exclude {','.join(sorted(excluded_classes))}: "
                f"{before} → {len(asn_labels)} ASNs",
                file=sys.stderr,
            )
    else:
        if partition_index is not None:
            parser.error("--partition requires --dag")
        if excluded_classes:
            parser.error("--exclude requires --dag")
        if not args.asns:
            parser.error("ASN(s) required, or use --dag")
        asn_labels = [_parse_asn(a) for a in args.asns]
    triggers = _claim_cycle_triggers()

    import os as _os
    worker_idx = _os.environ.get("CLAUDE_WORKER_INDEX", "(unset)")
    config_dirs = _os.environ.get("CLAUDE_CONFIG_DIRS", "(unset)")
    partition_str = (
        f"{partition_index}/{partition_total}"
        if partition_index is not None else "(none)"
    )
    print(
        f"  [CLAIM-SCHED] worker_idx={worker_idx} partition={partition_str} "
        f"CLAUDE_CONFIG_DIRS={config_dirs}",
        file=sys.stderr,
    )
    print(
        f"  [CLAIM-SCHED] {len(triggers)} triggers across "
        f"{len(asn_labels)} ASNs: {', '.join(asn_labels)}",
        file=sys.stderr,
    )

    total_fires = 0
    total_errors: list[tuple[str, str, str, str]] = []
    inner_capped: set[str] = set()
    overall_start = time.time()

    all_asn_labels = list(asn_labels)

    outer_pass = 0
    empty_waits = 0
    while outer_pass < args.max_outer:
        if partition_index is not None:
            from lib.protocols.febe.session import open_session
            from lib.shared.paths import LATTICE
            with open_session(LATTICE) as filter_session:
                active_set, ready_topo, asn_labels = (
                    compute_active_ready_partition(
                        filter_session, all_asn_labels, triggers,
                        partition_index, partition_total,
                    )
                )
            if not active_set:
                elapsed = time.time() - overall_start
                print(
                    f"  [CLAIM-SCHED] global active set empty — full "
                    f"quiescence reached, exiting after {outer_pass} "
                    f"productive outer pass(es) ({empty_waits} empty "
                    f"waits); total_fires={total_fires} "
                    f"errors={len(total_errors)} ({elapsed:.0f}s)",
                    file=sys.stderr,
                )
                return 0 if not total_errors else 1
            if not asn_labels:
                empty_waits += 1
                print(
                    f"  [CLAIM-SCHED] partition empty "
                    f"(active={len(active_set)} ready={len(ready_topo)} "
                    f"< workers={partition_total}); sleeping "
                    f"{args.empty_partition_wait}s "
                    f"(empty-wait #{empty_waits})",
                    file=sys.stderr,
                )
                time.sleep(args.empty_partition_wait)
                continue

        outer_pass += 1
        print(
            f"\n  [CLAIM-SCHED] outer pass {outer_pass}",
            file=sys.stderr,
        )
        if partition_index is not None:
            print(
                f"  [CLAIM-SCHED] active={len(active_set)} "
                f"ready={len(ready_topo)} partition={len(asn_labels)}: "
                f"{', '.join(asn_labels)}",
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
                f"  [CLAIM-SCHED] {asn_label}: "
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
                    f"\n  [CLAIM-SCHED] graceful shutdown after "
                    f"{len(result.fires)} fire(s) on {asn_label}; "
                    f"total_fires={total_fires} "
                    f"errors={len(total_errors)} ({elapsed:.0f}s)",
                    file=sys.stderr,
                )
                return 0 if not total_errors else 1
        if not fired_any and partition_index is None:
            elapsed = time.time() - overall_start
            print(
                f"\n  [CLAIM-SCHED] quiescent across all ASNs after "
                f"{outer_pass} outer passes; total_fires={total_fires} "
                f"errors={len(total_errors)} ({elapsed:.0f}s)",
                file=sys.stderr,
            )
            return 0 if not total_errors else 1

    elapsed = time.time() - overall_start
    print(
        f"\n  [CLAIM-SCHED] hit max-outer={args.max_outer} without "
        f"fixed-point quiescence; total_fires={total_fires} "
        f"empty_waits={empty_waits} errors={len(total_errors)} "
        f"inner_capped={sorted(inner_capped)} ({elapsed:.0f}s)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
