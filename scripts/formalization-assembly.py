#!/usr/bin/env python3
"""
Formalization Export — assemble formal-statements.md + deps from a formalized ASN.

Mechanically extracts formal interface from the property table and derivation
sections, trims narrative via LLM, then generates the dependency graph
(mechanical + LLM scan). Commits both artifacts.

Usage:
    python scripts/formalization-export.py 40
    python scripts/formalization-export.py 40 --normalize   # run format gate first
    python scripts/formalization-export.py 40 --dry-run
    python scripts/formalization-export.py 34 36 40          # multiple ASNs
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, formal_stmts, dep_graph, load_manifest
from lib.shared.common import find_asn
from lib.formalization.assembly.produce_interface import assemble_formal_statements
from lib.formalization.assembly.validate_contracts import validate_contracts
from lib.formalization.core.build_dependency_graph import generate_deps, write_deps_yaml

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _generate_deps(asn_num, label):
    """Generate deps YAML: mechanical extract + LLM scan."""
    # Phase 1: Mechanical extract
    try:
        deps = generate_deps(asn_num)
        if deps:
            path = write_deps_yaml(asn_num, deps)
            print(f"  [DEPS] mechanical: {path.relative_to(WORKSPACE)} "
                  f"({len(deps['properties'])} properties)", file=sys.stderr)
        else:
            print(f"  [DEPS] WARNING: mechanical extract failed for {label}",
                  file=sys.stderr)
            return
    except Exception as e:
        print(f"  [DEPS] WARNING: mechanical extract failed for {label}: {e}",
              file=sys.stderr)
        return

    # Phase 2: LLM scan for undeclared dependencies
    try:
        from lib.formalization.assembly.scan_undeclared_deps import scan_asn
        scan_asn(asn_num, model="sonnet", effort="high")
    except Exception as e:
        print(f"  [DEPS] WARNING: LLM dep scan failed for {label}: {e}",
              file=sys.stderr)


def _export_one(asn_id, do_format_gate=False, contract_check="fail"):
    """Export a single ASN: optional format gate + contract validation + assembly + deps.

    contract_check: "fail" (default), "warn", or "skip"

    Returns (asn_label, True) on success, (asn_id, False) on failure.
    """
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id}", file=sys.stderr)
        return asn_id, False

    asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))

    # Format gate (if requested)
    if do_format_gate:
        from lib.blueprinting.format import normalize_format
        ok = normalize_format(asn_num)
        if not ok:
            print(f"  [ERROR] Format normalization failed for {asn_label}",
                  file=sys.stderr)
            return asn_label, False

    # Contract validation gate
    if contract_check != "skip":
        mismatches = validate_contracts(asn_num)
        if mismatches:
            for label, detail in mismatches:
                print(f"  [CONTRACT MISMATCH] {label}: {detail}",
                      file=sys.stderr)
            if contract_check == "fail":
                print(f"  [ERROR] {len(mismatches)} contract mismatch(es) — "
                      f"aborting assembly for {asn_label}", file=sys.stderr)
                return asn_label, False
            else:
                print(f"  [WARNING] {len(mismatches)} contract mismatch(es) — "
                      f"continuing (warn mode)", file=sys.stderr)

    # Assembly
    path = assemble_formal_statements(asn_num)
    if path is None:
        print(f"  [ERROR] Assembly failed for {asn_label}", file=sys.stderr)
        return asn_label, False

    print(str(path))

    # Deps generation
    _generate_deps(asn_num, asn_label)

    return asn_label, True


def main():
    parser = argparse.ArgumentParser(
        description="Formalization Export — formal-statements.md + deps from formalized ASNs")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 55 56 34) or paths")
    parser.add_argument("--normalize", action="store_true",
                        help="Run format normalization gate before assembly")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without doing it")
    parser.add_argument("--skip-contract-check", action="store_true",
                        help="Skip contract validation gate")
    parser.add_argument("--warn-contract-check", action="store_true",
                        help="Report contract mismatches without failing")
    args = parser.parse_args()

    if args.dry_run:
        for asn_id in args.asns:
            _, asn_label = find_asn(asn_id)
            print(f"  [DRY RUN] Would export {asn_label}", file=sys.stderr)
        return

    succeeded = []
    failed = []

    contract_check = "fail"
    if args.skip_contract_check:
        contract_check = "skip"
    elif args.warn_contract_check:
        contract_check = "warn"

    for asn_id in args.asns:
        label, ok = _export_one(asn_id, do_format_gate=args.normalize,
                                contract_check=contract_check)
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

        # Hint for extensions
        if len(args.asns) == 1:
            asn_num = int(re.sub(r"[^0-9]", "", str(args.asns[0])))
            manifest = load_manifest(asn_num)
            if manifest.get("extends"):
                print(f"\n  [NEXT] Absorb into base: "
                      f"python scripts/absorb.py {asn_num}",
                      file=sys.stderr)

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
