"""Reconciliation predicates — partial-failure detection.

The simulator's operations (document write + link emission) are not
transactional. Either side can succeed while the other fails, leaving
the lattice in a partial-failure state: orphan files (doc on disk, no
substrate reference) or dangling links (substrate reference, no doc on
disk). See `docs/hypergraph-protocol/error-handling.md` for the full
atomicity story.

These predicates are detection-only — no destructive action. Callers
(janitor scripts, stage-end checks) decide what to do with the
findings: retract dangling links, delete orphan files, back-fill
missing data, or investigate further.

Three surfaces, each with an orphan/dangling pair:
- Attribute sidecars (`label`, `name`, `description`, `signature`)
- Claim-layer findings (sourced via `comment.revise`/`comment.observe`)
- Note-layer findings (sourced via `comment.revise`/`comment.observe`/
  `comment.out-of-scope`)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Union

from lib.backend.links import Link
from lib.febe.protocol import Session
from lib.lattice.attributes import VALID_ATTRIBUTE_KINDS


# ============================================================
#  Attribute reconciliation
# ============================================================

# Sidecar filename pattern: <stem>.<kind>.md where kind is one of the
# four attribute kinds.
_SIDECAR_RE = re.compile(
    r"^(?P<stem>.+)\.(?P<kind>label|name|description|signature)\.md$"
)


def orphan_sidecars(
    session: Session,
    scope_dir: Union[str, Path],
) -> List[Path]:
    """Sidecar files on disk with no active attribute link pointing at them.

    Walks `scope_dir` recursively for files matching
    `*.{label|name|description|signature}.md`. For each, checks
    whether an active attribute link of the matching kind has the
    file's address in its to_set. Files with no such link are
    orphans — partial failure left a sidecar but no substrate
    reference.

    Returns absolute paths, sorted.

    Cases this catches:
    - Document write succeeded but link emission failed (the typical
      partial-failure case; orphan file lingers).
    - Sidecar was written manually or by a process that didn't emit
      the link.
    - Link was retracted but the sidecar wasn't cleaned up (a
      different kind of orphan; the substrate cleared but the file
      stayed).
    """
    scope = Path(scope_dir).resolve()
    if not scope.exists():
        return []
    lattice_root = session.store.lattice_dir.resolve()
    orphans: List[Path] = []
    for path in sorted(scope.rglob("*.md")):
        m = _SIDECAR_RE.match(path.name)
        if not m:
            continue
        kind = m.group("kind")
        try:
            sidecar_rel = str(path.relative_to(lattice_root))
        except ValueError:
            continue
        sidecar_addr = session.get_addr_for_path(sidecar_rel)
        if sidecar_addr is None:
            orphans.append(path)
            continue
        active = session.active_links(kind, to_set=[sidecar_addr])
        if not active:
            orphans.append(path)
    return orphans


def dangling_attribute_links(session: Session) -> List[Link]:
    """Active attribute links whose target sidecar file no longer exists.

    Walks every active link of the four attribute kinds. For each,
    checks that the to_set sidecar address resolves to an existing
    file on disk. Links whose targets are missing or unresolvable are
    dangling.

    Returns the list of dangling Link records (the substrate-level
    artifact, not the missing file path — the file IS missing).

    Cases this catches:
    - Link was emitted but document write failed (the reverse
      partial-failure case).
    - Sidecar was deleted manually after the link was filed; link
      was never retracted.
    - Path map references a file that has since been moved or removed.
    """
    lattice_root = session.store.lattice_dir.resolve()
    dangling: List[Link] = []
    for kind in sorted(VALID_ATTRIBUTE_KINDS):
        for link in session.active_links(kind):
            for sidecar_addr in link.to_set:
                sidecar_rel = session.get_path_for_addr(sidecar_addr)
                if sidecar_rel is None:
                    dangling.append(link)
                    break
                if not (lattice_root / sidecar_rel).exists():
                    dangling.append(link)
                    break
    return dangling


# ============================================================
#  Claim-layer finding reconciliation
# ============================================================

# Comment subtypes that source from a finding doc in the
# claim-convergence layer. Both target a claim document.
_CLAIM_FINDING_COMMENT_KINDS = ("comment.revise", "comment.observe")


def orphan_claim_finding_docs(
    session: Session,
    findings_dir: Union[str, Path],
) -> list:
    """Claim-layer finding files on disk with no active comment link.

    Walks `findings_dir` recursively for `*.md` files. For each,
    checks whether any active `comment.revise` or `comment.observe`
    link has the file's address in its from_set. Files with no
    comment link are orphans — partial failure left a finding doc
    but the comment that should reference it never emitted (or was
    retracted without cleaning up the file).

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
        for kind in _CLAIM_FINDING_COMMENT_KINDS:
            if session.active_links(kind, from_set=[finding_addr]):
                any_link = True
                break
        if not any_link:
            orphans.append(path)
    return orphans


def dangling_claim_finding_links(session: Session) -> list:
    """Active claim-layer comment links whose source finding doc is missing.

    Walks every active `comment.revise` and `comment.observe` link.
    For each, checks the from_set finding address resolves to an
    existing file. Links whose source file is missing are dangling —
    link emission succeeded but the doc write didn't (or the doc was
    deleted manually after the link was filed).

    Returns Link records (the substrate-level artifact).
    """
    lattice_root = session.store.lattice_dir.resolve()
    dangling: list = []
    for kind in _CLAIM_FINDING_COMMENT_KINDS:
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


# ============================================================
#  Note-layer finding reconciliation
# ============================================================

# Comment subtypes the note-layer reconciliation predicates check.
# emit_note_findings maps OUT_OF_SCOPE classifications to
# comment.out-of-scope.
_NOTE_FINDING_COMMENT_KINDS = (
    "comment.revise",
    "comment.observe",
    "comment.out-of-scope",
)


def orphan_note_finding_docs(
    session: Session,
    findings_dir: Union[str, Path],
) -> list:
    """Note-layer finding files on disk with no active comment link.

    Walks `findings_dir` recursively for `*.md` files. For each,
    checks whether any active `comment.revise`, `comment.observe`, or
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


def dangling_note_finding_links(session: Session) -> list:
    """Active note-layer comment links whose source finding doc is missing.

    Walks every active `comment.revise`, `comment.observe`, and
    `comment.out-of-scope` link. For each, checks the from_set finding
    address resolves to an existing file. Links whose source file is
    missing are dangling.

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
