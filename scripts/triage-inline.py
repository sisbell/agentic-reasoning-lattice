#!/usr/bin/env python3
"""
Triage Inline — prioritize lint inline findings into an action plan.

Reads the inline lint report, missing dependencies report, and property
table. Sends to an LLM which deduplicates, applies prioritization
criteria, and outputs a promote/extract/leave action plan.

By default, accumulates with any existing triage report (union of findings).
Use --rewrite to start from scratch.

Run lint inline and lint missing first to build the reports.

Usage:
    python scripts/triage-inline.py 34
    python scripts/triage-inline.py 34 --rewrite
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


def _parse_triage_section(text, section):
    """Parse a triage section into a dict of {key: line}.
    Key is SOURCE → TARGET (without the reason)."""
    entries = {}
    in_section = False
    for line in text.split("\n"):
        if line.strip().startswith("## "):
            in_section = line.strip().lstrip("# ").strip().lower() == section.lower()
            continue
        if not in_section:
            continue
        m = re.match(r'^- (.+?\s*→\s*\S+)', line.strip())
        if m:
            key = m.group(1).strip()
            entries[key] = line.strip()
    return entries


def _merge_triage(existing_text, new_text):
    """Merge new triage into existing, keeping the union of findings.
    Returns merged text and count of new entries."""
    new_count = 0
    sections = []
    for section in ("Promote", "Extract", "Leave"):
        existing = _parse_triage_section(existing_text, section)
        new = _parse_triage_section(new_text, section)
        # Add new entries not already present
        for key, line in new.items():
            if key not in existing:
                existing[key] = line
                new_count += 1
        lines = sorted(existing.values())
        sections.append(f"## {section}\n\n" + "\n".join(lines) if lines else f"## {section}\n\n(none)")
    merged = "\n\n".join(sections)
    return merged, new_count


def main():
    parser = argparse.ArgumentParser(
        description="Triage Inline — prioritize findings into action plan")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--rewrite", action="store_true",
                        help="Overwrite existing triage instead of accumulating")
    parser.add_argument("--cycles", type=int, default=1,
                        help="Number of triage cycles to run (default: 3)")
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

    out_path = lint_path(asn_label, "triage")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear existing on --rewrite
    if args.rewrite and out_path.exists():
        out_path.unlink()

    for cycle in range(1, args.cycles + 1):
        print(f"\n  === Cycle {cycle}/{args.cycles} ===", file=sys.stderr)
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

        if not out_path.exists():
            out_path.write_text(f"# Triage — {asn_label}\n\n"
                                f"*Generated: {time.strftime('%Y-%m-%d %H:%M')}*\n\n"
                                f"{triage_text}\n")
            new_count = len(re.findall(r'^- .+→', triage_text, re.M))
            print(f"  [TRIAGE] {new_count} entries ({elapsed:.0f}s)",
                  file=sys.stderr)
        else:
            existing_text = out_path.read_text()
            merged, new_count = _merge_triage(existing_text, triage_text)
            if new_count > 0:
                out_path.write_text(f"# Triage — {asn_label}\n\n"
                                    f"*Generated: {time.strftime('%Y-%m-%d %H:%M')}*\n\n"
                                    f"{merged}\n")
            print(f"  [TRIAGE] {new_count} new entries ({elapsed:.0f}s)",
                  file=sys.stderr)

        print(f"  Report: {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

        if new_count > 0:
            step_commit_asn(asn_num, hint="triage-inline")


if __name__ == "__main__":
    main()
