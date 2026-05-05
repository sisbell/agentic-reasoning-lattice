"""
Promotion step functions — shared by open-questions and out-of-scope orchestrators.

- load_existing_inquiries: walk substrate inquiry classifiers, read title +
  question from each inquiry doc's frontmatter
- next_asn_number: walk substrate inquiry classifiers, return max ASN num + 1
- parse_promoted: parse LLM promotion output into structured items
- create_inquiry_doc: write a new substrate-citizen inquiry doc + emit classifier
- load_existing_promotion: read previous promotion report from substrate path
- save_promotion_report: write report + emit promotion classifier + provenance edges
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.backend.emit import (
    emit_derivation, emit_inquiry, emit_promotion,
)
from lib.shared.common import find_asn
from lib.shared.frontmatter import read_doc_frontmatter
from lib.shared.paths import (
    INQUIRY_DIR, LATTICE, WORKSPACE,
    inquiry_doc_path, promotion_doc_path,
)


def _inquiry_addrs(session):
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


def load_existing_inquiries(session):
    """Read title + question from every active inquiry doc.

    Returns formatted text for injection into the promotion prompt.
    """
    entries = []
    for asn_num, _ in sorted(_inquiry_addrs(session)):
        front = read_doc_frontmatter(inquiry_doc_path(asn_num))
        title = front.get("title", "")
        question = front.get("question", "")
        if title:
            entries.append(
                f"- ASN-{asn_num:04d}: {title} — {question}"
            )
    return "\n".join(entries) if entries else "(none)"


def next_asn_number(session):
    """Return the next available ASN number.

    Sourced from substrate: max ASN num over active inquiry classifiers + 1.
    Inquiry-to-ASN is 1-1 by construction; no manifests-dir scan needed.
    """
    nums = [n for n, _ in _inquiry_addrs(session)]
    return max(nums, default=0) + 1


def parse_promoted(text):
    """Parse LLM promotion output into list of promoted items.

    Each item is a dict with keys: title, question, area, nelson, gregory.
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

        # New promoted question
        if stripped.startswith("- **"):
            if current:
                items.append(current)
            current = {}
            continue

        if current is None:
            continue

        # Parse metadata lines
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
    session, asn_num, title, question, area, source_asn,
    nelson=10, gregory=10,
):
    """Create a new substrate-citizen inquiry doc for a promoted item.

    Writes the inquiry frontmatter + body to the canonical inquiry
    path, registers the path in substrate, and emits the `inquiry`
    classifier. Returns the new inquiry's substrate address.
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


def load_existing_promotion(asn_num, kind):
    """Read previous promotion report's content. Returns "" if missing."""
    path = promotion_doc_path(asn_num, kind)
    if path.exists():
        return path.read_text().strip()
    return ""


def save_promotion_report(
    session, asn_num, kind, text, *, source_note_addr=None,
    promoted_inquiry_addrs=(),
):
    """Persist the promotion report + emit substrate audit edges.

    1. Writes the report markdown at the canonical promotion path.
    2. Registers the path; emits `promotion.<kind>` classifier
       (idempotent on re-run — same path, same address).
    3. Emits `provenance.derivation` from the source ASN's note to
       the report (idempotent).
    4. Emits `provenance.derivation` from the report to each newly
       minted inquiry (idempotent — re-runs that promote the same
       item again hit the existing edge).
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
