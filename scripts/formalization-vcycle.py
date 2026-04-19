#!/usr/bin/env python3
"""
V-Cycle Formalization Review — multigrid-inspired convergence.

Three scales of optimization in a V-cycle:
  Local:    local-review, contract-review (one property at a time)
  Regional: regional-sweep (high-dependency clusters, bottom-up DAG walk)
  Global:   full-review (full ASN scan)

Upward pass (restriction): local → regional → global — builds confidence.
Downward pass (prolongation): regional → local — verifies corrections.
Repeat until all scales converge.

Usage:
    python scripts/formalization-vcycle.py 36
    python scripts/formalization-vcycle.py 36 --max-passes 3
    python scripts/formalization-vcycle.py 36 --min-cone-deps 3
    python scripts/formalization-vcycle.py 36 --dry-run
"""

import argparse
import importlib
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR
from lib.shared.common import find_asn, build_label_index, load_property_metadata
from lib.formalization.regional import run_regional_sweep, run_regional_review
from lib.formalization.core.build_dependency_graph import generate_formalization_deps

# Hyphenated script names need importlib
_local_review = importlib.import_module("local-review")
_contract_review = importlib.import_module("contract-review")
_full_review = importlib.import_module("full-review")

run_local_review = _local_review.run_local_review
run_contract_review = _contract_review.run_contract_review
run_full_review = _full_review.run_full_review


def _git_head():
    """Return current HEAD hash."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    return result.stdout.strip()


def _get_changed_labels(asn_label, before_hash):
    """Get property labels changed since before_hash.

    Diffs HEAD vs before_hash for the ASN's formalization dir,
    maps changed filenames to labels via build_label_index.
    """
    prop_dir = FORMALIZATION_DIR / asn_label
    result = subprocess.run(
        ["git", "diff", "--name-only", before_hash, "HEAD",
         "--", f"vault/3-formalization/{asn_label}/"],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    if not result.stdout.strip():
        return set()

    label_index = build_label_index(prop_dir)
    stem_to_label = {stem: lbl for lbl, stem in label_index.items()}

    changed = set()
    for line in result.stdout.strip().split("\n"):
        fname = Path(line).name
        if fname.startswith("_") or fname.startswith(".") or "reviews/" in line:
            continue
        stem = fname.replace(".md", "").replace(".yaml", "")
        label = stem_to_label.get(stem, stem)
        changed.add(label)

    return changed


def _affected_cones(changed_labels, asn_num, min_deps=4):
    """Find cones whose apex or deps overlap with changed_labels.

    Returns list of (apex_label, dep_labels) tuples.
    """
    _, asn_label = find_asn(str(asn_num))
    prop_dir = FORMALIZATION_DIR / asn_label
    asn_labels = set(build_label_index(prop_dir).keys())
    all_meta = load_property_metadata(prop_dir)

    cones = []
    for label, meta in all_meta.items():
        same_deps = [d for d in meta.get("depends", []) if d in asn_labels]
        if len(same_deps) < min_deps:
            continue
        # Check if apex or any dep overlaps with changed_labels
        cone_labels = {label} | set(same_deps)
        if cone_labels & changed_labels:
            cones.append((label, same_deps))

    return cones


def _downstream_labels(changed_labels, deps_data):
    """Find labels that depend on any changed label (one level)."""
    downstream = set()
    props = deps_data.get("properties", {})
    for label, info in props.items():
        follows = set(info.get("follows_from", []))
        if follows & changed_labels:
            downstream.add(label)
    return downstream


def run_vcycle(asn_num, max_passes=5, min_cone_deps=4, dry_run=False):
    """Run V-cycle formalization review.

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    deps_data = generate_formalization_deps(asn_num)

    print(f"\n  [V-CYCLE] {asn_label}", file=sys.stderr)
    overall_start = time.time()

    for pass_num in range(1, max_passes + 1):
        print(f"\n  {'='*50}", file=sys.stderr)
        print(f"  V-CYCLE PASS {pass_num}/{max_passes}", file=sys.stderr)
        print(f"  {'='*50}", file=sys.stderr)

        all_changed = set()

        # ── Upward (restriction) ──
        print(f"\n  ── Upward ──", file=sys.stderr)

        # 1. Local review (property scale)
        h = _git_head()
        run_local_review(asn_num, max_cycles=5, dry_run=dry_run)
        proof_changed = _get_changed_labels(asn_label, h)
        all_changed |= proof_changed
        print(f"  [LOCAL-REVIEW] → {len(proof_changed)} changed",
              file=sys.stderr)

        # 2. Contract review (local)
        h = _git_head()
        run_contract_review(asn_num, max_cycles=5, dry_run=dry_run)
        contract_changed = _get_changed_labels(asn_label, h)
        all_changed |= contract_changed
        print(f"  [CONTRACT-REVIEW] → {len(contract_changed)} changed",
              file=sys.stderr)

        # 3. Regional sweep (regional)
        h = _git_head()
        run_regional_sweep(asn_num, min_deps=min_cone_deps, dry_run=dry_run)
        cone_changed = _get_changed_labels(asn_label, h)
        all_changed |= cone_changed
        print(f"  [REGIONAL-SWEEP] → {len(cone_changed)} changed",
              file=sys.stderr)

        # 4. Full review (global)
        h = _git_head()
        run_full_review(asn_num, max_cycles=3, dry_run=dry_run)
        global_changed = _get_changed_labels(asn_label, h)
        all_changed |= global_changed
        print(f"  [FULL-REVIEW] → {len(global_changed)} changed",
              file=sys.stderr)

        # ── Downward (prolongation) ──
        # Descend if ANY upward step changed anything — not just global.
        # Global may miss issues due to context overload, but regional sweep
        # or local fixes still need verification at finer scales.
        upward_changed = set(all_changed)
        if upward_changed:
            print(f"\n  ── Downward ({len(upward_changed)} labels affected) ──",
                  file=sys.stderr)

            # 5. Regional: re-check affected cones
            h = _git_head()
            affected_cones = _affected_cones(upward_changed, asn_num, min_cone_deps)
            for apex, deps in affected_cones:
                print(f"  [REGIONAL-REVIEW] {apex} ({len(deps)} deps)",
                      file=sys.stderr)
                run_regional_review(asn_num, apex, deps, max_cycles=2,
                                dry_run=dry_run)
            regional_changed = _get_changed_labels(asn_label, h)
            all_changed |= regional_changed
            print(f"  [REGIONAL-REVIEW] → {len(regional_changed)} changed",
                  file=sys.stderr)

            # 6-7. Local: re-check affected properties
            affected = upward_changed | regional_changed
            if deps_data:
                affected |= _downstream_labels(affected, deps_data)

            h = _git_head()
            for label in sorted(affected):
                run_local_review(asn_num, max_cycles=2, single_label=label,
                                 dry_run=dry_run)
                run_contract_review(asn_num, max_cycles=2, single_label=label,
                                    dry_run=dry_run)
            local_changed = _get_changed_labels(asn_label, h)
            all_changed |= local_changed
            print(f"  [LOCAL-RECHECK] → {len(local_changed)} changed",
                  file=sys.stderr)

        # ── Convergence ──
        print(f"\n  Pass {pass_num}: {len(all_changed)} labels changed total",
              file=sys.stderr)

        if not all_changed:
            elapsed = time.time() - overall_start
            print(f"\n  {'='*50}", file=sys.stderr)
            print(f"  CONVERGED after {pass_num} pass{'es' if pass_num > 1 else ''}",
                  file=sys.stderr)
            print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)
            print(f"  {'='*50}", file=sys.stderr)
            return "converged"

        if dry_run:
            print(f"\n  [DRY RUN] Would continue to next pass.",
                  file=sys.stderr)
            break

    elapsed = time.time() - overall_start
    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  NOT CONVERGED after {max_passes} passes",
          file=sys.stderr)
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    return "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="V-Cycle Formalization Review — multigrid convergence")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--max-passes", type=int, default=5,
                        help="Maximum V-cycle passes (default: 5)")
    parser.add_argument("--min-cone-deps", type=int, default=4,
                        help="Minimum same-ASN deps for regional sweep (default: 4)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_vcycle(asn_num, max_passes=args.max_passes,
                         min_cone_deps=args.min_cone_deps,
                         dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
