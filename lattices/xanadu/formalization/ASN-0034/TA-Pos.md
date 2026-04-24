## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. Every tumbler in `T` is either positive or a zero tumbler, and none is both. This equivalence rests on logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

Reading the Definition against T0 gives the content of this partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` demands a nonzero component (the existential is not vacuous) and `Zero(t)` forces every component to equal `0` (the universal is not vacuous).

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))`; `(A t ∈ T :: Zero(t) ⟺ (A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0))`; **Z** = {t ∈ T : Zero(t)}.
- *Consequence:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` cited in prose to unpack the Definition's quantifier ranges.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

*Note on notation (outside the formal contract).* The predicate `Pos(t)` is written with a dedicated symbol rather than as `t > 0`: `>` is reserved for a separate tumbler ordering under which zero tumblers need not all be minimal, so writing `Pos(t)` as `t > 0` would conflate the two relations. This tumbler ordering is supplied by claims outside this region and enters no obligation of TA-Pos.
