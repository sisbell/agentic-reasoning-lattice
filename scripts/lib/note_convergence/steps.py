"""
Discovery pipeline step wrappers — subprocess calls to review, consult, revise, commit.

Shared by the review orchestrator (scripts/note-review.py) and the
revision loop orchestrator (lib/note_convergence/revise.py).
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE
from lib.shared.common import find_asn, stage_asn_files

REVIEW_SCRIPT = WORKSPACE / "scripts" / "lib" / "discovery" / "review.py"
CONSULT_REVISION_SCRIPT = WORKSPACE / "scripts" / "lib" / "discovery" / "revise" / "gather_evidence.py"
REVISE_SCRIPT = WORKSPACE / "scripts" / "lib" / "discovery" / "revise.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def step_review(asn_id):
    """Run review.py. Returns (review_path, converged).

    converged is True when the reviewer's VERDICT is CONVERGED (exit 2).
    """
    print(f"\n  === REVIEW ===", file=sys.stderr)
    cmd = [sys.executable, str(REVIEW_SCRIPT), str(asn_id)]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
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
    """Run gather_evidence.py. Returns consultation results path or None."""
    print(f"\n  === CONSULT ===", file=sys.stderr)
    cmd = [sys.executable, str(CONSULT_REVISION_SCRIPT), str(asn_id)]

    # Pass the review filename (e.g., "review-6") for targeting
    review_name = Path(review_path).stem
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
    """Run review_revise.py. Returns (asn_path, converged).

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
    """Run commit.py. If asn_id is provided, stage only that ASN's files."""
    print(f"\n  === COMMIT ===", file=sys.stderr)

    if asn_id is not None:
        stage_asn_files(f"ASN-{int(asn_id):04d}")

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
