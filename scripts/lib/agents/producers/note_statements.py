"""Note-statements agent — one LLM call per fire to extract a note's
formal-statements artifact.

Fires when the note is `is_claim_confirmed` (per the N+1 refinement
pattern: no open revises AND latest review came up clean) AND the
statements sidecar's freshness anchor doesn't point at the note's
current head. On each fire:

  1. Read the source note's md content.
  2. LLM produces a structured formal-statements list (per
     produce-statements.md prompt). Existing extracted text is also
     supplied so the LLM can return it verbatim if still accurate.
  3. Persist as the note's `statements` attribute sidecar via
     attest_against_doc_head: chain advance + emit citation.depends
     from new sidecar version to version_head(note). The predicate
     walks that anchor.

The new sidecar version's anchor cites the note's current head, so
the predicate flips True until the next note advance.
"""

from __future__ import annotations

import json
import re
import sys
import time
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.attributes import attest_against_doc_head
from lib.lattice.config import lattice_config
from lib.lattice.labels import (
    extract_label_digits,
    format_label,
    label_pattern,
)
from lib.predicates import statements_sidecar_of
from lib.protocols.febe.protocol import Session
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import USAGE_LOG, prompt_path


STATEMENTS_MODEL = "sonnet"
STATEMENTS_TEMPLATE = prompt_path("agents/producers/note_statements.md")


def _strip_preamble(text: str) -> str:
    """Strip any preamble before the statements header line."""
    marker = re.search(rf"^# {label_pattern().pattern}", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def _add_source_line(text: str, note_path_name: str, asn_content: str) -> str:
    """Insert the *Source: ... — Extracted: ...* metadata line after
    the title, mirroring the legacy note-assembly output."""
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", asn_content)
    all_dates = re.findall(
        r"\d{4}-\d{2}-\d{2}",
        date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    source_line = (
        f"\n*Source: {note_path_name} (revised {asn_date}) — "
        f"Extracted: {time.strftime('%Y-%m-%d')}*\n"
    )
    lines = text.split("\n", 1)
    if len(lines) == 2:
        return lines[0] + "\n" + source_line + lines[1]
    return text + "\n" + source_line


def _log_usage(asn_label: str, elapsed: float) -> None:
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "note-statements",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


class NoteStatementsAgent(Agent):
    """One LLM extraction per fire to refresh the note's statements
    sidecar."""

    role: ClassVar[str] = "note-statements"

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_path = session.get_path_for_addr(note_addr)
        if note_path is None:
            return AgentResult(success=False, detail="no-note-path")

        full_note = session.store.lattice_dir / note_path
        if not full_note.exists():
            return AgentResult(success=False, detail="no-note-file")

        asn_content = full_note.read_text()
        asn_label = self._asn_label_from_path(note_path)
        sidecar_addr = statements_sidecar_of(session, note_addr)
        existing_text = self._read_sidecar_text(session, sidecar_addr)

        # LLM call
        prompt = self._build_prompt(asn_content, existing_text)
        print(
            f"  [NOTE-STATEMENTS] {asn_label} "
            f"(prompt {len(prompt) // 1024}KB)",
            file=sys.stderr,
        )
        result = invoke_claude(
            prompt, model=STATEMENTS_MODEL, effort="high",
        )
        if not result.text:
            return AgentResult(success=False, detail="llm-failed")

        body = _strip_preamble(result.text)
        body = _add_source_line(body, full_note.name, asn_content)
        if not body.endswith("\n"):
            body += "\n"

        # attest_against_doc_head: chain advance + freshness anchor.
        # content_changed comes from byte-comparison (LLM returns text
        # without an explicit no-change verdict). True on first
        # emission and on real edits; False only when the LLM produced
        # byte-identical output.
        content_changed = (
            existing_text is None or body.strip() != existing_text
        )
        attest_against_doc_head(
            session, note_path, "statements", body, note_addr,
            content_changed=content_changed,
        )

        _log_usage(asn_label, result.elapsed)
        print(
            f"  [NOTE-STATEMENTS] {asn_label} done ({elapsed:.0f}s)",
            file=sys.stderr,
        )
        return AgentResult(success=True, detail="emitted")

    def _build_prompt(
        self, asn_content: str, existing: Optional[str],
    ) -> str:
        """Render the produce-statements prompt with optional existing-
        extraction context."""
        template = STATEMENTS_TEMPLATE.read_text()
        return template.replace("{{asn_content}}", asn_content)

    def _read_sidecar_text(
        self, session: Session, sidecar_addr: Optional[Address],
    ) -> Optional[str]:
        """Read the statements sidecar's file content, or None if
        unresolvable."""
        if sidecar_addr is None:
            return None
        sidecar_path = session.get_path_for_addr(sidecar_addr)
        if sidecar_path is None:
            return None
        full = session.store.lattice_dir / sidecar_path
        if not full.exists():
            return None
        return full.read_text().strip() or None

    def _asn_label_from_path(self, path: str) -> str:
        digits = extract_label_digits(path)
        if digits:
            return format_label(int(digits))
        return f"{lattice_config().label_prefix}-????"
