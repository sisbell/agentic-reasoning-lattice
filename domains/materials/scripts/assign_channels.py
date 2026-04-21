#!/usr/bin/env python3
"""
Materials channel-assignment logic for the revise-stage evidence gatherer.

Owns the materials-specific pieces of the revise orchestrator:
  - the prompt that asks an LLM to decide which channels each finding needs
  - the parser that reads the response back into role-keyed question dicts
  - the display-name map (role -> authority label)

Generic code in scripts/lib/revise/gather_evidence.py imports this module
and dispatches channel consultations without knowing the channel labels.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import DOMAIN_PROMPTS
from lib.shared.common import read_file


PROMPT_TEMPLATE = DOMAIN_PROMPTS / "revise" / "assign-channels.md"

DISPLAY_NAMES = {
    "theory": "Theory",
    "evidence": "Evidence",
}


def build_prompt(asn_content, revise_section):
    """Build the channel-assignment prompt for a review's REVISE section."""
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        raise FileNotFoundError(f"prompt template not found: {PROMPT_TEMPLATE}")
    return template.format(asn_content=asn_content, revise_section=revise_section)


_AUTHORITY_TO_ROLE = {
    "Theory": "theory",
    "Evidence": "evidence",
}


def parse(response):
    """Parse a channel-assignment response into a list of finding dicts.

    Each dict has: number (int), title (str), reason (str),
    questions (dict[role, question_text]; empty when the finding is internal).
    """
    items = []
    current = None

    for line in response.split("\n"):
        line = line.strip()

        m = re.match(r"##\s+Issue\s+(\d+):\s*(.+)", line)
        if m:
            if current:
                items.append(current)
            current = {
                "number": int(m.group(1)),
                "title": m.group(2).strip(),
                "reason": None,
                "questions": {},
            }
            continue

        if current is None:
            continue

        m = re.match(r"Reason:\s*(.+)", line)
        if m:
            current["reason"] = m.group(1).strip()
            continue

        m = re.match(r"(\w+)\s+question:\s*(.+)", line)
        if m:
            role = _AUTHORITY_TO_ROLE.get(m.group(1))
            if role:
                current["questions"][role] = m.group(2).strip()
            continue

    if current:
        items.append(current)

    return items
