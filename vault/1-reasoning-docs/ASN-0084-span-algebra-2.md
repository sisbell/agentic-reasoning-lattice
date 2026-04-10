# ASN-0084: Span Algebra 2

*2026-04-10*

This ASN extends ASN-0053 (Span Algebra) with properties characterizing the permutation structure of cut-point transposition and its effect on block decompositions. When a contiguous range of V-positions is partitioned by cut points and two regions exchange places, the resulting bijection has a uniform displacement structure determined by region widths alone. The block decomposition — a partition into contiguous V-to-I mapping spans (ASN-0058) — transforms by splitting at cuts, classifying into regions, and reassembling with per-region displacements. These properties extend span algebra by characterizing how contiguous intervals interact under the permutation class that cut-point transposition defines.


## State and Vocabulary

We work with system state Σ = (C, E, M, R) per ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The arrangement M(d) is the mutable layer.

For a V-position v with subspace(v) = v₁ and #v = m, the *ordinal* is ord(v) = [v₂, ..., vₘ] — the tumbler obtained by stripping the subspace identifier. The reconstruction vpos(S, o) = [S, o₁, ..., oₖ] is its inverse.

We restrict to depth-2 V-positions (#v = 2, ordinal depth 1) throughout this ASN. At depth 2, D-SEQ (ASN-0036) gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, and ordinals are single natural numbers. This restriction simplifies the presentation; generalization to deeper ordinals is structurally identical by D-CTG-depth (ASN-0036), which reduces contiguity at any depth m ≥ 3 to contiguity of the last component alone.

We recall D-CTG (VContiguity, ASN-0036): within each subspace, V-positions form a contiguous ordinal range with no gaps.

In the state-transition framework of ASN-0047, arrangement reordering (K.μ~) admits a bijection π : dom(M(d)) → dom(M'(d)) such that M'(d)(π(v)) = M(d)(v) for all v ∈ dom(M(d)). The corollary is ran(M'(d)) = ran(M(d)) — the multiset of I-addresses is invariant. But K.μ~ admits *any* bijection. A rearrangement determined by cut points is a specific kind of K.μ~ — one where the regions to exchange are identified by a tuple of cut positions. The properties in this ASN characterize this specific permutation.

Notation: `c₀ + j` denotes j ordinal increments via TA5(c) (ASN-0034), and `c₀ + 0 = c₀` by the M-aux convention (ASN-0058).


## Cut Points and the Region Partition

A *cut sequence* specifies the boundaries of regions to transpose. We formalize this as a tuple of tumblers within a single subspace. The cut positions are tumblers satisfying CS1–CS4 below; the last cut c_{n−1} serves as an exclusive upper bound and need not belong to V_S(d).

**Definition — CutSequence.** A *cut sequence* for document d in subspace S is a tuple C = (c₀, c₁, ..., c_{n−1}) of tumblers satisfying:

(CS1) n ∈ {3, 4} — exactly three or four cuts.

(CS2) c₀ < c₁ < ... < c_{n−1} under T1 (ASN-0034) — strictly ordered.

(CS3) subspace(cᵢ) = S for all i — all cuts in the same subspace.

(CS4) #cᵢ = 2 for all i — depth-2 positions.

The cut positions partition the V-positions of the affected range into regions. For n = 3 (the *pivot*), the cuts define two adjacent regions. For n = 4 (the *swap*), the cuts define two outer regions separated by a middle region.

**Definition — RegionPartition.** Given a cut sequence C for document d in subspace S with V_S(d) ≠ ∅:

For n = 3, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₂} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
β = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — second region
```

For n = 4, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₃} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
μ = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — middle region
β = {v ∈ V_S(d) : c₂ ≤ v < c₃}     — second region
```

Pairwise disjointness follows from the strict ordering of cut points and the trichotomy of T1. Exhaustiveness follows from every v ∈ A falling in exactly one inter-cut interval. Each region is a set of consecutive V-positions (by D-CTG, ASN-0036, restricted to the interval between its bounding cuts).

We write w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths.


## Rearrangement Postconditions

The following precondition and postcondition clauses define the rearrangement operation. They are the assumed operational context for the properties introduced in this ASN.

**R-PRE — RearrangePrecondition.**

(i) d ∈ E_doc (the document exists).

(ii) V_S(d) ≠ ∅ (the subspace is non-empty — one cannot rearrange nothing).

(iii) The cut sequence C = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) The affected range lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

(v) Both transposed regions are non-empty: w_α ≥ 1 and w_β ≥ 1.

(vi) **Subspace confinement**: all cuts and all resulting positions remain within subspace S. At depth 2, this is satisfied automatically when all cut ordinals are positive — the rearrangement permutes ordinals within a contiguous range, and no ordinal leaves the range [ord(c₀), ord(c_{n−1})).

Clause (iv) ensures that the affected range is covered: no gap exists within [c₀, c_{n−1}). Combined with D-CTG, this says the entire inter-cut range consists of valid V-positions in V_S(d). Clause (v) excludes degenerate cases where one region is empty.


### 3-Cut Pivot Postcondition

Three cuts produce two adjacent regions that exchange places. The operation is: place β's content where α was, then place α's content immediately after.

**Definition — PivotPostcondition.** Given a 3-cut sequence C = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

where `c₀ + j` and `c₁ + j` denote j ordinal increments via TA5(c) (ASN-0034), and `c₀ + 0 = c₀` by the M-aux convention (ASN-0058). The domain is dom(M'(d)) = dom(M(d)).

In words: the first w_β positions of the affected range receive the content that was in β (clause R-P1). The next w_α positions receive the content that was in α (clause R-P2). Everything outside the affected range is unchanged (clause R-EXT).


### 4-Cut Swap Postcondition

Four cuts produce two outer regions separated by a middle region. The semantics is a direct extension of the pivot: place β's content where α was, place μ's content immediately after, place α's content last.

**Definition — SwapPostcondition.** Given a 4-cut sequence C = (c₀, c₁, c₂, c₃) satisfying R-PRE, the *swap* produces M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₃:

`M'(d)(v) = M(d)(v)`

(R-S1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₂ + j)`

(R-S2) For 0 ≤ j < w_μ:

`M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)`

(R-S3) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)`

with dom(M'(d)) = dom(M(d)).

The arrangement is: region β content starting at c₀ (clause R-S1), then middle content (clause R-S2), then region α content (clause R-S3). Everything outside [c₀, c₃) is unchanged (clause R-EXT).

We must verify that the clauses cover [c₀, c₃) without overlap. The total width is w_β + w_μ + w_α. We need this to equal |[c₀, c₃)| = w_α + w_μ + w_β. Trivially: w_β + w_μ + w_α = w_α + w_μ + w_β. The three clause ranges are [c₀, c₀ + w_β), [c₀ + w_β, c₀ + w_β + w_μ), [c₀ + w_β + w_μ, c₀ + w_β + w_μ + w_α). By M-aux associativity, the last position is c₀ + (w_β + w_μ + w_α) = c₀ + (w_α + w_μ + w_β). And c₀ + (w_α + w_μ + w_β) has ordinal ord(c₀) + w_α + w_μ + w_β = ord(c₃), so the three ranges tile [c₀, c₃) exactly.


## Postcondition Well-Definedness

**R-PIV — PivotWellDefined (LEMMA, supporting).** The pivot postcondition defines a total function on V_S(d) (each position is assigned exactly one I-address).

*Proof.* We must show: (a) every v ∈ V_S(d) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For (a): the positions addressed by R-EXT are those outside [c₀, c₂). The positions addressed by R-P1 are {c₀ + j : 0 ≤ j < w_β}. At depth 2, c₀ = [S, p] and c₀ + j = [S, p + j], so these positions have ordinals p, p + 1, ..., p + w_β − 1. By D-SEQ, these are distinct positions in V_S(d) (since R-PRE(iv) guarantees all ordinals from p to p + w_α + w_β − 1 are occupied). The positions addressed by R-P2 are {c₀ + w_β + j : 0 ≤ j < w_α} = {[S, p + w_β + j] : 0 ≤ j < w_α}, with ordinals p + w_β, ..., p + w_β + w_α − 1. By M-aux (ASN-0058), c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.

The R-P1 ordinal range is [p, p + w_β). The R-P2 ordinal range is [p + w_β, p + w_β + w_α). Since w_β ≥ 1, these ranges are disjoint. Their union is [p, p + w_β + w_α) = [p, p + w_α + w_β). And p + w_α + w_β is the ordinal of c₂ (since |[c₀, c₂)| = w_α + w_β, and by D-SEQ the ordinals are consecutive). So the union of R-P1 and R-P2 covers exactly [c₀, c₂) ∩ V_S(d). Together with R-EXT (covering V_S(d) \ [c₀, c₂)), every position is covered exactly once.

For (b): the right-hand sides reference M(d)(c₁ + j) for j < w_β and M(d)(c₀ + j) for j < w_α. By R-PRE(iv), all positions in [c₀, c₂) are in V_S(d) ⊆ dom(M(d)). The positions c₁ + j for j < w_β have ordinals in [ord(c₁), ord(c₂)) = the ordinals of β. The positions c₀ + j for j < w_α have ordinals in [ord(c₀), ord(c₁)) = the ordinals of α. Both sets are subsets of [c₀, c₂) ∩ V_S(d) ⊆ dom(M(d)). ∎


**R-SWP — SwapWellDefined (LEMMA, supporting).** The swap postcondition defines a total function on V_S(d).

*Proof.* Identical in structure to R-PIV. The three clause ranges partition [c₀, c₃) (shown above). The right-hand sides reference M(d) at positions in β (clause R-S1), μ (clause R-S2), and α (clause R-S3), all within dom(M(d)) by R-PRE(iv). ∎


## The 3-Cut Pivot Permutation

**R-PPERM — PivotPermutation (LEMMA).** The bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                   if v < c₀ or v ≥ c₂     (exterior)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α  (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β  (β → start)
```

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case. For exterior v: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT. For v = c₀ + j in α: π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₀ + j) = M(d)(v) by R-P2. For v = c₁ + j in β: π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₁ + j) = M(d)(v) by R-P1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the three image sets — V_S(d) \ [c₀, c₂), {c₀ + w_β + j : 0 ≤ j < w_α}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (shown in R-PIV). Surjectivity: every position in dom(M'(d)) = dom(M(d)) is the image of some position under π (the three image sets cover V_S(d), also shown in R-PIV). ∎


## The 4-Cut Swap Permutation

**R-SPERM — SwapPermutation (LEMMA).** The bijection π satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                        if v < c₀ or v ≥ c₃               (exterior)
         ⎪ c₀ + w_β + w_μ + j       if v = c₀ + j, 0 ≤ j < w_α        (α → end)
π(v) =  ⎨ c₀ + w_β + j             if v = c₁ + j, 0 ≤ j < w_μ        (μ → middle)
         ⎩ c₀ + j                   if v = c₂ + j, 0 ≤ j < w_β        (β → start)
```

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case.

For exterior v: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT.

For v = c₀ + j in α (0 ≤ j < w_α): π(v) = c₀ + w_β + w_μ + j, and M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j) = M(d)(v) by R-S3.

For v = c₁ + j in μ (0 ≤ j < w_μ): π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₁ + j) = M(d)(v) by R-S2.

For v = c₂ + j in β (0 ≤ j < w_β): π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₂ + j) = M(d)(v) by R-S1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + w_μ + j; the μ case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the four image sets — V_S(d) \ [c₀, c₃), {c₀ + w_β + w_μ + j : 0 ≤ j < w_α}, {c₀ + w_β + j : 0 ≤ j < w_μ}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (shown in R-SWP). Surjectivity: every position in dom(M'(d)) = dom(M(d)) is the image of some position under π (the four image sets cover V_S(d), also shown in R-SWP). ∎

We observe the structural relationship between the two forms: the 4-cut postcondition formulas (R-S1, R-S2, R-S3) reduce to the 3-cut formulas (R-P1, R-P2) when w_μ is set to zero in the expressions — R-S2 vanishes, and R-S3 becomes R-P2. However, the preconditions prevent this degenerate case from arising: CS2 requires c₁ < c₂, so w_μ ≥ 1. The two forms are distinct primitives. The 3-cut pivot transposes two *adjacent* regions; the 4-cut swap transposes two regions separated by at least one middle position.


## Displacement Analysis

The permutations R-PPERM and R-SPERM can be characterized by ordinal displacements — how far each position moves within its subspace. These displacements illuminate the structure and connect to the block decomposition transformation.

**Definition — PermutationDisplacement.** For a position v in the affected range, define Δ(v) = ord(π(v)) − ord(v) (an integer, possibly negative).

For the 3-cut pivot, from R-PPERM:

```
Δ(v) = +w_β      if v ∈ α     (shifts forward by width of β)
Δ(v) = −w_α      if v ∈ β     (shifts backward by width of α)
Δ(v) = 0         otherwise
```

For the 4-cut swap, from R-SPERM:

```
Δ(v) = +(w_β + w_μ)        if v ∈ α   (shifts forward past middle and β)
Δ(v) = +(w_β − w_α)        if v ∈ μ   (adjusts by width difference)
Δ(v) = −(w_α + w_μ)        if v ∈ β   (shifts backward past middle and α)
Δ(v) = 0                   otherwise
```

We observe a symmetry in the 3-cut case: the forward displacement of α equals the width of β, and vice versa. The displacements sum to zero over the affected range: w_α · w_β + w_β · (−w_α) = 0. This is a necessary consequence of π being a bijection on a contiguous range — positions merely exchange, so the total displacement is zero.

In the 4-cut case, the symmetry is more subtle. The forward displacement of α is w_β + w_μ, while the backward displacement of β is w_α + w_μ. These are equal only when w_α = w_β. The middle compensates: w_μ · (w_β − w_α) absorbs the imbalance. The total displacement over the affected range is w_α · (w_β + w_μ) + w_μ · (w_β − w_α) + w_β · (−(w_α + w_μ)) = w_α · w_β + w_α · w_μ + w_μ · w_β − w_μ · w_α − w_β · w_α − w_β · w_μ = 0.

The displacement formulation makes it clear that every position in the affected range shifts by a value determined solely by the region widths — the displacement does not depend on the position's location within its region. All positions in α shift by the same amount; all positions in β shift by the same amount.


## Block Decomposition Transformation

**R-BLK — BlockDecompositionTransformation (LEMMA).** Let B = {β₁, ..., βₘ} be a block decomposition of M(d) satisfying B1–B3 (ASN-0058). Let the cut sequence C have cut positions c₀, ..., c_{n−1}. The rearranged arrangement M'(d) admits a block decomposition B' obtained by:

*Phase 1: Split.* For each cut position cᵢ, if cᵢ falls in the interior of some block βₖ = (vₖ, aₖ, nₖ) — meaning cᵢ ∈ V(βₖ) and cᵢ ≠ vₖ — split βₖ at the point c = ord(cᵢ) − ord(vₖ) via M4 (SplitDefinition, ASN-0058). This produces two blocks: (vₖ, aₖ, c) and (vₖ + c, aₖ + c, nₖ − c). By M5 (SplitPartition) and M6f (SplitFrame), the resulting decomposition is equivalent to B. After all splits, no block straddles any cut position.

*Phase 2: Classify.* Each block in the post-split decomposition lies entirely within one region (exterior left, α, μ if 4-cut, β, or exterior right), because no block crosses a cut boundary.

*Phase 3: Reassemble.* Apply the permutation to each block's V-start:

- Exterior blocks: unchanged.
- α blocks: β_k = (vₖ, aₖ, nₖ) becomes (π(vₖ), aₖ, nₖ) — the V-start shifts by the α displacement, the I-start and width are preserved.
- β blocks: similarly, V-start shifts by the β displacement.
- μ blocks (4-cut only): V-start shifts by the μ displacement.

The I-start and width of each block are preserved because REARRANGE modifies no I-addresses and the displacement is uniform within each region (all positions in a region shift by the same amount). The resulting blocks satisfy B3 (Consistency): for each block j, the reassembled block is (π(vⱼ), aⱼ, nⱼ), and for each offset k with 0 ≤ k < nⱼ: M'(d)(π(vⱼ) + k) = M'(d)(π(vⱼ + k)) = M(d)(vⱼ + k) = aⱼ + k. The second equality holds because π(vⱼ + k) = π(vⱼ) + k — the uniform displacement means ordinal increment commutes with the permutation within each region.

*Proof (commutativity).* For v = vⱼ + k in region α (3-cut case): π(v) = v + w_β (adding w_β ordinal positions). And π(vⱼ) + k = (vⱼ + w_β) + k = vⱼ + (w_β + k) = (vⱼ + k) + w_β = v + w_β = π(v), using M-aux and commutativity of natural-number addition at the ordinal level. The argument is identical for β, μ, and exterior regions. ∎

Coverage (B1) and disjointness (B2) follow from π being a bijection: π maps the V-extents of the original blocks to pairwise-disjoint sets covering dom(M'(d)).

The decomposition B' is valid but not necessarily maximally merged. After rearrangement, blocks that were in different regions may become V-adjacent and I-adjacent. For example, if the last block of β (now placed at the end of the β region in its new position) happens to be I-adjacent with the first block of the following region, M7 (MergeCondition, ASN-0058) is satisfied and the two blocks could be merged. The maximally merged decomposition (M12) may therefore have fewer blocks than B'.


## Worked Example: 3-Cut Pivot on a 5-Position Document

We trace a concrete 3-cut pivot to verify the postconditions against explicit values. Let document d have subspace S = 1 with V_S(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 5.0.2.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.2    (I-address E)
```

Content A–C originates from document 3.0.1 (origin 3.0.1); D–E from document 5.0.2 (origin 5.0.2). The canonical decomposition has two blocks: β₁ = ([1,1], 3.0.1.0.1.1, 3) and β₂ = ([1,4], 5.0.2.0.1.1, 2).

We apply a 3-cut pivot with C = ([1,2], [1,4], [1,5]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5]. The affected range is [c₀, c₂) = {[1,2], [1,3], [1,4]}. Region α = {[1,2], [1,3]} (w_α = 2), region β = {[1,4]} (w_β = 1).

**R-PRE verification.** (i) d ∈ E_doc. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 3; CS2: [1,2] < [1,4] < [1,5]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,5]) are in V_S(d). (v) w_α = 2 ≥ 1, w_β = 1 ≥ 1. (vi) All ordinals positive. ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,5]) = M(d)([1,5]) = E.

R-P1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-P2 (j = 0): M'(d)(c₀ + 1 + 0) = M'(d)([1,3]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-P2 (j = 1): M'(d)(c₀ + 1 + 1) = M'(d)([1,4]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = D     (was β, now at start of affected range)
M'(d)([1,3]) = B     (was α position 1, shifted forward by w_β = 1)
M'(d)([1,4]) = C     (was α position 2, shifted forward by w_β = 1)
M'(d)([1,5]) = E     (exterior, unchanged)
```

**R-PPERM verification.** The permutation π: π([1,1]) = [1,1] (exterior), π([1,2]) = [1,3] (α: c₀ + 0 → c₀ + w_β + 0 = [1,3]), π([1,3]) = [1,4] (α: c₀ + 1 → c₀ + w_β + 1 = [1,4]), π([1,4]) = [1,2] (β: c₁ + 0 → c₀ + 0 = [1,2]), π([1,5]) = [1,5] (exterior). We check: M'(d)(π([1,2])) = M'(d)([1,3]) = B = M(d)([1,2]) ✓. M'(d)(π([1,4])) = M'(d)([1,2]) = D = M(d)([1,4]) ✓.

**Block decomposition after rearrangement.** The new canonical decomposition has four blocks: ([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2), ([1,5], E, 1). Block ([1,3], B, 2) is valid because B = 3.0.1.0.1.2 and C = 3.0.1.0.1.3 = B + 1. Block ([1,5], E, 1) is exterior, unchanged by R-EXT. Note that D = 5.0.2.0.1.1 cannot merge with A = 3.0.1.0.1.1 (different origins, per M16) nor with B = 3.0.1.0.1.2 (not I-adjacent: D + 1 ≠ B). Block ([1,3], B, 2) cannot merge with ([1,5], E, 1): C + 1 = 3.0.1.0.1.4 ≠ E = 5.0.2.0.1.2 (different origins). The cut at [1,2] (c₀, interior to β₁ at offset 1) split the original block β₁ into ([1,1], A, 1) and ([1,2], B, 2), and the rearrangement inserted the single-element block for D between them.


## Worked Example: 4-Cut Swap on an 8-Position Document

We trace a 4-cut swap with unequal region widths. Let document d have subspace S = 1 with V_S(d) = {[1,1], ..., [1,8]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 7.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.1    (I-address E)
M(d)([1,6]) = 5.0.2.0.1.2    (I-address F)
M(d)([1,7]) = 5.0.2.0.1.3    (I-address G)
M(d)([1,8]) = 3.0.1.0.1.4    (I-address H)
```

Content A–C originates from document 3.0.1; D from document 7.0.1; E–G from document 5.0.2; H from document 3.0.1. The canonical decomposition has four blocks: β₁ = ([1,1], A, 3), β₂ = ([1,4], D, 1), β₃ = ([1,5], E, 3), β₄ = ([1,8], H, 1).

We apply a 4-cut swap with C = ([1,2], [1,4], [1,5], [1,8]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5], c₃ = [1,8]. The affected range is [c₀, c₃) = {[1,2], ..., [1,7]}. Region α = {[1,2], [1,3]} (w_α = 2), middle μ = {[1,4]} (w_μ = 1), region β = {[1,5], [1,6], [1,7]} (w_β = 3). Since w_α = 2 ≠ w_β = 3, the middle displacement w_β − w_α = 1 is nonzero.

**R-PRE verification.** (i) d ∈ E_doc. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 4; CS2: [1,2] < [1,4] < [1,5] < [1,8]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,8]) are in V_S(d). (v) w_α = 2 ≥ 1, w_β = 3 ≥ 1. (vi) All ordinals positive. ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,8]) = M(d)([1,8]) = H.

R-S1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₂ + 0) = M(d)([1,5]) = E.

R-S1 (j = 1): M'(d)(c₀ + 1) = M'(d)([1,3]) = M(d)(c₂ + 1) = M(d)([1,6]) = F.

R-S1 (j = 2): M'(d)(c₀ + 2) = M'(d)([1,4]) = M(d)(c₂ + 2) = M(d)([1,7]) = G.

R-S2 (j = 0): M'(d)(c₀ + 3 + 0) = M'(d)([1,5]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-S3 (j = 0): M'(d)(c₀ + 3 + 1 + 0) = M'(d)([1,6]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-S3 (j = 1): M'(d)(c₀ + 3 + 1 + 1) = M'(d)([1,7]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = E     (from β via R-S1)
M'(d)([1,3]) = F     (from β via R-S1)
M'(d)([1,4]) = G     (from β via R-S1)
M'(d)([1,5]) = D     (from μ via R-S2)
M'(d)([1,6]) = B     (from α via R-S3)
M'(d)([1,7]) = C     (from α via R-S3)
M'(d)([1,8]) = H     (exterior, unchanged)
```

The three swap clauses tile [c₀, c₃) = [[1,2], [1,8]) exactly: R-S1 covers ordinals 2–4 (w_β = 3 positions), R-S2 covers ordinal 5 (w_μ = 1 position), R-S3 covers ordinals 6–7 (w_α = 2 positions). Total: 3 + 1 + 2 = 6 = |[c₀, c₃)|. ✓

**R-SPERM verification.** The permutation π:

- π([1,1]) = [1,1] (exterior).
- π([1,2]) = c₀ + w_β + w_μ + 0 = [1,6] (α: j = 0). Check: M'(d)([1,6]) = B = M(d)([1,2]) ✓.
- π([1,3]) = c₀ + w_β + w_μ + 1 = [1,7] (α: j = 1). Check: M'(d)([1,7]) = C = M(d)([1,3]) ✓.
- π([1,4]) = c₀ + w_β + 0 = [1,5] (μ: j = 0). Check: M'(d)([1,5]) = D = M(d)([1,4]) ✓.
- π([1,5]) = c₀ + 0 = [1,2] (β: j = 0). Check: M'(d)([1,2]) = E = M(d)([1,5]) ✓.
- π([1,6]) = c₀ + 1 = [1,3] (β: j = 1). Check: M'(d)([1,3]) = F = M(d)([1,6]) ✓.
- π([1,7]) = c₀ + 2 = [1,4] (β: j = 2). Check: M'(d)([1,4]) = G = M(d)([1,7]) ✓.
- π([1,8]) = [1,8] (exterior).

**Displacement verification.** Δ([1,2]) = 6 − 2 = +4 = w_β + w_μ ✓. Δ([1,3]) = 7 − 3 = +4 ✓. Δ([1,4]) = 5 − 4 = +1 = w_β − w_α ✓. Δ([1,5]) = 2 − 5 = −3 = −(w_α + w_μ) ✓. Δ([1,6]) = 3 − 6 = −3 ✓. Δ([1,7]) = 4 − 7 = −3 ✓. The middle-region displacement is +1, confirming the asymmetric structure when w_α ≠ w_β.

**Block decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to β₁ = ([1,1], A, 3) at offset 1. Split: ([1,1], A, 1) and ([1,2], B, 2). The remaining cuts c₁ = [1,4], c₂ = [1,5], c₃ = [1,8] coincide with block starts, so no further splits. Post-split decomposition: {([1,1], A, 1), ([1,2], B, 2), ([1,4], D, 1), ([1,5], E, 3), ([1,8], H, 1)}.

*Phase 2 (Classify):* ([1,1], A, 1) → exterior left. ([1,2], B, 2) → α. ([1,4], D, 1) → μ. ([1,5], E, 3) → β. ([1,8], H, 1) → exterior right.

*Phase 3 (Reassemble):* Apply region displacements:

- ([1,1], A, 1) → ([1,1], A, 1) (exterior, Δ = 0)
- ([1,2], B, 2) → ([1,6], B, 2) (α, Δ = +4)
- ([1,4], D, 1) → ([1,5], D, 1) (μ, Δ = +1)
- ([1,5], E, 3) → ([1,2], E, 3) (β, Δ = −3)
- ([1,8], H, 1) → ([1,8], H, 1) (exterior, Δ = 0)

Sorted by V-start: {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 2), ([1,8], H, 1)}. Checking B3: for block ([1,2], E, 3), M'(d)([1,2]) = E, M'(d)([1,3]) = F = E + 1, M'(d)([1,4]) = G = E + 2 ✓.

*Merge check:* ([1,6], B, 2) and ([1,8], H, 1) are V-adjacent (6 + 2 = 8) and I-adjacent (B + 2 = 3.0.1.0.1.4 = H). Merge: ([1,6], B, 3). No other pair satisfies both conditions — ([1,1], A, 1) and ([1,2], E, 3) differ in origin; ([1,2], E, 3) and ([1,5], D, 1) differ in origin; ([1,5], D, 1) and ([1,6], B, 2) differ in origin.

**Canonical decomposition:** {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 3)}. The rearrangement brought B, C (formerly at [1,2]–[1,3]) adjacent to H (at [1,8]), and since B + 2 = H, they merge into a single block of width 3. Meanwhile A, formerly part of a width-3 block with B and C, is now isolated.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| R-PIV | LEMMA | Pivot postcondition is a total function on V_S(d) | supporting |
| R-SWP | LEMMA | Swap postcondition is a total function on V_S(d) | supporting |
| R-PPERM | LEMMA | Bijection π for 3-cut pivot: α shifts forward by w_β, β shifts backward by w_α | introduced |
| R-SPERM | LEMMA | Bijection π for 4-cut swap: α shifts forward by w_β + w_μ, μ shifts by w_β − w_α, β shifts backward by w_α + w_μ | introduced |
| R-BLK | LEMMA | Block decomposition transforms by split-at-cuts then displace-per-region, preserving B1–B3 | introduced |


## Open Questions

Does the 4-cut swap definition generalize to k-cut rearrangements for k > 4, and if so, what is the natural class of permutations that "rearrangement by cut points" can express?

What must a well-formed editing sequence guarantee about the composition of multiple rearrangements — is the composition of two rearrangements always expressible as a single rearrangement, or can sequences of rearrangements produce arrangements unreachable by any single operation?

Under what conditions can a rearrangement cause the number of mapping blocks in the canonical decomposition to increase, and is there an upper bound on the increase relative to the number of cut points?

What constraints, if any, must cut points satisfy relative to the mapping block boundaries of the canonical decomposition, or are arbitrary cut positions within the V-span always valid?
