**D-MIN (VMinimumPosition).** For each document d and subspace S with V_S(d) non-empty, define:

`min_S(d) = min(V_S(d))`

the unique least element of V_S(d) under the lexicographic order (T1, ASN-0034).

V_S(d) is a finite non-empty subset of T: finiteness follows from S8-fin (dom(Σ.M(d)) is finite) and V_S(d) ⊆ dom(Σ.M(d)); membership in T follows from dom(Σ.M(d)) ⊆ T (Σ.M(d)). All positions in V_S(d) share depth m (S8-depth) with m ≥ 2 (S8-vdepth), so T1 provides a total order on V_S(d). A finite non-empty totally ordered set has a unique minimum, and that minimum is a member of the set. Therefore min_S(d) exists and min_S(d) ∈ V_S(d).

The value of min_S(d) is characterized by D-MIN-VAL (MinimumPositionValue): under AX-6 (MinimumPresence), min_S(d) = [S, 1, …, 1], the depth-m tuple with subspace identifier S and every subsequent component equal to 1. At depth 2 this gives min_S(d) = [S, 1].

*Formal Contract:*
- *Definition:* `min_S(d) = min(V_S(d))` — the unique least element of V_S(d) under the lexicographic order (T1, ASN-0034).
- *Preconditions:* V_S(d) ≠ ∅; `V_S(d) ⊆ dom(Σ.M(d))` (V_S(d), SubspaceVPositionSet); `dom(Σ.M(d)) ⊆ T` (Σ.M(d)); dom(Σ.M(d)) is finite (S8-fin); all positions in V_S(d) share depth m (S8-depth) with m ≥ 2 (S8-vdepth); T1 is a total order on tumblers of equal depth, hence on V_S(d).
- *Postconditions:* `min_S(d) ∈ V_S(d)`; for all `p ∈ V_S(d)`, `min_S(d) ≤ p` under T1. ∎
