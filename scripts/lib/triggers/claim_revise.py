"""Claim-revise trigger — fires per unresolved comment.revise on a
claim in the requested ASN.

  scope:     each open `comment.revise` link targeting a claim that
             is derived from the requested ASN's source note (CLI),
             or every active comment.revise (daemon)
  predicate: has_resolution (skip if a resolution.* link already
             targets the comment)
  agent:     ClaimReviseAgent

Per-comment granularity: the comment is the substrate predicate, not
the claim. The runner walks each unresolved comment, the agent fires
once per comment, and quiescence = every applicable comment has been
resolved.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.refiners.claim_revise import ClaimReviseAgent
from lib.backend.addressing import Address
from lib.predicates import has_resolution
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.triggers._commit_paths import (
    _asn_label_from_path, per_claim_commit_paths, rationale_dir_for_asn,
)
from lib.triggers.scope import _claim_set_for_scope


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield comment.revise addresses to consider this pass.

    CLI mode: comments whose target is a claim derived from the
    ASN's source note. Daemon mode: every active comment.revise.
    """
    if scope.asn_label is None:
        for link in session.active_links("comment.revise"):
            yield link.addr
        return

    scope_claims = _claim_set_for_scope(session, scope)
    for link in session.active_links("comment.revise"):
        if not link.to_set:
            continue
        if link.to_set[0] not in scope_claims:
            continue
        yield link.addr


def _commit_paths(session: Session, comment_addr: Address) -> list[str]:
    """Resolve the comment's target claim and return that claim's
    file family, plus the per-ASN rationale dir for any
    `resolution.py reject` calls the reviser made.
    """
    try:
        comment = session.get_link(comment_addr)
    except KeyError:
        return []
    if not comment.to_set:
        return []
    claim_addr = comment.to_set[0]
    paths = per_claim_commit_paths(session, claim_addr)
    claim_path = session.get_path_for_addr(claim_addr)
    asn_label = _asn_label_from_path(claim_path) if claim_path else None
    rdir = rationale_dir_for_asn(claim_path, asn_label)
    if rdir:
        paths.append(rdir)
    return paths


claim_revise = Trigger(
    name="claim-revise",
    scope_query=_scope_query,
    predicate=has_resolution,
    agent=ClaimReviseAgent(),
    supports_claim_filter=True,
    commit_paths=_commit_paths,
)
