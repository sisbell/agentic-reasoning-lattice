#!/usr/bin/env python3
"""
Review an ASN for rigor — Dijkstra-style proof checking.

Loads the ASN content and shared vocabulary, injects them into a review
prompt template, and invokes claude --print with --tools "" (review is
pure analysis, no file access needed).

Results written to vault/discovery/reviews/ for traceability.

Usage:
    python scripts/review-asn.py 4
    python scripts/review-asn.py 9 --model sonnet
    python scripts/review-asn.py 9 --effort high
    python scripts/review-asn.py 4 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

from paths import WORKSPACE, ASNS_DIR, VOCABULARY, REVIEWS_DIR, USAGE_LOG, sorted_reviews

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, or full path."""
    # If it's an existing file path, use it directly
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    # Normalize to 4-digit number
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


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


def strip_preamble(text):
    """Strip any tool-use preamble before the review header."""
    marker = re.search(r"^# Review of ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


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
            "skill": "review",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Review an ASN for rigor")
    parser.add_argument("asn", help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/modeling/asns/", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/modeling/vocabulary.md not found", file=sys.stderr)

    # Build prompt
    print(f"  [REVIEW] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content, vocabulary)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model} with --tools """,
              file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model,
                                  effort=args.effort)

    if not text:
        print("  No review produced", file=sys.stderr)
        sys.exit(1)

    # Strip any preamble before review header
    text = strip_preamble(text)

    # Write output (sequential numbering: review-1, review-2, ...)
    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    existing = sorted_reviews(asn_label)
    next_num = 1
    for f in existing:
        m = re.search(r"review-(\d+)\.md$", f.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    output_path = REVIEWS_DIR / asn_label / f"review-{next_num}.md"
    output_path.write_text(text + "\n")

    # Parse verdict
    verdict_match = re.search(r"^VERDICT:\s*(\w+)", text, re.MULTILINE)
    verdict = verdict_match.group(1).upper() if verdict_match else "REVISE"
    print(f"  [VERDICT] {verdict}", file=sys.stderr)

    # Log usage
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(output_path))

    print(f"  [WROTE] {output_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Exit 2 if converged (distinct from error=1)
    if verdict == "CONVERGED":
        sys.exit(2)


if __name__ == "__main__":
    main()
