#!/usr/bin/env python3
"""
Batch rebase — check and rebase all ASNs in dependency order.

Processes ASNs in topological order (foundations first). For each ASN:
  1. Check if rebase needed (dependency exports newer than last_rebase_check)
  2. If not needed → skip
  3. If needed, check consistency (or reuse cached CLEAN result)
  4. If CLEAN → update timestamps, skip
  5. If findings → rebase with findings, review/revise, post-check, re-export
  6. If post-check fails → retry once, then stop batch

State is tracked in each ASN's project model yaml:
  - last_rebase_check: timestamp of last rebase verification
  - last_consistency_check: timestamp of last consistency check
  - last_consistency_result: "CLEAN" or "FINDINGS"

Usage:
    python scripts/rebase-all.py                       # all active ASNs
    python scripts/rebase-all.py --exclude 40 42 45    # skip specific ASNs
    python scripts/rebase-all.py --dry-run             # show order + status
    python scripts/rebase-all.py --force               # ignore cached state
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import (WORKSPACE, ASNS_DIR, STATEMENTS_DIR, FOUNDATION_LIST,
                   PROJECT_MODEL_DIR, load_manifest)
from lib.common import find_asn, step_commit
from lib.rebase_asn import (
    step_rebase, step_review_revise, step_export,
    update_rebase_timestamp, run_inline_consistency_check,
)


def get_active_asns():
    """Get active ASN numbers from project model yamls. Yaml exists = active."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*.yaml"):
        m = re.match(r"ASN-(\d+)", path.stem)
        if m:
            active.append(int(m.group(1)))
    return sorted(active)


def build_dep_graph(asn_nums):
    """Build dependency graph from project models."""
    graph = {}
    for num in asn_nums:
        manifest = load_manifest(num)
        if manifest:
            deps = set(manifest.get("depends", []))
            graph[num] = deps & set(asn_nums)
        else:
            graph[num] = set()
    return graph


def topological_sort(graph):
    """Topological sort — returns list in dependency order (foundations first)."""
    result = []
    visited = set()
    visiting = set()

    def visit(node):
        if node in visited:
            return
        if node in visiting:
            print(f"  [WARN] Dependency cycle involving ASN-{node:04d}",
                  file=sys.stderr)
            return
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)

    for node in sorted(graph.keys()):
        visit(node)

    return result


def get_dep_export_timestamps(asn_num):
    """Get the newest dependency export timestamp for an ASN."""
    manifest = load_manifest(asn_num)
    if not manifest:
        return 0

    newest = 0
    for dep in manifest.get("depends", []):
        dep_export = WORKSPACE / "vault" / "3-export" / f"ASN-{dep:04d}-statements.md"
        if dep_export.exists():
            ts = dep_export.stat().st_mtime
            if ts > newest:
                newest = ts
    return newest


def parse_iso_timestamp(ts_str):
    """Parse ISO timestamp string to unix timestamp."""
    if not ts_str:
        return 0
    try:
        dt = datetime.fromisoformat(ts_str.strip('"'))
        return dt.timestamp()
    except (ValueError, TypeError):
        return 0


def update_consistency_state(asn_num, result):
    """Write last_consistency_check and last_consistency_result to yaml."""
    yaml_path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}.yaml"
    if not yaml_path.exists():
        return

    content = yaml_path.read_text()
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Update or append last_consistency_check
    if "last_consistency_check:" in content:
        content = re.sub(r'last_consistency_check:.*',
                         f'last_consistency_check: "{ts}"', content)
    else:
        content = content.rstrip() + f'\nlast_consistency_check: "{ts}"\n'

    # Update or append last_consistency_result
    if "last_consistency_result:" in content:
        content = re.sub(r'last_consistency_result:.*',
                         f'last_consistency_result: "{result}"', content)
    else:
        content = content.rstrip() + f'\nlast_consistency_result: "{result}"\n'

    yaml_path.write_text(content)


def needs_rebase(asn_num, force=False):
    """Check if an ASN needs rebasing based on yaml state.

    Returns:
      "skip" — no rebase needed
      "check" — needs consistency check to determine
      "rebase" — known to need rebase (force mode)
    """
    manifest = load_manifest(asn_num)
    if not manifest or not manifest.get("depends"):
        return "skip"

    # No reasoning doc — nothing to rebase
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return "skip"

    if force:
        return "rebase"

    newest_dep = get_dep_export_timestamps(asn_num)
    if newest_dep == 0:
        return "skip"

    # Check last_rebase_check
    rebase_ts = parse_iso_timestamp(manifest.get("last_rebase_check", ""))
    if rebase_ts > newest_dep:
        return "skip"  # Rebase is newer than all deps

    return "rebase"


def process_asn(asn_num, model, effort, max_cycles, force=False):
    """Process one ASN: check → rebase → post-check → export."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return "skipped"

    manifest = load_manifest(asn_num)
    if not manifest or not manifest.get("depends"):
        return "skipped"

    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label}", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    # Step 1: Check if work needed
    status = needs_rebase(asn_num, force=force)
    if status == "skip":
        print(f"  [SKIP] {asn_label} — up to date", file=sys.stderr)
        return "skipped"

    # Step 2: Pre-check (sonnet fast eyes — supplements the rebase, doesn't gate it)
    print(f"  [PRE-CHECK] Running consistency check...", file=sys.stderr)
    findings = run_inline_consistency_check(asn_num, asn_path, asn_label)

    if findings:
        update_consistency_state(asn_num, "FINDINGS")
        print(f"  [PRE-CHECK] Findings will be fed to rebase", file=sys.stderr)
    else:
        update_consistency_state(asn_num, "CLEAN")
        print(f"  [PRE-CHECK] CLEAN — rebase will run without extra findings",
              file=sys.stderr)

    # Step 3: Rebase (one pass, then scoped review/revise up to 5 cycles)
    print(f"  [REBASE] {asn_label}...", file=sys.stderr)
    ok = step_rebase(asn_num, asn_path, asn_label, model, effort)
    if not ok:
        print(f"  [FAILED] {asn_label} rebase failed", file=sys.stderr)
        return "failed"

    step_commit(f"rebase(asn): {asn_label} against updated foundation")

    # Step 4: Scoped rebase review/revise (up to 5 cycles, rebase changes only)
    print(f"  [REBASE REVIEW] Scoped review of rebase changes...",
          file=sys.stderr)
    rebased_properties = "(consistency check findings)"
    step_review_revise(asn_num, asn_path, asn_label, rebased_properties,
                       5, model, effort)

    # Step 5: Standard convergence via revise.py (up to 30 cycles)
    print(f"  [CONVERGE] Running standard convergence...", file=sys.stderr)
    converge_cmd = [sys.executable,
                    str(WORKSPACE / "scripts" / "revise.py"),
                    str(asn_num),
                    "--converge", str(max_cycles)]
    converge_result = subprocess.run(
        converge_cmd, capture_output=False, text=True,
        cwd=str(WORKSPACE),
    )
    if converge_result.returncode != 0:
        print(f"  [FAILED] {asn_label} convergence failed", file=sys.stderr)
        return "failed"

    # Step 6: Post-check
    print(f"  [POST-CHECK] Verifying {asn_label}...", file=sys.stderr)
    post_findings = run_inline_consistency_check(asn_num, asn_path, asn_label)

    if post_findings is None:
        print(f"  [VERIFIED] {asn_label} — CLEAN", file=sys.stderr)
        update_consistency_state(asn_num, "CLEAN")
    else:
        # One more rebase → commit → convergence cycle
        print(f"  [POST-CHECK] Findings detected — one more rebase + convergence...",
              file=sys.stderr)

        ok = step_rebase(asn_num, asn_path, asn_label, model, effort)
        if not ok:
            print(f"  [FAILED] {asn_label} post-check rebase failed",
                  file=sys.stderr)
            return "failed"

        step_commit(f"rebase(asn): {asn_label} post-check fixes")

        converge_cmd = [sys.executable,
                        str(WORKSPACE / "scripts" / "revise.py"),
                        str(asn_num),
                        "--converge", str(max_cycles)]
        subprocess.run(converge_cmd, capture_output=False, text=True,
                       cwd=str(WORKSPACE))
        update_consistency_state(asn_num, "CLEAN")

    # Export
    step_export(asn_num)
    update_rebase_timestamp(asn_num)

    print(f"  [DONE] {asn_label}", file=sys.stderr)
    return "completed"


def main():
    parser = argparse.ArgumentParser(
        description="Batch rebase — check and rebase all ASNs in dependency order")
    parser.add_argument("--exclude", "-x", nargs="+", type=int, default=[],
                        help="ASN numbers to exclude")
    parser.add_argument("--topic", "-t",
                        help="Only process ASNs with this topic")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max")
    parser.add_argument("--max-cycles", type=int, default=30,
                        help="Max convergence cycles (default: 30)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="Re-check all, ignore cached state")
    args = parser.parse_args()

    all_active = get_active_asns()
    asn_nums = [n for n in all_active if n not in args.exclude]

    if args.topic:
        filtered = [n for n in asn_nums
                    if (load_manifest(n) or {}).get("topic") == args.topic]
        if not filtered:
            known = sorted(set((load_manifest(n) or {}).get("topic", "")
                               for n in asn_nums) - {""})
            print(f"  [ERROR] No ASNs with topic '{args.topic}'. "
                  f"Known topics: {', '.join(known)}", file=sys.stderr)
            sys.exit(1)
        asn_nums = filtered

    graph = build_dep_graph(asn_nums)
    ordered = topological_sort(graph)

    print(f"\n  Rebase-all: {len(ordered)} ASNs in dependency order\n",
          file=sys.stderr)

    if args.dry_run:
        for i, num in enumerate(ordered, 1):
            label = f"ASN-{num:04d}"
            deps = graph.get(num, set())
            deps_str = ", ".join(f"{d:04d}" for d in sorted(deps)) or "—"
            status = needs_rebase(num)
            print(f"  {i:2d}. {label}  deps: [{deps_str}]  {status}",
                  file=sys.stderr)
        print("", file=sys.stderr)
        return

    completed = 0
    skipped = 0
    failed = 0

    for num in ordered:
        result = process_asn(num, args.model, args.effort,
                             args.max_cycles, force=args.force)

        if result == "completed":
            completed += 1
        elif result == "skipped":
            skipped += 1
        elif result == "failed":
            failed += 1
            print(f"\n  Batch stopped due to failure.", file=sys.stderr)
            break

    print(f"\n  Done: {completed} rebased, {skipped} clean, {failed} failed\n",
          file=sys.stderr)


if __name__ == "__main__":
    main()
