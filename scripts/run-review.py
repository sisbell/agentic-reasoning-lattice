#!/usr/bin/env python3
"""
Review-revise pipeline — review → revise → commit, optionally repeated.

Orchestrates ASN quality improvement by calling step scripts:
  1. Review: Dijkstra-style rigor check (opus, no tools)
  2. Revise: targeted fixes addressing review findings (opus, with tools)
  3. Commit: commit vault changes (sonnet)

Each cycle produces a numbered review in vault/reviews/ and revises the ASN
in place. Multiple cycles progressively tighten the specification.

Usage:
    python scripts/run-review.py 9                # 1 cycle: review → revise → commit
    python scripts/run-review.py 9 --cycles 2     # 2 cycles
    python scripts/run-review.py 9 --review-only  # just review, no revise or commit
    python scripts/run-review.py 9 --resume revise  # skip review, use latest
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
ASNS_DIR = WORKSPACE / "vault" / "asns"
REVIEWS_DIR = WORKSPACE / "vault" / "reviews"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"

REVIEW_SCRIPT = WORKSPACE / "scripts" / "review-asn.py"
REVISE_SCRIPT = WORKSPACE / "scripts" / "revise-asn.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"

STEPS = ["review", "revise", "commit"]


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def step_review(asn_id):
    """Run review-asn.py. Returns review file path or None."""
    print(f"\n  === REVIEW ===", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT), str(asn_id)],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [REVIEW] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    review_path = result.stdout.strip()
    if review_path and Path(review_path).exists():
        return review_path
    return None


def has_revise_items(review_path):
    """Check if review has REVISE items."""
    try:
        content = Path(review_path).read_text()
        return "## REVISE" in content
    except (FileNotFoundError, OSError):
        return False


def step_revise(asn_id, review_spec=None):
    """Run revise-asn.py. Returns ASN path or None."""
    print(f"\n  === REVISE ===", file=sys.stderr)
    cmd = [sys.executable, str(REVISE_SCRIPT), str(asn_id)]
    if review_spec:
        cmd.append(review_spec)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [REVISE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        return asn_path
    return None


def step_commit(hint=""):
    """Run commit.py. Returns True if committed."""
    print(f"\n  === COMMIT ===", file=sys.stderr)
    cmd = [sys.executable, str(COMMIT_SCRIPT)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Review-revise pipeline for ASNs")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("--cycles", "-n", type=int, default=1,
                        help="Number of review-revise cycles (default: 1)")
    parser.add_argument("--review-only", action="store_true",
                        help="Run review only, no revise or commit")
    parser.add_argument("--resume", choices=STEPS,
                        help="Resume from this step (skip earlier steps)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/asns/", file=sys.stderr)
        sys.exit(1)

    print(f"  [PIPELINE] {asn_label} ({asn_path.name})", file=sys.stderr)
    if not args.review_only:
        print(f"  [PIPELINE] {args.cycles} cycle(s): review → revise → commit",
              file=sys.stderr)

    start = time.time()

    for cycle in range(1, args.cycles + 1):
        if args.cycles > 1:
            print(f"\n  ──── Cycle {cycle}/{args.cycles} ────",
                  file=sys.stderr)

        # Review
        if not args.resume or args.resume == "review":
            review_path = step_review(args.asn)
            if review_path is None:
                print(f"  [PIPELINE] Review failed, stopping", file=sys.stderr)
                sys.exit(1)
            print(f"  [REVIEW] {review_path}", file=sys.stderr)
            args.resume = None  # clear resume after first step
        else:
            review_path = None

        if args.review_only:
            break

        # Check for REVISE items
        if review_path and not has_revise_items(review_path):
            print(f"  [PIPELINE] No REVISE items — ASN is clean",
                  file=sys.stderr)
            # Still commit the review file
            step_commit(f"Review {asn_label} — no revisions needed")
            break

        # Revise
        if not args.resume or args.resume == "revise":
            asn_result = step_revise(args.asn)
            if asn_result is None:
                print(f"  [PIPELINE] Revise failed, stopping",
                      file=sys.stderr)
                sys.exit(1)
            args.resume = None

        # Commit
        if not args.resume or args.resume == "commit":
            step_commit(f"Review and revise {asn_label} (cycle {cycle})")
            args.resume = None

    elapsed = time.time() - start
    print(f"\n  [PIPELINE] Done ({elapsed:.0f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
