The proof of D-CTG-depth is the structural center of this ASN. I read it fully before flagging.

**D-CTG-depth: shared-prefix argument (first postcondition).** The contradiction is correctly set up: any pair u, x ∈ V_1(d) disagreeing at an interior component j (2 ≤ j ≤ m−1) admits an explicit witness w (T0 comprehension, all components ℕ-valued, depth m ≥ 1) satisfying D-CTG's full guard — subspace(w)=1 (since j≥2 puts position 1 in the copy-from-u region), #w=m=#u, zeros(w)=0 (every component ≥ 1 by S8a on u and the n > uⱼ₊₁ ≥ 1 bound), u < w < x (T1(i) at k=j+1 and k=j respectively, both ≤ m−1 < m = min(#u,#w)). D-CTG then places w ∈ V_1(d). T0(a) iterated from M₀=uⱼ₊₁ produces a strictly increasing sequence n₁ < n₂ < …, each nₖ ∈ ℕ (component of a tumbler), giving distinct wₖ by T3 (they differ at j+1). Infinitely many distinct elements in V_1(d) ⊆ dom(M(d)) contradicts S8-fin. The u < x, WLOG (by symmetry of the goal), covers the general pair. ✓

**D-CTG-depth: reduction argument (second postcondition), forward direction.** For u < v < x with v ∈ T, #v=m, subspace(v)=1, zeros(v)=0 — suppose v disagrees with u at some i ∈ {1,…,m−1}. Position 1 is excluded because v₁=1=u₁. So the nonempty set {i : 1 ≤ i ≤ m−1 ∧ vᵢ≠uᵢ} ⊆ {2,…,m−1}; NAT-wellorder supplies least element j≥2. u < v (guard) + first disagreement at j + j ≤ m−1 < m = min(#u,#v) → T1(i) → uⱼ < vⱼ. First postcondition gives xⱼ = uⱼ < vⱼ; v and x agree on 1..j−1 (same as v and u, since u and x agree on 1..m−1); T1(i) gives x < v. But v < x from the guard. T1 trichotomy: ¬(x < v ∧ v < x). Contradiction. So v shares 1..m−1 with u and x. T1(i) at k=m then collapses u < v < x to uₘ < vₘ < xₘ. Converse direction is immediate by T1(i) at k=m with the shared prefix. ✓

**OrdShiftHom.** Part (a): r₁ = v₁ (position 1 is in the copy region since m≥2), so subspace(r) = r₁ = v₁ = subspace(v). ✓ Part (b): components 1..m−1 copied from v satisfying S8a give rᵢ = vᵢ ≥ 1; action-point component rₘ = vₘ + n ≥ 1 from OrdinalShift's exported lower bound; every component ≥ 1 → zeros(r)=0; #r=m≥2 from TA0. ✓

---

### zeros(v) = 0 guard in second postcondition not consumed by the biconditional proof

**Class**: OBSERVE
**Foundation**: S8a (ArrangementDomainRestriction)
**ASN**: D-CTG-depth, second postcondition: `(A v : v ∈ T ∧ #v = m ∧ subspace(v) = 1 ∧ zeros(v) = 0 : u < v < x ≡ …)`
**Issue**: The guard `zeros(v) = 0` does not appear in the biconditional proof. The forward direction uses only `subspace(v) = 1` (to exclude i=1 from {i : 1 ≤ i ≤ m−1 ∧ vᵢ ≠ uᵢ}) and `#v = m` (for T1(i)). The converse uses only the shared prefix and T1(i) at k=m. The guard is present for D-CTG domain-compatibility (since S8a forces dom(Σ.M(d)) to hold only zero-free positions, and the second postcondition is designed to match D-CTG's application scope), but this purpose is nowhere stated. A precise reader seeing an unconsumed quantifier guard must reconstruct this motivation from context.
**What needs resolving**: Either add a one-sentence note explaining why `zeros(v) = 0` is included despite the biconditional proof not consuming it (D-CTG applicability), or remove the guard and widen the statement to all v ∈ T with #v = m and subspace(v) = 1, with a sentence noting that the result then specialises to D-CTG's guard domain when zeros(v) = 0.

---

### "Prefix conjunct cannot be dropped" asserted without witness

**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder)
**ASN**: D-CTG-depth, second postcondition closing paragraph: *"The prefix conjunct cannot be dropped: a v differing from u before component m can satisfy uₘ < vₘ < xₘ yet violate u < v < x"*
**Issue**: This meta-claim — that the conjunction is strictly necessary and not merely a proof artifact — is asserted without a concrete counterexample. The biconditional itself is fully proved, so the claim is correct. But the remark about conjunct-necessity is a separate existential claim ("there exists v with uₘ < vₘ < xₘ but not u < v < x") and is left unsupported. A precise reader cannot verify it in place.
**What needs resolving**: Exhibit one concrete counterexample, e.g. u = [1, 2, 3], x = [1, 2, 8], v = [1, 1, 5] (depth 3, subspace 1, zeros = 0): u₃ = 3 < 5 = v₃ < 8 = x₃, yet v₂ = 1 < 2 = u₂ so T1(i) at k=2 gives v < u, contradicting u < v. One sentence suffices.

VERDICT: OBSERVE