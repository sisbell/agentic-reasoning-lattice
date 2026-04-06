#!/usr/bin/env python3
"""
Elaboration Assembly — format gate + formal-statements + deps from an elaborated ASN.

Always runs format gate first (elaboration may leave rough formatting).
No contract validation — contracts are rough at this stage.

Usage:
    python scripts/elaboration-assembly.py 40
    python scripts/elaboration-assembly.py 34 40 42    # multiple ASNs
    python scripts/elaboration-assembly.py 40 --dry-run
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, formal_stmts, dep_graph
from lib.shared.common import find_asn
from lib.formalization.core.asn_normalizer import step_stabilize
from lib.formalization.assembly.produce_interface import assemble_formal_statements
from lib.formalization.core.build_dependency_graph import generate_deps, write_deps_yaml

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _assemble_one(asn_id):
    """Format gate + assembly + deps for one ASN.

    Returns (asn_label, True) on success, (asn_id, False) on failure.
    """
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id}", file=sys.stderr)
        return asn_id, False

    asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))

    # Format gate (always)
    print(f"\n  [FORMAT] {asn_label}", file=sys.stderr)
    step_stabilize(asn_num)

    # Assembly
    path = assemble_formal_statements(asn_num)
    if path is None:
        print(f"  [ERROR] Assembly failed for {asn_label}", file=sys.stderr)
        return asn_label, False

    print(f"  {path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Deps
    try:
        deps = generate_deps(asn_num)
        if deps:
            write_deps_yaml(asn_num, deps)
            print(f"  dependency-graph.yaml", file=sys.stderr)
    except Exception as e:
        print(f"  [DEPS] WARNING: {e}", file=sys.stderr)

    # LLM dep scan
    try:
        from lib.formalization.assembly.scan_undeclared_deps import scan_asn
        scan_asn(asn_num, model="sonnet", effort="high")
    except Exception as e:
        print(f"  [DEPS] WARNING: LLM scan failed: {e}", file=sys.stderr)

    return asn_label, True


def main():
    parser = argparse.ArgumentParser(
        description="Elaboration Assembly — format + formal-statements + deps")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 40 34 42)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done")
    args = parser.parse_args()

    if args.dry_run:
        for asn_id in args.asns:
            _, asn_label = find_asn(asn_id)
            print(f"  [DRY RUN] Would assemble {asn_label}", file=sys.stderr)
        return

    succeeded = []
    failed = []

    for asn_id in args.asns:
        label, ok = _assemble_one(asn_id)
        if ok:
            succeeded.append(label)
        else:
            failed.append(label)

    # Commit
    if succeeded:
        labels = ", ".join(sorted(succeeded))
        print(f"\n  [COMMIT] {labels}", file=sys.stderr)
        for lbl in sorted(succeeded):
            lbl_num = int(re.sub(r"[^0-9]", "", lbl))
            subprocess.run(
                ["git", "add",
                 str(formal_stmts(lbl_num)),
                 str(dep_graph(lbl_num))],
                capture_output=True, text=True, cwd=str(WORKSPACE))
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"elaboration-assembly: {labels}"]
        subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE))

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
