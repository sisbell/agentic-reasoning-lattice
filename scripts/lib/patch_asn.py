#!/usr/bin/env python3
"""
Apply a targeted patch to an ASN with scoped review/revise cycle.

Reads a patch instruction file, applies the fix, propagates ripple
effects, then runs a scoped review/revise cycle to verify correctness.

Usage:
    python scripts/patch.py 63 --patch patch-1.md
    python scripts/patch.py 63 --patch patch-1.md --dry-run
"""

import argparse
import re
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, REVIEWS_DIR,
                   VOCABULARY, load_manifest,
                   next_review_number)
from lib.common import (read_file, find_asn, invoke_claude, invoke_claude_agent,
                         log_usage, step_commit_asn)
from lib.foundation import load_foundation_statements


PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
PATCH_TEMPLATE = PROMPTS_DIR / "patch.md"
PATCH_REVIEW_TEMPLATE = PROMPTS_DIR / "patch-review.md"
PATCH_REVISE_TEMPLATE = PROMPTS_DIR / "patch-revise.md"
PATCHES_DIR = WORKSPACE / "vault" / "1-reasoning-docs-patches"


def validate(asn_num, patch_name):
    """Validate ASN and patch file exist."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    patch_dir = PATCHES_DIR / f"ASN-{asn_num:04d}"
    patch_path = patch_dir / patch_name
    if not patch_path.exists():
        print(f"  [ERROR] Patch not found: {patch_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    return asn_path, asn_label, patch_path


def step_apply(asn_num, asn_path, asn_label, patch_content, model, effort):
    """Step 1: Apply patch to ASN."""
    template = read_file(PATCH_TEMPLATE)
    if not template:
        print("  [ERROR] Patch prompt template not found", file=sys.stderr)
        return False

    prompt = (template
              .replace("{{patch_content}}", patch_content)
              .replace("{{asn_path}}", str(asn_path)))

    print(f"  [PATCH] Applying to {asn_label}...", file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=15,
    )

    if data is None:
        print(f"  [ERROR] Patch application failed", file=sys.stderr)
        return False

    log_usage("patch-apply", elapsed, asn=asn_num)
    print(f"  [APPLIED] {asn_label}", file=sys.stderr)
    return True


def step_patch_review(asn_num, asn_path, asn_label, patch_content,
                      model, effort):
    """Step 2a: Scoped review of the patch."""
    asn_content = asn_path.read_text()
    vocabulary = read_file(VOCABULARY)
    foundation = load_foundation_statements(asn_num)

    template = read_file(PATCH_REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Patch review prompt not found", file=sys.stderr)
        return None

    prompt = (template
              .replace("{{asn_content}}", asn_content)
              .replace("{{patch_content}}", patch_content)
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation))

    print(f"  [REVIEW] Patch review of {asn_label}...", file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model=model, effort=effort)

    if not text:
        print(f"  [WARN] Patch review produced no output", file=sys.stderr)
        return None

    log_usage("patch-review", elapsed, asn=asn_num)

    # Write review to file
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if "VERDICT: CONVERGED" in text:
        print(f"  [CONVERGED] Patch is clean", file=sys.stderr)
        return "CONVERGED"

    print(f"  [REVISE] Patch issues found", file=sys.stderr)
    return text


def step_patch_revise(asn_num, asn_path, asn_label, patch_content,
                      review_text, model, effort):
    """Step 2b: Fix patch issues."""
    vocabulary = read_file(VOCABULARY)
    foundation = load_foundation_statements(asn_num)

    template = read_file(PATCH_REVISE_TEMPLATE)
    if not template:
        print("  [ERROR] Patch revise prompt not found", file=sys.stderr)
        return False

    prompt = (template
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_path}}", str(asn_path))
              .replace("{{patch_content}}", patch_content)
              .replace("{{review_content}}", review_text))

    print(f"  [REVISE] Fixing patch issues in {asn_label}...",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=15,
    )

    if data is None:
        print(f"  [WARN] Patch revise failed", file=sys.stderr)
        return False

    log_usage("patch-revise", elapsed, asn=asn_num)
    return True


def step_review_revise(asn_num, asn_path, asn_label, patch_content,
                       max_cycles, model, effort):
    """Step 2: Patch review/revise loop."""
    for cycle in range(1, max_cycles + 1):
        print(f"\n  --- Patch review cycle {cycle}/{max_cycles} ---",
              file=sys.stderr)

        result = step_patch_review(asn_num, asn_path, asn_label,
                                   patch_content, model, effort)

        if result is None:
            print(f"  [WARN] Review failed, retrying once...",
                  file=sys.stderr)
            result = step_patch_review(asn_num, asn_path, asn_label,
                                       patch_content, model, effort)
            if result is None:
                print(f"  [WARN] Review failed again, stopping",
                      file=sys.stderr)
                return False

        if result == "CONVERGED":
            return True

        ok = step_patch_revise(asn_num, asn_path, asn_label, patch_content,
                               result, model, effort)
        if not ok:
            print(f"  [WARN] Revise failed at cycle {cycle}",
                  file=sys.stderr)
            return False

        step_commit_asn(asn_num,
                    f"patch(asn): {asn_label} patch revise cycle {cycle}")

    print(f"  [WARN] Did not converge after {max_cycles} cycles",
          file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN with scoped review")
    parser.add_argument("asn", type=int,
                        help="ASN number to patch")
    parser.add_argument("--patch", required=True,
                        help="Patch filename (in vault/1-reasoning-docs-patches/ASN-NNNN/)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-cycles", type=int, default=10,
                        help="Max review/revise cycles (default: 10)")
    parser.add_argument("--report", action="store_true",
                        help="Show impact report without applying")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_label = f"ASN-{args.asn:04d}"

    # Validate
    asn_path, asn_label, patch_path = validate(args.asn, args.patch)
    patch_content = patch_path.read_text()

    print(f"  [PATCH] {asn_label} ← {patch_path.name}", file=sys.stderr)

    if args.report:
        report_template = read_file(PROMPTS_DIR / "patch-report.md")
        if not report_template:
            print("  [ERROR] Patch report prompt not found", file=sys.stderr)
            sys.exit(1)
        asn_content = asn_path.read_text()
        prompt = (report_template
                  .replace("{{patch_content}}", patch_content)
                  .replace("{{asn_content}}", asn_content))
        print(f"  [REPORT] Analyzing impact...", file=sys.stderr)
        text, elapsed = invoke_claude(prompt, model=args.model,
                                      effort=args.effort)
        if text:
            print(f"\n{text}\n", file=sys.stderr)
        else:
            print("  [ERROR] No report produced", file=sys.stderr)
        return

    if args.dry_run:
        print(f"  [DRY RUN] Steps: apply → scoped review/revise",
              file=sys.stderr)
        print(f"  Patch content:\n{patch_content}", file=sys.stderr)
        return

    # Step 1: Apply patch
    ok = step_apply(args.asn, asn_path, asn_label, patch_content,
                    args.model, args.effort)
    if not ok:
        print(f"  [ABORT] Patch application failed", file=sys.stderr)
        sys.exit(1)

    step_commit_asn(args.asn,
                f"patch(asn): {asn_label} apply {patch_path.name}")

    # Step 2: Scoped review/revise
    step_review_revise(args.asn, asn_path, asn_label, patch_content,
                       args.max_cycles, args.model, args.effort)

    # Re-export
    print(f"  [EXPORT] Re-exporting {asn_label}...", file=sys.stderr)
    import subprocess
    cmd = [sys.executable,
           str(WORKSPACE / "scripts" / "export.py"),
           str(args.asn)]
    subprocess.run(cmd, capture_output=False, text=True,
                   cwd=str(WORKSPACE))

    log_usage("patch-complete", 0, asn=args.asn)
    print(f"\n  [DONE] {asn_label} patched", file=sys.stderr)
    print(f"  [NEXT] Optional full review: "
          f"python scripts/revise.py {args.asn} --converge",
          file=sys.stderr)


if __name__ == "__main__":
    main()
