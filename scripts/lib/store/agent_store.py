"""Agent-attributing wrapper around Store.

`AgentStore(store, agent_doc)` proxies a `Store` and auto-emits a
`manages` link from `agent_doc` to every link the wrapped store creates.
The `agent` classifier on `agent_doc` is filed once at construction
(idempotent via `emit_agent`).

Attribution skips `agent` and `manages` types themselves: the agent
isn't classified as one of its own operations, and a `manages` link
isn't a managed operation. (Without that skip, `emit_manages` would
recurse infinitely on its own emission.)

Cross-process attribution: orchestrators that invoke subprocesses (e.g.
cone-review → reviser → decide.py) set `XANADU_AGENT_DOC` so each
subprocess that uses `default_store()` picks up the same agent identity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.store.agent import emit_agent, emit_manages


_ATTRIBUTION_SKIP_TYPES = frozenset({"agent", "manages"})


class AgentStore:
    def __init__(self, store, agent_doc):
        self._store = store
        self._agent_doc = agent_doc
        emit_agent(store, agent_doc)

    @property
    def agent_doc(self):
        return self._agent_doc

    def make_link(self, from_set, to_set, type_set, ts=None):
        link_id = self._store.make_link(
            from_set, to_set, type_set, ts=ts,
        )
        type_str = type_set[0] if isinstance(type_set, list) and type_set else None
        if type_str not in _ATTRIBUTION_SKIP_TYPES:
            emit_manages(self._store, self._agent_doc, link_id)
        return link_id

    def get(self, link_id):
        return self._store.get(link_id)

    def find_links(self, home_set=None, from_set=None, to_set=None, type_set=None):
        return self._store.find_links(
            home_set=home_set, from_set=from_set,
            to_set=to_set, type_set=type_set,
        )

    def find_num_links(self, home_set=None, from_set=None, to_set=None, type_set=None):
        return self._store.find_num_links(
            home_set=home_set, from_set=from_set,
            to_set=to_set, type_set=type_set,
        )

    def rebuild_index(self):
        return self._store.rebuild_index()

    def close(self):
        return self._store.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self._store.__exit__(*args)
