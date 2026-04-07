#!/usr/bin/env python3
"""
Formalize — Dijkstra rewrite + formal contracts with convergence.

Rewrites every non-definition property's proof to Dijkstra standard
and ensures each has a complete formal contract. Uses incremental
convergence: rewrite all needing quality → re-check → rewrite dirty
set + dependents → converge.

Usage:
    python scripts/formalize.py 40
    python scripts/formalize.py 40 --max-cycles 1     # single pass
    python scripts/formalize.py 40 --mode full_sweep   # check all each cycle
    python scripts/formalize.py 40 --label B0a         # single property
    python scripts/formalize.py 40 --dry-run           # list what needs quality
    python scripts/formalize.py 40 --contracts-only    # only missing contracts
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, REVIEWS_DIR, next_review_number
from lib.shared.common import find_asn, extract_property_sections, step_commit_asn
from lib.formalization.core.asn_normalizer import step_refresh_deps
from lib.formalization.core.build_dependency_graph import generate_deps, write_deps_yaml
from lib.formalization.core.topological_sort import topological_sort_labels
from lib.formalization.formalize.produce_contract import (
    find_properties_needing_quality, quality_rewrite,
    _has_formal_contract, _downstream_dependents, _compute_hash,
)
from lib.formalization.assembly.validate_contracts import validate_contract


def run_formalize(asn_num, max_cycles=5, mode="incremental",
                  dry_run=False, single_label=None, contracts_only=False,
                  force_rebuild=False):
    """Run the formalize pipeline.

    Args:
        asn_num: ASN number
        max_cycles: Maximum convergence cycles
        mode: "incremental" (dirty set + dependents) or "full_sweep"
        dry_run: List what needs quality without rewriting
        single_label: If set, only formalize this one property (force rewrite even if contract exists)

    Returns:
        "converged" or "not_converged"
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [FORMALIZE] {asn_label}", file=sys.stderr)

    start_time = time.time()
    converged = False
    dirty_set = None  # None = all properties on first pass
    force_all = force_rebuild or (single_label is not None)

    total_rewritten = 0
    total_failed = 0

    for cycle in range(1, max_cycles + 1):
        # Format gate
        step_refresh_deps(asn_num)

        # Validate axiom contracts (axioms are excluded from quality_rewrite
        # but their contracts can still be incomplete)
        if not dry_run:
            from lib.formalization.core.build_dependency_graph import find_property_table, parse_table_row
            text = asn_path.read_text()
            rows = find_property_table(text)
            if rows:
                all_labels = []
                axiom_labels = []
                for row in rows[2:]:
                    cells = parse_table_row(row)
                    if cells and cells[0].strip():
                        label = cells[0].strip().strip("`*")
                        all_labels.append(label)
                        status = cells[-1].strip().lower()
                        if status in ("axiom", "design requirement"):
                            axiom_labels.append(label)

                if axiom_labels and (single_label is None or single_label in axiom_labels):
                    print(f"  [AXIOM CONTRACTS] {len(axiom_labels)} axioms",
                          file=sys.stderr)
                    sections = extract_property_sections(
                        text, known_labels=all_labels, truncate=False)
                    check_labels = [single_label] if single_label else axiom_labels
                    for label in check_labels:
                        section = sections.get(label, "")
                        if not section or not _has_formal_contract(section):
                            continue
                        match, detail = validate_contract(label, section)
                        if match:
                            print(f"    {label}: MATCH", file=sys.stderr)
                        else:
                            print(f"    {label}: MISMATCH", file=sys.stderr)
                            for line in detail.split('\n')[:3]:
                                if line.strip():
                                    print(f"      {line.strip()}", file=sys.stderr)

        # Find properties needing quality
        force = force_rebuild or (single_label is not None)
        needs, current_hashes = find_properties_needing_quality(
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
        deps_data = generate_deps(asn_num)
        ordered = topological_sort_labels(deps_data) if deps_data else []
        needs_labels = {n["label"] for n in needs}
        needs_map = {n["label"]: n for n in needs}

        # Order needs by dependency
        ordered_needs = [l for l in ordered if l in needs_labels]
        # Add any not in the graph
        ordered_needs += sorted(needs_labels - set(ordered_needs))

        label_desc = (f"{len(ordered_needs)} properties"
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

        # Rewrite each property (single attempt — convergence loop handles retries)
        cycle_rewritten = 0
        cycle_failed = 0
        changed = set()

        for label in ordered_needs:
            item = needs_map[label]
            ok, file_changed, response = quality_rewrite(
                asn_num, label, item["section"], max_cycles=1)

            if ok:
                cycle_rewritten += 1
                if file_changed:
                    changed.add(label)

                    # Write review file for this change
                    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
                    review_num = next_review_number(asn_label)
                    rev_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"
                    with open(rev_path, "w") as rf:
                        rf.write(f"# Formalize — {asn_label} / {label}\n\n")
                        rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                        rf.write(response + "\n")

                    # Commit this change
                    step_commit_asn(asn_num, hint=f"{label} quality rewrite")

                # Re-read sections for subsequent properties
                text = asn_path.read_text()
                all_labels = list(deps_data.get("properties", {}).keys()) if deps_data else []
                sections = extract_property_sections(
                    text, known_labels=all_labels, truncate=False)
                for l in needs_labels:
                    if l in sections:
                        needs_map[l]["section"] = sections[l]

                # Update hash incrementally (survives kill)
                updated_section = sections.get(label, item["section"])
                if deps_data and label in deps_data.get("properties", {}):
                    deps_data["properties"][label]["hash"] = _compute_hash(updated_section)
                    write_deps_yaml(asn_num, deps_data)
            else:
                cycle_failed += 1
                if response.startswith("REJECTED:"):
                    # Review gate rejected the rewrite — write review and stop
                    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
                    review_num = next_review_number(asn_label)
                    rev_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"
                    with open(rev_path, "w") as rf:
                        rf.write(f"# Quality Rewrite REJECTED — {asn_label} / {label}\n\n")
                        rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                        rf.write(response + "\n")
                    print(f"\n  [ABORT] Quality rewrite rejected for {label}. "
                          f"Review: {rev_path.relative_to(WORKSPACE)}",
                          file=sys.stderr)
                    return "rejected"

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
    parser.add_argument("--label", help="Formalize a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List properties needing quality pass")
    parser.add_argument("--contracts-only", action="store_true",
                        help="Only rewrite properties missing contracts")
    parser.add_argument("--force", action="store_true",
                        help="Full rebuild — ignore hashes, process all properties")
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
