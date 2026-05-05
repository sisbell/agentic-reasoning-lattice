#!/usr/bin/env python3
"""Regenerate the lattice index into _workspace/index.md.

Walks every inquiry doc, derives stage and depends from substrate, and
writes a flat ASN table. Workspace artifact, regenerated on demand.

Stage rules:
  inquiry  — inquiry exists, no note draft yet
  note     — note exists, no claims derived
  derived  — claims derived from note, none have a comment.revise yet
  claims   — at least one derived claim has a comment.revise

Retired ASNs are excluded.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.predicates import is_retired
from lib.predicates.citations import depends as note_depends
from lib.predicates.convergence import derived_claims
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import (
    INQUIRY_DIR, LATTICE, WORKSPACE_DIR, inquiry_doc_path, load_inquiry,
)


def _stage(session, note_addr) -> str:
    derived = list(derived_claims(session, note_addr))
    if not derived:
        return "note"
    for claim_addr in derived:
        if session.active_links("comment.revise", to_set=[claim_addr]):
            return "claims"
    return "derived"


def _depends_label(session, addr) -> str:
    """Render the doc's citation.depends as e.g. '34,36,43' (ASN nums).

    Works for either a note address or an inquiry address; both layers
    use the same `citation.depends` link type. Note-level citations
    mirror inquiry-level ones (Phase 2a migration), so an inquiry-stage
    row reads the inquiry's citation graph and a later-stage row reads
    the note's.
    """
    nums = []
    for dep in note_depends(session, addr):
        path = session.get_path_for_addr(dep)
        if not path:
            continue
        m = re.search(r"ASN-(\d{4})", path)
        if m:
            nums.append(int(m.group(1)))
    nums = sorted(set(nums))
    return ",".join(str(n) for n in nums) if nums else "—"


def _row_for_inquiry(session, inquiry_path):
    m = re.match(r"ASN-(\d{4})", inquiry_path.stem)
    if not m:
        return None
    asn_num = int(m.group(1))
    asn_label = f"ASN-{asn_num:04d}"
    title = load_inquiry(asn_num).get("title", "—")

    inquiry_addr = session.get_addr_for_path(
        str(inquiry_doc_path(asn_num).relative_to(LATTICE)),
    )

    asn_path, _ = find_asn(str(asn_num))
    note_addr = None
    if asn_path is not None:
        note_addr = session.get_addr_for_path(
            str(asn_path.relative_to(LATTICE)),
        )
        if note_addr is not None and is_retired(session, note_addr):
            return None

    if note_addr is None:
        deps = _depends_label(session, inquiry_addr) if inquiry_addr else "—"
        return (asn_label, title, "inquiry", deps)

    return (
        asn_label,
        title,
        _stage(session, note_addr),
        _depends_label(session, note_addr),
    )


def main():
    session = open_session(LATTICE)
    rows = []
    for inquiry_path in sorted(INQUIRY_DIR.glob("ASN-*.md")):
        row = _row_for_inquiry(session, inquiry_path)
        if row is not None:
            rows.append(row)

    lines = [
        "# ASN Index",
        "",
        "Regenerate with: `python3 scripts/regenerate-index.py`",
        "",
        "| ASN | Title | Stage | Depends |",
        "|-----|-------|-------|---------|",
    ]
    for asn_label, title, stage, deps in rows:
        lines.append(f"| {asn_label} | {title} | {stage} | {deps} |")

    out_path = WORKSPACE_DIR / "index.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"wrote {out_path} ({len(rows)} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
