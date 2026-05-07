"""Shared helpers for LLM-call wrappers.

Three primitives that recur across the per-claim LLM-dispatching
producers (claim_contract, claim_signature_resolve, citation_resolve,
and similar):

- `invoke_text(prompt, *, model, effort, tools)` — call invoke_claude
  with empty-response handling; returns (raw_text, elapsed). Raises
  on empty response.

- `parse_yaml_dict(text)` — strip fences + yaml.safe_load + assert
  dict. Raises ValueError on parse failure or non-dict.

- `parse_two_sections(text, header1, header2)` — split a response
  with two named YAML sections (e.g. `INTRODUCES:` / `REMOVES:`,
  `CLASSIFICATIONS:` / `RETRACTIONS:`); strip fences and yaml.safe_load
  each. Returns (parsed1, parsed2) — both lists. Raises ValueError on
  missing/misordered headers, parse errors, or non-list result.

Producer helpers compose these for the prompt-render → call → parse
flow, then add domain-specific validation on the parsed structure.
"""

from __future__ import annotations

from typing import Optional, Tuple

import yaml

from lib.shared.invoke_claude import invoke_claude, strip_code_fence


def invoke_text(
    prompt: str,
    *,
    model: str = "sonnet",
    effort: str = "high",
    tools: Optional[str] = None,
) -> Tuple[str, float]:
    """Run LLM; return (raw_text, elapsed). Raise on empty response."""
    if tools is None:
        result = invoke_claude(prompt, model=model, effort=effort)
    else:
        result = invoke_claude(prompt, model=model, effort=effort, tools=tools)
    if not result.text:
        raise RuntimeError(
            f"LLM returned empty after {result.elapsed:.0f}s",
        )
    return result.text, result.elapsed


def parse_yaml_dict(text: str) -> dict:
    """Strip code fence, parse YAML, assert dict. Raise on failure."""
    stripped = strip_code_fence(text.strip())
    try:
        parsed = yaml.safe_load(stripped)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}\n--- raw ---\n{stripped}")
    if not isinstance(parsed, dict):
        raise ValueError(
            f"expected YAML dict, got {type(parsed).__name__}: "
            f"{parsed!r}\n--- raw ---\n{stripped}"
        )
    return parsed


def parse_two_sections(
    text: str, header1: str, header2: str,
) -> Tuple[list, list]:
    """Find `<header1>:` and `<header2>:` in text; parse each body as
    a YAML list. Returns (parsed1, parsed2).

    Both sections must be present, header1 must precede header2, and
    each parsed body must be a list (or None, treated as empty list).
    Raises ValueError on missing/misordered headers, YAML parse error,
    or non-list parse result.
    """
    text = text.strip()
    h1 = f"{header1}:"
    h2 = f"{header2}:"
    idx1 = text.find(h1)
    idx2 = text.find(h2)
    if idx1 < 0:
        raise ValueError(f"missing {h1} header in response:\n{text}")
    if idx2 < 0:
        raise ValueError(f"missing {h2} header in response:\n{text}")
    if idx2 < idx1:
        raise ValueError(f"{h2} appears before {h1} in response")

    body1 = strip_code_fence(text[idx1 + len(h1):idx2].strip())
    body2 = strip_code_fence(text[idx2 + len(h2):].strip())

    try:
        parsed1 = yaml.safe_load(body1) or []
        parsed2 = yaml.safe_load(body2) or []
    except yaml.YAMLError as e:
        raise ValueError(
            f"YAML parse error: {e}\n"
            f"--- {header1} ---\n{body1}\n"
            f"--- {header2} ---\n{body2}"
        )
    if not isinstance(parsed1, list):
        raise ValueError(
            f"{header1} must be a list, got "
            f"{type(parsed1).__name__}: {parsed1!r}\n"
            f"--- raw block ---\n{body1}"
        )
    if not isinstance(parsed2, list):
        raise ValueError(
            f"{header2} must be a list, got "
            f"{type(parsed2).__name__}: {parsed2!r}\n"
            f"--- raw block ---\n{body2}"
        )
    return parsed1, parsed2
