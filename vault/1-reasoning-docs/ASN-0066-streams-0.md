# ASN-0066: Streams 0

*2026-03-21*

This ASN extends the two-space model (ASN-0036) with a contiguity design constraint on document arrangements. Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." We formalize these structural properties as constraints on V-position sets within each subspace, extending the arrangement invariants established in ASN-0036.


## Subspace Position Sets

Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036).


## Arrangement Contiguity

**D-CTG — VContiguity (DESIGN).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction. Suppose V_S(d) contained two positions differing before the last component — say [S, 1, 5] and [S, 2, 1]. Every intermediate [S, v₂, v₃] with [S, 1, 5] < [S, v₂, v₃] < [S, 2, 1] must belong to V_S(d) by D-CTG. But these intermediates include [S, 1, 6], [S, 1, 7], ... — infinitely many positions with v₂ = 1, contradicting S8-fin. (Note: in the text subspace, the intermediate [S, 2, 0] would additionally violate S8a, but S8-fin alone suffices — the argument applies to all subspaces regardless of S8a's range guard.)

**D-CTG-depth — SharedPrefixReduction (COROLLARY; from D-CTG, S8-fin).** For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

Combining D-CTG-depth with D-MIN and S8-fin, we obtain the general form:

**D-SEQ — SequentialPositions (COROLLARY; from D-CTG, D-MIN, S8-fin, S8-depth).** For each document d and subspace S, if V_S(d) is non-empty then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m (the common V-position depth in subspace S). At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (ASN-0036 introduces the arrangement as a partial function; no content has been allocated, so no V-mapping exists), so V_S(d) = ∅ for every subspace S. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_S(d) non-empty). Observe that not all arrangement modifications preserve D-CTG: removing a single interior V-position from dom(M(d)) leaves the positions on either side no longer contiguous. D-CTG is therefore preserved only by those modifications that constitute well-formed editing operations — operations that restore contiguity after structural changes (e.g., by shifting subsequent positions).

Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN.


## Starting Position

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

**D-MIN — VMinimumPosition (DESIGN).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth, ASN-0036), and every component after the first is 1.

At depth 2 this gives min(V_S(d)) = [S, 1]. Combined with D-CTG and S8-fin, a document with n elements in subspace S occupies V-positions [S, 1] through [S, n] — matching Nelson's "addresses 1 through 100."


## Concrete Example

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


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| D-CTG | DESIGN | V-positions within each subspace form a contiguous ordinal range — design constraint on well-formed document states | introduced |
| D-MIN | DESIGN | The minimum V-position in each non-empty subspace has all post-subspace components equal to 1 | introduced |
| D-CTG-depth | COROLLARY | At depth m ≥ 3, all positions in non-empty V_S(d) share components 2 through m − 1; contiguity reduces to the last component (from D-CTG, S8-fin) | introduced |
| D-SEQ | COROLLARY | Non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 (from D-CTG, D-MIN, S8-fin, S8-depth) | introduced |


## Open Questions

Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?
