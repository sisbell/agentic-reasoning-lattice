"""Agent-attribution context: env-var lifecycle + helpers.

Three pieces:

- `default_store(lattice_dir)` — returns a Store wrapped in AgentStore
  if `XANADU_AGENT_DOC` is set, else a plain Store. The standard
  way for subprocess tools to open the substrate while inheriting
  the orchestrator's agent identity.
- `agent_context(agent_doc_path)` — context manager that binds
  `XANADU_AGENT_DOC` for the duration of a block. Restores any prior
  value on exit.
- `attributed_to(role)` — decorator that wraps an orchestrator
  entrypoint in `agent_context(agent_doc_path(role))`.

The env-var convention (`XANADU_AGENT_DOC`) lets cross-process
attribution work without explicit hand-off: parent sets, subprocess
inherits, subprocess's `default_store` sees the env var and wraps.
"""

from __future__ import annotations

import contextlib
import functools
import os
from pathlib import Path

from lib.backend.store import Store

from .store import AgentStore


AGENT_DOC_ENV_VAR = "XANADU_AGENT_DOC"


def default_store(lattice_dir: str | Path):
    """Return a Store, wrapped in AgentStore if XANADU_AGENT_DOC is set.

    Orchestrators set the env var so subprocess tools that emit
    substrate links inherit the agent identity and attribute every
    operation back to it. Standalone runs (no env var) get a plain
    Store.

    `lattice_dir` is the lattice root (e.g., LATTICE).
    """
    store = Store(lattice_dir)
    agent_doc_path = os.environ.get(AGENT_DOC_ENV_VAR)
    if not agent_doc_path:
        return store
    # Translate the agent doc's filesystem path to its tumbler. The
    # env var holds a lattice-relative path string; if not yet in the
    # path map, register it.
    agent_addr = store.register_path(agent_doc_path)
    return AgentStore(store, agent_addr)


@contextlib.contextmanager
def agent_context(agent_doc_path: str):
    """Bind XANADU_AGENT_DOC for the duration of the block.

    `agent_doc_path` is a lattice-relative filesystem path. Restores
    any prior value on exit so nested orchestrators inherit cleanly.
    """
    prior = os.environ.get(AGENT_DOC_ENV_VAR)
    os.environ[AGENT_DOC_ENV_VAR] = agent_doc_path
    try:
        yield
    finally:
        if prior is None:
            os.environ.pop(AGENT_DOC_ENV_VAR, None)
        else:
            os.environ[AGENT_DOC_ENV_VAR] = prior


def attributed_to(role: str):
    """Decorator: wrap an orchestrator entrypoint so its body runs inside
    `agent_context(agent_doc_path(role))`. Imports `agent_doc_path` from
    `lib.shared.paths` lazily to avoid circular imports.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            from lib.shared.paths import agent_doc_path
            agent_doc = str(agent_doc_path(role))
            with agent_context(agent_doc):
                return fn(*args, **kwargs)
        return wrapper
    return decorator
