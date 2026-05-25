"""Note-clone producer — duplicate an ASN under a new ASN number.

Operator-gated pure producer. One fire = promote a workspace clone
spec md to a substrate-citizen `clone` doc, copy the source's note
md / inquiry doc / consultation directory under a new ASN identity,
mirror citation.depends edges, emit lineage. Both ASNs live as
peers afterward, with `provenance.clone` recording where the new
one came from.

Used when an existing ASN already has expensive consultation work
attached and you want to tweak it without disturbing the original.
This is NOT supersession — supersession is for version replacement
(head replaces predecessor); a clone keeps both alive.

Caste: pure producer (one-shot identity grant). Identity grants per
fire:

  - `clone` classifier on the spec doc (workspace → substrate)
  - `note` classifier on the new clone note
  - `inquiry` classifier on the new inquiry doc (if source had one)
  - `provenance.clone(F=[origin], G=[clone])` lineage fact
  - Mirrored `citation.depends` from origin → clone (note-level
    and inquiry-level)

Operator workflow:

  1. Drop a spec md into `_workspace/clones/<filename>.md`:

     ```yaml
     ---
     clone_from: 48
     create_note: 59
     ---

     # Why I'm cloning ASN-48

     [Operator's rationale: what experiment, what hypothesis,
      why preserve the original, etc.]
     ```

  2. Run `python scripts/note-clone.py --spec <filename>`.
  3. Clone goes through standard runner walk like any new note.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation_bundle, emit_clone, emit_inquiry, emit_note,
    emit_provenance_clone,
)
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import format_label
from lib.shared.common import find_asn
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.git_ops import step_commit
from lib.shared.paths import (
    CLONE_DIR, CLONE_INBOX, CONSULTATIONS_DIR, LATTICE, NOTE_DIR,
    WORKSPACE, inquiry_doc_path,
)


# ─── Spec promotion (workspace → substrate) ────────────────────────


def _promote_spec_to_substrate(
    session: Session, spec_filename: str,
):
    """Copy workspace spec md into substrate, register, emit `clone`
    classifier. Returns (substrate_path, spec_addr) or None."""
    workspace_path = CLONE_INBOX / spec_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Clone spec not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    CLONE_DIR.mkdir(parents=True, exist_ok=True)
    substrate_path = CLONE_DIR / spec_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(substrate_path.resolve().relative_to(WORKSPACE.resolve()))
    spec_addr = session.store.register_path(substrate_rel)
    emit_clone(session.store, spec_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, spec_addr


# ─── Validation ────────────────────────────────────────────────────


def _validate(
    clone_from: int, create_note: int,
) -> Tuple[Path, str, str] | None:
    """Confirm origin exists, target doesn't. Returns
    (origin_path, origin_label, clone_label) or None."""
    origin_label = format_label(clone_from)
    clone_label = format_label(create_note)

    origin_path, _ = find_asn(str(clone_from))
    if origin_path is None:
        print(f"  [ERROR] {origin_label} note not found", file=sys.stderr)
        return None

    if list(NOTE_DIR.glob(f"{clone_label}-*.md")):
        print(f"  [ERROR] {clone_label} note already exists", file=sys.stderr)
        return None
    if inquiry_doc_path(create_note).exists():
        print(
            f"  [ERROR] {clone_label} inquiry already exists",
            file=sys.stderr,
        )
        return None

    return origin_path, origin_label, clone_label


# ─── Mechanical copies (no LLM) ────────────────────────────────────


def _copy_note_md(
    origin_path: Path, origin_label: str, clone_label: str,
) -> Path:
    """Copy origin note md to clone-named path. Returns clone path."""
    new_name = origin_path.name.replace(origin_label, clone_label, 1)
    clone_path = origin_path.parent / new_name
    content = origin_path.read_text().replace(origin_label, clone_label)
    clone_path.write_text(content)
    print(
        f"  [COPIED] {origin_path.relative_to(WORKSPACE)} → "
        f"{clone_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return clone_path


def _copy_inquiry_doc(
    clone_from: int, create_note: int,
    origin_label: str, clone_label: str,
) -> Path | None:
    """Copy origin inquiry doc with label substitution. Returns clone
    inquiry path or None if origin had no inquiry."""
    origin_inquiry = inquiry_doc_path(clone_from)
    clone_inquiry = inquiry_doc_path(create_note)
    if not origin_inquiry.exists():
        print(f"  [SKIP] No inquiry doc for {origin_label}", file=sys.stderr)
        return None

    content = origin_inquiry.read_text().replace(origin_label, clone_label)
    clone_inquiry.parent.mkdir(parents=True, exist_ok=True)
    clone_inquiry.write_text(content)
    print(
        f"  [COPIED] {origin_inquiry.relative_to(WORKSPACE)} → "
        f"{clone_inquiry.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return clone_inquiry


def _copy_consultations(origin_label: str, clone_label: str) -> bool:
    """Copy origin consultation directory with label substitution."""
    origin_consult = CONSULTATIONS_DIR / origin_label / "consultation"
    clone_consult = CONSULTATIONS_DIR / clone_label / "consultation"

    if not origin_consult.exists():
        print(
            f"  [SKIP] No consultations for {origin_label}",
            file=sys.stderr,
        )
        return False

    if clone_consult.exists():
        shutil.rmtree(clone_consult)
    shutil.copytree(origin_consult, clone_consult)

    copied = 0
    for filepath in clone_consult.rglob("*.md"):
        text = filepath.read_text()
        if origin_label in text:
            filepath.write_text(text.replace(origin_label, clone_label))
        copied += 1

    print(
        f"  [COPIED] consultation ({copied} files) → "
        f"{clone_consult.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return True


# ─── Substrate emission ────────────────────────────────────────────


def _emit_substrate(
    session: Session,
    *,
    origin_note_path: Path, clone_note_path: Path,
    origin_inquiry_path: Path | None, clone_inquiry_path: Path | None,
) -> Tuple[Address, Address | None]:
    """Register clone docs, emit classifiers, mirror citation.depends,
    record provenance.clone lineage. Returns (clone_note_addr,
    clone_inquiry_addr | None)."""
    origin_note_rel = str(origin_note_path.relative_to(WORKSPACE))
    clone_note_rel = str(clone_note_path.relative_to(WORKSPACE))

    origin_note_addr = session.get_addr_for_path(origin_note_rel)
    clone_note_addr = session.store.register_path(clone_note_rel)
    emit_note(session.store, clone_note_addr)
    emit_provenance_clone(session.store, origin_note_addr, clone_note_addr)

    clone_inquiry_addr = None
    if origin_inquiry_path is not None and clone_inquiry_path is not None:
        origin_inquiry_addr = session.get_addr_for_path(
            str(origin_inquiry_path.relative_to(WORKSPACE)),
        )
        clone_inquiry_addr = session.store.register_path(
            str(clone_inquiry_path.relative_to(WORKSPACE)),
        )
        emit_inquiry(session.store, clone_inquiry_addr)

        if origin_inquiry_addr is not None:
            for link in session.active_links(
                "citation.depends", from_set=[origin_inquiry_addr],
            ):
                # Preserve the origin link's to_set shape — if origin
                # was fan-out, clone is fan-out; if origin was a single
                # pair, clone is a single pair (a 1-target bundle is
                # still valid under FanOutPair). Base→base convention;
                # version drift handled at load time.
                if link.to_set:
                    emit_citation_bundle(
                        session.store, clone_inquiry_addr,
                        list(link.to_set), direction="depends",
                    )

    if origin_note_addr is not None:
        for link in session.active_links(
            "citation.depends", from_set=[origin_note_addr],
        ):
            if link.to_set:
                emit_citation_bundle(
                    session.store, clone_note_addr,
                    list(link.to_set), direction="depends",
                )

    return clone_note_addr, clone_inquiry_addr


# ─── Agent class ───────────────────────────────────────────────────


class NoteCloneAgent(Agent):
    """One clone per fire — pure producer (operator-gated).

    Reads operator intent from a workspace spec md (clone_from /
    create_note + rationale), promotes the spec to substrate,
    mechanically copies the origin's note / inquiry / consultations
    under a new ASN identity, mirrors citation.depends, emits lineage
    via provenance.clone. No LLM call; this is structured copy.
    """

    role: ClassVar[str] = "note-clone"

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
        substrate_path, _spec_addr = promotion

        # 2. Parse spec frontmatter
        fm, _body = read_doc_with_frontmatter(substrate_path)
        try:
            clone_from = int(fm["clone_from"])
            create_note = int(fm["create_note"])
        except (KeyError, ValueError, TypeError) as e:
            return AgentResult(
                success=False,
                detail=f"spec-frontmatter-malformed: {e}",
            )

        # 3. Validate
        validated = _validate(clone_from, create_note)
        if validated is None:
            return AgentResult(success=False, detail="validation-failed")
        origin_path, origin_label, clone_label = validated

        os.environ.setdefault("PROTOCOL_ASN_LABEL", clone_label)

        print(
            f"  [CLONE] {origin_label} → {clone_label}",
            file=sys.stderr,
        )

        # 4. Mechanical copies
        clone_note_path = _copy_note_md(origin_path, origin_label, clone_label)
        clone_inquiry_path = _copy_inquiry_doc(
            clone_from, create_note, origin_label, clone_label,
        )
        _copy_consultations(origin_label, clone_label)

        origin_inquiry_path = inquiry_doc_path(clone_from)
        if not origin_inquiry_path.exists():
            origin_inquiry_path = None
            clone_inquiry_path = None

        # 5. Substrate emission
        _emit_substrate(
            session,
            origin_note_path=origin_path,
            clone_note_path=clone_note_path,
            origin_inquiry_path=origin_inquiry_path,
            clone_inquiry_path=clone_inquiry_path,
        )
        print(
            f"  [LINEAGE] provenance.clone {origin_label} → {clone_label}",
            file=sys.stderr,
        )

        # 6. Commit
        step_commit(f"clone(asn): {origin_label} → {clone_label}")

        return AgentResult(
            success=True,
            detail=f"cloned={origin_label} as={clone_label}",
        )
