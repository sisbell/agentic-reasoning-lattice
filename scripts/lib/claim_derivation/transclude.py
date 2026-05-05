"""Transclude — project regions of the source note into per-claim docs.

Phase 3 of claim derivation. The previous phases identified each claim's
location and metadata in section YAMLs. This phase mechanically projects
each claim's content from the source note into a new addressable
document in the docuverse, then emits the substrate links that classify
that document and record its provenance.

For each claim the LLM identified:
  - Resolve the LLM-extracted body to a byte range in the source note
    via `find_in_source` (exact, then whitespace-normalized match). The
    bytes written are the source's bytes — the LLM's output is a probe,
    not authoritative content.
  - Write `_docuverse/documents/claim/<asn>/<label>.md` (the body) plus
    `<label>.label.md` and `<label>.name.md` sidecars.
  - Emit substrate links: `claim` classifier, `contract.<kind>` (if a
    type was identified), `citation` links from declared depends, plus
    `label` and `name` content links to the sidecars.

After all claims are written, emit a `provenance.derivation` link from
the source note to each claim, recording the historical fact that this
claim was derived from this note.

Structural sections (preamble, worked example, etc. — sections of the
source note that don't contain claims) are relocated as workspace
artifacts under `_workspace/claim-derivation/<asn>/structural/`.

Description sidecars are NOT written here — that's the
claim-describe trigger's job (lib/triggers/claim_describe.py +
lib/agents/claim_describe/). The Claim Document Contract's
description requirements (#1 file completeness, #4 description
link) are satisfied after the trigger fires on each fresh claim,
not at the end of transclude. This is a known boundary.

Usage (standalone):
    python scripts/lib/claim_derivation/transclude.py 36
    python scripts/lib/claim_derivation/transclude.py 36 --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, LATTICE, CLAIM_DERIVATION_DIR, CLAIM_DIR,
)
from lib.shared.common import find_asn
from lib.shared.git_ops import step_commit_asn
from lib.backend.emit import (
    emit_citation, emit_claim, emit_contract, emit_derivation,
    emit_supersession, emit_transclusion,
)
from lib.predicates import statements_sidecar_of, supersession_head
from lib.shared.paths import transclusion_path
from lib.lattice.attributes import emit_attribute
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.session import open_session

_WHITESPACE_RE = re.compile(r"\s+")


def find_in_source(source_note_text, llm_body_text):
    """Locate `llm_body_text` in `source_note_text` and return the
    matched source-bytes substring, or None on failure.

    The Phase-1 LLM returns a `body:` field that's its best attempt at
    copying a region of the source note verbatim. LLMs drift slightly
    in practice; this function treats the LLM body as a probe and
    returns the source's actual bytes so the disassembler writes a
    verbatim substring of the source note. Strict by design — no fuzzy
    matching, since fuzzy is silent acceptance of unexplained drift.

    Match strategy is two-stage:
    1. Exact byte-substring match.
    2. Whitespace-normalized match — collapse runs of whitespace to
       single spaces in both source and probe, locate, then map back to
       the source's original bytes.
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


def _normalize_with_offset_map(text):
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


def _clean_label(raw_label):
    """Strip trailing dots and replace spaces with dashes. Return the
    cleaned label and a bool indicating whether anything changed."""
    cleaned = raw_label.rstrip(".").replace(" ", "-")
    return cleaned, cleaned != raw_label


def _load_claims(sections_dir):
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


def _is_structural(yaml_path):
    """A section is structural iff its yaml is missing or has no claims."""
    if not yaml_path.exists():
        return True
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return not (data and data.get("claims"))


def _structural_slug(md_path):
    """Map `00-preamble.md` → `preamble`."""
    name = md_path.stem
    return name.split("-", 1)[1] if "-" in name else name


def _render_signature(entries):
    """Render annotate's signature list into a markdown bullet sidecar.

    `entries` is a list of {symbol, meaning} dicts (annotate-signature's
    output shape — non-logical symbols the claim introduces). Returns
    a markdown string with one bullet per symbol, or None if the list
    is empty / contains no usable entries (caller skips emitting the
    sidecar in that case)."""
    if not entries:
        return None
    lines = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        symbol = (e.get("symbol") or "").strip()
        meaning = (e.get("meaning") or "").strip()
        if not symbol:
            continue
        if meaning:
            lines.append(f"- `{symbol}` — {meaning}")
        else:
            lines.append(f"- `{symbol}`")
    if not lines:
        return None
    return "\n".join(lines)


def transclude_asn(asn_num, dry_run=False):
    """Project claim regions from the source note into the docuverse.

    Returns True if every claim was successfully transcluded; False if
    any claim's body failed to resolve into the source note (the run
    continues for other claims; failures are reported)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    sections_dir = CLAIM_DERIVATION_DIR / asn_label / "sections"
    if not sections_dir.exists():
        print(f"  No sections directory — run decompose first",
              file=sys.stderr)
        return False

    claims_dir = CLAIM_DIR / asn_label
    structural_dir = CLAIM_DERIVATION_DIR / asn_label / "structural"
    source_note_text = asn_path.read_text()

    print(f"\n  [TRANSCLUDE] {asn_label}", file=sys.stderr)
    print(f"  Source:    {asn_path.relative_to(WORKSPACE)}", file=sys.stderr)
    print(f"  Sections:  {sections_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  Output:    {claims_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  Structural:{structural_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # ── Phase A: load + resolve bodies via find_in_source ────────────────
    claims_to_emit = []   # successfully resolved
    failed = []           # body didn't match source
    seen_labels = set()

    for yaml_basename, prop in _load_claims(sections_dir):
        raw_label = prop.get("label", "")
        if not raw_label:
            print(f"    WARNING: claim without label in {yaml_basename}",
                  file=sys.stderr)
            continue
        label, label_was_cleaned = _clean_label(raw_label)
        if label_was_cleaned:
            print(f"    FIX label: {raw_label!r} → {label!r}",
                  file=sys.stderr)
        if label in seen_labels:
            print(f"    WARNING: duplicate label {label!r} in {yaml_basename}",
                  file=sys.stderr)
            continue
        seen_labels.add(label)

        llm_body = (prop.get("body") or "").strip()
        resolved = find_in_source(source_note_text, llm_body)
        if resolved is None:
            failed.append((label, yaml_basename, llm_body[:120]))
            continue

        claims_to_emit.append({
            "label": label,
            "name": (prop.get("name") or "").strip(),
            "type": (prop.get("type") or "").strip() or None,
            "depends": [d for d in (prop.get("depends") or []) if d],
            "signature": prop.get("signature") or [],
            "body_text": resolved.rstrip() + "\n",
        })

    if failed:
        print(f"\n  [TRANSCLUDE] {len(failed)} claim(s) failed body "
              f"resolution against source note:", file=sys.stderr)
        for label, yaml_basename, snippet in failed:
            print(f"    {label} (in {yaml_basename}): "
                  f"no exact / whitespace-normalized match. "
                  f"LLM body started: {snippet!r}", file=sys.stderr)

    if not claims_to_emit and not failed:
        print(f"  [TRANSCLUDE] No claims to emit (and no failures).",
              file=sys.stderr)
        return True

    if dry_run:
        for c in claims_to_emit:
            print(f"    {c['label']}.md  (resolved {len(c['body_text'])} bytes)",
                  file=sys.stderr)
        return not failed

    # ── Phase B: write per-claim files + emit substrate links ────────────
    claims_dir.mkdir(parents=True, exist_ok=True)

    # Local label → md-path index (lattice-relative substrate keys), used
    # for citation resolution within this ASN.
    lattice_root = Path(LATTICE).resolve()
    local_index = {
        c["label"]: str((claims_dir / f"{c['label']}.md").resolve()
                        .relative_to(lattice_root))
        for c in claims_to_emit
    }

    with open_session(LATTICE) as session:
        store = session.store  # for emit_* (Pass 2 will migrate)
        # lattice.labels.build_cross_asn_label_index returns
        # {label: claim_doc_addr}. local_index uses path strings; build
        # an addr-keyed merge by registering the new claim paths.
        cross_index = build_cross_asn_label_index(store)
        local_addr_index = {
            label: store.register_path(rel)
            for label, rel in local_index.items()
        }
        merged_index = {**cross_index, **local_addr_index}

        # Translate asn_path (the source note) once for derivation.
        asn_rel = str(asn_path.resolve().relative_to(lattice_root))
        asn_addr = store.register_path(asn_rel)

        for c in claims_to_emit:
            stem = c["label"]
            body_md = claims_dir / f"{stem}.md"
            body_md.write_text(c["body_text"])

            # Sidecar files + content links (label, name, signature).
            emit_attribute(session, body_md, "label", c["label"])
            emit_attribute(session, body_md, "name", c["name"] or c["label"])

            sig_md = _render_signature(c["signature"])
            if sig_md:
                emit_attribute(session, body_md, "signature", sig_md)

            # Classifier + contract — need the body's tumbler address.
            body_rel = str(body_md.resolve().relative_to(lattice_root))
            body_addr = store.register_path(body_rel)
            emit_claim(store, body_addr)
            if c["type"]:
                emit_contract(store, body_addr, c["type"])

            # Citation links from declared depends.
            for dep_label in c["depends"]:
                if dep_label not in merged_index:
                    print(f"    WARN {stem}: depends '{dep_label}' "
                          f"not in label index — citation skipped",
                          file=sys.stderr)
                    continue
                emit_citation(store, body_addr, merged_index[dep_label])

            print(f"    {stem}.md", file=sys.stderr)

        # ── Phase C: provenance.derivation links per claim ───────────────
        for c in claims_to_emit:
            body_md = claims_dir / f"{c['label']}.md"
            body_rel = str(body_md.resolve().relative_to(lattice_root))
            body_addr = store.register_path(body_rel)
            emit_derivation(store, asn_addr, body_addr)

        # ── Phase C.5: claim-statements transclusion ─────────────────────
        # Substrate citizen, no on-disk file. Content rendered live
        # by lib/renderers/claim_statements.py at read time, dispatched
        # via the `transclusion.claim-statements` runtime tag.
        transclusion_rel = str(
            transclusion_path(asn_label, "claim-statements")
            .resolve().relative_to(lattice_root)
        )
        transclusion_addr = store.register_path(transclusion_rel)
        emit_transclusion(store, transclusion_addr, "claim-statements")
        emit_derivation(store, asn_addr, transclusion_addr)

        # ── Phase C.6: supersede the note's statements artifact ──────────
        # If note-statements ran (LLM extraction filed a `statements`
        # sidecar on the note), emit supersession from its current
        # head → the transclusion doc. Foundation reads walking the
        # chain land at the transclusion post-derivation. If no
        # statements link exists yet, do nothing.
        stmt_addr = statements_sidecar_of(session, asn_addr)
        if stmt_addr is not None:
            head = supersession_head(session, stmt_addr)
            emit_supersession(store, head, transclusion_addr)

    # ── Phase D: structural sections → workspace ────────────────────────
    structural_count = 0
    structural_dir.mkdir(parents=True, exist_ok=True)
    for md_path in sorted(sections_dir.glob("*.md")):
        if not _is_structural(md_path.with_suffix(".yaml")):
            continue
        slug = _structural_slug(md_path)
        shutil.copy2(md_path, structural_dir / f"{slug}.md")
        print(f"    structural/{slug}.md", file=sys.stderr)
        structural_count += 1

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n  [TRANSCLUDE] {len(claims_to_emit)} claims emitted, "
          f"{len(failed)} failures, {structural_count} structural files",
          file=sys.stderr)

    step_commit_asn(asn_num, hint="transclude")
    return not failed


def main():
    parser = argparse.ArgumentParser(
        description="Transclude: project source-note regions as per-claim "
                    "docs in the docuverse + emit substrate links")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Resolve claims but write nothing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = transclude_asn(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
