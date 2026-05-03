"""Notation primitive helpers — read the lattice's notation doc.

The substrate has at most one `notation` classifier link; the doc it
classifies holds a markdown bullet list of primitive symbols. This
module reads that doc and returns the symbol set.

Project convention: notation docs are markdown bullet lists of
backtick-wrapped symbols. Not a substrate primitive — composes
substrate queries (active_links over the `notation` classifier)
plus the project's convention for how notation docs are structured.
"""

from __future__ import annotations

import re
from typing import Set

from lib.backend.predicates import active_links
from lib.backend.store import Store

_BULLET_RE = re.compile(r"^- `([^`]+)`")


def read_notation(store: Store) -> Set[str]:
    """The set of primitive symbols declared by the active notation doc.

    Empty set if no notation classifier exists, or the doc is missing
    / empty.
    """
    symbols: Set[str] = set()
    for link in active_links(store.state, "notation"):
        for doc_addr in link.to_set:
            doc_path = store.path_for_addr(doc_addr)
            if doc_path is None:
                continue
            doc_full = store.lattice_dir / doc_path
            if not doc_full.exists():
                continue
            for line in doc_full.read_text().splitlines():
                m = _BULLET_RE.match(line)
                if m:
                    symbols.add(m.group(1))
    return symbols
