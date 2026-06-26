**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m — the common depth of V-positions in the text subspace, fixed by S8-depth — and every component is 1. At depth 2 this reads min(V_1(d)) = [1, 1].

This is a *design requirement* on well-formed strand states, not a derived result. We are fixing where a document's text begins. V-positions are 1-indexed: by convention every component is counted upward from 1, so the least position the text subspace can offer is the all-ones tuple [1, 1, ..., 1]. D-MIN requires that a non-empty document actually *reaches* that floor — its text block is anchored at the origin of its subspace. We call this the *left-anchoring* invariant and impose it on every reachable state.

**Non-derivability from the other constraints.** D-MIN is logically independent of contiguity (D-CTG), positivity and depth (S8a), and finiteness (S8-fin) — none of them entails left-anchoring, so D-MIN cannot be a theorem over them. A depth-2 witness:

`V_1(d) = {[1, 5], [1, 6], [1, 7]}.`

It is contiguous in the sense D-CTG demands — the only position strictly between its extremes [1, 5] and [1, 7] is [1, 6], which is present, so there is no internal gap — every component is strictly positive at the common depth 2 (S8a, S8-depth), and the set is finite (S8-fin); yet

`min({[1, 5], [1, 6], [1, 7]}) = [1, 5] ≠ [1, 1].`

A contiguous, positive, finite, fixed-depth block can thus float above the origin — exactly what D-MIN rules out.

**The base state and downstream use.** Before any operation, dom(Σ.M(d)) = ∅ for every d, so V_1(d) = ∅ and the requirement is vacuous: its guard (V_1(d) non-empty) is unmet. The first transition that populates a document's text subspace must place its initial position at [1, 1, ..., 1], and from then on min(V_1(d)) is pinned to the all-ones tuple. The downstream claims consume D-MIN in exactly this posited form: D-SEQ reads min(V_1(d)) = [1, ..., 1] to fix the shared prefix and the least last-component value, and ValidInsertionPosition / ValidFirstInsertionPosition build their satisfying positions outward from it.

*Formal Contract:*

- *Design Requirement:* For each document d with V_1(d) ≠ ∅, min(V_1(d)) = [1, 1, ..., 1] — the length-m tuple (m the common V-position depth fixed by S8-depth) with every component 1; at depth 2, min(V_1(d)) = [1, 1]. This is posited as an invariant of every well-formed strand state (the left-anchoring of a document's text at its subspace origin); it is *not* entailed by D-CTG, S8a, and S8-fin, witnessed by the contiguous, positive, finite, depth-2 set {[1, 5], [1, 6], [1, 7]}, whose minimum is [1, 5] ≠ [1, 1].
- *Definition:* min(S) denotes the least element of S under T1's strict total order `<` on tumblers (LexicographicOrder, ASN-0034), which restricted to the fixed depth m is exactly lexicographic order on integer m-tuples. We apply min only to S = V_1(d), and V_1(d) ⊆ dom(Σ.M(d)) is finite by S8-fin. A strict total order has a unique least element on every finite non-empty set — fold the binary minimum (well-defined by T1's totality, order-independent by T1's transitivity) across the finitely many elements — so min(V_1(d)) exists and is unique whenever V_1(d) ≠ ∅. We need no well-ordering of the infinite position space, only the finiteness of the single set to which min is applied.

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common depth m shared by all V-positions in the text subspace, so that the all-ones tuple [1, 1, ..., 1] in the statement has a definite length
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict total order `<` on tumblers whose restriction to the fixed-depth m-tuples is the lexicographic total order under which `min(V_1(d))` is the least element
  - S8-fin (FiniteArrangement) — supplies the finiteness of dom(Σ.M(d)); since V_1(d) ⊆ dom(Σ.M(d)), this makes V_1(d) finite, which is what guarantees min(V_1(d)) exists (a finite non-empty totally ordered set has a least element), replacing any appeal to a well-ordering of the infinite position space
