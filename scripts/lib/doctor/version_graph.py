"""Version-graph consistency check.

The substrate carries two redundant representations of versioning:

  - the parent map (`state.parent`), populated by `register_version`
    in-process and walked by `version_head` / `version_children`.
  - the supersession-link chain in `links.jsonl`, walked by
    `supersession_head` / `_walk_supersession`.

`Store._reattach_doc_owners` rebuilds `_owner` and link allocators
from `links.jsonl` on session load, but does NOT rebuild the parent
map. So after a reload, `version_head` returns the base address for
any doc that was versioned in a prior session, while
`supersession_head` correctly returns the chain head.

This check walks every doc with at least one outgoing supersession
link and flags any address whose `version_head` disagrees with its
`supersession_head`. ERROR severity — `attest_against_doc_head`
emits its freshness anchor against `version_head`, so divergence
silently anchors against the wrong target.
"""

from __future__ import annotations

from typing import Iterable

from lib.predicates.versions import supersession_head, version_head
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "version-graph"
CHECK_DESCRIPTION = (
    "Persisted supersession chain disagrees with in-memory parent map. "
    "The parent map (walked by `version_head`) isn't rebuilt from "
    "supersession links on session load, so any doc versioned in a "
    "prior session reports its base address as the head."
)


def check_version_graph(session: Session) -> Iterable[Issue]:
    """Yield one Issue per doc whose parent-map head ≠ supersession head."""
    seen: set = set()
    for link in session.active_links("supersession"):
        if not link.from_set:
            continue
        base = link.from_set[0]
        if base in seen:
            continue
        seen.add(base)

        vh = version_head(session, base)
        sh = supersession_head(session, base)
        if vh == sh:
            continue
        path = session.get_path_for_addr(base) or "(no path)"
        yield Issue(
            severity=Severity.ERROR,
            check=CHECK_NAME,
            message=(
                f"{path}  base={base}  parent_map_head={vh}  "
                f"supersession_head={sh}"
            ),
        )
