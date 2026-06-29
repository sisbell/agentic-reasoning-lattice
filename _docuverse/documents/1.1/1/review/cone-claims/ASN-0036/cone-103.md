## Review

### Dependency and Symbol Grounding

**NAT-induction**: Correctly posited as a foundation axiom augmenting the NAT-* group. Depends on NAT-carrier (for ℕ), NAT-zero (for `0 ∈ ℕ`), and NAT-closure (for `k+1 ∈ ℕ` and the successor map). The gap it fills — that the order-and-addition axioms are not categorical and do not entail generation-from-0 — is correctly stated as a known metamathematical fact. No exhibiting of a separating model is needed, and none is attempted.

**D-PRED**: The induction set `H = {n ∈ ℕ : n = 0 ∨ (E i ∈ ℕ :: i+1 = n)}` contains 0 (left disjunct), is closed under successor (k+1 witnesses the right disjunct with i=k, k+1 ∈ ℕ by NAT-closure), so NAT-induction gives H = ℕ. For j ≥ 1 the zero alternative is excluded: `0 < 0+1 = 1` (NAT-addcompat at n=0, NAT-closure left identity), chained with `1 ≤ j` via the two-case split on NAT-order's ≤-definition (pure <-transitivity when 1 < j, indiscernibility of = when 1 = j) gives `0 < j`, whence `j ≠ 0` by irreflexivity. The Depends list correctly excludes NAT-wellorder as the induction engine and correctly includes NAT-induction. The claim exports existence alone, matching D-INJ's consumption.

### D-INJ Proof

Base case (P=1): The singleton image `{h.1}` is enumerated by the map with f.1=h.1, strictly increasing vacuously. NAT-card's value clause at q=1 reads `|{h.1}|=1`. Sound.

Inductive step: NAT-wellorder extracts μ = min S (S non-empty since h.1 ∈ S). Uniqueness of k₀ via injectivity of h (h.a = h.b with a ≠ b gives a symmetric contradiction to injectivity). The renumbering ρ's three injectivity cases are correctly handled: identity branch (a < b directly), straddle branch (chain a < k₀ ≤ b < b+1 via two-case ≤-split and NAT-addcompat), successor branch (NAT-cancel right cancellation at summand 1). Surjectivity of ρ onto the punctured segment: the below-k₀ sub-case uses NAT-discrete at (j, P+1) and successor reflection (itself derived via NAT-order's ≤-definition, NAT-cancel for the equality sub-case, NAT-addcompat + NAT-order irreflexivity for the strict sub-case); the above-k₀ sub-case draws the predecessor from D-PRED and bounds it via NAT-discrete + successor reflection. The composite h' is injective (standard composition argument), its image is S' = S \ {μ}, and the IH gives |S'| = P. Prepending μ to S''s strictly increasing enumeration g' builds a strictly increasing length-(P+1) enumeration g of S: the seam step (μ < g'.1 by ≤-minimality of μ in S together with μ ∉ S' forcing the strict inequality via trichotomy) and the spanning step (two-case split on NAT-order's ≤-definition closing μ < g'.1 ≤ g'.r) are both correctly discharged. NAT-card's value clause at q=P+1 yields |S|=P+1.

The closing remark on the P > n regime (not assumed by the proof; NAT-card's upper bound then forces P ≤ n) is correctly stated and connects cleanly to D-CTG-depth's usage at P=N+1, n=N.

### D-CTG-depth Proof

**Setup and ordering**: T3's reverse direction gives u ≠ x from the interior disagreement, so T1's trichotomy reduces to u < x or x < u. The relabeling argument is sound: the interior disagreement set is symmetric in u and x, and the witness construction is anchored on the smaller member, so x < u collapses onto u < x by swap.

**First disagreement j**: NAT-wellorder applied to the non-empty set {i : 2 ≤ i ∧ i+1 ≤ m ∧ uᵢ ≠ xᵢ} ⊆ ℕ yields j. Agreement for i < j: at i=1, u₁=x₁=1 (shared subspace); at 2 ≤ i < j, the chain j+1 ≤ m → (NAT-addcompat) j < j+1 → (two-case ≤-split) j < m → (pure <-transitivity) i < m → (NAT-discrete at (i,m)) i+1 ≤ m places i in the interior range, and minimality of j forces uᵢ = xᵢ.

**Pinning k=j**: Clause (ii) of T1 is impossible (m+1 ≤ m contradicts NAT-addcompat's m < m+1 by trichotomy). So clause (i) holds. k < j: at k=1 the shared subspace value gives u₁=x₁ against clause (i); at k ≥ 2, NAT-discrete at (k,m) places k in the interior range, minimality forces uₖ=xₖ, against clause (i). k > j: T1's agreement clause at i=j gives uⱼ=xⱼ, against the disagreement. Hence k=j and uⱼ < xⱼ.

**Witness construction**: w of depth m with wᵢ=uᵢ for i ≤ j, wⱼ₊₁=n (any n > uⱼ₊₁), wᵢ=1 for i ≥ j+2 (empty when j+1=m). All components in ℕ; T0's comprehension gives w ∈ T. u < w: T1(i) at position j+1 (agreement on i ≤ j; uⱼ₊₁ < n; j+1 ≤ m). w < x: T1(i) at position j (agreement on i < j since wᵢ=uᵢ=xᵢ there; wⱼ=uⱼ < xⱼ; j < m from interior bound via NAT-addcompat + two-case ≤-split).

**Zero-freeness**: S8a's positivity Consequence gives uᵢ > 0 for i ≤ j; NAT-order transitivity at (0, uⱼ₊₁, n) gives wⱼ₊₁ = n > 0; NAT-closure's Consequence 0 < 1 gives wᵢ = 1 > 0 for i ≥ j+2. Positivity implies non-zero (if wᵢ=0 and wᵢ>0 then 0<0 by irreflexivity contradiction). NAT-card's empty-set characterization yields zeros(w)=0.

**Finiteness contradiction**: S8-fin furnishes N ∈ ℕ and a bijection f : {r : 1 ≤ r ≤ N} → dom(M(d)). T0(a) applied N+1 times (each feeding the previous output as the next bound, a finite iteration) produces n₁ < n₂ < … < nₙ₊₁, all > uⱼ₊₁. Each w⁽ᵏ⁾ is distinct (T3 on differing j+1 components) and in V₁(d) (D-CTG applied N+1 times at the same u, x). Surjectivity of f gives rₖ for each w⁽ᵏ⁾; single-valuedness of f makes k ↦ rₖ injective. D-INJ at P=N+1, n=N gives |{rₖ}|=N+1; NAT-card's upper bound gives |{rₖ}|≤N. So N+1≤N, against N < N+1 (NAT-addcompat) via the two-case ≤-split and irreflexivity. Contradiction closes the proof.

**Shared-prefix postcondition**: No interior disagreement exists, so all positions in V₁(d) agree on components 2 through m-1. Combined with the shared subspace value at component 1, all positions agree on the full prefix (components 1 through m-1) and vary only at component m. The scope restriction m ≥ 3 is correctly stated as a precondition, with m=2 deferred to D-SEQ.

### Posit Consistency

S8a, D-CTG, S8-depth, and S8-fin are all correctly identified as protocol design posits, clearly distinguished from derived claims. Their Depends lists are grounded to the symbols they name. The cross-posit relationships (S8a and S8-depth as parallel, independent constraints on the same domain) are correctly described without false topological ordering.

### Declined Findings Verification

D-CTG-depth's Depends does not contain D-PRED or NAT-cancel. The NAT-discrete entry describes D-CTG-depth's direct use (instantiation at (i,m) for interior-range placement) without reference to ρ or k₀. The declined findings are fully resolved in the current artifact.

VERDICT: CONVERGED