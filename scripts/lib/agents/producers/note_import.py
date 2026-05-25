"""Note-import producer — promote an external doc into the note set.

Operator-gated pure producer. One fire = promote a workspace import
spec md to a substrate-citizen `import` doc, copy a source doc from
anywhere in the repo into the note set under a new ASN identity,
emit the new note's `note` classifier, register the operator's
declared `citation.depends` edges, and emit `provenance.import` for
the audit trail.

Source disposition: **leave in place**. The source doc stays where it
is; the new note is a fresh copy that subsequently diverges as the
review/revise cycle refines it. The two may drift over time.

Used when an existing reference doc (e.g., `docs/protocols/...`)
should enter the lattice as a derived note for further refinement.

Caste: pure producer (one-shot identity grant). Identity grants per
fire:

  - `import` classifier on the spec doc (workspace → substrate)
  - `note` classifier on the new note
  - `citation.depends` edges on the new note for each declared dep
  - `provenance.import(F=[spec_doc], G=[new_note])` lineage fact

Operator workflow:

  1. Drop a spec md into `_workspace/imports/<filename>.md`:

     ```yaml
     ---
     create_note: 86
     title: "Substrate Type Registry"
     source_doc: "docs/protocols/substrate/types.md"
     depends: [34, 36, 43]
     ---

     # Why I'm importing this doc

     [Operator's rationale prose...]
     ```

  2. Run `python scripts/note-import.py --spec <filename>`.
  3. New note goes through the standard runner walk like any new note.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation_bundle, emit_import, emit_note, emit_provenance_import,
)
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import format_label
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.git_ops import step_commit
from lib.shared.paths import (
    DOCUVERSE_DIR, IMPORT_DIR, IMPORT_INBOX, LATTICE, NOTE_DIR, WORKSPACE,
)


def _slugify(title: str) -> str:
    """Convert a title to a filename-safe slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-") or "untitled"


# ─── Spec promotion (workspace → substrate) ────────────────────────


def _promote_spec_to_substrate(
    session: Session, spec_filename: str,
):
    """Copy workspace spec md into substrate, register, emit `import`
    classifier. Returns (substrate_path, spec_addr) or None."""
    workspace_path = IMPORT_INBOX / spec_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Import spec not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    substrate_path = IMPORT_DIR / spec_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(substrate_path.resolve().relative_to(WORKSPACE.resolve()))
    spec_addr = session.store.register_path(substrate_rel)
    emit_import(session.store, spec_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, spec_addr


# ─── Validation ────────────────────────────────────────────────────


def _validate(
    create_note: int, title: str, source_doc: str,
) -> Tuple[Path, str, str] | None:
    """Confirm target ASN slot is free and source doc exists.
    Returns (source_path, new_label, slug) or None.
    """
    new_label = format_label(create_note)
    slug = _slugify(title)

    if list(NOTE_DIR.glob(f"{new_label}-*.md")):
        print(f"  [ERROR] {new_label} note already exists", file=sys.stderr)
        return None

    source_path = (WORKSPACE / source_doc).resolve()
    if not source_path.exists():
        print(
            f"  [ERROR] Source doc not found: {source_doc}",
            file=sys.stderr,
        )
        return None
    if source_path.suffix != ".md":
        print(
            f"  [ERROR] Source doc must be a .md file: {source_doc}",
            file=sys.stderr,
        )
        return None
    if not source_path.is_relative_to(WORKSPACE.resolve()):
        print(
            f"  [ERROR] Source doc must live inside the repo: {source_doc}",
            file=sys.stderr,
        )
        return None
    if source_path.is_relative_to((WORKSPACE / "_docuverse").resolve()):
        try:
            rel = source_path.relative_to(WORKSPACE.resolve())
            if "/note/" in str(rel):
                print(
                    f"  [ERROR] Source doc is already a note: {source_doc}",
                    file=sys.stderr,
                )
                return None
        except ValueError:
            pass

    return source_path, new_label, slug


# ─── Note materialization ──────────────────────────────────────────


def _copy_source_to_note(
    source_path: Path, new_label: str, slug: str, title: str,
) -> Path:
    """Copy source doc to the note path. Replace the H1 with the
    operator-declared title (so the new note opens cleanly).
    """
    note_path = NOTE_DIR / f"{new_label}-{slug}.md"
    content = source_path.read_text()

    # If the source has an H1 on the first non-blank line, replace
    # it. Otherwise prepend.
    lines = content.split("\n")
    h1_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            h1_idx = i
            break
        if line.strip():
            break
    new_h1 = f"# {new_label}: {title}"
    if h1_idx is not None:
        lines[h1_idx] = new_h1
        content = "\n".join(lines)
    else:
        content = f"{new_h1}\n\n{content}"

    note_path.write_text(content)
    print(
        f"  [COPIED] {source_path.relative_to(WORKSPACE.resolve())} → "
        f"{note_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return note_path


# ─── Substrate emission ────────────────────────────────────────────


def _emit_substrate(
    session: Session,
    *,
    spec_addr: Address,
    note_path: Path,
    depends: List[int],
) -> Address:
    """Register the new note, emit classifier + citation.depends edges +
    provenance.import lineage. Returns the new note's address.
    """
    from lib.shared.common import find_asn
    note_rel = str(note_path.relative_to(WORKSPACE))
    note_addr = session.store.register_path(note_rel)
    emit_note(session.store, note_addr)

    dep_addrs = []
    for dep_asn_id in depends:
        dep_path, _ = find_asn(str(dep_asn_id))
        if dep_path is None:
            print(
                f"  [WARN] dep ASN-{dep_asn_id:04d} not found, skipping",
                file=sys.stderr,
            )
            continue
        dep_rel = str(dep_path.resolve().relative_to(WORKSPACE.resolve()))
        dep_addr = session.store.path_to_addr.get(dep_rel)
        if dep_addr is None:
            print(
                f"  [WARN] dep ASN-{dep_asn_id:04d} ({dep_rel}) "
                f"has no substrate address, skipping",
                file=sys.stderr,
            )
            continue
        dep_addrs.append(dep_addr)
    if dep_addrs:
        # Fan-out citation.depends from note_addr — imports have no
        # inquiry, so the LEGACY note-side direction is correct here
        # (loader's fallback handles this case explicitly).
        emit_citation_bundle(
            session.store, note_addr, dep_addrs, direction="depends",
        )

    emit_provenance_import(session.store, spec_addr, note_addr)
    return note_addr


# ─── Staging for commit ────────────────────────────────────────────


def _stage_for_commit(substrate_spec_path: Path, note_path: Path) -> None:
    """Stage the import's emitted files so `scripts/commit.py` can
    commit them. Scoped to the four files this fire actually wrote:
    the substrate spec, the new note, and the two substrate metadata
    files (`links.jsonl`, `paths.json`) that accumulate emissions.

    The commit prompt explicitly says callers must stage; without this,
    the LLM sees an empty cached diff and reports done without
    committing. Substrate state ends up ahead of git until a later
    commit picks up the residue.
    """
    paths = [
        str(substrate_spec_path.resolve().relative_to(WORKSPACE.resolve())),
        str(note_path.resolve().relative_to(WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "links.jsonl").resolve().relative_to(
            WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "paths.json").resolve().relative_to(
            WORKSPACE.resolve())),
    ]
    subprocess.run(
        ["git", "add"] + paths,
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )


# ─── Agent class ───────────────────────────────────────────────────


class NoteImportAgent(Agent):
    """One import per fire — pure producer (operator-gated).

    Reads operator intent from a workspace spec md (create_note /
    title / source_doc / depends + rationale), promotes the spec to
    substrate, copies the named source doc into the note set under
    the chosen ASN identity, emits the `note` classifier and the
    declared `citation.depends` edges, and emits `provenance.import`
    for the audit trail. No LLM call.

    The source doc stays in place. The new note diverges from the
    source as the review/revise cycle refines it.
    """

    role: ClassVar[str] = "note-import"

    def run(
        self, session: Session, addr: Address,
        *, spec_filename: str,
    ) -> AgentResult:
        # Operator-gated: addr is unused (the spec doc carries the
        # source/target). Accepted to match Agent dispatch surface.
        del addr

        # 1. Promote workspace spec → substrate
        promotion = _promote_spec_to_substrate(session, spec_filename)
        if promotion is None:
            return AgentResult(success=False, detail="spec-not-in-workspace")
        substrate_path, spec_addr = promotion

        # 2. Parse spec frontmatter
        fm, _body = read_doc_with_frontmatter(substrate_path)
        try:
            create_note = int(fm["create_note"])
            title = str(fm["title"]).strip()
            source_doc = str(fm["source_doc"]).strip()
        except (KeyError, ValueError, TypeError) as e:
            return AgentResult(
                success=False,
                detail=f"spec-frontmatter-malformed: {e}",
            )
        depends_raw = fm.get("depends", [])
        if not isinstance(depends_raw, list):
            return AgentResult(
                success=False,
                detail="spec-frontmatter-malformed: depends must be a list",
            )
        try:
            depends = [int(d) for d in depends_raw]
        except (ValueError, TypeError) as e:
            return AgentResult(
                success=False,
                detail=f"spec-frontmatter-malformed: depends contains non-int: {e}",
            )

        # 3. Validate
        validated = _validate(create_note, title, source_doc)
        if validated is None:
            return AgentResult(success=False, detail="validation-failed")
        source_path, new_label, slug = validated

        os.environ.setdefault("PROTOCOL_ASN_LABEL", new_label)

        print(
            f"  [IMPORT] {source_doc} → {new_label} ({title})",
            file=sys.stderr,
        )

        # 4. Copy source doc into note dir (with H1 retitled)
        note_path = _copy_source_to_note(source_path, new_label, slug, title)

        # 5. Substrate emission
        note_addr = _emit_substrate(
            session,
            spec_addr=spec_addr,
            note_path=note_path,
            depends=depends,
        )
        print(
            f"  [LINEAGE] provenance.import spec → {new_label}",
            file=sys.stderr,
        )
        if depends:
            print(
                f"  [DEPS] citation.depends → "
                f"{', '.join(f'ASN-{d:04d}' for d in depends)}",
                file=sys.stderr,
            )

        # 6. Stage + commit. `scripts/commit.py` expects the caller to
        # have already staged the files it wants committed (per the
        # commit prompt: "staging is handled by the caller"). Without
        # this, the LLM-driven commit step sees an empty cached diff
        # and reports done without actually committing.
        _stage_for_commit(substrate_path, note_path)
        step_commit(f"import(asn): {source_doc} → {new_label} ({title})")

        return AgentResult(
            success=True,
            detail=f"imported={source_doc} as={new_label}",
        )
