"""Claims-statements refresh agent — owns the ASN-level
`claims.statements` aggregate's lifecycle.

Two-mode behavior driven by predicate state:

  First fire (claims confirmed, no aggregate yet) — *create*. Mint a
  substrate address for the aggregate, file the `claims.statements`
  identity classifier, emit `note → provenance.derivation →
  aggregate`, retire the `note.statements` sidecar (its supersession
  chain has reached the point where the aggregate takes over), emit
  `supersession(note.statements → aggregate)`, and write the
  mechanically-assembled content to disk.

  Subsequent fires (aggregate exists, chain trails max claim chain) —
  *advance*. Re-assemble the content from current per-claim files
  + sidecars, write the new content to disk, then `register_version`
  to tick the substrate chain. The disk file always reflects the
  latest assembly; the substrate chain advance flips `is_head_version`
  False on the prior head for downstream cites (cascade signal).

Assembly is mechanical (no LLM): walks `provenance.derivation` from
the note to enumerate derived claims, reads each claim's body
(Formal Contract section), name sidecar, and description sidecar,
and produces the consolidated markdown block via
`render_claim_statements`.

The two-mode shape matches the user's "version the assembly" framing:
the assembly artifact is born once at the discovery → claim transition
(first claim-quiescence) as a real on-disk file, and on each
subsequent claim-quiescence wave the file is regenerated and the
substrate chain ticks once.
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_claims_statements, emit_derivation, emit_retired,
    emit_supersession,
)
from lib.predicates import claims_statements_for_note
from lib.protocols.febe.protocol import Session
from lib.renderers.claim_statements import render_claim_statements
from lib.shared.paths import transclusion_path


class ClaimsStatementsRefreshAgent(Agent):
    """Create-or-advance the claims.statements aggregate."""

    role: ClassVar[str] = "claims-statements-refresh"

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        doc = claims_statements_for_note(session, note_addr)
        if doc is None:
            doc = self._create(session, note_addr)
            self._write_content(session, doc)
            print(
                f"  [CLAIMS-STATEMENTS-REFRESH] created {doc}",
                file=sys.stderr,
            )
            return AgentResult(success=True, detail="created")

        self._write_content(session, doc)
        new_addr = session.register_version(doc)
        print(
            f"  [CLAIMS-STATEMENTS-REFRESH] advanced {doc} -> {new_addr}",
            file=sys.stderr,
        )
        return AgentResult(success=True, detail="advanced")

    def _create(self, session: Session, note_addr: Address) -> Address:
        """Mint the aggregate address, file the identity classifier,
        retire note.statements, and emit the supersession bridge.
        """
        store = session.store
        lattice_root = store.lattice_dir.resolve()
        note_path = session.get_path_for_addr(note_addr)
        asn_label = _asn_label_from_path(note_path)

        rel = str(
            transclusion_path(asn_label, "claim-statements")
            .resolve().relative_to(lattice_root)
        )
        addr = store.register_path(rel)

        emit_claims_statements(store, addr)
        emit_derivation(store, note_addr, addr)

        sidecar = _note_statements_sidecar(session, note_addr)
        if sidecar is not None:
            emit_supersession(store, sidecar, addr)
            emit_retired(store, sidecar)

        return addr

    def _write_content(self, session: Session, addr: Address) -> None:
        """Mechanically assemble the aggregate's content and write to disk."""
        rel = session.get_path_for_addr(addr)
        if rel is None:
            return
        full = session.store.lattice_dir / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        content = render_claim_statements(session, addr)
        full.write_text(content)


def _note_statements_sidecar(
    session: Session, note_addr: Address,
) -> Optional[Address]:
    """Resolve the note's `statements` attribute sidecar, or None."""
    for link in session.active_links("statements", from_set=[note_addr]):
        if link.to_set:
            return link.to_set[0]
    return None


def _asn_label_from_path(path: str) -> str:
    m = re.search(r"(ASN-\d{4})", path or "")
    return m.group(1) if m else "ASN-????"
