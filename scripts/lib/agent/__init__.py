"""Agent — provenance attribution wrapper around the substrate.

Domain-neutral provenance protocol: every link emitted by an
agent-bound store auto-files a `manages` link from the agent doc
to the emitted link. Cross-process attribution is via the
XANADU_AGENT_DOC env var; orchestrators set it before spawning
subprocess tools, and each subprocess inherits the agent identity.

Public API:

- `AgentStore(store, agent_doc)` — wraps a Store; auto-emits manages
- `default_store(lattice_dir)` — returns AgentStore if env var set,
  else plain Store
- `agent_context(agent_doc_path)` — context manager binding the
  XANADU_AGENT_DOC env var for a block
- `attributed_to(role)` — decorator that wraps an entrypoint in
  agent_context with the role's standard agent doc

This package belongs above the substrate (`lib/backend/`) — the
provenance protocol composes substrate primitives (emit_agent,
make_link with type=manages) with environment-variable-based
identity. Generic across domains; not xanadu- or claim-specific.
"""

from .context import (
    AGENT_DOC_ENV_VAR,
    agent_context,
    attributed_to,
    default_store,
)
from .store import AgentStore

__all__ = [
    "AGENT_DOC_ENV_VAR",
    "AgentStore",
    "agent_context",
    "attributed_to",
    "default_store",
]
