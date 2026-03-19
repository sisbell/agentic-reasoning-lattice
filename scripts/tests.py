#!/usr/bin/env python3
"""
Extract test cases from worked examples.

Decomposes worked examples into individual examples, then uses an LLM
to extract concrete Given/Assert test cases from each example.
Review/revise loop ensures executability, completeness, and correctness.

Usage:
    python scripts/tests.py extract 34
    python scripts/tests.py extract 34 --example 1
    python scripts/tests.py extract 34 --max-cycles 5
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS = WORKSPACE / "scripts" / "prompts" / "test-cases"
EXAMPLES_DIR = WORKSPACE / "vault" / "5-examples"
TESTCASES_DIR = WORKSPACE / "vault" / "6-test-cases"

EXTRACT_MODEL = "sonnet"
REVIEW_MODEL = "sonnet"
EXTRACT_PROMPT = PROMPTS / "extract.md"
REVIEW_PROMPT = PROMPTS / "review.md"



def split_examples(examples_text):
    """Split worked examples into individual examples.

    Returns list of (example_num, example_name, example_text) tuples.
    Handles both '## Example N:' and legacy '## Scenario N:' headers.
    Excludes Coverage and Backlog sections.
    """
    pattern = r"^## (?:Example|Scenario) (\d+): (.+)$"
    examples = []
    lines = examples_text.split("\n")
    current_num = None
    current_name = None
    current_lines = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            if current_num is not None:
                examples.append(
                    (current_num, current_name, "\n".join(current_lines).strip())
                )
            current_num = int(match.group(1))
            current_name = match.group(2)
            current_lines = [line]
        elif re.match(r"^## (Coverage|Backlog)", line):
            if current_num is not None:
                examples.append(
                    (current_num, current_name, "\n".join(current_lines).strip())
                )
            current_num = None
            current_name = None
            current_lines = []
        elif current_num is not None:
            current_lines.append(line)

    if current_num is not None:
        examples.append(
            (current_num, current_name, "\n".join(current_lines).strip())
        )

    return examples


def call_claude(prompt, model=EXTRACT_MODEL):
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
        print(f"[ERROR] Claude call failed (exit {result.returncode})",
              file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        return None

    return result.stdout.strip()


def extract_test_cases(example_text, review_text=None):
    """Extract or revise test cases from a single example."""
    template = EXTRACT_PROMPT.read_text()

    parts = [template]

    if review_text:
        parts.append(f"""## Your Assignment: REVISE

Address every issue identified in the review. Do not rewrite from scratch —
make targeted fixes, additions, and removals.

## Review

{review_text}""")

    parts.append(f"## Example\n\n{example_text}")

    prompt = "\n\n---\n\n".join(parts)

    start = time.time()
    result = call_claude(prompt)
    elapsed = time.time() - start

    if result is None:
        return None, elapsed

    tc_count = len(re.findall(r"^## TC-\d+", result, re.MULTILINE))
    return result, elapsed


def review_test_cases(example_text, test_cases_text):
    """Review extracted test cases. Returns (review_text, verdict, elapsed)."""
    template = REVIEW_PROMPT.read_text()

    prompt = f"""{template}

---

## Worked Example

{example_text}

---

## Test Cases to Review

{test_cases_text}"""

    start = time.time()
    result = call_claude(prompt, model=REVIEW_MODEL)
    elapsed = time.time() - start

    if result is None:
        return None, None, elapsed

    if "VERDICT: CONVERGED" in result:
        return result, "CONVERGED", elapsed
    elif "VERDICT: REVISE" in result:
        return result, "REVISE", elapsed
    else:
        return result, None, elapsed


def process_example(example_num, example_name, example_text,
                    out_dir, review_dir, max_cycles):
    """Extract and review/revise test cases for one example."""
    print(f"\n  ── Example {example_num}: {example_name} ──")

    tc_file = out_dir / f"case-{example_num}.md"

    # Count existing reviews to know where we are
    existing_reviews = sorted(review_dir.glob(f"case-{example_num}-review-*.md"))
    cycle_start = len(existing_reviews) + 1

    if existing_reviews:
        print(f"  Resuming from cycle {cycle_start} "
              f"({len(existing_reviews)} prior reviews)")

    # Step 1: Extract if no test cases exist
    if not tc_file.exists():
        print(f"  [EXTRACT] Generating test cases...")
        result, elapsed = extract_test_cases(example_text)
        if result is None:
            print(f"  [EXTRACT] FAILED ({elapsed:.0f}s)")
            return 0
        tc_file.write_text(result)
        tc_count = len(re.findall(r"^## TC-\d+", result, re.MULTILINE))
        print(f"  [EXTRACT] Done — {tc_count} test cases ({elapsed:.0f}s)")

    # Step 2: Review/revise loop
    for cycle in range(cycle_start, cycle_start + max_cycles):
        print(f"  [REVIEW] Cycle {cycle}...")

        tc_text = tc_file.read_text()
        review_text, verdict, elapsed = review_test_cases(
            example_text, tc_text
        )

        if review_text is None:
            print(f"  [REVIEW] FAILED ({elapsed:.0f}s)")
            break

        review_path = review_dir / f"case-{example_num}-review-{cycle}.md"
        review_path.write_text(review_text)

        if verdict == "CONVERGED":
            print(f"  [REVIEW] CONVERGED ({elapsed:.0f}s)")
            tc_count = len(re.findall(r"^## TC-\d+", tc_text, re.MULTILINE))
            return tc_count

        if verdict == "REVISE":
            issue_count = (review_text.count("### Issue")
                           + review_text.count("### Gap")
                           + review_text.count("### Error"))
            print(f"  [REVIEW] REVISE — {issue_count} findings ({elapsed:.0f}s)")

            print(f"  [REVISE] Addressing findings...")
            result, elapsed = extract_test_cases(
                example_text, review_text=review_text
            )
            if result is None:
                print(f"  [REVISE] FAILED ({elapsed:.0f}s)")
                break
            tc_file.write_text(result)
            tc_count = len(re.findall(r"^## TC-\d+", result, re.MULTILINE))
            print(f"  [REVISE] Done — {tc_count} test cases ({elapsed:.0f}s)")
        else:
            print(f"  [REVIEW] Unknown verdict ({elapsed:.0f}s)")
            break

    # Max cycles reached
    tc_text = tc_file.read_text()
    tc_count = len(re.findall(r"^## TC-\d+", tc_text, re.MULTILINE))
    print(f"  [MAX CYCLES] {max_cycles} cycles reached")
    return tc_count


def cmd_extract(args):
    """Extract test cases from worked examples."""
    label = f"ASN-{args.asn:04d}"

    examples_file = EXAMPLES_DIR / label / "examples-1.md"
    if not examples_file.exists():
        print(f"[ERROR] No worked examples found: {examples_file}",
              file=sys.stderr)
        sys.exit(1)

    examples_text = examples_file.read_text()
    examples = split_examples(examples_text)

    if not examples:
        print(f"[ERROR] No examples found in {examples_file}",
              file=sys.stderr)
        sys.exit(1)

    if args.example:
        examples = [
            (n, name, text) for n, name, text in examples
            if n == args.example
        ]
        if not examples:
            print(f"[ERROR] Example {args.example} not found",
                  file=sys.stderr)
            sys.exit(1)

    out_dir = TESTCASES_DIR / label
    out_dir.mkdir(parents=True, exist_ok=True)
    review_dir = out_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Test Case Extraction: {label}")
    print(f"Examples to extract: {len(examples)}")
    print(f"Max review cycles: {args.max_cycles}")
    print(f"{'='*60}")

    total_start = time.time()
    total_tcs = 0

    for example_num, example_name, example_text in examples:
        tc_count = process_example(
            example_num, example_name, example_text,
            out_dir, review_dir, args.max_cycles,
        )
        total_tcs += tc_count

    total_elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print(f"Extracted {total_tcs} test cases from {len(examples)} examples "
          f"({total_elapsed:.0f}s)")
    print(f"Output: {out_dir}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Test case pipeline for worked examples"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser(
        "extract", help="Extract test cases from worked examples"
    )
    extract_parser.add_argument("asn", type=int,
                                help="ASN number (e.g., 34)")
    extract_parser.add_argument("--example", type=int, default=None,
                                help="Extract from a specific example only")
    extract_parser.add_argument("--max-cycles", type=int, default=3,
                                help="Max review/revise cycles per example "
                                     "(default: 3)")

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)


if __name__ == "__main__":
    main()
