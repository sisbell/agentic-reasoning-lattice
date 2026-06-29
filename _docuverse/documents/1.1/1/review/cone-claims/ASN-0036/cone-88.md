## Audit Trace

**Dependency graph:** Σ.M(d) and subspace both root at T0. V-sub composes them. S8a, S8-fin, S8-depth, D-CTG each consume V-sub or dom(Σ.M(d)) directly. D-CTG-depth sits at the apex, drawing on all five posits plus the full NAT-\* and T-series foundation stack. No circularity.

**Posit inventory:** D-CTG, S8-depth, S8-fin, S8a are all correctly marked as protocol design posits, each with an explicit "not derived from X, Y, Z" disclaimer. The disclaimers are accurate: AX-1/AX-2 fix base state and V-mapping targets respectively, never key shape or betweenness; S0–S3 govern C alone. ✓

**D-CTG formal statement:** Guard `#v = #u` (not `#v = #q`) is consistent — S8-depth makes all V_1(d) members share depth m, so both extremes have the same depth and the guard is equivalent to `#v = m`. Quantifier is well-typed: v ∈ T for component projection and length; tumbler order from T1; zeros from T4; subspace from its own definition. Depends list complete. ✓

**D-CTG-depth — proof walk:**

*Setup.* Negating the postcondition yields two positions u, x ∈ V_1(d) disagreeing at some interior component. T3 gives u ≠ x from any component disagreement; T1 trichotomy then forces u < x or x < u. The proof's witness construction is symmetric under relabeling (disagreement set, j, and witness shape are all invariant), so WLOG u < x is valid. ✓

*First disagreement j.* The interior disagreement set {i : 2 ≤ i ∧ i+1 ≤ m ∧ uᵢ ≠ xᵢ} ⊆ ℕ is non-empty by assumption; NAT-wellorder yields least element j. Properties: 2 ≤ j, j+1 ≤ m, uⱼ ≠ xⱼ; minimality gives uᵢ = xᵢ for all 2 ≤ i < j; adding u₁ = x₁ = 1 (both V_1(d) members) gives agreement on all 1 ≤ i < j. ✓

*Pinning T1's witness to j.* Clause (ii) of T1 demands #u+1 ≤ #x, i.e., m+1 ≤ m — forbidden by NAT-addcompat's m < m+1 and NAT-order trichotomy. Clause (i) holds. The witness k satisfies k ≥ j (if k < j then uₖ = xₖ contradicts uₖ < xₖ) and k ≤ j (if k > j then T1's agreement covers i = j, contradicting disagreement there). So k = j and uⱼ < xⱼ. ✓

*Witness construction and ordering.* For any n > uⱼ₊₁, define w of depth m: copy u on positions 1–j; set wⱼ₊₁ = n; fill positions j+2 through m with 1 (empty range when j+1 = m). Component map is total and ℕ-valued (uᵢ ∈ ℕ from T0; n ∈ ℕ extracted from T0(a)'s tumbler; 1 ∈ ℕ from NAT-closure). T0 comprehension gives w ∈ T. ✓

- **u < w:** w agrees with u on 1–j; wⱼ₊₁ = n > uⱼ₊₁; j+1 ≤ m = min(m,m) satisfies T1(i). ✓
- **w < x:** w agrees with x on 1 through j−1 (since u and x agree there by minimality of j); wⱼ = uⱼ < xⱼ. Need j ≤ m for T1(i). Backward direction: j+1 ≤ m and j < j+1 (NAT-addcompat) chain via NAT-order transitivity to j < m, hence j ≤ m. ✓

*Zero-freeness of w.* Components 1–j positive by S8a applied to u ∈ dom(M(d)). wⱼ₊₁ = n > uⱼ₊₁ > 0 by NAT-order transitivity. wᵢ = 1 > 0 for j+2 ≤ i ≤ m by NAT-closure's 0 < 1. Component-filter {i : wᵢ = 0} = ∅; NAT-card's k=0 case gives zeros(w) = 0. D-CTG's guards are all met; D-CTG deposits w ∈ V_1(d) ⊆ dom(Σ.M(d)). ✓

*Infinite sequence via T0(a).* T0(a) at t = u, i = j+1, successive bounds: n₁ > uⱼ₊₁, n₂ > n₁, … gives strictly increasing n₁ < n₂ < …, each ∈ ℕ (component of a T0 tumbler). Corresponding witnesses w⁽¹⁾, w⁽²⁾, … are distinct by T3 (differing at component j+1). Each lands in dom(Σ.M(d)) via D-CTG. ✓

*Finiteness contradiction via S8-fin.* S8-fin supplies N ∈ ℕ and bijection f : {j ∈ ℕ : 1 ≤ j ≤ N} → dom(Σ.M(d)) — total, injective (distinct indices distinct values), surjective. Take first N+1 witnesses. Surjectivity gives jₖ ∈ {1,…,N} with f.jₖ = w⁽ᵏ⁾. Map k ↦ jₖ is injective: jₖ = jₗ ⟹ f.jₖ = f.jₗ (single-valued) ⟹ w⁽ᵏ⁾ = w⁽ˡ⁾, contradicting k ≠ l. So {jₖ : 1 ≤ k ≤ N+1} ⊆ {j ∈ ℕ : 1 ≤ j ≤ N} has N+1 pairwise-distinct members. NAT-card value clause: N+1 distinct naturals totally ordered by NAT-order trichotomy, strictly increasing enumeration of length N+1, so |{jₖ}| = N+1. NAT-card upper bound at n = N: |{jₖ}| ≤ N. Combined: N+1 ≤ N. NAT-addcompat gives N < N+1; chained with N+1 ≤ N by NAT-order transitivity gives N < N; NAT-order irreflexivity rejects this. Contradiction. ✓

**Postcondition coverage.** Universal over all pairs u, x ∈ V_1(d). u = x: trivial (uᵢ = xᵢ). u ≠ x, both orderings: relabeling symmetry. Singleton V_1(d): universal vacuously holds. ✓

**Prefix reduction remark.** Postcondition establishes agreement on interior components 2–(m−1); combined with subspace(p) = p₁ = 1 for all p ∈ V_1(d) (component 1 fixed), the full prefix 1–(m−1) agrees. Positions differ only at component m. This reading-off is correct and consistent with what D-SEQ would consume. ✓

**Depends list completeness.** All symbols appearing in D-CTG-depth's proof body are accounted for: V-sub (V_1(d) membership), S8-depth (common depth m), T1 (trichotomy and clause (i)), NAT-order (transitivity, irreflexivity), NAT-addcompat (strict successor, backward direction j+1 ≤ m ⟹ j < m), NAT-wellorder (first disagreement), S8a (component positivity of u), D-CTG (forces w ∈ V_1(d)), NAT-closure (1 ∈ ℕ, 0 < 1), T4 (zeros), NAT-card (empty-set characterization, value clause, upper bound), T0 (comprehension for w ∈ T), T0(a) (infinite sequence), T3 (distinctness of witnesses), S8-fin (bijection structure), subspace (w₁ = u₁ = 1 check). ✓

No uncovered cases, no ungrounded symbols, no broken precondition chains, no circular dependencies found across the full claim system.

VERDICT: CONVERGED