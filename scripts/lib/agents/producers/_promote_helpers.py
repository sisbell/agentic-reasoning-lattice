"""Shared helpers for the two promote producers.

`note_promote_open_questions` and `note_promote_out_of_scope` differ
in input source (note body vs review files) and prompt template, but
share the substrate-side machinery: walking active inquiries for
dedup context, allocating new ASN numbers, parsing the LLM's
verdicts, creating inquiry docs, persisting the report with audit
edges.

These helpers exist to keep both agents lean. They don't carry any
caste-specific logic — pure scaffolding around the substrate writes.
"""

from __future__ import annotations

import re
import sys
from typing import Iterable, List, Tuple

from lib.backend.addressing import Address
from lib.backend.emit import emit_derivation, emit_inquiry, emit_promotion
from lib.protocols.febe.protocol import Session
from lib.shared.frontmatter import read_doc_frontmatter
from lib.shared.paths import (
    LATTICE, WORKSPACE, inquiry_doc_path, promotion_doc_path,
)


def _inquiry_addrs(session: Session) -> Iterable[Tuple[int, Address]]:
    """Yield (asn_num, addr) for every active inquiry classifier."""
    for link in session.active_links("inquiry"):
        if not link.to_set:
            continue
        addr = link.to_set[0]
        path = session.get_path_for_addr(addr)
        if not path:
            continue
        m = re.search(r"ASN-(\d+)", path)
        if m:
            yield int(m.group(1)), addr


def load_existing_inquiries(session: Session) -> str:
    """Read title + question from every active inquiry doc.

    Returns formatted text for injection into the promotion prompt.
    Used by both promote agents to give the LLM dedup context.
    """
    entries = []
    for asn_num, _ in sorted(_inquiry_addrs(session)):
        front = read_doc_frontmatter(inquiry_doc_path(asn_num))
        title = front.get("title", "")
        question = front.get("question", "")
        if title:
            entries.append(f"- ASN-{asn_num:04d}: {title} — {question}")
    return "\n".join(entries) if entries else "(none)"


def next_asn_number(session: Session) -> int:
    """Return the next available ASN number (max + 1 over active inquiries).

    Inquiry-to-ASN is 1-1 by construction; no manifests-dir scan.
    """
    nums = [n for n, _ in _inquiry_addrs(session)]
    return max(nums, default=0) + 1


def parse_promoted(text: str) -> List[dict]:
    """Parse LLM promotion output into list of promoted items.

    Each item is a dict with keys: title, question, area, nelson, gregory.
    Both promote agents use the same output schema.
    """
    items = []
    in_promoted = False
    current = None

    for line in text.split("\n"):
        stripped = line.strip()

        if stripped.startswith("## Promoted"):
            in_promoted = True
            continue
        if stripped.startswith("## Declined"):
            in_promoted = False
            if current:
                items.append(current)
                current = None
            continue

        if not in_promoted:
            continue

        if stripped.startswith("- **"):
            if current:
                items.append(current)
            current = {}
            continue

        if current is None:
            continue

        if stripped.startswith("- Title:"):
            current["title"] = stripped[len("- Title:"):].strip()
        elif stripped.startswith("- Question:"):
            current["question"] = stripped[len("- Question:"):].strip()
        elif stripped.startswith("- Area:"):
            current["area"] = stripped[len("- Area:"):].strip()
        elif stripped.startswith("- Nelson:"):
            try:
                current["nelson"] = int(stripped[len("- Nelson:"):].strip())
            except ValueError:
                current["nelson"] = 10
        elif stripped.startswith("- Gregory:"):
            try:
                current["gregory"] = int(stripped[len("- Gregory:"):].strip())
            except ValueError:
                current["gregory"] = 10

    if current:
        items.append(current)
    return items


def create_inquiry_doc(
    session: Session, asn_num: int, title: str, question: str,
    area: str, source_asn: int,
    nelson: int = 10, gregory: int = 10,
) -> Address:
    """Create a substrate-citizen inquiry doc for a promoted item.

    Writes inquiry frontmatter + body, registers the path, emits the
    `inquiry` classifier. Returns the new inquiry's address.
    """
    path = inquiry_doc_path(asn_num)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"---\n"
        f'title: "{title}"\n'
        f'question: "{question}"\n'
        f'covers: ""\n'
        f'out_of_scope: ""\n'
        f'area: "{area}"\n'
        f"nelson: {nelson}\n"
        f"gregory: {gregory}\n"
        f'source: "promoted from ASN-{source_asn:04d}"\n'
        f"---\n"
        f"\n"
        f"# Inquiry: {title}\n"
    )
    path.write_text(body)
    rel = str(path.relative_to(LATTICE))
    addr = session.store.register_path(rel)
    emit_inquiry(session.store, addr)
    print(f"  [CREATED] {path.relative_to(WORKSPACE)}", file=sys.stderr)
    return addr


def load_existing_promotion(asn_num: int, kind: str) -> str:
    """Read previous promotion report's content. Returns "" if missing."""
    path = promotion_doc_path(asn_num, kind)
    if path.exists():
        return path.read_text().strip()
    return ""


def save_promotion_report(
    session: Session, asn_num: int, kind: str, text: str,
    *, source_note_addr: Address | None = None,
    promoted_inquiry_addrs: Iterable[Address] = (),
) -> Address:
    """Persist the report + emit substrate audit edges.

    1. Writes the report at the canonical promotion path.
    2. Registers; emits `promotion.<kind>` classifier (idempotent on re-run).
    3. Emits `provenance.derivation(source_note → report)`.
    4. Emits `provenance.derivation(report → each new inquiry)`.
    """
    path = promotion_doc_path(asn_num, kind)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n")

    rel = str(path.relative_to(LATTICE))
    report_addr = session.store.register_path(rel)
    emit_promotion(session.store, report_addr, kind)

    if source_note_addr is not None:
        emit_derivation(session.store, source_note_addr, report_addr)

    for inq_addr in promoted_inquiry_addrs:
        emit_derivation(session.store, report_addr, inq_addr)

    print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)
    return report_addr
