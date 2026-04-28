"""Library: emit a substrate-owned attribute link (`label`, `name`,
`description`, `signature`).

Substrate-owned attributes are general-purpose document primitives — any
document can carry them, regardless of the protocol operating on it. The
attribute's value lives in a sibling document (`<stem>.<kind>.md`); the
substrate link associates the claim md with that sibling.

- label: short address (e.g., "T0", "NAT-cancel"). One-line file.
- name: canonical identity (e.g., "CarrierSetDefinition"). One-line file.
- description: prose summary, multi-line markdown allowed.
- signature: markdown bullet list of non-logical symbols this claim
  introduces, each as ``- `<symbol>` — <meaning>``. Optional: claims
  that introduce no new symbols have no signature sidecar (and no
  `signature` link).

Stage-1 mutability: attribute docs are edited in place when the value
changes. The link survives. Same treatment as claim md files (which
are also edited in place by the reviser). When Xanadu lands document
versioning, both gain history at the document layer; the link graph
doesn't change.

Retraction is reserved for wrong-link cases (link filed on the wrong
claim, points at the wrong document). Not for value changes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import LATTICE


VALID_KINDS = {"label", "name", "description", "signature"}
ATTRIBUTE_SUFFIXES = tuple(f".{k}.md" for k in sorted(VALID_KINDS))


def emit_attribute(store, claim_md_path, kind, value, lattice_root=None):
    """Emit a `kind` attribute link from claim_md_path to a sibling doc.

    `kind` must be one of "label", "name", "description", "signature".
    `value` is the attribute's content (single-line for label/name;
    multi-line allowed for description).

    Behavior:
    - Computes sibling doc path: `<claim_dir>/<stem>.<kind>.md`.
    - Writes the doc with `value` (overwriting if content differs;
      edit-in-place mutability).
    - Emits the typed link if it doesn't already exist.

    Idempotency: if the link already exists AND the doc's content matches
    `value`, returns `(existing_link_id, False)`. If the doc content
    differs, the doc is overwritten but the link stays — returns
    `(existing_link_id, False)`. `created` is True only when a *new link*
    is emitted.

    `lattice_root` is an optional override for lattice-relative path
    computation (mirrors `findings_dir` overrides elsewhere). When None,
    uses the lattice root from `lib.shared.paths`.

    Returns (link_id, created_bool).
    Raises ValueError if `kind` is not a valid attribute kind.
    """
    if kind not in VALID_KINDS:
        raise ValueError(
            f"unknown attribute kind {kind!r}; expected one of {sorted(VALID_KINDS)}"
        )

    root = Path(lattice_root) if lattice_root else Path(LATTICE)
    claim_md = (root / claim_md_path).resolve() if not Path(claim_md_path).is_absolute() else Path(claim_md_path).resolve()

    stem = claim_md.stem
    attr_doc_abs = claim_md.parent / f"{stem}.{kind}.md"

    # Edit-in-place semantics: write/overwrite the doc with `value`.
    # For label/name, normalize to a trailing newline for tidy single-line files.
    # For description, preserve `value` verbatim (multi-line markdown).
    if kind == "description":
        body = value if value.endswith("\n") else value + "\n"
    else:
        body = value.rstrip("\n") + "\n"
    if not attr_doc_abs.exists() or attr_doc_abs.read_text() != body:
        attr_doc_abs.parent.mkdir(parents=True, exist_ok=True)
        attr_doc_abs.write_text(body)

    claim_rel = str(claim_md.relative_to(root.resolve()))
    attr_rel = str(attr_doc_abs.relative_to(root.resolve()))

    # Idempotency check: same kind link from this claim already pointing
    # at the expected sibling doc?
    candidates = store.find_links(
        from_set=[claim_rel], to_set=[attr_rel], type_set=[kind],
    )
    for link in candidates:
        if (link["type_set"] == [kind]
                and link["from_set"] == [claim_rel]
                and link["to_set"] == [attr_rel]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[claim_rel], to_set=[attr_rel], type_set=[kind],
    )
    return link_id, True
