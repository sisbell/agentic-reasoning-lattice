#!/usr/bin/env python3
"""Migrate inquiry + consultation tree from old ASN number to new ASN.

Mechanical operator-driven copy: brings over the inquiry md file and
the entire consultation tree (questions, answers, per-cycle
assessments), re-registers all paths in the substrate under the new
ASN identity, and re-emits the substrate facts (`inquiry`,
`consultation.questions`, `consultation.answer.<role>`,
`consultation.coverage`) so the runner's `note_draft` trigger can
fire on the new inquiry and synthesize a fresh note from the existing
(expensive) consultation answers — without re-running consultation.

What this is FOR:
  - Reincarnating a retired ASN under a fresh number while preserving
    the LLM-generated consultation answers that informed the original
    discovery.
  - The old inquiry/consultation directories are left untouched
    (audit trail / historical depth).
  - The new inquiry, once registered + linked, becomes a target for
    the runner's note_draft trigger. One cheap LLM call later, a fresh
    note exists in the lattice ready for review/revise cycles.

What this is NOT for:
  - Migrating already-drafted notes. (For that, the note's content
    has been refined through review/revise cycles and is the canonical
    artifact; copy the note md, not the inquiry.)
  - Importing an external doc as a note. (Use scripts/note-import.py.)

Role mapping: legacy `nelson`/`gregory` answer-file role suffixes
map to the current `theory`/`evidence` subtypes per the type
registry (`consultation.answer.theory`, `consultation.answer.evidence`).

Usage:
    python scripts/asn-migrate.py --from 59 --to 89
    python scripts/asn-migrate.py --from 59 --to 89 --dry-run
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import (
    emit_consultation_answer, emit_consultation_coverage,
    emit_consultation_questions, emit_inquiry,
)
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import (
    CONSULTATIONS_DIR, DOCUVERSE_DIR, INQUIRY_DIR, LATTICE, WORKSPACE,
)


# Legacy role → current subtype mapping.
#   nelson  → theory   (Ted Nelson / Literary Machines source)
#   gregory → evidence (Green codebase / implementation source)
# Identity entries pass through for already-modern files.
_ROLE_MAP = {
    "nelson": "theory",
    "gregory": "evidence",
    "theory": "theory",
    "evidence": "evidence",
}


def _stage_for_commit(new_inquiry: Path, new_consult_dir: Path) -> None:
    """Stage the migrated files + substrate metadata so
    `scripts/commit.py`'s LLM-driven commit sees the right cached diff.
    Same pattern as the staging fix in note_import.py — the commit
    prompt explicitly says callers must stage.
    """
    paths = [
        str(new_inquiry.resolve().relative_to(WORKSPACE.resolve())),
        str(new_consult_dir.resolve().relative_to(WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "links.jsonl").resolve().relative_to(
            WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "paths.json").resolve().relative_to(
            WORKSPACE.resolve())),
    ]
    subprocess.run(
        ["git", "add"] + paths,
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )


def migrate(old_num: int, new_num: int, dry_run: bool = False) -> int:
    old_label = format_label(old_num)
    new_label = format_label(new_num)

    old_inquiry = INQUIRY_DIR / f"{old_label}.md"
    old_consult_dir = CONSULTATIONS_DIR / old_label
    if not old_inquiry.exists():
        print(
            f"  [ERROR] old inquiry not found: "
            f"{old_inquiry.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return 1
    if not old_consult_dir.exists():
        print(
            f"  [ERROR] old consultation dir not found: "
            f"{old_consult_dir.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return 1

    new_inquiry = INQUIRY_DIR / f"{new_label}.md"
    new_consult_dir = CONSULTATIONS_DIR / new_label
    if new_inquiry.exists() or new_consult_dir.exists():
        print(
            f"  [ERROR] target already exists for {new_label}; "
            f"refusing to overwrite",
            file=sys.stderr,
        )
        return 1

    # Enumerate what will be migrated
    questions_file = old_consult_dir / "consultation" / "questions.md"
    answer_files = sorted(old_consult_dir.glob("consultation/answer-*.md"))

    print(f"  [MIGRATE] {old_label} → {new_label}", file=sys.stderr)
    print(f"    inquiry: {old_inquiry.name}", file=sys.stderr)
    print(
        f"    questions.md: {'yes' if questions_file.exists() else 'no'}",
        file=sys.stderr,
    )
    print(f"    answer files: {len(answer_files)}", file=sys.stderr)

    if dry_run:
        print("    [DRY RUN] no changes made", file=sys.stderr)
        return 0

    # Copy
    shutil.copy2(old_inquiry, new_inquiry)
    shutil.copytree(old_consult_dir, new_consult_dir)

    # Register + emit substrate
    with open_session(LATTICE) as session:
        store = session.store

        # Inquiry
        inq_rel = str(new_inquiry.resolve().relative_to(WORKSPACE.resolve()))
        new_inquiry_addr = store.register_path(inq_rel)
        emit_inquiry(store, new_inquiry_addr)

        # Questions doc (if present)
        new_questions = new_consult_dir / "consultation" / "questions.md"
        if new_questions.exists():
            q_rel = str(
                new_questions.resolve().relative_to(WORKSPACE.resolve())
            )
            q_addr = store.register_path(q_rel)
            emit_consultation_questions(store, q_addr)
            emit_consultation_coverage(store, q_addr, new_inquiry_addr)

        # Answer docs
        registered, skipped = 0, 0
        for ans in sorted(new_consult_dir.glob("consultation/answer-*.md")):
            m = re.match(r"answer-\d+-(.+)\.md", ans.name)
            if not m:
                print(
                    f"    [WARN] unparseable filename {ans.name!r}; skipping",
                    file=sys.stderr,
                )
                skipped += 1
                continue
            raw_role = m.group(1)
            role = _ROLE_MAP.get(raw_role)
            if role is None:
                print(
                    f"    [WARN] unknown role {raw_role!r} in {ans.name}; "
                    f"skipping classifier+coverage",
                    file=sys.stderr,
                )
                skipped += 1
                continue
            ans_rel = str(ans.resolve().relative_to(WORKSPACE.resolve()))
            ans_addr = store.register_path(ans_rel)
            emit_consultation_answer(store, ans_addr, role)
            emit_consultation_coverage(store, ans_addr, new_inquiry_addr)
            registered += 1
        print(
            f"    registered answers: {registered}, skipped: {skipped}",
            file=sys.stderr,
        )

    # Stage + commit
    _stage_for_commit(new_inquiry, new_consult_dir)
    step_commit(
        f"migrate(asn): {old_label} → {new_label} — "
        f"inquiry + consultation",
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from", dest="src", type=int, required=True,
        help="Old ASN number (e.g., 59)",
    )
    parser.add_argument(
        "--to", dest="dst", type=int, required=True,
        help="New ASN number (e.g., 89)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would migrate without making changes",
    )
    args = parser.parse_args()
    return migrate(args.src, args.dst, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
