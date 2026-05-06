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

from lib.backend.emit import emit_attribute_link
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
    """Attest an attribute against the doc's current revision state.

    Single create-or-advance path:
    - First-time: creates link + sidecar at supersession chain
      length 1 (delegates to emit_attribute).
    - Subsequent: advances the sidecar's chain by 1 via
      register_version, then writes the new content (file write
      skipped if byte-identical).

    Use this for every producer fire / CLI invocation that records
    an attestation. The chain advance encodes "I checked at this
    revision" — meaningful even when the new content is identical
    to the old (no-op LLM output still counts as an attestation
    that the existing sidecar is correct as-of-now).

    For attribute kinds with a freshness predicate
    (description/signature/statements), the chain advance is
    REQUIRED — predicates compare chain lengths to detect staleness,
    and skipping the advance leaves them stuck in False, causing
    the runner to re-fire until max_iterations.

    For attribute kinds without a freshness predicate (label/name),
    the chain still advances harmlessly. This is the relaxed-model's
    "advance where it doesn't hurt" stance: cost is one supersession
    link per call; benefit is one fewer discipline at the call site.
    Future predicates over those kinds get the chain machinery for
    free.

    Returns (link, created) where created is True iff the link was
    freshly emitted (i.e., first-time call); False on subsequent.
    """
    # Resolve claim_addr to detect first vs subsequent. We reuse
    # emit_attribute's path-resolution logic by computing it once
    # here, so the lookup is in sync with the delegate.
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
    claim_rel = str(claim_md.relative_to(root.resolve()))

    claim_addr = session.get_addr_for_path(claim_rel)
    if claim_addr is not None:
        existing = session.active_links(kind, from_set=[claim_addr])
        for link in existing:
            if link.to_set:
                # Subsequent: advance the sidecar's chain before the
                # delegate does its file write + link lookup.
                session.register_version(link.to_set[0])
                break

    return emit_attribute(session, claim_md_path, kind, value, lattice_root)
