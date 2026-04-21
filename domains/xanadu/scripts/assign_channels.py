#!/usr/bin/env python3
"""
Xanadu channel-assignment logic for the revise-stage evidence gatherer.

Owns the xanadu-specific pieces of the revise orchestrator:
  - the prompt that asks an LLM to decide which channels each finding needs
  - the parser that reads the response back into role-keyed question dicts
  - the display-name map (role -> authority name)

Generic code in scripts/lib/revise/gather_evidence.py imports this module
and dispatches channel consultations without knowing about Nelson, Gregory,
Literary Machines, or udanax-green.
"""

import re


DISPLAY_NAMES = {
    "theory": "Nelson",
    "evidence": "Gregory",
}


def build_prompt(asn_content, revise_section):
    """Build the channel-assignment prompt for a review's REVISE section."""
    return f"""You are deciding which expert channels each review finding needs consulted before revision.

## Channels

- **Nelson** (theory channel) — Ted Nelson's design intent. What the system was *meant* to do, what semantic constraints the designer intended. Nelson has access to Literary Machines and Nelson's concept notes. Ask Nelson when the fix requires understanding design intent. Examples: "Was this operation intended to be total or partial?", "Does the design require this ordering to be strict?"

- **Gregory** (evidence channel) — the udanax-green implementation. What the code actually does, what constraints it enforces, what edge cases it handles. Gregory has access to the knowledge base synthesis and the udanax-green C source. Ask Gregory when the fix requires evidence from the implementation. Examples: "Does the allocator enforce single-depth increment?", "What does INSERT do when the span crosses a boundary?"

A finding may need Nelson, Gregory, both, or neither (if the fix is derivable from the ASN's own content — definitions, proofs, or reasoning already present).

## ASN Content

{asn_content}

## REVISE Items

{revise_section}

## Instructions

For each REVISE issue, output a block in exactly this format:

```
## Issue N: [title from review]
Reason: [1-2 sentences explaining which channels are needed and why — or why the fix is internal]
Nelson question: [one focused question]       (include only if Nelson is needed)
Gregory question: [one focused question]      (include only if Gregory is needed)
```

If the fix is derivable from the ASN alone, omit both question lines.

Output ONLY the issue blocks, nothing else."""


_AUTHORITY_TO_ROLE = {
    "Nelson": "theory",
    "Gregory": "evidence",
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
