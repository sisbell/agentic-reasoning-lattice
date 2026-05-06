"""Body-resolution helpers for claim_decompose.

These helpers were previously in lib/claim_derivation/transclude.py.
They moved here when the transclude phase was retired (its identity-
emission work absorbed into ClaimDecomposeAgent; its annotate-derived
emissions superseded by predicate-fired producers).

Public:
- `find_in_source(source_note_text, llm_body_text)` — locate the
  LLM-proposed body in the source note via exact then whitespace-
  normalized match. Returns the source's actual bytes (so we write
  a verbatim substring), or None on failure. Strict by design — no
  fuzzy matching.
- `load_claims_from_yamls(sections_dir)` — read every section yaml
  and return [(yaml_basename, claim_dict), ...] preserving order.
- `clean_label(raw_label)` — strip trailing dots, replace spaces
  with dashes; returns (cleaned, was_changed).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

import yaml


_WHITESPACE_RE = re.compile(r"\s+")


def find_in_source(source_note_text: str, llm_body_text: str) -> str | None:
    """Locate `llm_body_text` in `source_note_text` and return the
    matched source-bytes substring, or None on failure.

    The decompose-phase LLM returns a `body:` field that's its best
    attempt at copying a region of the source note verbatim. LLMs
    drift slightly in practice; this function treats the LLM body as
    a probe and returns the source's actual bytes so the caller
    writes a verbatim substring of the source note. Strict by design
    — no fuzzy matching, since fuzzy is silent acceptance of
    unexplained drift.

    Match strategy is two-stage:
    1. Exact byte-substring match.
    2. Whitespace-normalized match — collapse runs of whitespace to
       single spaces in both source and probe, locate, then map back
       to the source's original bytes.
    """
    if not source_note_text or not llm_body_text:
        return None

    if llm_body_text in source_note_text:
        return llm_body_text

    normalized_probe = _WHITESPACE_RE.sub(" ", llm_body_text).strip()
    if not normalized_probe:
        return None

    norm_source, norm_to_src = _normalize_with_offset_map(source_note_text)

    start_norm = norm_source.find(normalized_probe)
    if start_norm == -1:
        return None

    end_norm = start_norm + len(normalized_probe)
    src_start = norm_to_src[start_norm]
    src_end_inclusive = norm_to_src[end_norm - 1]
    src_end = src_end_inclusive + 1
    while (src_end < len(source_note_text)
           and source_note_text[src_end].isspace()
           and end_norm < len(norm_source)
           and norm_source[end_norm] == " "):
        src_end += 1

    return source_note_text[src_start:src_end]


def _normalize_with_offset_map(text: str) -> Tuple[str, List[int]]:
    """Collapse whitespace runs to single spaces; return (normalized,
    offset_map) where offset_map[i] is the source byte offset for
    position i in the normalized text. Leading/trailing whitespace
    preserved positionally.
    """
    out_chars = []
    offset_map = []
    in_ws_run = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if in_ws_run:
                continue
            out_chars.append(" ")
            offset_map.append(i)
            in_ws_run = True
        else:
            out_chars.append(ch)
            offset_map.append(i)
            in_ws_run = False
    return "".join(out_chars), offset_map


def clean_label(raw_label: str) -> Tuple[str, bool]:
    """Strip trailing dots and replace spaces with dashes. Return the
    cleaned label and a bool indicating whether anything changed."""
    cleaned = raw_label.rstrip(".").replace(" ", "-")
    return cleaned, cleaned != raw_label


def load_claims_from_yamls(sections_dir: Path) -> List[Tuple[str, dict]]:
    """Read every section yaml under `sections_dir`. Returns a list of
    (yaml_basename, claim_dict) tuples, preserving section ordering.

    Empty yamls and yamls without a `claims` list are skipped."""
    out = []
    for yaml_path in sorted(sections_dir.glob("*.yaml")):
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        for prop in data.get("claims") or []:
            out.append((yaml_path.name, prop))
    return out
