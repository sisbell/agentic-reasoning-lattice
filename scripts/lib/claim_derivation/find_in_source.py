"""Resolve LLM-extracted claim body to a byte range in the source note.

The claim derivation pipeline's Phase 1 LLM returns a `body:` field per
claim — its best attempt at copying a region of the source note verbatim.
LLMs are unreliable at exact verbatim multi-paragraph reproduction; in
practice the body drifts slightly from the source (whitespace
normalization, punctuation tweaks, occasional minor reformatting).

This module treats the LLM body as a *probe* into the source. Given the
source note text and the LLM body, it locates the corresponding region
in the source and returns the source's bytes. The bytes the disassembler
writes are always the source's bytes — never the LLM's — so the claim
md is, by construction, a verbatim substring of the source note at
emission time.

Match strategy is two-stage strict (no fuzzy yet):

1. Exact byte-substring match.
2. Whitespace-normalized match — collapse runs of whitespace to single
   spaces in both source and probe, locate, then map the matched range
   back to the source's original bytes.

Returns the matched source range as a string, or None if no match found.
Strict by design — fuzzy matching is silent acceptance of unexplained
drift; failures should surface, not be smoothed over.
"""

import re


_WHITESPACE_RE = re.compile(r"\s+")


def find_in_source(source_note_text, llm_body_text):
    """Locate `llm_body_text` in `source_note_text`.

    Returns the matched source-bytes substring on success, or None if no
    match found. The returned string is always a substring of the source
    note (preserving the source's exact bytes, ignoring whatever drift
    the LLM introduced).
    """
    if not source_note_text or not llm_body_text:
        return None

    # Stage 1: exact byte-substring match
    if llm_body_text in source_note_text:
        return llm_body_text

    # Stage 2: whitespace-normalized match
    normalized_probe = _WHITESPACE_RE.sub(" ", llm_body_text).strip()
    if not normalized_probe:
        return None

    # Build a normalized form of the source plus an index mapping
    # each normalized-string position back to the source's byte offset.
    norm_source, norm_to_src = _normalize_with_offset_map(source_note_text)

    start_norm = norm_source.find(normalized_probe)
    if start_norm == -1:
        return None

    end_norm = start_norm + len(normalized_probe)
    src_start = norm_to_src[start_norm]
    # The end-index points one past the last matched normalized char;
    # use the src offset for end_norm-1 plus the length of the source
    # char at that position to land on the next byte boundary.
    src_end_inclusive = norm_to_src[end_norm - 1]
    # Walk forward across any source whitespace following the matched
    # region's last source char, since the probe may have collapsed
    # trailing whitespace.
    src_end = src_end_inclusive + 1
    while (src_end < len(source_note_text)
           and source_note_text[src_end].isspace()
           and end_norm < len(norm_source)
           and norm_source[end_norm] == " "):
        src_end += 1

    return source_note_text[src_start:src_end]


def _normalize_with_offset_map(text):
    """Collapse whitespace runs to single spaces in `text`. Returns
    (normalized_text, offset_map) where offset_map[i] is the source byte
    offset corresponding to position i in normalized_text.

    Leading/trailing whitespace in `text` is preserved positionally
    (source-anchored) — only internal runs collapse. The first whitespace
    char of a run maps to its source offset; subsequent whitespace chars
    in the run are dropped.
    """
    out_chars = []
    offset_map = []
    in_ws_run = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if in_ws_run:
                continue  # drop interior whitespace from runs
            out_chars.append(" ")
            offset_map.append(i)
            in_ws_run = True
        else:
            out_chars.append(ch)
            offset_map.append(i)
            in_ws_run = False
    return "".join(out_chars), offset_map
