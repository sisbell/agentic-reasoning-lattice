#!/usr/bin/env python3
"""
Review an ASN for rigor — Dijkstra-style proof checking.

Loads the ASN content and shared vocabulary, injects them into a review
prompt template, and invokes claude --print with --tools "" (review is
pure analysis, no file access needed).

Results written to vault/2-review/ for traceability.

Usage:
    python scripts/lib/review_check.py 4
    python scripts/lib/review_check.py 9 --model sonnet
    python scripts/lib/review_check.py 9 --effort high
    python scripts/lib/review_check.py 4 --dry-run
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
from paths import WORKSPACE, ASNS_DIR, VOCABULARY, REVIEWS_DIR, USAGE_LOG, STATEMENTS_DIR, FOUNDATION_LIST, INQUIRIES_FILE, sorted_reviews
from lib.foundation import load_foundation_statements

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"


def load_out_of_scope(asn_number):
    """Look up out_of_scope for an ASN from inquiries.yaml. Returns string or empty."""
    try:
        import yaml
        with open(INQUIRIES_FILE) as f:
            data = yaml.safe_load(f)
        for inq in data.get("inquiries", []):
            if inq["id"] == asn_number:
                return inq.get("out_of_scope", "")
    except (FileNotFoundError, KeyError):
        pass
    return ""


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


def build_prompt(asn_content, vocabulary, out_of_scope=""):
    """Assemble review prompt from template + injected content."""
    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print("  Review prompt template not found at scripts/prompts/review.md",
              file=sys.stderr)
        sys.exit(1)

    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR)

    scope_note = (f"\n\n## Scope\n\nThe following topics are OUT OF SCOPE for this ASN. "
                  f"Do not flag missing coverage for them. If the ASN defines properties "
                  f"for these topics, flag them as OUT_OF_SCOPE: {out_of_scope}"
                  if out_of_scope else "")

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{foundation_statements}}", foundation
    ) + scope_note


def strip_preamble(text):
    """Strip any tool-use preamble before the review header."""
    marker = re.search(r"^# Review of ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def validate_review(text):
    """Check that review text has required structure. Returns error message or None."""
    if not re.search(r"^# Review of ASN-\d+", text, re.MULTILINE):
        return "missing '# Review of ASN-NNNN' header"
    if not re.search(r"^VERDICT:\s*\w+", text, re.MULTILINE):
        return "missing VERDICT line"
    if not (re.search(r"^## REVISE", text, re.MULTILINE) or
            re.search(r"^## OUT_OF_SCOPE", text, re.MULTILINE)):
        return "missing ## REVISE or ## OUT_OF_SCOPE section"
    return None


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
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")

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
            for line in result.stderr.strip().split("\n"):
                print(f"    stderr: {line}", file=sys.stderr)
        if result.stdout:
            stdout_len = len(result.stdout)
            print(f"    stdout: {stdout_len} chars partial output",
                  file=sys.stderr)
            # Show last 500 chars to see where it stopped
            tail = result.stdout[-500:]
            print(f"    stdout tail: ...{tail}", file=sys.stderr)
        else:
            print(f"    stdout: empty", file=sys.stderr)
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
        print(f"  No ASN found for {args.asn} in vault/asns/", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/vocabulary.md not found", file=sys.stderr)

    # Build prompt
    print(f"  [REVIEW] {asn_label}", file=sys.stderr)
    asn_number = int(asn_label.replace("ASN-", ""))
    out_of_scope = load_out_of_scope(asn_number)
    if out_of_scope:
        print(f"  [SCOPE] Out of scope: {out_of_scope}", file=sys.stderr)
    prompt = build_prompt(asn_content, vocabulary, out_of_scope=out_of_scope)
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

    # Validate review structure before writing
    error = validate_review(text)
    if error:
        print(f"  MALFORMED REVIEW: {error}", file=sys.stderr)
        print(f"  Response length: {len(text)} chars, {len(text.splitlines())} lines",
              file=sys.stderr)
        sys.exit(1)

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
