# ASN-0081: Span Algebra 1

*2026-04-09*

This ASN extends the span algebra (ASN-0053) with ordinal extraction functions and ordinal contraction properties. When a contiguous span of V-positions is removed from a subspace arrangement and the surviving right-region positions shift left to close the gap, the resulting shift function has three fundamental properties: it preserves I-address mappings at shifted positions (D-SHIFT), it is order-preserving and injective (D-BJ), and it closes the gap exactly at the contraction point with no overlap and no residual gap (D-SEP, D-DP). The ordinal extraction and reconstruction functions separate subspace structure from within-subspace arithmetic, enabling the shift to be expressed as pure tumbler subtraction on ordinals.


## Foundation Citations

The following ASN-0036 properties are cited throughout. We use short labels for readability; each references the canonical statement in ASN-0036.

- **S8-depth** (FixedDepthVPositions): all V-positions within a subspace share the same tumbler depth — `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`.
- **S8a** (VPositionWellFormedness): V-positions are zero-free and positive — `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`. In particular, every component of every V-position is strictly positive.
- **D-CTG** (VContiguity): within subspace S, V_S(d) is order-contiguous — `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`.


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

We work with V-positions within a subspace of a document's arrangement. Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions to I-addresses. Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**Scoping axiom.** Throughout this ASN, V-positions have depth #p = 2 (ordinal depth 1). This restricts the analysis to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially. Generalization to deeper ordinals is noted as an open question.

A contraction takes a document d, a subspace S, and a contraction span (p, w) specifying the contiguous range of V-positions to remove. Let r = p ⊕ w denote the right cut point — the exclusive upper bound of the contraction.

**Contraction formal contract.**

*Preconditions:*

- `p ∈ V_S(d)` — p is a current V-position in subspace S of document d.
- `w > 0` — the contraction width is positive.
- `#w = #p` — the displacement has the same depth as p.
- `w₁ = 0` — the displacement preserves the subspace identifier under addition.
- `#p = 2` (scoping axiom) — V-positions have depth 2, restricting to single-component ordinals.
- Containment: with D-SEQ giving `V_S(d) = {[S, k] : 1 ≤ k ≤ N}`, the condition `p₂ + w₂ − 1 ≤ N` — the contraction span lies entirely within the current arrangement.

The contraction span (p, w) partitions V_S(d) into three disjoint, exhaustive regions.

**Definition — ThreeRegions.**

```
L = {v ∈ V_S(d) : v < p}            — left of contraction
X = {v ∈ V_S(d) : p ≤ v < r}        — the contracted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of contraction
```

By trichotomy of the total order (T1, ASN-0034), every v ∈ V_S(d) falls in exactly one region. Define Q₃ = {σ(v) : v ∈ R} as the set of shifted right-region positions, where σ is defined in D-SHIFT below. The post-state arrangement M'(d) is the arrangement after the contraction has been applied.


## Right Shift

**D-SHIFT** — *RightShift* (POST, postcondition). Every position in the right region survives with its I-address mapping intact, but its V-position shifts left by w_ord. Define the shift function: for v ∈ R, let σ(v) = vpos(S, ord(v) ⊖ w_ord) — TumblerSub applied to the ordinal component, then reconstructed as a V-position.

*Preconditions:* As stated in the contraction formal contract: p ∈ V_S(d), #p = 2, w > 0, #w = #p, w₁ = 0, containment satisfied. r = p ⊕ w; R = {v ∈ V_S(d) : v ≥ r}; M'(d) is the post-contraction arrangement.

*Postconditions:*

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

The shift is well-defined. For any v ∈ R, ord(v) ≥ ord(r) = ord(p) ⊕ w_ord (since v ≥ r). The subtraction ord(v) ⊖ w_ord is well-defined by TA2 (SubtractionWellDefined, ASN-0034). At our restricted depth #p = 2: ord(v) = [vₘ] and w_ord = [c] for positive integer c, so [vₘ] ⊖ [c] = [vₘ − c] is well-defined when vₘ ≥ c, which holds since vₘ ≥ ord(r)₁ = pₘ + c. The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p) (verified in D-SEP below). Since p ∈ V_S(d) and S8a guarantees all components of every V-position are strictly positive, we have p₂ ≥ 1, hence ord(p) = [p₂] is positive. So the shifted V-position satisfies S8a.

What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap. This is the two-space separation in action: the arrangement (Vstream) is modified while the content (Istream) remains invariant. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].


## Region Postconditions

The contraction's effect on regions L and X, and on state outside subspace S and document d, must be stated explicitly.

**D-L** — *LeftPreservation* (FRAME, introduced). Positions in the left region are preserved unchanged:

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

**D-DOM** — *DomainCharacterization* (POST, introduced). The post-state arrangement within subspace S consists of exactly the preserved left region and the shifted right region:

`{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃`

Combined with D-L and D-SHIFT, this fully characterizes M'(d) within subspace S: positions in L retain their original I-address mappings, positions in Q₃ hold shifted mappings from R, and no other subspace-S positions exist in dom(M'(d)). The original X mappings are not preserved — any X address that reappears in Q₃ carries the shifted I-address from the corresponding R position, not its pre-contraction content.

**D-CS** — *CrossSubspaceFrame* (FRAME, introduced). Positions in other subspaces are unchanged:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

**D-CD** — *CrossDocumentFrame* (FRAME, introduced). Other documents are unchanged:

`(A d' ≠ d : M'(d') = M(d'))`

**D-I** — *ContentStoreFrame* (FRAME, introduced). The content store is unchanged:

`(A a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`

This is S0 (ContentImmutability, ASN-0036) applied to the contraction transition: contraction modifies only the arrangement M(d), leaving the content store invariant.


## Shift Correctness

We verify that the shift σ defined by D-SHIFT is well-behaved: order-preserving, injective, and gap-closing.

**D-BJ** — *ShiftBijectivity* (LEMMA, lemma). The map σ : R → Q₃ is an order-preserving bijection.

*Preconditions:* #p = 2 (scoping axiom); v₁, v₂ ∈ R with v₁ < v₂.

*Postconditions:* `σ(v₁) < σ(v₂)`

*Proof.* All ordinals in R share the same depth (S8-depth), giving #ord(v₁) = #ord(v₂). For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (since they share the subspace identifier, the ordering depends only on the ordinal). Both ordinals satisfy ord(v) ≥ w_ord (established above). By TA3-strict (OrderPreservationSubtractionStrict, ASN-0034) — a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord, hence σ(v₁) < σ(v₂). ∎

Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂). The shift creates no collisions.

**D-SEP** — *GapClosure* (LEMMA, lemma). The contraction width exactly bridges the ordinal distance between p and r, so shifting the right cut point back by the width recovers the ordinal of the left cut point. When R ≠ ∅, D-CTG ensures this algebraic identity has the semantic consequence that the shifted right region begins exactly where the left region ends.

*Preconditions:* #p = 2 (scoping axiom); r = p ⊕ w.

*Postconditions:*

- (a) Algebraic identity: `ord(r) ⊖ w_ord = ord(p)`.
- (b) When R ≠ ∅: by D-CTG, r = min(R) — the last element of X and some v ∈ R bracket r in V_S(d), so contiguity forces r ∈ V_S(d). Then σ(r) is well-defined and ord(σ(r)) = ord(p), i.e., min({ord(u) : u ∈ Q₃}) = ord(p).

*Proof of (a).* We need (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At our restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c]: the two sequences have equal length 1, divergence at position 1 where (p₂ + c) > c, giving r₁ = (p₂ + c) − c = p₂. Result: [p₂] = ord(p). ✓

This applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when the action point k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied.

*Proof of (b).* Suppose R ≠ ∅, so there exists v ∈ V_S(d) with v ≥ r. The last element of X (with ordinal ord(p) + c − 1) is in V_S(d), and v ∈ V_S(d) with v ≥ r > last element of X. By D-CTG, every same-subspace, same-depth position between them — including r — is in V_S(d). Hence r ∈ R and r = min(R) (since r ≤ v for all v ∈ R by definition). By D-BJ, σ is order-preserving, so σ(r) = min(Q₃). By part (a), ord(σ(r)) = ord(p). ∎

**D-DP** — *DensePartition* (LEMMA, lemma). The post-state arrangement in subspace S is exactly the union of the preserved left region and the shifted right region, with no overlap and no gap at the contraction boundary.

*Preconditions:* #p = 2 (scoping axiom); L, X, R as defined by ThreeRegions; D-L, D-DOM, D-SHIFT, D-SEP, and D-CTG hold.

*Postconditions:*

- (a) No overlap: `L ∩ Q₃ = ∅`
- (b) Boundary adjacency: when R ≠ ∅, `min({ord(u) : u ∈ Q₃}) = ord(p)`, and `(A v ∈ L : ord(v) < ord(p))`

*Proof.* Every v ∈ L satisfies v < p, hence ord(v) < ord(p) (same subspace, ordering determined by ordinal). By D-SEP(b), when R ≠ ∅ the minimum ordinal in Q₃ is ord(p), and by D-BJ every other element of Q₃ has ordinal strictly greater than ord(p). So every element of L has ordinal strictly less than ord(p) and every element of Q₃ has ordinal ≥ ord(p), giving L ∩ Q₃ = ∅.

The boundary is tight. At depth 2 with contiguous allocation (D-CTG), L contains exactly the positions with ordinals below ord(p), and Q₃ begins at ordinal ord(p) (D-SEP). The ordinals ord(p) − 1 and ord(p) are consecutive natural numbers; no ordinal falls between them. D-DOM confirms that the post-state domain in subspace S is exactly L ∪ Q₃. ∎


## Invariant Preservation

The postconditions and frame conditions above characterize the post-state arrangement. We now verify that the post-state satisfies the system invariants established in ASN-0036.

**S2-post** — *ArrangementFunctionality* (LEMMA, introduced). The post-state M'(d) is a function.

*Proof.* By D-DOM, dom(M'(d)) within subspace S is L ∪ Q₃. By D-DP(a), L ∩ Q₃ = ∅. For v ∈ L, M'(d)(v) is uniquely determined by D-L. For v ∈ Q₃, v = σ(u) for a unique u ∈ R (D-BJ, injectivity), and M'(d)(v) = M(d)(u) is uniquely determined by D-SHIFT and S2 on the pre-state. Since the two regions are disjoint and each assigns a unique value, M'(d) is a function within subspace S. By D-CS, positions in other subspaces retain their pre-state mappings, functional by S2 on the pre-state. ∎

**S3-post** — *ReferentialIntegrity* (LEMMA, introduced). The post-state satisfies `ran(M'(d)) ⊆ dom(Σ'.C)`.

*Proof.* Every I-address in ran(M'(d)) was an I-address in ran(M(d)): positions in L map to the same I-addresses as before (D-L), and positions in Q₃ map to I-addresses from R (D-SHIFT). By S3 on the pre-state, ran(M(d)) ⊆ dom(Σ.C). By D-I (content store frame), dom(Σ.C) ⊆ dom(Σ'.C). Hence ran(M'(d)) ⊆ dom(Σ'.C). ∎

**D-CTG-post** — *VContiguityPreservation* (LEMMA, introduced). The post-state V_S(d) is contiguous.

*Proof.* By D-SEQ, the pre-state V_S(d) = {[S, k] : 1 ≤ k ≤ N}. L consists of positions with ordinals strictly less than ord(p) — by D-CTG on the pre-state, L = {[S, k] : 1 ≤ k < p₂}, which is contiguous. Q₃ is the order-preserving image of R under σ (D-BJ). R = {[S, k] : p₂ + c ≤ k ≤ N} is contiguous, and σ shifts each ordinal by −c, giving Q₃ = {[S, k − c] : p₂ + c ≤ k ≤ N} = {[S, k] : p₂ ≤ k ≤ N − c}. This is contiguous. At the boundary, L's maximum ordinal is p₂ − 1 and Q₃'s minimum ordinal is p₂ (D-SEP(b)), which are adjacent. When L = ∅, Q₃ alone is contiguous. When R = ∅, L alone is contiguous. In all cases, L ∪ Q₃ is contiguous. ∎

**D-MIN-post** — *VMinimumPreservation* (LEMMA, introduced). The post-state minimum V-position in subspace S is [S, 1, ..., 1].

*Proof.* Two cases. When L ≠ ∅: the pre-state minimum is min(V_S(d)) = [S, 1] (D-MIN). Since p > min(V_S(d)), we have min(V_S(d)) ∈ L. D-L preserves it, so min(L ∪ Q₃) = [S, 1]. When L = ∅: p = min(V_S(d)) = [S, 1] by D-MIN, so ord(p) = [1]. By D-SEP(b), min Q₃ has ordinal ord(p) = [1], giving min Q₃ = [S, 1]. ∎


## Worked Example

We verify the postconditions against a concrete scenario. Consider document d with subspace S = 1 and five contiguous V-positions:

M(d) = {[1,1] → i₁,  [1,2] → i₂,  [1,3] → i₃,  [1,4] → i₄,  [1,5] → i₅}

Contract at p = [1,2] with w = [0,2], so c = 2 and r = p ⊕ w = [1,4].

**Three-region partition.** L = {[1,1]}, X = {[1,2], [1,3]}, R = {[1,4], [1,5]}.

**Shift computation.** w_ord = [2]. For each v ∈ R:

- σ([1,4]) = vpos(1, [4] ⊖ [2]) = vpos(1, [2]) = [1,2]
- σ([1,5]) = vpos(1, [5] ⊖ [2]) = vpos(1, [3]) = [1,3]

Q₃ = {[1,2], [1,3]}.

**Post-state.** M'(d) = {[1,1] → i₁,  [1,2] → i₄,  [1,3] → i₅}

**Verification:**

- *D-L:* M'(d)([1,1]) = i₁ = M(d)([1,1]). ✓
- *D-SHIFT:* M'(d)([1,2]) = i₄ = M(d)([1,4]); M'(d)([1,3]) = i₅ = M(d)([1,5]). ✓
- *D-DOM:* {v ∈ dom(M'(d)) : subspace(v) = 1} = {[1,1], [1,2], [1,3]} = L ∪ Q₃. ✓
- *D-BJ:* [1,4] < [1,5] and σ([1,4]) = [1,2] < [1,3] = σ([1,5]). ✓
- *D-SEP:* ord(r) ⊖ w_ord = [4] ⊖ [2] = [2] = ord(p). ✓
- *D-DP:* L ∩ Q₃ = ∅; min Q₃ ordinal = [2] = ord(p); all L ordinals < ord(p). ✓

We observe that addresses [1,2] and [1,3] appear in both X and Q₃ but with different I-address mappings: M(d)([1,2]) = i₂ whereas M'(d)([1,2]) = i₄. The addresses are reused by the shift — D-DOM characterizes this correctly, where the former D-X ("positions in X are absent from dom(M'(d))") would have been contradicted.

**Boundary case: L = ∅.** Consider the same five-position arrangement but with contraction at the beginning: p = [1,1], w = [0,2], so c = 2 and r = p ⊕ w = [1,3].

**Three-region partition.** L = ∅, X = {[1,1], [1,2]}, R = {[1,3], [1,4], [1,5]}.

**Shift computation.** w_ord = [2]. For each v ∈ R:

- σ([1,3]) = vpos(1, [3] ⊖ [2]) = vpos(1, [1]) = [1,1]
- σ([1,4]) = vpos(1, [4] ⊖ [2]) = vpos(1, [2]) = [1,2]
- σ([1,5]) = vpos(1, [5] ⊖ [2]) = vpos(1, [3]) = [1,3]

Q₃ = {[1,1], [1,2], [1,3]}.

**Post-state.** M'(d) = {[1,1] → i₃,  [1,2] → i₄,  [1,3] → i₅}

**Verification:**

- *D-L:* L = ∅, vacuously satisfied. ✓
- *D-SHIFT:* M'(d)([1,1]) = i₃ = M(d)([1,3]); M'(d)([1,2]) = i₄ = M(d)([1,4]); M'(d)([1,3]) = i₅ = M(d)([1,5]). ✓
- *D-DOM:* {v ∈ dom(M'(d)) : subspace(v) = 1} = {[1,1], [1,2], [1,3]} = ∅ ∪ Q₃ = Q₃. ✓
- *D-BJ:* [1,3] < [1,4] < [1,5] and σ([1,3]) = [1,1] < [1,2] = σ([1,4]) < [1,3] = σ([1,5]). ✓
- *D-SEP(a):* ord([1,3]) ⊖ [2] = [3] ⊖ [2] = [1] = ord([1,1]) = ord(p). ✓
- *D-SEP(b):* min Q₃ = [1,1], ord([1,1]) = [1] = ord(p). ✓
- *D-DP:* L ∩ Q₃ = ∅ (L = ∅). ✓
- *D-MIN-post:* min Q₃ = [1,1] = [S, 1]. ✓
- *S2-post:* Three distinct V-positions, each assigned a unique I-address. ✓
- *S3-post:* {i₃, i₄, i₅} ⊆ ran(M(d)) ⊆ dom(Σ.C) (S3) ⊆ dom(Σ'.C) (D-I). ✓
- *D-CTG-post:* {[1,1], [1,2], [1,3]} = {[1,k] : 1 ≤ k ≤ 3}, contiguous. ✓


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ord(v) | DEF | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier | introduced |
| vpos(S, o) | DEF | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord | introduced |
| w_ord | DEF | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0 | introduced |
| D-L | frame | (A v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| D-DOM | postcondition | {v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃ | introduced |
| D-CS | frame | Cross-subspace positions unchanged | introduced |
| D-CD | frame | Cross-document arrangements unchanged | introduced |
| D-I | frame | (A a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)) — content store unchanged | introduced |
| D-SHIFT | postcondition | (A v ∈ R : M'(d)(σ(v)) = M(d)(v)) where σ(v) = vpos(S, ord(v) ⊖ w_ord) | introduced |
| D-BJ | lemma | σ is order-preserving and injective on R | introduced |
| D-SEP | lemma | ord(r) ⊖ w_ord = ord(p); when R ≠ ∅, min Q₃ ordinal = ord(p) | introduced |
| D-DP | lemma | L ∩ Q₃ = ∅ and no residual gap at contraction boundary | introduced |
| S2-post | lemma | Post-state M'(d) is a function | introduced |
| S3-post | lemma | Post-state ran(M'(d)) ⊆ dom(Σ'.C) | introduced |
| D-CTG-post | lemma | Post-state V_S(d) is contiguous | introduced |
| D-MIN-post | lemma | Post-state min V_S(d) = [S, 1, ..., 1] | introduced |


## Open Questions

- Can the gap-closure formula (D-SEP) and dense partition (D-DP) be generalized to ordinals of depth greater than one while preserving the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment?
