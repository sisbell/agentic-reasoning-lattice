"""Claim-describe trigger — fires on claims whose description is stale.

  scope:     each claim derived from the requested ASN's source note
  predicate: description_is_fresh
  agent:     ClaimDescribeAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.claim_describe import ClaimDescribeAgent
from lib.backend.addressing import Address
from lib.predicates import derived_claims, description_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    Filters out non-claim derivations (e.g., the claim-statements
    view doc) so the agent only describes actual claims.
    """
    if scope.asn_label is None:
        return
    asn_num = int(scope.asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return
    rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(rel)
    if note_addr is None:
        return
    for derived_addr in derived_claims(session, note_addr):
        if session.active_links("claim", to_set=[derived_addr]):
            yield derived_addr


claim_describe = Trigger(
    name="claim-describe",
    scope_query=_scope_query,
    predicate=description_is_fresh,
    agent=ClaimDescribeAgent(),
)
