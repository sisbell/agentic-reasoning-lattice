**D-MIN (VMinimumPosition).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

D-MIN is a design requirement on valid arrangements. V-position components are strictly positive natural numbers (S8a), so 1 is the smallest value any component can take. The position [S, 1, …, 1] is therefore the least element of subspace S under lexicographic order (T1): any other position in subspace S shares the first component S but must differ at some subsequent component; at the first such component j, [S, 1, …, 1] has value 1 and the other position, having a positive natural (S8a) distinct from 1, has value strictly greater than 1 — making it strictly larger by T1(i). D-MIN requires that this least position is always present when the subspace is non-empty — every operation that populates or modifies V_S(d) must include [S, 1, …, 1] in the resulting set.

At depth 2 this gives min(V_S(d)) = [S, 1]. The full characterization of V_S(d) as a contiguous range — that a document with n elements in subspace S occupies V-positions [S, 1] through [S, n], matching Nelson's "addresses 1 through 100" — follows from D-SEQ, which combines D-MIN with D-CTG and S8-fin.

D-MIN's axiom, together with contiguity (D-CTG) and finiteness (S8-fin), motivates a sequential structure: positions within a subspace should differ only at the last component and form a contiguous range starting at 1. D-SEQ formalizes this derivation by case analysis on the common depth m.

*Formal Contract:*
- *Axiom:* `min(V_S(d)) = [S, 1, ..., 1]` — for any non-empty subspace, the minimum V-position is the depth-m tuple with subspace identifier S and every subsequent component equal to 1. This is a design requirement: operations that modify V_S(d) must preserve this minimum.
- *Preconditions:* `V_S(d) ⊆ dom(Σ.M(d))` (V_S(d), SubspaceVPositionSet), `dom(Σ.M(d)) ⊆ T` (Σ.M(d)), so the lexicographic order `<` (T1, ASN-0034) is well-defined on V-positions; V_S(d) ≠ ∅; all positions in V_S(d) share depth m (S8-depth); S8-vdepth gives m ≥ 2; S8a (V-position well-formedness) gives zeros(v) = 0 for all V-positions, so every component ≥ 1.
- *Postconditions:* `min(V_S(d)) = [S, 1, ..., 1]` is the least element of V_S(d) under the lexicographic order (T1, ASN-0034). Since every V-position component is at least 1 (S8a) and the tuple [S, 1, …, 1] has the minimum possible value at every post-subspace component, no element of V_S(d) can precede it.
