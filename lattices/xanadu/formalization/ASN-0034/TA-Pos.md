## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. Every tumbler in `T` is either positive or a zero tumbler, and none is both. This equivalence rests on logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

A separate consequence concerns the content of the partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` exhibits a nonzero component and `Zero(t)` makes every component equal to `0`.

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))`; `(A t ∈ T :: Zero(t) ⟺ (A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0))`; **Z** = {t ∈ T : Zero(t)}.
- *Consequence:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` cited in the partition-consequence prose.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

*Note on notation (outside the formal contract).* The predicate `Pos(t)` is not written `t > 0`, because `>` is reserved elsewhere for a lexicographic ordering on tumblers under which a zero tumbler may strictly exceed another zero tumbler: the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds. Writing `Pos(t)` as `t > 0` would therefore conflate two distinct relations. The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos.
