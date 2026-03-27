#!/usr/bin/env python3
"""
Dafny verification loop — verify → classify → fix → re-verify with tier escalation.

Orchestrates the three-tier verification loop (analogous to run-review.py):
  1. Verify: run dafny verify, parse errors, classify by tier
  2. Fix: LLM-assisted fix (Tier 1 = syntax, Tier 2 = proof with extract context)
  3. Re-verify: check fix, escalate tier if fix fails
  4. Escape: Tier 3 writes escalation report and exits

Exit codes:
    0 = verified
    1 = invocation error
    3 = Tier 3 escalation (spec error — needs ASN revision)

Usage:
    python scripts/model.py verify-dafny 1                     # verify + fix loop
    python scripts/model.py verify-dafny 1 --max-tier1 3       # up to 3 Tier 1 fix attempts
    python scripts/model.py verify-dafny 1 --max-tier2 2       # up to 2 Tier 2 fix attempts
    python scripts/model.py verify-dafny 1 --full               # proof-index → extract → generate → verify loop
    python scripts/model.py verify-dafny 1 --dry-run            # check paths, no execution
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import (WORKSPACE, ASNS_DIR, DAFNY_DIR, PROOF_INDEX_DIR,
                   VERIFICATION_DIR, USAGE_LOG,
                   find_latest_modeling_dir, formal_stmts)

VERIFY_SCRIPT = WORKSPACE / "scripts" / "lib" / "modeling" / "verify_run.py"
FIX_SCRIPT = WORKSPACE / "scripts" / "lib" / "modeling" / "fix.py"
PROOF_INDEX_SCRIPT = WORKSPACE / "scripts" / "lib" / "modeling" / "index.py"
EXTRACT_SCRIPT = WORKSPACE / "scripts" / "lib" / "modeling" / "statements.py"
GENERATE_SCRIPT = WORKSPACE / "scripts" / "lib" / "modeling" / "dafny.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def step_verify(asn_id, timeout=300):
    """Run verify-dafny.py. Returns (report_path, exit_code).

    Exit codes from verify-dafny.py:
        0 = verified, 2 = Tier 1 only, 3 = Tier 2+, 4 = Tier 3
    """
    print(f"\n  === VERIFY ===", file=sys.stderr)
    cmd = [sys.executable, str(VERIFY_SCRIPT), str(asn_id),
           "--timeout", str(timeout)]

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    report_path = result.stdout.strip()
    if report_path and Path(report_path).exists():
        return report_path, result.returncode

    if result.returncode == 1:
        return None, 1

    return None, result.returncode


def step_fix(asn_id, report_path=None, with_extract=False):
    """Run fix-dafny.py. Returns patched .dfy path or None."""
    tier_label = "Tier 2" if with_extract else "Tier 1"
    print(f"\n  === FIX ({tier_label}) ===", file=sys.stderr)

    cmd = [sys.executable, str(FIX_SCRIPT), str(asn_id)]
    if report_path:
        cmd.extend(["--report", str(report_path)])
    if with_extract:
        cmd.append("--with-extract")

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    if result.returncode != 0:
        print(f"  [FIX] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    dfy_path = result.stdout.strip()
    if dfy_path and Path(dfy_path).exists():
        return dfy_path
    return None


def step_commit(hint=""):
    """Run commit.py. Returns True if committed."""
    print(f"\n  === COMMIT ===", file=sys.stderr)
    cmd = [sys.executable, str(COMMIT_SCRIPT)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def step_proof_index(asn_id):
    """Run contract-asn.py. Returns proof index path or None."""
    print(f"\n  === PROOF INDEX ===", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(PROOF_INDEX_SCRIPT), str(asn_id)],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [PROOF-INDEX] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)
    path = result.stdout.strip()
    return path if path and Path(path).exists() else None


def step_extract(asn_id):
    """Run extract-properties.py. Returns extract path or None."""
    print(f"\n  === EXTRACT ===", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(EXTRACT_SCRIPT), str(asn_id)],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [EXTRACT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)
    path = result.stdout.strip()
    return path if path and Path(path).exists() else None


def step_generate(asn_id):
    """Run generate-dafny.py. Returns .dfy path or None."""
    print(f"\n  === GENERATE ===", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(GENERATE_SCRIPT), str(asn_id)],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [GENERATE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)
    path = result.stdout.strip()
    return path if path and Path(path).exists() else None


def is_stale(source, target):
    """Check if target is older than source (needs regeneration)."""
    if not target.exists():
        return True
    if not source.exists():
        return False
    return source.stat().st_mtime > target.stat().st_mtime


def write_escalation(asn_label, report_path, tier2_attempts):
    """Write a Tier 3 escalation report."""
    VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    esc_path = VERIFICATION_DIR / f"{asn_label}-escalation.md"

    # Read the latest verification report for error details
    report_content = ""
    try:
        report_content = Path(report_path).read_text()
    except (FileNotFoundError, OSError, TypeError):
        pass

    # Extract error summaries from report
    error_lines = []
    for m in re.finditer(r"^### Line (\d+) .+\n\n```\n(.+?)\n```",
                         report_content, re.MULTILINE | re.DOTALL):
        error_lines.append(f"- Line {m.group(1)}: {m.group(2).strip()}")

    errors_text = "\n".join(error_lines) if error_lines else "(see verification report)"

    content = f"""# Dafny Escalation — {asn_label}

*Generated: {time.strftime('%Y-%m-%d %H:%M')}*

## Verification Failures

{errors_text}

**Fix attempts:** {tier2_attempts} (Tier 2 exhausted)

## Assessment

The verification errors could not be resolved by automated Dafny fixes.
This indicates possible issues with the property statements themselves —
preconditions may be too weak, invariants may not hold on valid states,
or the formal encoding may not match the ASN's intent.

## Recommended action

Re-run review-revise cycle with these findings as input:
```
python scripts/review.py {asn_label.split('-')[1].lstrip('0') or '0'}
```
"""

    esc_path.write_text(content)
    return esc_path


def run_full_pipeline(asn_id, asn_label):
    """Run proof-index → extract → generate if stale or missing.

    Returns True if all steps succeeded, False otherwise.
    """
    asn_matches = sorted(ASNS_DIR.glob(f"{asn_label}-*.md"))
    if not asn_matches:
        print(f"  No ASN found for {asn_label}", file=sys.stderr)
        return False
    asn_path = asn_matches[0]

    index_path = PROOF_INDEX_DIR / f"{asn_label}-proof-index.md"
    asn_num = int(re.search(r'\d+', asn_label).group())
    extract_path = formal_stmts(asn_num)

    # Proof index: regenerate if ASN is newer
    if is_stale(asn_path, index_path):
        print(f"  [PIPELINE] Proof index stale or missing — regenerating",
              file=sys.stderr)
        if step_proof_index(asn_id) is None:
            return False
    else:
        print(f"  [PIPELINE] Proof index up to date", file=sys.stderr)

    # Extract: regenerate if proof index is newer
    if is_stale(index_path, extract_path):
        print(f"  [PIPELINE] Extract stale or missing — regenerating",
              file=sys.stderr)
        if step_extract(asn_id) is None:
            return False
    else:
        print(f"  [PIPELINE] Extract up to date", file=sys.stderr)

    # Generate: always fresh
    print(f"  [PIPELINE] Generating Dafny module", file=sys.stderr)
    if step_generate(asn_id) is None:
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Dafny verification loop with tier escalation")
    parser.add_argument("asn", help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--max-tier1", type=int, default=3,
                        help="Max Tier 1 fix attempts (default: 3)")
    parser.add_argument("--max-tier2", type=int, default=2,
                        help="Max Tier 2 fix attempts (default: 2)")
    parser.add_argument("--timeout", "-t", type=int, default=300,
                        help="Dafny verification timeout in seconds (default: 300)")
    parser.add_argument("--full", action="store_true",
                        help="Run full pipeline: proof-index → extract → generate → verify loop")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check paths and show plan without execution")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/",
              file=sys.stderr)
        sys.exit(1)

    gen_dir = find_latest_modeling_dir(asn_label)

    print(f"  [PIPELINE] {asn_label} — Dafny verification loop", file=sys.stderr)
    print(f"  [PIPELINE] Tier 1 max: {args.max_tier1}, "
          f"Tier 2 max: {args.max_tier2}", file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] ASN: {asn_path}", file=sys.stderr)
        print(f"  [DRY RUN] Dafny: {gen_dir or '(none)'}", file=sys.stderr)
        if args.full:
            index = PROOF_INDEX_DIR / f"{asn_label}-proof-index.md"
            asn_num = int(re.search(r'\d+', asn_label).group())
            extract = formal_stmts(asn_num)
            print(f"  [DRY RUN] --full: would check staleness of:", file=sys.stderr)
            print(f"    Proof index: {index} (exists: {index.exists()})",
                  file=sys.stderr)
            print(f"    Extract: {extract} (exists: {extract.exists()})",
                  file=sys.stderr)
        if gen_dir is None and not args.full:
            print(f"  [DRY RUN] No modeling directory found — "
                  f"use --full or run model.py dafny first", file=sys.stderr)
        return

    start = time.time()

    # Full pipeline: proof-index → extract → generate
    if args.full:
        print(f"\n  ──── Full Pipeline ────", file=sys.stderr)
        if not run_full_pipeline(args.asn, asn_label):
            print(f"  [PIPELINE] Full pipeline failed", file=sys.stderr)
            sys.exit(1)

    # Re-check modeling dir (may have been created by --full pipeline)
    if gen_dir is None:
        gen_dir = find_latest_modeling_dir(asn_label)
    if gen_dir is None or not any(gen_dir.glob("*.dfy")):
        print(f"  No .dfy files in {DAFNY_DIR.relative_to(WORKSPACE)}"
              f"/{asn_label}/modeling-*/",
              file=sys.stderr)
        print(f"  Run: python scripts/model.py dafny {args.asn}",
              file=sys.stderr)
        print(f"  Or use --full to run the complete pipeline", file=sys.stderr)
        sys.exit(1)

    # ── Verification loop ──────────────────────────────────────────────

    tier1_attempts = 0
    tier2_attempts = 0
    last_report = None

    print(f"\n  ──── Verification Loop ────", file=sys.stderr)

    while True:
        # Verify
        report_path, exit_code = step_verify(args.asn, args.timeout)

        if report_path is None and exit_code == 1:
            print(f"  [PIPELINE] Verification invocation failed", file=sys.stderr)
            sys.exit(1)

        last_report = report_path

        # Verified — done
        if exit_code == 0:
            print(f"\n  [PIPELINE] VERIFIED — all properties pass",
                  file=sys.stderr)
            step_commit(f"Verify {asn_label} — Dafny verification passed")
            break

        # Tier 1 only (exit code 2)
        if exit_code == 2:
            tier1_attempts += 1
            if tier1_attempts > args.max_tier1:
                print(f"\n  [PIPELINE] Tier 1 attempts exhausted "
                      f"({args.max_tier1}) — escalating to Tier 2",
                      file=sys.stderr)
                # Fall through to Tier 2
            else:
                print(f"\n  [PIPELINE] Tier 1 fix attempt "
                      f"{tier1_attempts}/{args.max_tier1}", file=sys.stderr)
                dfy = step_fix(args.asn, report_path, with_extract=False)
                if dfy is None:
                    print(f"  [PIPELINE] Tier 1 fix failed — escalating to Tier 2",
                          file=sys.stderr)
                else:
                    continue  # Re-verify

        # Tier 2+ (exit code 3, or Tier 1 exhausted)
        if exit_code in (2, 3):
            tier2_attempts += 1
            if tier2_attempts > args.max_tier2:
                print(f"\n  [PIPELINE] Tier 2 attempts exhausted "
                      f"({args.max_tier2}) — escalating to Tier 3",
                      file=sys.stderr)
                # Fall through to Tier 3 escape
            else:
                print(f"\n  [PIPELINE] Tier 2 fix attempt "
                      f"{tier2_attempts}/{args.max_tier2}", file=sys.stderr)
                dfy = step_fix(args.asn, report_path, with_extract=True)
                if dfy is None:
                    print(f"  [PIPELINE] Tier 2 fix failed", file=sys.stderr)
                    if tier2_attempts >= args.max_tier2:
                        pass  # Fall through to Tier 3
                    else:
                        continue  # Try again
                else:
                    continue  # Re-verify

        # Tier 3 escape (exit code 4, or all attempts exhausted)
        print(f"\n  [PIPELINE] TIER 3 ESCAPE — writing escalation report",
              file=sys.stderr)
        esc_path = write_escalation(asn_label, last_report, tier2_attempts)
        print(f"  [WROTE] {esc_path.relative_to(WORKSPACE)}", file=sys.stderr)
        step_commit(f"Verify {asn_label} — escalation (Tier 3)")

        elapsed = time.time() - start
        print(f"\n  [PIPELINE] Done ({elapsed:.0f}s) — "
              f"Tier 3 escalation, exit 3", file=sys.stderr)
        sys.exit(3)

    elapsed = time.time() - start
    print(f"\n  [PIPELINE] Done ({elapsed:.0f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
