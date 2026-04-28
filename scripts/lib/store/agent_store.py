"""Agent-attributing wrapper around Store.

`AgentStore(store, agent_doc)` proxies a `Store` and auto-emits a
`manages` link from `agent_doc` to every link the wrapped store creates.
The `agent` classifier on `agent_doc` is filed once at construction
(idempotent via `emit_agent`).

Attribution skips `agent` and `manages` parent types: the agent isn't
classified as one of its own operations, and a `manages` link isn't a
managed operation. Without that skip, the wrapper would recurse on its
own attribution emission.

Cross-process attribution: orchestrators that invoke subprocesses (e.g.
cone-review → reviser → decide.py) set `XANADU_AGENT_DOC` so each
subprocess that uses `default_store()` picks up the same agent identity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.store.agent import emit_agent


_ATTRIBUTION_SKIP_PARENTS = frozenset({"agent", "manages"})


class AgentStore:
    def __init__(self, store, agent_doc):
        self._store = store
        self._agent_doc = agent_doc
        emit_agent(store, agent_doc)

    @property
    def agent_doc(self):
        return self._agent_doc

    def make_link(self, from_set, to_set, type_set, ts=None):
        link_id = self._store.make_link(from_set, to_set, type_set, ts=ts)
        type_str = type_set[0] if isinstance(type_set, list) and type_set else None
        parent = type_str.split(".", 1)[0] if type_str else None
        if parent not in _ATTRIBUTION_SKIP_PARENTS:
            # Fresh link id, so the active (agent, operation) pair can't
            # already exist — skip emit_manages's idempotency query and
            # file the link directly.
            self._store.make_link(
                from_set=[self._agent_doc],
                to_set=[link_id],
                type_set=["manages"],
            )
        return link_id

    def __getattr__(self, name):
        return getattr(self._store, name)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self._store.__exit__(*args)
