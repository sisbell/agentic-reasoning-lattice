**D-MIN-VAL (MinimumPositionValue).** For each document d and subspace S with V_S(d) non-empty:

`min_S(d) = [S, 1, …, 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

*Proof.* By AX-6 (MinimumPresence), [S, 1, …, 1] ∈ V_S(d). We show it is the least element under T1, whence it equals min_S(d) (D-MIN).

Let p ∈ V_S(d) with p ≠ [S, 1, …, 1]. Both p and [S, 1, …, 1] have depth m (S8-depth) and belong to T (dom(Σ.M(d)) ⊆ T by Σ.M(d)). Equal depth with inequality gives, by the contrapositive of T3 (CanonicalRepresentation, ASN-0034), a least index j at which they disagree. The first component is the subspace identifier S in both, so j > 1. At component j, [S, 1, …, 1] has value 1; the position p, having a strictly positive natural at every post-subspace component (S8a) distinct from 1 at position j, has value strictly greater than 1. By T1(i) (TumblerOrdering, ASN-0034), [S, 1, …, 1] < p.

Since [S, 1, …, 1] ∈ V_S(d) and [S, 1, …, 1] ≤ p for every p ∈ V_S(d), the element [S, 1, …, 1] is the unique minimum of V_S(d) under T1. By D-MIN, min_S(d) = min(V_S(d)), so min_S(d) = [S, 1, …, 1]. ∎

At depth 2 this gives min_S(d) = [S, 1]. The full characterization of V_S(d) as a contiguous range — that a document with n elements in subspace S occupies V-positions [S, 1] through [S, n], matching Nelson's "addresses 1 through 100" — follows from D-SEQ, which combines D-MIN-VAL with D-CTG and S8-fin.

D-MIN-VAL, together with contiguity (D-CTG) and finiteness (S8-fin), motivates a sequential structure: positions within a subspace differ only at the last component and form a contiguous range starting at 1. D-SEQ formalizes this derivation by case analysis on the common depth m.

*Formal Contract:*
- *Theorem:* `min_S(d) = [S, 1, …, 1]` — for any non-empty subspace, the minimum V-position (D-MIN) equals the depth-m tuple with subspace identifier S and every subsequent component equal to 1.
- *Preconditions:* V_S(d) ≠ ∅; `[S, 1, …, 1] ∈ V_S(d)` (AX-6, MinimumPresence); `V_S(d) ⊆ dom(Σ.M(d)) ⊆ T` (V_S(d), Σ.M(d)); all positions in V_S(d) share depth m (S8-depth) with m ≥ 2 (S8-vdepth); S8a gives zeros(v) = 0 for all V-positions, so every component ≥ 1; T3 (CanonicalRepresentation, ASN-0034) provides component-level disagreement from tumbler inequality at equal depth.
- *Postconditions:* `min_S(d) = [S, 1, …, 1]`. For any p ∈ V_S(d) with p ≠ [S, 1, …, 1], T3 and S8-depth give a least disagreeing component j > 1; S8a forces pⱼ > 1 since [S, 1, …, 1]ⱼ = 1 and they disagree; T1(i) gives [S, 1, …, 1] < p. AX-6 provides [S, 1, …, 1] ∈ V_S(d), and D-MIN identifies it as min_S(d). ∎
