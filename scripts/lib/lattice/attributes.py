"""Project-level attribute helpers — name/label/description/signature.

Sidecar convention: each attribute is stored as a
`<claim_stem>.<kind>.md` file alongside the claim's `.md`. The
substrate has an attribute link from the claim doc to the sidecar
doc (link type = the kind).

Pass 2 of the binding work split this from `lib/backend/emit.py`:
the bundled `emit_attribute` there did both the filesystem write
and the link emission in one call. Now the two operations are
explicit:

    1. session.update_document(sidecar_path, body)  — FEBE doc write
    2. emit_attribute_link(...)                     — substrate link

This makes the protocol shape honest. Under a distributed backend,
the document write and the link emission cross different
operational paths; bundled inside the substrate they would mask
that. See `docs/hypergraph-protocol/error-handling.md` for the
atomicity story (operations are not transactional; partial failure
is recoverable via reconciliation).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple, Union

from lib.backend.addressing import Address
from lib.backend.emit import emit_attribute_link
from lib.backend.links import Link
from lib.febe.protocol import Session

VALID_ATTRIBUTE_KINDS = {"label", "name", "description", "signature"}

# Sidecar filename pattern: <stem>.<kind>.md where kind is one of the
# four attribute kinds. Used by the reconciliation predicates to
# identify candidate sidecar files on disk.
_SIDECAR_RE = re.compile(
    r"^(?P<stem>.+)\.(?P<kind>label|name|description|signature)\.md$"
)


def emit_attribute(
    session: Session,
    claim_md_path: Union[str, Path],
    kind: str,
    value: str,
    lattice_root: Union[str, Path, None] = None,
) -> Tuple[Link, bool]:
    """Set an attribute on a claim doc.

    Composes two visible operations:
      1. `session.update_document(sidecar_path, body)` — FEBE write
      2. `emit_attribute_link(session.store, ...)` — substrate link

    `claim_md_path` may be lattice-relative or absolute. The sidecar
    path is derived as `<claim_dir>/<stem>.<kind>.md`. Both docs are
    registered in the path map (allocated fresh tumblers if new).

    Returns (link, created) where `created` indicates whether the
    link was freshly emitted (False if an active link already
    existed).

    Body normalization:
    - `description` gets a trailing newline if it doesn't end with
      one; otherwise body is value as-is.
    - All other kinds get rstrip + single trailing newline.

    Skip-if-identical optimization on the document write: if the
    sidecar already exists with byte-identical content, the write
    is skipped (reduces no-op churn in diffs). The link emission's
    idempotency (active-link lookup) handles the same property at
    the substrate layer.
    """
    if kind not in VALID_ATTRIBUTE_KINDS:
        raise ValueError(
            f"invalid attribute kind {kind!r}; must be one of "
            f"{sorted(VALID_ATTRIBUTE_KINDS)}"
        )

    root = Path(lattice_root) if lattice_root else session.store.lattice_dir
    claim_md = Path(claim_md_path)
    if not claim_md.is_absolute():
        claim_md = (root / claim_md).resolve()
    else:
        claim_md = claim_md.resolve()
    stem = claim_md.stem
    sidecar_abs = claim_md.parent / f"{stem}.{kind}.md"

    if kind == "description":
        body = value if value.endswith("\n") else value + "\n"
    else:
        body = value.rstrip("\n") + "\n"

    root_resolved = root.resolve()
    claim_rel = str(claim_md.relative_to(root_resolved))
    sidecar_rel = str(sidecar_abs.relative_to(root_resolved))

    # 1. Document write (skip if content already identical)
    if not sidecar_abs.exists() or sidecar_abs.read_text() != body:
        session.update_document(sidecar_rel, body)

    # 2. Substrate link emission (idempotent via active-link lookup)
    claim_addr = session.register_path(claim_rel)
    sidecar_addr = session.register_path(sidecar_rel)
    return emit_attribute_link(session.store, claim_addr, kind, sidecar_addr)


# ============================================================
#  Reconciliation predicates
# ============================================================

# These detect partial-failure states between the document write and
# the link emission (per docs/hypergraph-protocol/error-handling.md).
# They are detection-only — no destructive action. Callers (janitor
# scripts, stage-end checks) decide what to do with the findings.


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
            # Sidecar lives outside the lattice; skip
            continue
        sidecar_addr = session.get_addr_for_path(sidecar_rel)
        if sidecar_addr is None:
            # File exists but isn't in the path map at all — orphan
            # (substrate doesn't know about it).
            orphans.append(path)
            continue
        active = session.active_links(kind, to_set=[sidecar_addr])
        if not active:
            orphans.append(path)
    return orphans


def dangling_attribute_links(session: Session) -> List[Link]:
    """Active attribute links whose target sidecar file no longer exists.

    Walks every active link of the four attribute kinds (`label`,
    `name`, `description`, `signature`). For each, checks that the
    to_set sidecar address resolves to an existing file on disk.
    Links whose targets are missing or unresolvable are dangling.

    Returns the list of dangling Link records (the substrate-level
    artifact, not the missing file path — the file IS missing, after
    all).

    Cases this catches:
    - Link was emitted but document write failed (the reverse
      partial-failure case).
    - Sidecar was deleted manually after the link was filed; link
      was never retracted.
    - Path map references a file that has since been moved or
      removed.
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
