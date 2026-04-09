# ASN-0081: Span Algebra 1

*2026-04-09*

This ASN extends the span algebra (ASN-0053) with ordinal extraction functions and ordinal contraction properties. When a contiguous span of V-positions is removed from a subspace arrangement and the surviving right-region positions shift left to close the gap, the resulting shift function has three fundamental properties: it preserves I-address mappings at shifted positions (D-SHIFT), it is order-preserving and injective (D-BJ), and it closes the gap exactly at the contraction point with no overlap and no residual gap (D-SEP). The ordinal extraction and reconstruction functions separate subspace structure from within-subspace arithmetic, enabling the shift to be expressed as pure tumbler subtraction on ordinals.


## Ordinal Extraction

We frequently need to separate a V-position into its subspace identifier and its ordinal within that subspace. Per the ordinal-only formulation of TA7a (ASN-0034), we define the extraction and reconstruction functions.

**Definition — OrdinalExtraction.** For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier.

**Definition — VPositionReconstruction.** For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

**Definition — OrdinalDisplacementProjection.** For a V-depth displacement w with w₁ = 0 and #w = m, the *ordinal displacement* is:

`w_ord = [w₂, ..., wₘ]`

of depth m − 1. At the restricted depth m = 2 (see D-SHIFT below), w = [0, c] for positive integer c, and w_ord = [c].


## Contraction Setup

We work with V-positions within a subspace of a document's arrangement. Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d, where M(d) is the document's arrangement function. All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036).

A contraction takes a document d, a subspace S, and a contraction span (p, w) specifying the contiguous range of V-positions to remove. Here p is a V-position in subspace S with #p = 2 (depth-2 V-positions, ordinal depth 1), and w is a positive displacement of the same depth as p with w₁ = 0 (preserving the subspace identifier under addition). The contraction span lies entirely within the current arrangement. Let r = p ⊕ w denote the right cut point — the exclusive upper bound of the contraction.

The contraction span (p, w) partitions V_S(d) into three disjoint, exhaustive regions.

**Definition — ThreeRegions.**

```
L = {v ∈ V_S(d) : v < p}            — left of contraction
X = {v ∈ V_S(d) : p ≤ v < r}        — the contracted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of contraction
```

By trichotomy of the total order (T1, ASN-0034), every v ∈ V_S(d) falls in exactly one region. Define Q₃ = {σ(v) : v ∈ R} as the set of shifted right-region positions, where σ is defined in D-SHIFT below. The post-state arrangement M'(d) is the arrangement after the contraction has been applied.


## Right Shift

**D-SHIFT** — *RightShift* (POST, postcondition). Every position in the right region survives with its I-address mapping intact, but its V-position shifts left by w_ord. Define the shift function: for v ∈ R, let σ(v) = vpos(S, ord(v) ⊖ w_ord) — TumblerSub applied to the ordinal component, then reconstructed as a V-position. Then:

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

The shift is well-defined. For any v ∈ R, ord(v) ≥ ord(r) = ord(p) ⊕ w_ord (since v ≥ r). The subtraction ord(v) ⊖ w_ord is well-defined by TA2 (SubtractionWellDefined, ASN-0034). At our restricted depth #p = 2: ord(v) = [vₘ] and w_ord = [c] for positive integer c, so [vₘ] ⊖ [c] = [vₘ − c] is well-defined when vₘ ≥ c, which holds since vₘ ≥ ord(r)₁ = pₘ + c. The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p) (verified in D-SEP below), which is positive by S8a (ASN-0036). So the shifted V-position satisfies S8a.

What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap. This is the two-space separation in action: the arrangement (Vstream) is modified while the content (Istream) remains invariant. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].


## Shift Correctness

We verify that the shift σ defined by D-SHIFT is well-behaved: order-preserving, injective, and gap-closing.

**D-BJ** — *ShiftBijectivity* (LEMMA, lemma). The map σ : R → Q₃ is an order-preserving bijection:

`(A v₁, v₂ ∈ R : v₁ < v₂ ⟹ σ(v₁) < σ(v₂))`

*Proof.* All ordinals in R share the same depth (S8-depth). For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (since they share the subspace identifier, the ordering depends only on the ordinal). Both ordinals satisfy ord(v) ≥ w_ord (established above). By TA3-strict (OrderPreservationSubtractionStrict, ASN-0034) — a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord, hence σ(v₁) < σ(v₂). ∎

Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂). The shift creates no collisions.

**D-SEP** — *GapClosure* (LEMMA, lemma). The shifted right-region positions abut the left-region positions with no gap and no overlap. Specifically, the minimum shifted ordinal equals ord(p):

`σ(r) has ordinal ord(r) ⊖ w_ord = ord(p)`

*Proof.* We need (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At our restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c]: the two sequences have equal length 1, divergence at position 1 where (p₂ + c) > c, giving r₁ = (p₂ + c) − c = p₂. Result: [p₂] = ord(p). ✓

This applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when the action point k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied. ∎

**Consequence.** The left region L has V-positions with ordinals less than ord(p). The shifted right region Q₃ has V-positions with ordinals from ord(p) onward (by D-SEP) through ord(v_max) ⊖ w_ord. The gap closes exactly at p: the left region ends just before ord(p), and the shifted right region begins at ord(p). No overlap (since L < p ≤ Q₃) and no residual gap.


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ord(v) | DEF | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier | introduced |
| vpos(S, o) | DEF | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord | introduced |
| w_ord | DEF | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0 | introduced |
| D-SHIFT | POST | (A v ∈ R : M'(d)(σ(v)) = M(d)(v)) where σ(v) = vpos(S, ord(v) ⊖ w_ord) | introduced |
| D-BJ | LEMMA | σ is order-preserving and injective on R | introduced |
| D-SEP | LEMMA | σ(r) has ordinal ord(p) — gap closes exactly at the deletion point | introduced |


## Open Questions

Can the gap-closure formula (D-SEP) and contiguity preservation (D-DP) be generalized to ordinals of depth greater than one while preserving the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment?
