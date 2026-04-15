**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_S(d) be non-empty with common depth m ≥ 3 (S8-depth). Since `V_S(d) ⊆ dom(M(d))` (V_S(d), SubspaceVPositionSet) and `dom(M(d)) ⊆ T` (Σ.M(d)), every element of `V_S(d)` belongs to `T`, so T1 applies to V-positions throughout. Suppose for contradiction that V_S(d) contains two positions v₁ and v₂ with v₁ < v₂ (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j (in particular, (v₁)₁ = S = (v₂)₁, since both belong to V_S(d)), and (v₁)ⱼ < (v₂)ⱼ (the inequality follows from v₁ < v₂ by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We produce infinitely many intermediates by applying T0(a) (UnboundedComponentValues, ASN-0034) to v₁ at position j + 1. Since v₁ ∈ T and j + 1 ≤ m (because j ≤ m − 1), position j + 1 is a valid component of v₁. For any bound M, T0(a) yields a tumbler t' ∈ T that agrees with v₁ at every position except j + 1, where t'ⱼ₊₁ > M. Each such t' satisfies:

- **subspace(t') = S**: Since j ≥ 2, position 1 is unchanged, so t'₁ = (v₁)₁ = S.
- **#t' = m**: By T0(a)'s postcondition, `#t' = #v₁ = m`.
- **t' > v₁**: t' agrees with v₁ on components 1 through j (all positions other than j + 1 are unchanged, and j < j + 1). At component j + 1, t'ⱼ₊₁ > M ≥ (v₁)ⱼ₊₁ (choosing M ≥ (v₁)ⱼ₊₁). Since j + 1 is the first disagreeing component and j + 1 ≤ m = min(m, m), by T1(i), t' > v₁.
- **t' < v₂**: t' agrees with v₂ on components 1 through j − 1 (these are copied from v₁, which agrees with v₂ through those positions by the definition of j). At component j, t'ⱼ = (v₁)ⱼ < (v₂)ⱼ. Since j ≤ m − 1 < m = min(m, m), by T1(i), t' < v₂.
- **t' ∈ T**: By T0(a)'s postcondition.

Since v₁ < t' < v₂, subspace(t') = S, and #t' = m = #v₁, D-CTG requires t' ∈ V_S(d). The set of values attainable at position j + 1 is unbounded in ℕ (T0(a) exceeds every bound M), hence infinite. Distinct values at position j + 1 yield distinct tumblers (by T3, CanonicalRepresentation, ASN-0034, they differ at component j + 1). This produces infinitely many distinct positions in V_S(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_S(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1. Write π = (S, P₂, …, P_{m−1}) for this common prefix. ∎

*Reduction.* We derive from the shared-prefix result and T1 that D-CTG contiguity of V_S(d) reduces to contiguity of the m-th component. Let v₁, v₂ ∈ V_S(d) with v₁ < v₂, and let w ∈ T satisfy subspace(w) = S, #w = m, and v₁ < w < v₂. We show w shares the prefix π. Suppose w disagrees with π at some component in [2, m − 1]; let j be the least such index. By minimality of j, wᵢ = Pᵢ = (v₁)ᵢ for all 1 ≤ i < j (the case i = 1 holds because w₁ = S = (v₁)₁). The first disagreement between w and any member of V_S(d) is therefore at position j, with j ≤ m − 1 ≤ min(m, m). If wⱼ > Pⱼ: v₂ and w agree at positions 1 through j − 1, and (v₂)ⱼ = Pⱼ < wⱼ, so by T1(i) v₂ < w — contradicting w < v₂. If wⱼ < Pⱼ: v₁ and w agree at positions 1 through j − 1, and wⱼ < Pⱼ = (v₁)ⱼ, so by T1(i) w < v₁ — contradicting v₁ < w. No such j exists, hence w agrees with π at every component in [2, m − 1].

Since every intermediate w shares the prefix π, all components 1 through m − 1 are fixed among same-depth same-subspace tumblers lying between members of V_S(d). The first point of disagreement under T1 can occur only at component m, so for same-prefix tumblers u and q of depth m, u < q iff uₘ < qₘ. The D-CTG contiguity condition — `(A v : subspace(v) = S ∧ #v = m ∧ v₁ < v < v₂ : v ∈ V_S(d))` — therefore reduces to `(A n : (v₁)ₘ < n < (v₂)ₘ : π.n ∈ V_S(d))`, which is contiguity of the m-th component over ℕ. ∎

Nelson's specification includes a second claim beyond contiguity: that ordinal numbering begins at 1, so V_S(d) occupies {prefix.1, prefix.2, …, prefix.N} rather than an arbitrary contiguous block starting at some a ≥ 1. This base-ordinal property is independent of D-CTG and is formalized separately as AX-4 (BaseOrdinal).

*Formal Contract:*
- *Preconditions:* `V_S(d) ⊆ dom(M(d))` (V_S(d), SubspaceVPositionSet), `dom(M(d)) ⊆ T` (Σ.M(d)), providing carrier-set membership for T1; V_S(d) non-empty; common depth m ≥ 3 (S8-depth); D-CTG (VContiguity); S8-fin (finite arrangement).
- *Postconditions:* (1) *Shared prefix* — `(A v₁, v₂ : v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d) : (A j : 2 ≤ j ≤ #v₁ − 1 : (v₁)ⱼ = (v₂)ⱼ))`. (2) *Last-component reduction* — writing π = (S, P₂, …, P_{m−1}) for the shared prefix: `(A v₁, v₂ : v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d) ∧ v₁ < v₂ : (A w : subspace(w) = S ∧ #w = m ∧ v₁ < w < v₂ : (A j : 2 ≤ j ≤ m − 1 : wⱼ = Pⱼ)))`. Consequently, D-CTG contiguity reduces to `(A n : (v₁)ₘ < n < (v₂)ₘ : π.n ∈ V_S(d))`.
