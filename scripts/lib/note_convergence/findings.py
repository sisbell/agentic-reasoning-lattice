"""Note-convergence finding helper — per-finding doc materialization.

Pass 2 split this from `lib/backend/emit.py` where it bundled
filesystem writes with substrate link emissions. Now the document
write and the link emission are visibly separate calls.

For each finding (title, cls, body):
  1. session.update_document(<findings_dir>/<asn>/<review_stem>/<n>.md)
  2. emit_finding classifier on the per-finding doc
  3. emit comment.{revise|out-of-scope} from finding doc to note
  4. emit provenance.derivation from aggregate review to finding

Atomicity story: operations are not transactional; partial failure
recoverable via reconciliation. See
docs/hypergraph-protocol/error-handling.md.
"""

from __future__ import annotations

from pathlib import Path

from lib.backend.addressing import Address
from lib.backend.emit import emit_comment, emit_derivation, emit_finding
from lib.febe.protocol import Session


def emit_note_findings(
    session: Session,
    note_addr: Address,
    aggregate_addr: Address,
    findings: list,
    asn_label: str,
    review_stem: str,
    findings_dir,
):
    """Materialize each note-review finding as a doc and emit substrate
    facts.

    `findings` is a list of (title, cls, body). For each:
      1. session.update_document(<findings_dir>/<asn>/<review_stem>/<n>.md)
      2. emit_finding classifier on the per-finding doc
      3. emit comment.{revise|out-of-scope} from finding doc to note
      4. emit provenance.derivation from aggregate review to finding

    Returns list of {title, cls, comment_id, note_path, finding_path}.
    """
    findings_root = Path(findings_dir)
    out_dir = findings_root / asn_label / review_stem
    lattice_root = session.store.lattice_dir.resolve()

    note_rel = session.get_path_for_addr(note_addr)
    results = []
    for n, (title, cls, body) in enumerate(findings):
        finding_path = out_dir / f"{n}.md"
        finding_rel = str(finding_path.resolve().relative_to(lattice_root))

        # 1. Document write
        session.update_document(finding_rel, body)

        # 2. Substrate facts
        finding_addr = session.register_path(finding_rel)
        emit_finding(session.store, finding_addr)

        cls_normalized = (cls or "REVISE").upper()
        if cls_normalized == "OUT_OF_SCOPE":
            comment_kind = "out-of-scope"
        else:
            comment_kind = "revise"

        comment = emit_comment(
            session.store, finding_addr, note_addr, kind=comment_kind,
        )

        emit_derivation(session.store, aggregate_addr, finding_addr)

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment.addr,
            "note_path": note_rel,
            "finding_path": finding_rel,
        })

    return results


# ============================================================
#  Reconciliation predicates
# ============================================================

# Detect partial-failure states in the note-finding pipeline. Per
# docs/hypergraph-protocol/error-handling.md, operations are not
# transactional; callers should run reconciliation at stage
# boundaries to surface inconsistencies.

# Comment subtypes the reconciliation predicates check. Note: the
# schema (lib.backend.schema) lists "out-of-scope" as a valid comment
# subtype, but it isn't in the type catalog (lib.backend.types) and
# can't actually be emitted via session.active_links lookup. We use
# only the catalog-resolvable subtypes here. If the schema/catalog
# mismatch is closed later, add the missing subtype to this tuple.
_NOTE_FINDING_COMMENT_KINDS = ("comment.revise", "comment.observe")


def orphan_finding_docs(
    session: Session,
    findings_dir,
) -> list:
    """Note-layer finding files on disk with no active comment link.

    Walks `findings_dir` recursively for `*.md` files. For each,
    checks whether any active `comment.revise` or
    `comment.out-of-scope` link has the file's address in its
    from_set. Files with no comment link are orphans.

    Returns absolute paths, sorted.
    """
    scope = Path(findings_dir).resolve()
    if not scope.exists():
        return []
    lattice_root = session.store.lattice_dir.resolve()
    orphans: list = []
    for path in sorted(scope.rglob("*.md")):
        try:
            finding_rel = str(path.relative_to(lattice_root))
        except ValueError:
            continue
        finding_addr = session.get_addr_for_path(finding_rel)
        if finding_addr is None:
            orphans.append(path)
            continue
        any_link = False
        for kind in _NOTE_FINDING_COMMENT_KINDS:
            if session.active_links(kind, from_set=[finding_addr]):
                any_link = True
                break
        if not any_link:
            orphans.append(path)
    return orphans


def dangling_finding_links(session: Session) -> list:
    """Active note-layer comment links whose source finding doc is
    missing.

    Walks every active `comment.revise` and `comment.out-of-scope`
    link. For each, checks the from_set finding address resolves
    to an existing file. Links whose source file is missing are
    dangling.

    Returns Link records.
    """
    lattice_root = session.store.lattice_dir.resolve()
    dangling: list = []
    for kind in _NOTE_FINDING_COMMENT_KINDS:
        for link in session.active_links(kind):
            for finding_addr in link.from_set:
                finding_rel = session.get_path_for_addr(finding_addr)
                if finding_rel is None:
                    dangling.append(link)
                    break
                if not (lattice_root / finding_rel).exists():
                    dangling.append(link)
                    break
    return dangling
