"""Schema constants — file-system layout for attribute sidecars.

Type-set queries (which types exist, which subtypes a parent admits,
type validation) live in `lib/backend/shapes.py` — that module is the
single source of truth for the substrate's link catalog. This module
holds only the file-system concerns: which attribute sidecar suffixes
exist on disk, used by file-walking helpers that distinguish claim
body markdown from sidecar markdown.

`validate_type` is re-exported from here for backwards compatibility
with callers that import it from this module.
"""

from __future__ import annotations

# Re-export for backwards compatibility — the canonical home is shapes.py.
from .shapes import validate_type  # noqa: F401


# File suffixes for attribute sidecars (used by file-walking helpers
# that distinguish claim body markdown from sidecars).
VALID_ATTRIBUTE_KINDS = frozenset({
    "label", "name", "description", "signature", "statements", "references",
    "motif.attribution",
})
ATTRIBUTE_SUFFIXES = tuple(f".{k}.md" for k in sorted(VALID_ATTRIBUTE_KINDS))
