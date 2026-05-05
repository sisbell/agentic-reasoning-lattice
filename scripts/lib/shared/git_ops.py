"""Git operations — staging, commit, HEAD lookup.

`step_commit` stages-and-commits whatever is currently dirty;
`step_commit_asn` scopes staging to a single ASN's known directory
patterns so concurrent ASN pipelines don't include each other's
changes.
"""

import glob
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, NOTE_DIR,
    CLAIM_REVIEWS_DIR, NOTE_REVIEWS_DIR,
    CLAIM_CONVERGENCE_DIR, CLAIM_DIR,
    CONSULTATIONS_DIR, EXAMPLES_DIR,
    CLAIM_FINDINGS_DIR, NOTE_FINDINGS_DIR,
    CITATION_RESOLVE_DIR, SIGNATURE_RESOLVE_DIR,
    RATIONALE_DIR, DOCUVERSE_LOG,
)


def git_head_sha(cwd=None):
    """Return the current HEAD SHA. cwd defaults to WORKSPACE."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(cwd or WORKSPACE), capture_output=True, text=True,
    )
    return result.stdout.strip()


def stage_asn_files(label):
    """Stage git files scoped to a single ASN. Returns True if anything staged.

    `glob.glob` matches both the markdown note file and any directories
    named `ASN-NNNN`; `git add` on a directory stages its contents.
    """
    patterns = [
        NOTE_DIR / f"{label}-*",
        CLAIM_REVIEWS_DIR / label,
        NOTE_REVIEWS_DIR / label,
        CLAIM_CONVERGENCE_DIR / label,
        CLAIM_DIR / label,
        CONSULTATIONS_DIR / label,
        EXAMPLES_DIR / label,
        CLAIM_FINDINGS_DIR / label,
        NOTE_FINDINGS_DIR / label,
        CITATION_RESOLVE_DIR / label,
        SIGNATURE_RESOLVE_DIR / label,
        RATIONALE_DIR / label,
        DOCUVERSE_LOG,
    ]
    staged = False
    for p in patterns:
        matches = glob.glob(str(p))
        if matches:
            result = subprocess.run(
                ["git", "add"] + matches,
                capture_output=True, text=True, cwd=str(WORKSPACE),
            )
            if result.returncode == 0:
                staged = True
    return staged


def step_commit_asn(asn_id, hint="", *, max_attempts=3, backoff_seconds=(5, 15)):
    """Stage and commit only files belonging to a specific ASN.

    Stages files matching the ASN's known directory patterns, then runs
    commit.py for the commit message. For concurrent safety — two ASN
    pipelines won't include each other's changes.

    Retries the commit-script subprocess up to `max_attempts` times when
    it exits non-zero. Most failures are transient (LLM API rate limit,
    network blip during message generation). Sleeps `backoff_seconds[i]`
    between attempts; iterates with the last value if attempts exceed
    the tuple's length.

    The substrate writes that preceded this call have already happened —
    if the commit can't land at all, those writes leave substrate ahead
    of git until a later commit picks up the staged-but-uncommitted
    files. Retry is the cheap defense against that drift.
    """
    label = f"ASN-{int(asn_id):04d}"
    if not stage_asn_files(label):
        print(f"  [COMMIT] No changes for {label}", file=sys.stderr)
        return False

    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
    if hint:
        cmd.append(hint)

    last_result = None
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            wait = backoff_seconds[min(attempt - 2, len(backoff_seconds) - 1)]
            print(f"  [COMMIT] retry {attempt}/{max_attempts} after {wait}s...",
                  file=sys.stderr)
            time.sleep(wait)

        last_result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
        )
        if last_result.returncode == 0:
            break
        print(f"  [COMMIT] attempt {attempt}/{max_attempts} failed",
              file=sys.stderr)
        if last_result.stderr:
            for line in last_result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)

    if last_result is None or last_result.returncode != 0:
        print(f"  [COMMIT] FAILED after {max_attempts} attempts — "
              f"changes left staged for next commit", file=sys.stderr)
        return False

    if last_result.stderr:
        for line in last_result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if last_result.stdout.strip():
        print(f"  {last_result.stdout.strip()}", file=sys.stderr)
    return True


def step_commit(hint=""):
    """Run commit.py via subprocess. Returns True if committed.

    Stages all lattices/xanadu/ changes. For ASN-scoped commits, use
    step_commit_asn() instead.
    """
    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
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
