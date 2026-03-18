#!/usr/bin/env python3
"""
Verify a Dafny specification and classify errors by tier.

Runs `dafny verify` on the generated .dfy file, parses errors into
structured format, and classifies each error as Tier 1 (syntax/type),
Tier 2 (proof-structural), or Tier 3 (spec error).

Writes a verification report to vault/4-modeling/verification/.

Exit codes:
    0 = verified (all properties pass)
    1 = invocation error (dafny not found, bad arguments)
    2 = all errors are Tier 1 (syntax/type — auto-fixable)
    3 = Tier 2 errors present (proof-structural)
    4 = Tier 3 errors present (spec error — escape)

Usage:
    python scripts/lib/model_verify_run.py 1
    python scripts/lib/model_verify_run.py ASN-0001 --dry-run
    python scripts/lib/model_verify_run.py ASN-0001 --timeout 120
"""

import argparse
import json
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, VERIFICATION_DIR, USAGE_LOG,
                    find_latest_modeling_dir)


# ── Error categorization patterns ──────────────────────────────────────

TIER_1_PATTERNS = [
    r"unresolved identifier",
    r"wrong number of (?:type )?arguments",
    r"type mismatch",
    r"member .+ does not exist",
    r"invalid UnaryExpression",
    r"invalid expression",
    r"expected .+ got",
    r"undeclared identifier",
    r"not a type",
    r"incorrect argument type",
    r"arguments must have comparable types",
    r"duplicate member name",
    r"rbrace expected",
    r"semicolon expected",
    r"syntax error",
]

TIER_2_PATTERNS = [
    r"postcondition might not hold",
    r"assertion might not hold",
    r"decreases expression might not decrease",
    r"cannot prove termination",
    r"insufficient reads clause",
    r"insufficient triggers",
    r"function precondition might not hold",
    r"index out of range",
    r"possible division by zero",
    r"call may violate context's modifies clause",
    r"timed? ?out",
    r"out of resource",
]

TIER_1_RE = re.compile("|".join(TIER_1_PATTERNS), re.IGNORECASE)
TIER_2_RE = re.compile("|".join(TIER_2_PATTERNS), re.IGNORECASE)


def find_dafny_files(asn_id):
    """Find .dfy files for an ASN in the latest modeling directory.

    Returns (list_of_dfy_paths, asn_label). Empty list if none found.
    """
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return [], None
    label = f"ASN-{int(num):04d}"
    gen_dir = find_latest_modeling_dir(label)
    if gen_dir is None:
        return [], label
    files = sorted(gen_dir.glob("*.dfy"))
    return files, label


def classify_error(message):
    """Classify an error message into a tier (1, 2, or 3)."""
    if TIER_1_RE.search(message):
        return 1
    if TIER_2_RE.search(message):
        return 2
    # Default: unrecognized errors start as Tier 2 (conservative)
    return 2


def parse_dafny_output(output, dfy_path):
    """Parse dafny verify output into structured errors.

    Returns list of dicts: {line, column, code, message, tier, raw}
    """
    errors = []
    filename = dfy_path.name

    # Dafny error format: file(line,col): Error: message
    # Also: file(line,col): Error CODE: message
    error_re = re.compile(
        r"^(.+?)\((\d+),(\d+)\):\s*(Error|Warning)(?:\s+(\w+))?:\s*(.+)$",
        re.MULTILINE,
    )

    for m in error_re.finditer(output):
        filepath, line, col, severity, code, message = m.groups()
        if severity == "Warning":
            continue  # --allow-warnings skips these

        tier = classify_error(message)
        errors.append({
            "line": int(line),
            "column": int(col),
            "code": code or "",
            "message": message.strip(),
            "tier": tier,
            "raw": m.group(0),
        })

    # Check for timeout in overall output
    if re.search(r"timed? ?out|out of resource", output, re.IGNORECASE):
        if not any(e for e in errors if "time" in e["message"].lower()):
            errors.append({
                "line": 0,
                "column": 0,
                "code": "TIMEOUT",
                "message": "Verification timed out",
                "tier": 2,
                "raw": "verification timeout",
            })

    return errors


def max_tier(errors):
    """Return the highest tier among errors, or 0 if none."""
    if not errors:
        return 0
    return max(e["tier"] for e in errors)


def next_report_number(asn_label):
    """Find the next verification report number."""
    existing = sorted(VERIFICATION_DIR.glob(f"{asn_label}-verify-*.md"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"-verify-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


def write_report(asn_label, dfy_path, errors, elapsed, report_num):
    """Write a verification report to vault/4-modeling/verification/."""
    VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    report_path = VERIFICATION_DIR / f"{asn_label}-verify-{report_num}.md"

    lines = [
        f"# Verification Report — {asn_label} (#{report_num})",
        f"",
        f"*Source: {dfy_path.name} — Verified: {time.strftime('%Y-%m-%d %H:%M')} — "
        f"Duration: {elapsed:.0f}s*",
        f"",
    ]

    if not errors:
        lines.append("**Result: VERIFIED** — all properties pass.")
    else:
        tier_counts = {1: 0, 2: 0, 3: 0}
        for e in errors:
            tier_counts[e["tier"]] = tier_counts.get(e["tier"], 0) + 1

        highest = max_tier(errors)
        lines.append(f"**Result: FAILED** — {len(errors)} error(s), "
                      f"max tier {highest}")
        lines.append(f"")
        lines.append(f"| Tier | Count |")
        lines.append(f"|------|-------|")
        for t in (1, 2, 3):
            if tier_counts[t]:
                lines.append(f"| {t} | {tier_counts[t]} |")
        lines.append(f"")
        lines.append(f"## Errors")
        lines.append(f"")

        for e in sorted(errors, key=lambda x: (x["tier"], x["line"])):
            tier_label = {1: "Syntax/type", 2: "Proof-structural",
                          3: "Spec error"}[e["tier"]]
            lines.append(f"### Line {e['line']} — Tier {e['tier']} ({tier_label})")
            lines.append(f"")
            lines.append(f"```")
            lines.append(e["raw"])
            lines.append(f"```")
            lines.append(f"")

    report_path.write_text("\n".join(lines) + "\n")
    return report_path


def run_dafny(dfy_path, timeout_seconds=300):
    """Run dafny verify and return (returncode, stdout+stderr, elapsed)."""
    cmd = ["dafny", "verify", "--allow-warnings", str(dfy_path)]

    start = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout_seconds, cwd=str(WORKSPACE),
        )
        elapsed = time.time() - start
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        return result.returncode, output.strip(), elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return -1, f"Verification timed out after {timeout_seconds}s", elapsed
    except FileNotFoundError:
        return -2, "dafny command not found — is Dafny installed?", 0.0


def log_usage(asn_label, elapsed, error_count, highest_tier):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "verify-dafny",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "errors": error_count,
            "max_tier": highest_tier,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Verify a Dafny specification and classify errors by tier")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--timeout", "-t", type=int, default=300,
                        help="Verification timeout in seconds (default: 300)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check paths and exit without running dafny")
    args = parser.parse_args()

    # Find .dfy files in latest modeling directory
    dfy_files, asn_label = find_dafny_files(args.asn)
    if not dfy_files:
        print(f"  No .dfy files found for {args.asn} in "
              f"vault/4-modeling/dafny/{asn_label or '?'}/modeling-*/",
              file=sys.stderr)
        print(f"  Run: python scripts/model.py dafny {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    names = ", ".join(p.name for p in dfy_files)
    print(f"  [VERIFY] {asn_label} — {len(dfy_files)} file(s): {names}",
          file=sys.stderr)

    if args.dry_run:
        for f in dfy_files:
            print(f"  [DRY RUN] Would run: dafny verify --allow-warnings {f}",
                  file=sys.stderr)
        return

    # Run dafny verify on each file, aggregate results
    all_errors = []
    total_elapsed = 0

    for dfy_path in dfy_files:
        returncode, output, elapsed = run_dafny(dfy_path, args.timeout)
        total_elapsed += elapsed

        if returncode == -2:
            print(f"  {output}", file=sys.stderr)
            sys.exit(1)

        errors = parse_dafny_output(output, dfy_path)
        all_errors.extend(errors)

    highest = max_tier(all_errors)

    # Write report (use first file for the report header)
    report_num = next_report_number(asn_label)
    report_path = write_report(asn_label, dfy_files[0], all_errors,
                               total_elapsed, report_num)

    # Log usage
    log_usage(asn_label, total_elapsed, len(all_errors), highest)

    # Print report path to stdout (for pipeline consumption)
    print(str(report_path))

    # Status to stderr
    if not all_errors:
        print(f"  [VERIFIED] {asn_label} — all properties pass "
              f"({total_elapsed:.0f}s)", file=sys.stderr)
    else:
        tier_summary = ", ".join(
            f"T{t}:{sum(1 for e in all_errors if e['tier'] == t)}"
            for t in (1, 2, 3) if any(e["tier"] == t for e in all_errors)
        )
        print(f"  [FAILED] {len(all_errors)} error(s) [{tier_summary}] "
              f"({total_elapsed:.0f}s)", file=sys.stderr)

    print(f"  [WROTE] {report_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Exit code based on tier
    if not all_errors:
        sys.exit(0)
    elif highest == 1:
        sys.exit(2)
    elif highest == 2:
        sys.exit(3)
    else:
        sys.exit(4)


if __name__ == "__main__":
    main()
