"""Renderer for `view.claim-statements` virtual documents.

A claim-statements view sits at a substrate address (no on-disk
file) and represents the assembled "what does this ASN say?"
artifact downstream discovery cites as a dependency. Reading the
view walks the substrate live:

- One incoming `provenance.derivation` link from the source note
  identifies the ASN anchor.
- Outgoing `provenance.derivation` links from the note enumerate
  the derived claims (in derivation order).
- For each claim, the renderer reads the body's `*Formal Contract:*`
  section + the name/description sidecars to assemble per-claim
  blocks.

The output mirrors the format the legacy `assemble_claim_statements`
function produced from yaml summaries, but reads from substrate-sourced
sidecars (`<stem>.name.md`, `<stem>.description.md`) and is computed
fresh on every call rather than cached to disk.
"""

from __future__ import annotations

import re
import time
from typing import Optional

from lib.backend.addressing import Address
from lib.lattice.render import read_doc, register_renderer
from lib.predicates import derived_claims
from lib.protocols.febe.protocol import Session
from lib.shared.foundation import _extract_formal_contract
from lib.shared.paths import view_path


_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def render_claim_statements(session: Session, addr: Address) -> str:
    """Assemble the claim-statements view's content from current substrate.

    Walks back to the source note via incoming `provenance.derivation`,
    then forward via `derived_claims` to enumerate the cluster.
    """
    note_addr = _source_note(session, addr)
    note_path = session.get_path_for_addr(note_addr)
    if note_path is None:
        return ""

    lattice_root = session.store.lattice_dir
    note_full = lattice_root / note_path
    note_text = note_full.read_text() if note_full.exists() else ""

    asn_label = _asn_label_from_path(note_path)
    asn_date = _extract_source_date(note_text)

    parts = [
        f"# {asn_label} Formal Statements\n",
        f"*Source: {note_full.name} (revised {asn_date}) — "
        f"Extracted: {time.strftime('%Y-%m-%d')}*\n",
    ]

    for claim_addr in derived_claims(session, note_addr):
        block = _render_claim_block(session, claim_addr)
        if block:
            parts.append(block)

    return "\n".join(parts) + "\n"


def _source_note(session: Session, view_addr: Address) -> Address:
    """Find the source note via incoming provenance.derivation."""
    incoming = session.active_links(
        "provenance.derivation", to_set=[view_addr],
    )
    if not incoming:
        raise ValueError(
            f"view {view_addr} has no incoming provenance.derivation"
        )
    return incoming[0].from_set[0]


def _asn_label_from_path(path: str) -> str:
    """Extract `ASN-NNNN` from a doc path."""
    m = re.search(r"(ASN-\d{4})", path)
    return m.group(1) if m else "ASN-????"


def _extract_source_date(note_text: str) -> str:
    """Pull the most recent ISO date from the note's metadata line."""
    date_line = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", note_text)
    if not date_line:
        return "unknown"
    all_dates = _DATE_RE.findall(date_line.group(0))
    return all_dates[-1] if all_dates else "unknown"


def _render_claim_block(session: Session, claim_addr: Address) -> str:
    """Read the per-claim files; produce the markdown block for this claim.

    Returns "" if the claim's md path is unresolvable.
    """
    rel = session.get_path_for_addr(claim_addr)
    if rel is None:
        return ""

    md_full = session.store.lattice_dir / rel
    if not md_full.exists():
        return ""

    stem = md_full.stem
    claim_dir = md_full.parent

    name_doc = claim_dir / f"{stem}.name.md"
    desc_doc = claim_dir / f"{stem}.description.md"

    name = _read_first_line(name_doc) or stem
    description = _read_full(desc_doc)
    contract = _extract_formal_contract(md_full.read_text())

    pieces = [f"## {stem} — {name}\n"]
    if description:
        pieces.append(f"{description}\n")
    if contract:
        pieces.append(f"{contract}\n")
    pieces.append("---\n")
    return "\n".join(pieces)


def _read_first_line(path):
    if not path.exists():
        return None
    content = path.read_text().strip()
    if not content:
        return None
    return content.split("\n", 1)[0].strip() or None


def _read_full(path):
    if not path.exists():
        return None
    content = path.read_text().strip()
    return content or None


register_renderer("claim-statements", render_claim_statements)


def read_claim_statements_view(
    session: Session, asn_label: str,
) -> Optional[str]:
    """Render the claim-statements view for an ASN, by label.

    Convenience for consumers that don't already hold the view's
    Address. Returns the rendered markdown, or None if no view doc
    is registered for this ASN.
    """
    lattice_root = session.store.lattice_dir.resolve()
    rel = str(
        view_path(asn_label, "claim-statements")
        .resolve().relative_to(lattice_root)
    )
    addr = session.get_addr_for_path(rel)
    if addr is None:
        return None
    return read_doc(session, addr)
