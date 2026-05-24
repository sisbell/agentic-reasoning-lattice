"""Note-patch producer — apply a targeted patch to an ASN note.

Operator-gated producer. One fire = promote a workspace patch md to a
substrate-citizen `patch` doc, apply the patch via LLM, run a one-shot
patch-scoped review that emits findings as first-class substrate
citizens, re-export, commit.

The agent does NOT drive convergence itself. The patch-scoped review
emits open `comment.revise` findings as substrate; the standard
`note_revise` trigger picks them up the next time the runner walks.
Operator drives convergence afterward via `scripts/run-trigger.py`
on the relevant note triggers (`note_review`, `note_consult`,
`note_revise`); under a running daemon convergence happens
automatically.

Caste: producer. Identity grants per fire:

  - `patch.note` classifier on the patch doc (workspace → substrate
    promotion)
  - `provenance.derivation(F=[patch], G=[note])` audit edge
  - `review` classifier on the patch-scoped review doc
  - `review.coverage(review → note)`
  - `provenance.derivation(F=[patch], G=[review])` to tie the
    patch-scoped review back to the patch fire
  - `finding` classifier + `comment.revise` per finding
  - `provenance.derivation(review → finding)` per finding (via
    record_one_finding)

Operator workflow:

  1. Drop a patch md into `_workspace/patches/note/<ASN-NNNN>/<filename>.md`
     (gitignored input drop).
  2. Run `python scripts/note-patch.py <asn> --patch <filename>`.
  3. Drive note-side convergence on the patch reviewer's findings
     by invoking `note_review`, `note_consult`, `note_revise` via
     `scripts/run-trigger.py NAME <asn>` (or wait for the daemon).

Why one-shot review (no inner loop): the patch-scoped reviewer's
job is to focus the LLM on the change and surface narrow findings.
Convergence is the standard runner walk's job. Avoiding the inner
loop keeps the agent simple and unifies convergence machinery.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.note_review import extract_note_findings
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_derivation, emit_patch_note, emit_review, emit_review_content,
    emit_review_coverage,
)
from lib.shared.prompts import read_prompt
from lib.lattice.findings import record_one_finding
from lib.lattice.labels import extract_label_digits, format_label
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.foundation import FoundationError, load_foundation
from lib.shared.invoke_claude import invoke_claude, invoke_claude_agent
from lib.shared.paths import (
    LATTICE, NOTE_FINDINGS_DIR, NOTE_REVIEWS_DIR,
    PATCH_INBOX_NOTE, PATCH_NOTE_DIR,
    WORKSPACE, next_review_number, prompt_path,
)


PATCH_MODEL = "opus"
PATCH_EFFORT = "max"

APPLY_TEMPLATE = prompt_path("agents/producers/note_patch/apply.md")
REVIEW_TEMPLATE = prompt_path("agents/producers/note_patch/review.md")


# ─── Patch promotion (workspace → substrate) ────────────────────────


def _promote_patch_to_substrate(
    session: Session,
    note_addr: Address,
    asn_label: str,
    patch_filename: str,
):
    """Copy the workspace patch md into the substrate doc tree, register
    its path, emit `patch` classifier + `provenance.derivation` from
    patch → note. Returns (substrate_path, patch_addr), or None if the
    workspace patch is missing.
    """
    workspace_path = PATCH_INBOX_NOTE / asn_label / patch_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    substrate_dir = PATCH_NOTE_DIR / asn_label
    substrate_dir.mkdir(parents=True, exist_ok=True)
    substrate_path = substrate_dir / patch_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(
        substrate_path.resolve().relative_to(WORKSPACE.resolve())
    )
    patch_addr = session.store.register_path(substrate_rel)

    emit_patch_note(session.store, patch_addr)
    emit_derivation(session.store, patch_addr, note_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, patch_addr


# ─── LLM steps ──────────────────────────────────────────────────────


def _apply_patch(
    asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str,
) -> bool:
    """Apply patch to the ASN note via LLM with Edit tools."""
    template = read_prompt(APPLY_TEMPLATE)
    if not template:
        print("  [ERROR] Apply prompt template not found", file=sys.stderr)
        return False

    prompt = (
        template
        .replace("{{patch_content}}", patch_content)
        .replace("{{asn_path}}", str(asn_path))
    )
    print(f"  [PATCH] Applying to {asn_label}...", file=sys.stderr)
    response = invoke_claude_agent(
        prompt, model=model, effort=effort,
        tools="Read,Edit,Grep", max_turns=15,
    )
    if response.data is None:
        print(f"  [ERROR] Patch application failed", file=sys.stderr)
        return False
    print(f"  [APPLIED] {asn_label}", file=sys.stderr)
    return True


def _patch_scoped_review(
    asn_num: int, asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str,
) -> str | None:
    """One-shot patch-scoped review. Returns review text, or None on
    LLM failure."""
    asn_content = asn_path.read_text()
    vocabulary = read_file(resolve_campaign(asn_num).vocabulary_path)
    try:
        foundation = load_foundation(asn_num)
    except FoundationError as e:
        print(
            f"  [FOUNDATION] {asn_label}: {e}",
            file=sys.stderr,
        )
        return None

    template = read_prompt(REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Review prompt template not found", file=sys.stderr)
        return None

    prompt = (
        template
        .replace("{{asn_content}}", asn_content)
        .replace("{{patch_content}}", patch_content)
        .replace("{{vocabulary}}", vocabulary)
        .replace("{{foundation_statements}}", foundation)
    )

    print(f"  [REVIEW] Patch-scoped review of {asn_label}...", file=sys.stderr)
    result = invoke_claude(prompt, model=model, effort=effort)
    if not result.text:
        print(f"  [WARN] Patch review produced no output", file=sys.stderr)
        return None
    log_usage("patch-review", result.elapsed, asn=asn_num)
    return result.text


# ─── Substrate emission for the review + findings ───────────────────


def _emit_review_with_findings(
    session: Session,
    asn_label: str,
    note_addr: Address,
    patch_addr: Address,
    review_text: str,
):
    """Persist patch-scoped review + emit review classifier + coverage +
    per-finding decomposition. Same shape as the standard note_review
    producer, plus an extra provenance.derivation(patch → review) edge
    so the audit trail ties the review back to the patch fire.

    Returns (review_addr, n_findings).
    """
    next_n = next_review_number(asn_label, kind="note")
    review_dir = NOTE_REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"review-{next_n}.md"
    body = review_text + "\n"

    review_rel = str(review_path.relative_to(session.store.lattice_dir))
    session.update_document(review_rel, body)
    review_addr = session.register_path(review_rel)
    emit_review(session.store, review_addr)
    emit_review_content(session.store, review_addr)
    emit_review_coverage(session.store, review_addr, note_addr)
    emit_derivation(session.store, patch_addr, review_addr)

    findings = extract_note_findings(review_text)
    findings_root = NOTE_FINDINGS_DIR / asn_label / f"review-{next_n}"
    for n, (_title, cls, fbody) in enumerate(findings):
        finding_rel = str(
            (findings_root / f"{n}.md").relative_to(session.store.lattice_dir)
        )
        comment_kind = (
            "out-of-scope" if (cls or "REVISE").upper() == "OUT_OF_SCOPE"
            else "revise"
        )
        record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=fbody,
            target_addr=note_addr,
            review_addr=review_addr,
            comment_kind=comment_kind,
        )

    revise_count = sum(
        1 for _, c, _ in findings if (c or "").upper() == "REVISE"
    )
    oos_count = len(findings) - revise_count
    print(
        f"  [REVIEW] {asn_label} {review_path.name} — "
        f"{revise_count} REVISE, {oos_count} OUT_OF_SCOPE",
        file=sys.stderr,
    )
    return review_addr, len(findings)


# ─── Re-export ──────────────────────────────────────────────────────


def _re_export(asn_num: int, asn_label: str) -> None:
    """Subprocess to existing note-assembly.py until that's also lifted."""
    print(f"  [EXPORT] Re-exporting {asn_label}...", file=sys.stderr)
    cmd = [
        sys.executable,
        str(WORKSPACE / "scripts" / "note-assembly.py"),
        str(asn_num),
    ]
    subprocess.run(cmd, capture_output=False, text=True, cwd=str(WORKSPACE))


# ─── Agent class ────────────────────────────────────────────────────


class NotePatchAgent(Agent):
    """One patch application per fire.

    Pure producer (operator-gated). Emits substrate identity for the
    patch + a patch-scoped review with proper findings. The standard
    note_revise trigger picks up the open comment.revise findings the
    next time the runner walks; the agent itself does NOT drive
    convergence.
    """

    role: ClassVar[str] = "note-patch"

    def __init__(
        self, *,
        model: str = PATCH_MODEL,
        effort: str = PATCH_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, note_addr: Address,
        *, patch_filename: str,
    ) -> AgentResult:
        # 1. Resolve note path
        note_rel = session.get_path_for_addr(note_addr)
        if note_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path_full = WORKSPACE / note_rel
        if not asn_path_full.exists():
            return AgentResult(success=False, detail="no-note-file")

        digits = extract_label_digits(note_rel)
        if digits is None:
            return AgentResult(success=False, detail="unparseable-note-path")
        asn_num = int(digits)
        asn_label = format_label(asn_num)
        asn_path, _ = find_asn(str(asn_num))
        if asn_path is None:
            return AgentResult(success=False, detail="find_asn-failed")

        os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

        # 2. Promote workspace patch → substrate
        promotion = _promote_patch_to_substrate(
            session, note_addr, asn_label, patch_filename,
        )
        if promotion is None:
            return AgentResult(success=False, detail="patch-not-in-workspace")
        substrate_path, patch_addr = promotion
        patch_content = substrate_path.read_text()

        # 3. Apply the patch
        ok = _apply_patch(
            asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
        )
        if not ok:
            return AgentResult(success=False, detail="apply-failed")
        # Body was edited; advance the note's supersession chain so
        # downstream cascade-fresh predicates detect the edit.
        session.register_version(note_addr)
        log_usage("patch-apply", 0, asn=asn_num)

        # 4. One-shot patch-scoped review (emits review + findings as
        #    first-class substrate so note_revise picks them up).
        review_text = _patch_scoped_review(
            asn_num, asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
        )
        if review_text is None:
            return AgentResult(success=False, detail="review-failed")

        review_addr, n_findings = _emit_review_with_findings(
            session, asn_label, note_addr, patch_addr, review_text,
        )

        # 5. Re-export
        _re_export(asn_num, asn_label)

        # 6. Final commit
        log_usage("patch-complete", 0, asn=asn_num)

        return AgentResult(
            success=True,
            detail=(
                f"patch={patch_filename} review={review_addr} "
                f"findings={n_findings}"
            ),
        )
