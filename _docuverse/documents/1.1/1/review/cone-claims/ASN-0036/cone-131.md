The audit below works through the full dependency graph — foundations through posits through theorems — checking definition stability, precondition chains, proof coverage, and Depends completeness.

---

**Foundation audit.** All NAT-* foundations are internally consistent. NAT-order's exactly-one trichotomy and ≤-transitivity consequences are correctly derived from the axiom clauses. NAT-discrete's no-interval consequence is correctly derived. NAT-induction is correctly identified as independent of the order-and-addition axioms (non-categorical) and posited rather than derived. NAT-card's k=0 case correctly grounds |∅|=0 without convention on empty functions.

**Σ.M(d) → subspace → V-sub chain.** Clean. The text-subspace constant `1 ∈ ℕ` is grounded from NAT-closure at every site that writes it as a first-class value (V-sub, subspace's depth guard). Neither subspace nor T0 re-exports that constant, so each consumer that writes it directly grounds it from NAT-closure. ✓

**Posit consistency.** S8a, D-CTG, S8-depth, and S8-fin are all clearly labeled as design constraints, not theorems. None of them are claimed to follow from S0–S3, AX-1, or AX-2; the prose explanation of why they cannot is accurate. ✓

**D-PRED proof.** The set H = {n ∈ ℕ : n = 0 ∨ (E i ∈ ℕ :: i+1 = n)} contains 0 (left disjunct) and is closed under successor (i := k witnesses the right disjunct for k+1, no membership of k consulted). NAT-induction gives H = ℕ. For j ≥ 1: the chain 0 < 1 ≤ j → 0 < j (two-case split on NAT-order's ≤-definition) then irreflexivity excludes j = 0. Predecessor existence follows. NAT-induction is correctly identified as the load-bearing step (well-ordering alone cannot force the least counterexample to be a successor). ✓

**D-INJ proof.** Base P=1: the singleton image is enumerated by a vacuously strictly increasing length-1 function; NAT-card's value clause reads cardinality 1. Step P→P+1: the deletion-and-renumber ρ is verified injective via three sub-cases (a<b<k₀ identity branch; a<k₀≤b straddle, closed by mixed transitivity two-case split; k₀≤a<b successor branch, settled by NAT-cancel's right cancellation). ρ's surjectivity onto the punctured segment uses NAT-discrete (lower and upper bounds for each placement) and D-PRED (predecessor existence for the above-k₀ sub-case). The successor-reflection lemma (n+1 ≤ m+1 ⟹ n ≤ m) is derived inline by splitting NAT-order's ≤-definition and using NAT-cancel for the equality sub-case. The prepend construction and g's strict increase (across/beyond/spanning seam) are all fully walked. ✓

**D-CTG-depth proof.** The contradiction argument is structurally sound:
- Interior first-disagreement j extracted by NAT-wellorder from the non-empty interior-disagreement set. ✓
- Prefix agreement (all 1 ≤ i < j agree) established by the j < m derivation (NAT-addcompat + two-case split) then NAT-discrete at (i,m) for interior placement, then minimality of j. ✓
- T1 witness pinned to k = j: k < j contradicts uₖ = xₖ (from prefix agreement) against clause (i)'s uₖ < xₖ; k > j contradicts uⱼ ≠ xⱼ against the agreement clause covering i = j. ✓
- Witness w constructed via T0 comprehension with all components ∈ ℕ (NAT-closure for the constant-1 tail; T0 component projection for the u-prefix; T0(a) extracts nₖ ∈ ℕ). ✓
- zeros(w) = 0: S8a's positivity consequence gives uᵢ > 0 for prefix components; NAT-order transitivity carries 0 < uⱼ₊₁ < n to 0 < n for wⱼ₊₁; NAT-closure's 0 < 1 covers wᵢ = 1 > 0 for the suffix. Zero-filter empty → NAT-card k=0 case → zeros(w) = 0. ✓
- u < w (T1 clause (i) at k = j+1; j+1 ≤ m from interior bound) and w < x (T1 clause (i) at k = j; j < m derived from j+1 ≤ m). ✓
- D-CTG gives w ∈ V_1(d). ✓
- N+1 witnesses built by N+1 successive T0(a) instantiations (finite, determined after reading N from S8-fin); strict increase n₁ < … < n_{N+1} from iterative bound feeding. Distinct witnesses by T3 (differ at j+1). ✓
- k ↦ rₖ injective by single-valuedness of f (if rₖ = rₗ then f.rₖ = f.rₗ, so w⁽ᵏ⁾ = w⁽ˡ⁾, contradicting distinctness). ✓
- D-INJ at P := N+1, n := N gives |{rₖ}| = N+1; NAT-card upper bound gives |{rₖ}| ≤ N; N+1 ≤ N against N < N+1 (NAT-addcompat) closes by the same two-case split → N < N → irreflexivity contradiction. ✓

**Depends completeness.** Verified for all claims. D-PRED and NAT-cancel are correctly absent from D-CTG-depth's Depends (transitive through D-INJ, per the settled declined finding). NAT-induction is correctly absent from D-CTG-depth's Depends (transitive through D-INJ and D-PRED). NAT-zero is absent from D-INJ's Depends correctly (0 does not appear as a first-class constant in D-INJ's proof; it enters only transitively through NAT-card's k=0 case). All first-class constants (0, 1, 2, 3) are grounded at the claim that writes them directly.

**WLOG argument.** The interior-disagreement set {i : 2 ≤ i ∧ i+1 ≤ m ∧ uᵢ ≠ xᵢ} is symmetric in u, x; its minimum j is the same under either ordering. The witness construction anchors on the smaller element; swapping (u,x)→(x,u) produces a symmetric construction reaching the same contradiction. The WLOG is valid. ✓

---

### S8-fin formal axiom binds `j` three times within one formula
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S8-fin (FiniteArrangement) — Axiom: `f : {j ∈ ℕ : 1 ≤ j ≤ n} → dom(Σ.M(d)) ∧ (A i, j : 1 ≤ i < j ≤ n : f.i ≠ f.j) ∧ (A v : v ∈ dom(Σ.M(d)) : (E j : 1 ≤ j ≤ n : f.j = v))`
**Issue**: The variable `j` is bound in three separate contexts within the single axiom clause: the set-builder `{j ∈ ℕ : 1 ≤ j ≤ n}`, the injectivity universal `(A i, j : 1 ≤ i < j ≤ n : f.i ≠ f.j)`, and the surjectivity existential `(E j : 1 ≤ j ≤ n : f.j = v)`. Each is formally correct (locally scoped), but a reader must simultaneously track three binding occurrences of the same name. D-CTG-depth's precondition already disambiguates by using `r` throughout both the injectivity and surjectivity contexts.
**What needs resolving**: N/A — the formula is formally correct; renaming the injectivity and surjectivity bound variables to `r` (or any name distinct from the set-builder's `j`) would improve readability but does not affect soundness.

---

VERDICT: OBSERVE