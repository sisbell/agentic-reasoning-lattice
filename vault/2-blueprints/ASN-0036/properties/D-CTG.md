## Arrangement contiguity

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." We formalize these structural properties as constraints on V-position sets within each subspace, extending the arrangement invariants established above.

Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**D-CTG (VContiguity).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions in V_S(d) must share components 2 through m − 1.

*Proof.* Suppose for contradiction that V_S(d) contains two positions v₁ < v₂ (both depth m by S8-depth) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (since v₁ < v₂ by T1(i)). For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist).

Then w has subspace S (since w₁ = (v₁)₁ = S) and depth m. We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, n > (v₁)ⱼ₊₁. By T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree there). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. By T1(i), w < v₂.

By D-CTG, every such w belongs to V_S(d). By T0(a), unboundedly many values of n exist; distinct values of n produce tumblers that differ at component j + 1, hence are distinct by T3 (CanonicalRepresentation, ASN-0034) — yielding infinitely many distinct positions in V_S(d), contradicting S8-fin. ∎

This applies uniformly to all depths m ≥ 3 and all divergence points j ∈ {2, …, m − 1}. At depth m = 3, the only possible pre-last divergence is j = 2. For illustration: suppose V_S(d) contained [S, 1, 5] and [S, 2, 1]. Setting j = 2, for any n > 5, w = [S, 1, n] satisfies [S, 1, 5] < [S, 1, n] < [S, 2, 1], so D-CTG forces [S, 1, 6], [S, 1, 7], ... into V_S(d) — infinitely many, contradicting S8-fin. At depth m = 4, divergence could occur at j = 2 or j = 3; the same construction applies in each case.
