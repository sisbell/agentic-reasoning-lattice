"""Cone sweep — bottom-up DAG walk reviewing every qualifying cone."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import CLAIM_DIR
from lib.shared.common import find_asn, build_label_index
from lib.claim_convergence.core.build_dependency_graph import generate_claim_convergence_deps
from lib.claim_convergence.core.topological_sort import topological_levels
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import is_claim_converged, active_links
from lib.store.store import Store

from .review import run_cone_review


def run_cone_sweep(asn_num, min_deps=4, max_cycles=8, dry_run=False,
                   model="sonnet", all_mode=False):
    """Proactive cone-scope sweep — bottom-up DAG walk.

    For each claim with >= min_deps same-ASN dependencies,
    run a cone review. Process in topological order (foundations first)
    so each cone's dependencies are stable when it runs.

    Resumable: writes progress to
    `_workspace/cone-sweep/<asn>/progress.json` at apex transitions.
    On restart, skips apexes already completed in the same sweep
    (matched by min_deps + all_mode params). Within a sweep, also
    skips apexes whose convergence predicate already holds — unless
    `all_mode=True`, which forces re-review of every cone (useful
    for surfacing new observations on prior-clean apexes).

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim-convergence directory for {asn_label}", file=sys.stderr)
        return "failed"

    deps_data = generate_claim_convergence_deps(asn_num)
    if not deps_data:
        print(f"  No dependency data for {asn_label}", file=sys.stderr)
        return "failed"

    levels = topological_levels(deps_data)
    asn_labels = set(build_label_index(claim_dir).keys())

    # Workspace progress: skip apexes already done in this in-progress sweep.
    # `--all` unconditionally clears prior progress (it's a fresh re-review of
    # every cone). Otherwise, resume by replaying the completed set.
    from lib.claim_convergence.sweep_progress import (
        read_progress, write_progress, clear_progress,
    )
    if all_mode:
        clear_progress(asn_label)
        completed = set()
    else:
        saved = read_progress(asn_label)
        completed = set(saved.get("completed", [])) if saved else set()
        if completed:
            print(f"\n  [REGIONAL-SWEEP] resuming — {len(completed)} "
                  f"apex(es) already done in this sweep", file=sys.stderr)

    print(f"\n  [REGIONAL-SWEEP] {asn_label} — {len(asn_labels)} claims, "
          f"min_deps={min_deps}{'  --all' if all_mode else ''}",
          file=sys.stderr)

    start_time = time.time()
    cones_reviewed = 0
    cones_skipped = 0
    any_not_converged = False

    store = Store()
    label_index = build_cross_asn_label_index(store=store)
    rev_index = {p: l for l, p in label_index.items()}
    try:
        for level_idx, level_labels in enumerate(levels):
            for label in level_labels:
                from_path = label_index.get(label)
                if not from_path:
                    continue
                same_deps = [
                    rev_index[link["to_set"][0]]
                    for link in active_links(
                        store, "citation.depends", from_set=[from_path],
                    )
                    if link["to_set"]
                    and rev_index.get(link["to_set"][0]) in asn_labels
                ]
                if len(same_deps) < min_deps:
                    continue

                # Workspace gate: already done in this sweep run.
                if label in completed:
                    cones_skipped += 1
                    continue

                # Decide whether to process. Both `--all` and predicate-False
                # process; predicate-True in default mode skips the work.
                if all_mode:
                    cones_reviewed += 1
                    result = run_cone_review(
                        asn_num, label, same_deps,
                        max_cycles=max_cycles, dry_run=dry_run, model=model)
                    if result != "converged":
                        any_not_converged = True
                elif is_claim_converged(store, from_path):
                    print(f"  [REGIONAL-SWEEP] {label}: predicate True, skipping",
                          file=sys.stderr)
                    cones_skipped += 1
                else:
                    cones_reviewed += 1
                    result = run_cone_review(
                        asn_num, label, same_deps,
                        max_cycles=max_cycles, dry_run=dry_run, model=model)
                    if result != "converged":
                        any_not_converged = True

                # Uniform marking: mark completed iff the predicate now holds.
                # This makes `completed` mean exactly "predicate True at the
                # time this apex was visited" — same answer for skip and
                # process paths. Apexes that didn't converge stay re-visitable.
                if is_claim_converged(store, from_path):
                    completed.add(label)
                    write_progress(asn_label, {"completed": sorted(completed)})
    finally:
        store.close()

    elapsed = time.time() - start_time
    if cones_reviewed == 0 and cones_skipped == 0:
        print(f"\n  [REGIONAL-SWEEP] No claims with >= {min_deps} same-ASN deps.",
              file=sys.stderr)
    else:
        print(f"\n  [REGIONAL-SWEEP] {cones_reviewed} reviewed, "
              f"{cones_skipped} skipped, in {elapsed:.0f}s",
              file=sys.stderr)

    # Natural completion → clear progress (no resume needed next time).
    if not dry_run:
        clear_progress(asn_label)

    return "not_converged" if any_not_converged else "converged"
