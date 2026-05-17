"""Claims-statements refresh agent — owns the ASN-level
`claims.statements` aggregate's lifecycle.

Two-mode behavior driven by predicate state:

  First fire (claims confirmed, no aggregate yet) — *create*. Mint a
  substrate address for the aggregate, file the `claims.statements`
  identity classifier, emit `note → provenance.derivation →
  aggregate`, emit `supersession(note.statements → aggregate)` (so
  readers walking from the sidecar address land on the live
  aggregate), write the mechanically-assembled content to disk, and
  emit `citation.depends` from the new aggregate to each derived
  claim's current head (the freshness anchors). The sidecar is NOT
  retired — `retired` is the runner's note-skip signal and belongs
  on note docs, not on sidecars; the supersession bridge alone is
  enough to steer readers.

  Subsequent fires (aggregate exists, at least one claim has
  advanced past its anchor) — *advance*. Re-assemble the content
  from current per-claim files + sidecars, write the new content to
  disk, `register_version` to tick the substrate chain, then re-
  emit `citation.depends` from the new aggregate version to each
  derived claim's current head. The disk file always reflects the
  latest assembly; the chain advance + new anchors carry the
  cascade signal for downstream cites.

Assembly is mechanical (no LLM): walks `provenance.derivation` from
the note to enumerate derived claims, reads each claim's body
(Formal Contract section), name sidecar, and description sidecar,
and produces the consolidated markdown block via
`render_claim_statements`.

The 1:N variant of the citation-anchor freshness pattern. Each
fire emits N `citation.depends` links — one per derived claim —
from the new aggregate version to `version_head(claim)`. The
predicate `is_claims_statements_fresh` walks those anchors;
freshness is address-identity (every cited claim is still head),
not chain-length comparison.
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar, List, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation, emit_claims_statements, emit_derivation,
    emit_supersession,
)
from lib.predicates import (
    claims_statements_for_note, derived_claims, resolve_to_scope,
)
from lib.predicates.cascade import (
    cited_targets_in_chain, content_sources_for_claim,
)
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.renderers.claim_statements import render_claim_statements
from lib.lattice.labels import extract_label_digits, format_label


class ClaimsStatementsRefreshAgent(Agent):
    """Create-or-advance the claims.statements aggregate.

    The trigger feeds the agent one canonical claim of the ASN; the
    agent multi-holds every classified claim of the ASN (honest mutex
    against cone-review, per-claim refiners, etc.) and walks back to
    the note for the assembly work.
    """

    role: ClassVar[str] = "claims-statements-refresh"
    node: ClassVar[str] = "1.3"

    def resolve_holds(
        self, session: Session, addr: Address, scope_type: str,
    ) -> List[Address]:
        """Hold every classified claim of the ASN. Mutex against
        cone-review (apex hold) and per-claim refiners that edit the
        claim files the aggregate is rendering from."""
        note = resolve_to_scope(session, addr, "note")
        if note is None:
            return []
        classified = {
            link.to_set[0]
            for link in session.active_links("claim")
            if link.to_set
        }
        return [c for c in derived_claims(session, note) if c in classified]

    def run(self, session: Session, addr: Address) -> AgentResult:
        note_addr = resolve_to_scope(session, addr, "note")
        if note_addr is None:
            return AgentResult(
                success=False, detail="no-note-for-canonical-claim",
            )
        doc = claims_statements_for_note(session, note_addr)
        if doc is None:
            doc = self._create(session, note_addr)
            self._write_content(session, doc)
            self._emit_anchors(session, doc, note_addr)
            print(
                f"  [CLAIMS-STATEMENTS-REFRESH] created {doc}",
                file=sys.stderr,
            )
            return AgentResult(success=True, detail="created")

        self._write_content(session, doc)
        new_addr = session.register_version(doc)
        self._emit_anchors(session, doc, note_addr)
        print(
            f"  [CLAIMS-STATEMENTS-REFRESH] advanced {doc} -> {new_addr}",
            file=sys.stderr,
        )
        return AgentResult(success=True, detail="advanced")

    def _create(self, session: Session, note_addr: Address) -> Address:
        """Mint the aggregate address, file the identity classifier,
        and emit the supersession bridge from the note's statements
        sidecar.
        """
        store = session.store
        lattice_root = store.lattice_dir.resolve()
        note_path = session.get_path_for_addr(note_addr)
        asn_label = _asn_label_from_path(note_path)

        agg_path = self.claim_dir / asn_label / "_statements.md"
        rel = str(agg_path.resolve().relative_to(lattice_root))
        addr = store.register_path(rel)

        emit_claims_statements(store, addr)
        emit_derivation(store, note_addr, addr)

        sidecar = _note_statements_sidecar(session, note_addr)
        if sidecar is not None:
            emit_supersession(store, sidecar, addr)

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

    def _emit_anchors(
        self, session: Session, doc_addr: Address, note_addr: Address,
    ) -> None:
        """Emit `citation.depends` from the aggregate's current head to
        each content source whose `version_head` isn't already cited
        anywhere in the aggregate's supersession chain.

        Sources per claim come from `content_sources_for_claim` (claim
        doc + name sidecar + description sidecar today). Per-fire
        emissions are incremental — anchors from prior versions stay
        valid (append-only substrate), so unchanged sources don't
        get re-anchored. Only newly-advanced sources (or sources
        that have never been cited) produce fresh anchors.
        """
        store = session.store
        classified_claims = {
            link.to_set[0]
            for link in session.active_links("claim")
            if link.to_set
        }
        aggregate_head = version_head(session, doc_addr)
        cited = cited_targets_in_chain(session, doc_addr)
        for claim in derived_claims(session, note_addr):
            if claim not in classified_claims:
                continue
            for source in content_sources_for_claim(session, claim):
                target = version_head(session, source)
                if target in cited:
                    continue
                emit_citation(
                    store, aggregate_head, target, direction="depends",
                )
                cited.add(target)


def _note_statements_sidecar(
    session: Session, note_addr: Address,
) -> Optional[Address]:
    """Resolve the note's `statements` attribute sidecar, or None."""
    for link in session.active_links("statements", from_set=[note_addr]):
        if link.to_set:
            return link.to_set[0]
    return None


def _asn_label_from_path(path: str) -> str:
    digits = extract_label_digits(path or "")
    return format_label(int(digits)) if digits else format_label(0).replace("0000", "????")
