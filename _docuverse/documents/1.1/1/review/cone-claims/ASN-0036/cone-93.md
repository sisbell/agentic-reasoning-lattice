Reading the proofs in full before flagging anything.

The NAT-* stratum is ground truth. D-CTG, S8-fin, S8a, S8-depth, subspace, V-sub, and Σ.M(d) are posits stated cleanly — their formal contracts are tight and their Depends lists are accurate. The overall contradiction structure of D-CTG-depth (disagreement at interior j → infinitely many intermediates via D-CTG + T0(a) → finiteness via S8-fin + D-INJ + NAT-card → N+1 ≤ N → irreflexivity) is logically valid. The induction in D-INJ is sound.

Two Depends omissions survive careful verification. Both involve NAT-discrete (NatDiscreteness, ASN-0034; forward direction m < n ⟹ m+1 ≤ n), which T1 and T4 both cite explicitly for this exact direction.

---

### D-INJ: surjectivity of ρ uses NAT-discrete, which is absent from Depends

**Class**: REVISE
**Foundation**: NAT-discrete (NatDiscreteness, ASN-0034) — forward direction `m < n ⟹ m + 1 ≤ n`
**ASN**: D-INJ (InjectiveImageCardinality), proof body: *"Surjectivity onto the punctured segment: every index below k₀ is hit by itself…"*; Formal Contract Depends list: `NAT-card, NAT-wellorder, NAT-order, NAT-closure, NAT-addcompat, NAT-cancel` (NAT-discrete absent).
**Issue**: The surjectivity claim asserts: for every j ∈ {k : 1 ≤ k ≤ P+1} \ {k₀} with j < k₀, ρ.j = j (j hits itself). For this, j must lie in ρ's domain {k : 1 ≤ k ≤ P}, requiring j ≤ P. From j < k₀ ≤ P+1 and transitivity of `<`, we have j < P+1. Descending from j < P+1 to j ≤ P requires NAT-discrete at (m,n) = (j, P+1): `j < P+1 ⟹ j+1 ≤ P+1`, then right cancellation at 1 (NAT-cancel, already listed) gives j ≤ P. Without this step the surjectivity sub-case "j < k₀ is hit by itself" is ungrounded, the bijection claim for ρ fails, and the derivation `Image(h') = {h.k : 1 ≤ k ≤ P+1 ∧ k ≠ k₀} = S \ {μ}` cannot be completed — which is the hinge the IH application and the prepend-μ construction turn on. NAT-discrete is not listed in D-INJ's Depends even though T1 and T4 cite it explicitly for this forward direction.
**What needs resolving**: Add NAT-discrete (NatDiscreteness, ASN-0034) to D-INJ's Depends, citing its forward direction `m < n ⟹ m+1 ≤ n` as used to pass from `j < P+1` to `j+1 ≤ P+1` in the `j < k₀` surjectivity sub-case.

---

### D-CTG-depth: k = j pinning uses NAT-discrete, which is absent from Depends

**Class**: REVISE
**Foundation**: NAT-discrete (NatDiscreteness, ASN-0034) — forward direction `m < n ⟹ m + 1 ≤ n`
**ASN**: D-CTG-depth (SharedPrefixReduction), proof body: *"Were k < j, then k satisfies 1 ≤ k < j, where we have already established agreement, giving uₖ = xₖ and contradicting uₖ < xₖ"*; Formal Contract Depends list does not include NAT-discrete.
**Issue**: The k = j pinning handles two cases. The k > j case is clean (T1's own agreement clause at i = j gives uⱼ = xⱼ, contradicting j's membership in the interior disagreement set). The k < j case splits on k = 1 (also clean: u₁ < x₁ contradicts u₁ = x₁ = 1) and k ≥ 2. For k ≥ 2 and k < j, the argument is that k is itself an interior disagreement point — T1 gives uₖ < xₖ, so uₖ ≠ xₖ, and k ≥ 2, so k would be in {i : 2 ≤ i ∧ i+1 ≤ m ∧ uᵢ ≠ xᵢ}, contradicting j's minimality. But placing k in that set requires k+1 ≤ m. The available chain is: k < j (given) and j < m (derived from j < j+1 by NAT-addcompat and j+1 ≤ m by j's membership in the interior range, chained by NAT-order transitivity), so k < m by transitivity. Then k < m ⟹ k+1 ≤ m is exactly NAT-discrete's forward direction. Without this step the sub-case k ≥ 2, k < j is ungrounded: k fails to be placed in the interior range and the minimality of j cannot be invoked, leaving the k = j pinning incomplete. This pinning is necessary to conclude uⱼ < xⱼ, which drives the entire subsequent witness construction. NAT-discrete is not in D-CTG-depth's Depends.
**What needs resolving**: Add NAT-discrete (NatDiscreteness, ASN-0034) to D-CTG-depth's Depends, citing its forward direction `m < n ⟹ m+1 ≤ n` as used at (m,n) = (k,m) in the `k ≥ 2, k < j` sub-case of the k = j pinning.

---

VERDICT: REVISE