"""
Dependency Review — validate dependency references with convergence.

Runs dependency-report (structural drift, registry misclassification)
and fixes findings. Designed to run between contract-review and
cross-review.

Usage:
    python scripts/dependency-review.py 40
    python scripts/dependency-review.py 40 --max-cycles 1     # single pass, no fixing
    python scripts/dependency-review.py 40 --dry-run           # review only
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
from lib.shared.paths import (WORKSPACE, FORMALIZATION_DIR, USAGE_LOG,
                    next_review_number, load_manifest)
from lib.shared.common import find_asn, read_file, assemble_readonly, step_commit_asn
from lib.shared.foundation import load_foundation_statements

DEP_REPORT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "shared" / "dependency-report.md"
REVISE_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "rebase" / "revise.md"


def run_dependency_report(asn_num):
    """Run dependency-report LLM check. Returns report text, or None if clean."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return None

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    if not depends:
        return None

    foundation = load_foundation_statements(asn_num)
    if not foundation:
        return None

    template = read_file(DEP_REPORT_TEMPLATE)
    if not template:
        print(f"  [ERROR] dependency-report.md not found", file=sys.stderr)
        return None

    # Use assembled per-property files if available, otherwise monolithic ASN
    asn_content = assemble_readonly(asn_label)
    if not asn_content:
        asn_content = asn_path.read_text()

    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_content)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    print(f"  [DEP-REPORT] Running...", end="", file=sys.stderr, flush=True)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" failed ({elapsed:.0f}s)", file=sys.stderr)
        return None

    text = result.stdout.strip()

    if "RESULT: CLEAN" in text:
        print(f" clean ({elapsed:.0f}s)", file=sys.stderr)
        return None

    # Extract finding count from RESULT line
    m = re.search(r'RESULT:\s*(\d+)\s*FINDING', text)
    count = int(m.group(1)) if m else "?"
    print(f" {count} findings ({elapsed:.0f}s)", file=sys.stderr)
    return text


def revise_report(asn_num, report_text):
    """Apply fixes for all findings in a dependency report. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    # Point agent at formalization directory if available
    prop_dir = FORMALIZATION_DIR / asn_label
    if prop_dir.exists():
        rel_path = prop_dir.relative_to(WORKSPACE)
    else:
        rel_path = asn_path.relative_to(WORKSPACE)

    template = read_file(REVISE_TEMPLATE)

    prompt = (template
        .replace("{{asn_path}}", str(rel_path))
        .replace("{{report}}", report_text))

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

    print(f"    [REVISE]...", end="", file=sys.stderr, flush=True)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" failed ({elapsed:.0f}s)", file=sys.stderr)
        return False

    cost = 0
    try:
        data = json.loads(result.stdout)
        cost = data.get("total_cost_usd", 0)
    except (json.JSONDecodeError, KeyError):
        pass

    print(f" done ({elapsed:.0f}s, ${cost:.2f})", file=sys.stderr)
    return True


def run_dependency_review(asn_num, max_cycles=10, dry_run=False):
    """Run dependency review with convergence loop.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    if not depends:
        print(f"  {asn_label} has no dependencies — nothing to check",
              file=sys.stderr)
        return "converged"

    review_dir = FORMALIZATION_DIR / asn_label / "reviews"

    print(f"\n  [DEPENDENCY-REVIEW] {asn_label}", file=sys.stderr)

    start_time = time.time()
    converged = False
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Run dependency report
        report = run_dependency_report(asn_num)

        if report is None:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        # New review file per cycle
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Dependency Check — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            rf.write(report + "\n")

        if dry_run or max_cycles == 1:
            print(f"\n  Findings reported.", file=sys.stderr)
            break

        # Revise all findings in one pass
        ok = revise_report(asn_num, report)

        if not ok:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        # Commit
        step_commit_asn(asn_num,
                        f"dependency-review(asn): {asn_label} — cycle {cycle}")

    # Append final result to last review file
    elapsed = time.time() - start_time
    if had_findings:
        with open(review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Converged after {cycle} cycle{'s' if cycle > 1 else ''}.\n")
            else:
                rf.write(f"Not converged after {cycle} cycles.\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(f"\n  Review: {review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if had_findings and not dry_run and not converged:
        step_commit_asn(asn_num,
                        f"dependency-review(asn): {asn_label} — not converged")

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Dependency Review — validate dependency references")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=10,
                        help="Maximum convergence cycles (default: 3)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_dependency_review(asn_num, max_cycles=args.max_cycles,
                                   dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
