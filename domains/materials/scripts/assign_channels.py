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

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import CHANNELS_DIR, prompt_path
from lib.shared.common import read_file
from lib.shared.campaign import resolve_campaign


PROMPT_TEMPLATE = prompt_path("revise/assign-channels.md")

DISPLAY_NAMES = {
    "theory": "Theory",
    "evidence": "Evidence",
}


def _channel_description(channel_name):
    """Read the channel's description from its meta.yaml."""
    meta_path = CHANNELS_DIR / channel_name / "meta.yaml"
    try:
        meta = yaml.safe_load(meta_path.read_text()) or {}
    except FileNotFoundError:
        raise FileNotFoundError(
            f"channel meta.yaml not found: {meta_path}"
        )
    description = meta.get("description", "").strip()
    if not description:
        raise ValueError(
            f"channel {channel_name} meta.yaml missing `description:` field"
        )
    return description


def build_prompt(asn_content, revise_section, asn_id):
    """Build the channel-assignment prompt for a review's REVISE section.

    Resolves the ASN's campaign, reads each bound channel's meta.yaml
    description, and substitutes into the prompt template.
    """
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        raise FileNotFoundError(f"prompt template not found: {PROMPT_TEMPLATE}")

    campaign = resolve_campaign(asn_id)
    theory_description = _channel_description(campaign.theory_channel)
    evidence_description = _channel_description(campaign.evidence_channel)

    return template.format(
        asn_content=asn_content,
        revise_section=revise_section,
        theory_description=theory_description,
        evidence_description=evidence_description,
    )


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
