#!/usr/bin/env python3
"""
Triage Inline — prioritize lint inline findings into an action plan.

Reads the inline lint report, missing dependencies report, and property
table. Sends to an LLM which deduplicates, applies prioritization
criteria, and outputs a promote/extract/leave action plan.

Run lint inline and lint missing first to build the reports.

Usage:
    python scripts/triage-inline.py 34
    python scripts/triage-inline.py 34 --dry-run
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE,
    blueprint_properties_dir, lint_path,
)
from lib.shared.common import find_asn, step_commit_asn

PROMPT_PATH = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
               / "triage.md")


def main():
    parser = argparse.ArgumentParser(
        description="Triage Inline — prioritize findings into action plan")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show inputs without running LLM")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    blueprint_dir = blueprint_properties_dir(asn_label)

    # Read inline report
    inline_path = lint_path(asn_label, "inline")
    if not inline_path.exists():
        print(f"  No inline lint report. Run: python scripts/lint.py inline {asn_num}",
              file=sys.stderr)
        sys.exit(1)
    inline_report = inline_path.read_text()

    # Read missing report (optional)
    missing_path = lint_path(asn_label, "missing")
    if missing_path.exists():
        missing_report = missing_path.read_text()
    else:
        missing_report = "(no missing dependencies report — run lint.py missing first)"

    # Read table
    table_path = blueprint_dir / "_table.md"
    if table_path.exists():
        table = table_path.read_text()
    else:
        table = "(no table file)"

    print(f"\n  [TRIAGE] {asn_label}", file=sys.stderr)
    print(f"  Inline report: {inline_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    if args.dry_run:
        derived = len(re.findall(r'^\- \*\*derived\*\*', inline_report, re.M))
        defn = len(re.findall(r'^\- \*\*definition\*\*', inline_report, re.M))
        print(f"  {derived} derived, {defn} definition findings to triage",
              file=sys.stderr)
        print(f"  Missing report: {'yes' if missing_path.exists() else 'no'}",
              file=sys.stderr)
        return

    # Build prompt
    template = PROMPT_PATH.read_text()
    prompt = (template
              .replace("{{inline_report}}", inline_report)
              .replace("{{missing_report}}", missing_report)
              .replace("{{table}}", table))

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-6",
        "--tools", "",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    print(f"  Triaging...", file=sys.stderr)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED ({elapsed:.0f}s)", file=sys.stderr)
        sys.exit(1)

    triage_text = result.stdout.strip()

    # Write triage report
    out_path = lint_path(asn_label, "triage")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"# Triage — {asn_label}\n\n"
                        f"*Generated: {time.strftime('%Y-%m-%d %H:%M')}*\n\n"
                        f"{triage_text}\n")

    # Count actions
    promote_count = len(re.findall(r'^- .+→', triage_text, re.M))
    print(f"\n  [TRIAGE] Done ({elapsed:.0f}s)", file=sys.stderr)
    print(f"  Report: {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    step_commit_asn(asn_num, hint="triage-inline")


if __name__ == "__main__":
    main()
