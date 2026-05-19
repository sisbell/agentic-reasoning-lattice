"""Note-revise agent — invoke Claude with editing tools to address open
revise findings on a note.

`NoteReviseAgent` is the class-form entry point the trigger runner
invokes. One fire = collect open `comment.revise` findings on the
note, assemble a discovery-methodology prompt with per-finding
instructions, invoke Claude with Edit/Read/Bash tools. The Claude
session closes each comment via `resolution.py`
once it has addressed (or rejected) the finding.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.predicates import unresolved_revise_comments
from lib.lattice.labels import (
    extract_label_digits,
    format_label,
    label_pattern,
)
from lib.shared.prompts import read_prompt
from lib.lattice.render import read_doc
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import load_foundation_for_note
from lib.shared.invoke_claude import invoke_claude_agent
from lib.shared.paths import (
    USAGE_LOG, WORKSPACE, prompt_path, worker_pending_jsonl,
)


METHODOLOGY_PROMPT = prompt_path("agents/_shared/methodology.md")

MODEL = "claude-opus-4-7[1m]"


def build_prompt(
    asn_path: Path,
    findings: list,
    vocab: str,
    consultation_content=None,
    asn_number=None,
) -> str:
    """Build revise prompt: discovery methodology + per-finding instructions.

    `findings` is a list of (comment_id, finding_addr, title, body)
    tuples — one per open `comment.revise` link on the note. The
    finding_addr is unused here but kept on the tuple so callers can
    walk consultation.coverage off it. The agent is instructed to
    address each in the note md and call resolution.py
    per finding to close the comment in the substrate.
    """
    skill_body = read_prompt(METHODOLOGY_PROMPT)
    if not skill_body:
        print(
            f"  Discovery prompt not found at "
            f"{METHODOLOGY_PROMPT.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        sys.exit(1)

    parts = [skill_body]

    if vocab:
        parts.append(f"## Shared Vocabulary\n\n{vocab}")

    foundation = load_foundation_for_note(asn_path, asn_number)
    if foundation:
        parts.append(foundation)

    rel_path = asn_path.relative_to(WORKSPACE)
    asn_label = label_pattern().match(asn_path.stem).group(0)

    assignment = f"""## Your Assignment: REVISE {asn_label}

You are revising an existing ASN based on per-finding review feedback.
Read the ASN at `{rel_path}`, then address each finding below.

**Do not rewrite the ASN from scratch.** Make targeted fixes per finding.
Preserve the existing structure, notation, and reasoning where it is not
affected by the finding.

Write the revised ASN back to `{rel_path}`.

For each finding below, after you have addressed it (either by editing
the note or by deciding the finding is incorrect), close the
corresponding comment in the link store:

  python scripts/agent_tools/resolution.py accept --comment-id <id>
  python scripts/agent_tools/resolution.py reject --comment-id <id> --rationale "<one or two sentences>"

`accept` means you applied the fix; `reject` means the finding is
incorrect and you wrote a rationale instead. Do this once per finding."""

    if consultation_content:
        assignment += f"""

## Consultation Results

The following expert consultations were conducted based on the review.
Use these answers as evidence when addressing the corresponding findings.

{consultation_content}"""

    assignment += "\n\n## Findings\n"
    for n, (comment_id, _finding_addr, title, body) in enumerate(findings, 1):
        assignment += (
            f"\n### Finding {n}: {title}\n"
            f"**Comment ID:** `{comment_id}`\n\n"
            f"{body}\n"
        )

    parts.append(assignment)
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Trigger-runner entry: class form


def _collect_open_revises(
    session: Session, note_addr: Address,
) -> List[Tuple[Address, Address, str, str]]:
    """Return list of (comment_addr, finding_addr, title, body) for
    unresolved revise comments targeting the note. Each finding's body
    is read from its finding doc; missing finding docs are skipped with
    a stderr note.

    finding_addr is needed downstream to walk consultation.coverage
    links in `_build_consultation_content`.
    """
    items: List[Tuple[Address, Address, str, str]] = []
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        finding_rel = session.get_path_for_addr(finding_addr)
        if not finding_rel:
            continue
        try:
            body = read_doc(session, finding_addr).strip()
        except FileNotFoundError:
            print(
                f"  [SKIP] finding doc missing: {finding_rel}",
                file=sys.stderr,
            )
            continue
        first_line = body.splitlines()[0] if body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"
        items.append((c.addr, finding_addr, title, body))
    return items


def _build_consultation_content(
    session: Session,
    items: List[Tuple[Address, Address, str, str]],
) -> str | None:
    """Assemble per-finding consultation answers for the revise prompt.

    For each open revise finding, walks `consultation.coverage` links
    targeting it and reads each answer doc that has the
    `consultation.answer` classifier (the assessment doc also covers
    findings but isn't a Q/A; skipped). Returns markdown text grouped
    by finding, or None if no answers exist.

    Substrate-grounded — no filename inspection, no aggregate file.
    """
    parts: list[str] = []
    for _comment_addr, finding_addr, title, _body in items:
        coverage = session.active_links(
            "consultation.coverage", to_set=[finding_addr],
        )
        if not coverage:
            continue
        section: list[str] = []
        for link in coverage:
            if not link.from_set:
                continue
            source_addr = link.from_set[0]
            if not session.active_links(
                "consultation.answer", to_set=[source_addr],
            ):
                continue
            try:
                section.append(read_doc(session, source_addr).strip())
            except (KeyError, FileNotFoundError):
                continue
        if section:
            parts.append(f"### Finding: {title}\n")
            parts.extend(section)
            parts.append("")
    return "\n\n".join(parts).strip() or None if parts else None


def _log_revise_usage(
    asn_label: str, elapsed: float, data: dict | None,
) -> None:
    """Append a revise-usage entry to the lattice usage log."""
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": "note-revise",
        "asn": asn_label,
        "elapsed_s": round(elapsed, 1),
    }
    if data is not None:
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (
            usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
        )
        out = usage.get("output_tokens", 0)
        entry.update({
            "input_tokens": inp,
            "output_tokens": out,
            "num_turns": data.get("num_turns", 0),
            "cost_usd": cost,
        })
    try:
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


class NoteReviseAgent(Agent):
    """One Claude-with-tools invocation that addresses every open
    revise finding on a note.

    Fires when the note has unresolved `comment.revise` links (i.e.,
    `is_doc_quiescent` is False). The Claude session itself edits the
    note md and closes each comment via `resolution.py`.
    """

    role: ClassVar[str] = "note-revise"

    def __init__(self, *, model: str = "opus", effort: str = "max"):
        self.model = model
        self.effort = effort

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_path_rel = session.get_path_for_addr(note_addr)
        if note_path_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path = session.store.lattice_dir / note_path_rel
        if not asn_path.exists():
            return AgentResult(success=False, detail="no-note-file")

        digits = extract_label_digits(note_path_rel)
        if digits is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_number = int(digits)
        asn_label = format_label(asn_number)

        findings = _collect_open_revises(session, note_addr)
        if not findings:
            return AgentResult(
                success=True, detail="no-open-revises",
            )

        vocab = read_file(resolve_campaign(asn_label).vocabulary_path)
        consultation_content = _build_consultation_content(session, findings)
        prompt = build_prompt(
            asn_path, findings, vocab,
            consultation_content=consultation_content,
            asn_number=asn_number,
        )
        print(
            f"  [NOTE-REVISE] {asn_label} {len(findings)} finding(s) "
            f"(prompt {len(prompt) // 1024}KB)",
            file=sys.stderr,
        )

        os.environ["PROTOCOL_ASN_LABEL"] = asn_label
        response = invoke_claude_agent(
            prompt, model=self.model, effort=self.effort,
            tools="Edit,Bash,Write,Read,Glob,Grep",
            max_turns=None,
        )
        _log_revise_usage(asn_label, response.elapsed, response.data)
        if response.data is None:
            return AgentResult(
                success=False, elapsed=response.elapsed, detail="llm-failed",
            )

        # One register_version per fire (regardless of accept count).
        # resolution.py used to advance per accept, growing the note's
        # version chain by N per fire when N findings were closed; the
        # semantics are "one logical edit per fire," so the lifecycle
        # belongs here, not in the per-finding decision tool.
        #
        # In worker mode the LLM's tool subprocesses emit resolution.edit
        # links to _workspace/links.worker-N.jsonl (the per-worker
        # pending buffer), NOT to canonical links.jsonl. This session's
        # in-memory state was loaded from canonical at session start
        # and does not reflect pending writes, so session.active_links
        # alone returns 0 acceptances and register_version never fires.
        # Scan the pending buffer too — same pattern _reconcile_link_cursor
        # uses to coordinate across processes.
        accept_count = 0
        finding_targets = {
            str(comment_addr)
            for comment_addr, _finding, _title, _body in findings
        }
        accepted_targets = set()
        for comment_addr, _finding, _title, _body in findings:
            if session.active_links(
                "resolution.edit", to_set=[comment_addr],
            ):
                accepted_targets.add(str(comment_addr))
        worker_idx_env = os.environ.get("CLAUDE_WORKER_INDEX")
        if worker_idx_env not in (None, ""):
            pending_path = worker_pending_jsonl(int(worker_idx_env))
            if pending_path and pending_path.exists():
                res_edit_type = str(
                    session.store.state.types.address_for("resolution.edit")
                )
                with open(pending_path) as pf:
                    for line in pf:
                        line = line.rstrip("\n")
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if res_edit_type not in entry.get("type_set", []):
                            continue
                        for tgt in entry.get("to_set", []):
                            if tgt in finding_targets:
                                accepted_targets.add(tgt)
        accept_count = len(accepted_targets)
        if accept_count > 0:
            session.register_version(note_addr)

        return AgentResult(
            success=True,
            elapsed=response.elapsed,
            detail=f"addressed={len(findings)}",
        )
