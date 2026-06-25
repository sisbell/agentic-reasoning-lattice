**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m — the common depth of V-positions in the text subspace, fixed by S8-depth — and every component is 1. At depth 2 this reads min(V_1(d)) = [1, 1].

This is a *design requirement* on well-formed strand states, not a derived result. We are fixing where a document's text begins. V-positions are 1-indexed: by convention every component is counted upward from 1, so the least position the text subspace can offer is the all-ones tuple [1, 1, ..., 1]. D-MIN requires that a non-empty document actually *reaches* that floor — its text block is anchored at the origin of its subspace. We call this the *left-anchoring* invariant and impose it on every reachable state.

**Why this must be posited rather than proved.** It is tempting to read left-anchoring off the constraints already in hand — contiguity (D-CTG), positivity and depth (S8a), and finiteness (S8-fin) — but they do not entail it, and it is worth seeing exactly where the entailment fails. Take, at depth 2, the candidate

`V_1(d) = {[1, 5], [1, 6], [1, 7]}.`

We check it against every constraint a well-formed text subspace must meet. It is contiguous in the sense D-CTG demands: the only position strictly between its extremes [1, 5] and [1, 7] is [1, 6], and that position is present, so there is no internal gap. Every component is strictly positive and every position has depth 2, so it meets S8a; the set is finite, so it meets S8-fin; and all three positions share the common depth 2 that S8-depth requires. Yet

`min({[1, 5], [1, 6], [1, 7]}) = [1, 5] ≠ [1, 1].`

So a contiguous, positive, finite, fixed-depth block need not begin at the origin: it may float above it. Contiguity constrains the *shape* of V_1(d) — an unbroken run of last components — but is silent on *where* that run starts; positivity only bounds the floor from below; finiteness only bounds the extent. The one fact none of them supplies is that the run starts at the floor rather than hovering above it, and that fact is precisely the content of D-MIN. It is therefore logically independent of D-CTG, S8a, and S8-fin, and cannot be a theorem over them. We supply it as a design decision: documents are laid down left-anchored, beginning at [1, 1, ..., 1]. The premise that would actually force it — a "block starts at the subspace origin" invariant on how content is allocated — lives in the strand/operations layer; D-MIN is the form that invariant takes for the text subspace here.

**The base state and downstream use.** Before any operation, dom(Σ.M(d)) = ∅ for every d, so V_1(d) = ∅ and the requirement is vacuous: its guard (V_1(d) non-empty) is unmet. The first transition that populates a document's text subspace must place its initial position at [1, 1, ..., 1], and from then on min(V_1(d)) is pinned to the all-ones tuple. The downstream claims consume D-MIN in exactly this posited form: D-SEQ reads min(V_1(d)) = [1, ..., 1] to fix the shared prefix and the least last-component value, and ValidInsertionPosition / ValidFirstInsertionPosition build their satisfying positions outward from it.

*Formal Contract:*

- *Design Requirement:* For each document d with V_1(d) ≠ ∅, min(V_1(d)) = [1, 1, ..., 1] — the length-m tuple (m the common V-position depth fixed by S8-depth) with every component 1; at depth 2, min(V_1(d)) = [1, 1]. This is posited as an invariant of every well-formed strand state (the left-anchoring of a document's text at its subspace origin); it is *not* entailed by D-CTG, S8a, and S8-fin, witnessed by the contiguous, positive, finite, depth-2 set {[1, 5], [1, 6], [1, 7]}, whose minimum is [1, 5] ≠ [1, 1].
- *Definition:* min(S) denotes the least element of S under the lexicographic total order on integer m-tuples; since V-positions are 1-indexed (every component ≥ 1), this order well-orders the position space, so min(S) exists for every non-empty S.

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common depth m shared by all V-positions in the text subspace, so that the all-ones tuple [1, 1, ..., 1] in the statement has a definite length
