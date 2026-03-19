#!/usr/bin/env python3
"""
Extract test cases from worked examples.

Decomposes worked examples into individual examples, then uses an LLM
to extract concrete Given/Assert test cases from each example.

Usage:
    python scripts/tests.py extract 34
    python scripts/tests.py extract 34 --example 1
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
ASNS_DIR = WORKSPACE / "vault" / "asns"
EXAMPLES_DIR = WORKSPACE / "vault" / "5-examples"
TESTCASES_DIR = WORKSPACE / "vault" / "6-test-cases"

EXTRACT_MODEL = "sonnet"
EXTRACT_PROMPT = PROMPTS / "extract.md"


def find_asn_file(asn_num):
    """Find the ASN markdown file."""
    label = f"ASN-{asn_num:04d}"
    matches = list(ASNS_DIR.glob(f"{label}-*.md"))
    if not matches:
        print(f"[ERROR] No ASN file found for {label}", file=sys.stderr)
        sys.exit(1)
    return matches[0]


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


def extract_test_cases(asn_file, example_num, example_name, example_text,
                       label):
    """Extract test cases from a single example."""
    print(f"  [EXTRACT] Example {example_num}: {example_name}")

    template = EXTRACT_PROMPT.read_text()
    asn_text = asn_file.read_text()

    prompt = f"""{template}

---

## ASN

{asn_text}

---

## Example

{example_text}"""

    start = time.time()
    result = call_claude(prompt)
    elapsed = time.time() - start

    if result is None:
        print(f"  [EXTRACT] FAILED ({elapsed:.0f}s)")
        return None

    tc_count = len(re.findall(r"^## TC-\d+", result, re.MULTILINE))
    print(f"  [EXTRACT] Done — {tc_count} test cases ({elapsed:.0f}s)")
    return result


def cmd_extract(args):
    """Extract test cases from worked examples."""
    asn_file = find_asn_file(args.asn)
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

    print(f"\n{'='*60}")
    print(f"Test Case Extraction: {label}")
    print(f"ASN: {asn_file.name}")
    print(f"Examples: {examples_file.name}")
    print(f"Examples to extract: {len(examples)}")
    print(f"{'='*60}")

    total_start = time.time()
    total_tcs = 0

    for example_num, example_name, example_text in examples:
        result = extract_test_cases(
            asn_file, example_num, example_name, example_text, label
        )

        if result is None:
            print(f"  [SKIP] Example {example_num} failed")
            continue

        out_file = out_dir / f"example-{example_num}.md"
        out_file.write_text(result)

        tc_count = len(re.findall(r"^## TC-\d+", result, re.MULTILINE))
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

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)


if __name__ == "__main__":
    main()
