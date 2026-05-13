"""Patch-apply trigger — fires on substrate-resident patch.note docs
that haven't been applied yet.

  scope:     each `patch.note`-classified doc (CLI: filter to one
             ASN-scoped subdir; daemon: every active patch.note)
  predicate: skip if patch has any outbound `provenance.derivation`
             to a review-classified doc (i.e., the apply + review
             chain has already fired)
  agent:     PatchApplyAgent

Bridges operationally-emitted patches (e.g., from MotifDispatchAgent)
to the existing apply machinery. Operator-authored workspace patches
still go through `scripts/note-patch.py` CLI; this trigger fires on
already-substrate-resident patches.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.patch_apply import PatchApplyAgent
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield patch.note-classified addresses to consider this pass.

    Daemon mode: every patch.note. CLI mode (scope.asn_label set):
    filter to patches whose substrate path is under the requested
    ASN's `patch/note/<asn>/` subdir.
    """
    for link in session.active_links("patch.note"):
        if not link.to_set:
            continue
        patch_addr = link.to_set[0]
        if scope.asn_label is not None:
            path = session.get_path_for_addr(patch_addr)
            if path is None or f"/patch/note/{scope.asn_label}/" not in path:
                continue
        yield patch_addr


def _predicate(session: Session, patch_addr: Address) -> bool:
    """True (skip) iff the patch has outbound `provenance.derivation`
    to a `review`-classified doc — i.e., it's already been applied
    and its post-apply review has emitted.

    Operator-authored patches (promoted via note-patch.py CLI) carry
    outbound derivation to the target note from the promote step but
    NOT to a review until the apply has finished. This predicate
    specifically checks for the review-target shape so we don't skip
    not-yet-applied patches that happen to have target-note
    derivations.
    """
    for link in session.active_links(
        "provenance.derivation", from_set=[patch_addr],
    ):
        for target in link.to_set:
            if any(session.active_links("review", to_set=[target])):
                return True
            if any(session.active_links("review.content", to_set=[target])):
                return True
            if any(session.active_links("review.structural", to_set=[target])):
                return True
    return False


patch_apply = Trigger(
    name="patch-apply",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=PatchApplyAgent(),
)
