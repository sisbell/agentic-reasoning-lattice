#!/usr/bin/env python3
"""One-shot: backfill consultation classifiers for existing data.

Walks `_docuverse/documents/consultation/<asn>/<session>/` for the
active lattice and emits the appropriate substrate classifier for
each file:

    questions.md            → consultation.questions
    assessment.md           → consultation.assessment
    answer-NN-<role>.md     → consultation.answer
    answers.md              → skipped (workspace-shaped rendering;
                              not classified per the consultation
                              substrate-citizenship policy)
    anything else           → skipped with a log line

Idempotent — re-runs converge on the same substrate state. Run once
per lattice after the writer hookup commit (`9188bac5`) lands so new
consultations are already classifying themselves.

Skips `<asn>/sessions/` subdirectories — those are per-call
transcripts produced by `scripts/consult.py`, not the
question/answer/assessment shape this backfill is for. They get
their own treatment if needed (separate effort).

Usage:
    LATTICE=xanadu    ./run/backfill-consultations.sh             # default --min-asn 34
    LATTICE=materials ./run/backfill-consultations.sh --min-asn 1
    LATTICE=xanadu    ./run/backfill-consultations.sh --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import LATTICE, LATTICE_NAME
from lib.store.emit import (
    emit_consultation_answer, emit_consultation_assessment,
    emit_consultation_questions,
)
from lib.store.store import default_store

CONSULTATION_DIR = LATTICE / "_docuverse" / "documents" / "consultation"

# Matches `answer-NN-<role>.md` where <role> is either a normalized role
# label (`theory` / `evidence` — used by materials) or a raw channel name
# (`nelson` / `gregory` / etc. — used by xanadu's older convention). The
# substrate classifier doesn't care which token it is; the role is in the
# doc body's `## Question N [<role>]` header.
ANSWER_RE = re.compile(r"^answer-\d+-[a-z][a-z0-9-]*\.md$")
ASN_RE = re.compile(r"^ASN-(\d+)$")


def classify_one(store, path, dry_run):
    """Return (kind, action) where kind is the classifier name or
    'skipped'/'unrecognized', and action is 'created' / 'existed' /
    'would-emit' / 'noop'.
    """
    name = path.name
    if name == "answers.md":
        return "skipped", "noop"
    if name == "questions.md":
        if dry_run:
            return "questions", "would-emit"
        _, created = emit_consultation_questions(store, path)
        return "questions", "created" if created else "existed"
    if name == "assessment.md":
        if dry_run:
            return "assessment", "would-emit"
        _, created = emit_consultation_assessment(store, path)
        return "assessment", "created" if created else "existed"
    if ANSWER_RE.match(name):
        if dry_run:
            return "answer", "would-emit"
        _, created = emit_consultation_answer(store, path)
        return "answer", "created" if created else "existed"
    return "unrecognized", "noop"


def main():
    ap = argparse.ArgumentParser(
        description="Backfill consultation substrate classifiers."
    )
    ap.add_argument("--min-asn", type=int, default=34,
                    help="Lowest ASN number to backfill (inclusive). "
                         "Default 34 — matches the 'ASN-34+ is what "
                         "matters' policy on xanadu. Pass --min-asn 1 "
                         "to include all ASNs (use for materials).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Walk and classify-by-name without filing any "
                         "substrate links. Reports what it would do.")
    args = ap.parse_args()

    print(f"  Lattice: {LATTICE_NAME}", file=sys.stderr)
    print(f"  Consultation dir: {CONSULTATION_DIR.relative_to(LATTICE.parent.parent)}",
          file=sys.stderr)
    if not CONSULTATION_DIR.exists():
        print(f"  Nothing here — no consultations to backfill.", file=sys.stderr)
        sys.exit(0)

    asn_dirs = []
    for asn_dir in sorted(CONSULTATION_DIR.iterdir()):
        if not asn_dir.is_dir():
            continue
        m = ASN_RE.match(asn_dir.name)
        if not m:
            continue
        asn_num = int(m.group(1))
        if asn_num < args.min_asn:
            continue
        asn_dirs.append(asn_dir)

    print(f"  In scope (ASN >= {args.min_asn}): {len(asn_dirs)} ASN dirs",
          file=sys.stderr)
    if args.dry_run:
        print(f"  DRY RUN — no substrate links will be filed.", file=sys.stderr)

    counts = {
        "questions": {"created": 0, "existed": 0, "would-emit": 0},
        "answer":    {"created": 0, "existed": 0, "would-emit": 0},
        "assessment":{"created": 0, "existed": 0, "would-emit": 0},
    }
    skipped = 0
    unrecognized = []

    with default_store() as store:
        for asn_dir in asn_dirs:
            for session_dir in sorted(asn_dir.iterdir()):
                if not session_dir.is_dir():
                    continue
                if session_dir.name == "sessions":
                    continue  # per-call transcripts; not in this backfill's scope
                for f in sorted(session_dir.iterdir()):
                    if not f.is_file():
                        continue
                    kind, action = classify_one(store, f, args.dry_run)
                    if kind == "skipped":
                        skipped += 1
                    elif kind == "unrecognized":
                        unrecognized.append(f.relative_to(LATTICE))
                    else:
                        counts[kind][action] += 1

    print(f"\n  Classifier links:", file=sys.stderr)
    for kind in ("questions", "answer", "assessment"):
        c = counts[kind]
        if args.dry_run:
            print(f"    {kind:12s}: would-emit {c['would-emit']:>4d}",
                  file=sys.stderr)
        else:
            total = c["created"] + c["existed"]
            print(f"    {kind:12s}: {total:>4d} total ({c['created']} new, "
                  f"{c['existed']} already classified)", file=sys.stderr)

    if skipped:
        print(f"    skipped     : {skipped:>4d} (answers.md — workspace-shaped, "
              f"not classified per policy)", file=sys.stderr)
    if unrecognized:
        print(f"\n  Unrecognized files (not classified, not skipped — review):",
              file=sys.stderr)
        for u in unrecognized:
            print(f"    {u}", file=sys.stderr)


if __name__ == "__main__":
    main()
