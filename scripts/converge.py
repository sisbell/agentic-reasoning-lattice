#!/usr/bin/env python3
"""
Formalize — Dijkstra rewrite + formal contracts with convergence.

Rewrites every non-definition claim's proof to Dijkstra standard
and ensures each has a complete formal contract. Uses incremental
convergence: rewrite all needing quality → re-check → rewrite dirty
set + dependents → converge.

Usage:
    python scripts/converge.py 40
    python scripts/converge.py 40 --max-cycles 1     # single pass
    python scripts/converge.py 40 --mode full_sweep   # check all each cycle
    python scripts/converge.py 40 --label B0a         # single claim
    python scripts/converge.py 40 --dry-run           # list what needs quality
    python scripts/converge.py 40 --contracts-only    # only missing contracts
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, CLAIM_CONVERGENCE_DIR, CLAIM_DIR, next_review_number
from lib.shared.common import find_asn, step_commit_asn, build_label_index, parallel_llm_calls
from lib.claim_convergence.core.build_dependency_graph import generate_claim_convergence_deps
from lib.claim_convergence.core.topological_sort import topological_sort_labels, topological_levels
from lib.claim_convergence.converge.produce_contract import (
    find_claims_needing_quality, produce_contract,
    _has_formal_contract, _downstream_dependents, _compute_hash,
)
import hashlib
import json


def _load_cache(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {}

def _save_cache(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def run_formalize(asn_num, max_cycles=5, mode="incremental",
                  dry_run=False, single_label=None, contracts_only=False,
                  force_rebuild=False):
    """Run the formalize pipeline.

    Args:
        asn_num: ASN number
        max_cycles: Maximum convergence cycles
        mode: "incremental" (dirty set + dependents) or "full_sweep"
        dry_run: List what needs quality without rewriting
        single_label: If set, only formalize this one claim (force rewrite even if contract exists)

    Returns:
        "converged" or "not_converged"
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [FORMALIZE] {asn_label}", file=sys.stderr)

    review_dir = CLAIM_CONVERGENCE_DIR / asn_label / "reviews"
    cc_dir = CLAIM_CONVERGENCE_DIR / asn_label
    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim doc directory for {asn_label}", file=sys.stderr)
        print(f"  Run: python scripts/promote-blueprint.py {asn_num}",
              file=sys.stderr)
        return "failed"

    _label_index = build_label_index(claim_dir)
    cc_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cc_dir / "_cache.json"
    cache = _load_cache(cache_path)
    print(f"  Directory: {claim_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    start_time = time.time()
    converged = False
    dirty_set = None  # None = all claims on first pass
    force_all = force_rebuild or (single_label is not None)

    total_rewritten = 0
    total_failed = 0

    for cycle in range(1, max_cycles + 1):
        # Find claims needing quality
        force = force_rebuild or (single_label is not None)
        needs, current_hashes = find_claims_needing_quality(
            asn_num, force_all=force_all, force_rebuild=force)

        # Filter to single label
        if single_label:
            needs = [n for n in needs if n["label"] == single_label]

        # Filter to dirty set (incremental mode, cycle > 1)
        if dirty_set is not None and mode == "incremental":
            needs = [n for n in needs if n["label"] in dirty_set]

        if not needs:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if total_rewritten == 0:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        # Sort in dependency order
        deps_data = generate_claim_convergence_deps(asn_num)
        ordered = topological_sort_labels(deps_data) if deps_data else []
        needs_labels = {n["label"] for n in needs}
        needs_map = {n["label"]: n for n in needs}

        # Order needs by dependency
        ordered_needs = [l for l in ordered if l in needs_labels]
        # Add any not in the graph
        ordered_needs += sorted(needs_labels - set(ordered_needs))

        label_desc = (f"{len(ordered_needs)} claims"
                      + (f" (dirty set)" if dirty_set is not None else ""))
        print(f"\n  [CYCLE {cycle}/{max_cycles}] {label_desc}",
              file=sys.stderr)

        if dry_run:
            for label in ordered_needs:
                item = needs_map[label]
                has_contract = _has_formal_contract(item["section"])
                status = "has contract" if has_contract else "NO contract"
                print(f"    {label:30s} {status}", file=sys.stderr)
            break

        # Rewrite claims in parallel by dependency level
        cycle_rewritten = 0
        cycle_failed = 0
        changed = set()
        rejected = False

        levels = topological_levels(deps_data)

        for level_idx, level_labels in enumerate(levels):
            level_needs = [l for l in level_labels if l in needs_labels]
            if not level_needs:
                continue

            print(f"\n  [LEVEL {level_idx}] {len(level_needs)} claims",
                  file=sys.stderr)

            def _process_one(label):
                item = needs_map[label]
                stem = _label_index.get(label, label)
                claim_path = item.get("path") or claim_dir / f"{stem}.md"
                ok, file_changed, response = produce_contract(
                    asn_num, label, item["section"],
                    claim_path=claim_path, max_cycles=1)
                return label, (ok, file_changed, response)

            results = parallel_llm_calls(
                level_needs, _process_one, max_workers=10)

            # Process results
            level_changed = False
            for label, result_tuple in results:
                if result_tuple is None:
                    cycle_failed += 1
                    continue
                ok, file_changed, response = result_tuple
                if ok:
                    cycle_rewritten += 1
                    if file_changed:
                        changed.add(label)
                        level_changed = True

                        # Write review file
                        review_dir.mkdir(parents=True, exist_ok=True)
                        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
                        rev_path = review_dir / f"review-{review_num}.md"
                        with open(rev_path, "w") as rf:
                            rf.write(f"# Formalize — {asn_label} / {label}\n\n")
                            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                            rf.write(response + "\n")

                        # Update hash cache
                        stem = _label_index.get(label, label)
                        md_path = claim_dir / f"{stem}.md"
                        yaml_path = claim_dir / f"{stem}.yaml"
                        if md_path.exists():
                            hash_input = md_path.read_text()
                            if yaml_path.exists():
                                hash_input += yaml_path.read_text()
                            cache[label] = _compute_hash(hash_input)
                            _save_cache(cache_path, cache)
                else:
                    cycle_failed += 1
                    if response and response.startswith("REJECTED:"):
                        review_dir.mkdir(parents=True, exist_ok=True)
                        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
                        rev_path = review_dir / f"review-{review_num}.md"
                        with open(rev_path, "w") as rf:
                            rf.write(f"# Produce Contract REJECTED — {asn_label} / {label}\n\n")
                            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                            rf.write(response + "\n")
                        print(f"\n  [ABORT] Produce contract rejected for {label}.",
                              file=sys.stderr)
                        rejected = True

            if rejected:
                return "rejected"

            # Commit after each level, re-read for next level's deps
            if level_changed:
                step_commit_asn(asn_num, hint=f"produce-contract level {level_idx}")

                # Re-read claim files for next level
                for l in needs_labels:
                    l_stem = _label_index.get(l, l)
                    l_path = claim_dir / f"{l_stem}.md"
                    if l_path.exists():
                        needs_map[l]["section"] = l_path.read_text()

        total_rewritten += cycle_rewritten
        total_failed += cycle_failed

        print(f"\n  {cycle_rewritten} rewritten ({len(changed)} changed), "
              f"{cycle_failed} failed", file=sys.stderr)

        if not changed:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''} "
                  f"(no changes).", file=sys.stderr)
            break

        if single_label:
            break

        if max_cycles == 1:
            break

        # Dirty set for next cycle
        dirty_set = changed | _downstream_dependents(changed, deps_data)

    elapsed = time.time() - start_time
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Formalize — Dijkstra rewrite + formal contracts")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Maximum convergence cycles (default: 5)")
    parser.add_argument("--mode", choices=["incremental", "full_sweep"],
                        default="incremental",
                        help="Convergence mode (default: incremental)")
    parser.add_argument("--label", help="Formalize a single claim only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List claims needing quality pass")
    parser.add_argument("--contracts-only", action="store_true",
                        help="Only rewrite claims missing contracts")
    parser.add_argument("--force", action="store_true",
                        help="Full rebuild — ignore hashes, process all claims")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_formalize(asn_num, max_cycles=args.max_cycles,
                            mode=args.mode, dry_run=args.dry_run,
                            single_label=args.label,
                            contracts_only=args.contracts_only,
                            force_rebuild=args.force)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
