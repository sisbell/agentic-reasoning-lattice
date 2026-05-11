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
from pathlib import Path

from lib.backend.addressing import Address
from lib.backend.types import TypeRegistry
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import WORKSPACE


_MAX_DIFF_CHARS = 30000
_LINKS_JSONL = "_docuverse/links.jsonl"


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )


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


def _stage_dirty() -> None:
    """Stage every modified + untracked file under `_docuverse/`.

    Strictly scoped to substrate citizens. No `git add -u` (which
    would sweep tracked changes anywhere in the repo). Anything
    outside `_docuverse/` is the operator's responsibility — auto-
    commit must not silently fold unrelated edits into a fire's
    commit.
    """
    _git("add", "_docuverse/")


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


def commit_after_fire(trigger_name: str, addr: str) -> None:
    """Stage + commit any working-tree changes from one agent fire.

    No-op when the tree is clean. Errors from git or the LLM call are
    swallowed with a stderr note; the runner continues. Stale dirt is
    swept up by the next successful fire's commit.
    """
    try:
        if not _is_dirty():
            return
        if _is_noise_only_delta():
            return
        _stage_dirty()
        if not _git("diff", "--cached", "--name-only").stdout.strip():
            # Nothing actually got staged (e.g., changes were under
            # paths we deliberately don't auto-add).
            return
        msg = _draft_message(trigger_name, addr)
        commit = _git("commit", "-m", msg)
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
