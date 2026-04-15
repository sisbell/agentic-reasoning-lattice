**D-CTG (VContiguity).** For each d ∈ D and subspace S, V_S(d) is either empty or contains every intermediate of the same depth between its extremes:

`(A d ∈ D, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v ∈ T : v₁ = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions admit no gaps among tumblers of the same depth. The guard `v₁ = S` is first-component extraction, equivalent to `subspace(v) = S` by SubspaceIdentifier — since T0 (CarrierSetDefinition, ASN-0034) guarantees `#v ≥ 1` for every `v ∈ T`, SubspaceIdentifier's preconditions are satisfied throughout T, and the component notation `v₁` is used here as a direct synonym. If positions [1, 3] and [1, 7] are occupied and 3 < k < 7, then [1, k] must also be occupied. This quantification over v ∈ T is no restriction. Every same-depth same-subspace intermediate is a finite sequence of naturals with length ≥ 1, hence a member of T by T0 (CarrierSetDefinition, ASN-0034). At depth m = 2, OrdinalShift (ASN-0034) provides a constructive witness: shift(u, n) ∈ T with #shift(u, n) = #u, advancing the last component by n while preserving the subspace identifier. At depth m ≥ 3, shift preserves all non-last components, so not every intermediate is shift-reachable without the shared-prefix result established below by D-CTG-depth (SharedPrefixReduction).

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are those [S, i] ∈ T with a < i < b. Combined with S8-fin (dom(Σ.M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a contiguous block of ordinals at that depth.

At depth m ≥ 3, D-CTG combined with S8-fin and S8-depth forces a stronger restriction: all positions in V_S(d) must share components 2 through m − 1. This is a derived consequence — not part of the contiguity invariant itself — and D-CTG-depth (SharedPrefixReduction) establishes that result.

We establish the invariant by induction over the operation history.

*Base case.* By AX-1 (InitialEmptyState), `dom(Σ₀.M(d)) = ∅` for every document `d`, so `V_S(d) = ∅` for every subspace `S`. The universal quantification holds vacuously — the empty set contains no pair of positions between which a gap could exist.

*Inductive step.* Suppose contiguity holds in state Σ: within each subspace, V-positions form a gapless range. Let Σ → Σ' be any state transition; by AX-5 (ClosedWorldTransition), some op ∈ Op produces Σ' from Σ. Each such operation must ensure that no gap appears within any subspace — neither by introducing a position beyond the current extremes without filling the interval, nor by removing an interior position without collapsing the surrounding range. Therefore `V_S(d)` in Σ' remains contiguous.

Every operation specification must individually discharge the obligation that it maps a contiguous arrangement to a contiguous arrangement. The base case and the closure argument above reduce that global invariant to a per-operation verification condition. ∎

*Formal Contract:*
- *Preconditions:* `V_S(d) ⊆ dom(Σ.M(d))` (V_S(d), SubspaceVPositionSet), `dom(Σ.M(d)) ⊆ T` (Σ.M(d)), so the lexicographic order `<` (T1, ASN-0034) is well-defined on V-positions.
- *Invariant:* `(A d ∈ D, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v ∈ T : v₁ = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))` — within each subspace, every tumbler of the same depth lying between two V-positions belongs to V_S(d), for every reachable state Σ. The guard `v₁ = S` is first-component extraction (equivalent to `subspace(v)` on all of T by SubspaceIdentifier, since T0 guarantees `#v ≥ 1`). The v ∈ T guard is operationally universal for same-depth same-subspace tuples (OrdinalShift; T0, ASN-0034).
