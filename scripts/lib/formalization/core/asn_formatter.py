"""
Format normalization gate — review/revise cycle + mechanical assembly.

Pipeline:
1. Format review/revise (sonnet) — fix headers, status vocab, add missing entries
2. Formal statements assembly (mechanical) — table + sections → formal-statements.md

Usage (standalone):
    python scripts/lib/normalize_format.py 43
    python scripts/lib/normalize_format.py 43 --review-only
    python scripts/lib/normalize_format.py 43 --assemble-only
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, REVIEWS_DIR
from lib.shared.common import find_asn, extract_property_sections

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "format"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"
REVISE_TEMPLATE = PROMPTS_DIR / "revise.md"

MAX_CYCLES = 30


def _invoke_claude(prompt, model="sonnet", effort="high", tools=False):
    """Call claude --print. If tools=True, allows file read/write."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag]
    if not tools:
        cmd += ["--tools", ""]

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
        print(f"  [FORMAT] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return "", elapsed

    return result.stdout.strip(), elapsed


def _log_usage(step, elapsed, asn_num):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"normalize-{step}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Format review/revise cycle (LLM, sonnet)
# ---------------------------------------------------------------------------

def _format_review_path(asn_label):
    """Path to format review findings file."""
    return REVIEWS_DIR / asn_label / "format-review.md"


def step_format_review(asn_num):
    """Run format review. Returns (is_clean, findings_text).

    Saves findings to vault/2-review/ASN-NNNN/format-review.md.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [FORMAT] ASN-{asn_num:04d} not found", file=sys.stderr)
        return True, ""

    template = REVIEW_TEMPLATE.read_text()
    asn_content = asn_path.read_text()
    prompt = template.replace("{{asn_content}}", asn_content)

    text, elapsed = _invoke_claude(prompt, model="sonnet", effort="high")
    _log_usage("review", elapsed, asn_num)

    if not text:
        return True, ""

    if "RESULT: CLEAN" in text:
        print(f"  [FORMAT] Clean ({elapsed:.0f}s)", file=sys.stderr)
        return True, text

    # Save findings to disk (only when there are issues)
    review_path = _format_review_path(asn_label)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(text)

    # Extract finding count
    m = re.search(r"RESULT:\s*(\d+)\s*FINDING", text)
    count = m.group(1) if m else "?"
    print(f"  [FORMAT] {count} findings ({elapsed:.0f}s)", file=sys.stderr)
    return False, text


def step_format_revise(asn_num, findings):
    """Run format revise with agentic tool access. Returns True on success."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = REVISE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)
    prompt = (template
              .replace("{{asn_path}}", str(rel_path))
              .replace("{{findings}}", findings))

    print(f"  [FORMAT] Revising {asn_label}...", file=sys.stderr)

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start
    _log_usage("revise", elapsed, asn_num)

    if result.returncode != 0:
        print(f"  [FORMAT] Revise FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return False

    print(f"  [FORMAT] Revised ({elapsed:.0f}s)", file=sys.stderr)
    return True


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def normalize_format(asn_num):
    """Run format normalization. Returns True if clean.

    Format review/revise cycle (up to 30 cycles).
    Findings saved to vault/2-review/ASN-NNNN/format-review.md.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return True  # nothing to normalize

    # Clean prior format review
    review_path = _format_review_path(asn_label)
    if review_path.exists():
        review_path.unlink()

    print(f"  [FORMAT] Checking {asn_label}...", file=sys.stderr)

    for cycle in range(1, MAX_CYCLES + 1):
        is_clean, findings = step_format_review(asn_num)
        if is_clean:
            return True

        if cycle == MAX_CYCLES:
            print(f"  [FORMAT] Max cycles ({MAX_CYCLES}) reached, "
                  f"still has findings", file=sys.stderr)
            return False

        print(f"  [FORMAT] Cycle {cycle}/{MAX_CYCLES} — revising...",
              file=sys.stderr)
        ok = step_format_revise(asn_num, findings)
        if not ok:
            print(f"  [FORMAT] Revise failed, stopping", file=sys.stderr)
            return False

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Format normalization — review/revise + mechanical assembly")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--review-only", action="store_true",
                        help="Run review only, don't revise")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.review_only:
        is_clean, findings = step_format_review(asn_num)
        if findings:
            print(findings)
        sys.exit(0 if is_clean else 1)

    ok = normalize_format(asn_num)
    if ok:
        print(f"\n  [FORMAT] ASN-{asn_num:04d} format is clean",
              file=sys.stderr)
    else:
        print(f"\n  [FORMAT] ASN-{asn_num:04d} still has format issues",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
