#!/usr/bin/env python3
"""
Align an ASN's notation to match canonical vocabulary.

Loads the vocabulary and alignment prompt template, then runs claude -p
with tools so the agent can read the ASN, apply notation changes, and
write the result back. Idempotent — re-running on an aligned ASN is a no-op.

Usage:
    python scripts/align-vocab.py 4               # align ASN-0004
    python scripts/align-vocab.py 3 -m sonnet     # faster
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
ALIGN_TEMPLATE = PROMPTS_DIR / "align-vocab.md"
ASNS_DIR = WORKSPACE / "vault" / "asns"
VOCAB_PATH = WORKSPACE / "vault" / "vocabulary.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 4, 04, 0004, ASN-0004, or full path."""
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


def build_prompt(asn_path, asn_label, vocabulary):
    """Assemble alignment prompt from template + injected content."""
    template = read_file(ALIGN_TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/align-vocab.md",
              file=sys.stderr)
        sys.exit(1)

    rel_path = asn_path.relative_to(WORKSPACE)

    return template.replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{asn_label}}", asn_label
    ).replace(
        "{{asn_path}}", str(rel_path)
    )


def invoke_claude(prompt, model="opus", effort="max"):
    """Run claude -p with tools. Returns parsed JSON output."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", "30",
        "--allowedTools", "Bash,Write,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        num_turns = data.get("num_turns", 0)

        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} turns:{num_turns} ${cost:.4f}",
              file=sys.stderr)

        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Align ASN notation to canonical vocabulary")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    # Require vocabulary
    if not VOCAB_PATH.exists():
        print("  ERROR: vault/vocabulary.md not found", file=sys.stderr)
        print("  Run extract-vocab.py first to create the vocabulary.",
              file=sys.stderr)
        sys.exit(1)

    vocabulary = VOCAB_PATH.read_text()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/asns/", file=sys.stderr)
        sys.exit(1)

    # Build prompt
    print(f"  [ALIGN] {asn_label} ({asn_path.name})", file=sys.stderr)
    prompt = build_prompt(asn_path, asn_label, vocabulary)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)

    # Run
    data, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if data is None:
        print("  Alignment failed", file=sys.stderr)
        sys.exit(1)

    print(f"  [OK] {asn_path.name}", file=sys.stderr)
    print(str(asn_path))


if __name__ == "__main__":
    main()
