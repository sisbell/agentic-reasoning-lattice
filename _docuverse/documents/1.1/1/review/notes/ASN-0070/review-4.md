# Review of ASN-0070

## REVISE

### Issue 1: F-canonical Step 1, case k = 1 — wrong exclusion reason

**ASN-0070, F-canonical Step 1 (Case k = 1)**: "The reach has first component greater than S, so the lex interval [s, s ⊕ ℓ) includes tumblers of subspace S, S+1, ..., (s ⊕ ℓ)_1. The component crosses subspaces, violating the per-subspace structure of R(d, e)|_S."

**Problem**: The V-restricted denotation `⟦σ⟧_V` filters to subspace S at depth m_S(d) by definition, so cross-subspace tumblers in `⟦σ⟧` are excluded by V-restriction — "crosses subspaces" does not exclude this case. Moreover, when ℓ_1 = 1, the full denotation does not even cross subspaces ((s ⊕ ℓ)_1 = S + 1, so the half-open interval's first component is just S), so the premise fails entirely.

The actual exclusion reason is the same as case 2 ≤ k < m_S(d): ⟦σ⟧_V is infinite. For k = 1 with any ℓ_1 ≥ 1, any depth-m tumbler t = [S, s_2, …, s_{m-1}, s_m + n] for n ≥ 0 satisfies t < s ⊕ ℓ (divergence at position 1, t_1 = S < S + ℓ_1) and t ≥ s — giving infinitely many qualifying tumblers, contradicting R(d, e)|_S ⊆ dom(M(d)) finite (S8-fin).

**Required**: Unify the exclusion argument across all k < m_S(d) using the finiteness criterion; drop the "crosses subspaces" reasoning, which does not establish the conclusion under V-restriction and fails outright when ℓ_1 = 1.

### Issue 2: F-canonical Step 1, case 2 ≤ k < m_S(d) — construction wording inconsistent

**ASN-0070, F-canonical Step 1 (Case 2 ≤ k < m_S(d))**: "Consider depth-m_S(d) tumblers t with t_i = s_i for i < k, t_k = s_k, and t_j arbitrary for j > k subject to t_m ≥ s_m."

**Problem**: As stated, "t_j arbitrary for j > k" with only "t_m ≥ s_m" as constraint does not guarantee t ≥ s — if t_{k+1} < s_{k+1}, then t < s by T1 case (i). The next sentence implicitly tightens the construction ("when positions k+1, …, m-1 tie with s"), but this constraint is not part of the construction itself. The subsequent claim "The tail t_{k+1}, …, t_m ranges over ℕ unbounded" then misrepresents the actual construction, in which only t_m varies (since k+1 to m-1 are tied to s).

**Required**: State the construction unambiguously, e.g., "Consider depth-m_S(d) tumblers t with t_i = s_i for 1 ≤ i ≤ m-1 and t_m ∈ {s_m, s_m + 1, s_m + 2, …}." Then conclude infinite cardinality directly from t_m ranging over ℕ_{≥ s_m}.

### Issue 3: F-canonical Step 2 — "maximal contiguous runs" undefined; unique decomposition not derived

**ASN-0070, F-canonical Step 2**: "Hence ⟦Σ̂⟧_V decomposes uniquely into maximal contiguous runs of depth-m_S(d) subspace-S tumblers, and each run reconstructs one (s_j, c_j) pair."

**Problem**: The uniqueness of the canonical form turns on this step, but "maximal contiguous runs" is asserted without definition and the decomposition's uniqueness is asserted without derivation. The reader must reconstruct the argument:

- Define "consecutive" for depth-m subspace-S tumblers: t, t' consecutive iff no depth-m subspace-S t'' satisfies t < t'' < t' in T1 (this corresponds to shared prefix and last components differing by 1).
- Within a single ⟦σ_j⟧_V = {[s_j(1..m-1), s_j(m) + i] : 0 ≤ i < c_j}, all elements are pairwise consecutive (in the above sense).
- Between ⟦σ_j⟧_V and ⟦σ_{j+1}⟧_V, the tumbler reach(σ_j) = [s_j(1..m-1), s_j(m) + c_j] is a depth-m subspace-S tumbler not in ⟦Σ̂⟧_V (it is the exclusive upper bound of σ_j and < start(σ_{j+1}) by N2), creating a verifiable gap.
- Hence ⟦Σ̂⟧_V partitions into maximal runs of consecutive tumblers, each run uniquely identifying one (s_j = min(run), c_j = |run|).

Without this derivation, the step where "⟦·⟧_V determines ⟦·⟧" — the bridge that lets S9 lift to V-restricted equivalence — is asserted but not established.

**Required**: Define "consecutive depth-m_S(d) subspace-S tumblers" precisely, prove internal contiguity of each ⟦σ_j⟧_V and inter-component gap (e.g., via reach(σ_j)), and conclude unique reconstruction of (s_j, c_j) from each maximal run.

VERDICT: REVISE
