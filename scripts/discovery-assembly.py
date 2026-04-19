#!/usr/bin/env python3
"""
Discovery Export — extract formal-statements.md + deps from a discovery ASN.

Uses LLM to parse narrative reasoning into structured formal statements,
then generates the dependency graph (mechanical + LLM scan).
Commits both artifacts.

Usage:
    python scripts/discovery-export.py 40
    python scripts/discovery-export.py 40 --dry-run
    python scripts/discovery-export.py 34 36 40          # multiple ASNs
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, formal_stmts, dep_graph
from lib.shared.common import find_asn
from lib.discovery.assembly.produce_statements import export_one
from lib.formalization.core.build_dependency_graph import generate_discovery_deps, write_deps_yaml

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _generate_deps(asn_num, label):
    """Generate deps YAML: mechanical extract + LLM scan."""
    try:
        deps = generate_discovery_deps(asn_num)
        if deps:
            path = write_deps_yaml(asn_num, deps)
            print(f"  [DEPS] mechanical: {path.relative_to(WORKSPACE)} "
                  f"({len(deps['claims'])} claims)", file=sys.stderr)
        else:
            print(f"  [DEPS] WARNING: mechanical extract failed for {label}",
                  file=sys.stderr)
            return
    except Exception as e:
        print(f"  [DEPS] WARNING: mechanical extract failed for {label}: {e}",
              file=sys.stderr)
        return

    try:
        from lib.formalization.assembly.scan_undeclared_deps import scan_asn
        scan_asn(asn_num, model="sonnet", effort="high")
    except Exception as e:
        print(f"  [DEPS] WARNING: LLM dep scan failed for {label}: {e}",
              file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Discovery Export — formal-statements.md + deps from discovery ASNs")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 55 56 34) or paths")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model for statement extraction (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (default: high)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without doing it")
    parser.add_argument("--deps-only", action="store_true",
                        help="Generate dependency graph only, skip formal-statements")
    args = parser.parse_args()

    if args.deps_only:
        for asn_id in args.asns:
            asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))
            _, label = find_asn(asn_id)
            if label:
                _generate_deps(asn_num, label)
        return

    succeeded = []
    failed = []

    for asn_id in args.asns:
        label, ok = export_one(asn_id, model=args.model,
                                effort=args.effort, dry_run=args.dry_run)
        if ok:
            succeeded.append(label)
            # Generate deps (unless dry run)
            if not args.dry_run:
                asn_num = int(re.sub(r"[^0-9]", "", label))
                _generate_deps(asn_num, label)
        else:
            failed.append(label)

    # Commit
    if succeeded and not args.dry_run:
        labels = ", ".join(sorted(succeeded))
        print(f"\n  === COMMIT ({labels}) ===", file=sys.stderr)
        for lbl in sorted(succeeded):
            lbl_num = int(re.sub(r"[^0-9]", "", lbl))
            subprocess.run(
                ["git", "add", str(formal_stmts(lbl_num)), str(dep_graph(lbl_num))],
                capture_output=True, text=True, cwd=str(WORKSPACE))
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"Export statements {labels}"]
        subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE))

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
