**D-CTG (VContiguity).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin and S8-depth forces a stronger restriction: all positions in V_S(d) must share components 2 through m − 1. This is a derived consequence — not part of the contiguity invariant itself — and D-CTG-depth (SharedPrefixReduction) establishes that result.

We establish the invariant by induction over the operation history.

*Base case.* By AX-1 (InitialEmptyState), `dom(Σ₀.M(d)) = ∅` for every document `d`, so `V_S(d) = ∅` for every subspace `S`. The universal quantification holds vacuously — the empty set contains no pair of positions between which a gap could exist.

*Inductive step.* Suppose contiguity holds in state Σ: within each subspace, V-positions form a gapless range. Let Σ → Σ' be any state transition; by AX-5 (ClosedWorldTransition), some op ∈ Op produces Σ' from Σ. Each such operation must ensure that no gap appears within any subspace — neither by introducing a position beyond the current extremes without filling the interval, nor by removing an interior position without collapsing the surrounding range. Therefore `V_S(d)` in Σ' remains contiguous.

Every operation specification must individually discharge the obligation that it maps a contiguous arrangement to a contiguous arrangement. The base case and the closure argument above reduce that global invariant to a per-operation verification condition. ∎

*Formal Contract:*
- *Preconditions:* `V_S(d) ⊆ dom(M(d))` (V_S(d), SubspaceVPositionSet), `dom(M(d)) ⊆ T` (Σ.M(d)), so the lexicographic order `<` (T1, ASN-0034) is well-defined on V-positions.
- *Invariant:* `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))` — within each subspace, V-positions form a contiguous range under lexicographic order.
