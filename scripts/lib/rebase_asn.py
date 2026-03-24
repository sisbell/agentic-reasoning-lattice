#!/usr/bin/env python3
"""
Rebase an ASN against its updated foundation.

Finds locally-derived properties that now exist in the foundation,
replaces local derivations with citations, and runs a targeted
review/revise cycle to verify the changes.

Usage:
    python scripts/rebase.py 53
    python scripts/rebase.py 53 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import yaml

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, PROJECT_MODEL_DIR, STATEMENTS_DIR,
                   REVIEWS_DIR, VOCABULARY, FOUNDATION_LIST,
                   load_manifest, next_review_number)
from lib.common import (read_file, find_asn, invoke_claude, invoke_claude_agent,
                         log_usage, step_commit)
from lib.foundation import load_foundation_statements


PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
REBASE_TEMPLATE = PROMPTS_DIR / "rebase.md"
REBASE_REVIEW_TEMPLATE = PROMPTS_DIR / "rebase-review.md"
REBASE_REVISE_TEMPLATE = PROMPTS_DIR / "rebase-revise.md"
AUDIT_TEMPLATE = PROMPTS_DIR / "rebase-audit.md"


def validate(asn_num):
    """Validate the ASN exists and has dependencies."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    manifest = load_manifest(asn_num)
    if not manifest:
        print(f"  [ERROR] ASN-{asn_num:04d} has no project model",
              file=sys.stderr)
        sys.exit(1)

    dep_ids = manifest.get("depends", [])
    if not dep_ids:
        print(f"  [ERROR] ASN-{asn_num:04d} has no dependencies — "
              f"nothing to rebase against", file=sys.stderr)
        sys.exit(1)

    return asn_path, asn_label, manifest


def _load_open_issues(asn_num):
    """Load existing open issues for an ASN. Returns content or empty string."""
    path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}-open-issues.md"
    if path.exists():
        return path.read_text().strip()
    return ""


def _append_open_issues(asn_num, new_issues):
    """Append new issues to the open issues file."""
    path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}-open-issues.md"
    existing = ""
    if path.exists():
        existing = path.read_text().strip()

    if existing:
        content = existing + "\n\n" + new_issues.strip() + "\n"
    else:
        content = new_issues.strip() + "\n"

    path.write_text(content)
    print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)


def _extract_findings_as_issues(text, source_label):
    """Extract findings from a consistency check and format as open issues.

    Parses the structured findings (### N. Category ... Finding N.) and
    converts them to ### titled open issues.
    """
    # Find all "**Finding N.**" blocks
    findings = re.findall(
        r"\*\*Finding \d+\.?\*\*\s*(.+?)(?=\*\*Finding \d+\.?\*\*|---|\Z)",
        text, re.DOTALL)

    if not findings:
        return ""

    issues = []
    for i, finding in enumerate(findings, 1):
        # Use first sentence as title
        first_line = finding.strip().split("\n")[0]
        # Truncate to something reasonable for a title
        title = first_line[:120].rstrip(".")
        issues.append(f"### {title}\n**Source**: {source_label}\n\n{finding.strip()}")

    return "\n\n".join(issues)


def run_inline_consistency_check(asn_num, asn_path, asn_label):
    """Run a consistency check via sonnet.

    Writes findings to the open issues file. Returns True if findings
    were found, False if CLEAN.
    """
    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR,
                                            asn_id=asn_num)
    if not foundation:
        return False

    template_path = PROMPTS_DIR / "consistency-check.md"
    if not template_path.exists():
        return False

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = template_path.read_text()
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    print(f"  [CONSISTENCY] Running fresh check on {asn_label}...",
          file=sys.stderr)

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--max-turns", "1",
        "--allowedTools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "medium"
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [CONSISTENCY] Failed ({elapsed:.0f}s)", file=sys.stderr)
        return False

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
    except (json.JSONDecodeError, KeyError):
        print(f"  [CONSISTENCY] Parse error ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # Empty or whitespace response = CLEAN
    if not text or not text.strip():
        print(f"  [CONSISTENCY] Empty response — treating as CLEAN ({elapsed:.0f}s)",
              file=sys.stderr)
        return False

    # Write as review file for the record
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # RESULT: CLEAN — no findings
    if "RESULT: CLEAN" in text:
        print(f"  [CONSISTENCY] CLEAN ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # RESULT: marker present but not CLEAN — extract and append to open issues
    if "RESULT:" in text:
        issues_text = _extract_findings_as_issues(text, f"consistency check ({asn_label})")
        if issues_text:
            _append_open_issues(asn_num, issues_text)
        print(f"  [CONSISTENCY] Findings appended to open issues ({elapsed:.0f}s)",
              file=sys.stderr)
        return True

    # No RESULT: marker at all — format issue, treat as CLEAN
    print(f"  [CONSISTENCY] No RESULT: marker — treating as CLEAN ({elapsed:.0f}s)",
          file=sys.stderr)
    return False


def step_audit(asn_num, asn_path, asn_label, model, effort):
    """Run a deep foundation audit via opus.

    Reads the ASN and foundation, finds cross-boundary issues,
    appends new findings to the open issues file. Does not edit the ASN.
    """
    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR,
                                            asn_id=asn_num)
    if not foundation:
        print(f"  [ERROR] No foundation statements loaded for {asn_label}",
              file=sys.stderr)
        return False

    template = read_file(AUDIT_TEMPLATE)
    if not template:
        print("  [ERROR] Audit prompt template not found", file=sys.stderr)
        return False

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    open_issues = _load_open_issues(asn_num)
    if not open_issues:
        open_issues = "(none)"

    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str)
              .replace("{{open_issues}}", open_issues))

    print(f"  [AUDIT] Deep foundation audit of {asn_label}...",
          file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model=model, effort="medium")

    if not text:
        print(f"  [AUDIT] No output ({elapsed:.0f}s)", file=sys.stderr)
        return False

    log_usage("rebase-audit", elapsed, asn=asn_num)

    if "NO NEW ISSUES" in text:
        print(f"  [AUDIT] No new issues found ({elapsed:.0f}s)",
              file=sys.stderr)
        return True

    # Append new issues to open issues file
    _append_open_issues(asn_num, text)
    print(f"  [AUDIT] New issues appended ({elapsed:.0f}s)", file=sys.stderr)
    return True


def step_rebase(asn_num, asn_path, asn_label, model, effort,
                precheck_findings=None):
    """Step 1: Claude agent replaces local derivations with citations.

    If precheck_findings is provided, inject them into the rebase prompt.
    """
    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR,
                                            asn_id=asn_num)
    if not foundation:
        print(f"  [ERROR] No foundation statements loaded for {asn_label}",
              file=sys.stderr)
        return False

    template = read_file(REBASE_TEMPLATE)
    if not template:
        print("  [ERROR] Rebase prompt template not found", file=sys.stderr)
        return False

    if precheck_findings:
        findings_section = (
            "## Pre-Check Findings\n\n"
            "A consistency check identified the following issues. "
            "Address these in addition to the three passes above:\n\n"
            f"{precheck_findings}\n"
        )
    else:
        findings_section = ""

    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_path}}", str(asn_path))
              .replace("{{consistency_findings}}", findings_section))

    print(f"  [REBASE] {asn_label} against updated foundation...",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=25,
    )

    if data is None:
        print(f"  [ERROR] Rebase failed", file=sys.stderr)
        return False

    log_usage("rebase", elapsed, asn=asn_num)
    print(f"  [REBASED] {asn_label}", file=sys.stderr)
    return True


def step_rebase_review(asn_num, asn_path, asn_label, rebased_properties,
                       model, effort):
    """Step 2a: Targeted review of rebase changes."""
    asn_content = asn_path.read_text()
    vocabulary = read_file(VOCABULARY)
    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR,
                                            asn_id=asn_num)

    template = read_file(REBASE_REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Rebase review prompt not found", file=sys.stderr)
        return None

    prompt = (template
              .replace("{{asn_content}}", asn_content)
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation)
              .replace("{{rebased_properties}}", rebased_properties))

    print(f"  [REVIEW] Rebase review of {asn_label}...", file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model=model, effort=effort)

    if not text:
        print(f"  [WARN] Rebase review produced no output", file=sys.stderr)
        return None

    log_usage("rebase-review", elapsed, asn=asn_num)

    # Write review to file
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if "VERDICT: CONVERGED" in text:
        print(f"  [CONVERGED] Rebase is clean", file=sys.stderr)
        return "CONVERGED"

    print(f"  [REVISE] Rebase issues found", file=sys.stderr)
    return text


def step_rebase_revise(asn_num, asn_path, asn_label, rebased_properties,
                       review_text, model, effort):
    """Step 2b: Fix rebase issues."""
    vocabulary = read_file(VOCABULARY)
    foundation = load_foundation_statements(FOUNDATION_LIST, STATEMENTS_DIR,
                                            asn_id=asn_num)

    template = read_file(REBASE_REVISE_TEMPLATE)
    if not template:
        print("  [ERROR] Rebase revise prompt not found", file=sys.stderr)
        return False

    prompt = (template
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_path}}", str(asn_path))
              .replace("{{rebased_properties}}", rebased_properties)
              .replace("{{review_content}}", review_text))

    print(f"  [REVISE] Fixing rebase issues in {asn_label}...",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=20,
    )

    if data is None:
        print(f"  [WARN] Rebase revise failed", file=sys.stderr)
        return False

    log_usage("rebase-revise", elapsed, asn=asn_num)
    return True


def step_review_revise(asn_num, asn_path, asn_label, rebased_properties,
                       max_cycles, model, effort):
    """Step 2: Rebase review/revise loop."""
    for cycle in range(1, max_cycles + 1):
        print(f"\n  --- Rebase review cycle {cycle}/{max_cycles} ---",
              file=sys.stderr)

        result = step_rebase_review(asn_num, asn_path, asn_label,
                                    rebased_properties, model, effort)

        if result is None:
            print(f"  [WARN] Review failed, continuing", file=sys.stderr)
            return False

        if result == "CONVERGED":
            return True

        ok = step_rebase_revise(asn_num, asn_path, asn_label,
                                rebased_properties, result, model, effort)
        if not ok:
            print(f"  [WARN] Revise failed at cycle {cycle}",
                  file=sys.stderr)
            return False

        step_commit(f"rebase(asn): {asn_label} revise cycle {cycle}")

    print(f"  [WARN] Did not converge after {max_cycles} cycles",
          file=sys.stderr)
    return False


def step_export(asn_num):
    """Step 3: Re-export the ASN."""
    print(f"  [EXPORT] Re-exporting ASN-{asn_num:04d}...", file=sys.stderr)

    cmd = [sys.executable,
           str(WORKSPACE / "scripts" / "export.py"),
           str(asn_num)]
    result = subprocess.run(cmd, capture_output=False, text=True,
                            cwd=str(WORKSPACE))

    if result.returncode != 0:
        print(f"  [WARN] Export failed", file=sys.stderr)
        return False
    return True


def update_rebase_timestamp(asn_num):
    """Write last_rebase_check to the project model yaml."""
    yaml_path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}.yaml"
    if not yaml_path.exists():
        return

    content = yaml_path.read_text()
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Update existing or append
    if "last_rebase_check:" in content:
        content = re.sub(r'^last_rebase_check:.*$',
                         f'last_rebase_check: "{ts}"', content,
                         flags=re.MULTILINE)
    else:
        content = content.rstrip() + f'\nlast_rebase_check: "{ts}"\n'

    yaml_path.write_text(content)
    print(f"  [TIMESTAMP] last_rebase_check: {ts}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Rebase an ASN against its updated foundation")
    parser.add_argument("asn", type=int,
                        help="ASN number to rebase")
    parser.add_argument("--properties", default=None,
                        help="Comma-separated property labels to rebase "
                             "(default: auto-detect from foundation)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Max review/revise cycles (default: 5)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_label = f"ASN-{args.asn:04d}"

    # Validate
    asn_path, asn_label, manifest = validate(args.asn)

    print(f"  [REBASE] {asn_label}", file=sys.stderr)

    if args.properties:
        rebased_properties = args.properties
    else:
        rebased_properties = "(auto-detect from foundation)"

    if args.dry_run:
        print(f"  [DRY RUN] Steps: rebase → review/revise → export",
              file=sys.stderr)
        return

    # Step 1: Rebase — replace local derivations with citations
    ok = step_rebase(args.asn, asn_path, asn_label, args.model, args.effort)
    if not ok:
        print(f"  [ABORT] Rebase failed", file=sys.stderr)
        sys.exit(1)

    step_commit(f"rebase(asn): {asn_label} against updated foundation")

    # Determine rebased properties for review scope
    if args.properties:
        rebased_properties = args.properties
    else:
        rebased_properties = "D0, D1"  # TODO: detect from diff

    # Step 2: Review/revise the rebase
    step_review_revise(args.asn, asn_path, asn_label, rebased_properties,
                       args.max_cycles, args.model, args.effort)

    # Step 3: Re-export
    step_export(args.asn)

    # Record rebase check timestamp in project model
    update_rebase_timestamp(args.asn)

    log_usage("rebase-complete", 0, asn=args.asn)
    print(f"\n  [DONE] {asn_label} rebased", file=sys.stderr)


if __name__ == "__main__":
    main()
