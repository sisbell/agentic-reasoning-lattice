### Ordinal displacement and shift

**OrdinalDisplacement (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

Since δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, it satisfies the carrier set criterion, so δ(n, m) ∈ T by T0. Since n ≥ 1, the m-th component of δ(n, m) is nonzero, whence Pos(δ(n, m)) by TA-Pos. By ActionPoint, actionPoint(δ(n, m)) = min({i : 1 ≤ i ≤ m ∧ δ(n, m)ᵢ ≠ 0}); since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≥ 1, the minimum is m. ∎

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m
- *Depends:* T0 (CarrierSetDefinition) — invoked to discharge `δ(n, m) ∈ T` ("Since δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, it satisfies the carrier set criterion, so δ(n, m) ∈ T by T0"), where T0's three-part membership characterisation of T as the set of finite sequences over ℕ with length ≥ 1 supplies the carrier-set criterion. TA-Pos (PositiveTumbler) — invoked to discharge `Pos(δ(n, m))` ("Since n ≥ 1, the m-th component of δ(n, m) is nonzero, whence Pos(δ(n, m)) by TA-Pos"), where TA-Pos's positivity predicate is satisfied by the nonzero m-th component. ActionPoint (ActionPoint) — invoked to discharge `actionPoint(δ(n, m)) = m` ("By ActionPoint, actionPoint(δ(n, m)) = min({i : 1 ≤ i ≤ m ∧ δ(n, m)ᵢ ≠ 0}); since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≥ 1, the minimum is m"), where ActionPoint's defining minimum-position formula is computed against the explicit component pattern of δ.
- *Postconditions:* δ(n, m) ∈ T (by T0), Pos(δ(n, m)) (by TA-Pos), actionPoint(δ(n, m)) = m (by ActionPoint)
