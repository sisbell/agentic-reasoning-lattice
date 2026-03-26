#!/usr/bin/env python3
"""
Review pipeline — produce a Dijkstra-style review of an ASN.

Runs a single review pass: analyze the ASN for rigor, produce structured
findings, commit the review file, and stop. Revision is handled separately
by revise.py.

Usage:
    python scripts/review.py 9                # review, commit, stop
    python scripts/review.py 9 --review-only  # (deprecated, same as default)
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import WORKSPACE, ASNS_DIR

REVIEW_SCRIPT = WORKSPACE / "scripts" / "lib" / "review_check.py"
CONSULT_REVISION_SCRIPT = WORKSPACE / "scripts" / "lib" / "review_consult.py"
REVISE_SCRIPT = WORKSPACE / "scripts" / "lib" / "review_revise.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


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
    """Run review-asn.py. Returns (review_path, converged).

    converged is True when the reviewer's VERDICT is CONVERGED (exit 2).
    """
    print(f"\n  === REVIEW ===", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT), str(asn_id)],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    converged = result.returncode == 2

    if result.returncode not in (0, 2):
        print(f"  [REVIEW] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                print(f"    {line}", file=sys.stderr)
        return None, False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    review_path = result.stdout.strip()
    if review_path and Path(review_path).exists():
        return review_path, converged
    return None, False


def has_revise_items(review_path):
    """Check if review has REVISE items.

    Recognizes both standard review format (## REVISE) and
    consistency check format (RESULT: n FINDINGS).
    """
    try:
        content = Path(review_path).read_text()
        if "## REVISE" in content:
            return True
        if "RESULT:" in content and "FINDINGS" in content:
            return True
        return False
    except (FileNotFoundError, OSError):
        return False


def step_consult_revision(asn_id, review_path):
    """Run consult_for_revision.py. Returns consultation results path or None."""
    print(f"\n  === CONSULT ===", file=sys.stderr)
    cmd = [sys.executable, str(CONSULT_REVISION_SCRIPT), str(asn_id)]

    # Pass the review filename (e.g., "review-6") for targeting
    review_name = Path(review_path).stem  # e.g., ASN-0001-review-6
    # Extract "review-N" part
    m = re.search(r"(review-\d+)", review_name)
    if m:
        cmd.append(m.group(1))

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [CONSULT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    consultation_path = result.stdout.strip()
    if consultation_path and Path(consultation_path).exists():
        return consultation_path
    return None


def step_revise(asn_id, review_spec=None, consultation_path=None):
    """Run revise-asn.py. Returns (asn_path, converged).

    converged is True when the ASN was not modified (exit 2).
    """
    print(f"\n  === REVISE ===", file=sys.stderr)
    cmd = [sys.executable, str(REVISE_SCRIPT), str(asn_id)]
    if review_spec:
        cmd.append(review_spec)
    if consultation_path:
        cmd.extend(["--consultation", consultation_path])

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    converged = result.returncode == 2

    if result.returncode not in (0, 2):
        print(f"  [REVISE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        return asn_path, converged
    return None, False


def step_commit(hint="", asn_id=None):
    """Run commit.py. If asn_id is provided, stage only that ASN's files.

    For concurrent safety — two ASN pipelines won't include each
    other's changes when asn_id is specified.
    """
    print(f"\n  === COMMIT ===", file=sys.stderr)

    # Stage only this ASN's files if scoped
    if asn_id is not None:
        import glob
        label = f"ASN-{int(asn_id):04d}"
        patterns = [
            f"vault/1-reasoning-docs/{label}-*",
            f"vault/2-review/{label}",
            f"vault/0-consultations/{label}",
            f"vault/project-model/{label}/",
            f"vault/6-examples/{label}",
        ]
        for pattern in patterns:
            full = str(WORKSPACE / pattern)
            matches = glob.glob(full)
            if matches:
                subprocess.run(
                    ["git", "add"] + matches,
                    capture_output=True, text=True, cwd=str(WORKSPACE),
                )
            # Also handle directories
            dirpath = WORKSPACE / pattern
            if dirpath.is_dir():
                subprocess.run(
                    ["git", "add", str(dirpath)],
                    capture_output=True, text=True, cwd=str(WORKSPACE),
                )

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
        description="Review an ASN — produce findings and stop")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("--review-only", action="store_true",
                        help="(deprecated — review-only is now the default)")
    args = parser.parse_args()

    if args.review_only:
        print("  Note: --review-only is deprecated; review.py is now review-only by default.",
              file=sys.stderr)

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/", file=sys.stderr)
        sys.exit(1)

    print(f"  [REVIEW] {asn_label} ({asn_path.name})", file=sys.stderr)
    asn_number = int(asn_label.replace("ASN-", ""))

    start = time.time()

    # Review
    review_path, converged = step_review(args.asn)
    if review_path is None:
        print(f"  [REVIEW] Review failed, retrying once...", file=sys.stderr)
        review_path, converged = step_review(args.asn)
        if review_path is None:
            print(f"  [REVIEW] Review failed again", file=sys.stderr)
            sys.exit(1)
    print(f"  [REVIEW] {review_path}", file=sys.stderr)

    # Converged — commit and exit 2
    if converged:
        print(f"  [REVIEW] CONVERGED — no significant issues",
              file=sys.stderr)
        step_commit(f"Review {asn_label} — converged", asn_id=asn_number)
        elapsed = time.time() - start
        print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)
        asn_num = asn_label.replace("ASN-", "").lstrip("0") or "0"
        print(f"\n  [NEXT] Export statements: python scripts/normalize.py {asn_num}",
              file=sys.stderr)
        sys.exit(2)

    # Check for REVISE items
    if has_revise_items(review_path):
        step_commit(f"Review {asn_label}", asn_id=asn_number)
        elapsed = time.time() - start
        print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)
        print(f"  REVISE items found. Run: python scripts/revise.py {args.asn}",
              file=sys.stderr)
        sys.exit(0)

    # No REVISE items — commit and exit
    step_commit(f"Review {asn_label} — no revisions needed", asn_id=asn_number)
    elapsed = time.time() - start
    print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
