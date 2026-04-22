## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. Here `tᵢ` is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` bounding that range is the non-strict companion of `<` defined on ℕ by NAT-order; the equality `tᵢ = 0` and the bounding inequalities `1 ≤ i ≤ #t` in the two clauses are thus well-typed within ℕ, and the negation `¬` in the `Pos` clause is classical propositional negation applied to that equality, requiring no additional symbol on ℕ.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. Every tumbler in `T` is either positive or a zero tumbler, and none is both. This equivalence rests on logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i : 1 ≤ i ≤ #t : tᵢ = 0)`, irrespective of whether the index range `{i : 1 ≤ i ≤ #t}` is empty; at a hypothetical length-`0` tumbler `Pos` would reduce to `False` and `Zero` to `True`, and the biconditional `False ⟺ ¬True` would still hold.

A separate consequence concerns the content of the partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` witnesses the existence of a nonzero component and `Zero(t)` witnesses the existence of a component equal to `0`. A length-`0` tumbler would satisfy `Zero(t)` vacuously, since the universal over an empty index range holds trivially; T0's clause removes that degenerate case from `T`.

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `Pos(t)` iff `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`; **Z** = {t ∈ T : Zero(t)}.
- *Complementarity:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Nonvacuity of the partition:* the index range `1 ≤ i ≤ #t` in the Pos/Zero clauses is nonempty for every `t ∈ T`, by T0's `(A a ∈ T :: 1 ≤ #a)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` underwriting the Nonvacuity clause.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

*Note on notation (outside the formal contract).* The predicate `Pos(t)` is not written `t > 0`, because `>` is reserved elsewhere for a lexicographic ordering on tumblers under which a zero tumbler may strictly exceed another zero tumbler: the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds. Writing `Pos(t)` as `t > 0` would therefore conflate two distinct relations. The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos.
