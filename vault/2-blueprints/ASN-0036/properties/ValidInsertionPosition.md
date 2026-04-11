### Concrete example

Consider document d at depth 2 in the text subspace (S = 1), with arrangement:

M(d) = {[1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃}

Then V₁(d) = {[1,1], [1,2], [1,3]}.

**D-CTG check.** The extremes are [1,1] and [1,3]. The only intermediate with subspace 1 and depth 2 between them is [1,2], which is in V₁(d). For the adjacent pairs — ([1,1],[1,2]) and ([1,2],[1,3]) — there are no intermediates. D-CTG is satisfied. ✓

**D-MIN check.** min(V₁(d)) = [1,1], whose last component is 1. ✓

**Violation.** Suppose we removed [1,2], yielding V₁(d) = {[1,1], [1,3]}. Now [1,2] is an intermediate between [1,1] and [1,3] that is absent from V₁(d) — D-CTG is violated. This illustrates why removing a single interior V-position is not a well-formed editing operation on its own; a well-formed deletion must also shift subsequent positions to restore contiguity.

Now consider depth 3. Let document d' have arrangement:

M(d') = {[1,1,1] ↦ a₁,  [1,1,2] ↦ a₂,  [1,1,3] ↦ a₃}

Then V₁(d') = {[1,1,1], [1,1,2], [1,1,3]}.

**D-CTG check.** The extremes are [1,1,1] and [1,1,3]. The only intermediate at subspace 1 and depth 3 between them is [1,1,2], which is in V₁(d'). ✓

**D-MIN check.** min(V₁(d')) = [1,1,1] = [S, 1, 1], with all post-subspace components equal to 1. ✓

**Violation (depth ≥ 3).** Suppose instead V₁(d') = {[1,1,1], [1,2,1]}. D-CTG requires every intermediate with subspace 1 and depth 3 between [1,1,1] and [1,2,1] to be present. But [1,1,2], [1,1,3], [1,1,4], ... are all intermediates — infinitely many, contradicting S8-fin. This is D-CTG-depth in action: positions differing before the last component cannot coexist in a finite arrangement.

## Valid insertion position

We work with the arrangement M(d) and the contiguity constraint D-CTG from above. Write V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the V-positions in subspace S of document d.

When V_S(d) is contiguous with |V_S(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ).

**Definition (ValidInsertionPosition).** A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions in the subspace.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, there is one valid position per choice of depth m — but since m is chosen once and then held fixed by S8-depth, exactly one position is valid for any given depth.

We verify the structural claims. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift and TumblerAdd, shift([S, 1, ..., 1], j) = [S, 1, ..., 1] ⊕ δ(j, m); since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j. The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j].

*Distinctness.* The N + 1 positions have last components 1 (for j = 0, where v = min(V_S(d))), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the N + 1 tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift (ASN-0034). For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction. All valid positions have the common V-position depth required by S8-depth.

*Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

*S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0 — satisfying S8a.
