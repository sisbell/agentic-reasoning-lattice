"""Agent-attributing wrapper around Store.

`AgentStore(store, agent_doc)` proxies a `Store`, emits the `agent`
classifier on `agent_doc` once at construction, and auto-emits a
`manages` link from `agent_doc` to every link the wrapped store
creates afterwards.

Skips attribution on `agent` and `manages` parent types: the agent
isn't classified as one of its own operations, and a `manages` link
isn't a managed operation. Without that skip the wrapper would
recurse on its own attribution emission.

Cross-process attribution: orchestrators that invoke subprocesses
(e.g. cone-review → reviser) set `XANADU_AGENT_DOC` so each
subprocess that opens a fresh AgentStore picks up the same agent
identity.
"""

from __future__ import annotations

from typing import Iterable

from .addressing import Address
from .emit import emit_agent
from .links import Link
from .state import TypeArg
from .store import Store

_ATTRIBUTION_SKIP_PARENTS = frozenset({"agent", "manages"})


class AgentStore:
    """Wraps a Store; auto-files `manages` for every emitted link."""

    def __init__(self, store: Store, agent_doc: Address) -> None:
        self._store = store
        self._agent_doc = agent_doc
        emit_agent(store, agent_doc)

    @property
    def agent_doc(self) -> Address:
        return self._agent_doc

    @property
    def state(self):
        return self._store.state

    def make_link(
        self,
        homedoc: Address,
        from_set: Iterable[Address],
        to_set: Iterable[Address],
        type_: TypeArg,
    ) -> Link:
        link = self._store.make_link(homedoc, from_set, to_set, type_)
        # Determine the parent of the type for the skip check. type_
        # may be a string ("citation.depends") or an Address. In the
        # Address case we bypass the skip since lookup is non-trivial;
        # most production callers pass strings.
        parent = None
        if isinstance(type_, str):
            parent = type_.split(".", 1)[0]
        if parent not in _ATTRIBUTION_SKIP_PARENTS:
            self._store.make_link(
                homedoc=self._agent_doc,
                from_set=[self._agent_doc],
                to_set=[link.addr],
                type_="manages",
            )
        return link

    def __getattr__(self, name):
        # Delegate everything else (find_links, addr_for_path, etc.)
        # to the wrapped store.
        return getattr(self._store, name)
