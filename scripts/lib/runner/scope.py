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
