#!/usr/bin/env python3
"""
Formalization Rebase — validate and fix ASN references to upstream deps.

Four review passes (mechanical, cross-reference, extension, dependency-report)
with a convergence loop. Format gate runs on entry to each cycle.

Usage:
    python scripts/formalization-rebase.py 40
    python scripts/formalization-rebase.py 40 --max-cycles 1     # single pass, no fixing
    python scripts/formalization-rebase.py 40 --mode incremental  # track dirty set
    python scripts/formalization-rebase.py 40 --dry-run           # show what would run
"""

import argparse
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, REVIEWS_DIR, load_manifest, next_review_number
from lib.shared.common import find_asn, step_commit_asn
from lib.formalization.core.asn_normalizer import step_refresh_deps
from lib.formalization.core.build_dependency_graph import generate_deps
from lib.formalization.rebase.review import run_review
from lib.formalization.rebase.revise import revise


def _group_by_label(findings):
    """Group findings by property label. Returns list of (label, [findings])."""
    groups = defaultdict(list)
    for f in findings:
        groups[f.label].append(f)
    return sorted(groups.items())


def _downstream_dependents(asn_num, changed_labels):
    """Find properties that depend on any of the changed labels."""
    deps_data = generate_deps(asn_num)
    if not deps_data:
        return set()

    dependents = set()
    for label, prop_data in deps_data.get("properties", {}).items():
        follows = set(prop_data.get("follows_from", []))
        if follows & changed_labels:
            dependents.add(label)

    return dependents


def _apply_name_fixes(asn_num, findings):
    """Mechanically fix inline name mismatches. Returns set of changed labels."""
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return set()

    text = asn_path.read_text()
    changed = set()

    for f in findings:
        m = re.search(
            r'(\S+) cited as "(\w+)" but upstream canonical name is "(\w+)"',
            f.detail)
        if not m:
            continue

        up_label = m.group(1)
        wrong_name = m.group(2)
        right_name = m.group(3)

        old = f"{up_label} ({wrong_name})"
        new = f"{up_label} ({right_name})"

        if old in text:
            text = text.replace(old, new)
            changed.add(f.label)

    if changed:
        asn_path.write_text(text)

    return changed


def run_rebase(asn_num, max_cycles=5, mode="full_sweep", dry_run=False):
    """Run the dependency rebase pipeline.

    Args:
        asn_num: ASN number
        max_cycles: Maximum convergence cycles
        mode: "full_sweep" (all properties each cycle) or
              "incremental" (dirty set + dependents)
        dry_run: Show what would run without fixing

    Returns:
        "converged" or "not_converged"
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])
    if not depends:
        print(f"  {asn_label} has no dependencies — nothing to rebase",
              file=sys.stderr)
        return "converged"

    print(f"\n  [REBASE] {asn_label} (depends: {depends})", file=sys.stderr)

    start_time = time.time()
    target_labels = None  # None = all properties
    all_findings = []
    converged = False
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        label_desc = f"{len(target_labels)} properties (dirty set)" if target_labels else "all properties"
        print(f"\n  [CYCLE {cycle}/{max_cycles}] {label_desc}, {mode}",
              file=sys.stderr)

        # Format gate
        step_refresh_deps(asn_num)

        # Run review
        findings = run_review(asn_num, target_labels)

        if not findings:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        # New review file per cycle
        (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label)
        review_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Dependency Rebase — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            for f in findings:
                rf.write(f"- **{f.label}** [{f.category}] ({f.location}): "
                         f"{f.detail}\n")
            rf.write(f"\n{len(findings)} findings.\n")

        all_findings = findings

        # Print findings summary
        print(f"\n  {len(findings)} findings:", file=sys.stderr)
        for f in findings:
            print(f"  [{f.label}] {f.category}: {f.detail[:80]}",
                  file=sys.stderr)

        if dry_run:
            print(f"\n  [DRY RUN] Would revise {len(_group_by_label(findings))} properties",
                  file=sys.stderr)
            break

        if max_cycles == 1:
            # Single pass mode — report only, don't fix
            print(f"\n  Single pass — {len(findings)} findings reported, no fixes applied.",
                  file=sys.stderr)
            break

        # Split findings into mechanical fixes and LLM fixes
        mechanical_fixes = [f for f in findings if f.category == "name-mismatch"]
        llm_fixes = [f for f in findings if f.category != "name-mismatch"]

        changed_labels = set()

        # Mechanical fixes first (cheap, reliable)
        if mechanical_fixes:
            fixed = _apply_name_fixes(asn_num, mechanical_fixes)
            if fixed:
                changed_labels.update(fixed)
                print(f"  [NAME-FIX] {len(fixed)} inline name corrections",
                      file=sys.stderr)

        # LLM revise for remaining findings
        if llm_fixes:
            print(f"\n  [REVISE] {len(_group_by_label(llm_fixes))} properties...",
                  file=sys.stderr)
            for label, label_findings in _group_by_label(llm_fixes):
                ok = revise(asn_num, label, label_findings)
                if ok:
                    changed_labels.add(label)

        if not changed_labels:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        # Commit
        step_commit_asn(asn_num,
                        f"rebase(asn): {asn_label} — dependency rebase cycle {cycle}")

        # Update target set for next cycle
        if mode == "incremental":
            target_labels = changed_labels | _downstream_dependents(
                asn_num, changed_labels)
        # full_sweep: target_labels stays None (all properties)

    # Append final result to last review file
    elapsed = time.time() - start_time
    if had_findings:
        with open(review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Converged after {cycle} cycle{'s' if cycle > 1 else ''}.\n")
            else:
                rf.write(f"Not converged after {cycle} cycles. "
                         f"{len(all_findings)} findings remain.\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(f"\n  Review: {review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if had_findings and not dry_run and not converged:
        step_commit_asn(asn_num,
                        f"rebase(asn): {asn_label} — dependency rebase (not converged)")

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Formalization Rebase — validate and fix ASN references to upstream deps")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Maximum convergence cycles (default: 5)")
    parser.add_argument("--mode", choices=["full_sweep", "incremental"],
                        default="full_sweep",
                        help="Convergence mode (default: full_sweep)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show findings without fixing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_rebase(asn_num, max_cycles=args.max_cycles,
                         mode=args.mode, dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
