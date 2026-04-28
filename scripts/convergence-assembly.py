#!/usr/bin/env python3
"""
Formalization Assembly — produce formal-statements.md + dependency graph.

Mechanically assembles the export from YAML summaries + .md formal contracts.
No LLM calls. Requires summaries — run summarize.py first.

Usage:
    python scripts/convergence-assembly.py 34
    python scripts/convergence-assembly.py 34 36 40
    python scripts/convergence-assembly.py 34 --deps-only
    python scripts/convergence-assembly.py 34 --dry-run
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, formal_stmts, dep_graph
from lib.shared.common import find_asn
from lib.claim_convergence.assembly.produce_interface import assemble_formal_statements
from lib.claim_convergence.core.build_dependency_graph import generate_claim_convergence_deps, write_deps_yaml

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _generate_deps(asn_num, label):
    """Generate deps YAML from per-claim metadata."""
    try:
        deps = generate_claim_convergence_deps(asn_num)
        if deps:
            path = write_deps_yaml(asn_num, deps)
            print(f"  [DEPS] {path.relative_to(WORKSPACE)} "
                  f"({len(deps['claims'])} claims)", file=sys.stderr)
        else:
            print(f"  [DEPS] WARNING: extract failed for {label}",
                  file=sys.stderr)
    except Exception as e:
        print(f"  [DEPS] WARNING: extract failed for {label}: {e}",
              file=sys.stderr)


def _export_one(asn_id):
    """Export a single ASN: assembly + deps.

    Returns (asn_label, True) on success, (asn_id, False) on failure.
    """
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id}", file=sys.stderr)
        return asn_id, False

    asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))

    # Assembly (mechanical — reads YAML summaries + .md contracts)
    path = assemble_formal_statements(asn_num)
    if path is None:
        print(f"  [ERROR] Assembly failed for {asn_label}", file=sys.stderr)
        return asn_label, False

    print(str(path))

    # Deps generation (already mechanical)
    _generate_deps(asn_num, asn_label)

    return asn_label, True


def main():
    parser = argparse.ArgumentParser(
        description="Formalization Assembly — formal-statements.md + deps")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 34 36 40) or paths")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without doing it")
    parser.add_argument("--deps-only", action="store_true",
                        help="Generate dependency graph only, skip formal-statements")
    args = parser.parse_args()

    if args.dry_run:
        for asn_id in args.asns:
            _, asn_label = find_asn(asn_id)
            print(f"  [DRY RUN] Would export {asn_label}", file=sys.stderr)
        return

    if args.deps_only:
        for asn_id in args.asns:
            asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))
            _, asn_label = find_asn(asn_id)
            if asn_label:
                _generate_deps(asn_num, asn_label)
        return

    succeeded = []
    failed = []

    for asn_id in args.asns:
        label, ok = _export_one(asn_id)
        if ok:
            succeeded.append(label)
        else:
            failed.append(label)

    # Commit
    if succeeded:
        labels = ", ".join(sorted(succeeded))
        print(f"\n  === COMMIT ({labels}) ===", file=sys.stderr)
        for lbl in sorted(succeeded):
            lbl_num = int(re.sub(r"[^0-9]", "", lbl))
            subprocess.run(
                ["git", "add", str(formal_stmts(lbl_num)), str(dep_graph(lbl_num))],
                capture_output=True, text=True, cwd=str(WORKSPACE))
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"Export formal statements {labels}"]
        subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE))

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
