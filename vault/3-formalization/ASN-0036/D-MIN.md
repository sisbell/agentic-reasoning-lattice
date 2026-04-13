**D-MIN (VMinimumPosition).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

D-MIN is a design requirement on valid arrangements. V-position components are strictly positive natural numbers (S8a), so 1 is the smallest value any component can take. The position [S, 1, …, 1] is therefore the least element of subspace S under lexicographic order (T1): any other position in subspace S shares the first component S but must differ at some subsequent component j, where [S, 1, …, 1] has value 1 and the other position, being a distinct tuple of positive naturals, has value greater than 1 at j — making it strictly larger by T1(i). D-MIN requires that this least position is always present when the subspace is non-empty — every operation that populates or modifies V_S(d) must include [S, 1, …, 1] in the resulting set.

At depth 2 this gives min(V_S(d)) = [S, 1]. D-SEQ derives the full sequential characterization — V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} — by combining D-MIN with D-CTG, S8-fin, and S8-vdepth.

*Formal Contract:*
- *Axiom:* `min(V_S(d)) = [S, 1, ..., 1]` — for any non-empty subspace, the minimum V-position is the depth-m tuple with subspace identifier S and every subsequent component equal to 1. This is a design requirement: operations that modify V_S(d) must preserve this minimum.
- *Preconditions:* V_S(d) ≠ ∅; all positions in V_S(d) share depth m (S8-depth); all V-position components are strictly positive (S8a).
- *Postconditions:* [S, 1, …, 1] ∈ V_S(d) and is the least element of V_S(d) under lexicographic order (T1). The full sequential characterization of V_S(d) is derived in D-SEQ.
