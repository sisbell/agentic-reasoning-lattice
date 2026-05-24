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

Deps handling: declare the new ASN's deps either in the source
inquiry's frontmatter ahead of time (`depends: [34, 36, ...]`) or
via `--depends 34,36,...` on this CLI. The migrator writes the
declared deps into the new inquiry's frontmatter and emits
substrate `citation.depends` links from the new inquiry. If the
source inquiry already has a `depends:` field and `--depends` is
not given, it carries forward unchanged.

Usage:
    python scripts/asn-migrate.py --from 59 --to 89
    python scripts/asn-migrate.py --from 59 --to 89 --depends 34,36,47,53,58,82
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
    emit_citation_bundle, emit_consultation_answer, emit_consultation_coverage,
    emit_consultation_questions, emit_inquiry,
)
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.git_ops import step_commit
from lib.shared.paths import (
    CONSULTATIONS_DIR, DOCUVERSE_DIR, INQUIRY_DIR, LATTICE, NOTE_DIR, WORKSPACE,
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


def _resolve_depends(old_inquiry: Path, cli_depends: str | None) -> list[int]:
    """Determine the deps list for the new inquiry.

    Precedence: CLI flag overrides; else inherit from source inquiry's
    frontmatter; else empty (operator can add later via editing the
    new inquiry md + running asn-sync-deps).
    """
    if cli_depends:
        try:
            return sorted({int(x) for x in cli_depends.split(",") if x.strip()})
        except ValueError as e:
            raise SystemExit(f"invalid --depends list: {cli_depends!r} ({e})")
    fm, _body = read_doc_with_frontmatter(old_inquiry)
    raw = (fm or {}).get("depends")
    if not raw:
        return []
    try:
        return sorted({int(x) for x in raw})
    except (ValueError, TypeError) as e:
        raise SystemExit(
            f"source inquiry has malformed depends: {raw!r} ({e})"
        )


def _write_depends_into_inquiry(new_inquiry: Path, deps: list[int]) -> None:
    """Inject `depends: [...]` into the new inquiry's YAML frontmatter.

    Idempotent: replaces an existing `depends:` line if present;
    otherwise inserts before the closing `---`.
    """
    text = new_inquiry.read_text()
    deps_line = f"depends: [{', '.join(str(d) for d in deps)}]"
    if re.search(r"^depends:\s*\[.*?\]\s*$", text, re.MULTILINE):
        new_text = re.sub(
            r"^depends:\s*\[.*?\]\s*$", deps_line, text,
            count=1, flags=re.MULTILINE,
        )
    else:
        # Insert before the second `---` (close of frontmatter).
        new_text = re.sub(
            r"(^---\s*\n.*?)(\n---\s*$)",
            lambda m: m.group(1) + "\n" + deps_line + m.group(2),
            text, count=1, flags=re.DOTALL | re.MULTILINE,
        )
    new_inquiry.write_text(new_text)


def _find_note_base_addr(store, asn_num: int):
    """Find the BASE/identity address of a dep ASN's note."""
    label = format_label(asn_num)
    prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    for path, addr in store.path_to_addr.items():
        if path.startswith(prefix) and not path.endswith(".statements.md"):
            return addr
    return None


def migrate(
    old_num: int, new_num: int,
    dry_run: bool = False, depends: str | None = None,
) -> int:
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
    declared_deps = _resolve_depends(old_inquiry, depends)

    print(f"  [MIGRATE] {old_label} → {new_label}", file=sys.stderr)
    print(f"    inquiry: {old_inquiry.name}", file=sys.stderr)
    print(
        f"    questions.md: {'yes' if questions_file.exists() else 'no'}",
        file=sys.stderr,
    )
    print(f"    answer files: {len(answer_files)}", file=sys.stderr)
    if declared_deps:
        print(
            f"    depends: {', '.join(f'ASN-{d:04d}' for d in declared_deps)}",
            file=sys.stderr,
        )
    else:
        print(
            f"    depends: (none — set in inquiry md + run asn-sync-deps "
            f"later if needed)",
            file=sys.stderr,
        )

    if dry_run:
        print("    [DRY RUN] no changes made", file=sys.stderr)
        return 0

    # Copy
    shutil.copy2(old_inquiry, new_inquiry)
    shutil.copytree(old_consult_dir, new_consult_dir)
    if declared_deps:
        _write_depends_into_inquiry(new_inquiry, declared_deps)

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

        # citation.depends fan-out from new inquiry → declared dep
        # notes' BASE addresses. One bundled link in the FanOutPair
        # shape per the 2026-05-24 reconciliation; loads cleanly via
        # the new substrate-only foundation loader.
        if declared_deps:
            dep_addrs = []
            for dep_id in declared_deps:
                dep_addr = _find_note_base_addr(store, dep_id)
                if dep_addr is None:
                    print(
                        f"    [WARN] dep ASN-{dep_id:04d} note not found; "
                        f"skipping",
                        file=sys.stderr,
                    )
                    continue
                dep_addrs.append(dep_addr)
            if dep_addrs:
                emit_citation_bundle(
                    store, new_inquiry_addr, dep_addrs,
                    direction="depends",
                )
                print(
                    f"    emitted citation.depends fan-out: "
                    f"{len(dep_addrs)}/{len(declared_deps)} targets",
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
        "--depends", default=None,
        help="Comma-separated dep ASN numbers (e.g., 34,36,47,53,58,82). "
             "Overrides any `depends:` in the source inquiry's frontmatter. "
             "If omitted, falls back to the source inquiry's `depends:` (if "
             "present) — else no deps are declared and operator can add "
             "them later via editing the new inquiry md + asn-sync-deps.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would migrate without making changes",
    )
    args = parser.parse_args()
    return migrate(
        args.src, args.dst,
        dry_run=args.dry_run, depends=args.depends,
    )


if __name__ == "__main__":
    sys.exit(main())
