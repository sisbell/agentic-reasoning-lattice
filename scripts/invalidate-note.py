#!/usr/bin/env python3
"""Operator-driven note dep-integration audit trigger.

Emits a synthetic review + finding + comment.revise on the target note
so the runner picks up a dep-audit pass:

  1. is_doc_quiescent flips False (open revise present)
  2. note_consult routes the finding through consultation
  3. note_revise fires → reviser actions the audit directive: reviews body
     against declared dependencies, replaces redevelopments with citations
     where the dep already establishes the claim, and flags unused deps
  4. note_review re-evaluates the revised body

Use after dep changes (additions, swaps, foundation cycles) when the
body should be brought into alignment with the new dependency set.

Usage:
    python scripts/invalidate-note.py <asn> --reason "<why>"

Example:
    python scripts/invalidate-note.py 76 --reason "ASN-0098 added as dep"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_review_content, emit_review_coverage
from lib.lattice.findings import record_one_finding
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.paths import (
    LATTICE, NOTE_FINDINGS_DIR, NOTE_REVIEWS_DIR, next_review_number,
)


SYNTHETIC_REVIEW_TEMPLATE = """# Operator-Triggered Dep Audit of {asn_label}

This review was emitted to direct an audit of the note body against its
declared dependencies. See finding 0 for the audit directive.

## REVISE

### Issue 1: Body-dependency integration audit

Reason: {reason}

VERDICT: REVISE
"""

SYNTHETIC_FINDING_TEMPLATE = """Audit the note body against the inquiry's declared dependencies.

For each dep listed in the inquiry's `depends:` set, check whether the
body redevelops claims, lemmas, or proofs that the foundation already
establishes. Where redevelopment is found, replace it with explicit
citation to the foundation (cite by ASN number and claim name).

If a declared dep has no use site in the body after auditing, document
why it is retained or flag for removal from `depends:`.

Reason for this audit: {reason}
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
        prog="invalidate-note",
        description=(
            "Emit a synthetic review + finding directing the reviser to "
            "audit the note body against its declared dependencies."
        ),
    )
    parser.add_argument("asn", help="ASN number (e.g., 43, 0043, ASN-0043)")
    parser.add_argument(
        "--reason", required=True,
        help="One-line rationale for the audit trail.",
    )
    args = parser.parse_args()

    _, asn_label = _parse_asn(args.asn)

    with open_session(LATTICE) as session:
        note_addr, note_path = _resolve_note_addr(session, asn_label)

        review_num = next_review_number(asn_label, kind="note")
        review_dir = NOTE_REVIEWS_DIR / asn_label
        review_dir.mkdir(parents=True, exist_ok=True)
        review_path = review_dir / f"review-{review_num}.md"
        review_rel = str(review_path.relative_to(session.store.lattice_dir))
        review_body = SYNTHETIC_REVIEW_TEMPLATE.format(
            asn_label=asn_label, reason=args.reason,
        )
        session.update_document(review_rel, review_body)
        review_addr = session.register_path(review_rel)
        emit_review_content(session.store, review_addr)
        emit_review_coverage(session.store, review_addr, note_addr)

        finding_root = NOTE_FINDINGS_DIR / asn_label / f"review-{review_num}"
        finding_root.mkdir(parents=True, exist_ok=True)
        finding_path = finding_root / "0.md"
        finding_rel = str(finding_path.relative_to(session.store.lattice_dir))
        finding_body = SYNTHETIC_FINDING_TEMPLATE.format(reason=args.reason)
        finding_addr, comment = record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=finding_body,
            target_addr=note_addr,
            review_addr=review_addr,
            comment_kind="revise",
        )

    print(
        f"  [INVALIDATE] {asn_label} review-{review_num}: "
        f"review={review_addr} finding={finding_addr} comment={comment.addr}",
        file=sys.stderr,
    )
    print(
        f"  Next runner pass will fire note_consult → note_revise → "
        f"note_review on {asn_label}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
