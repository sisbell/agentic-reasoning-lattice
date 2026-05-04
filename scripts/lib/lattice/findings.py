"""Per-finding doc materialization — shared across review domains.

Both note-convergence and claim-convergence reviews follow the same
pattern: write a per-finding markdown doc, then emit three substrate
facts (finding classifier, comment link to the target, provenance
derivation from the aggregate review). Targets and comment-kind sets
differ; the doc-write + link-emit shape is identical.

Atomicity story: operations are not transactional; partial failure
recoverable via reconciliation. See
docs/hypergraph-protocol/error-handling.md.
"""

from __future__ import annotations

from typing import Tuple

from lib.backend.addressing import Address
from lib.backend.emit import emit_comment, emit_derivation, emit_finding
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session


def record_one_finding(
    session: Session,
    *,
    finding_path_rel: str,
    body: str,
    target_addr: Address,
    review_addr: Address,
    comment_kind: str,
) -> Tuple[Address, Link]:
    """Materialize one finding: doc write + three substrate facts.

    1. session.update_document(finding_path_rel, body)
    2. emit_finding classifier on the per-finding doc
    3. emit comment.<comment_kind> from finding doc to target
    4. emit provenance.derivation from aggregate review to finding

    Caller is responsible for resolving target_addr and mapping the
    domain-specific classification to a substrate comment kind.

    Returns (finding_addr, comment_link).
    """
    session.update_document(finding_path_rel, body)
    finding_addr = session.register_path(finding_path_rel)
    emit_finding(session.store, finding_addr)
    comment = emit_comment(
        session.store, finding_addr, target_addr, kind=comment_kind,
    )
    emit_derivation(session.store, review_addr, finding_addr)
    return finding_addr, comment
