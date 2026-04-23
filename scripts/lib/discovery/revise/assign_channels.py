"""Revise-stage channel assignment — decide which channels each REVISE
finding needs consulted, then parse the LLM's response.

Tolerant parser: recognizes both the generic role labels ("Theory",
"Evidence") used by the shared revise prompt AND the capitalized channel
names ("Nelson", "Gregory", "Maxwell-1867", ...) used by lattice-specific
overrides. No per-channel display_name configuration required — the
channel name itself, title-cased by '-', IS the label for convention-based
parsing.
"""

import re

from lib.shared.paths import prompt_path, load_channel_meta
from lib.shared.common import read_file
from lib.shared.campaign import resolve_campaign

PROMPT_TEMPLATE = prompt_path("discovery/revise/assign-channels.md")

# Always-recognized role labels, regardless of channels bound.
_ROLE_LABELS = {"Theory": "theory", "Evidence": "evidence"}


def _capitalize_channel(name):
    """Title-case a channel name by its '-' separators.
    nelson → Nelson, maxwell-1867 → Maxwell-1867, dulong-petit-1819 → Dulong-Petit-1819."""
    return "-".join(p[:1].upper() + p[1:] for p in name.split("-"))


def _channel_description(channel_name):
    desc = (load_channel_meta(channel_name).get("description") or "").strip()
    if not desc:
        raise ValueError(
            f"channel {channel_name} meta.yaml missing `description:` field")
    return desc


def display_names(asn_id):
    """Return {role: capitalized_channel_name} for the ASN's bound channels.
    Used by revise-stage log output for category labels."""
    campaign = resolve_campaign(asn_id)
    return {
        "theory": _capitalize_channel(campaign.theory_channel),
        "evidence": _capitalize_channel(campaign.evidence_channel),
    }


def category_label(roles, asn_id):
    """Derive a display category from the set of channels a finding needs."""
    if not roles:
        return "INTERNAL"
    if len(roles) >= 2:
        return "BOTH"
    return display_names(asn_id)[next(iter(roles))].upper()


def build_prompt(asn_content, revise_section, asn_id):
    """Build the channel-assignment prompt. Resolves the ASN's campaign,
    reads each bound channel's description from meta.yaml, substitutes
    into the prompt template picked by the lattice-override resolver."""
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        raise FileNotFoundError(f"prompt template not found: {PROMPT_TEMPLATE}")
    campaign = resolve_campaign(asn_id)
    return template.format(
        asn_content=asn_content,
        revise_section=revise_section,
        theory_description=_channel_description(campaign.theory_channel),
        evidence_description=_channel_description(campaign.evidence_channel),
    )


def parse(response, asn_id):
    """Parse a channel-assignment response into finding dicts.

    Accepts labels from either convention — the hardcoded role labels
    ("Theory"/"Evidence" — shared prompt) and the capitalized channel
    names of the ASN's bound channels (xanadu override uses "Nelson"/
    "Gregory"; a hypothetical materials override could use "Maxwell-1867"/
    "Dulong-Petit-1819").

    Each returned finding dict has: number (int), title (str), reason (str
    or None), questions (dict[role, question_text]; empty when internal).
    """
    campaign = resolve_campaign(asn_id)
    # Build channel-name mappings first; hardcoded role labels are applied
    # last so they always win — protects against a channel name that happens
    # to collide with "Theory"/"Evidence" being bound to the opposite role.
    authority_to_role = {
        _capitalize_channel(campaign.theory_channel): "theory",
        _capitalize_channel(campaign.evidence_channel): "evidence",
    }
    authority_to_role.update(_ROLE_LABELS)

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

        m = re.match(r"(\w[\w-]*)\s+question:\s*(.+)", line)
        if m:
            role = authority_to_role.get(m.group(1))
            if role:
                current["questions"][role] = m.group(2).strip()

    if current:
        items.append(current)
    return items
