# ASN-0065: REARRANGE Operation

*2026-03-21*

We are looking for the precise effect of rearranging segments of a document's content stream by cut points. Nelson names the operation REARRANGE and defines it tersely: "Rearrange transposes two regions of text" [LM 4/67]. Transposition — two things exchanging places — is a permutation, and a very specific one: no content is created, none destroyed, none duplicated. The bytes change position; they do not change identity.

This makes REARRANGE the most conservative of all editing operations. INSERT adds new content to the permanent store. DELETE removes content from the current arrangement (though not from the store). COPY maps existing content into new V-positions. REARRANGE does none of these. It touches nothing but the arrangement — the mapping from V-positions to I-addresses — and it touches that mapping only by permuting its domain. Every I-address that appeared before appears after, at exactly the same multiplicity.

The question is: what exactly does this permutation look like, what must it preserve, and what may it change?


## State and Vocabulary

We work with system state Σ = (C, E, M, R) per ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The content store is append-only (S0, P0). The arrangement M(d) is the mutable layer. REARRANGE must specify exactly how it reorders M(d) while respecting C's immutability and, indeed, leaving M(d)'s range untouched.

For a V-position v with subspace(v) = v₁ and #v = m, the *ordinal* is ord(v) = [v₂, ..., vₘ] — the tumbler obtained by stripping the subspace identifier. The reconstruction vpos(S, o) = [S, o₁, ..., oₖ] is its inverse.

We restrict to depth-2 V-positions (#v = 2, ordinal depth 1) throughout this ASN. At depth 2, D-SEQ (ASN-0036) gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, and ordinals are single natural numbers. This restriction simplifies the presentation; generalization to deeper ordinals is structurally identical by D-CTG-depth (ASN-0036), which reduces contiguity at any depth m ≥ 3 to contiguity of the last component alone (see Open Questions).

We recall D-CTG (VContiguity, ASN-0036): within each subspace, V-positions form a contiguous ordinal range with no gaps. REARRANGE must preserve this invariant.


## Rearrangement as Arrangement Reordering

Nelson locates REARRANGE squarely within the Istream/Vstream separation:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Rearrangement alters the *order* — the Vstream — while leaving the *content* — the Istream — untouched. In the state-transition framework of ASN-0047, this is K.μ~ (ArrangementReordering): a distinguished composite (K.μ⁻ + K.μ⁺) admitting a bijection π : dom(M(d)) → dom(M'(d)) such that M'(d)(π(v)) = M(d)(v) for all v ∈ dom(M(d)). The corollary is ran(M'(d)) = ran(M(d)) — the multiset of I-addresses is invariant.

But K.μ~ admits *any* bijection. REARRANGE is a specific kind of K.μ~ — one determined by cut points that identify two regions to exchange. We need to characterize this specific permutation.


## Cut Points and the Region Partition

Nelson specifies two variants:

> "With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

A *cut sequence* specifies the boundaries. We formalize this as a tuple of V-positions within a single subspace.

**Definition — CutSequence.** A *cut sequence* for document d in subspace S is a tuple C = (c₀, c₁, ..., c_{n−1}) of V-positions satisfying:

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


## Precondition

**R-PRE — RearrangePrecondition (PRE).**

(i) d ∈ E_doc (the document exists).

(ii) V_S(d) ≠ ∅ (the subspace is non-empty — one cannot rearrange nothing).

(iii) The cut sequence C = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) The affected range lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

(v) Both transposed regions are non-empty: w_α ≥ 1 and w_β ≥ 1.

(vi) **Subspace confinement**: all cuts and all resulting positions remain within subspace S. At depth 2, this is satisfied automatically when all cut ordinals are positive — the rearrangement permutes ordinals within a contiguous range, and no ordinal leaves the range [ord(c₀), ord(c_{n−1})).

Clause (iv) ensures that the affected range is covered: no gap exists within [c₀, c_{n−1}). Combined with D-CTG, this says the entire inter-cut range consists of valid V-positions in V_S(d). Clause (v) excludes degenerate cases where one region is empty. When w_α = 0 or w_β = 0, one region contributes nothing to the transposition, and the operation would be a no-op for the empty region. We require non-empty regions to ensure the permutation is non-trivial.


## The 3-Cut Pivot

We begin with the simpler case: three cuts producing two adjacent regions that exchange places. Nelson: with three cuts, the regions "from cut 1 to cut 2" and "from cut 2 to cut 3" are transposed. In our notation, region α = [c₀, c₁) and region β = [c₁, c₂).

The operation is: place β's content where α was, then place α's content immediately after.

**Definition — PivotPostcondition.** Given a 3-cut sequence C = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

where `c₀ + j` and `c₁ + j` denote j ordinal increments via TA5(c) (ASN-0034), and `c₀ + 0 = c₀` by the M-aux convention (ASN-0058). The domain is dom(M'(d)) = dom(M(d)).

In words: the first w_β positions of the affected range receive the content that was in β (clause R-P1). The next w_α positions receive the content that was in α (clause R-P2). Everything outside the affected range is unchanged (clause R-EXT).

We verify that these clauses are well-defined and cover all positions in V_S(d).

**R-PIV — PivotWellDefined (LEMMA).** The pivot postcondition defines a total function on V_S(d) (each position is assigned exactly one I-address).

*Proof.* We must show: (a) every v ∈ V_S(d) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For (a): the positions addressed by R-EXT are those outside [c₀, c₂). The positions addressed by R-P1 are {c₀ + j : 0 ≤ j < w_β}. At depth 2, c₀ = [S, p] and c₀ + j = [S, p + j], so these positions have ordinals p, p + 1, ..., p + w_β − 1. By D-SEQ, these are distinct positions in V_S(d) (since R-PRE(iv) guarantees all ordinals from p to p + w_α + w_β − 1 are occupied). The positions addressed by R-P2 are {c₀ + w_β + j : 0 ≤ j < w_α} = {[S, p + w_β + j] : 0 ≤ j < w_α}, with ordinals p + w_β, ..., p + w_β + w_α − 1. By M-aux (ASN-0058), c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.

The R-P1 ordinal range is [p, p + w_β). The R-P2 ordinal range is [p + w_β, p + w_β + w_α). Since w_β ≥ 1, these ranges are disjoint. Their union is [p, p + w_β + w_α) = [p, p + w_α + w_β). And p + w_α + w_β is the ordinal of c₂ (since |[c₀, c₂)| = w_α + w_β, and by D-SEQ the ordinals are consecutive). So the union of R-P1 and R-P2 covers exactly [c₀, c₂) ∩ V_S(d). Together with R-EXT (covering V_S(d) \ [c₀, c₂)), every position is covered exactly once.

For (b): the right-hand sides reference M(d)(c₁ + j) for j < w_β and M(d)(c₀ + j) for j < w_α. By R-PRE(iv), all positions in [c₀, c₂) are in V_S(d) ⊆ dom(M(d)). The positions c₁ + j for j < w_β have ordinals in [ord(c₁), ord(c₂)) = the ordinals of β. The positions c₀ + j for j < w_α have ordinals in [ord(c₀), ord(c₁)) = the ordinals of α. Both sets are subsets of [c₀, c₂) ∩ V_S(d) ⊆ dom(M(d)). ∎

We now identify the permutation explicitly.

**R-PPERM — PivotPermutation (LEMMA).** The bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                   if v < c₀ or v ≥ c₂     (exterior)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α  (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β  (β → start)
```

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case. For exterior v: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT. For v = c₀ + j in α: π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₀ + j) = M(d)(v) by R-P2. For v = c₁ + j in β: π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₁ + j) = M(d)(v) by R-P1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the three image sets — V_S(d) \ [c₀, c₂), {c₀ + w_β + j : 0 ≤ j < w_α}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (shown in R-PIV). Surjectivity: every position in dom(M'(d)) = dom(M(d)) is the image of some position under π (the three image sets cover V_S(d), also shown in R-PIV). ∎


## The 4-Cut Swap

Four cuts produce two outer regions separated by a middle region. Nelson: with four cuts, the regions "from cut 1 to cut 2" and "from cut 3 to cut 4" are transposed. In our notation, α = [c₀, c₁) and β = [c₂, c₃), with the middle μ = [c₁, c₂) between them.

The semantics is a direct extension of the pivot: place β's content where α was, place μ's content immediately after, place α's content last.

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

**R-SWP — SwapWellDefined (LEMMA).** The swap postcondition defines a total function on V_S(d).

*Proof.* Identical in structure to R-PIV. The three clause ranges partition [c₀, c₃) (shown above). The right-hand sides reference M(d) at positions in β (clause R-S1), μ (clause R-S2), and α (clause R-S3), all within dom(M(d)) by R-PRE(iv). ∎

The permutation for the swap is:

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

The permutations R-PPERM and R-SPERM can be characterized by ordinal displacements — how far each position moves within its subspace. These displacements illuminate the structure and connect to the implementation.

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

**R-CP verification.** The multiset of I-addresses is {A, B, C, D, E} before and after. ✓

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

**R-CP verification.** The multiset of I-addresses is {A, B, C, D, E, F, G, H} before and after. ✓

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


## Content Preservation

The central invariant of REARRANGE is that the multiset of I-addresses in the arrangement is unchanged.

**R-CP — ContentPreservation (INV).** For any rearrangement satisfying R-PRE:

`ran(M'(d)) = ran(M(d))`

as multisets (that is, for every I-address a, the multiplicity |{v : M'(d)(v) = a}| = |{v : M(d)(v) = a}|).

*Proof.* By R-PPERM (or R-SPERM for the 4-cut case), π is a bijection dom(M(d)) → dom(M'(d)) with M'(d)(π(v)) = M(d)(v). For any I-address a:

`{v : M'(d)(v) = a} = {π(u) : M(d)(u) = a}`

Since π is a bijection, |{π(u) : M(d)(u) = a}| = |{u : M(d)(u) = a}|. ∎

Nelson states this explicitly:

> "Rearrange transposes two regions of text." [LM 4/67]

The word "transposes" is precise — a transposition is a permutation, not a transformation that can add, remove, or duplicate content. Gregory's implementation confirms: only the V-displacement component (`cdsp.dsas[V]`) of POOM entries is modified; I-addresses are never touched [edit.c:125]. The spanfilade (link endpoint index) and granfilade (content store) are completely untouched by `rearrangend`.

**Corollary (R-CP-set).** As a set equality: `{a : (E v :: M'(d)(v) = a)} = {a : (E v :: M(d)(v) = a)}`.

REARRANGE cannot orphan content. Unlike DELETE, which can remove all V-references to an I-address, leaving content unreachable through any arrangement, rearrangement preserves every reference. Content that was reachable through the arrangement before remains reachable after.


## Frame Conditions

REARRANGE modifies only the arrangement of the target document in the target subspace. Everything else is held constant.

**R-CF — RearrangeFrame (INV).**

(a) C' = C — the content store is unchanged. No bytes are created, destroyed, or modified. Rearrangement is a pure arrangement operation.

(b) E' = E — the entity set is unchanged. No documents, accounts, or nodes are created or destroyed.

(c) R' = R — the provenance relation is unchanged. Since ran(M'(d)) = ran(M(d)) (R-CP), no new I-address enters the arrangement, and no I-address leaves it. J3 (ReorderingIsolation, ASN-0047) mandates exactly this: R' = R. The remaining coupling constraints of ValidComposite are vacuously satisfied: J0 (AllocationRequiresPlacement) is vacuous because dom(C') \ dom(C) = ∅ by R-CF(a). J1 (ExtensionRecordsProvenance) is vacuous because ran(M'(d)) \ ran(M(d)) = ∅ by R-CP. J1' (ProvenanceRequiresExtension) is vacuous because R' \ R = ∅ by J3. (J2, ContractionIsolation, does not apply — REARRANGE is K.μ~, not elementary K.μ⁻.)

**R-XD — CrossDocumentIsolation (INV).** For all d' ≠ d:

`M'(d') = M(d')`

REARRANGE targets a single document. No other document's arrangement is consulted or modified.

**R-XS — SubspaceConfinement (INV).** For all v with subspace(v) ≠ S:

`M'(d)(v) = M(d)(v)`

Within the target document, only the affected subspace changes. Link-subspace positions (subspace 0) and any other subspaces are untouched.

**R-IID — DocumentIdentityPreservation (INV).**

`d ∈ E'_doc`

The document remains a valid entity after rearrangement. This follows from E' = E (R-CF(b)).


## K.μ~ Preconditions and Arrangement Invariants

We verify that REARRANGE satisfies the K.μ~ preconditions (ASN-0047) and preserves the arrangement invariants required by the ReachableStateInvariants theorem.

**R-KMU — K.μ~ Precondition Verification (LEMMA).** REARRANGE satisfies the K.μ~ preconditions.

*Proof.* K.μ~ requires: (i) d ∈ E_doc, (ii) the bijection π produces V-positions satisfying S8a, and (iii) M'(d) satisfies S8-depth. Clause (i) is R-PRE(i). For clause (ii): π maps dom(M(d)) to itself — dom(M'(d)) = dom(M(d)). For the text-subspace portion (v₁ ≥ 1), this is established by R-PIV and R-SWP; for positions outside subspace S, R-XS gives M'(d)(v) = M(d)(v), so those positions are fixed by π. Since every v ∈ dom(M(d)) satisfies S8a in the pre-state, and π(v) ∈ dom(M(d)), every image under π satisfies S8a. For clause (iii): S8-depth requires all V-positions in a subspace to share the same depth. Since dom(M'(d)) = dom(M(d)), the depth profile is unchanged. ∎

**R-S2P — FunctionalityPreservation (LEMMA).** REARRANGE preserves S2 (ArrangementFunctionality).

*Proof.* R-PIV and R-SWP establish that the postcondition defines a total function on V_S(d) — each V-position is assigned exactly one I-address. For positions outside subspace S, M'(d)(v) = M(d)(v) by R-XS, which is uniquely determined by S2 in the pre-state. ∎

**R-S3P — ReferentialIntegrityPreservation (LEMMA).** REARRANGE preserves S3 (ReferentialIntegrity).

*Proof.* By R-CP, ran(M'(d)) = ran(M(d)). By S3 in the pre-state, ran(M(d)) ⊆ dom(C). By R-CF(a), C' = C, so dom(C') = dom(C). Therefore ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C'). ∎

**R-S8P — StructuralPreservation (LEMMA).** REARRANGE preserves S8a, S8-depth, and S8-fin.

*Proof.* All three properties are predicates on dom(M(d)). Since dom(M'(d)) = dom(M(d)), each is inherited from the pre-state. S8a (VPositionWellFormedness): every v ∈ dom(M'(d)) = dom(M(d)) satisfies zeros(v) = 0 ∧ v > 0. S8-depth (FixedDepthVPositions): all V-positions in each subspace share depth, unchanged by domain equality. S8-fin (FiniteArrangement): |dom(M'(d))| = |dom(M(d))| < ∞. ∎


## Contiguity Preservation

REARRANGE must leave V_S(d) contiguous (D-CTG, ASN-0036). We verify this.

**R-DP — ContiguityPreservation (LEMMA).** If V_S(d) satisfies D-CTG before rearrangement, then V_S'(d) satisfies D-CTG after rearrangement.

*Proof.* The domain of M'(d) restricted to subspace S is dom(M'(d)) ∩ {v : subspace(v) = S}. By dom(M'(d)) = dom(M(d)) (from the bijection π), this equals dom(M(d)) ∩ {v : subspace(v) = S} = V_S(d). Since V_S'(d) = V_S(d) as a set of positions, contiguity is inherited. ∎

This is the simplest possible contiguity argument: REARRANGE does not change which positions exist, only what content they map to. The domain of the arrangement is invariant. Similarly:

**R-WR — WidthPreservation (LEMMA).** |V_S'(d)| = |V_S(d)|.

*Proof.* V_S'(d) = V_S(d) (same positions, different content mapping). ∎


## Block Decomposition

We now examine how REARRANGE transforms the block decomposition of M(d) (ASN-0058). This connects the abstract specification to the concrete mechanics of the operation.

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

Gregory's implementation confirms this structure. The `makecutsnd` call [edit.c:110] performs Phase 1 by calling `slicecbcpm` [ndcuts.c:373] on every POOM bottom crum that straddles a cut. The offset loop [edit.c:113–136] performs Phase 3 by calling `tumbleradd` on the V-displacement of each classified crum. Phase 2 is implicit in `rearrangecutsectionnd` [edit.c:191–204], which returns the region number for each crum based on the rightmost cut at or to the left of its V-start.


## Link Survivability

Links attach to I-addresses, not V-positions. REARRANGE changes V-positions but preserves all I-addresses. Therefore links are entirely unaffected.

**R-LS — LinkSurvivability (LEMMA).** If a link's endset references I-address a, and a ∈ ran(M(d)), then a ∈ ran(M'(d)) after any rearrangement.

*Proof.* By R-CP, ran(M'(d)) = ran(M(d)). ∎

Nelson states this emphatically:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Since REARRANGE preserves all bytes — it neither adds nor removes any I-address reference — "anything is left at each end" is trivially satisfied. The link survives with its full original byte set intact.

After rearrangement, a link that referenced a contiguous span of I-addresses still references those same I-addresses, but they may now occupy non-contiguous V-positions. This is a natural consequence of Nelson's design:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes." [LM 4/42]

The V-space rendering of a link endset changes (the endset may span two non-adjacent V-regions), but the underlying I-address set is invariant. A front end rendering the link would highlight both V-regions.

Similarly, transclusion relationships survive rearrangement. A transcluded region split by a cut point becomes two V-separated pieces, each retaining its original I-address identity. The system continues to recognize their origin: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40].


## The Boundary Between Rearranged Segments

When two previously non-adjacent segments become adjacent through rearrangement, the boundary between them deserves attention. In the Vstream, the new adjacency is seamless — V-positions are dense and contiguous (D-CTG), and the user sees no discontinuity. In the POOM (the V-to-I mapping), the boundary is a span break: the last I-address of one segment and the first I-address of the next are not consecutive.

This is not a special condition created by REARRANGE. It is the normal state of any document that has undergone editing. Every INSERT creates new span boundaries (the inserted content has different I-addresses from the surrounding text). Every transclusion (COPY) creates span boundaries. The POOM was specifically designed to handle arbitrary numbers of such boundaries efficiently.

Nelson's architecture separates *arrangement* (Vstream, mutable, seamless) from *identity* (Istream, permanent, discontinuous after editing). The block decomposition (ASN-0058) captures this separation: each block is a contiguous V-to-I correspondence run, and the document is a sequence of such blocks. REARRANGE changes which blocks appear where; it does not change the fundamental character of the representation.


## Historical Recoverability

Nelson requires that the prior arrangement be recoverable. The storage system is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "Any previous instant [can be] reconstructed." [LM 2/15]

REARRANGE is a change to the arrangement. The append-only model records this change, and the prior arrangement can be reconstructed. We note this as a system-level guarantee rather than a property of REARRANGE itself — the recoverability depends on the storage layer recording the state transition, not on any special structure of the rearrangement.

In the formal model, version creation (J4, Fork, ASN-0047) captures the relevant mechanism: the pre-rearrangement arrangement can be preserved as a prior version by forking before rearranging. The version's arrangement maps the same V-positions to the same I-addresses as the pre-rearrangement state, since Fork preserves the entire M(d).


## The 3-Cut Pivot as the Fundamental Case

We observe that the 4-cut swap can be expressed as a specific pattern of two 3-cut pivots. Given a 4-cut sequence (c₀, c₁, c₂, c₃), one could achieve the same result by:

1. Pivot with cuts (c₀, c₁, c₂): swaps [c₀, c₁) and [c₁, c₂). After this, α is at [c₁, c₂) and μ is at [c₀, c₁), and β is at its original position.

But this is not the same as the 4-cut swap — the content layout after this single pivot is [μ, α, β], while the swap target is [β, μ, α]. Achieving the swap would require a second pivot with adjusted cut points to account for the changed positions.

The 4-cut swap is therefore best understood as a primitive operation in its own right, defined directly by its postcondition (R-S1, R-S2, R-S3). Whether an implementation realizes it as a single pass or as composed pivots is an implementation choice; the abstract specification is the postcondition.


## Implementation Observations

Several aspects of Gregory's implementation illuminate the abstract specification without constraining it. We note them here as non-normative observations.

**Split precedes displacement.** The `makecutsnd` call [edit.c:110] ensures that no POOM bottom crum straddles a cut point before the displacement loop runs. If a cut falls in the interior of a crum, `slicecbcpm` [ndcuts.c:373] physically splits it into two crums at the boundary. Any crum that still straddles a cut during the displacement phase triggers a fatal error (`gerror` at [edit.c:118]). This enforces the abstract Phase 1 of R-BLK as a hard precondition for Phase 3.

**Pure POOM mutation.** REARRANGE operates exclusively on the document's POOM (permutation matrix enfilade). The entry point `dorearrange` [do1.c:34] calls only `findorgl` and `rearrangepm`; there is no reference to the spanfilade or granfilade. Compare with `docopy`, which calls both `insertpm` (POOM) and `insertspanf` (spanfilade). This confirms R-CF: the content store and link index are structurally untouched.

**3-cut displacement correctness.** For the 3-cut case, `makeoffsetsfor3or4cuts` [edit.c:177–181] computes:

```
diff[1] = c₂ − c₁     (= w_β, forward shift for α)
diff[2] = −(c₁ − c₀)  (= −w_α, backward shift for β)
```

These match the displacement analysis exactly: positions in α shift forward by w_β, positions in β shift backward by w_α. The sign-flip is implemented by toggling the `.sign` field of the tumbler [edit.c:180]. The 3-cut implementation is sound.

**4-cut displacement discrepancy.** For the 4-cut case, `makeoffsetsfor3or4cuts` [edit.c:169–176] computes:

```
diff[1] = c₂ − c₀         (= w_α + w_μ)
diff[2] = (c₃ − c₂) − (c₁ − c₀)  (= w_β − w_α)
diff[3] = −(c₂ − c₀)      (= −(w_α + w_μ))
```

The displacement analysis (derived from R-SPERM) requires:

```
Δ_α = w_β + w_μ       (forward shift for α)
Δ_μ = w_β − w_α       (middle adjustment)
Δ_β = −(w_α + w_μ)    (backward shift for β)
```

The implementation's diff[2] and diff[3] match Δ_μ and Δ_β respectively. However, diff[1] = w_α + w_μ, while Δ_α = w_β + w_μ. These agree only when w_α = w_β (the two swapped regions have equal width). When w_α ≠ w_β, the implementation's diff[1] is incorrect by w_β − w_α. The effect is that region α lands at position c₂ (start of β's original location) rather than at c₀ + w_β + w_μ (the correct destination after β and μ). This produces overlapping or gapped V-regions within the POOM — a collision between the displaced α crums and the displaced μ crums — violating arrangement functionality (S2, ASN-0036).

The discrepancy arises because the code computes diff[3] = −diff[1] (negating diff[1] by sign-flip [edit.c:175–176]), enforcing a symmetry (Δ_α = −Δ_β) that holds only when w_α = w_β. The correct computation would derive diff[1] and diff[3] independently: diff[1] = c₃ − c₁ = w_β + w_μ and diff[3] = −(c₂ − c₀) = −(w_α + w_μ).

**No subspace guard.** The `rearrangend` function [edit.c:78] applies `tumbleradd` to V-displacements without checking whether the result remains in the original subspace. A pivot with cuts spanning the text subspace (1.x) and link subspace (2.x) boundary would relocate POOM entries across subspaces — text content could end up at link V-positions, or vice versa. This violates the subspace convention but produces no crash. The abstract specification avoids this through R-PRE(vi), which requires subspace confinement as a precondition. The precondition is not enforced by the implementation; it must be maintained by the caller.

**Out-of-range cuts produce a silent no-op.** When all cut points fall outside the document's V-span, every POOM crum is classified into the exterior (section 0 or section 4), which receives zero displacement. The function completes without error, having made no changes. When some cuts are in-range and others are out-of-range, the in-range portion proceeds while the out-of-range blade values are fed into the offset arithmetic, potentially producing invalid displacements. The abstract specification avoids this through R-PRE(iv), which requires the entire affected range to lie within the current arrangement.

**Tree rebalancing after displacement.** After applying offsets, `rearrangend` calls `recombine(fullcrumptr)` [edit.c:139] and `splitcrumupwards(fullcrumptr)` [edit.c:141] to rebalance the POOM tree. The `recombine` pass sorts siblings by diagonal sum (V + I displacement) and merges under-full nodes. This changes the tree shape but not the abstract mapping — `incontextlistnd` [context.c:75] performs insertion-sort by V-address on retrieval results, guaranteeing correct ordering regardless of the internal tree structure. Confluence is preserved: the same abstract arrangement M'(d) is represented regardless of the tree's shape.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R-PRE | Precondition: d ∈ E_doc, V_S(d) ≠ ∅, valid cut sequence, affected range ⊆ V_S(d), non-empty regions, subspace confinement | introduced |
| R-EXT | (A v : v < c₀ ∨ v ≥ c_{n−1} : M'(d)(v) = M(d)(v)) — exterior unchanged | introduced |
| R-P1 | (A j : 0 ≤ j < w_β : M'(d)(c₀ + j) = M(d)(c₁ + j)) — pivot: β content to start | introduced |
| R-P2 | (A j : 0 ≤ j < w_α : M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)) — pivot: α content to end | introduced |
| R-S1 | (A j : 0 ≤ j < w_β : M'(d)(c₀ + j) = M(d)(c₂ + j)) — swap: β content to start | introduced |
| R-S2 | (A j : 0 ≤ j < w_μ : M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)) — swap: μ content to middle | introduced |
| R-S3 | (A j : 0 ≤ j < w_α : M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)) — swap: α content to end | introduced |
| R-PIV | Pivot postcondition is a total function on V_S(d) | introduced |
| R-PPERM | Bijection π for 3-cut pivot: α shifts forward by w_β, β shifts backward by w_α | introduced |
| R-SWP | Swap postcondition is a total function on V_S(d) | introduced |
| R-SPERM | Bijection π for 4-cut swap: α shifts forward by w_β + w_μ, μ shifts by w_β − w_α, β shifts backward by w_α + w_μ | introduced |
| R-CP | ran(M'(d)) = ran(M(d)) — content preservation as multiset equality | introduced |
| R-CF | C' = C, E' = E, R' = R — frame conditions | introduced |
| R-XD | (A d' ≠ d : M'(d') = M(d')) — cross-document isolation | introduced |
| R-XS | (A v : subspace(v) ≠ S : M'(d)(v) = M(d)(v)) — subspace confinement | introduced |
| R-IID | d ∈ E'_doc — document identity preserved | introduced |
| R-KMU | K.μ~ preconditions satisfied: π maps dom(M(d)) to itself, S8a and S8-depth inherited | introduced |
| R-S2P | S2 preserved: postcondition defines a total function on V_S(d) | introduced |
| R-S3P | S3 preserved: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C') | introduced |
| R-S8P | S8a, S8-depth, S8-fin preserved: dom(M'(d)) = dom(M(d)) | introduced |
| R-DP | REARRANGE preserves D-CTG (V-position contiguity) | introduced |
| R-WR | \|V_S'(d)\| = \|V_S(d)\| — extent size preserved | introduced |
| R-BLK | Block decomposition transforms by split-at-cuts then displace-per-region, preserving B1–B3 | introduced |
| R-LS | Link survivability: links reference I-addresses, which are invariant under rearrangement | introduced |


## Open Questions

Does the 4-cut swap definition generalize to k-cut rearrangements for k > 4, and if so, what is the natural class of permutations that "rearrangement by cut points" can express?

What must a well-formed editing sequence guarantee about the composition of multiple rearrangements — is the composition of two rearrangements always expressible as a single rearrangement, or can sequences of rearrangements produce arrangements unreachable by any single operation?

Under what conditions can a rearrangement cause the number of mapping blocks in the canonical decomposition to increase, and is there an upper bound on the increase relative to the number of cut points?

The depth-2 restriction (R-PRE clause iv, #v = 2) is a presentational simplification, not a technical limitation: D-CTG-depth (ASN-0036) proves that for depth m ≥ 3, all positions in V_S(d) share components 2 through m − 1, and D-SEQ gives V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}. The displacement arithmetic depends only on the last component, so generalization to arbitrary depth is immediate.

What must a front-end guarantee when rendering a link endset that has been split across non-adjacent V-regions by rearrangement — must both regions be presented as a single logical selection, or may they be rendered independently?

What abstract property must a document-discovery index satisfy to remain correct after rearrangement, given that the spanfilade is not updated and the I-address set is invariant?

What constraints, if any, must cut points satisfy relative to the mapping block boundaries of the canonical decomposition, or are arbitrary cut positions within the V-span always valid?
