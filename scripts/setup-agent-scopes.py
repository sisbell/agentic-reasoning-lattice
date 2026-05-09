#!/usr/bin/env python3
"""Tag agent docs with their `agent.scope.<type>` classifier.

Run once after the substrate is upgraded with the `agent.scope.<type>`
classifier types (per docs/design-notes/stigmergic-coordination.md).
Idempotent: re-running on already-classified agent docs is a no-op
(emit_classifier returns the existing link).

Adds `agent.scope.note` to:
  - cone-review.md (cone work conflicts at the ASN-level note)
  - full-review.md (full review covers the ASN-level note)

Usage:
    python scripts/setup-agent-scopes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_agent_scope
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


_NOTE_SCOPED_AGENTS = (
    "cone-review",
    "full-review",
)


def main() -> int:
    with open_session(LATTICE) as session:
        store = session.store
        for role in _NOTE_SCOPED_AGENTS:
            doc_path = f"_docuverse/documents/agent/{role}.md"
            agent_addr = session.get_addr_for_path(doc_path)
            if agent_addr is None:
                print(
                    f"  [SETUP-AGENT-SCOPES] {role}: agent doc not "
                    f"registered ({doc_path}); skipping",
                    file=sys.stderr,
                )
                continue
            link, created = emit_agent_scope(store, agent_addr, "note")
            status = "added" if created else "already present"
            print(
                f"  [SETUP-AGENT-SCOPES] {role}: agent.scope.note "
                f"{status} ({link.addr})",
                file=sys.stderr,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
