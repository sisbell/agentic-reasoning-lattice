# ASN-0061: DELETE Operation

*2026-03-21*

We are looking for the precise postcondition of DELETE — the operation that removes content from a document's current arrangement. In a system where the content store is append-only (S0, ASN-0036) and every allocated address is permanent (T8, ASN-0034), "deletion" cannot mean destruction. What it means — what it must mean — is removal of the arrangement mapping: the V-positions that referenced the content are excised from the document's Vstream, and the surviving positions close the gap. The content itself persists in permanent storage. Nelson makes this absolute: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].

The task before us is to say exactly what "closing the gap" requires, what the operation preserves, and what the system looks like after the gap has closed.

We work with system state Σ = (C, E, M, R) per ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The content store is append-only (S0, P0). The arrangement M(d) is the mutable layer. DELETE must specify exactly how it contracts M(d) while respecting C's immutability.


## Arrangement Contiguity

Before we can specify DELETE, we must name the invariant DELETE must preserve. Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100. DELETE removes addresses (closing the gap)."

We formalize this as a contiguity predicate on V-positions within a subspace. Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036).

**D-CTG — VContiguity (DESIGN).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

D-CTG is a design constraint on well-formed document states, not a reachable-state invariant in the ASN-0047 sense (it does not appear in the ReachableStateInvariants theorem). It further restricts which composite transitions constitute well-formed editing operations, beyond ASN-0047's validity predicate. We verify the base case: in Σ₀, V_S(d) = ∅ for all d and S (since M₀(d) = ∅ by InitialState, ASN-0047), so D-CTG holds vacuously. Note that bare K.μ⁻ — a valid elementary transition under ASN-0047 — can violate D-CTG by removing a single interior V-position; D-CTG is therefore not preserved by all valid composites, only by those that constitute well-formed editing operations.

We treat D-CTG as a precondition that DELETE both assumes and preserves. Whether INSERT, COPY, and REARRANGE also preserve D-CTG is a separate verification obligation for each operation's ASN.


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

of depth m − 1. At the restricted depth m = 2 (see D-PRE(iv) below), w = [0, c] for positive integer c, and w_ord = [c].


## Precondition

DELETE takes three arguments: a document d, a subspace S, and a deletion span (p, w) specifying the contiguous range of V-positions to remove. Here p is a V-position in subspace S, and w is a positive displacement of the same depth as p (per TA7a, ASN-0034) with w₁ = 0 (preserving the subspace identifier under addition). The ordinal displacement w_ord = [w₂, ..., w_{#w}] encodes the count of positions to delete.

The span is arbitrary — it need not align with any boundaries of how content was originally contributed. Nelson is explicit: V-positions are addressed "regardless of their native origin" [LM 4/11]; a deletion can excise the middle of a correspondence run, split a mapping block, or remove the entire document's content in one operation.

**D-PRE — DeletePrecondition (PRE).**

(i) d ∈ E_doc (the document exists).

(ii) w > 0 (positive deletion width — one cannot delete nothing).

(iii) subspace(p) = S where S ≥ 1 (text subspace; link-subspace deletion follows the same structure but we derive text-subspace first).

(iv) #p = 2 (depth-2 V-positions, ordinal depth 1). All proofs in this ASN — including the round-trip property D-SEP and the contiguity preservation D-DP — rely on properties of depth-1 ordinals (single natural numbers). Generalization to deeper ordinals is noted as an open question.

(v) The deletion span lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = #p ∧ p ≤ v < p ⊕ w : v ∈ V_S(d))`

Every V-position of the correct depth within the deletion range must currently exist in d's subspace-S arrangement. We use a depth-restricted membership predicate rather than span denotation (ASN-0053), because ⟦(p, w)⟧ includes tumblers at all depths between p and p ⊕ w (by T0(b) and T5, ASN-0034), while V_S(d) contains only tumblers of fixed depth #p (by S8-depth, ASN-0036). Attempting to delete non-existent positions is undefined.

(vi) #w = #p (the displacement has the same depth as the V-position). This ensures the action point of w satisfies TA0 (AdditionWellDefined, ASN-0034) for p ⊕ w.

(vii) w₁ = 0 (the displacement preserves the subspace identifier). Under TumblerAdd, r₁ = p₁ + w₁; without w₁ = 0, the result p ⊕ w would have subspace identifier p₁ + w₁ ≠ S, violating subspace confinement.

When V_S(d) is contiguous (D-CTG), the precondition (v) reduces to a bound on the span endpoints. Let v_min and v_max be the minimum and maximum of V_S(d). Then (v) requires p ≥ v_min and p ⊕ w ≤ shift(v_max, 1) — the deletion starts within the extent and ends at or before the first position past the extent.


## The Three-Region Partition

The deletion span (p, w) partitions V_S(d) into three disjoint, exhaustive regions. Let r = p ⊕ w denote the right cut point — the exclusive upper bound of the deletion.

**Definition — ThreeRegions.**

```
L = {v ∈ V_S(d) : v < p}            — left of deletion
X = {v ∈ V_S(d) : p ≤ v < r}        — the deleted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of deletion
```

By trichotomy of the total order (T1, ASN-0034), every v ∈ V_S(d) falls in exactly one region. These are pairwise disjoint: L ∩ X = ∅ because v < p ∧ v ≥ p is impossible; X ∩ R = ∅ because v < r ∧ v ≥ r is impossible; L ∩ R = ∅ because v < p ∧ v ≥ r with p < r (from w > 0 and TA-strict, ASN-0034) yields v < p ≤ v, a contradiction. Exhaustiveness: L ∪ X ∪ R = V_S(d).

By D-PRE(v), every V-position of depth #p in the range [p, r) belongs to V_S(d), so X includes at least p itself (since p < r by TA-strict, ASN-0034, and p ∈ V_S(d) by D-PRE(v)). Thus |X| ≥ 1.

L or R may be empty. L = ∅ when p = v_min (deletion starts at the first position). R = ∅ when r = shift(v_max, 1) (deletion extends through the last position). Both empty simultaneously means the entire subspace content is deleted: X = V_S(d).


## Effect on the Arrangement

We can now state what DELETE does. The specification has three components corresponding to the three regions, plus frame conditions for what the operation does not change.

**D-LEFT — LeftInvariance (POST).** Every position in the left region is unchanged — same V-position, same I-address:

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

Neither the V-position nor the I-address changes. Content before the deletion point reads exactly as before, at exactly the same V-position. Nelson says the Vstream "closes the gap" — content before the gap is untouched.

**D-DOM — PostStateDomain (POST).** The post-state domain of M'(d) in subspace S is exactly L ∪ Q₃:

`dom(M'(d)) ∩ {v : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}`

where Q₃ = {σ(v) : v ∈ R} is the set of shifted right-region positions (defined in D-SHIFT below). The original mappings at positions in X are discarded: no position in X retains its pre-state mapping. When R ≠ ∅, the shifted right-region positions begin at ordinal ord(p) (by D-SEP below), so some V-positions in X are reoccupied by shifted content — but the I-address at each reoccupied position comes from D-SHIFT, not from the pre-state mapping at that position. The I-addresses formerly referenced from X are not destroyed — they remain in dom(C) by P0 (ContentPermanence, ASN-0047) — but the arrangement no longer points to them from these V-positions. Nelson's diagram on page 4/9 explicitly names this state: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)."

**D-SHIFT — RightShift (POST).** Every position in the right region survives with its I-address mapping intact, but its V-position shifts left by w_ord. Define the shift function: for v ∈ R, let σ(v) = vpos(S, ord(v) ⊖ w_ord) — TumblerSub applied to the ordinal component, then reconstructed as a V-position. Then:

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

The shift is well-defined. For any v ∈ R, ord(v) ≥ ord(r) = ord(p) ⊕ w_ord (since v ≥ r). The subtraction ord(v) ⊖ w_ord is well-defined by TA2 (SubtractionWellDefined, ASN-0034). At our restricted depth #p = 2: ord(v) = [vₘ] and w_ord = [c] for positive integer c, so [vₘ] ⊖ [c] = [vₘ − c] is well-defined when vₘ ≥ c, which holds since vₘ ≥ ord(r)₁ = pₘ + c. The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p) (verified in D-SEP below), which is positive by S8a (ASN-0036). So the shifted V-position satisfies S8a.

What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap. This is the two-space separation in action: the arrangement (Vstream) is modified while the content (Istream) remains invariant. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].


## Frame Conditions

The specification is incomplete without stating what DELETE does *not* change. The frame is as important as the effect.

**D-CF — ContentFrame (FRAME).**

`C' = C  ∧  E' = E  ∧  R' = R`

DELETE does not allocate or modify content (C' = C). DELETE does not create or destroy entities (E' = E). DELETE does not record new provenance (R' = R). These equalities are verified in the composite transition decomposition below: both K.μ⁻ and K.μ⁺ have C' = C and E' = E as elementary frame conditions (ASN-0047), and the provenance frame R' = R follows from the K.μ⁻ frame together with the K.μ⁺ frame, with J1 shown vacuous since ran(M'(d)) ⊆ ran(M(d)).

This is the sharpest distinction from INSERT, which modifies C (allocation), extends R (provenance recording), and extends M (placement). DELETE modifies M alone.

**D-XD — CrossDocumentFrame (FRAME).**

`(A d' : d' ≠ d : M'(d') = M(d'))`

DELETE on document d has no effect on any other document's arrangement. Each document's arrangement is an independent mapping over permanent content. Nelson makes this a core guarantee: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11]. The I-addresses are permanent (T8, ASN-0034). The arrangements are independent (M15, ASN-0058). Modifying one document's Vstream cannot affect another's.

**D-XS — SubspaceConfinement (FRAME).**

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

Within document d itself, subspaces other than S are completely unchanged. A deletion in the text subspace does not alter link-subspace positions, and vice versa. This follows from the subspace partitioning of V-positions (T7, ASN-0034): the three-region partition is computed within subspace S; positions in other subspaces fall into none of the three regions and are untouched.

Gregory's implementation confirms this isolation through an arithmetic mechanism: the `strongsub` exponent guard in `tumblersub` prevents cross-subspace shifts when the deletion width's action point lies below the subspace identifier's tumbler level. At the abstract level, the property follows from T7 without requiring any particular arithmetic guard — subspaces are structurally disjoint.

**D-IID — DocumentIdentity (POST).**

`d ∈ E'_doc`

The document d continues to exist after DELETE. Removal modifies the arrangement, not the entity structure. Nelson explicitly contrasts this with CREATENEWVERSION, which creates a new document identity [LM 4/66]. DELETE is "re-twisting the braid when its parts are rearranged, added or subtracted" [LM 2/15] — not cutting the braid and starting anew. "A document is really an evolving ONGOING BRAID" [LM 2/14], and DELETE is one of the ways it evolves.


### Domain Completeness

D-LEFT, D-DOM, D-SHIFT, and D-XS together determine dom(M'(d)). Let:

```
Q₁ = {v ∈ dom(M(d)) : subspace(v) ≠ S}                        (by D-XS)
Q₂ = L                                                          (by D-LEFT)
Q₃ = {σ(v) : v ∈ R}                                            (by D-SHIFT)
```

D-DOM gives dom(M'(d)) ∩ V_S = Q₂ ∪ Q₃, and D-XS gives the non-S portion Q₁, so dom(M'(d)) = Q₁ ∪ Q₂ ∪ Q₃. The ⊆ direction — that dom(M'(d)) contains no other positions — follows from the composite transition structure established below: step (i) removes the deleted and right-region positions, step (ii) reintroduces the right-region positions at shifted locations. No other step modifies M(d). Therefore |dom(M'(d))| = |dom(M(d))| − |X|.

We verify that Q₁ through Q₃ are pairwise disjoint. Q₁ is disjoint from Q₂ and Q₃ by subspace. Q₂ has positions < p. Q₃ has positions σ(v) with ord(σ(v)) ≥ ord(p) (by D-SEP below). Since Q₂ ⊂ V_S(d) with ordinals < ord(p), and Q₃ ⊂ V_S with ordinals ≥ ord(p), they are disjoint.


## Shift Correctness

We verify that the shift σ defined by D-SHIFT is well-behaved: order-preserving, injective, and gap-closing.

**D-BJ — ShiftBijectivity (LEMMA).** The map σ : R → Q₃ is an order-preserving bijection:

`(A v₁, v₂ ∈ R : v₁ < v₂ ⟹ σ(v₁) < σ(v₂))`

*Proof.* All ordinals in R share the same depth (S8-depth). For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (since they share the subspace identifier, the ordering depends only on the ordinal). Both ordinals satisfy ord(v) ≥ w_ord (established above). By TA3-strict (OrderPreservationSubtractionStrict, ASN-0034) — a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord, hence σ(v₁) < σ(v₂). ∎

Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂). The shift creates no collisions.

**D-SEP — GapClosure (LEMMA).** The shifted right-region positions abut the left-region positions with no gap and no overlap. Specifically, the minimum shifted ordinal equals ord(p):

`σ(r) has ordinal ord(r) ⊖ w_ord = ord(p)`

*Proof.* We need (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At our restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c]: the two sequences have equal length 1, divergence at position 1 where (p₂ + c) > c, giving r₁ = (p₂ + c) − c = p₂. Result: [p₂] = ord(p). ✓

This applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when the action point k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied. ∎

**Consequence.** The left region L has V-positions with ordinals less than ord(p). The shifted right region Q₃ has V-positions with ordinals from ord(p) onward (by D-SEP) through ord(v_max) ⊖ w_ord. The gap closes exactly at p: the left region ends just before ord(p), and the shifted right region begins at ord(p). No overlap (since L < p ≤ Q₃) and no residual gap.


## Contiguity Preservation

The central correctness property: DELETE preserves the contiguity invariant.

**D-DP — ContiguityPreservation (LEMMA).** If D-CTG holds in state Σ, and DELETE(d, S, p, w) satisfies D-PRE, then D-CTG holds in successor state Σ'.

*Proof.* We must show that V_S'(d) — the post-deletion V-positions in subspace S — is either empty or occupies every intermediate position between its extremes.

**Case 1: L = ∅ and R = ∅.** Then X = V_S(d) — the entire content is deleted. After DELETE, V_S'(d) = ∅. D-CTG holds vacuously.

**Case 2: L = ∅ and R ≠ ∅.** The deletion starts at v_min. After DELETE, V_S'(d) = Q₃ = {σ(v) : v ∈ R}. At our restricted depth #p = 2, R occupies ordinals {a, a+1, ..., b} for some a, b (contiguous by D-CTG on the pre-state; depth-1 ordinals are natural numbers). The shift σ subtracts the constant c = w_ord₁ from each ordinal, yielding {a − c, a − c + 1, ..., b − c}. Integer subtraction by a constant preserves the unit gap between consecutive ordinals, so Q₃ is contiguous. ✓

**Case 3: L ≠ ∅ and R ≠ ∅.** The left region L is contiguous (D-CTG on the pre-state, restricted to positions below p). The shifted right region Q₃ is contiguous (same depth-1 argument as Case 2). The two are adjacent: max(L) has ordinal ord(p) − 1 (the immediate predecessor of p in V_S(d), which exists because L ≠ ∅ and D-CTG ensures contiguity), and min(Q₃) has ordinal ord(p) (by D-SEP). Since ord(p) − 1 and ord(p) are consecutive natural numbers, L and Q₃ are adjacent with no gap and no overlap. The union L ∪ Q₃ is therefore contiguous.

**Case 4: L ≠ ∅ and R = ∅.** V_S'(d) = L, which is contiguous by D-CTG restricted to positions below p. ∎

**D-WR — WidthReduction (COROLLARY).** The extent of M_S(d) decreases by exactly the deletion width:

`|V_S'(d)| = |V_S(d)| − |X|`

Since |L| + |X| + |R| = |V_S(d)| and |V_S'(d)| = |L| + |R| (positions in L survive unchanged, positions in R are shifted bijectively), we have |V_S'(d)| = |V_S(d)| − |X|. ∎


## DELETE as Composite Transition

We verify that DELETE decomposes into the elementary transitions of ASN-0047 and satisfies the coupling constraints.

The composite Σ → Σ' consists of one or two elementary steps, depending on whether the right region R is empty.

(i) *Arrangement contraction* — K.μ⁻ on document d: remove all V-positions in X ∪ R from M_S(d), leaving only the positions in L (and all positions in other subspaces). Precondition: d ∈ E_doc. Satisfied by D-PRE(i). Frame: C' = C, E' = E, R' = R (K.μ⁻ frame, ASN-0047).

(ii) *Arrangement extension* — K.μ⁺ on document d, **only when R ≠ ∅**: reintroduce the right-region content at shifted positions. K.μ⁺ requires strict domain extension (dom(M'(d)) ⊃ dom(M(d)) at the intermediate state). When R = ∅ — Cases 1 and 4 of D-DP, where the deletion extends through the last position — there are no right-region positions to reintroduce, so the strict-superset precondition cannot be met; the composite reduces to K.μ⁻ alone. When R ≠ ∅, |Q₃| ≥ 1 provides at least one new V-position. For each v ∈ R, add the mapping M'(d)(σ(v)) = M(d)(v). Precondition: each M(d)(v) ∈ dom(C') (yes — these I-addresses were already in ran(M(d)) ⊆ dom(C) by S3, and C' = C by step (i)). The new V-positions σ(v) satisfy S8a (ordinals positive, as established under D-SHIFT). The depth #σ(v) = #v (TumblerSub preserves depth at the ordinal level), satisfying S8-depth. The domain remains finite (S8-fin): |L| + |R| < |V_S(d)| which is finite. Frame: C' = C, E' = E, R' = R (K.μ⁺ frame, ASN-0047).

**Elementary preconditions at intermediate states.** Step (i) removes positions; the precondition d ∈ E_doc holds. When R ≠ ∅, step (ii) adds positions; the V-positions σ(v) must not already be in dom(M) at the intermediate state. After step (i), dom includes L (with ordinals < p) and non-S positions. The shifted positions σ(v) have ordinals ≥ ord(p) (by D-SEP). Since L has ordinals < ord(p), and σ(v) have subspace S (distinct from non-S positions), no collision occurs. ✓

**Coupling constraints (R = ∅).** The composite is K.μ⁻ alone. J0 (AllocationRequiresPlacement): dom(C') = dom(C), no new content allocated, vacuous. J1 (ExtensionRecordsProvenance): ran(M'(d)) ⊆ ran(M(d)) (contraction only removes mappings), so ran(M'(d)) \ ran(M(d)) = ∅, vacuous. J1' (ProvenanceRequiresExtension): R' = R, so R' \ R = ∅, vacuous. The composite is valid.

**Coupling constraints (R ≠ ∅).** J0 (AllocationRequiresPlacement): no new content is allocated (dom(C') = dom(C)), vacuously satisfied. J1 (ExtensionRecordsProvenance): the I-addresses reintroduced in step (ii) are new relative to the intermediate state but not new relative to the composite's initial state. J1 requires that new I-addresses in ran(M'(d)) \ ran(M(d)) — where M(d) is the composite's initial arrangement — be covered by provenance. Since ran(M'(d)) ⊆ ran(M(d)) — the right-region I-addresses were already present in the initial arrangement, and the deleted I-addresses are removed — ran(M'(d)) \ ran(M(d)) = ∅. J1 is vacuous. J1' (ProvenanceRequiresExtension): R' \ R = ∅. Vacuous.

The composite is a valid transition: DELETE preserves all coupling constraints.


## Block Decomposition Effect

We express DELETE's effect on the block decomposition of M(d) (ASN-0058). Let B be the current decomposition of the text-subspace arrangement. Since DELETE in subspace S leaves all other subspaces unchanged (D-XS), we separate B by subspace: B_S = {β ∈ B : subspace(v(β)) = S} and B_other = B \ B_S. Only B_S is affected; B_other passes through unchanged.

Partition B_S relative to the two cut points p and r = p ⊕ w. For each block β = (v, a, n) ∈ B_S, let v_end = shift(v, n). Exactly one of six conditions holds:

(a) *Entirely in L*: v_end ≤ p. Block is untouched.

(b) *Straddles the left cut only*: v < p < v_end ≤ r. Split at interior point c₁ satisfying v + c₁ = p (at ordinal depth 1, c₁ = ord(p)₁ − ord(v)₁; well-defined by M4, ASN-0058): left piece β_L = (v, a, c₁) survives in L; right piece is in X and is removed.

(c) *Entirely in X*: p ≤ v and v_end ≤ r. Block is removed.

(d) *Straddles the right cut only*: p ≤ v < r < v_end. Split at interior point c₂ satisfying v + c₂ = r (at ordinal depth 1, c₂ = ord(r)₁ − ord(v)₁): left piece is in X (removed); right piece β_R = (r, a + c₂, n − c₂) survives, with V-start shifted to σ(r).

(e) *Entirely in R*: v ≥ r. Block survives with V-start shifted: β' = (σ(v), a, n).

(f) *Straddles both cuts*: v < p and v_end > r. Two splits produce three pieces: the left survivor β_L = (v, a, c₁) where v + c₁ = p, the removed middle of width c₂ − c₁ where v + c₂ = r, and the right survivor β_R = (r, a + c₂, n − c₂) which shifts to (σ(r), a + c₂, n − c₂). This case arises when a single block spans the entire deletion interval.

**D-BLK — BlockTransformation (LEMMA).** The post-DELETE decomposition is:

`B' = B_other ∪ B_left ∪ {(σ(v_R), a_R, n_R) : (v_R, a_R, n_R) ∈ B_right}`

where B_left collects surviving left pieces from cases (a), (b), and (f), and B_right collects surviving right pieces from cases (d), (e), and (f).

*Verification of B1–B3.* Coverage (B1): B_other covers V-positions in other subspaces (D-XS). Within subspace S: B_left covers the left region (D-LEFT), shifted B_right covers the shifted right region (D-SHIFT). Disjointness (B2): B_other is disjoint from the S blocks by subspace. Within S: B_left has V-extents ending before p; shifted B_right has V-extents starting at or beyond p (by D-SEP); no overlap between B_left and shifted B_right. Within B_left: each block is a subset of an originally disjoint block from B_S, and splitting preserves disjointness (M5, ASN-0058), so B_left blocks remain pairwise disjoint. Within shifted B_right: the original right-region blocks were pairwise disjoint (B2 on the pre-state decomposition), and σ is order-preserving (D-BJ), so their shifted V-extents remain pairwise disjoint. Consistency (B3): for B_left, M'(d)(v + j) = M(d)(v + j) = a + j by D-LEFT and the original B3. For shifted B_right, we need M'(d)(σ(v) + j) = a + j. By D-SHIFT, M'(d)(σ(v + j)) = M(d)(v + j) = a + j. And σ(v) + j = σ(v + j): the ordinal of σ(v) + j is (ord(v) ⊖ w_ord) + j, and the ordinal of σ(v + j) is (ord(v) + j) ⊖ w_ord. At our restricted ordinal depth 1: [(vₘ − c) + j] = [(vₘ + j) − c] where c = w_ord₁, by commutativity and associativity of natural-number arithmetic. ∎

The key observation: **I-addresses are never modified.** Every I-address in ran(M_S(d)) either survives in M'_S(d) at a shifted V-position or is removed from the arrangement entirely. No I-address is altered, and no new I-address is introduced. The mapping blocks in B' differ from those in B only in their V-starts (shifted for the right region) and their presence (absent for the deleted region).

Gregory's implementation confirms this structure: the two-phase "cut then classify" protocol in `deletend` [edit.c:31–76] first splits crums at the blade positions via `makecutsnd` (Phase 1), then classifies each resulting crum as case 0 (left of deletion — unchanged), case 1 (within deletion — `disown` + `subtreefree`), or case 2 (right of deletion — `tumblersub` on V-displacement) (Phase 2). The abstract specification captures exactly this three-way classification.


### Worked Example

Consider document d with five text positions at V-positions [1, 1] through [1, 5], mapped to I-addresses b, b + 1, ..., b + 4. The block decomposition is B = {([1, 1], b, 5)}.

DELETE two positions starting at p = [1, 2]. Parameters: w = [0, 2] (ordinal width 2), S = 1, r = [1, 2] ⊕ [0, 2] = [1, 4].

**Three-region partition.** L = {[1, 1]}, X = {[1, 2], [1, 3]}, R = {[1, 4], [1, 5]}.

**Block split.** β = ([1, 1], b, 5) straddles the left cut: [1, 1] < [1, 2] and v_end = [1, 6] > [1, 2]. Split at c₁ = ord([1, 2]) − ord([1, 1]) = 2 − 1 = 1. β_L = ([1, 1], b, 1). The remaining piece ([1, 2], b + 1, 4) straddles the right cut: [1, 2] < [1, 4] < [1, 6]. Split at c₂ = ord([1, 4]) − ord([1, 2]) = 4 − 2 = 2. The middle piece ([1, 2], b + 1, 2) is in X — removed. The right piece ([1, 4], b + 3, 2) is in R — shifted.

**Arrangement effect:**

| V (before) | I (before) | Region | V (after) | I (after) |
|---|---|---|---|---|
| [1, 1] | b | L | [1, 1] | b |
| [1, 2] | b + 1 | X | — | — |
| [1, 3] | b + 2 | X | — | — |
| [1, 4] | b + 3 | R | [1, 2] | b + 3 |
| [1, 5] | b + 4 | R | [1, 3] | b + 4 |

Shift uses w_ord = [2] (the ordinal projection of w = [0, 2]): σ([1, 4]) = vpos(1, [4] ⊖ [2]) = vpos(1, [2]) = [1, 2]. σ([1, 5]) = vpos(1, [5] ⊖ [2]) = vpos(1, [3]) = [1, 3]. Each shifted position preserves its I-address.

**D-BLK (block decomposition).** B' = {([1, 1], b, 1), ([1, 2], b + 3, 2)}.

B1 (coverage): 3 V-positions [1, 1], [1, 2], [1, 3] partitioned among two blocks. B2 (disjointness): V-extents {[1, 1]} and {[1, 2], [1, 3]} are disjoint. B3 (consistency): first block by D-LEFT; second block: M'(d)([1, 2]) = b + 3 and M'(d)([1, 3]) = b + 4. ✓

**Contiguity preserved.** Pre-state: [1, 1]..[1, 5] contiguous. Post-state: [1, 1]..[1, 3] contiguous. D-WR: 5 − 2 = 3 positions. ✓

Note the resulting decomposition is not maximally merged — the two blocks are V-adjacent but not I-adjacent (b + 1 ≠ b + 3), so the merge condition M7 (ASN-0058) is not satisfied. This is correct: deletion can fragment what was once a single correspondence run into multiple disjoint runs, and no subsequent recombination is required.


## Invariant Preservation

We verify that DELETE preserves each foundation invariant.

**P0 (ContentPermanence, ASN-0047).** C' = C by D-CF. All prior content preserved.

**P1 (EntityPermanence).** E' = E by D-CF. All entities preserved, including d itself (D-IID).

**P8 (EntityHierarchy).** E' = E, so the predicate is unchanged.

**P2 (ProvenancePermanence).** R' = R by D-CF. R' ⊇ R. ✓

**P3 (ArrangementMutabilityOnly).** The composite uses only contraction (K.μ⁻) and extension (K.μ⁺) — the two arrangement-change modes permitted by P3(a–b). No other component admits change: C' = C, E' = E, R' = R by D-CF. ✓

**S0 (ContentImmutability, ASN-0036).** C' = C; no content entry is modified.

**S2 (ArrangementFunctionality, ASN-0036).** M'(d) is a function — each V-position maps to exactly one I-address. The three groups Q₁, Q₂, Q₃ are pairwise disjoint (verified in Domain Completeness above). Within each group: Q₁ inherits functionality from M(d) via D-XS; Q₂ inherits from M(d) via D-LEFT; Q₃ inherits from M(d) via D-SHIFT plus injectivity of σ (D-BJ).

**S3 (ReferentialIntegrity, ASN-0036).** Every I-address in ran(M'(d)) is in dom(C'). For Q₁ and Q₂: I-addresses unchanged from ran(M(d)) ⊆ dom(C) = dom(C'). For Q₃: same argument — σ changes V-positions, not I-addresses.

**S8a (VPositionWellFormedness, ASN-0036).** For Q₁ and Q₂: unchanged V-positions, already satisfying S8a. For Q₃: shifted V-positions have positive ordinals (established under D-SHIFT), and the subspace identifier is preserved by σ.

**S8-depth (FixedDepthVPositions, ASN-0036).** For Q₁: depth unchanged. For Q₂: depth unchanged. For Q₃: TumblerSub on ordinals preserves depth at depth 1 (#([a] ⊖ [b]) = 1 = #[a]).

**S8-fin (FiniteArrangement, ASN-0036).** |dom(M'(d))| = |dom(M(d))| − |X| < |dom(M(d))|, finite since the original is finite.

**P4 (ProvenanceBounds, ASN-0047).** Contains(Σ') ⊆ R'. Since ran(M'(d)) ⊆ ran(M(d)) — the right-region I-addresses are preserved and the deleted I-addresses are removed, while no new I-addresses are introduced — and no other arrangement changes (D-XD), we have Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. ✓

**P4a (HistoricalFidelity).** R' = R by D-CF; no new provenance entries are introduced, so no new historical justification is required. All existing entries retain their witnesses from prior states. ✓

**P5 (DestructionConfinement).** C' = C ⊇ C (a); E' = E ⊇ E (b); R' = R ⊇ R (c) — all by D-CF. Only M admits loss, via K.μ⁻. ✓

**P6 (ExistentialCoherence, ASN-0047).** For all a ∈ dom(C'): origin(a) ∈ E'_doc. Unchanged: C' = C and E' = E, so P6 in Σ implies P6 in Σ'.

**P7, P7a (ProvenanceGrounding, ProvenanceCoverage).** R' = R, C' = C, E' = E. Both predicates inherited from Σ.


## Content Orphaning

DELETE creates a gap between content existence and content reachability.

**Definition — ContentOrphan.** An I-address a is *orphaned* in state Σ when:

`a ∈ dom(C) ∧ (A d ∈ E_doc : a ∉ ran(M(d)))`

Content at an orphaned address exists permanently (S0) but is not referenced by any document's current arrangement. V-space queries — which traverse M(d) to locate content — cannot reach it.

**D-ORPH — OrphanCreation (LEMMA).** DELETE can increase the set of orphaned I-addresses. Specifically: if a ∈ ran(M_S(d)), every V-position in subspace S of document d mapping to a lies within the deleted interval — `(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)` — and a ∉ ran(M_{S'}(d)) for all S' ≠ S, and a ∉ ran(M(d')) for all d' ≠ d, then after DELETE, a is orphaned.

*Proof.* By D-DOM, the post-state domain in subspace S is L ∪ Q₃. For a to appear in ran(M'_S(d)), some position in L ∪ Q₃ must map to a. No position in L maps to a: L ⊂ V_S(d) \ X, so any v' ∈ L with M(d)(v') = a would contradict the hypothesis that all such v' lie in X. No position in Q₃ maps to a: each σ(v) ∈ Q₃ has M'(d)(σ(v)) = M(d)(v) for v ∈ R by D-SHIFT, and v ∈ R ⊂ V_S(d) \ X, so again M(d)(v) = a would contradict the hypothesis. Therefore a ∉ ran(M'_S(d)). By D-XS, M'_{S'}(d) = M_{S'}(d) for S' ≠ S; by hypothesis, a ∉ ran(M_{S'}(d)). By D-XD, M'(d') = M(d') for d' ≠ d; by hypothesis, a ∉ ran(M(d')). Therefore a ∉ ⋃{ran(M'(d')) : d' ∈ E_doc}. Since a ∈ dom(C) = dom(C') by P0, a is orphaned in Σ'. ∎

Orphaning is a deliberate architectural consequence, not a defect. Nelson's diagram on 4/9 names the state explicitly: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)." The content persists at its permanent I-address. Its structural attribution (S7, ASN-0036) — encoding the creator's identity in the tumbler address itself — is unseverable. The address can be recovered through any prior arrangement that referenced it (historical backtrack), and through any other document that independently references it via transclusion. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40].

What orphaning means concretely is that all standard retrieval paths — which begin with a V-position and follow M(d) to an I-address — cannot reach the orphaned content. The content is not gone; it is merely not addressed in any current arrangement. Gregory's implementation confirms: no backend operation enumerates orphaned I-addresses; all retrieval paths are V-space-first.


## Provenance Divergence

The provenance relation R records which documents have ever contained which I-addresses. DELETE does not modify R (D-CF: R' = R). But DELETE does modify Contains(Σ) — the set of current (a, d) containment pairs.

**D-PSTALE — ProvenanceStaleness (LEMMA).** After DELETE, the provenance relation can properly contain the current containment relation:

`(E Σ, (d, S, p, w) satisfying D-PRE, Σ' = DELETE(Σ, d, S, p, w) :: Contains(Σ') ⊂ R')`

*Proof.* Before DELETE, let a = M(d)(v) for some v ∈ X such that a is referenced only from positions in X within document d — that is, `(A v' : v' ∈ dom(M(d)) ∧ M(d)(v') = a : v' ∈ X)` — and a ∉ ran(M(d')) for all d' ≠ d. Then (a, d) ∈ Contains(Σ) ⊆ R by P4. After DELETE, the conditions of D-ORPH are satisfied (every within-document mapping to a lies in X, and no cross-document mapping exists), so a is orphaned: a ∉ ⋃{ran(M'(d')) : d' ∈ E_doc}. In particular, (a, d) ∉ Contains(Σ'). But (a, d) ∈ R' since R' = R. Hence (a, d) ∈ R' \ Contains(Σ'). ∎

The stale provenance entries are the system's historical memory. They record that document d once contained I-address a, even though it no longer does. This is what P4a (HistoricalFidelity, ASN-0047) captures: every entry in R has a historical justification.

The practical consequence: any document-discovery index built on R (or on a similar write-only structure) reports supersets of true current containment after deletion. Gregory's implementation confirms this directly: the spanfilade — the document-discovery index — has no delete function; `dodeletevspan` touches only the POOM. Queries via `FINDDOCSCONTAINING` return documents from which content has been deleted. Filtering to exact containment requires a secondary V-space check: attempt to resolve the reported I-addresses through M(d); those with no V-position are stale.


## Implementation Observations

Several aspects of Gregory's implementation illuminate the abstract specification without constraining it. We note them here as non-normative observations.

**No merge after deletion.** After DELETE splits a mapping block at the cut points, the resulting fragments remain as separate POOM entries permanently. The `recombine` pass [edit.c:75] that follows DELETE performs B-tree rebalancing — adjusting which parent nodes group which children — but never merges leaf-level crums that become I-address-contiguous after the shift. The only I-contiguity check in the codebase (`isanextensionnd` [insertnd.c:301–309]) fires exclusively on the INSERT path. Abstractly, this means the implementation may maintain more mapping blocks than the canonical decomposition (M12, ASN-0058) would require. The abstract specification is agnostic: any valid decomposition satisfying B1–B3 suffices.

**Tree height monotonically increases.** The POOM tree's height can grow (via `levelpush` during insertion) but never shrink — the `levelpull` function [genf.c:318–342] is entirely commented out. A document that was once large retains its tree height after all content is deleted. Abstractly, this is invisible: the arrangement function M(d) is defined by its mapping, not by the height of the data structure.

**Transient negative displacements.** During the shift phase, `tumblersub` can produce negative V-displacement values in POOM crum nodes when the deletion width exceeds a crum's relative displacement [edit.c:63]. These are normalized immediately by `setwispnd` [wisp.c:171–228], which detects the minimum child displacement and adjusts the subtree to restore non-negative relative displacements while preserving absolute positions. Abstractly, this is invisible: the specification defines the shift on ordinals, not on relative displacements within a tree.

**Stale discovery index.** The spanfilade is not updated by DELETE. The `dodeletevspan` function [do1.c:158–167] touches only the POOM; no `deletespanf` function exists anywhere in the codebase [spanf1.c, spanf2.c]. This causes `FINDDOCSCONTAINING` to return false positives — documents that formerly contained the queried I-addresses. This is the implementation manifestation of D-PSTALE.

**Full-width delete leaves an empty arrangement.** When the deletion span covers the entire V-extent, all POOM bottom crums are freed via `disown` + `subtreefree`. The apex's width is zeroed by `setwispnd` [wisp.c:187–189], causing `isemptyorgl` to return TRUE and subsequent retrieval to return empty results. The tree structure (interior nodes, height) persists as dead scaffolding.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ord(v) | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier | introduced |
| vpos(S, o) | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord | introduced |
| w_ord | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0 | introduced |
| D-CTG | V-positions within each subspace form a contiguous ordinal range — design constraint (DESIGN, not a reachable-state invariant) assumed and preserved by DELETE | introduced |
| D-PRE | DELETE requires d ∈ E_doc, w > 0, subspace(p) ≥ 1, #p = 2, span ⊆ current extent, #w = #p, w₁ = 0 | introduced |
| D-LEFT | (A v ∈ L : M'(d)(v) = M(d)(v)) — left region unchanged | introduced |
| D-DOM | dom(M'(d)) ∩ V_S = L ∪ Q₃ — post-state domain fully determined by D-LEFT and D-SHIFT | introduced |
| D-SHIFT | (A v ∈ R : M'(d)(σ(v)) = M(d)(v)) where σ(v) = vpos(S, ord(v) ⊖ w_ord) | introduced |
| D-CF | C' = C, E' = E, R' = R — DELETE modifies only M(d) in subspace S | introduced |
| D-XD | (A d' ≠ d : M'(d') = M(d')) — cross-document isolation | introduced |
| D-XS | (A v : subspace(v) ≠ S : M'(d)(v) = M(d)(v)) — subspace confinement | introduced |
| D-IID | d ∈ E'_doc — document identity preserved | introduced |
| D-BJ | σ is order-preserving and injective on R | introduced |
| D-SEP | σ(r) has ordinal ord(p) — gap closes exactly at the deletion point | introduced |
| D-DP | DELETE preserves D-CTG | introduced |
| D-WR | \|V_S'(d)\| = \|V_S(d)\| − \|X\| — extent decreases by deletion width | introduced |
| D-BLK | Block decomposition transforms by split/remove/shift, preserving B1–B3 | introduced |
| D-ORPH | DELETE orphans I-address a when all within-document mappings to a lie in X and no cross-document references exist | introduced |
| D-PSTALE | After DELETE, R can properly contain Contains(Σ') — stale provenance | introduced |


## Open Questions

Does every well-formed editing operation (INSERT, COPY, REARRANGE) preserve D-CTG, or are there operations that legitimately produce non-contiguous V-position sets?

What conditions must a version-reconstruction mechanism satisfy to guarantee that any prior arrangement — including the pre-deletion state — is recoverable from the post-deletion state and system history?

Under what conditions can a sequence of deletions and insertions cause the number of mapping blocks in a decomposition to grow without bound relative to the content size?

What must a document-discovery index guarantee after deletion — is superset reporting (D-PSTALE) an acceptable contract, or must exact containment queries be supported?

Can the gap-closure formula (D-SEP) and contiguity preservation (D-DP) be generalized to ordinals of depth greater than one while preserving the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment?

If a single I-address is referenced by two V-positions in the same document (within-document sharing per S5, ASN-0036), and DELETE removes one of those positions, what must the surviving mapping and provenance relation satisfy?

What properties must hold when DELETE removes a V-span whose I-addresses are also referenced by link endsets, given that links attach to I-addresses rather than V-positions?
