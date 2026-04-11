## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. But the mapping has internal structure: contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (FiniteArrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin follows from the operational reality: each V-position enters `dom(M(d))` through a specific operation (INSERT, COPY, etc.), and the system has performed only finitely many operations. No operation introduces infinitely many V-positions.
