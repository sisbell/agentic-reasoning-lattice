"""Agent module library: file `agent` classifier and `manages` attribution links.

Per the [Agent Module spec](../../../docs/modules/agent-module.md):

- An `agent` link classifies a doc as an agent (same shape as `claim`,
  `review`, `contract`). The agent's identity is the doc's address.
- A `manages` link declares an agent is currently responsible for an
  operation. Doc-to-link shape (from agent doc to operation link id).

Both operations are idempotent against the active set (not raw FindLinks),
so a retracted classifier or manages link does not falsely satisfy the
existence check. Re-emitting after retraction creates a fresh link.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.store.queries import active_links


def emit_agent(store, agent_doc_path):
    """Classify a doc as an agent. Idempotent on active classifiers.

    Returns (link_id, created). If an active `agent` classifier already
    targets `agent_doc_path`, returns its id with created=False. Otherwise
    files a new classifier and returns (new_id, True).
    """
    candidates = active_links(store, "agent", to_set=[agent_doc_path])
    for link in candidates:
        if (link["from_set"] == []
                and link["to_set"] == [agent_doc_path]):
            return link["id"], False
    link_id = store.make_link(
        from_set=[], to_set=[agent_doc_path], type_set=["agent"],
    )
    return link_id, True


def emit_manages(store, agent_doc_path, operation_link_id):
    """File a `manages` link from agent doc to operation. Idempotent on
    the active (agent, operation) pair.

    Returns (link_id, created). If an active `manages` link already exists
    from `agent_doc_path` to `operation_link_id`, returns its id with
    created=False. Otherwise files a new manages link.
    """
    candidates = active_links(
        store, "manages",
        from_set=[agent_doc_path],
        to_set=[operation_link_id],
    )
    for link in candidates:
        if (link["from_set"] == [agent_doc_path]
                and link["to_set"] == [operation_link_id]):
            return link["id"], False
    link_id = store.make_link(
        from_set=[agent_doc_path],
        to_set=[operation_link_id],
        type_set=["manages"],
    )
    return link_id, True
