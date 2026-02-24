#!/usr/bin/env python3
"""
Review an ASN for rigor — Dijkstra-style proof checking.

Loads the ASN content and shared vocabulary, injects them into a review
prompt template, and invokes claude --print for pure analysis (no tools).

Results written to vault/reviews/ for traceability.
Prints the output file path to stdout.

Usage:
    python scripts/review-asn.py vault/asns/ASN-0004-content-insertion.md
    python scripts/review-asn.py vault/asns/ASN-0004-content-insertion.md --model sonnet
    python scripts/review-asn.py vault/asns/ASN-0004-content-insertion.md --effort high
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"
VOCABULARY = WORKSPACE / "vault" / "vocabulary.md"
REVIEWS_DIR = WORKSPACE / "vault" / "reviews"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def extract_asn_label(asn_path):
    """Extract ASN-NNNN from filename like ASN-0004-content-insertion.md."""
    name = Path(asn_path).stem
    match = re.match(r"(ASN-\d+)", name)
    return match.group(1) if match else name


def build_prompt(asn_content, vocabulary):
    """Assemble review prompt from template + injected content."""
    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print("  Review prompt template not found at scripts/prompts/review.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    )


def invoke_claude(prompt, model="opus", effort="max"):
    """Call claude --print. Returns response text."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--output-format", "json",
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
        return "", elapsed, {}

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)

        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        return text, elapsed, {"input_tokens": inp, "output_tokens": out,
                               "cost_usd": cost}
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return result.stdout, elapsed, {}


def log_usage(elapsed, usage):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "review",
            "elapsed_s": round(elapsed, 1),
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cost_usd": usage.get("cost_usd", 0),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Review an ASN for rigor")
    parser.add_argument("asn", help="Path to the ASN file to review")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus — reviews need maximum rigor)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    # Read ASN
    asn_path = Path(args.asn)
    if not asn_path.exists():
        print(f"  ASN file not found: {asn_path}", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()
    asn_label = extract_asn_label(asn_path)

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/vocabulary.md not found", file=sys.stderr)

    # Build prompt
    print(f"  [REVIEW] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content, vocabulary)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    # Invoke
    text, elapsed, usage = invoke_claude(prompt, model=args.model,
                                         effort=args.effort)

    if not text:
        print("  No review produced", file=sys.stderr)
        sys.exit(1)

    # Write output
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = REVIEWS_DIR / f"{asn_label}-review-{ts}.md"
    output_path.write_text(text)

    # Log usage
    log_usage(elapsed, usage)

    # Print the output file path to stdout
    print(str(output_path))

    print(f"  [LOG] {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
