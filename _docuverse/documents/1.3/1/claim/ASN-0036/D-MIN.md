**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in the text subspace per S8-depth), and every component is 1.

At depth 2 this gives min(V_1(d)) = [1, 1].

We now derive the general form: the contiguity, minimum, and finiteness constraints together force V_1(d) into a single block of last-component values. The proof below establishes this in four steps.

**Step 1 — a minimum exists.** V_1(d) is non-empty by hypothesis, and finite by the finiteness constraint on a document's V-positions. The V-positions of depth m are totally ordered by the lexicographic order on integer m-tuples, and every finite non-empty subset of a totally ordered set has a unique least element. Hence min(V_1(d)) is well-defined; write it as μ = [μ_1, μ_2, ..., μ_m]. The remaining steps identify μ.

**Step 2 — the all-ones tuple is a universal lower bound.** V-positions are 1-indexed: each component of every V-position is an integer that is at least 1, because positions are counted upward from the document origin. Consequently, for any V-position v = [v_1, ..., v_m] we have 1 ≤ v_i for every i, so at the first coordinate where [1, 1, ..., 1] and v differ (if they differ at all) the entry of [1, 1, ..., 1] is the smaller. Under lexicographic order this gives

`[1, 1, ..., 1] ≤ v   for every v ∈ V_1(d),`

i.e. [1, 1, ..., 1] lower-bounds the whole set. In particular [1, 1, ..., 1] ≤ μ.

**Step 3 — the all-ones tuple is a member of V_1(d).** By the contiguity constraint, V_1(d) is a single block with no internal gaps, and a document's text is laid down starting at the origin of its subspace. The minimum constraint of Step 2 identifies that origin: since no component can be smaller than 1, the smallest position the subspace admits is [1, 1, ..., 1], and that is where the block begins. A non-empty block contains its starting position, so

`[1, 1, ..., 1] ∈ V_1(d).`

Concretely, the block's V-positions share the all-but-last prefix of ones and differ only in their last component, which ranges over a contiguous integer interval whose least value is 1 — the "single block of last-component values" anticipated above.

**Step 4 — the member that lower-bounds the set is its minimum.** From Step 3, [1, 1, ..., 1] ∈ V_1(d); from Step 2, [1, 1, ..., 1] ≤ v for every v ∈ V_1(d). A set element that is also a lower bound of the set is, by antisymmetry of the lexicographic total order, the least element of the set. Therefore

`min(V_1(d)) = [1, 1, ..., 1],`

a tuple of length m with every component equal to 1. Specializing to depth m = 2 recovers min(V_1(d)) = [1, 1], as stated. ∎

*Formal Contract:*

- *Preconditions:* d is a document with V_1(d) non-empty and finite; the V-positions of d's text subspace share the common depth m (per S8-depth) and are ordered lexicographically; V_1(d) is contiguous — a single block whose last components fill a gap-free integer interval, anchored at the text-subspace origin.
- *Postconditions:* min(V_1(d)) = [1, 1, ..., 1], the length-m tuple with every component equal to 1; at depth 2, min(V_1(d)) = [1, 1].
- *Axiom:* V-position components are positive integers — positions are 1-indexed from the document origin by design — so [1, 1, ..., 1] is the least tuple of the depth-m position space.
- *Definition:* min(S) denotes the least element of S under the lexicographic total order on integer m-tuples.

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common depth m shared by all V-positions in a subspace, used in the statement (tuple of length m) and Step 1 (lexicographic order on integer m-tuples)