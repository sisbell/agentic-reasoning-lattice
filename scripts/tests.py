#!/usr/bin/env python3
"""
Test case pipeline for worked examples.

Subcommands:
    extract  — decompose worked examples into Given/Assert test cases
    codegen  — translate test cases to Rust #[test] functions

Usage:
    python scripts/tests.py extract 34
    python scripts/tests.py extract 34 --example 1
    python scripts/tests.py extract 34 --max-cycles 5
    python scripts/tests.py codegen 34
    python scripts/tests.py codegen 34 --case 4
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
EXAMPLES_DIR = WORKSPACE / "vault" / "6-examples"
TESTCASES_DIR = WORKSPACE / "vault" / "7-test-cases"

ORACLE_DIR = WORKSPACE / "vault" / "oracle" / "xanadu-oracle-rust"
TESTS_DIR = ORACLE_DIR / "tests"

EXTRACT_MODEL = "sonnet"
REVIEW_MODEL = "sonnet"
CODEGEN_MODEL = "sonnet"
EXTRACT_PROMPT = PROMPTS / "extract.md"
REVIEW_PROMPT = PROMPTS / "review.md"
CODEGEN_PROMPT = PROMPTS / "codegen.md"



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
            issue_count = review_text.count("### ")
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


def extract_rust_code(response):
    """Extract Rust code from LLM response.

    Returns the raw response if it looks like bare Rust (no markdown fences).
    Otherwise extracts content from ```rust ... ``` fences.
    """
    # If response starts with mod/use/#, treat as bare Rust
    stripped = response.lstrip()
    if stripped.startswith(("mod ", "use ", "#[", "#!", "//", "extern ")):
        return response

    # Try to extract from markdown fences
    blocks = re.findall(r"```rust\s*\n(.*?)```", response, re.DOTALL)
    if blocks:
        return "\n\n".join(blocks)

    # Fallback: return as-is
    return response


def extract_oracle_api(oracle_src):
    """Extract public API signatures from oracle source.

    Pulls out module names and pub fn signatures with their doc comments,
    skipping implementation bodies. Gives the LLM enough to map test case
    operations to oracle calls without the full 1500-line source.
    """
    lines = oracle_src.split("\n")
    api_lines = []
    current_module = None
    in_impl_default = False
    brace_depth = 0

    for line in lines:
        # Track modules (top-level pub mod resets state)
        m = re.match(r"^pub mod (\w+)", line)
        if m:
            current_module = m.group(1)
            in_impl_default = False
            api_lines.append(f"\n// --- {current_module} ---")
            continue

        # Track impl _default blocks (static methods)
        if "impl _default" in line:
            in_impl_default = True
            continue

        # Any other impl block ends _default context
        if re.match(r"\s+impl\b", line) and "_default" not in line:
            in_impl_default = False
            continue

        # Collect pub fn signatures inside impl _default
        if in_impl_default and line.strip().startswith("pub fn "):
            sig = line.rstrip().rstrip("{").rstrip()
            api_lines.append(
                f"  // {current_module}::_default::{sig.strip()}")
            continue

        # Collect pub enum variants for type context
        if line.strip().startswith("pub enum "):
            api_lines.append(f"  {line.strip()}")
            continue

        # Collect field accessors (on data types, not _default)
        if (not in_impl_default
                and line.strip().startswith("pub fn ")
                and "(&self)" in line):
            sig = line.rstrip().rstrip("{").rstrip()
            api_lines.append(f"  {sig.strip()}")
            continue

    return "\n".join(api_lines)


def codegen_case(case_num, case_text, oracle_api, harness_src):
    """Generate Rust test code from a single test case file."""
    template = CODEGEN_PROMPT.read_text()

    prompt = template.replace("{{ORACLE_API}}", oracle_api)
    prompt = prompt.replace("{{HARNESS}}", harness_src)
    prompt = prompt.replace("{{TEST_CASE}}", case_text)

    start = time.time()
    result = call_claude(prompt, model=CODEGEN_MODEL)
    elapsed = time.time() - start

    if result is None:
        return None, elapsed

    rust_code = extract_rust_code(result)
    return rust_code, elapsed


def cmd_codegen(args):
    """Generate Rust #[test] files from test cases."""
    label = f"ASN-{args.asn:04d}"
    tc_dir = TESTCASES_DIR / label

    if not tc_dir.exists():
        print(f"[ERROR] No test cases found: {tc_dir}", file=sys.stderr)
        sys.exit(1)

    # Find case files
    case_files = sorted(tc_dir.glob("case-*.md"))
    if not case_files:
        print(f"[ERROR] No case-*.md files in {tc_dir}", file=sys.stderr)
        sys.exit(1)

    if args.case:
        case_files = [f for f in case_files
                      if f.name == f"case-{args.case}.md"]
        if not case_files:
            print(f"[ERROR] case-{args.case}.md not found", file=sys.stderr)
            sys.exit(1)

    # Ensure tests directory exists
    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load oracle API and harness (once, shared across all cases)
    oracle_src_file = ORACLE_DIR / "src" / "xanadu_oracle.rs"
    harness_file = TESTS_DIR / "harness" / "mod.rs"

    if not oracle_src_file.exists():
        print(f"[ERROR] Oracle source not found: {oracle_src_file}",
              file=sys.stderr)
        sys.exit(1)
    if not harness_file.exists():
        print(f"[ERROR] Harness not found: {harness_file}",
              file=sys.stderr)
        sys.exit(1)

    oracle_api = extract_oracle_api(oracle_src_file.read_text())
    harness_src = harness_file.read_text()

    print(f"\n{'='*60}")
    print(f"Codegen: {label}")
    print(f"Cases to generate: {len(case_files)}")
    print(f"Oracle API: {len(oracle_api.splitlines())} lines")
    print(f"Output: {TESTS_DIR}")
    print(f"{'='*60}")

    total_start = time.time()
    generated = 0

    for case_file in case_files:
        m = re.match(r"case-(\d+)\.md", case_file.name)
        if not m:
            continue
        case_num = int(m.group(1))
        out_file = TESTS_DIR / f"case_{case_num}.rs"

        print(f"\n  ── Case {case_num}: {case_file.name} ──")

        case_text = case_file.read_text()
        tc_count = len(re.findall(r"^## TC-\d+", case_text, re.MULTILINE))

        print(f"  [CODEGEN] {tc_count} test cases → Rust...")
        rust_code, elapsed = codegen_case(case_num, case_text,
                                          oracle_api, harness_src)

        if rust_code is None:
            print(f"  [CODEGEN] FAILED ({elapsed:.0f}s)")
            continue

        out_file.write_text(rust_code)
        fn_count = len(re.findall(r"#\[test\]", rust_code))
        print(f"  [CODEGEN] Done — {fn_count} #[test] functions ({elapsed:.0f}s)")
        generated += 1

    total_elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print(f"Generated {generated}/{len(case_files)} case files ({total_elapsed:.0f}s)")
    print(f"Output: {TESTS_DIR}")
    print(f"{'='*60}")
    print(f"\nNext: cd {ORACLE_DIR} && cargo test")


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
    extract_parser.add_argument("--max-cycles", type=int, default=8,
                                help="Max review/revise cycles per example "
                                     "(default: 8)")

    codegen_parser = subparsers.add_parser(
        "codegen", help="Generate Rust #[test] from test cases"
    )
    codegen_parser.add_argument("asn", type=int,
                                help="ASN number (e.g., 34)")
    codegen_parser.add_argument("--case", type=int, default=None,
                                help="Generate for a specific case only")

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "codegen":
        cmd_codegen(args)


if __name__ == "__main__":
    main()
