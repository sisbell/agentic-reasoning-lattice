**Definition (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1.

  (i) If there exists `k` with `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `#a ≠ #b`, NAT-order's trichotomy applied to `(#a, #b)` rules out the `#a = #b` branch and leaves exactly one of `#a < #b` or `#b < #a`. In sub-case (ii-a), `#a < #b` and `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, whence `divergence(a, b) = #a + 1`. In sub-case (ii-b), `#b < #a` and `(A i : 1 ≤ i ≤ #b : aᵢ = bᵢ)`, whence `divergence(a, b) = #b + 1`. In either sub-case the divergence lies one position past the shorter tumbler's last component — prefix divergence, where one tumbler is a proper prefix of the other.

Case (i)'s value `k` is unique: `aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)` forces `k` to be the least element of `S := {i ∈ ℕ : 1 ≤ i ∧ i ≤ #a ∧ i ≤ #b ∧ aᵢ ≠ bᵢ}`, supplied by NAT-wellorder. Case (ii)'s value is determined arithmetically from the shorter length selected by NAT-order's trichotomy.

Exactly one case applies for any `a ≠ b`. Mutual exclusivity: if case (i) holds, some `aₖ ≠ bₖ` with `k ≤ #a ∧ k ≤ #b` falsifies case (ii)'s universal agreement at shared positions. Exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so by T3, `a = b`, contradicting `a ≠ b`.

The function is symmetric: `divergence(a, b) = divergence(b, a)`. In case (i), the qualifying set `S` is invariant under operand swap — `1 ≤ i` mentions neither operand, `i ≤ #a ∧ i ≤ #b` by `∧`-commutativity, `aᵢ ≠ bᵢ` by `≠`-symmetry — so NAT-wellorder returns the same least element; the prior-position agreement transforms by `=`-symmetry. In case (ii), swapping `(a, b)` exchanges sub-cases (ii-a) and (ii-b); both select one-plus the shorter tumbler's length.

For prefix-related pairs, `divergence(a, b) > #a` in sub-case (ii-a) and `divergence(a, b) > #b` in sub-case (ii-b). TA1-strict requires `actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b` and `actionPoint(w) ≥ divergence(a, b)`, which are jointly unsatisfiable for prefix-related operands. TA1 covers these cases, showing both results become equal and order is preserved as non-reversal.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* (i) if `∃ k : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `#a ≠ #b`, NAT-order's trichotomy on `(#a, #b)` rules out `#a = #b` and leaves exactly one of: (ii-a) `#a < #b` with `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, giving `divergence(a, b) = #a + 1`; or (ii-b) `#b < #a` with `(A i : 1 ≤ i ≤ #b : aᵢ = bᵢ)`, giving `divergence(a, b) = #b + 1`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `a, b ∈ T`, lengths `#a, #b`, and component projections `aₖ, bₖ, aᵢ, bᵢ` as ℕ-valued, making component (in)equalities well-formed.
  - T1 (LexicographicOrder) — Divergence formalizes T1's "first divergence position"; case (i) corresponds to T1 case (i) mediated by NAT-order trichotomy on `(aₖ, bₖ)` at caller sites; case (ii) corresponds directly to T1 case (ii), with sub-cases (ii-a)/(ii-b) fixing the T1 direction.
  - T3 (CanonicalRepresentation) — exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so `a = b`, contradicting `a ≠ b`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b); trichotomy at component pair `(aₖ, bₖ)` bridges case (i) to T1's directed case (i) at caller sites.
  - NAT-wellorder (NatWellOrdering) — least-element principle selects case (i)'s `k` from the nonempty subset `{i ∈ ℕ : 1 ≤ i ∧ i ≤ #a ∧ i ≤ #b ∧ aᵢ ≠ bᵢ}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — successor-closure `(A n ∈ ℕ :: n + 1 ∈ ℕ)` well-types case (ii)'s values `#a + 1` and `#b + 1` as ℕ.
- *Postconditions:* `divergence(a, b) ∈ ℕ`; exactly one of case (i) or case (ii) applies; in case (i), `divergence(a, b) = k` is the unique least index satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`; in case (ii), `divergence(a, b) = #a + 1` in sub-case (ii-a) and `divergence(a, b) = #b + 1` in sub-case (ii-b); `divergence(a, b) = divergence(b, a)` for all `a ≠ b`.
