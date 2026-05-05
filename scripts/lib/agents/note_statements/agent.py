"""Note-statements agent — one LLM call per fire to extract a note's
formal-statements artifact.

Fires when the note is `is_claim_confirmed` (per the N+1 convergence
pattern: no open revises AND latest review came up clean) AND the
statements supersession chain is shorter than the note's. On each
fire:

  1. Read the source note's md content.
  2. LLM produces a structured formal-statements list (per
     produce-statements.md prompt). Existing extracted text is also
     supplied so the LLM can return it verbatim if still accurate.
  3. Persist as the note's `statements` attribute sidecar:
     - First time: emit_attribute creates the link + sidecar.
     - Subsequent: register_version on the sidecar advances the
       statements chain; the sidecar file is overwritten in place.

The new sidecar version's chain is now equal to the note's chain
length, so the predicate flips True until the next confirmed cycle.
"""

from __future__ import annotations

import json
import re
import sys
import time
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.attributes import emit_attribute
from lib.predicates import statements_sidecar_of
from lib.protocols.febe.protocol import Session
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import USAGE_LOG, prompt_path


STATEMENTS_MODEL = "sonnet"
STATEMENTS_TEMPLATE = prompt_path("discovery/assembly/produce-statements.md")


def _strip_preamble(text: str) -> str:
    """Strip any preamble before the statements header line."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
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
        text, elapsed = invoke_claude(
            prompt, model=STATEMENTS_MODEL, effort="high",
        )
        if not text:
            return AgentResult(success=False, detail="llm-failed")

        body = _strip_preamble(text)
        body = _add_source_line(body, full_note.name, asn_content)
        if not body.endswith("\n"):
            body += "\n"

        # First-time: emit_attribute creates the link + sidecar.
        # Subsequent: register_version advances the statements chain;
        # write the new content to the sidecar file.
        if sidecar_addr is None:
            emit_attribute(session, note_path, "statements", body)
        else:
            session.register_version(sidecar_addr)
            sidecar_path = session.get_path_for_addr(sidecar_addr)
            full_sidecar = session.store.lattice_dir / sidecar_path
            full_sidecar.write_text(body)

        _log_usage(asn_label, elapsed)
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
        m = re.search(r"(ASN-\d{4})", path)
        return m.group(1) if m else "ASN-????"
