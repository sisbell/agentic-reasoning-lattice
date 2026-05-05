"""Scope — restricts where a trigger fires.

A scope is a filter the runner passes to each trigger's `scope_query`.
The trigger consults it to decide which substrate addresses are in
range. Today scopes are ASN-level; the structure can grow as new
filtering needs surface.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scope:
    """Substrate filter for a runner invocation.

    asn_label: restricts to one ASN's claims/notes (e.g., "ASN-0034").
    labels:    further restricts to specific claim labels within asn_label.
    Both None means global scope (used by daemon mode).
    """

    asn_label: str | None = None
    labels: frozenset[str] | None = None


def asn(num: int) -> Scope:
    """Convenience: scope to one ASN by number."""
    return Scope(asn_label=f"ASN-{int(num):04d}")


def cone(asn_num: int, apex_label: str) -> Scope:
    """Convenience: scope to one apex within an ASN."""
    return Scope(
        asn_label=f"ASN-{int(asn_num):04d}",
        labels=frozenset([apex_label]),
    )


def asn_note_addr(session, scope: Scope):
    """Resolve scope.asn_label to its source-note substrate address.

    Returns None if no asn_label is set, no note exists for that
    ASN number, the note path isn't registered, or the note is
    retired (out of active lattice). Retired ASNs are filtered out
    of every trigger's scope.

    Centralizes the boilerplate that every ASN-scoped trigger's
    scope_query needs — parse asn_num, find_asn, get_addr_for_path,
    retired filter.
    """
    if scope.asn_label is None:
        return None
    from lib.predicates import is_retired
    from lib.shared.common import find_asn
    from lib.shared.paths import LATTICE
    asn_num = int(scope.asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return None
    rel = str(asn_path.relative_to(LATTICE))
    addr = session.get_addr_for_path(rel)
    if addr is None or is_retired(session, addr):
        return None
    return addr
