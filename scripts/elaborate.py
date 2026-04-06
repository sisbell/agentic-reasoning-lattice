#!/usr/bin/env python3
"""
Elaborate — write standalone proofs for properties that lack them.

Narrows focus to one property at a time with curated context (host section
+ dependencies), writing rigorous Dijkstra-style proofs. This is the
elaboration phase between discovery and formalization.

Usage:
    python scripts/elaborate.py 40
    python scripts/elaborate.py 40 --max-cycles 5
    python scripts/elaborate.py 40 --dry-run
    python scripts/elaborate.py 40 --label B6
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, formal_stmts, dep_graph
from lib.shared.common import (find_asn, extract_property_sections,
                                step_commit_asn)
from lib.formalization.core.asn_normalizer import step_stabilize
from lib.formalization.core.build_dependency_graph import generate_deps, write_deps_yaml
from lib.formalization.core.topological_sort import topological_sort_labels
from lib.formalization.assembly.produce_interface import assemble_formal_statements
from lib.elaboration.standalone_proofs import (
    find_incomplete_sections, build_repair_context, repair_section,
)


def run_elaborate(asn_num, max_cycles=10, dry_run=False, single_label=None):
    """Run the elaboration pipeline.

    Returns (total_elaborated, total_failed).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return 0, 0

    print(f"\n  [ELABORATE] {asn_label}", file=sys.stderr)
    start_time = time.time()

    total_elaborated = 0
    total_failed = 0

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # 1. Format gate
        step_stabilize(asn_num)

        # 2. Detect incomplete sections
        incomplete = find_incomplete_sections(asn_num)

        if single_label:
            incomplete = [i for i in incomplete if i["label"] == single_label]

        if not incomplete:
            print(f"  [DETECT] 0 properties need standalone proofs",
                  file=sys.stderr)
            break

        print(f"  [DETECT] {len(incomplete)} properties need standalone proofs",
              file=sys.stderr)
        for item in incomplete:
            host = (f" (proof in {item['host_label']})"
                    if item['host_label'] else " (no embedded proof found)")
            print(f"    {item['label']}{host}", file=sys.stderr)

        if dry_run:
            break

        # Best-effort dependency ordering
        deps_data = generate_deps(asn_num)
        if deps_data:
            ordered_labels = topological_sort_labels(deps_data)
        else:
            ordered_labels = []
            deps_data = {"properties": {}, "depends": []}

        incomplete_labels = {i["label"] for i in incomplete}
        incomplete_map = {i["label"]: i for i in incomplete}

        # Order by deps, append any not in graph
        ordered = [l for l in ordered_labels if l in incomplete_labels]
        ordered += sorted(incomplete_labels - set(ordered))

        # Get all sections for context building
        text = asn_path.read_text()
        all_labels = list(deps_data.get("properties", {}).keys())
        sections = extract_property_sections(text, known_labels=all_labels,
                                              truncate=False)

        # 3. Repair each property
        for label in ordered:
            item = incomplete_map[label]
            dep_text = build_repair_context(asn_num, label, deps_data,
                                             sections)

            ok = repair_section(asn_num, label,
                                thin_section=item["thin_section"],
                                host_section=item["host_section"],
                                dependency_text=dep_text)

            if ok:
                total_elaborated += 1
                step_commit_asn(asn_num,
                                hint=f"{label} standalone proof")
                # Re-read sections for downstream properties
                text = asn_path.read_text()
                sections = extract_property_sections(
                    text, known_labels=all_labels, truncate=False)
            else:
                total_failed += 1

        if single_label:
            break

    # 4. Assembly (after all cycles)
    if not dry_run and total_elaborated > 0:
        print(f"\n  [ASSEMBLY]", file=sys.stderr)
        path = assemble_formal_statements(asn_num)
        if path:
            print(f"  formal-statements.md", file=sys.stderr)

        deps = generate_deps(asn_num)
        if deps:
            write_deps_yaml(asn_num, deps)
            print(f"  dependency-graph.yaml", file=sys.stderr)

        step_commit_asn(asn_num, hint="elaboration assembly")

    # 5. Report
    elapsed = time.time() - start_time
    print(f"\n  Done: {total_elaborated} elaborated, {total_failed} failed.",
          file=sys.stderr)
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    return total_elaborated, total_failed


def main():
    parser = argparse.ArgumentParser(
        description="Elaborate — write standalone proofs for incomplete properties")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=10,
                        help="Maximum outer cycles (default: 10)")
    parser.add_argument("--label", help="Elaborate a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List incomplete sections without repairing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    elaborated, failed = run_elaborate(asn_num, max_cycles=args.max_cycles,
                                        dry_run=args.dry_run,
                                        single_label=args.label)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
