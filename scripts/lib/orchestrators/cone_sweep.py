"""Cone-sweep orchestrator — bottom-up DAG walk reviewing every qualifying cone.

Walks the dependency DAG bottom-up, running focused regional reviews
on claims with >= min_deps same-ASN dependencies. Process in
topological order (foundations first) so each cone's dependencies are
stable when it runs. Resumable via progress.json.
"""

from __future__ import annotations

import sys
import time

from lib.claim_convergence.core.build_dependency_graph import (
    generate_claim_convergence_deps,
)
from lib.claim_convergence.core.topological_sort import topological_levels
from lib.claim_convergence.sweep_progress import (
    clear_progress, read_progress, write_progress,
)
from lib.febe.session import open_session
from lib.lattice.labels import build_cross_asn_label_index
from lib.orchestrators.cone_review import run_cone_review
from lib.predicates import is_claim_converged
from lib.shared.common import build_label_index, find_asn
from lib.shared.paths import CLAIM_DIR, LATTICE


def run_cone_sweep(
    asn_num, min_deps=4, max_cycles=8, dry_run=False,
    model="sonnet", all_mode=False,
):
    """Proactive cone-scope sweep — bottom-up DAG walk.

    For each claim with >= min_deps same-ASN dependencies, run a cone
    review. Process in topological order (foundations first) so each
    cone's dependencies are stable when it runs.

    Resumable: writes progress to
    `_workspace/cone-sweep/<asn>/progress.json` at apex transitions.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(
            f"  No claim-convergence directory for {asn_label}",
            file=sys.stderr,
        )
        return "failed"

    deps_data = generate_claim_convergence_deps(asn_num)
    if not deps_data:
        print(f"  No dependency data for {asn_label}", file=sys.stderr)
        return "failed"

    levels = topological_levels(deps_data)
    asn_labels = set(build_label_index(claim_dir).keys())

    if all_mode:
        clear_progress(asn_label)
        completed = set()
    else:
        saved = read_progress(asn_label)
        completed = set(saved.get("completed", [])) if saved else set()
        if completed:
            print(
                f"\n  [REGIONAL-SWEEP] resuming — {len(completed)} "
                f"apex(es) already done in this sweep",
                file=sys.stderr,
            )

    print(
        f"\n  [REGIONAL-SWEEP] {asn_label} — {len(asn_labels)} claims, "
        f"min_deps={min_deps}{'  --all' if all_mode else ''}",
        file=sys.stderr,
    )

    start_time = time.time()
    cones_reviewed = 0
    cones_skipped = 0
    any_not_converged = False

    session = open_session(LATTICE)
    label_index = build_cross_asn_label_index(session.store)
    rev_index = {addr: label for label, addr in label_index.items()}

    for level_idx, level_labels in enumerate(levels):
        for label in level_labels:
            from_addr = label_index.get(label)
            if from_addr is None:
                continue
            same_deps = [
                rev_index[link.to_set[0]]
                for link in session.active_links(
                    "citation.depends", from_set=[from_addr],
                )
                if link.to_set
                and rev_index.get(link.to_set[0]) in asn_labels
            ]
            if len(same_deps) < min_deps:
                continue

            if label in completed:
                cones_skipped += 1
                continue

            if all_mode:
                cones_reviewed += 1
                result = run_cone_review(
                    asn_num, label, same_deps,
                    max_cycles=max_cycles, dry_run=dry_run, model=model,
                )
                if result != "converged":
                    any_not_converged = True
            elif is_claim_converged(session, from_addr):
                print(
                    f"  [REGIONAL-SWEEP] {label}: predicate True, skipping",
                    file=sys.stderr,
                )
                cones_skipped += 1
            else:
                cones_reviewed += 1
                result = run_cone_review(
                    asn_num, label, same_deps,
                    max_cycles=max_cycles, dry_run=dry_run, model=model,
                )
                if result != "converged":
                    any_not_converged = True

            # Re-load session since run_cone_review may have appended
            # links to the JSONL while running.
            session = open_session(LATTICE)
            from_addr = (
                session.store.path_to_addr.get(
                    session.get_path_for_addr(from_addr) or "",
                    from_addr,
                ) if from_addr else None
            )
            if (
                from_addr is not None
                and is_claim_converged(session, from_addr)
            ):
                completed.add(label)
                write_progress(
                    asn_label, {"completed": sorted(completed)},
                )

    elapsed = time.time() - start_time
    if cones_reviewed == 0 and cones_skipped == 0:
        print(
            f"\n  [REGIONAL-SWEEP] No claims with >= {min_deps} "
            f"same-ASN deps.", file=sys.stderr,
        )
    else:
        print(
            f"\n  [REGIONAL-SWEEP] {cones_reviewed} reviewed, "
            f"{cones_skipped} skipped, in {elapsed:.0f}s",
            file=sys.stderr,
        )

    if not dry_run:
        clear_progress(asn_label)

    return "not_converged" if any_not_converged else "converged"
