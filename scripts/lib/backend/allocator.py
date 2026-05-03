"""Allocator discipline (ASN-0034 T10a).

Each allocator owns a base address and emits siblings densely via
inc(·, 0) — strictly +1 at the last position, no gaps (T10a, T10a.7).

To spawn a child allocator, the parent calls inc(·, k') with
k' ∈ {1, 2} on a t in its own domain. Each (t, k') pair produces at
most one child-spawning event (T10a axiom, enforced here by caching).

The at-most-once rule constrains *spawning*, not *emission* — a single
child allocator emits arbitrarily many sibling outputs once spawned.
"""

from __future__ import annotations

from typing import Dict, Tuple

from .addressing import Address, inc


class Allocator:
    def __init__(self, base: Address) -> None:
        self.base = base
        self._cursor: Address = base
        self._children: Dict[Tuple[Address, int], Allocator] = {}

    def emit_sibling(self) -> Address:
        addr = self._cursor
        self._cursor = inc(self._cursor, 0)
        return addr

    def get_or_spawn_child(self, t: Address, k_prime: int) -> "Allocator":
        if k_prime not in (1, 2):
            raise ValueError(f"k' must be 1 or 2, got {k_prime}")
        if k_prime == 2 and t.zeros() > 2:
            # T10a's T4-preservation precondition: zeros(t) ≤ 2 at k' = 2,
            # else inc(t, 2) introduces adjacent zeros (TA5a, case k ≥ 3).
            raise ValueError(
                f"k'=2 requires zeros(t) ≤ 2; {t} has zeros={t.zeros()}"
            )
        key = (t, k_prime)
        if key not in self._children:
            self._children[key] = Allocator(inc(t, k_prime))
        return self._children[key]

    def __repr__(self) -> str:
        return f"Allocator(base={self.base}, cursor={self._cursor})"
