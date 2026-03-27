#!/usr/bin/env python3
"""
Formalize all ASNs in dependency order.

Processes ASNs topologically (foundations first). For each ASN:
  1. Check if pipeline run needed (deps newer than last run, or --force)
  2. If needed -> run the formalization pipeline
  3. If not -> skip

Usage:
    python scripts/formalize-all.py                       # all active ASNs
    python scripts/formalize-all.py --only 34 36          # specific ASNs
    python scripts/formalize-all.py --exclude 40 42       # skip specific
    python scripts/formalize-all.py --topic foundation    # only a topic
    python scripts/formalize-all.py --dry-run             # show order + status
    python scripts/formalize-all.py --force               # ignore cached state
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (WORKSPACE, PROJECT_MODEL_DIR, load_manifest,
                   formal_stmts, project_yaml)
from lib.shared.common import find_asn
from lib.formalization.run import run_pipeline


def get_active_asns():
    """Get active ASN numbers from project model yamls."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*/project.yaml"):
        m = re.match(r"ASN-(\d+)", path.parent.name)
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
    """Topological sort -- returns list in dependency order."""
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


def needs_update(asn_num, force=False):
    """Check if an ASN needs a pipeline run."""
    if force:
        return True

    manifest = load_manifest(asn_num)
    if not manifest:
        return False

    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return False

    stmts_path = formal_stmts(asn_num)
    if not stmts_path.exists():
        return True

    yaml_path = project_yaml(asn_num)
    if yaml_path.exists():
        import yaml
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            data = {}

        last_run = data.get("last_pipeline_run", "")
        if last_run:
            try:
                last_ts = datetime.fromisoformat(
                    last_run.strip('"')).timestamp()
            except (ValueError, TypeError):
                last_ts = 0
        else:
            last_ts = 0

        if asn_path.stat().st_mtime > last_ts:
            return True

        for dep in manifest.get("depends", []):
            dep_stmts = formal_stmts(dep)
            if dep_stmts.exists() and dep_stmts.stat().st_mtime > last_ts:
                return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Formalize all ASNs in dependency order")
    parser.add_argument("--only", nargs="+", type=int, default=[],
                        help="Only process these ASN numbers")
    parser.add_argument("--exclude", "-x", nargs="+", type=int, default=[],
                        help="ASN numbers to exclude")
    parser.add_argument("--topic", "-t",
                        help="Only process ASNs with this topic")
    parser.add_argument("--max-review-cycles", type=int, default=30,
                        help="Max review/revise cycles (default: 30)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cached state, run all")
    args = parser.parse_args()

    all_active = get_active_asns()
    if args.only:
        asn_nums = [n for n in args.only if n in all_active]
    else:
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

    print(f"\n  Formalize: {len(ordered)} ASNs in dependency order\n",
          file=sys.stderr)

    if args.dry_run:
        for i, num in enumerate(ordered, 1):
            label = f"ASN-{num:04d}"
            deps = graph.get(num, set())
            deps_str = ", ".join(f"{d:04d}" for d in sorted(deps)) or "—"
            status = "update" if needs_update(num, args.force) else "skip"
            print(f"  {i:2d}. {label}  deps: [{deps_str}]  {status}",
                  file=sys.stderr)
        print("", file=sys.stderr)
        return

    completed = 0
    skipped = 0
    failed = 0

    for num in ordered:
        if not needs_update(num, args.force):
            label = f"ASN-{num:04d}"
            print(f"  [{label}] Up to date", file=sys.stderr)
            skipped += 1
            continue

        result = run_pipeline(num, force=args.force,
                              max_review_cycles=args.max_review_cycles)

        if result == "completed":
            completed += 1
        elif result == "failed":
            failed += 1
            print(f"\n  Pipeline stopped due to failure.",
                  file=sys.stderr)
            break
        else:
            skipped += 1

    print(f"\n  Done: {completed} completed, {skipped} skipped, "
          f"{failed} failed\n", file=sys.stderr)


if __name__ == "__main__":
    main()
