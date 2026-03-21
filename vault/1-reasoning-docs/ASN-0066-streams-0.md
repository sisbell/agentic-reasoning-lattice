# ASN-0066: Streams 0

*2026-03-21*

This ASN extends the two-space model (ASN-0036) with a contiguity design constraint on document arrangements. Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." We formalize this structural property as a constraint on V-position sets within each subspace, extending the arrangement invariants established in ASN-0036.


## Subspace Position Sets

Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036).


## Arrangement Contiguity

**D-CTG — VContiguity (DESIGN).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

D-CTG is a design constraint on well-formed document states, not a reachable-state invariant in the ASN-0047 sense (it does not appear in the ReachableStateInvariants theorem). It further restricts which composite transitions constitute well-formed editing operations, beyond ASN-0047's validity predicate. We verify the base case: in Σ₀, V_S(d) = ∅ for all d and S (since M₀(d) = ∅ by InitialState, ASN-0047), so D-CTG holds vacuously. Note that bare K.μ⁻ — a valid elementary transition under ASN-0047 — can violate D-CTG by removing a single interior V-position; D-CTG is therefore not preserved by all valid composites, only by those that constitute well-formed editing operations.

We treat D-CTG as a precondition that DELETE both assumes and preserves. Whether INSERT, COPY, and REARRANGE also preserve D-CTG is a separate verification obligation for each operation's ASN.


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| D-CTG | DESIGN | V-positions within each subspace form a contiguous ordinal range — design constraint assumed and preserved by well-formed editing operations | introduced |


## Open Questions

Does every well-formed editing operation (INSERT, COPY, REARRANGE) preserve D-CTG, or are there operations that legitimately produce non-contiguous V-position sets?
