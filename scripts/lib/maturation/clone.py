"""
Clone an ASN — duplicate the note, inquiry, consultations, and depends
graph under a new ASN number.

Used when an ASN already has expensive consultation work attached and
you want to tweak it without disturbing the original. Source remains
unchanged; the clone is fully independent thereafter, modulo a
`provenance.clone` audit edge that records where it came from.

This is NOT supersession. The substrate `supersession` link is for
version replacement (head replaces predecessor); a clone keeps both
docs alive as peers.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.backend.emit import (
    emit_citation, emit_clone, emit_inquiry, emit_note,
)
from lib.shared.common import find_asn
from lib.shared.paths import (
    CONSULTATIONS_DIR, INQUIRY_DIR, LATTICE, NOTE_DIR, WORKSPACE,
    inquiry_doc_path,
)


def validate(source_num, target_num):
    """Confirm source exists, target doesn't. Returns (source_label,
    target_label)."""
    source_label = f"ASN-{source_num:04d}"
    target_label = f"ASN-{target_num:04d}"

    source_note, _ = find_asn(str(source_num))
    if source_note is None:
        print(f"  [ERROR] {source_label} note not found", file=sys.stderr)
        sys.exit(1)

    target_note_matches = list(NOTE_DIR.glob(f"{target_label}-*.md"))
    if target_note_matches:
        print(f"  [ERROR] {target_label} note already exists",
              file=sys.stderr)
        sys.exit(1)
    if inquiry_doc_path(target_num).exists():
        print(f"  [ERROR] {target_label} inquiry already exists",
              file=sys.stderr)
        sys.exit(1)

    return source_label, target_label


def copy_note_md(source_num, target_num, source_label, target_label):
    """Copy the source note .md to a target-named path. Returns target path."""
    source_note, _ = find_asn(str(source_num))
    # Replace the ASN-NNNN prefix; keep the slug.
    new_name = source_note.name.replace(source_label, target_label, 1)
    target_path = source_note.parent / new_name

    content = source_note.read_text()
    content = content.replace(source_label, target_label)
    target_path.write_text(content)
    print(f"  [COPIED] {source_note.relative_to(WORKSPACE)} → "
          f"{target_path.relative_to(WORKSPACE)}", file=sys.stderr)
    return target_path


def copy_inquiry_doc(source_num, target_num, source_label, target_label):
    """Copy the source inquiry doc to the target's inquiry path.

    Returns the target inquiry path. Creates the directory if needed.
    """
    source_path = inquiry_doc_path(source_num)
    target_path = inquiry_doc_path(target_num)
    if not source_path.exists():
        print(f"  [SKIP] No inquiry doc for {source_label}",
              file=sys.stderr)
        return None

    content = source_path.read_text()
    content = content.replace(source_label, target_label)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content)
    print(f"  [COPIED] {source_path.relative_to(WORKSPACE)} → "
          f"{target_path.relative_to(WORKSPACE)}", file=sys.stderr)
    return target_path


def copy_consultations(source_label, target_label):
    """Copy entire consultation directory if it exists. Returns True if
    anything was copied."""
    source_consult = CONSULTATIONS_DIR / source_label / "consultation"
    target_consult = CONSULTATIONS_DIR / target_label / "consultation"

    if not source_consult.exists():
        print(f"  [SKIP] No consultations for {source_label}",
              file=sys.stderr)
        return False

    if target_consult.exists():
        shutil.rmtree(target_consult)
    shutil.copytree(source_consult, target_consult)

    copied = 0
    for filepath in target_consult.rglob("*.md"):
        text = filepath.read_text()
        if source_label in text:
            filepath.write_text(text.replace(source_label, target_label))
        copied += 1

    print(f"  [COPIED] consultation ({copied} files) → "
          f"{target_consult.relative_to(WORKSPACE)}", file=sys.stderr)
    return True


def emit_substrate_facts(
    session, source_note_path, target_note_path,
    source_inquiry_path, target_inquiry_path,
):
    """Register the cloned docs in substrate, emit classifiers, copy
    citation.depends from source onto target, and record the
    provenance.clone audit edge.
    """
    source_note_addr = session.get_addr_for_path(
        str(source_note_path.relative_to(LATTICE)),
    )
    target_note_addr = session.store.register_path(
        str(target_note_path.relative_to(LATTICE)),
    )
    emit_note(session.store, target_note_addr)
    emit_clone(session.store, source_note_addr, target_note_addr)

    target_inquiry_addr = None
    if source_inquiry_path is not None and target_inquiry_path is not None:
        source_inquiry_addr = session.get_addr_for_path(
            str(source_inquiry_path.relative_to(LATTICE)),
        )
        target_inquiry_addr = session.store.register_path(
            str(target_inquiry_path.relative_to(LATTICE)),
        )
        emit_inquiry(session.store, target_inquiry_addr)

        # Mirror inquiry-level citation.depends.
        if source_inquiry_addr is not None:
            for link in session.active_links(
                "citation.depends", from_set=[source_inquiry_addr],
            ):
                for cited in link.to_set:
                    emit_citation(
                        session.store, target_inquiry_addr, cited,
                        direction="depends",
                    )

    # Mirror note-level citation.depends.
    if source_note_addr is not None:
        for link in session.active_links(
            "citation.depends", from_set=[source_note_addr],
        ):
            for cited in link.to_set:
                emit_citation(
                    session.store, target_note_addr, cited,
                    direction="depends",
                )

    return target_note_addr, target_inquiry_addr
