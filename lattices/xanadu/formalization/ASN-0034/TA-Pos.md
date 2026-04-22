## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. Here `tᵢ` is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` bounding that range is the non-strict companion of `<` defined on ℕ by NAT-order; the equality `tᵢ = 0` and the bounding inequalities `1 ≤ i ≤ #t` in the two clauses are thus well-typed within ℕ, and the negation `¬` in the `Pos` clause is classical propositional negation applied to that equality, requiring no additional symbol on ℕ.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. Every tumbler in `T` is either positive or a zero tumbler, and none is both. The equivalence follows from the defining clauses by logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. The quantifier range is nonempty because T0 imposes `(A a ∈ T :: #a ≥ 1)`, so the complementarity partitions `T` into genuine positives — tumblers with at least one nonzero component — and genuine zero tumblers — tumblers with at least one component, each equal to `0` — rather than collapsing to a vacuous coincidence on a length-`0` tumbler.

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `Pos(t)` iff `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`; **Z** = {t ∈ T : Zero(t)}.
- *Complementarity:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`, obtained from the defining clauses by the DeMorgan duality of bounded quantifiers, with T0's `(A a ∈ T :: #a ≥ 1)` keeping the index range nonempty so the partition is genuine.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: #a ≥ 1)` that keeps the quantifier range nonempty for the complementarity clause.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

*Note on notation (outside the formal contract).* The predicate `Pos(t)` is not written `t > 0`, because `>` is reserved elsewhere for a lexicographic ordering on tumblers under which a zero tumbler may strictly exceed another zero tumbler: the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds. Writing `Pos(t)` as `t > 0` would therefore conflate two distinct relations. The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos.
