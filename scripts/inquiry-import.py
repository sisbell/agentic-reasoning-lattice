#!/usr/bin/env python3
"""Inquiry-import CLI — promote a workspace inquiry draft into the substrate.

The operator:
  1. Drops an inquiry md into `_workspace/inquiries/<filename>.md`.
     The filename should be `asn-NNNN-<description>.md` (NNNN is the
     ASN number). Frontmatter must include title, question, and
     depends.
  2. Runs `python scripts/inquiry-import.py --asn NNNN`
     (or `--spec <filename>` to be explicit about the source file).

Example workspace inquiry:

    ---
    title: CREATENEWDOCUMENT Operation
    out_of_scope: forking (CREATENEWVERSION), ...
    question: What happens when a user creates a new document under
      an account? What is allocated, what is preserved about existing
      documents and the content store, ...?
    depends: [34, 36, 40, 42, 45, 47, 93]
    ---

    # Inquiry: CREATENEWDOCUMENT Operation

What this does (mechanical, no LLM):

  - Copies the spec into the substrate at
    `_docuverse/documents/1.1/1/inquiry/ASN-NNNN.md`.
  - Registers the path in `paths.json`.
  - Emits the `inquiry` classifier on the new doc address.
  - Invokes `asn-sync-deps NNNN` to emit the `citation.depends`
    fan-out from the declared `depends:` list (auto-commits).

After this, the next runner pass will see the new inquiry and fire
`inquiry_consult` on it (the first stage of the standard pipeline:
inquiry → consult → draft → review → revise → ...).

What this is NOT:

  - Not for cloning an existing ASN: use `scripts/note-clone.py`.
  - Not for migrating an existing ASN to a new number: use
    `scripts/asn-migrate.py`.
  - Not for promoting an open question from a parent ASN: use
    `scripts/promote-open-questions.py`.
  - Not for importing a doc straight as a note: use
    `scripts/note-import.py`.

This is the missing "fresh inquiry from a workspace draft" tool,
mirroring the inbox pattern of `note-import` and `note-clone`.

Usage:
    python scripts/inquiry-import.py --asn 103
    python scripts/inquiry-import.py --spec asn-0103-createnewdocument.md
    python scripts/inquiry-import.py --asn 103 --dry-run
    python scripts/inquiry-import.py --asn 103 --force   # overwrite target
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_inquiry
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE, WORKSPACE, inquiry_doc_path


INQUIRY_INBOX = WORKSPACE / "_workspace" / "inquiries"


def _find_spec(asn_num: int | None, spec_name: str | None) -> Path:
    """Resolve which file in the inbox to import."""
    if spec_name:
        p = INQUIRY_INBOX / spec_name
        if not p.exists():
            raise SystemExit(
                f"  [ERROR] spec not found: {p.relative_to(WORKSPACE)}"
            )
        return p
    if asn_num is not None:
        pattern = f"asn-{asn_num:04d}-*.md"
        matches = sorted(INQUIRY_INBOX.glob(pattern))
        if not matches:
            raise SystemExit(
                f"  [ERROR] no spec found matching {pattern} in "
                f"{INQUIRY_INBOX.relative_to(WORKSPACE)}"
            )
        if len(matches) > 1:
            names = ", ".join(p.name for p in matches)
            raise SystemExit(
                f"  [ERROR] multiple specs match {pattern}: {names}. "
                f"Use --spec to pick one."
            )
        return matches[0]
    raise SystemExit("  [ERROR] must specify either --asn or --spec")


def _parse_asn_from_filename(spec_path: Path) -> int:
    """Extract NNNN from filenames like asn-NNNN-<desc>.md."""
    m = re.match(r"asn-(\d+)", spec_path.stem)
    if not m:
        raise SystemExit(
            f"  [ERROR] cannot extract ASN number from filename: "
            f"{spec_path.name}. Use --asn to specify explicitly."
        )
    return int(m.group(1))


def _validate_frontmatter(spec_path: Path) -> dict:
    """Lightweight frontmatter validation. Returns parsed dict.

    Requires `title`, `question`, `depends`. Other fields permitted.
    """
    import yaml
    text = spec_path.read_text()
    if not text.startswith("---\n"):
        raise SystemExit(
            f"  [ERROR] {spec_path.name}: missing YAML frontmatter"
        )
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        raise SystemExit(
            f"  [ERROR] {spec_path.name}: unterminated frontmatter"
        )
    fm = yaml.safe_load(text[4:end])
    if not isinstance(fm, dict):
        raise SystemExit(
            f"  [ERROR] {spec_path.name}: frontmatter is not a mapping"
        )
    required = ["title", "question", "depends"]
    missing = [f for f in required if f not in fm]
    if missing:
        raise SystemExit(
            f"  [ERROR] {spec_path.name}: frontmatter missing required "
            f"fields {missing}"
        )
    if not isinstance(fm["depends"], list) or not all(
        isinstance(d, int) for d in fm["depends"]
    ):
        raise SystemExit(
            f"  [ERROR] {spec_path.name}: `depends:` must be a list "
            f"of ASN numbers (integers)"
        )
    return fm


def import_inquiry(
    asn_num: int,
    spec_path: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> int:
    asn_label = format_label(asn_num)
    target_path = inquiry_doc_path(asn_num)

    if target_path.exists() and not force:
        print(
            f"  [{asn_label}] target already exists at "
            f"{target_path.relative_to(WORKSPACE)} — refusing to "
            f"overwrite (use --force to override).",
            file=sys.stderr,
        )
        return 1

    fm = _validate_frontmatter(spec_path)
    print(
        f"  [{asn_label}] spec:    {spec_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    print(f"  [{asn_label}] title:   {fm['title']}", file=sys.stderr)
    print(f"  [{asn_label}] depends: {fm['depends']}", file=sys.stderr)
    print(
        f"  [{asn_label}] target:  {target_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )

    if dry_run:
        print(
            f"  [{asn_label}] [DRY RUN] would copy → register → emit "
            f"inquiry → asn-sync-deps {asn_num}",
            file=sys.stderr,
        )
        return 0

    # Step 1: Copy spec to docuverse
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(spec_path, target_path)
    print(
        f"  [{asn_label}] copied → {target_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )

    # Step 2: Register path + emit `inquiry` classifier
    with open_session(LATTICE) as session:
        rel = str(target_path.resolve().relative_to(WORKSPACE.resolve()))
        inquiry_addr = session.store.register_path(rel)
        emit_inquiry(session.store, inquiry_addr)
        print(
            f"  [{asn_label}] registered as {inquiry_addr}, "
            f"emitted `inquiry` classifier",
            file=sys.stderr,
        )

    # Step 3: Emit citation.depends fan-out via asn-sync-deps
    # (asn-sync-deps auto-commits, capturing all three steps together)
    print(
        f"  [{asn_label}] invoking asn-sync-deps to emit dep fan-out...",
        file=sys.stderr,
    )
    result = subprocess.run(
        [sys.executable, "scripts/asn-sync-deps.py", str(asn_num)],
        cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(
            f"  [{asn_label}] [WARN] asn-sync-deps returned non-zero "
            f"exit ({result.returncode}); inquiry registered but deps "
            f"may not be reconciled. Re-run "
            f"`python3 scripts/asn-sync-deps.py {asn_num}` manually.",
            file=sys.stderr,
        )
        return 1

    print(f"  [{asn_label}] imported successfully", file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--asn", type=int,
        help="ASN number to import (looks up `asn-NNNN-*.md` in inbox)",
    )
    group.add_argument(
        "--spec",
        help="Spec filename in _workspace/inquiries/ (e.g. asn-0103-foo.md)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would happen without writing or emitting",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing inquiry at the target path",
    )
    args = parser.parse_args()

    spec_path = _find_spec(asn_num=args.asn, spec_name=args.spec)
    asn_num = args.asn if args.asn is not None else _parse_asn_from_filename(
        spec_path
    )
    return import_inquiry(
        asn_num, spec_path, dry_run=args.dry_run, force=args.force,
    )


if __name__ == "__main__":
    sys.exit(main())
