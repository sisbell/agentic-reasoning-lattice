#!/usr/bin/env python3
"""
Contract alignment + fix for Dafny files.

Provides the align-with-contract agent call and the align-validate cycle,
plus a standalone CLI for fixing unverified files.

Usage:
    python scripts/lib/modeling/dafny/align.py 1
    python scripts/lib/modeling/dafny/align.py 1 --property TA3
    python scripts/lib/modeling/dafny/align.py 1 --modeling 2
    python scripts/lib/modeling/dafny/align.py 1 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE
from lib.modeling.dafny.common import read_file, write_status_file, find_modeling_dir, log_usage
from lib.modeling.dafny.verify import verify
from lib.modeling.dafny.validate import validate

ALIGN_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "modeling" / "dafny" / "align-with-contract.md"


def align(dfy_path, errors, formal_contract, model="opus",
              effort="max", max_turns=12):
    """Run align-with-contract agent. Returns (success, elapsed, cost)."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--tools", "Read,Write,Bash",
        "--allowedTools", "Read,Write,Bash",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    dfy_source = read_file(dfy_path)
    align_template = read_file(ALIGN_TEMPLATE)
    prompt = (align_template
        .replace("{{dfy_path}}", str(dfy_path))
        .replace("{{dfy_source}}", dfy_source)
        .replace("{{errors}}", errors)
        .replace("{{formal_contract}}", formal_contract or "(not available)"))

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    cost = 0
    try:
        data = json.loads(result.stdout)
        cost = data.get("total_cost_usd", 0)
    except (json.JSONDecodeError, KeyError):
        pass

    return result.returncode == 0, elapsed, cost


def align_validate_cycle(dfy_path, formal_contract, label,
                          model="opus", effort="max", max_cycles=3):
    """Validate contract, then align -> verify -> validate cycle if FLAG.

    Runs initial validation. If CLEAN, returns immediately. If FLAG,
    runs align cycles until CLEAN or cycle limit. Prints status to stderr.
    Returns (contract_result, reason, total_cost).
    """
    # Initial validation
    rec, reason, _ = validate(dfy_path.read_text(), formal_contract, label)
    contract_result = rec.upper()
    total_cost = 0
    print(f" {contract_result}", file=sys.stderr,
          end="" if rec == "flag" else "\n", flush=True)

    for cycle in range(1, max_cycles + 1):
        if rec != "flag":
            break

        print(f"  [{label}] align cycle {cycle}...",
              file=sys.stderr, end="", flush=True)
        flag_errors = f"Contract validation failed:\n{reason}"
        ok, a_elapsed, a_cost = align(
            dfy_path, flag_errors, formal_contract,
            model=model, effort=effort)
        total_cost += a_cost

        # Re-verify after align
        a_status, a_vout = verify(dfy_path)
        if a_status != "verified":
            # Align broke the proof — feed dafny errors back
            print(f" {a_status.upper()}",
                  file=sys.stderr, end="", flush=True)
            reason = a_vout
            rec = "flag"
            contract_result = a_status.upper()
            continue

        # Re-validate contract
        rec, reason, _ = validate(
            dfy_path.read_text(), formal_contract, label)
        contract_result = rec.upper()
        print(f" {contract_result}", file=sys.stderr)

    return contract_result, reason, total_cost


def main():
    parser = argparse.ArgumentParser(
        description="Fix unverified Dafny files with agentic baby-steps")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Fix specific properties, comma-separated (e.g., T5 or T1,T3,TA0)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target specific modeling-N directory")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per property (default: 24)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be fixed without invoking Claude")
    args = parser.parse_args()

    # Find modeling directory
    num = re.sub(r"[^0-9]", "", str(args.asn))
    if not num:
        print(f"  Invalid ASN: {args.asn}", file=sys.stderr)
        sys.exit(1)
    asn_label = f"ASN-{int(num):04d}"
    gen_dir = find_modeling_dir(asn_label, args.modeling)
    if gen_dir is None:
        print(f"  No modeling directory found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    print(f"[FIX] {asn_label} — {gen_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Load formal contracts for contract alignment
    from lib.shared.paths import formal_stmts
    from lib.shared.common import extract_property_sections
    asn_num = int(re.sub(r"[^0-9]", "", asn_label))
    stmts_path = formal_stmts(asn_num)
    contract_sections = {}
    label_map = {}
    if stmts_path.exists():
        stmts_text = stmts_path.read_text()
        # Build label map: PascalCase name -> label
        for line in stmts_text.split("\n"):
            m = re.match(r'^##\s+(.+?)\s+\u2014\s+(.+?)(?:\s+\(|$)', line)
            if m:
                label = m.group(1).strip()
                name = m.group(2).strip()
                pascal = re.match(r'^([A-Z][a-zA-Z0-9]+)', name)
                if pascal:
                    label_map[pascal.group(1)] = label
        all_labels = list(set(label_map.values()))
        contract_sections = extract_property_sections(
            stmts_text, known_labels=all_labels, truncate=False)

    # Find .dfy files
    dfy_files = sorted(gen_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files found in {gen_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [f for f in dfy_files
                     if target.lower() in f.stem.lower()]
            if not found:
                print(f"  No file matching '{target}' found",
                      file=sys.stderr)
                print(f"  Available: {', '.join(f.stem for f in dfy_files)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        dfy_files = matches

    # Verify each file, collect proof failures (skip compile failures)
    failures = []
    compile_failures = []
    for dfy_path in dfy_files:
        status, output = verify(dfy_path)
        if status == "verified":
            print(f"  [OK] {dfy_path.stem}", file=sys.stderr)
        elif status == "compile_failure":
            print(f"  [COMPILE FAILURE] {dfy_path.stem} — needs regeneration",
                  file=sys.stderr)
            compile_failures.append(dfy_path)
        elif status == "proof_failure":
            error_lines = [line for line in output.split("\n")
                           if re.search(r"Error:", line)]
            failures.append((dfy_path, output))
            print(f"  [PROOF FAILURE] {dfy_path.stem}: "
                  f"{error_lines[0] if error_lines else 'solver rejected'}",
                  file=sys.stderr)
        else:
            print(f"  [{status.upper()}] {dfy_path.stem}", file=sys.stderr)

    if compile_failures:
        print(f"\n  {len(compile_failures)} compile failure(s) — skipped, "
              f"need regeneration", file=sys.stderr)

    if not failures:
        print(f"\n  No proof failures to fix.", file=sys.stderr)
        return

    print(f"\n  {len(failures)} proof failure(s) to fix", file=sys.stderr)

    if args.dry_run:
        for dfy_path, _ in failures:
            print(f"  [DRY RUN] Would fix {dfy_path.stem}", file=sys.stderr)
        return

    # Fix each failure
    total_cost = 0
    fixed = 0
    fix_results = []

    for dfy_path, errors in failures:
        print(f"\n  [{dfy_path.stem}]...", file=sys.stderr, end="", flush=True)

        # Find formal contract for this property
        prop_label = label_map.get(dfy_path.stem, "")
        formal_contract = contract_sections.get(prop_label, "")

        _, elapsed, cost = align(
            dfy_path, errors, formal_contract=formal_contract,
            model=args.model, effort=args.effort, max_turns=args.max_turns,
        )
        total_cost += cost

        # Verify result — validation chain
        status, vout = verify(dfy_path)
        contract_result = ""
        if status == "verified":
            m = re.search(r"(\d+) verified", vout)
            n = m.group(1) if m else "?"
            print(f" verified({n})", file=sys.stderr, end="", flush=True)

            # Validate contract + align cycle if FLAG
            if formal_contract:
                contract_result, _, a_cost = align_validate_cycle(
                    dfy_path, formal_contract, prop_label,
                    model=args.model, effort=args.effort)
                total_cost += a_cost
                print(f" {contract_result}", file=sys.stderr)
            else:
                print(f" (no contract)", file=sys.stderr)

            if contract_result in ("CLEAN", ""):
                fixed += 1
        elif status == "compile_failure":
            print(f" COMPILE FAILURE", file=sys.stderr)
        elif status == "proof_failure":
            print(f" STILL PROOF FAILURE", file=sys.stderr)
        else:
            print(f" {status.upper()}", file=sys.stderr)

        fix_results.append({
            "proof_label": dfy_path.stem,
            "status": status,
            "contract": contract_result,
            "cost": cost,
        })
        log_usage(asn_label, dfy_path.stem, elapsed, status == "verified", cost)

    # Update STATUS.md with fix results
    write_status_file(gen_dir, fix_results, source="fix")
    print(f"\n  Done: {fixed}/{len(failures)} fixed, ${total_cost:.2f}",
          file=sys.stderr)
    print(f"  Status: {gen_dir.name}/STATUS.md", file=sys.stderr)


if __name__ == "__main__":
    main()
