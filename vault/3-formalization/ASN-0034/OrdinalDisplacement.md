### Ordinal displacement and shift

**OrdinalDisplacement (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

Since δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, it satisfies the carrier set criterion, so δ(n, m) ∈ T by T0. Since n ≥ 1, the m-th component of δ(n, m) is nonzero, whence δ(n, m) > 0 by PositiveTumbler.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m with action point m
- *Postconditions:* δ(n, m) ∈ T (by T0), δ(n, m) > 0 (by PositiveTumbler)
