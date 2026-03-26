#!/usr/bin/env python3
"""
Extract formal properties from an ASN for Dafny translation.

Uses the proof index as a roster to locate each property in the ASN,
then extracts just the formal statement. Produces a compact properties
file suitable as input to the Dafny generation step.

Usage:
    python scripts/model.py statements 4
    python scripts/model.py statements ASN-0001 --dry-run
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
from paths import WORKSPACE, ASNS_DIR, PROOF_INDEX_DIR, USAGE_LOG, formal_stmts, asn_dir

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "extract-properties.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, or full path."""
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def build_prompt(asn_content, proof_index):
    """Assemble extraction prompt from template + injected content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/extract-properties.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{proof_index}}", proof_index
    )


def strip_preamble(text):
    """Strip any preamble before the properties header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


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


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "extract-properties",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Extract formal properties from an ASN for Dafny translation")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()

    # Read proof index (required)
    index_path = PROOF_INDEX_DIR / f"{asn_label}-proof-index.md"
    proof_index = read_file(index_path)
    if not proof_index:
        print(f"  No proof index found at {index_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        print(f"  Run: python scripts/model.py index {args.asn}", file=sys.stderr)
        sys.exit(1)

    # Build prompt
    print(f"  [EXTRACT] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content, proof_index)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model} with --tools ""',
              file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model,
                                  effort=args.effort)

    if not text:
        print("  No properties extracted", file=sys.stderr)
        sys.exit(1)

    # Strip any preamble
    text = strip_preamble(text)

    # Add source metadata after the title
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", asn_content)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}", date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    index_gen = re.search(r"Index generated: (\d{4}-\d{2}-\d{2})", proof_index)
    index_date = index_gen.group(1) if index_gen else "unknown"

    source_line = (f"\n*Source: {asn_path.name} (revised {asn_date}) — "
                   f"Index: {index_date} — "
                   f"Extracted: {time.strftime('%Y-%m-%d')}*\n")
    lines = text.split("\n", 1)
    if len(lines) == 2:
        text = lines[0] + "\n" + source_line + lines[1]
    else:
        text = text + "\n" + source_line

    # Write output
    asn_num = int(re.search(r'\d+', asn_label).group())
    asn_dir(asn_num).mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(text + "\n")

    # Log usage
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(out_path))

    print(f"  [WROTE] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
