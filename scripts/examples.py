#!/usr/bin/env python3
"""
Generate worked examples from an ASN with review/revise loop.

Generates an initial set of verification scenarios, then iterates
review (correctness + coverage gaps) and revise cycles until converged.

Usage:
    python scripts/examples.py 34
    python scripts/examples.py 34 --max-cycles 10
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, EXAMPLES_DIR, DOMAIN_PROMPTS, formal_stmts
from lib.shared.common import find_asn

PROMPTS = DOMAIN_PROMPTS / "examples"

GENERATE_MODEL = "claude-sonnet-4-6"
REVIEW_MODELS = ["claude-sonnet-4-6"]
GENERATE_PROMPT = PROMPTS / "derive-examples.md"
REVIEW_PROMPT = PROMPTS / "review.md"


def find_formal_statements(asn_num):
    """Find formal-statements.md for an ASN. Returns path or None."""
    path = formal_stmts(asn_num)
    if path.exists():
        return path
    return None


def call_claude(prompt, model=GENERATE_MODEL):
    """Call Claude with a prompt, return the response text."""
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    cmd = [
        "claude", "--print",
        "--model", model,
        "--tools", "",
    ]

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )

    if result.returncode != 0:
        print(f"[ERROR] Claude call failed (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        return None

    return result.stdout.strip()


def generate(asn_file, examples_file, review_file=None):
    """Generate or revise worked examples.

    Without review_file: initial generation from the ASN.
    With review_file: revision — injects review findings and current examples.
    """
    if review_file:
        print(f"  [REVISE] Addressing review findings...")
    else:
        print(f"  [GENERATE] Creating worked examples...")

    template = GENERATE_PROMPT.read_text()
    asn_text = asn_file.read_text()

    parts = [template]

    if review_file:
        examples_text = examples_file.read_text()
        review_text = review_file.read_text()

        parts.append(f"""## Your Assignment: REVISE

Address every correctness issue and coverage gap identified in the review.
Do not rewrite from scratch. Make targeted fixes and additions.
You may also pick up items from the Backlog if they are straightforward
to address alongside the review's findings.

Update the Coverage table and Backlog to reflect your changes.

## Current Worked Examples

{examples_text}

## Review

{review_text}""")

    parts.append(f"## Formal Statements\n\n{asn_text}")

    prompt = "\n\n---\n\n".join(parts)

    start = time.time()
    result = call_claude(prompt)
    elapsed = time.time() - start

    if result is None:
        label = "REVISE" if review_file else "GENERATE"
        print(f"  [{label}] FAILED ({elapsed:.0f}s)")
        return False

    examples_file.write_text(result)
    label = "REVISE" if review_file else "GENERATE"
    print(f"  [{label}] Done ({elapsed:.0f}s, {len(result)} chars)")
    return True


def review(asn_file, examples_file, review_file, cycle=1):
    """Review worked examples, return verdict."""
    model = REVIEW_MODELS[(cycle - 1) % len(REVIEW_MODELS)]
    model_name = model.split("-")[1]  # "opus" or "sonnet"
    print(f"  [REVIEW/{model_name}] Checking worked examples...")

    template = REVIEW_PROMPT.read_text()
    asn_text = asn_file.read_text()
    examples_text = examples_file.read_text()

    prompt = f"""{template}

---

## Formal Statements

{asn_text}

---

## Worked Examples to Review

{examples_text}"""

    start = time.time()
    result = call_claude(prompt, model=model)
    elapsed = time.time() - start

    if result is None:
        print(f"  [REVIEW/{model_name}] FAILED ({elapsed:.0f}s)")
        return None

    review_file.write_text(result)

    if "VERDICT: CONVERGED" in result:
        print(f"  [REVIEW/{model_name}] CONVERGED ({elapsed:.0f}s)")
        return "CONVERGED"
    elif "VERDICT: REVISE" in result:
        issue_count = result.count("### Issue") + result.count("### Gap")
        print(f"  [REVIEW/{model_name}] REVISE — {issue_count} findings ({elapsed:.0f}s)")
        return "REVISE"
    else:
        print(f"  [REVIEW/{model_name}] Unknown verdict ({elapsed:.0f}s)")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate worked examples from an ASN"
    )
    parser.add_argument("asn", type=int, help="ASN number (e.g., 34)")
    parser.add_argument("--max-cycles", type=int, default=15,
                        help="Max review/revise cycles (default: 15)")
    args = parser.parse_args()

    asn_file, _ = find_asn(args.asn)
    if asn_file is None:
        print(f"[ERROR] No ASN file found for ASN-{args.asn:04d}", file=sys.stderr)
        sys.exit(1)
    stmts_path = find_formal_statements(args.asn)
    spec_file = stmts_path if stmts_path else asn_file
    if stmts_path:
        print(f"  [SPEC] Using formal-statements.md", file=sys.stderr)
    else:
        print(f"  [SPEC] No formal-statements.md — using raw ASN", file=sys.stderr)
    label = f"ASN-{args.asn:04d}"

    example_dir = EXAMPLES_DIR / label
    example_dir.mkdir(parents=True, exist_ok=True)
    examples_file = example_dir / "examples-1.md"
    review_dir = example_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    # Count existing reviews to know where we are
    existing_reviews = sorted(review_dir.glob("review-*.md"))
    cycle_start = len(existing_reviews) + 1

    print(f"\n{'='*60}")
    print(f"Worked Examples: {label}")
    print(f"ASN: {asn_file.name}")
    print(f"Max cycles: {args.max_cycles}")
    if existing_reviews:
        print(f"Resuming from cycle {cycle_start} ({len(existing_reviews)} prior reviews)")
    print(f"{'='*60}")

    # Step 1: Generate if no examples exist
    if not examples_file.exists():
        success = generate(spec_file, examples_file)
        if not success:
            print("[FAILED] Generation failed")
            sys.exit(1)

    # Step 2: Review/revise loop
    total_start = time.time()

    for cycle in range(cycle_start, cycle_start + args.max_cycles):
        print(f"\n  ── Cycle {cycle}/{cycle_start + args.max_cycles - 1} ──")

        review_path = review_dir / f"review-{cycle}.md"
        verdict = review(spec_file, examples_file, review_path, cycle=cycle)

        if verdict == "CONVERGED":
            total_elapsed = time.time() - total_start
            print(f"\n{'='*60}")
            print(f"CONVERGED after {cycle - cycle_start + 1} cycle(s) ({total_elapsed:.0f}s)")
            print(f"Output: {examples_file}")
            print(f"{'='*60}")
            return

        if verdict == "REVISE":
            success = generate(spec_file, examples_file, review_file=review_path)
            if not success:
                print("[FAILED] Revision failed")
                sys.exit(1)
        else:
            print("[FAILED] Review returned unknown verdict")
            sys.exit(1)

    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"MAX CYCLES REACHED ({args.max_cycles}) ({total_elapsed:.0f}s)")
    print(f"Output: {examples_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
