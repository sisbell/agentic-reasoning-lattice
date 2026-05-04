"""Full-review trigger — fires on the source note of an unconfirmed ASN.

Wires the FullReviewAgent (lib/agents/full_review/) to the substrate
predicate `is_asn_confirmed`. The note's address is the substrate
anchor for the derived ASN: transclude emits `provenance.derivation`
from note → each derived claim, and the agent walks those links to
find the claim cluster.

  scope:     the source note for the requested ASN
  predicate: is_asn_confirmed
  agent:     FullReviewAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.full_review import FullReviewAgent
from lib.backend.addressing import Address
from lib.predicates import is_asn_confirmed
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield the source note address for the requested ASN, if any."""
    if scope.asn_label is None:
        return
    asn_num = int(scope.asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return
    rel = str(asn_path.relative_to(LATTICE))
    addr = session.get_addr_for_path(rel)
    if addr is not None:
        yield addr


full_review = Trigger(
    name="full-review",
    scope_query=_scope_query,
    predicate=is_asn_confirmed,
    agent=FullReviewAgent(),
)
