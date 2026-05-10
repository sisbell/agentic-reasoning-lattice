## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. This equivalence rests on logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

Reading the Definition against T0 gives the content of this partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` demands a nonzero component (the existential is not vacuous) and `Zero(t)` forces every component to equal `0` (the universal is not vacuous).

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))`; `(A t ∈ T :: Zero(t) ⟺ (A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0))`; **Z** = {t ∈ T : Zero(t)}.
- *Consequence:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` cited in prose to unpack the Definition's quantifier ranges.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the bounded existential `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` of the `Pos` clause and the bounded universal `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` of the `Zero` clause, over which the index variable `i` ranges before being further restricted by the carrier-side clause `i ∈ ℕ` and the term-side range `1 ≤ i ≤ #t`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.
