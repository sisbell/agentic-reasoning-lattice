#!/usr/bin/env python3
"""
LLM-assisted Dafny fix — reads errors + .dfy + context, produces patched .dfy.

Takes a verification report (from verify-dafny.py), loads the .dfy file and
relevant context, then invokes Claude to produce a corrected module.

For Tier 1 (syntax/type) errors: only the .dfy file and errors are needed.
For Tier 2 (proof-structural) errors: the extract and vocabulary provide
additional context about intended property semantics.

Usage:
    python scripts/fix-dafny.py 1
    python scripts/fix-dafny.py ASN-0001 --with-extract
    python scripts/fix-dafny.py ASN-0001 --report vault/3-modeling/verification/ASN-0001-verify-3.md
    python scripts/fix-dafny.py ASN-0001 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

from paths import (WORKSPACE, DAFNY_DIR, EXTRACTS_DIR, VERIFICATION_DIR,
                   VOCABULARY, USAGE_LOG)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "fix-dafny.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_dafny_file(asn_id):
    """Find .dfy file by ASN number."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    dfy_path = DAFNY_DIR / f"{label}.dfy"
    if dfy_path.exists():
        return dfy_path, label
    return None, label


def find_latest_report(asn_label):
    """Find the most recent verification report for an ASN."""
    if not VERIFICATION_DIR.exists():
        return None
    reports = sorted(VERIFICATION_DIR.glob(f"{asn_label}-verify-*.md"))
    if not reports:
        return None
    # Sort by numeric suffix
    def sort_key(p):
        m = re.search(r"-verify-(\d+)\.md$", p.name)
        return int(m.group(1)) if m else 0
    return sorted(reports, key=sort_key)[-1]


def extract_errors_from_report(report_path):
    """Extract error blocks from a verification report."""
    content = read_file(report_path)
    if not content:
        return ""

    # Extract everything under ## Errors
    errors_match = re.search(r"^## Errors\n(.+)", content,
                             re.MULTILINE | re.DOTALL)
    if errors_match:
        return errors_match.group(1).strip()

    # Fallback: extract code blocks
    blocks = re.findall(r"```\n(.+?)\n```", content, re.DOTALL)
    return "\n\n".join(blocks)


def build_prompt(dafny_code, errors, extract="", asn_context=""):
    """Assemble fix prompt from template + injected content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/formalization/fix-dafny.md",
              file=sys.stderr)
        sys.exit(1)

    # Handle conditional sections ({{#if extract}} ... {{/if}})
    if extract:
        template = re.sub(r"\{\{#if extract\}\}", "", template)
        template = re.sub(r"\{\{/if\}\}", "", template, count=1)
    else:
        template = re.sub(
            r"\{\{#if extract\}\}.*?\{\{/if\}\}", "", template,
            flags=re.DOTALL, count=1)

    if asn_context:
        template = re.sub(r"\{\{#if asn_context\}\}", "", template)
        template = re.sub(r"\{\{/if\}\}", "", template, count=1)
    else:
        template = re.sub(
            r"\{\{#if asn_context\}\}.*?\{\{/if\}\}", "", template,
            flags=re.DOTALL, count=1)

    return template.replace(
        "{{dafny_code}}", dafny_code
    ).replace(
        "{{errors}}", errors
    ).replace(
        "{{extract}}", extract
    ).replace(
        "{{asn_context}}", asn_context
    )


def extract_module(text):
    """Extract the Dafny module from the response, stripping fences and commentary."""
    # Strip ```dafny fences if present
    text = re.sub(r"^```dafny\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n```\s*$", "", text.rstrip())

    # Find module start
    module = re.search(r"^module ", text, re.MULTILINE)
    if module:
        text = text[module.start():]

    return text.rstrip()


def invoke_claude(prompt, model="sonnet", effort="high"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return "", elapsed

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed


def log_usage(asn_label, elapsed, tier):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "fix-dafny",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "tier": tier,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="LLM-assisted Dafny fix from verification errors")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--report", "-r",
                        help="Path to verification report (default: latest)")
    parser.add_argument("--with-extract", action="store_true",
                        help="Include extract context (for Tier 2 proof fixes)")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find .dfy file
    dfy_path, asn_label = find_dafny_file(args.asn)
    if dfy_path is None:
        print(f"  No .dfy file found for {args.asn} in vault/proofs/",
              file=sys.stderr)
        sys.exit(1)

    dafny_code = dfy_path.read_text()

    # Find verification report
    if args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            print(f"  Report not found: {args.report}", file=sys.stderr)
            sys.exit(1)
    else:
        report_path = find_latest_report(asn_label)
        if report_path is None:
            print(f"  No verification report found for {asn_label}",
                  file=sys.stderr)
            print(f"  Run: python scripts/verify-dafny.py {args.asn}",
                  file=sys.stderr)
            sys.exit(1)

    errors = extract_errors_from_report(report_path)
    if not errors:
        print(f"  No errors found in {report_path.name}", file=sys.stderr)
        sys.exit(0)

    # Determine tier context
    tier_label = "Tier 1"
    extract = ""
    asn_context = ""

    if args.with_extract:
        tier_label = "Tier 2"
        extract_path = EXTRACTS_DIR / f"{asn_label}-extract.md"
        extract = read_file(extract_path)
        if not extract:
            print(f"  Warning: no extract found at {extract_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)

    # Build prompt
    print(f"  [FIX] {asn_label} — {tier_label} from {report_path.name}",
          file=sys.stderr)
    prompt = build_prompt(dafny_code, errors, extract, asn_context)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model} with --tools ""',
              file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if not text:
        print("  No fix produced", file=sys.stderr)
        sys.exit(1)

    # Strip preamble/fences
    text = extract_module(text)

    if not text:
        print("  Empty module after extraction", file=sys.stderr)
        sys.exit(1)

    # Write patched file back
    dfy_path.write_text(text + "\n")

    # Log usage
    tier_num = 2 if args.with_extract else 1
    log_usage(asn_label, elapsed, tier_num)

    # Print output file path to stdout (for pipeline consumption)
    print(str(dfy_path))

    print(f"  [WROTE] {dfy_path.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
