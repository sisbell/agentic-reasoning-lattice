#!/usr/bin/env python3
"""
Discovery Patch — apply a targeted fix to an ASN with scoped review/revise.

Reads a patch instruction from the lattice's discovery/patches/ASN-NNNN/ directory,
applies the fix, propagates downstream effects, then runs a scoped
review/revise cycle to verify correctness.

Usage:
    python scripts/discovery-patch.py 63 --patch patch-1.md
    python scripts/discovery-patch.py 63 --patch patch-1.md --dry-run
    python scripts/discovery-patch.py 63 --patch patch-1.md --report
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE
from lib.shared.common import read_file, invoke_claude, log_usage, step_commit_asn
from lib.discovery.patch.apply import (
    validate, step_apply, step_review_revise, PROMPTS_DIR,
)


def main():
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN with scoped review")
    parser.add_argument("asn", type=int,
                        help="ASN number to patch")
    parser.add_argument("--patch", required=True,
                        help="Patch filename (in the lattice's discovery/patches/ASN-NNNN/ directory)")
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

    # Validate
    asn_path, asn_label, patch_path = validate(args.asn, args.patch)
    patch_content = patch_path.read_text()

    print(f"  [PATCH] {asn_label} ← {patch_path.name}", file=sys.stderr)

    if args.report:
        report_template = read_file(PROMPTS_DIR / "report.md")
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
    cmd = [sys.executable,
           str(WORKSPACE / "scripts" / "discovery-assembly.py"),
           str(args.asn)]
    subprocess.run(cmd, capture_output=False, text=True,
                   cwd=str(WORKSPACE))

    log_usage("patch-complete", 0, asn=args.asn)
    print(f"\n  [DONE] {asn_label} patched", file=sys.stderr)
    print(f"  [NEXT] Optional full review: "
          f"python scripts/discovery-revise.py {args.asn} --converge",
          file=sys.stderr)


if __name__ == "__main__":
    main()
