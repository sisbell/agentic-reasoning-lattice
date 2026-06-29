Reading the foundation statements, then tracing each claim's formal contract and proof structure as a system.

**D-CTG, S8-depth, S8a, S8-fin, subspace, V-sub, Σ.M(d)** are posits, not derived results. Their formal contracts are clean, their Depends lists correctly scope to the symbols in each formal statement, and the cross-posit topological ordering is sound. S8a's exclusion from S8-depth's Depends list is correctly justified (S8a contributes no symbol to `#u = #w`); OrdShiftHom's exclusion from S8-depth's Depends list is likewise correct (shift and δ do not appear in the formal posit).

**D-CTG-depth** is the only claim with a substantive proof. I traced it step by step.

*Steps 1–8 are sound:*

- The negation of the postcondition is correctly formed; the unordered pair {u, x} is correctly ordered u < x by T1 trichotomy after T3 excludes u = x.
- The WLOG is valid: the disagreement predicate and all witness-construction steps are symmetric under the swap of u ↔ x (the construction copies the *smaller* member's prefix in both orderings).
- The first interior disagreement j is correctly extracted via NAT-wellorder from the non-empty subset `{i : 2 ≤ i ∧ i+1 ≤ m ∧ uᵢ ≠ xᵢ} ⊆ ℕ`.
- The pinning of T1's witness to k = j is correctly argued in both directions (k < j gives uₖ = xₖ contradicting uₖ < xₖ; k > j gives uⱼ = xⱼ contradicting uⱼ ≠ xⱼ).
- The backward direction of j+1 ≤ m ⟺ j < m is correctly attributed to NAT-addcompat (j < j+1) chained through NAT-order transitivity with j+1 ≤ m, rather than NAT-discrete (which supplies only the forward direction).
- The witness w's construction is correct component-by-component; the empty-clause case j+1 = m is handled.
- u < w is established by T1(i) at k = j+1 ≤ m; w < x is established by T1(i) at k = j < m.
- zeros(w) = 0 is correctly derived: components i ≤ j from S8a's positivity predicate on u, component j+1 = n via NAT-order transitivity `0 < uⱼ₊₁ < n`, components j+2 through m from NAT-closure's consequence `0 < 1`.
- D-CTG is correctly applied: v = w ∈ T (T0 comprehension), subspace(w) = 1, #w = m = #u, zeros(w) = 0, u < w < x — all guards satisfied.
- T0(a) correctly yields an infinite strictly increasing sequence n₁ < n₂ < … exceeding uⱼ₊₁, giving infinitely many distinct w's (distinct by T3) in V_1(d).

*Step 9 is not established:*

---

### S8-fin contradiction in D-CTG-depth is not formally derived

**Class**: REVISE
**Foundation**: S8-fin (FiniteArrangement), NAT-card (NatFiniteSetCardinality), NAT-addcompat (NatAdditionOrderAndSuccessor), NAT-order (NatStrictTotalOrder)
**ASN**: D-CTG-depth proof, final paragraph — "The sequence is infinite and pairwise distinct. Distinct values of n yield distinct tumblers w … This produces infinitely many distinct positions in V_1(d), contradicting S8-fin (dom(M(d)) is finite)."
**Issue**: The proof constructs an infinite pairwise-distinct sequence of positions in V_1(d) ⊆ dom(M(d)) and asserts this contradicts S8-fin without deriving the contradiction from S8-fin's bijection formulation. S8-fin's axiom supplies a specific witness `n ∈ ℕ` and bijection `f : {j ∈ ℕ : 1 ≤ j ≤ n} → dom(Σ.M(d))`. "Infinitely many elements exist but the domain is finite" is not immediate from this formulation — it requires a derivation the proof does not give. Concretely: to go from "infinitely many distinct wₖ" to a formal arithmetic contradiction, one must (1) fix S8-fin's witness n; (2) select n+1 specific wₖ from the constructed infinite sequence; (3) by surjectivity of f, each wₖ = f(jₖ) for some jₖ ∈ {1,…,n}; by injectivity of f (the clause `(A i,j : 1 ≤ i < j ≤ n : f.i ≠ f.j)` and its contrapositive: f.i = f.j ∧ i < j gives f.i ≠ f.j, contradiction, so i = j), the jₖ are pairwise distinct; (4) apply NAT-card's upper bound — `|{j₁,…,jₙ₊₁}| ≤ n` since `{j₁,…,jₙ₊₁} ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` — while NAT-card's axiom gives `|{j₁,…,jₙ₊₁}| = n+1` (the unique k for which a strictly increasing length-k enumeration of the n+1 distinct elements exists); (5) n+1 ≤ n together with n < n+1 (NAT-addcompat at n) gives n < n by transitivity (NAT-order), contradicting irreflexivity ¬(n < n). None of steps (1)–(5) appear in the proof. This gap is inconsistent with D-CTG-depth's own level of detail, which carefully derives the backward direction of j+1 ≤ m ⟺ j < m and explicitly walks the three component-positivity cases for zeros(w) = 0.
**What needs resolving**: The proof should walk the five-step derivation above, or invoke a separately proved lemma of the form "a set in bijection with `{1,…,n}` has no n+1 pairwise distinct members" whose proof uses NAT-card's upper bound and NAT-addcompat's n < n+1. NAT-card and NAT-addcompat are already in D-CTG-depth's Depends list and suffice; no new dependency is introduced.

VERDICT: REVISE