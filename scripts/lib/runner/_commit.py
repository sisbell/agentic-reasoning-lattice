"""Per-fire auto-commit for the runner.

After every successful agent fire, snapshot the working-tree diff and
commit it under a Sonnet-drafted one-line message. Lets long convergence
runs survive crashes with at most one fire's work lost.

This is a development convenience, not a protocol primitive — the
substrate (`_docuverse/links.jsonl` + on-disk docs) is the audit trail,
and commits are checkpoints over that trail.

Failure modes are non-fatal: any subprocess error skips the commit and
keeps the runner moving. The next successful fire's commit will sweep
up the prior fire's residual diff.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from lib.backend.addressing import Address
from lib.backend.types import TypeRegistry
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import WORKSPACE, worker_pending_jsonl


_MAX_DIFF_CHARS = 30000
_LINKS_JSONL = "_docuverse/links.jsonl"

# Retry config for git operations that race on `.git/index.lock` (common
# under parallel runners). Total budget is the sum of (initial_delay *
# 2**i) over the retry count, plus the cost of each git invocation.
_GIT_LOCK_RETRY_COUNT = 6
_GIT_LOCK_RETRY_INITIAL_DELAY = 0.25


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )


# Error fragments that indicate transient parallel-git contention
# rather than a real failure. Each is something git emits when two
# processes race on a shared lock:
#   - "index.lock"           : git add / git commit race on .git/index.lock
#   - "another git process"  : older git wording for the same race
#   - "cannot lock ref"      : commit race on HEAD ref update (one
#                              process advanced HEAD between the loser's
#                              ref read and ref write)
#   - "reference already exists" : ref-lock race variant
_GIT_LOCK_ERROR_FRAGMENTS = (
    "index.lock",
    "another git process",
    "cannot lock ref",
    "reference already exists",
)


def _git_with_lock_retry(*args: str) -> subprocess.CompletedProcess:
    """Run a git command, retrying on transient parallel-git contention.

    Multiple parallel runner processes can race on git's locks when
    their fires finish simultaneously. The losing process gets one of
    the `_GIT_LOCK_ERROR_FRAGMENTS` patterns. Retry with exponential
    backoff (capped at the configured count) so transient contention
    doesn't drop a fire's commit.

    Returns the final CompletedProcess (success, non-lock error, or
    final attempt after retries exhausted).
    """
    delay = _GIT_LOCK_RETRY_INITIAL_DELAY
    for attempt in range(_GIT_LOCK_RETRY_COUNT):
        result = _git(*args)
        if result.returncode == 0:
            return result
        stderr_lower = (result.stderr or "").lower()
        if not any(frag in stderr_lower for frag in _GIT_LOCK_ERROR_FRAGMENTS):
            return result  # non-lock error; let caller see it
        if attempt < _GIT_LOCK_RETRY_COUNT - 1:
            time.sleep(delay)
            delay *= 2
    return result


def _is_dirty() -> bool:
    """True iff `_docuverse/` has any pending changes.

    Scoped strictly to substrate citizens — the auto-commit is for
    fire emissions, not for unrelated working-tree state (code
    edits, prompts, scripts in flight). Operator-side changes
    outside `_docuverse/` are the operator's to commit, never the
    runner's.
    """
    return bool(
        _git("status", "--porcelain", "--", "_docuverse/")
        .stdout.strip()
    )


_NOISE_TYPES_CACHE: set[str] | None = None


def _noise_type_addrs() -> set[str]:
    """Type addresses whose presence alone counts as commit-skippable noise.

    Holding/retraction pairs are mutex coordination, not content. A fire
    that emits only these has done no semantically-meaningful work
    (cf. docs/design-notes/stigmergic-coordination.md).
    """
    global _NOISE_TYPES_CACHE
    if _NOISE_TYPES_CACHE is None:
        paths_data = json.loads(
            (WORKSPACE / "_docuverse" / "paths.json").read_text()
        )
        registry_doc = Address(paths_data["_meta"]["registry_doc"])
        registry = TypeRegistry(registry_doc)
        _NOISE_TYPES_CACHE = {
            str(registry.address_for("holding")),
            str(registry.address_for("retraction")),
        }
    return _NOISE_TYPES_CACHE


def _is_noise_only_delta() -> bool:
    """True iff the only working-tree change is mutex-only emissions
    (holding + retraction) appended to `_docuverse/links.jsonl`.

    A fire that produces this delta has done its mutex coordination but
    no real content emission; committing would clutter the history with
    an empty checkpoint. We let the noise accumulate uncommitted; the
    next real-work fire's commit sweeps it up.
    """
    other = _git(
        "status", "--porcelain", "--", f":!{_LINKS_JSONL}",
    ).stdout.strip()
    if other:
        return False
    head_dump = _git("show", f"HEAD:{_LINKS_JSONL}")
    if head_dump.returncode != 0:
        # No HEAD version yet (very first commit) — treat as non-noise.
        return False
    head_count = len(head_dump.stdout.splitlines())
    cur_path = WORKSPACE / _LINKS_JSONL
    if not cur_path.exists():
        return False
    cur_lines = cur_path.read_text().splitlines()
    new_lines = cur_lines[head_count:]
    if not new_lines:
        return False
    noise = _noise_type_addrs()
    for line in new_lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return False
        type_set = data.get("type_set", [])
        if not type_set:
            return False
        if not all(t in noise for t in type_set):
            return False
    return True


def _stage_dirty(paths=None) -> None:
    """Stage every modified + untracked file under the given path(s).

    Strictly scoped to substrate citizens. No `git add -u` (which
    would sweep tracked changes anywhere in the repo). Anything
    outside the explicit paths is the operator's responsibility —
    auto-commit must not silently fold unrelated edits into a fire's
    commit.

    `paths=None` (default) sweeps all of `_docuverse/` (legacy
    behavior; dirty under parallel runners). When the trigger declares
    `commit_paths`, the runner passes the per-fire content paths plus
    substrate metadata, and only those land in the commit.

    Uses `_git_with_lock_retry` so concurrent runners don't lose
    their stage on `.git/index.lock` contention.
    """
    if paths is None:
        _git_with_lock_retry("add", "_docuverse/")
        return
    for p in paths:
        # Skip non-existent paths silently — a fire may not produce
        # every declared path on every invocation.
        from pathlib import Path
        if Path(p).exists():
            _git_with_lock_retry("add", p)


def _draft_message(trigger_name: str, addr: str) -> str:
    """Ask Sonnet for a descriptive commit message based on the staged
    diff. Multi-line: subject + body. Reads the actual change rather
    than relying only on trigger name."""
    stat = _git("diff", "--cached", "--stat").stdout
    raw_diff = _git("diff", "--cached").stdout
    truncated = len(raw_diff) > _MAX_DIFF_CHARS
    diff = raw_diff[:_MAX_DIFF_CHARS]
    if truncated:
        diff += f"\n\n[... diff truncated at {_MAX_DIFF_CHARS} chars; "
        diff += f"full diff was {len(raw_diff)} chars]"

    prompt = (
        f"Write a git commit message describing this agent fire's "
        f"effect on the substrate.\n\n"
        f"Trigger: {trigger_name}\n"
        f"Fire target: {addr}\n\n"
        f"Files changed (--stat):\n{stat}\n"
        f"Staged diff:\n{diff}\n\n"
        f"Format:\n"
        f"  <type>(<scope>): <subject line, ≤72 chars>\n"
        f"\n"
        f"  <body — 1-3 short paragraphs describing what changed and why,\n"
        f"  drawn from the diff itself rather than the trigger name. Skip\n"
        f"  the body for trivial cascade emissions (single anchor refresh,\n"
        f"  pure mutex pairs).>\n\n"
        f"Type vocabulary:\n"
        f"  - cascade   — downstream artifact refreshed in response to an\n"
        f"                upstream change (description, signature,\n"
        f"                aggregate, freshness anchor, etc.).\n"
        f"  - revise    — agent edited a claim or note body to address\n"
        f"                review findings.\n"
        f"  - refresh   — sidecar or aggregate rebuilt without semantic\n"
        f"                change.\n"
        f"  - audit     — structural review emitted findings.\n"
        f"  - review    — content review (full/cone) emitted findings.\n"
        f"  - fix       — corrected a substrate error.\n"
        f"  - decompose — note → per-claim derivation.\n"
        f"  - patch     — operator-driven patch applied.\n\n"
        f"Scope vocabulary:\n"
        f"  - `asn-NN/<claim-label>` when the change targets one claim\n"
        f"    (e.g., `asn-34/T10a.8`).\n"
        f"  - `asn-NN` when ASN-wide (e.g., `asn-36`).\n"
        f"  - `<doc-type>/asn-NN` for cross-cutting docs\n"
        f"    (e.g., `aggregate/asn-34`, `review/asn-36`).\n\n"
        f"Constraints:\n"
        f"  - Read the diff. Describe what actually changed, not what the\n"
        f"    trigger is named.\n"
        f"  - First line ≤72 chars, no trailing period.\n"
        f"  - Plain text only — no preamble, no markdown fences, no\n"
        f"    meta-commentary about the message itself.\n"
        f"  - Output only the message, nothing else."
    )
    result = invoke_claude(
        prompt, model="sonnet", effort="high", output_format=None,
    )
    text = (result.text or "").strip()
    if not text:
        return f"{trigger_name}: fired on {addr}"
    return text


def _flush_pending_jsonl() -> int:
    """Move this worker's pending substrate emissions into canonical.

    Acquires the substrate write lock (the same flock-style lock used
    by `register_path`), appends pending → canonical, truncates
    pending. No-op when there's no pending file (non-runner context,
    or pending file empty).

    Returns the number of jsonl lines flushed.

    Mirrors `Store.flush_pending` but runs without opening a Store
    handle — `commit_after_fire` runs between sessions, and a flush
    only needs file operations + the lock.
    """
    import os, fcntl
    worker_idx_raw = os.environ.get("CLAUDE_WORKER_INDEX")
    if worker_idx_raw is None or worker_idx_raw == "":
        return 0
    try:
        worker_idx = int(worker_idx_raw)
    except ValueError:
        return 0
    pending = worker_pending_jsonl(worker_idx)
    if pending is None or not pending.exists() or pending.stat().st_size == 0:
        return 0
    canonical = WORKSPACE / "_docuverse" / "links.jsonl"
    docuverse = WORKSPACE / "_docuverse"
    lock_path = docuverse / ".register_path.lock"
    fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        # Re-check size under lock.
        if not pending.exists() or pending.stat().st_size == 0:
            return 0
        with open(pending) as src:
            content = src.read()
        flushed = sum(1 for line in content.splitlines() if line.strip())
        with open(canonical, "a") as dst:
            dst.write(content)
        # Truncate pending.
        open(pending, "w").close()
        return flushed
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def commit_after_fire(
    trigger_name: str,
    addr: str,
    commit_paths=None,
) -> None:
    """Stage + commit any working-tree changes from one agent fire.

    `commit_paths` (optional list of repo-relative paths) restricts
    staging to those paths plus substrate metadata. None means
    sweep-all (legacy fallback). Substrate metadata
    (`_docuverse/links.jsonl` + `_docuverse/paths.json`) is always
    included when `commit_paths` is non-None — those are append-
    only / snapshot files that need to commit alongside content.

    No-op when the tree is clean. Errors from git or the LLM call are
    swallowed with a stderr note; the runner continues. Stale dirt is
    swept up by the next successful fire's commit.
    """
    # Flush this worker's per-worker substrate buffer into canonical
    # FIRST. Emissions during the fire went to `_workspace/links.
    # worker-N.jsonl`; flush appends them to canonical under a brief
    # substrate lock. Without this, the dirty-check below would
    # report clean (pending file is gitignored) and nothing would
    # commit.
    try:
        _flush_pending_jsonl()
    except Exception as exc:
        print(
            f"  [AUTO-COMMIT] pending flush failed on {trigger_name}/{addr}: "
            f"{exc!r}",
            file=sys.stderr,
        )

    try:
        if not _is_dirty():
            return
        if _is_noise_only_delta():
            return
        if commit_paths is not None:
            # Always include substrate metadata alongside per-fire content.
            scope_paths = list(commit_paths) + [
                "_docuverse/links.jsonl",
                "_docuverse/paths.json",
            ]
        else:
            scope_paths = ["_docuverse/"]
        _stage_dirty(scope_paths if commit_paths is not None else None)
        if not _git("diff", "--cached", "--name-only").stdout.strip():
            # Nothing actually got staged (e.g., changes were under
            # paths we deliberately don't auto-add).
            return
        msg = _draft_message(trigger_name, addr)
        # Path-scope the commit too. `git commit -m msg` (no paths)
        # commits ALL staged work, which sweeps any operator-staged
        # files outside the runner's scope into the auto-message.
        # Explicit `-- <paths>` restricts the commit to scope.
        commit = _git_with_lock_retry("commit", "-m", msg, "--", *scope_paths)
        if commit.returncode != 0:
            print(
                f"  [AUTO-COMMIT] commit failed: {commit.stderr.strip()[:200]}",
                file=sys.stderr,
            )
    except Exception as exc:
        print(
            f"  [AUTO-COMMIT] skipped on {trigger_name}/{addr}: {exc!r}",
            file=sys.stderr,
        )
