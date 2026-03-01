#!/usr/bin/env python3
"""
Generate a Dafny specification module from an ASN's extracted properties.

Takes the extract (formal properties + definitions with Dafny metadata)
and vocabulary, then produces a verified Dafny module.

Requires: extract file in vault/extracts/ (run extract-properties.py first)

Usage:
    python scripts/generate-dafny.py 4
    python scripts/generate-dafny.py ASN-0001 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
TEMPLATE = PROMPTS_DIR / "generate-dafny.md"
EXTRACTS_DIR = WORKSPACE / "vault" / "extracts"
DAFNY_DIR = WORKSPACE / "vault" / "dafny"
VOCABULARY = WORKSPACE / "vault" / "vocabulary.md"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_extract(asn_id):
    """Find extract file by ASN number."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    extract_path = EXTRACTS_DIR / f"{label}-extract.md"
    if extract_path.exists():
        return extract_path, label
    return None, label


def build_prompt(extract, vocabulary):
    """Assemble Dafny generation prompt from template + injected content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/generate-dafny.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{extract}}", extract
    ).replace(
        "{{vocabulary}}", vocabulary
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


def invoke_claude(prompt, model="opus", effort="max"):
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
            "skill": "generate-dafny",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dafny specification from ASN extract")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find extract
    extract_path, asn_label = find_extract(args.asn)
    if extract_path is None:
        print(f"  No extract found for {args.asn} in vault/extracts/",
              file=sys.stderr)
        print(f"  Run: python scripts/extract-properties.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    extract = extract_path.read_text()

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/vocabulary.md not found", file=sys.stderr)

    # Build prompt
    print(f"  [DAFNY] {asn_label}", file=sys.stderr)
    prompt = build_prompt(extract, vocabulary)
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
        print("  No Dafny code generated", file=sys.stderr)
        sys.exit(1)

    # Strip preamble/fences
    text = extract_module(text)

    # Write output
    DAFNY_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DAFNY_DIR / f"{asn_label}.dfy"
    out_path.write_text(text + "\n")

    # Log usage
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(out_path))

    print(f"  [WROTE] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
