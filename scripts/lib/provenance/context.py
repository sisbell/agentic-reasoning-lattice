"""Agent-attribution context: env-var lifecycle + helpers.

Two pieces:

- `agent_context(agent_doc_path)` — context manager that binds
  `XANADU_AGENT_DOC` for the duration of a block. Restores any prior
  value on exit.
- `attributed_to(role)` — decorator that wraps an orchestrator
  entrypoint in `agent_context(agent_doc_path(role))`.

The env-var convention (`XANADU_AGENT_DOC`) lets cross-process
attribution work without explicit hand-off: parent sets, subprocess
inherits, and `default_store` (in `lib/protocols/febe/session.py`)
sees the env var and wraps the substrate accordingly.
"""

from __future__ import annotations

import contextlib
import functools
import os


AGENT_DOC_ENV_VAR = "XANADU_AGENT_DOC"


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
