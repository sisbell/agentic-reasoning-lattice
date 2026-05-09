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
is recoverable via reconciliation — predicates in
`lib/predicates/reconciliation.py`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple, Union

from lib.backend.emit import emit_attribute_link, emit_citation
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session

VALID_ATTRIBUTE_KINDS = {
    "label", "name", "description", "signature", "statements", "references",
}


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


def attest_attribute(
    session: Session,
    claim_md_path: Union[str, Path],
    kind: str,
    value: str,
    lattice_root: Union[str, Path, None] = None,
) -> Tuple[Link, bool]:
    """Pure emission primitive: write sidecar file + emit attribute
    link. No chain advance.

    Idempotent. The file write is skip-if-identical (no I/O on a
    no-op re-write); the link emission is idempotent on the active
    link set.

    Chain advancement is the caller's responsibility — call
    `register_version` explicitly on the sidecar address before
    `attest_attribute` when the call represents a real content edit.
    For most producers this is handled by `attest_against_doc_head`,
    which takes an explicit `content_changed` flag and advances the
    chain only when the producer signals a real edit.

    Use this directly only when:
      - The attribute kind has no freshness predicate (`label`,
        `name`) AND the caller doesn't need chain-advance semantics.
      - First-emission cases, where the `emit_attribute_link` call
        creates the chain at length 1.

    Returns (link, created) where created is True iff the link was
    freshly emitted (first-time call); False on subsequent.
    """
    return emit_attribute(session, claim_md_path, kind, value, lattice_root)


def attest_against_doc_head(
    session: Session,
    doc_md_path: Union[str, Path],
    kind: str,
    value: str,
    doc_addr,
    *,
    content_changed: bool,
    lattice_root: Union[str, Path, None] = None,
) -> Tuple[Link, bool]:
    """Attest a sidecar with a freshness-anchor citation, conditionally
    advancing the chain.

    The producer signals via `content_changed` whether this fire
    represents a real edit:

    - `content_changed=True` AND a sidecar already exists: advance
      the existing sidecar's chain via `register_version` BEFORE the
      file write. The new chain head is the new content version.
    - `content_changed=False`: no chain advance. The sidecar's
      current head stays in place; the file write is idempotent
      (skip-if-identical at the FEBE layer).
    - First emission (no existing sidecar): no chain advance — the
      creation IS the first version; `content_changed` is ignored.

    In all three cases, after the attestation lands, emit
    `citation.depends` from the sidecar's current head version to
    `version_head(doc_addr)`. This is the freshness anchor; the
    `*_is_fresh` predicate walks it. On a no-op re-attestation
    against a doc that's advanced, the anchor re-points at the new
    doc head from the existing sidecar version.

    The chain represents content versions, not attestation events.
    The producer alone knows whether its fire produced a real edit
    (via LLM verdict, byte-compare, or domain knowledge); this
    primitive accepts that signal.

    Works for any doc kind (claim, note).
    """
    from lib.predicates.versions import version_head

    # Look up existing sidecar BEFORE attest_attribute to detect
    # subsequent vs first-emission. The lookup needs the doc_addr to
    # be registered already.
    existing_sidecar = None
    for link in session.active_links(kind, from_set=[doc_addr]):
        if link.to_set:
            existing_sidecar = link.to_set[0]
            break

    if existing_sidecar is not None and content_changed:
        session.register_version(existing_sidecar)

    link, created = attest_attribute(
        session, doc_md_path, kind, value, lattice_root,
    )
    sidecar_addr = link.to_set[0]
    sidecar_head = version_head(session, sidecar_addr)
    doc_head = version_head(session, doc_addr)
    emit_citation(
        session.store, sidecar_head, doc_head, direction="depends",
    )
    return link, created
