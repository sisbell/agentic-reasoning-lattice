#!/usr/bin/env python3
"""
Converge Patch — apply targeted fixes to ASNs in claim convergence.

Reads a patch instruction from the lattice's discovery/patches/ASN-NNNN/ directory,
applies the fix, and commits. The claim-convergence pipeline runs afterward
to verify correctness.

Usage:
    python scripts/converge-patch.py 34 --patch patch-ta5.md
    python scripts/converge-patch.py 34 --patch patch-ta5.md --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, PATCHES_DIR, prompt_path
from lib.shared.common import find_asn, step_commit_asn

APPLY_TEMPLATE = prompt_path("claim-convergence/patch/apply.md")


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
    """Apply patch to ASN."""
    template = APPLY_TEMPLATE.read_text()
    prompt = (template
              .replace("{{patch_content}}", patch_content)
              .replace("{{asn_path}}", str(asn_path.relative_to(WORKSPACE))))

    cmd = [
        "claude", "-p",
        "--model", {"opus": "claude-opus-4-7", "sonnet": "claude-sonnet-4-6"}[model],
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    print(f"  [APPLY] Applying to {asn_label}...",
          end="", file=sys.stderr, flush=True)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return False

    cost = 0
    try:
        data = json.loads(result.stdout)
        cost = data.get("total_cost_usd", 0)
    except (json.JSONDecodeError, KeyError):
        pass

    print(f" done ({elapsed:.0f}s, ${cost:.2f})", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "converge-patch",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN in claim convergence")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--patch", required=True,
                        help="Patch filename (in the lattice's discovery/patches/ASN-NNNN/ directory)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label, patch_path = validate(asn_num, args.patch)
    patch_content = patch_path.read_text()

    print(f"\n  [PATCH] {asn_label} \u2190 {patch_path.name}", file=sys.stderr)

    if args.dry_run:
        print(f"\n  [DRY RUN] Would apply:", file=sys.stderr)
        print(f"\n{patch_content}", file=sys.stderr)
        return

    ok = step_apply(asn_num, asn_path, asn_label, patch_content,
                    args.model, args.effort)
    if not ok:
        print(f"  [ABORT] Patch application failed", file=sys.stderr)
        sys.exit(1)

    step_commit_asn(asn_num,
                    hint=f"patch(asn): {asn_label} apply {patch_path.name}")

    print(f"\n  [NEXT] Run claim convergence pipeline to verify:",
          file=sys.stderr)
    print(f"  ./run/converge.sh --from dependency-review {asn_num}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
