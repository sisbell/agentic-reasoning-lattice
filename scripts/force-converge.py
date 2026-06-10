#!/usr/bin/env python3
"""Operator-driven manual convergence sign-off for a note.

The dual of invalidate-note.py. Emits the substrate facts the
convergence gate reads — NOTE_REVIEW_CONVERGENCE_DEPTH (2) consecutive
synthetic review docs with ZERO findings, each carrying the
review.content classifier, review.coverage onto the note, and a cascade
anchor (bundled citation.depends at the current foundation heads) — so
the note registers as converged without further LLM review cycles.

The sign-off expires honestly: the cascade anchor snapshots foundation
heads at sign-off time, so if a cited foundation later advances,
is_note_cascade_fresh flips False and the note legitimately re-enters
review. Manual convergence masks remaining review budget, never
dependency drift.

Refuses to run while the note has open comment.revise findings —
convergence also requires quiescence, and clean reviews atop open
findings would leave note_consult/note_revise firing. Close findings
first (resolution.py accept/reject per comment).

Usage:
    python scripts/force-converge.py <asn> --reason "<why>"

Example:
    python scripts/force-converge.py 116 --reason "budget sign-off; opus-era convergence accepted"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import (
    emit_citation_bundle, emit_review_content, emit_review_coverage,
)
from lib.lattice.labels import format_label
from lib.predicates import version_head
from lib.predicates.quiescence import is_doc_quiescent
from lib.protocols.febe.session import open_session
from lib.shared.foundation import FoundationError, foundation_dep_addrs
from lib.shared.paths import LATTICE, NOTE_REVIEWS_DIR, next_review_number
from lib.triggers.note_review import NOTE_REVIEW_CONVERGENCE_DEPTH


SYNTHETIC_REVIEW_TEMPLATE = """# Review of {asn_label} — MANUAL OPERATOR SIGN-OFF

**This is not an LLM review.** It was emitted by the operator via
`scripts/force-converge.py` ({pass_label}) to mark the note converged
without further review cycles.

Reason: {reason}

No findings were evaluated or filed by this sign-off. The most recent
substantive review of this note precedes this document; consult it for
the last assessed state. If a cited foundation advances after this
sign-off, the cascade anchor below goes stale and the note re-enters
normal review.

## REVISE

None.

## OUT_OF_SCOPE

(none — operator sign-off, no review performed)

VERDICT: CONVERGED
"""


def _parse_asn(raw: str) -> tuple[int, str]:
    digits = re.sub(r"\D", "", raw)
    if not digits:
        raise SystemExit(f"invalid ASN: {raw!r}")
    num = int(digits)
    return num, format_label(num)


def _resolve_note_addr(session, asn_label: str):
    for path, addr in session.store.path_to_addr.items():
        if f"/note/{asn_label}-" in path and not path.endswith(".statements.md"):
            return addr, path
    raise SystemExit(f"no note found for {asn_label}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="force-converge",
        description=(
            "Emit synthetic clean reviews + cascade anchor marking a "
            "note converged by manual operator sign-off."
        ),
    )
    parser.add_argument("asn", help="ASN number (e.g., 116, 0116, ASN-0116)")
    parser.add_argument(
        "--reason", required=True,
        help="One-line rationale for the audit trail.",
    )
    args = parser.parse_args()

    asn_number, asn_label = _parse_asn(args.asn)

    with open_session(LATTICE) as session:
        note_addr, _note_path = _resolve_note_addr(session, asn_label)

        if not is_doc_quiescent(session, note_addr):
            print(
                f"  [FORCE-CONVERGE] {asn_label} has open findings — "
                f"refusing to sign off over them.",
                file=sys.stderr,
            )
            print(
                "  Close each open comment first:\n"
                "    python scripts/agent_tools/resolution.py "
                "--comment-id <id> reject --rationale \"...\"",
                file=sys.stderr,
            )
            return 1

        try:
            foundation_heads = [
                version_head(session, dep)
                for dep in foundation_dep_addrs(session, asn_number)
            ]
        except FoundationError as e:
            print(
                f"  [FORCE-CONVERGE] {asn_label}: foundation deps "
                f"unresolvable ({e}); anchor will be omitted and the "
                f"sign-off cannot go cascade-stale — aborting. Fix deps "
                f"or sign off another way.",
                file=sys.stderr,
            )
            return 1

        review_dir = NOTE_REVIEWS_DIR / asn_label
        review_dir.mkdir(parents=True, exist_ok=True)

        emitted = []
        for i in range(NOTE_REVIEW_CONVERGENCE_DEPTH):
            review_num = next_review_number(asn_label, kind="note")
            review_path = review_dir / f"review-{review_num}.md"
            review_rel = str(
                review_path.relative_to(session.store.lattice_dir),
            )
            body = SYNTHETIC_REVIEW_TEMPLATE.format(
                asn_label=asn_label,
                reason=args.reason,
                pass_label=(
                    f"sign-off pass {i + 1} of "
                    f"{NOTE_REVIEW_CONVERGENCE_DEPTH}"
                ),
            )
            session.update_document(review_rel, body)
            review_addr = session.register_path(review_rel)
            emit_review_content(session.store, review_addr)
            emit_review_coverage(session.store, review_addr, note_addr)
            if foundation_heads:
                emit_citation_bundle(
                    session.store, review_addr, foundation_heads,
                    direction="depends",
                )
            emitted.append((review_num, review_addr))

    for review_num, review_addr in emitted:
        print(
            f"  [FORCE-CONVERGE] {asn_label} review-{review_num}: "
            f"review={review_addr} (clean, anchored)",
            file=sys.stderr,
        )
    print(
        f"  {asn_label} now satisfies the convergence gate "
        f"({NOTE_REVIEW_CONVERGENCE_DEPTH} consecutive clean reviews, "
        f"cascade anchor at current foundation heads).",
        file=sys.stderr,
    )
    print(
        f"  Re-opens automatically if a cited foundation advances; "
        f"re-open manually with: python scripts/invalidate-note.py "
        f"{asn_number} --reason \"...\"",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
