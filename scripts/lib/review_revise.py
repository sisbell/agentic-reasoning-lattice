#!/usr/bin/env python3
"""
Revise an ASN based on review feedback.

Loads the discovery prompt (methodology, notation, rigor standards),
injects vocabulary, appends the review content, and runs claude -p
with tools so the agent can read the ASN, make targeted fixes, and
consult Nelson/Gregory if needed.

Usage:
    python scripts/lib/review_revise.py 9              # ASN-0009 + latest review
    python scripts/lib/review_revise.py 9 review-1     # ASN-0009 + specific review
    python scripts/lib/review_revise.py 9 -m sonnet    # use sonnet instead of opus
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
from paths import WORKSPACE, VOCABULARY, ASNS_DIR, REVIEWS_DIR, USAGE_LOG, STATEMENTS_DIR, sorted_reviews

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
DISCOVERY_PROMPT = PROMPTS_DIR / "discovery.md"

MODEL = "claude-opus-4-6"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, etc."""
    # Normalize to 4-digit number
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def find_review(asn_label, review_spec=None):
    """Find review file. If review_spec is None, use latest."""
    if review_spec is None:
        # Latest review
        reviews = sorted_reviews(asn_label)
        return reviews[-1] if reviews else None

    # Try as-is first (full path)
    path = Path(review_spec)
    if path.exists():
        return path

    # Try in nested ASN dir (new layout)
    candidate = REVIEWS_DIR / asn_label / f"{review_spec}.md"
    if candidate.exists():
        return candidate

    # Try in nested ASN dir as-is
    candidate = REVIEWS_DIR / asn_label / review_spec
    if candidate.exists():
        return candidate

    # Try with .md in nested dir
    candidate = REVIEWS_DIR / asn_label / f"{review_spec}.md"
    if candidate.exists():
        return candidate

    return None


def build_prompt(asn_path, review_content, vocab, consultation_content=None):
    """Build revise prompt: discovery methodology + vocab + revise assignment + review."""
    skill_body = read_file(DISCOVERY_PROMPT)
    if not skill_body:
        print("  Discovery prompt not found at scripts/prompts/discovery.md",
              file=sys.stderr)
        sys.exit(1)

    parts = [skill_body]

    if vocab:
        parts.append(f"## Shared Vocabulary\n\n{vocab}")

    # ASN-0001 (Tumbler Arithmetic) is the verified foundation
    foundation = read_file(STATEMENTS_DIR / "ASN-0001-statements.md")
    if foundation:
        parts.append(f"## Foundation: ASN-0001 (Tumbler Arithmetic)\n\n"
                     f"ASN-0001 defines the addressing type system. Use its definitions "
                     f"(tumbler type, `⊕`, `⊖`, `<`, `sub()`, spans) — do not invent "
                     f"custom notation.\n\n{foundation}")

    rel_path = asn_path.relative_to(WORKSPACE)
    asn_label = re.match(r"(ASN-\d+)", asn_path.stem).group(1)

    assignment = f"""## Your Assignment: REVISE {asn_label}

You are revising an existing ASN based on review feedback. Read the ASN at
`{rel_path}`, then read the review below.

Address every REVISE item. OUT_OF_SCOPE items are noted but do not require changes now.

**Do not rewrite the ASN from scratch.** Make targeted fixes to address the
specific issues raised. Preserve the existing structure, notation, and reasoning
where it is not affected by the review.

Write the revised ASN back to `{rel_path}`."""

    if consultation_content:
        assignment += f"""

## Consultation Results

The following expert consultations were conducted based on this review.
Use these answers as evidence when addressing the corresponding REVISE items.

{consultation_content}"""

    assignment += f"""

## Review

{review_content}"""

    parts.append(assignment)

    return "\n\n".join(parts)


def invoke_claude(prompt, model=None, effort="max"):
    """Run claude -p with tools. Returns parsed JSON output."""
    use_model = model or MODEL
    cmd = [
        "claude", "-p",
        "--model", use_model,
        "--output-format", "json",
        "--max-turns", "30",
        "--allowedTools", "Edit,Bash,Write,Read,Glob,Grep",
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


def log_usage(asn_label, elapsed, data):
    """Append a usage entry to the log."""
    if data is None:
        return
    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0)
    inp = (usage.get("input_tokens", 0) +
           usage.get("cache_read_input_tokens", 0) +
           usage.get("cache_creation_input_tokens", 0))
    out = usage.get("output_tokens", 0)

    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "revise",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "input_tokens": inp,
            "output_tokens": out,
            "num_turns": data.get("num_turns", 0),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Revise an ASN based on review feedback")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("review", nargs="?",
                        help="Review identifier (e.g., review-1) — omit for latest")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--consultation",
                        help="Path to consultation results file (from consult_for_revision.py)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/asns/", file=sys.stderr)
        sys.exit(1)

    # Find review
    review_path = find_review(asn_label, args.review)
    if review_path is None:
        if args.review:
            print(f"  Review not found: {args.review} for {asn_label}",
                  file=sys.stderr)
        else:
            print(f"  No reviews found for {asn_label} in vault/2-review/",
                  file=sys.stderr)
        sys.exit(1)

    review_content = review_path.read_text()

    # Check for REVISE items
    if "## REVISE" not in review_content:
        print(f"  No REVISE section in {review_path.name}, nothing to do",
              file=sys.stderr)
        sys.exit(0)

    # Load vocabulary
    vocab = read_file(VOCABULARY)
    if not vocab:
        print("  Warning: vault/vocabulary.md not found", file=sys.stderr)

    # Load consultation results if provided
    consultation_content = None
    if args.consultation:
        consultation_content = read_file(args.consultation)
        if not consultation_content:
            print(f"  Warning: consultation file not found: {args.consultation}",
                  file=sys.stderr)
            consultation_content = None

    # Build prompt
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(args.model, args.model)

    print(f"  [REVISE] {asn_label} ({asn_path.name})", file=sys.stderr)
    print(f"  [REVIEW] {review_path.name}", file=sys.stderr)
    if consultation_content:
        print(f"  [CONSULTATION] {Path(args.consultation).name}", file=sys.stderr)
    prompt = build_prompt(asn_path, review_content, vocab, consultation_content)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)

    # Run
    data, elapsed = invoke_claude(prompt, model=model_flag, effort=args.effort)

    if data is None:
        print("  Revision failed", file=sys.stderr)
        sys.exit(1)

    # Log usage
    log_usage(asn_label, elapsed, data)

    # Verify the ASN was modified
    check = subprocess.run(
        ["git", "diff", "--quiet", str(asn_path)],
        cwd=str(WORKSPACE),
    )
    if check.returncode == 0:
        print(f"  [CONVERGED] {asn_path.name} was not modified — "
              f"review issues already addressed", file=sys.stderr)
        print(str(asn_path))
        sys.exit(2)  # distinct from error (1) — signals convergence
    else:
        print(f"  [OK] {asn_path.name}", file=sys.stderr)
    print(str(asn_path))


if __name__ == "__main__":
    main()
