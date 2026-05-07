"""Note-patch producer — apply a targeted patch to an ASN note.

Operator-gated composite producer. One fire = promote a workspace
patch md to a substrate-citizen `patch` doc, apply the patch via LLM,
drive patch-scoped review/revise cycles to convergence, re-export the
note, commit.

Caste: producer. Identity grant: the patch doc gets a `patch`
classifier + `provenance.derivation(F=[patch], G=[note])` audit edge.
The note md is edited and its supersession chain advances via
register_version.

Operator workflow:

  1. Drop a patch md into `_workspace/patches/<ASN-NNNN>/<filename>.md`
     (gitignored; operator's input drop).
  2. Run `python scripts/note-patch.py <asn> --patch <filename>`.
  3. Agent promotes the patch to substrate, applies it, drives
     review/revise to convergence, re-exports, commits.

The inner review/revise loop uses patch-specific prompts
(`prompts/shared/discovery/patch/{review,revise}.md`) — narrower
scope than the standard note_review/note_revise convergence walk.
The patch-specific reviewer sees the patch content and reviews ONLY
the changed material + downstream effects, avoiding scope creep
onto unaffected parts of the ASN.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_derivation, emit_patch
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.foundation import load_foundation_for_note
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import invoke_claude, invoke_claude_agent
from lib.shared.paths import (
    LATTICE, NOTE_REVIEWS_DIR, PATCH_DIR, PATCH_INBOX, WORKSPACE,
    next_review_number, prompt_path,
)


PATCH_MODEL = "opus"
PATCH_EFFORT = "max"
MAX_CYCLES = 10

APPLY_TEMPLATE = prompt_path("discovery/patch/apply.md")
REVIEW_TEMPLATE = prompt_path("discovery/patch/review.md")
REVISE_TEMPLATE = prompt_path("discovery/patch/revise.md")


# ─── Inner LLM helpers (apply / review / revise) ────────────────────


def _apply_patch(asn_path: Path, asn_label: str, patch_content: str,
                 *, model: str, effort: str) -> bool:
    """Step 1 — apply patch to the ASN via LLM with Edit tools."""
    template = read_file(APPLY_TEMPLATE)
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


def _review_patch(
    asn_num: int, asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str,
) -> Optional[str]:
    """Step 2a — patch-scoped review. Returns "CONVERGED" or review text,
    or None on LLM failure."""
    asn_content = asn_path.read_text()
    vocabulary = read_file(resolve_campaign(asn_num).vocabulary_path)
    foundation = load_foundation_for_note(asn_path, asn_num)

    template = read_file(REVIEW_TEMPLATE)
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

    print(f"  [REVIEW] Patch review of {asn_label}...", file=sys.stderr)
    result = invoke_claude(prompt, model=model, effort=effort)
    if not result.text:
        print(f"  [WARN] Patch review produced no output", file=sys.stderr)
        return None

    log_usage("patch-review", result.elapsed, asn=asn_num)

    # Persist review for audit; mirror existing flow's location.
    review_dir = NOTE_REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label, kind="note")
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(result.text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if "VERDICT: CONVERGED" in result.text:
        print(f"  [CONVERGED] Patch is clean", file=sys.stderr)
        return "CONVERGED"
    print(f"  [REVISE] Patch issues found", file=sys.stderr)
    return result.text


def _revise_patch(
    asn_num: int, asn_path: Path, asn_label: str, patch_content: str,
    review_text: str, *, model: str, effort: str,
) -> bool:
    """Step 2b — fix patch-scoped issues via LLM with Edit tools."""
    vocabulary = read_file(resolve_campaign(asn_num).vocabulary_path)
    foundation = load_foundation_for_note(asn_path, asn_num)

    template = read_file(REVISE_TEMPLATE)
    if not template:
        print("  [ERROR] Revise prompt template not found", file=sys.stderr)
        return False

    prompt = (
        template
        .replace("{{vocabulary}}", vocabulary)
        .replace("{{foundation_statements}}", foundation)
        .replace("{{asn_path}}", str(asn_path))
        .replace("{{patch_content}}", patch_content)
        .replace("{{review_content}}", review_text)
    )

    print(f"  [REVISE] Fixing patch issues in {asn_label}...", file=sys.stderr)
    response = invoke_claude_agent(
        prompt, model=model, effort=effort,
        tools="Read,Edit,Grep", max_turns=15,
    )
    if response.data is None:
        print(f"  [WARN] Patch revise failed", file=sys.stderr)
        return False
    log_usage("patch-revise", response.elapsed, asn=asn_num)
    return True


def _drive_review_revise(
    asn_num: int, asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str, max_cycles: int,
) -> bool:
    """Step 2 — patch-scoped review/revise convergence loop. Returns True
    on convergence, False on failure or max-cycles exhausted."""
    for cycle in range(1, max_cycles + 1):
        print(
            f"\n  --- Patch review cycle {cycle}/{max_cycles} ---",
            file=sys.stderr,
        )

        result = _review_patch(
            asn_num, asn_path, asn_label, patch_content,
            model=model, effort=effort,
        )
        if result is None:
            print(f"  [WARN] Review failed, retrying once...", file=sys.stderr)
            result = _review_patch(
                asn_num, asn_path, asn_label, patch_content,
                model=model, effort=effort,
            )
            if result is None:
                print(f"  [WARN] Review failed again, stopping", file=sys.stderr)
                return False

        if result == "CONVERGED":
            return True

        ok = _revise_patch(
            asn_num, asn_path, asn_label, patch_content, result,
            model=model, effort=effort,
        )
        if not ok:
            print(f"  [WARN] Revise failed at cycle {cycle}", file=sys.stderr)
            return False

        step_commit_asn(
            asn_num, f"patch(asn): {asn_label} patch revise cycle {cycle}",
        )

    print(
        f"  [WARN] Did not converge after {max_cycles} cycles",
        file=sys.stderr,
    )
    return False


def _re_export(asn_num: int, asn_label: str) -> None:
    """Step 3 — re-export note assembly. Subprocess to existing
    note-assembly.py until that's also lifted."""
    print(f"  [EXPORT] Re-exporting {asn_label}...", file=sys.stderr)
    cmd = [
        sys.executable,
        str(WORKSPACE / "scripts" / "note-assembly.py"),
        str(asn_num),
    ]
    subprocess.run(cmd, capture_output=False, text=True, cwd=str(WORKSPACE))


# ─── Patch promotion (workspace → substrate) ────────────────────────


def _promote_patch_to_substrate(
    session: Session,
    note_addr: Address,
    asn_label: str,
    patch_filename: str,
) -> tuple[Path, Address] | None:
    """Copy the workspace patch md into the substrate doc tree, register
    its path, emit the `patch` classifier + provenance.derivation
    edge from patch → note. Returns (substrate_path, patch_addr), or
    None if the workspace patch is missing.
    """
    workspace_path = PATCH_INBOX / asn_label / patch_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    substrate_dir = PATCH_DIR / asn_label
    substrate_dir.mkdir(parents=True, exist_ok=True)
    substrate_path = substrate_dir / patch_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(
        substrate_path.resolve().relative_to(LATTICE.resolve())
    )
    patch_addr = session.store.register_path(substrate_rel)

    emit_patch(session.store, patch_addr)
    emit_derivation(session.store, patch_addr, note_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(LATTICE)}",
        file=sys.stderr,
    )
    return substrate_path, patch_addr


# ─── Agent class ────────────────────────────────────────────────────


class NotePatchAgent(Agent):
    """One patch application per fire.

    Composite producer. Operator-gated outer fire (operator decides
    when to apply a patch); internal review/revise loop drives the
    patched ASN to convergence using patch-scoped prompts.
    """

    role: ClassVar[str] = "note-patch"

    def __init__(
        self, *,
        model: str = PATCH_MODEL,
        effort: str = PATCH_EFFORT,
        max_cycles: int = MAX_CYCLES,
    ):
        self.model = model
        self.effort = effort
        self.max_cycles = max_cycles

    def run(
        self, session: Session, note_addr: Address,
        *, patch_filename: str,
    ) -> AgentResult:
        # 1. Resolve note path
        note_rel = session.get_path_for_addr(note_addr)
        if note_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path_full = LATTICE / note_rel
        if not asn_path_full.exists():
            return AgentResult(success=False, detail="no-note-file")

        asn_path, asn_label = find_asn_from_path(note_rel)
        if asn_path is None:
            return AgentResult(success=False, detail="unparseable-note-path")
        asn_num = int(asn_label.split("-")[1])

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
        log_usage("patch-apply", 0, asn=asn_num)
        step_commit_asn(asn_num, f"patch(asn): {asn_label} apply {patch_filename}")

        # 4. Note md was edited — advance the chain so downstream
        #    sidecars know the source moved.
        session.register_version(note_addr)

        # 5. Patch-scoped review/revise convergence
        converged = _drive_review_revise(
            asn_num, asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
            max_cycles=self.max_cycles,
        )

        # 6. Re-export
        _re_export(asn_num, asn_label)

        # 7. Final commit + return
        log_usage("patch-complete", 0, asn=asn_num)
        step_commit_asn(asn_num, f"patch(asn): {asn_label} complete {patch_filename}")

        return AgentResult(
            success=converged,
            detail=(
                f"converged={converged} patch={patch_filename} "
                f"patch_addr={patch_addr}"
            ),
        )


def find_asn_from_path(note_rel: str) -> tuple[Optional[Path], Optional[str]]:
    """Resolve note's ASN path + label from the relative substrate path.

    The substrate path is `_docuverse/documents/note/<ASN-NNNN>-<title>.md`
    or similar. Use the existing find_asn helper which keys on the ASN
    number.
    """
    import re
    m = re.search(r"(ASN-(\d{4}))", note_rel)
    if m is None:
        return None, None
    asn_num = int(m.group(2))
    return find_asn(str(asn_num))
