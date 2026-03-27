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
import re
import subprocess
import sys
import time
import yaml

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, PROJECT_MODEL_DIR,
                   REVIEWS_DIR, VOCABULARY,
                   load_manifest, next_review_number,
                   formal_stmts, dep_graph, open_issues_path, project_yaml)
from lib.common import (read_file, find_asn, invoke_claude, invoke_claude_agent,
                         log_usage, step_commit)
from lib.foundation import load_foundation_statements


PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
REBASE_TEMPLATE = PROMPTS_DIR / "rebase.md"
REBASE_REVIEW_TEMPLATE = PROMPTS_DIR / "rebase-review.md"
REBASE_REVISE_TEMPLATE = PROMPTS_DIR / "rebase-revise.md"
AUDIT_TEMPLATE = PROMPTS_DIR / "rebase-audit.md"
SURFACE_CHECK_TEMPLATE = PROMPTS_DIR / "surface-check.md"
DOMAIN_EXTENSIONS_TEMPLATE = PROMPTS_DIR / "domain-extensions.md"
TRANSFER_VERIFICATION_TEMPLATE = PROMPTS_DIR / "transfer-verification.md"


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
    path = open_issues_path(asn_num)
    if path.exists():
        return path.read_text().strip()
    return ""


def _append_open_issues(asn_num, new_issues):
    """Append new issues to the open issues file."""
    path = open_issues_path(asn_num)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = ""
    if path.exists():
        existing = path.read_text().strip()

    if existing:
        content = existing + "\n\n" + new_issues.strip() + "\n"
    else:
        content = new_issues.strip() + "\n"

    path.write_text(content)
    print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)


def clear_open_issues(asn_num):
    """Clear the open issues file at the start of a rebase."""
    path = open_issues_path(asn_num)
    if path.exists():
        path.unlink()
        print(f"  [CLEARED] {path.relative_to(WORKSPACE)}", file=sys.stderr)


def _run_sonnet_check(asn_num, asn_path, asn_label, template_path,
                      step_name, clean_marker, effort="high",
                      has_open_issues=False):
    """Run a sonnet check from a template. Returns True if findings found.

    Common logic for surface-check, domain-extensions, and transfer-verification.
    """
    foundation = load_foundation_statements(asn_num)
    if not foundation:
        return False

    if not template_path.exists():
        print(f"  [{step_name}] Template not found: {template_path}",
              file=sys.stderr)
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

    if has_open_issues:
        open_issues = _load_open_issues(asn_num)
        prompt = prompt.replace("{{open_issues}}", open_issues or "(none)")

    print(f"  [{step_name}] Running on {asn_label}...", file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model="sonnet", effort=effort)

    if not text:
        print(f"  [{step_name}] No output ({elapsed:.0f}s)", file=sys.stderr)
        return False

    log_usage(f"rebase-{step_name.lower()}", elapsed, asn=asn_num)

    # Write as review file for the record
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Check for clean marker
    if clean_marker and clean_marker in text:
        print(f"  [{step_name}] Clean ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # Append raw output to open issues
    _append_open_issues(asn_num, text)
    print(f"  [{step_name}] Findings appended ({elapsed:.0f}s)",
          file=sys.stderr)
    return True


def step_surface_check(asn_num, asn_path, asn_label):
    """Surface check (sonnet): stale labels, drift, registry, deps, exhaustiveness.

    Returns True if findings were found, False if CLEAN.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        SURFACE_CHECK_TEMPLATE,
        step_name="SURFACE",
        clean_marker="RESULT: CLEAN",
    )


def step_find_extensions(asn_num, asn_path, asn_label):
    """Domain extension finder (sonnet): list all extensions and claimed analogs.

    Returns True if extensions were found, False if none.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        DOMAIN_EXTENSIONS_TEMPLATE,
        step_name="EXTENSIONS",
        clean_marker="NO EXTENSIONS FOUND",
    )


def step_verify_transfer(asn_num, asn_path, asn_label):
    """Transfer verification (sonnet, CoT): verify each domain extension is sound.

    Returns True if gaps were found, False if all verified or no extensions.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        TRANSFER_VERIFICATION_TEMPLATE,
        step_name="TRANSFER",
        clean_marker="ALL VERIFIED",
        effort="max",
    )


def step_audit(asn_num, asn_path, asn_label):
    """Run an open-ended foundation audit via opus.

    Reads the ASN, foundation, and accumulated open issues.
    Finds cross-boundary issues the structured checks missed.
    Appends new findings to the open issues file.
    """
    foundation = load_foundation_statements(asn_num)
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

    print(f"  [AUDIT] Open-ended audit of {asn_label}...",
          file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model="opus", effort="high")

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
    foundation = load_foundation_statements(asn_num)
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
    foundation = load_foundation_statements(asn_num)

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
    foundation = load_foundation_statements(asn_num)

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
           str(WORKSPACE / "scripts" / "normalize.py"),
           str(asn_num)]
    result = subprocess.run(cmd, capture_output=False, text=True,
                            cwd=str(WORKSPACE))

    if result.returncode != 0:
        print(f"  [WARN] Export failed", file=sys.stderr)
        return False
    return True


def update_rebase_timestamp(asn_num):
    """Write last_rebase_check to the project model yaml."""
    yaml_path = project_yaml(asn_num)
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
