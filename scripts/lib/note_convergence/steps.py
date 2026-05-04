"""Note-convergence pipeline steps.

Single-pass review and revise step functions used by the standalone
CLIs (`scripts/note-review.py`, `scripts/note-revise.py`). step_review
and step_revise dispatch directly to the agents and orchestrator
helpers — no Python subprocess wrapping. step_consult_revision and
step_commit still subprocess external scripts (gather_evidence.py and
commit.py respectively) since those live outside the agent layer.
"""

import re
import subprocess
import sys
import time
from pathlib import Path

from lib.agents.note_review import run_note_review
from lib.agents.note_revise import run_revise_pass
from lib.protocols.febe.session import open_session
from lib.orchestrators.note_converge import (
    collect_open_revises,
    commit_note_review,
    log_usage,
    process_resolved_issues,
)
from lib.shared.common import find_asn, read_file, stage_asn_files
from lib.shared.paths import LATTICE, NOTE_DIR, WORKSPACE


CONSULT_REVISION_SCRIPT = (
    WORKSPACE / "scripts" / "lib" / "consultation" / "gather_evidence.py"
)
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def step_review(asn_id):
    """Run a review pass directly. Returns (review_path, converged).

    converged is True when the reviewer's VERDICT is CONVERGED.
    """
    print("\n  === REVIEW ===", file=sys.stderr)
    asn_path, asn_label = find_asn(str(asn_id))
    if asn_path is None:
        print(
            f"  [REVIEW] FAILED — ASN-{asn_id} not found in "
            f"{NOTE_DIR.relative_to(WORKSPACE)}/", file=sys.stderr,
        )
        return None, False
    asn_number = int(asn_label.replace("ASN-", ""))

    print(f"  [REVIEW] {asn_label}", file=sys.stderr)

    start = time.time()
    verdict, text, elapsed = run_note_review(asn_path, asn_label)
    if verdict == "ERROR" or not text:
        print("  [REVIEW] FAILED — review error", file=sys.stderr)
        return None, False

    session = open_session(LATTICE)
    review_path, findings = commit_note_review(
        session, asn_path, asn_label, text,
    )

    if findings:
        revise_count = sum(1 for _, c, _ in findings if c == "REVISE")
        oos_count = len(findings) - revise_count
        print(
            f"  [FINDINGS] {revise_count} REVISE, "
            f"{oos_count} OUT_OF_SCOPE",
            file=sys.stderr,
        )

    process_resolved_issues(asn_number, text)
    print(f"  [VERDICT] {verdict}", file=sys.stderr)
    log_usage(asn_label, elapsed, skill="review")

    converged = verdict == "CONVERGED"
    return str(review_path), converged


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
    print("\n  === CONSULT ===", file=sys.stderr)
    cmd = [sys.executable, str(CONSULT_REVISION_SCRIPT), str(asn_id)]

    review_name = Path(review_path).stem
    m = re.search(r"(review-\d+)", review_name)
    if m:
        cmd.append(m.group(1))

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print("  [CONSULT] FAILED", file=sys.stderr)
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
    """Run a revise pass directly. Returns (asn_path, converged).

    converged is True when no open revise comments remained — either
    because none existed at the start (already converged) or because
    the agent closed all of them.
    """
    print("\n  === REVISE ===", file=sys.stderr)
    asn_path, asn_label = find_asn(str(asn_id))
    if asn_path is None:
        print(f"  [REVISE] FAILED — ASN-{asn_id} not found", file=sys.stderr)
        return None, False

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))

    session = open_session(LATTICE)
    findings = collect_open_revises(session, note_rel)

    if not findings:
        print(
            f"  [CONVERGED] No open revise comments on {asn_label}",
            file=sys.stderr,
        )
        return str(asn_path), True

    print(
        f"  [REVISE] {asn_label} ({asn_path.name}) — "
        f"{len(findings)} open finding(s)", file=sys.stderr,
    )

    consultation_content = None
    if consultation_path:
        consultation_content = read_file(consultation_path)
        if not consultation_content:
            print(
                f"  Warning: consultation file not found: "
                f"{consultation_path}",
                file=sys.stderr,
            )
            consultation_content = None
        else:
            print(
                f"  [CONSULTATION] {Path(consultation_path).name}",
                file=sys.stderr,
            )

    data, elapsed = run_revise_pass(
        asn_path, asn_label, findings,
        consultation_content=consultation_content,
    )
    if data is None:
        print("  [REVISE] Revision failed", file=sys.stderr)
        return None, False
    log_usage(asn_label, elapsed, skill="revise", data=data)

    session = open_session(LATTICE)
    remaining = collect_open_revises(session, note_rel)

    closed_count = len(findings) - len(remaining)
    print(
        f"  [CLOSED] {closed_count}/{len(findings)} comment(s) "
        f"resolved this session", file=sys.stderr,
    )

    if remaining:
        print(
            f"  [OPEN] {len(remaining)} comment(s) still need revision:",
            file=sys.stderr,
        )
        for _, title, _ in remaining:
            print(f"    - {title}", file=sys.stderr)

    converged = not remaining
    return str(asn_path), converged


def step_commit(hint="", asn_id=None):
    """Run commit.py. If asn_id is provided, stage only that ASN's files."""
    print("\n  === COMMIT ===", file=sys.stderr)

    if asn_id is not None:
        stage_asn_files(f"ASN-{int(asn_id):04d}")

    cmd = [sys.executable, str(COMMIT_SCRIPT)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print("  [COMMIT] FAILED", file=sys.stderr)
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
