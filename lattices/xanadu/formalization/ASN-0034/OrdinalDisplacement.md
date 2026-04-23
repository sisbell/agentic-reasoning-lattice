### Ordinal displacement and shift

**OrdinalDisplacement (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, so δ(n, m) ∈ T by T0. Component typing: the m-th component is n, with `n ∈ ℕ` from the precondition; positions 1..m−1 are 0, with `0 ∈ ℕ` from NAT-zero's first axiom clause `0 ∈ ℕ`.

The length postcondition `#δ(n, m) = m` holds by construction from the Definition clause.

Promote `n ≥ 1` to `n ≠ 0`: NAT-addcompat's `(A n ∈ ℕ :: n < n + 1)` at n = 0 gives `0 < 0 + 1`. NAT-closure posits `1 ∈ ℕ` directly, licensing its additive identity `(A n ∈ ℕ :: 0 + n = n)` to be instantiated at n = 1; this gives the equality `0 + 1 = 1`, and rewriting `0 < 0 + 1` by it yields `0 < 1`. NAT-order's `m ≤ n ⟺ m < n ∨ m = n` unfolds `n ≥ 1` to `1 < n ∨ 1 = n`. In the first disjunct, transitivity of `<` composes `0 < 1` with `1 < n` to yield `0 < n`; in the second, substitution of `n = 1` into `0 < 1` yields `0 < n`. By NAT-order's irreflexivity, `n ≠ 0`.

Since δ(n, m)ₘ = n and `n ≠ 0`, the m-th component is nonzero, whence Pos(δ(n, m)) by TA-Pos. By ActionPoint, actionPoint(δ(n, m)) = min({i : 1 ≤ i ≤ m ∧ δ(n, m)ᵢ ≠ 0}); since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≠ 0, this set equals {m}, whose minimum is m. ∎

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

*Formal Contract:*
- *Preconditions:* n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set criterion for `δ(n, m) ∈ T`; length operator `#·: T → ℕ` for `#δ(n, m) = m`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the m − 1 leading zero components.
  - NAT-order (NatStrictTotalOrder) — `≤`/`<` unfolding, transitivity of `<`, irreflexivity, used in `n ≥ 1 ⟹ n ≠ 0`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality at n = 0 supplies `0 < 0 + 1`, the pre-rewrite form of the anchor used in the `n ≥ 1 ⟹ n ≠ 0` promotion.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` directly and the additive identity `(A n ∈ ℕ :: 0 + n = n)`, whose instantiation at n = 1 gives `0 + 1 = 1`, rewriting `0 < 0 + 1` into the anchor `0 < 1` used in the `n ≥ 1 ⟹ n ≠ 0` promotion.
  - TA-Pos (PositiveTumbler) — positivity predicate witnessed at i = m.
  - ActionPoint (ActionPoint) — minimum-position formula evaluated against δ's component pattern.
- *Postconditions:* δ(n, m) ∈ T, #δ(n, m) = m, Pos(δ(n, m)), actionPoint(δ(n, m)) = m
