"""Library: emit and read the lattice's notation classifier link.

Notation = language-provided primitive symbols (logical operators, set
membership, universal quantifiers, …). Always in scope; not owned by
any claim. Sister concept to per-claim `signature` attributes, which
record claim-introduced non-logical symbols.

A lattice has at most one notation doc, classified by a single `notation`
link with empty `from_set`. The doc holds markdown bullets, one per
primitive symbol (``- `<symbol>``` form). Edit-in-place mutability: the
doc is overwritten when the primitive set changes; the link stays.

Used by invariant #7 (declared-symbols-resolve): a symbol used in a
claim's Formal Contract must resolve to an owning claim via the
transitive citation closure, OR be a primitive listed here.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import LATTICE


NOTATION_DOC_REL = "_docuverse/documents/notation/notation.md"

_BULLET_RE = re.compile(r"^- `([^`]+)`")


def _render_notation(primitives):
    """Render a list of primitive symbol strings as markdown bullets."""
    lines = []
    for sym in primitives:
        sym = (sym or "").strip()
        if sym:
            lines.append(f"- `{sym}`")
    return "\n".join(lines) + "\n" if lines else "\n"


def emit_notation(store, primitives, lattice_root=None):
    """Write the notation doc and emit its classifier link.

    `primitives` is an iterable of symbol strings.

    Behavior:
    - Writes `_docuverse/documents/notation/notation.md` (overwriting if
      content differs; edit-in-place mutability).
    - Emits the `notation` classifier link (`from_set=[]`,
      `to_set=[NOTATION_DOC_REL]`) if it doesn't already exist.

    Idempotency: if the link already exists AND the doc's content matches,
    returns `(existing_link_id, False)`. If the doc differs, the doc is
    overwritten but the link stays — also returns `(existing_link_id, False)`.
    `created` is True only when a *new link* is emitted.

    Returns (link_id, created_bool).
    """
    root = Path(lattice_root) if lattice_root else Path(LATTICE)
    doc_abs = root / NOTATION_DOC_REL
    body = _render_notation(list(primitives))

    if not doc_abs.exists() or doc_abs.read_text() != body:
        doc_abs.parent.mkdir(parents=True, exist_ok=True)
        doc_abs.write_text(body)

    candidates = store.find_links(
        to_set=[NOTATION_DOC_REL], type_set=["notation"],
    )
    for link in candidates:
        if (link["type_set"] == ["notation"]
                and link["from_set"] == []
                and link["to_set"] == [NOTATION_DOC_REL]):
            return link["id"], False

    link_id = store.make_link(
        from_set=[], to_set=[NOTATION_DOC_REL], type_set=["notation"],
    )
    return link_id, True


def read_notation(store, lattice_root=None):
    """Return the set of primitive symbols declared by the active
    notation doc. Returns an empty set if no notation link exists or
    the doc is missing/empty.
    """
    links = store.find_links(type_set=["notation"])
    if not links:
        return set()

    root = Path(lattice_root) if lattice_root else Path(LATTICE)
    symbols = set()
    for link in links:
        for doc_rel in link["to_set"]:
            doc_abs = root / doc_rel
            if not doc_abs.exists():
                continue
            for line in doc_abs.read_text().splitlines():
                m = _BULLET_RE.match(line)
                if m:
                    symbols.add(m.group(1))
    return symbols
