"""Provenance — agent-attribution machinery for cross-process work.

Domain-neutral provenance protocol: a process binds itself to an
agent doc via the `XANADU_AGENT_DOC` env var, and every substrate
emission auto-files a `manages` link from that agent doc to the
emitted link. Subprocesses inherit the env var; the cross-process
attribution chain works without explicit handoff.

Public API:

- `agent_context(agent_doc_path)` — context manager binding the
  `XANADU_AGENT_DOC` env var for a block
- `attributed_to(role)` — decorator that wraps an entrypoint in
  `agent_context` with the role's standard agent doc
- `AGENT_DOC_ENV_VAR` — the env var name (= "XANADU_AGENT_DOC")

The substrate-side plumbing — `_AttributingStore`, `default_store` —
lives in `lib/protocols/febe/session.py` (substrate construction is
a session-binding concern). This module is purely the cross-process
identity convention.
"""

from .context import (
    AGENT_DOC_ENV_VAR,
    agent_context,
    attributed_to,
)

__all__ = [
    "AGENT_DOC_ENV_VAR",
    "agent_context",
    "attributed_to",
]
