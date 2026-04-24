**Divergence (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1.

  (i) If there exists `k` with `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b` and `aₖ ≠ bₖ`, then `divergence(a, b)` is the least such `k` — equivalently, the unique `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`, the universal conjunct restating minimality — component divergence at a shared position.

  (ii) If `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)` — equivalently, lengths differ and case (i) does not apply — then NAT-order's trichotomy applied to `(#a, #b)` rules out the `#a = #b` branch and splits on which length is shorter. In sub-case (ii-a), `#a < #b`, so `i ≤ #a` entails `i ≤ #b` by NAT-order transitivity and the range `1 ≤ i ≤ #a ∧ i ≤ #b` reduces to `1 ≤ i ≤ #a`, yielding `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, whence `divergence(a, b) = #a + 1`. In sub-case (ii-b), `#b < #a`, so `i ≤ #b` entails `i ≤ #a` by NAT-order transitivity and the range `1 ≤ i ≤ #a ∧ i ≤ #b` reduces to `1 ≤ i ≤ #b`, yielding `(A i : 1 ≤ i ≤ #b : aᵢ = bᵢ)`, whence `divergence(a, b) = #b + 1`. In either sub-case the divergence lies one position past the shorter tumbler's last component — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. Mutual exclusivity: if case (i) holds, some `aₖ ≠ bₖ` with `k ≤ #a ∧ k ≤ #b` falsifies case (ii)'s universal agreement at shared positions. Exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so by T3, `a = b`, contradicting `a ≠ b`.

The function is symmetric: `divergence(a, b) = divergence(b, a)`. In case (i), the qualifying conjunction is invariant under operand swap — `1 ≤ k` mentions neither operand, `k ≤ #a ∧ k ≤ #b` by `∧`-commutativity, `aₖ ≠ bₖ` by `≠`-symmetry, `(A i : 1 ≤ i < k : aᵢ = bᵢ)` by `=`-symmetry — so the same `k` witnesses case (i) under swap. In case (ii), swapping `(a, b)` exchanges sub-cases (ii-a) and (ii-b); both select one-plus the shorter tumbler's length.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* (i) if `(∃ k : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b : aₖ ≠ bₖ)`, then `divergence(a, b)` is the least `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)` (equivalently, the unique such `k`, the universal conjunct being the minimality condition restated); (ii) if `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)`, then `divergence(a, b) = #a + 1` when `#a < #b` (sub-case (ii-a)) and `divergence(a, b) = #b + 1` when `#b < #a` (sub-case (ii-b)).
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `a, b ∈ T`, lengths `#a, #b`, and component projections `aₖ, bₖ, aᵢ, bᵢ` as ℕ-valued, making component (in)equalities well-formed.
  - T1 (LexicographicOrder) — Divergence formalizes T1's "first divergence position"; case (i) corresponds to T1 case (i) and case (ii) (with sub-cases (ii-a)/(ii-b)) corresponds to T1 case (ii).
  - T3 (CanonicalRepresentation) — exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so `a = b`, contradicting `a ≠ b`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b).
  - NAT-wellorder (NatWellOrdering) — existence of a least element in the nonempty subset `{k ∈ ℕ : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ}` grounds case (i)'s designating description, so "the least such `k`" is non-vacuous.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#b, 1)`, with `1 ∈ ℕ` from the same axiom, well-types case (ii)'s values `#a + 1` and `#b + 1` as ℕ.
- *Postconditions:* `divergence(a, b) ∈ ℕ`; exactly one of case (i) or case (ii) applies; in case (ii), `divergence(a, b) = #a + 1` in sub-case (ii-a) and `divergence(a, b) = #b + 1` in sub-case (ii-b); `divergence(a, b) = divergence(b, a)` for all `a ≠ b`.
