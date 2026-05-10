"""Agent-coordination predicates: holding and scope resolution.

Implements the substrate-side mechanisms for the repellent-pheromone
coordination pattern (per docs/design-notes/stigmergic-coordination.md):

- `is_held(resource)` — substrate-pure check for active `holding`
  links targeting a resource. Used by trigger predicates to yield
  when another agent is currently active on the same resource.
- `agent_scope_for(agent_doc)` — read the `agent.scope.<type>`
  classifier on an agent doc to discover its declared hold scope.
- `resolve_to_scope(addr, scope_type)` — walk substrate to map an
  arbitrary address (apex claim, comment, etc.) to a resource of
  the requested scope type. Returns None if unresolvable; callers
  treat None as a hard error (no silent fall-through to fire-without-
  hold).
- `stale_holdings(max_age_seconds)` — operator-facing observability:
  return holdings whose emit-time `ts` is older than the threshold.
  Uses the per-link `ts` field (Unix int seconds) per
  `feedback_ts_scoped_to_agentic.md` — `ts` is scoped to agentic
  concerns; this is one of those concerns.

Convention: predicate code reads `active_links` (open holdings only).
Closed holdings are completion data; predicate-layer code does not
read them.
"""

from __future__ import annotations

import time
from typing import List, Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


_VALID_SCOPE_TYPES = frozenset({"note", "claim", "inquiry", "lattice"})


def is_held(session: Session, resource_addr: Address) -> bool:
    """True iff any agent has an active `holding` against this resource."""
    return bool(
        session.active_links("holding", to_set=[resource_addr])
    )


def agent_scope_for(
    session: Session, agent_doc: Address,
) -> Optional[str]:
    """Read the `agent.scope.<type>` classifier on an agent doc.

    Returns the scope-type suffix (`"note"`, `"claim"`, `"inquiry"`)
    or None if no scope classifier is present. Multiple classifiers
    on one agent doc would return the first found in registry order
    (an agent should declare at most one scope).
    """
    for scope_type in _VALID_SCOPE_TYPES:
        if session.active_links(
            f"agent.scope.{scope_type}", to_set=[agent_doc],
        ):
            return scope_type
    return None


def resolve_to_scope(
    session: Session, addr: Address, scope_type: str,
) -> Optional[Address]:
    """Walk substrate to map `addr` to a resource of `scope_type`.

    Dispatch:
      scope_type="note"    + addr is note    → addr
                           + addr is claim   → walk provenance.derivation reverse to source note
                           + addr is comment → walk to comment's targeted claim, then to source note
      scope_type="claim"   + addr is claim   → addr
                           + addr is comment → comment's targeted claim
      scope_type="inquiry" + addr is inquiry → addr
      scope_type="lattice" + addr has outgoing `lattice` link → that link's target
                           + addr is itself a lattice doc → addr

    Returns None if the addr cannot be resolved to the requested
    scope. Callers (agent base class) treat None as a hard error.
    """
    if scope_type == "note":
        return _addr_to_note(session, addr)
    if scope_type == "claim":
        return _addr_to_claim(session, addr)
    if scope_type == "inquiry":
        return _addr_to_inquiry(session, addr)
    if scope_type == "lattice":
        return _addr_to_lattice(session, addr)
    return None


def stale_holdings(
    session: Session, max_age_seconds: int,
) -> List:
    """Return active `holding` links open longer than `max_age_seconds`.

    Operator-facing observability for stuck-fire detection. Reads
    per-link `ts` (Unix int seconds) directly. Links without `ts`
    (in-memory test fixtures) are skipped.

    Returned entries are full Link objects so callers can inspect
    `from_set` (which agent), `to_set` (which resource), and `ts`
    (when emitted).
    """
    threshold = int(time.time()) - max_age_seconds
    out = []
    for link in session.active_links("holding"):
        if link.ts is not None and link.ts < threshold:
            out.append(link)
    return out


# ─── Helpers ───────────────────────────────────────────────────────


def _addr_to_note(session: Session, addr: Address) -> Optional[Address]:
    """Resolve `addr` to its containing note address, or None."""
    if _is_classified_as(session, addr, "note"):
        return addr
    if _is_classified_as(session, addr, "claim"):
        # Walk provenance.derivation reverse: claim ← derivation ← note
        for link in session.active_links(
            "provenance.derivation", to_set=[addr],
        ):
            if link.from_set:
                source = link.from_set[0]
                if _is_classified_as(session, source, "note"):
                    return source
        return None
    if _is_comment(session, addr):
        # Comment → targeted doc → (if claim) → note
        target = _comment_target(session, addr)
        if target is None:
            return None
        return _addr_to_note(session, target)
    return None


def _addr_to_claim(session: Session, addr: Address) -> Optional[Address]:
    """Resolve `addr` to its associated claim address, or None."""
    if _is_classified_as(session, addr, "claim"):
        return addr
    if _is_comment(session, addr):
        target = _comment_target(session, addr)
        if target is None:
            return None
        if _is_classified_as(session, target, "claim"):
            return target
        return None
    # Review doc: walk outgoing `review.coverage` to the claim it covers.
    for link in session.active_links("review.coverage", from_set=[addr]):
        if link.to_set:
            target = link.to_set[0]
            if _is_classified_as(session, target, "claim"):
                return target
    return None


def _addr_to_inquiry(session: Session, addr: Address) -> Optional[Address]:
    """Resolve `addr` to its associated inquiry address, or None."""
    if _is_classified_as(session, addr, "inquiry"):
        return addr
    return None


def _addr_to_lattice(session: Session, addr: Address) -> Optional[Address]:
    """Resolve `addr` to its containing lattice doc, or None.

    Resolution order:
      1. If `addr` has an outgoing `lattice` membership link, return
         that link's target — every doc registered under the active
         lattice gets such a link, so this is the common path.
      2. Else if `addr` is itself a lattice doc (target of `lattice`
         membership links from other docs, but no outgoing `lattice`
         link of its own), return `addr`.
      3. Else None.

    Lattice docs aren't carrying a separate `lattice` classifier today
    (the `lattice` link type is membership-only). Detection-by-being-
    target is the practical signal until/unless a classifier is added.
    """
    # Outgoing membership: addr → lattice doc
    out = session.active_links("lattice", from_set=[addr])
    if out and out[0].to_set:
        return out[0].to_set[0]
    # Incoming membership: addr is the target of others → addr is itself
    # a lattice doc
    incoming = session.active_links("lattice", to_set=[addr])
    if incoming:
        return addr
    return None


def _is_classified_as(
    session: Session, addr: Address, kind: str,
) -> bool:
    """True iff `addr` carries an active classifier of the given kind."""
    return bool(session.active_links(kind, to_set=[addr]))


_TYPE_REGISTRY_CACHE: dict = {}


def _type_registry_for(session: Session):
    """Return a cached TypeRegistry rooted at the substrate's registry
    doc. Module-level cache keyed on registry-doc address; TypeRegistry
    construction iterates ~50 CANONICAL_POSITIONS entries — cheap but
    not free when called per resolve."""
    key = str(session.store.registry_doc)
    registry = _TYPE_REGISTRY_CACHE.get(key)
    if registry is None:
        from lib.backend.types import TypeRegistry
        registry = TypeRegistry(session.store.registry_doc)
        _TYPE_REGISTRY_CACHE[key] = registry
    return registry


def _is_comment(session: Session, addr: Address) -> bool:
    """True iff the addr is a comment.* link addr (not a doc).

    Detection: fetch the link and decode its `type_set` against the
    type registry; comments have type names starting with `comment`.
    `Link.type_` (the string-name attribute) is None for substrate-
    loaded links — only `type_set` (tuple of type addresses) is
    populated by the JSONL loader, so decoding is required.
    Falls back to False if the addr isn't a link or fetch fails.
    """
    try:
        link = session.get_link(addr)
    except (KeyError, AttributeError):
        return False
    registry = _type_registry_for(session)
    for type_addr in link.type_set:
        name = registry.name_for(type_addr)
        if name and name.startswith("comment"):
            return True
    return False


def _comment_target(
    session: Session, comment_addr: Address,
) -> Optional[Address]:
    """Return the comment's first target (single-target invariant for
    comments — one comment is about one doc). None if unresolvable.
    """
    try:
        link = session.get_link(comment_addr)
    except (KeyError, AttributeError):
        return None
    if not link.to_set:
        return None
    return link.to_set[0]


