#!/usr/bin/env python3
"""
Contract alignment + fix for Dafny files.

Provides the align-with-contract agent call and the align-validate cycle,
plus a standalone CLI for fixing unverified files.

Usage:
    python scripts/lib/verification/dafny/align.py 34
    python scripts/lib/verification/dafny/align.py 34 --claim TA3
    python scripts/lib/verification/dafny/align.py 34 --dry-run
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
from lib.shared.paths import WORKSPACE, CLAIM_DIR, DAFNY_DIR, prompt_path
from lib.shared.claim_files import build_label_index
from lib.verification.dafny.common import read_file, log_usage
from lib.verification.dafny.verify import verify
from lib.verification.dafny.validate import validate
from lib.shared.prompts import read_prompt

ALIGN_TEMPLATE = prompt_path("verification/dafny/align-with-contract.md")


def align(dfy_path, errors, formal_contract, *, asn_label, claim_label,
          cycle_num, model="opus", effort="max", max_turns=12):
    """Run align-with-contract agent. Returns (success, elapsed, cost).

    Agent commits after each dafny verify (path-scoped). Audit trail
    accumulates in `git log -- <dfy_path>` showing the align cycle's
    sequence of attempted fixes.
    """
    from lib.shared.invoke_claude import invoke_claude_agent
    from lib.shared.paths import WORKSPACE

    dfy_source = read_file(dfy_path)
    align_template = read_prompt(ALIGN_TEMPLATE)
    prompt = (align_template
        .replace("{{dfy_path}}", str(dfy_path))
        .replace("{{dfy_source}}", dfy_source)
        .replace("{{errors}}", errors)
        .replace("{{formal_contract}}", formal_contract or "(not available)"))

    # Append commit instructions — agent self-commits after each verify
    # for audit trail. Path-scoped to avoid sweeping unrelated work.
    prompt += f"""

## After EACH dafny verify, commit

Every `dafny verify` invocation (pass or fail) must be followed by a
git commit. This produces an audit trail of each attempted fix within
the align cycle.

After writing the .dfy and running verify:

  dafny verify {dfy_path} 2>&1 | tee /tmp/dafny-verify-{claim_label}.txt
  # determine status: "verified" if "0 errors";
  # "proof_failure" otherwise.
  {{
    echo "dafny({asn_label}): {claim_label} align-{cycle_num} → $status"
    echo
    cat /tmp/dafny-verify-{claim_label}.txt
  }} | git commit -- {dfy_path} -F -

The `-- {dfy_path}` is REQUIRED. It scopes the commit to ONLY this
.dfy. Without it, the commit would sweep unrelated staged work.

This commit happens for EVERY verify, including failures.
"""

    # Route through the shared wrapper — gets JSON envelope error
    # detection, quota cooldown, overload backoff+poll, account
    # rotation. Was previously a raw subprocess.run.
    res = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Write,Bash",
        enabled_tools="Read,Write,Bash",
        max_turns=max_turns,
        cwd=WORKSPACE,
    )

    # Success = wrapper got a result envelope without error
    ok = res.ok and res.data is not None and not res.data.get("is_error", False)
    return ok, res.elapsed, res.cost or 0


def align_validate_cycle(dfy_path, formal_contract, label,
                          *, asn_label,
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
            asn_label=asn_label, claim_label=label, cycle_num=cycle,
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
    parser.add_argument("--claim", "-p",
                        help="Fix specific claims, comma-separated")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per claim (default: 24)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be fixed without invoking Claude")
    args = parser.parse_args()

    # Find dafny directory
    num = re.sub(r"[^0-9]", "", str(args.asn))
    if not num:
        print(f"  Invalid ASN: {args.asn}", file=sys.stderr)
        sys.exit(1)
    asn_label = f"ASN-{int(num):04d}"
    gen_dir = DAFNY_DIR / asn_label
    if not gen_dir.exists():
        print(f"  No dafny directory found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    print(f"[FIX] {asn_label} — {gen_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Load formal contracts from per-claim files
    claim_dir = CLAIM_DIR / asn_label
    contract_sections = {}
    label_map = {}
    if claim_dir.exists():
        _label_index = build_label_index(claim_dir)
        _filename_to_label = {f"{stem}.md": lbl for lbl, stem in _label_index.items()}
        for f in claim_dir.glob("*.md"):
            if f.name.startswith("_"):
                continue
            label = _filename_to_label.get(f.name, f.stem)
            content = f.read_text()
            contract_sections[label] = content
            m = re.search(r'^\*\*\S+\s*\(([A-Z][a-zA-Z0-9]+)\)', content, re.MULTILINE)
            if m:
                label_map[m.group(1)] = label

    # Find .dfy files
    dfy_files = sorted(gen_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files found in {gen_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    # Filter to specific claims if requested
    if args.claim:
        targets = [t.strip() for t in args.claim.split(",")]
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
    review_dir = gen_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    total_cost = 0
    fixed = 0

    for dfy_path, errors in failures:
        print(f"\n  [{dfy_path.stem}]...", file=sys.stderr, end="", flush=True)

        # Find formal contract for this claim
        claim_label = label_map.get(dfy_path.stem, "")
        formal_contract = contract_sections.get(claim_label, "")

        _, elapsed, cost = align(
            dfy_path, errors, formal_contract=formal_contract,
            asn_label=asn_label, claim_label=claim_label, cycle_num=0,
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
                contract_result, reason, a_cost = align_validate_cycle(
                    dfy_path, formal_contract, claim_label,
                    asn_label=asn_label,
                    model=args.model, effort=args.effort)
                total_cost += a_cost
            else:
                print(f" (no contract)", file=sys.stderr)

            if contract_result in ("CLEAN", ""):
                fixed += 1
                # Clean — remove stale review
                review_path = review_dir / f"{claim_label}.md"
                if review_path.exists():
                    review_path.unlink()
            elif contract_result == "FLAG":
                review_path = review_dir / f"{claim_label}.md"
                with open(review_path, "w") as rf:
                    rf.write(f"# {claim_label} — Contract FLAG\n\n")
                    rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                    rf.write(f"{reason}\n")
        elif status == "compile_failure":
            print(f" COMPILE FAILURE", file=sys.stderr)
        elif status == "proof_failure":
            print(f" STILL PROOF FAILURE", file=sys.stderr)
        else:
            print(f" {status.upper()}", file=sys.stderr)

        log_usage(asn_label, dfy_path.stem, elapsed, status == "verified", cost)

    print(f"\n  Done: {fixed}/{len(failures)} fixed, ${total_cost:.2f}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
