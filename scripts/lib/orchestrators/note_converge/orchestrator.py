"""Note convergence helpers — substrate-side primitives for the
single-pass review/revise CLI flows.

The convergence loop itself moved to the trigger runner — see
`lib.triggers.note_review` / `lib.triggers.note_revise` and
`scripts/note-converge.py`. This module retains the substrate-side
helpers that the single-pass CLI flows still depend on:

- `commit_note_review(session, asn_path, asn_label, text)` — write
  the review file, emit substrate links, return (review_path, findings)
- `collect_open_revises(session, note_rel)` — substrate query for
  unresolved revise comments on a note
- `log_usage(asn_label, elapsed, *, skill, data=None)` — telemetry
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

from lib.agents.note_review import extract_note_findings
from lib.backend.emit import emit_review
from lib.protocols.febe.protocol import Session
from lib.lattice.findings import record_one_finding
from lib.predicates import unresolved_revise_comments
from lib.shared.paths import (
    LATTICE, NOTE_FINDINGS_DIR, REVIEWS_DIR, USAGE_LOG, sorted_reviews,
)


# ---------------------------------------------------------------------------
# Reusable orchestration helpers


def collect_open_revises(session: Session, note_rel: str) -> list:
    """Return list of (comment_addr, title, body) for unresolved revise
    comments on the note.

    Reads each comment's source finding doc to get the finding text.
    Title is the first non-blank line of the body, stripped of `### `
    if present.
    """
    items = []
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        return items
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        finding_rel = session.get_path_for_addr(finding_addr)
        if not finding_rel:
            continue
        finding_full = LATTICE / finding_rel
        if not finding_full.exists():
            print(
                f"  [SKIP] finding doc missing: {finding_rel}",
                file=sys.stderr,
            )
            continue
        body = finding_full.read_text().strip()
        first_line = body.splitlines()[0] if body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"
        items.append((c.addr, title, body))
    return items


def commit_note_review(
    session: Session, asn_path: Path, asn_label: str, text: str,
):
    """Write the review file (sequential numbering) and emit substrate
    links: `review` classifier on the file, `comment.{revise|out-of-scope}`
    per finding. Returns (review_path, findings).
    """
    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    existing = sorted_reviews(asn_label)
    next_num = 1
    for f in existing:
        m = re.search(r"review-(\d+)\.md$", f.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    output_path = REVIEWS_DIR / asn_label / f"review-{next_num}.md"
    body = text + "\n"

    findings = extract_note_findings(text)
    review_stem = f"review-{next_num}"
    lattice_root = session.store.lattice_dir.resolve()
    output_rel = str(output_path.resolve().relative_to(lattice_root))
    asn_rel = str(asn_path.resolve().relative_to(lattice_root))

    # 1. Document write (review aggregate)
    session.update_document(output_rel, body)

    # 2. Substrate facts
    output_addr = session.register_path(output_rel)
    asn_addr = session.register_path(asn_rel)
    emit_review(session.store, output_addr)

    findings_root = NOTE_FINDINGS_DIR / asn_label / review_stem
    for n, (_title, cls, body) in enumerate(findings):
        finding_rel = str(
            (findings_root / f"{n}.md").resolve().relative_to(lattice_root)
        )
        cls_normalized = (cls or "REVISE").upper()
        comment_kind = (
            "out-of-scope" if cls_normalized == "OUT_OF_SCOPE" else "revise"
        )
        record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=body,
            target_addr=asn_addr,
            review_addr=output_addr,
            comment_kind=comment_kind,
        )
    return output_path, findings


def log_usage(
    asn_label: str,
    elapsed: float,
    *,
    skill: str,
    data: Optional[dict] = None,
) -> None:
    """Append a usage entry to the log.

    `skill` is the operation name ("review" / "revise"). `data` is
    optional — if provided (revise's Claude-SDK output), token and
    cost stats are included.
    """
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": skill,
        "asn": asn_label,
        "elapsed_s": round(elapsed, 1),
    }
    if data is not None:
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (
            usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
        )
        out = usage.get("output_tokens", 0)
        entry.update({
            "input_tokens": inp,
            "output_tokens": out,
            "num_turns": data.get("num_turns", 0),
            "cost_usd": cost,
        })
    try:
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


