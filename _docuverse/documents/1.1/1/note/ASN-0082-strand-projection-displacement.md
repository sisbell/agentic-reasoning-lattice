# ASN-0082: Strand Projection Displacement

*2026-04-09*

This ASN extends ASN-0053 (Span Algebra) with two complementary shift properties governing the arrangement transformations that underlie INSERT and DELETE. The *post-insertion shift* (I3 and its preservation lemmas) guarantees that ordinal shift applied uniformly to arrangement positions at or beyond an insertion point preserves mapping values while relocating V-positions forward by a fixed displacement. The *post-contraction shift* (D-SHIFT, the gap-closure lemmas D-BJ, D-SEP, D-DP, and the post-state preservation lemmas S2-post, S3-post, D-CTG-post, D-MIN-post, D-SEQ-post, S8-depth-post, S8a-post, S8-fin-post, S7-post) is the dual: it characterizes the inverse displacement that closes the gap left by removing a contiguous range of positions, preserving the I-address mappings of the right region while shifting their V-positions backward and re-establishing the foundation's contiguity invariants. The ordinal shift and its inverse — defined via OrdinalShift, OrdinalDisplacement, and TumblerSub (ASN-0034) — are fundamental operations on the tumbler line whose interaction with arrangement mappings determines how contiguous regions of mapped positions are repositioned without altering the content they reference. Both properties belong in the span algebra domain because they characterize how the displacement arithmetic underlying span endpoints (reach(σ) = start(σ) ⊕ width(σ)) behaves when applied as a uniform translation to a region of a partial function over the tumbler line.


## Foundation Invariants

This ASN relies on two foundation invariants from ASN-0036 governing V-position structure:

**S8-depth** — *FixedDepthVPositions* (cited, ASN-0036). `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`. All V-positions within a given subspace of a document share the same tumbler depth.

**S8a** — *VPositionWellFormedness* (cited, ASN-0036). `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`. V-positions are zero-free, have depth at least 2, and have every component strictly positive. The componentwise positivity conjunct entails the specializations `v₁ ≥ 1` (positive subspace identifier) and `v > 0` (positive as a tumbler under lexicographic order), used pointwise in proofs below.

The contraction operation (below) additionally cites the following ASN-0036 properties:

- **S0** (ContentImmutability): for every state transition, `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`.
- **S2** (ArrangementFunctionality): each V-position in dom(M(d)) has a uniquely determined I-address.
- **S3** (ReferentialIntegrity): `ran(M(d)) ⊆ dom(Σ.C)`.
- **S8-fin** (FiniteArrangement): for each document d, dom(M(d)) is finite.
- **D-CTG** (VContiguity, text subspace only): `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`. The link subspace V_2(d) is exempt — sparse with tombstones is permitted (ASN-0036, D-CTG frame note).
- **D-SEQ** (SequentialPositions, text subspace only): when V_1(d) is non-empty with common depth m ≥ 2, there exists n ≥ 1 such that V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}.
- **D-MIN** (VMinimumPosition, text subspace only): when V_1(d) is non-empty, min(V_1(d)) = [1, 1, ..., 1] of length m. The link subspace is exempt — link positions need not begin at [2, 1, ..., 1].


## The Ordinal Shift

The *ordinal displacement* δ(n, m) is defined in the foundation: for n ≥ 1 and m ≥ 1, δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m (OrdinalDisplacement, ASN-0034).

When the depth is determined by context (typically m = #p for insertion position p), we write δₙ.

The *ordinal shift* is defined in the foundation: for a V-position v of depth m and n ≥ 1, shift(v, n) = v ⊕ δ(n, m) (OrdinalShift, ASN-0034). By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the ordinal within the V-position's subspace by exactly n, leaving all higher-level components unchanged.

We need two properties of this shift. Both are established in the foundation.

Order preservation is guaranteed: for v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂, shift(v₁, n) < shift(v₂, n) (TS1, ASN-0034).

The relative ordering of content is preserved through the shift. What was before other content remains before it after insertion — Nelson's guarantee that content appears "in its original relative order on either side" (Q2).

Injectivity is likewise guaranteed: for v₁, v₂ with #v₁ = #v₂ = m, shift(v₁, n) = shift(v₂, n) implies v₁ = v₂ (TS2, ASN-0034).

Injectivity ensures the shift creates no collisions: distinct V-positions remain distinct after shifting.

Additionally, shift preserves structural properties. Subspace preservation requires m ≥ 2: by TumblerAdd (ASN-0034), positions before the action point are copied from v — for δₙ with action point k = m, positions i < k are copied from v — so when m ≥ 2, position 1 (the subspace identifier) is preserved: shift(v, n)₁ = v₁, giving subspace(shift(v, n)) = subspace(v). When m = 1, shift([S], n) = [S + n] changes the subspace identifier; we exclude this by requiring #p ≥ 2 as an operation precondition. By S8-depth (ASN-0036), all V-positions in subspace S share a uniform depth d; the depth-compatibility precondition on I3 requires d = #p when such V-positions exist, so m = d = #p ≥ 2 holds for every V-position in the shifted region. This also ensures that the comparison v ≥ p in I3's quantifier is between equal-length tumblers, giving it the clean "at or to the right of p" semantics without prefix-case ambiguity. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves the S8a well-formedness conditions: the zero-count zeros(shift(v, n)) = 0 holds because shift copies positions 1 through m − 1 from v (all nonzero by S8a on M(d)) and produces vₘ + n > 0 at position m; the subspace identifier shift(v, n)₁ = v₁ ≥ 1 is preserved because shift copies position 1 from v when m ≥ 2; and positivity shift(v, n) > 0 follows from v₁ ≥ 1 > 0.


## Post-Insertion Shift

Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions (element-field tumblers in the Vstream) to I-addresses (element-field tumblers in the Istream).

**Scope.** This ASN characterizes the *shift sub-operation* of INSERT — the arrangement transformation that opens a gap of n positions at p by relocating existing content forward — not the full INSERT operation. The full INSERT additionally places n new content elements at the vacated gap positions [p, shift(p, n)), which entails extending dom(C) with n new I-addresses, allocating mappings for the gap positions, and re-deriving the contiguity invariants D-CTG, D-MIN, D-SEQ across the complete post-state. Those content-placement postconditions belong in a future INSERT ASN that composes the shift sub-operation specified here with content allocation. The frame I3-C below holds for the shift sub-operation in isolation: shifting existing content does not by itself add or modify any content-store entries. A composing INSERT operation will weaken I3-C to S0 (`dom(C) ⊆ dom(C') ∧ ...`) to permit n new I-addresses, and the composition's combined postcondition will be S0-compatible.

Within this scoped sub-operation, the shift relocates existing content at or beyond p in subspace S = subspace(p) = p₁ (with S ≥ 1) by n ≥ 1 ordinal positions, producing M'(d) from M(d) without touching C.

**I3** — *PostInsertionShift* (POSTCONDITION, introduced). Content at or beyond p shifts forward by n ordinal positions.

*Preconditions:* d is a document; M(d) : T ⇀ T is its arrangement; p ∈ T with #p ≥ 2 and subspace(p) = S ≥ 1; depth-compatible: if {v ∈ dom(M(d)) : subspace(v) = S} ≠ ∅ then #p = #v for any such v (unique depth by S8-depth, ASN-0036); n ≥ 1; M'(d) is the post-insertion arrangement.

*Postconditions:*

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

- I3-V (vacating): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d)))`

*Frame:*

- I3-L (left region): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`
- I3-X (cross-subspace): `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`
- I3-D (cross-document): `(A d' ≠ d : M'(d') = M(d'))`
- I3-C (content store): `dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))` — S9 (TwoStreamSeparation, ASN-0036) guarantees existing content is preserved; the shift stores no new content, so dom(C') = dom(C)

*Domain closure:*

- I3-CS (subspace S): `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : (v < p ∧ v ∈ dom(M(d))) ∨ (E u : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p : v = shift(u, n)))`
- I3-CX (cross-subspace): `(A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d)))`

The I-address is unchanged — only the V-position moves. This is Nelson's central guarantee (Q1, Q5): the permanent identity of every existing byte is invariant under insertion. "Since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. The shift moves content in the document's arrangement without touching the content's identity in the store. The left-region frame (I3-L) ensures that content before the insertion point is undisturbed. The cross-subspace frame (I3-X) ensures that link subspaces and other subspaces are unaffected by a text-subspace insertion. The cross-document frame (I3-D) ensures that other documents are unchanged. The content-store frame (I3-C) makes explicit that the shift is arrangement-only: S9 (TwoStreamSeparation, ASN-0036) guarantees existing content is preserved (`dom(C) ⊆ dom(C')` and values unchanged); since the shift stores no new content — it is purely an arrangement operation — the reverse inclusion holds and dom(C') = dom(C). The vacating postcondition (I3-V) completes the shift semantics: original positions at or beyond p that are not the destination of any shifted content are removed from dom(M'(d)), preventing content duplication in sparse arrangements. Without I3-V, an implementation could retain M'(d)(v) = M(d)(v) alongside M'(d)(shift(v, n)) = M(d)(v), duplicating content at both the original and shifted positions. The domain closure clauses (I3-CS, I3-CX) close dom(M'(d)) from above: no position enters the post-state domain except those explicitly placed by I3, I3-L, and I3-X. Without these clauses, the assignment and vacating postconditions constrain only positions that were in dom(M(d)) — an M'(d) satisfying them could contain additional positions at arbitrary depth, leaving dom(M'(d)) underdetermined.

**Consistency.** We verify that the eight clauses are mutually consistent, ensuring M'(d) and C' are well-defined. I3-C constrains C' independently of M'(d) — the content store is unchanged regardless of arrangement modifications. The remaining seven clauses constrain M'(d): the assignment clauses I3, I3-L, and I3-X specify positions that *are* in dom(M'(d)) with defined values; I3-V specifies positions that are *not* in dom(M'(d)); I3-CS and I3-CX constrain dom(M'(d)) to contain only positions placed by the assignment clauses. We must check pairwise disjointness of the assignment regions, that I3-V's vacated positions do not overlap any assignment region, and that the closure clauses are consistent with both. *Shifted vs left*: for v ≥ p in subspace S, shift(v, n) > v ≥ p by TS4 (ASN-0034), so shift(v, n) > p > u for every u < p; no shifted output coincides with a left-region position. *Shifted vs shifted*: TS2 (injectivity) guarantees distinct v's produce distinct shift(v, n)'s. *Shifted vs cross-subspace*: subspace preservation (shift(v, n)₁ = v₁ = S when m ≥ 2) ensures shifted positions remain in subspace S, disjoint from I3-X positions (subspace ≠ S). *Left vs cross-subspace*: left-region positions have subspace S, cross-subspace positions have subspace ≠ S — disjoint by definition. *Cross-document*: I3-D operates on d' ≠ d, disjoint from the other three by document identity. *Vacated vs assignment regions*: I3-V applies to positions v with subspace(v) = S and v ≥ p that are *not* shifted images; I3 assigns values only at shifted images shift(u, n), so I3-V and I3 are disjoint by the exclusion condition. I3-L applies only to v < p, while I3-V applies to v ≥ p — disjoint. I3-X applies only to subspace ≠ S, while I3-V applies to subspace S — disjoint. *Closure consistency*: I3-CS constrains dom(M'(d)) ∩ subspace S to positions placed by I3 and I3-L — exactly the positions those clauses establish. I3-CX constrains dom(M'(d)) outside subspace S to dom(M(d)) — exactly the set I3-X retains. I3-V removes positions in subspace S at or beyond p that are not shifted images; I3-CS independently excludes these same positions (they are neither left-region nor shifted-image), so the closure and vacating clauses agree. The eight clauses are mutually consistent, so M'(d) and C' are well-defined.

**Structural preservation.** We derive that S8-depth, S8a, S8-fin, and S2 hold for the post-state M'(d), and that referential integrity (S3) is preserved, enabling composition with subsequent operations.

**I3-VD** — *PostInsertionDepthUniformity* (LEMMA, derived). S8-depth holds for the post-state M'(d) across all subspaces. For subspace S: `(A v₁, v₂ ∈ dom(M'(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂ = m)`. By I3-CS, every v ∈ dom(M'(d)) with subspace(v) = S falls into exactly one of two regions. *Left region* (I3-L): v ∈ dom(M(d)) with subspace(v) = S and v < p; these have depth m by S8-depth on M(d). *Shifted region* (I3): shift(v, n) for v ∈ dom(M(d)) with subspace(v) = S and v ≥ p; #shift(v, n) = #δₙ = m by the result-length identity of TumblerAdd, and #v = m by S8-depth on M(d). Both regions yield depth m. For any subspace S' ≠ S: by I3-CX, the positions in dom(M'(d)) with subspace S' are exactly the positions in dom(M(d)) with subspace S', on which S8-depth holds by hypothesis. ∎

**I3-VP** — *PostInsertionWellFormedness* (LEMMA, derived). `(A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`. By I3-CS and I3-CX, every v ∈ dom(M'(d)) falls into exactly one of three regions. *Left region* (I3-L): v ∈ dom(M(d)) with subspace(v) = S and v < p; S8a on M(d) gives v's well-formedness directly. *Shifted region* (I3): shift(v, n) for v ∈ dom(M(d)) with subspace(v) = S and v ≥ p; by OrdAddS8a (ASN-0036) applied to v ⊕ δₙ, shift(v, n) satisfies S8a — the OrdAddS8a tail condition `(A i : actionPoint(δₙ) < i ≤ m : (δₙ)ᵢ > 0)` is vacuous since actionPoint(δₙ) = m. Equivalently, by direct computation: shift copies positions 1 through m − 1 from v (each strictly positive by S8a's componentwise positivity conjunct, so zero-free) and produces vₘ + n > 0 at position m, giving zeros(shift(v, n)) = 0, depth m ≥ 2, and componentwise positivity. *Cross-subspace region* (I3-X): v ∈ dom(M(d)) with subspace(v) ≠ S; S8a on M(d) gives v's well-formedness directly. ∎

**I3-S3** — *PostInsertionReferentialIntegrity* (LEMMA, derived). `(A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C'))`. By I3-C, dom(C') = dom(C). Every v ∈ dom(M'(d)) has M'(d)(v) equal to some M(d)(u) for u ∈ dom(M(d)): shifted positions have M'(d)(shift(u, n)) = M(d)(u) by I3; left-region and cross-subspace positions have M'(d)(v) = M(d)(v) by I3-L and I3-X. By S3 (ReferentialIntegrity, ASN-0036) on the pre-state, M(d)(u) ∈ dom(C) = dom(C'). ∎

**I3-S2** — *PostInsertionFunctionality* (LEMMA, derived). `M'(d)` is a function — S2 (ArrangementFunctionality, ASN-0036) holds for the post-state. The consistency check above establishes pairwise disjointness of the three assignment regions (shifted, left, cross-subspace); since each region assigns exactly one value per position, no position in dom(M'(d)) receives two values. ∎

**I3-fin** — *PostInsertionFiniteness* (LEMMA, derived). `dom(M'(d))` is finite — S8-fin (FiniteArrangement, ASN-0036) holds for the post-state. By I3-CS and I3-CX, every position in dom(M'(d)) either belongs to dom(M(d)) directly (left-region or cross-subspace) or is shift(v, n) for some v ∈ dom(M(d)) with subspace(v) = S and v ≥ p. The shifted-image set is at most as large as the source set by injectivity (TS2, ASN-0034). Both contributing sets are subsets or injective images of dom(M(d)), which is finite by S8-fin on the pre-state; their union is therefore finite. ∎

**I3-S7** — *PostInsertionAllocationInvariants* (LEMMA, derived). The post-state satisfies S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), and S7c (ElementFieldDepth). By I3-C, `dom(C') = dom(C)` and per-address values are unchanged. S7a, S7b, and S7c are predicates over `dom(C)`; since this set is unchanged and the pre-state satisfies all three, the post-state satisfies them identically. ∎

**Arrangement invariants not preserved.** The shift preserves typing invariants (S8-depth, S8a, S3) but does *not* preserve the contiguity invariants of ASN-0036. The gap created by the shift — n vacated positions between the left region and the shifted region — violates D-CTG (VContiguity): the post-state V_S(d) is not contiguous, as the worked example confirms ({[1,1], [1,2], [1,5], [1,6], [1,7]} has a gap between [1,2] and [1,5]). D-SEQ (SequentialPositions) is likewise violated, since V_S(d) is no longer {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for any n. When p = min(V_S(d)), the shift vacates the minimum position, additionally violating D-MIN (VMinimumPosition). These violations are inherent to the shift's purpose: it opens a gap for new content. The INSERT ASN must re-establish D-CTG, D-MIN, and D-SEQ by filling the gap positions, alongside re-deriving S8-depth and S8a for the complete post-state.

**Weakest-precondition analysis (I3-VP backwards through the shift).** We illustrate the wp method on one of the preservation lemmas — I3-VP, which asserts S8a for the post-state — to expose the constraints that the assignment statement `M'(d)(shift(v, n)) := M(d)(v)` imposes on the pre-state when we require S8a to hold of the assigned position `shift(v, n)`. The wp computation propagates the post-state predicate backwards through the assignment to yield the pre-state obligation. Reading these obligations against the I3 contract makes explicit which preconditions the contract supplies and which it does not need to state because they are entailed by foundation invariants.

The S8a postcondition on the shifted position is the conjunction `zeros(shift(v, n)) = 0 ∧ #shift(v, n) ≥ 2 ∧ (A i : 1 ≤ i ≤ #shift(v, n) : shift(v, n)ᵢ > 0)`. Substituting `shift(v, n) = v ⊕ δₙ` and using TumblerAdd's prefix-copy / action-point-advance / tail-copy behavior:

- `shift(v, n)ᵢ = vᵢ` for `1 ≤ i ≤ m − 1` (prefix copy, since actionPoint(δₙ) = m).
- `shift(v, n)ₘ = vₘ + n` (action-point advance).
- `#shift(v, n) = m` (result-length identity).

The wp of S8a backwards through `(target := shift(v, n))` becomes a predicate over v:

`wp(target := shift(v, n), S8a(target)) = (A i : 1 ≤ i ≤ m − 1 : vᵢ > 0) ∧ (vₘ + n > 0) ∧ (m ≥ 2)`

Each conjunct is a pre-state obligation, read in order:

1. *`(A i : 1 ≤ i ≤ m − 1 : vᵢ > 0)` — componentwise positivity on positions 1..m−1.* This is exactly S8a's componentwise-positivity conjunct applied to v, supplied by `v ∈ dom(M(d))` and the pre-state S8a invariant. The wp pinpoints why I3 needs `v ∈ dom(M(d))` (already given by the quantifier in I3): without that membership we would have no S8a hypothesis on v and the wp obligation would be open.
2. *`vₘ + n > 0` — strict positivity of the advanced ordinal.* Since `n ≥ 1` (I3 precondition) and `vₘ ≥ 1` (S8a on v at position m), `vₘ + n ≥ 1 + 1 = 2 > 0` by NAT-addcompat (ASN-0034). Note that `n ≥ 1` alone suffices when `vₘ ≥ 0`, but the foundation gives us the stronger `vₘ ≥ 1`. The wp clarifies that the `n ≥ 1` precondition is doing essential work here — `n = 0` would reduce this to `vₘ > 0`, which holds, but `shift(v, 0) = v` would also collapse the entire shift semantics.
3. *`m ≥ 2` — depth at least 2.* This is the I3 precondition `#p ≥ 2` (or equivalently the S8-depth common-depth value `m ≥ 2`), justified by S8a on the pre-state requiring `#v ≥ 2` for every `v ∈ dom(M(d))`.

The wp surfaces *what the assignment requires* from the pre-state, and against this we can verify what the contract supplies. The contract provides `v ∈ dom(M(d))` (giving conjunct 1 via S8a's componentwise positivity), `n ≥ 1` (giving conjunct 2 in combination with S8a's `vₘ ≥ 1`), and the depth-compatibility precondition `#p ≥ 2` (giving conjunct 3 via S8-depth's common-depth identity). All three wp obligations are discharged by I3's preconditions composed with S8a on the pre-state — confirming that the contract's preconditions are exactly the wp-derived constraints, with no slack.

*Why componentwise positivity of v on positions 1..m−1 specifically?* The wp obligation isolates this — not the full S8a — as what the shift requires of v's prefix. Position 1 (subspace identifier) needs `v₁ ≥ 1` so that `subspace(shift(v, n)) = v₁ = S ≥ 1`. Positions 2..m−1 (intermediate ordinal components, vacuous when `m = 2`) need `vᵢ ≥ 1` so the prefix copy yields a zero-free image. The shift does not need to know anything about `vₘ` for positions 1..m−1 since position m is advanced by `+n ≥ 1`, but does need `n ≥ 1` (already a precondition) to advance the action point's value to a positive natural even from `vₘ = 0`. The wp makes the dependency structure visible.

**Weakest-precondition analysis (I3-S2 backwards through the assignment regions).** I3-VP is a single-position obligation; the wp derivation above never crosses region boundaries. I3-S2 (functionality of M'(d)) is structurally different: its post-state predicate `(A v₁, v₂ ∈ dom(M'(d)) : v₁ = v₂ ⟹ M'(d)(v₁) = M'(d)(v₂))` quantifies over pairs that may straddle the four assignment regions (shifted, left, cross-subspace, vacated). The wp of this conjunction through the simultaneous assignment statements yields a pairwise no-conflict obligation against the pre-state, and it is here that subspace preservation and TS2's injectivity enter as wp-discharged hypotheses rather than free-floating facts. We work the case to expose those entry points.

Functionality holds iff for every pair of positions `v₁, v₂ ∈ dom(M'(d))`, `v₁ = v₂` implies `M'(d)(v₁) = M'(d)(v₂)`. Equivalently, no position in dom(M'(d)) receives two distinct values. The four assignment statements that populate M'(d) are:

- *(shift):* `M'(d)(shift(u, n)) := M(d)(u)` for u ∈ dom(M(d)) with subspace(u) = S and u ≥ p (I3).
- *(left):* `M'(d)(u) := M(d)(u)` for u ∈ dom(M(d)) with subspace(u) = S and u < p (I3-L).
- *(cross):* `M'(d)(u) := M(d)(u)` for u ∈ dom(M(d)) with subspace(u) ≠ S (I3-X).
- *(vacate):* `M'(d)(u) := ⊥` for u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p ∧ u ∉ {shift(u', n) : ...} (I3-V).

The wp of "no double assignment" backwards through the simultaneous assignment is the conjunction of *six* pairwise-disjointness obligations (the (vacate) statement removes positions from dom(M'(d)) and so cannot collide with another assignment within dom(M'(d)); collisions between (vacate) and a positive assignment are addressed below as the (shift) ∩ (vacate) overlap, where (shift) wins by construction):

1. *(shift) ∩ (shift):* `(A u₁, u₂ : both in shifted source : shift(u₁, n) = shift(u₂, n) ⟹ M(d)(u₁) = M(d)(u₂))`. Discharged by TS2 (ShiftInjectivity, ASN-0034): from `shift(u₁, n) = shift(u₂, n)`, TS2 gives `u₁ = u₂`, hence `M(d)(u₁) = M(d)(u₂)` by reflexivity of equality. The wp surfaces TS2 as the precise obligation: without injectivity of shift, two distinct pre-state positions could map to the same post-state V-position with conflicting I-addresses.
2. *(shift) ∩ (left):* `(A u₁ in shifted source, u₂ in left source : shift(u₁, n) = u₂ ⟹ M(d)(u₁) = M(d)(u₂))`. The hypothesis is impossible: u₁ ≥ p forces shift(u₁, n) > u₁ ≥ p (TS4), but u₂ < p, so shift(u₁, n) > p > u₂ — strict inequality, never equality. The wp reduces to `False ⟹ ...`, vacuously true. The wp pinpoints why TS4 (ShiftStrictlyAdvances, ASN-0034) is doing essential work: without `shift(u, n) > u`, an in-place shift (n = 0) could land a shifted image inside the left region.
3. *(shift) ∩ (cross):* `(A u₁ in shifted source, u₂ in cross source : shift(u₁, n) = u₂ ⟹ M(d)(u₁) = M(d)(u₂))`. The hypothesis is impossible by subspace preservation: subspace(shift(u₁, n)) = u₁₁ = S (TumblerAdd's prefix-copy when m ≥ 2), while subspace(u₂) ≠ S — different position-1 components, so no equality is possible. The wp surfaces the `m ≥ 2` precondition as the entry point: at m = 1, shift would change the subspace identifier and a shifted text-subspace image could collide with a link-subspace position.
4. *(left) ∩ (left):* `(A u₁, u₂ in left source : u₁ = u₂ ⟹ M(d)(u₁) = M(d)(u₂))` — trivial, since `u₁ = u₂` directly forces `M(d)(u₁) = M(d)(u₂)` (S2 on the pre-state, M(d) is a function).
5. *(left) ∩ (cross):* impossible — subspace(u₁) = S ≠ subspace(u₂) makes u₁ = u₂ unsatisfiable. The wp reduces to `False ⟹ ...`.
6. *(cross) ∩ (cross):* `(A u₁, u₂ in cross source : u₁ = u₂ ⟹ M(d)(u₁) = M(d)(u₂))` — trivial by S2 on the pre-state.

Each non-trivial obligation discharges via a foundation invariant or precondition: TS2 (ShiftInjectivity, ASN-0034) for (1); TS4 (ShiftStrictlyAdvances, ASN-0034) combined with the I3 preconditions `n ≥ 1` and the quantifier ranges `u₁ ≥ p, u₂ < p` for (2); subspace preservation derived from the I3 precondition `#p ≥ 2` for (3); pre-state S2 for (4) and (6); subspace-identifier disjointness for (5).

This is the same recipe as I3-VP (substitute the post-state predicate, push it backwards through the assignments, read each conjunct as a discharged obligation), but the *content* of the obligations is different: I3-VP's wp surfaces componentwise positivity of v's prefix; I3-S2's wp surfaces injectivity, advancement, and subspace preservation. The two together cover the structural roles of the four foundation properties (S8a, TS2, TS4, prefix-copy at m ≥ 2) that the contract promises.

The remaining post-state lemmas — I3-VD (depth uniformity), I3-S3 (referential integrity), I3-fin (finiteness) — admit wp derivations of the same form and discharge against TumblerAdd's result-length identity (for I3-VD), pre-state S3 plus I3-C (for I3-S3), and TS2 plus pre-state S8-fin (for I3-fin); we have not worked them in detail because the obligations they surface are subsumed by those already exposed for I3-VP and I3-S2.

**Gap and vacated regions.** I3-V explicitly vacates original positions at or beyond p that are not the destination of any shifted content, completing the shift semantics: content departs from its original position as it arrives at the shifted one. The vacated set includes original positions within the gap [p, shift(p, n)) — which would otherwise be unaddressed — as well as, in sparse arrangements, original positions beyond the gap whose shift pre-images are absent from dom(M(d)). After accounting for all eight clauses, the positions in [p, shift(p, n)) remain the only region not assigned a value by any postcondition — and I3-CS explicitly excludes them from dom(M'(d)), since they are neither left-region positions nor shifted images: p is not < p (so I3-L excludes it), and no shifted image lands in the gap — two cases establish this: (1) when v = p, shift(p, n) equals the exclusive upper bound of [p, shift(p, n)) and so is not in the gap; (2) when v > p with #v = #p = m, TS1 (ShiftOrderPreservation, ASN-0034) gives shift(v, n) > shift(p, n), placing the image strictly past the gap's upper bound. These n gap positions are where newly inserted content will be placed; the content-placement postcondition is an operation-level concern deferred to a future INSERT ASN. That ASN will extend the closed domain established by I3-CS — adding the gap positions to dom(M'(d)) — and must re-derive S8-depth, S8a, D-CTG, D-MIN, and D-SEQ for the complete post-state.


### Worked Example

Consider document d with five characters at V-positions [1, 1] through [1, 5], mapped to contiguous I-addresses b, b + 1, ..., b + 4.

Insert two characters at p = [1, 3]. Parameters: n = 2, S = 1, m = 2, δ₂ = [0, 2].

The left-region frame (I3-L) preserves [1, 1] and [1, 2] with unchanged I-addresses. I3 shifts: shift([1, 3], 2) = [1, 3] ⊕ [0, 2] = [1, 5], shift([1, 4], 2) = [1, 6], shift([1, 5], 2) = [1, 7]. Each shifted position preserves its I-address:

| V (before) | I (before) | V (after) | I (after) | Region |
|---|---|---|---|---|
| [1, 1] | b | [1, 1] | b | left (I3-L) |
| [1, 2] | b + 1 | [1, 2] | b + 1 | left (I3-L) |
| [1, 3] | b + 2 | [1, 5] | b + 2 | shifted (I3) |
| [1, 4] | b + 3 | [1, 6] | b + 3 | shifted (I3) |
| [1, 5] | b + 4 | [1, 7] | b + 4 | shifted (I3) |

Positions [1, 1] and [1, 2] are below p = [1, 3] and remain unchanged (I3-L). The three V-positions at or beyond p are each advanced by δ₂ = [0, 2]; their I-addresses are unchanged (I3).

**I3-V trace.** The shifted-image set is {shift(v, 2) : v ∈ dom(M(d)), subspace(v) = 1, v ≥ [1, 3]} = {[1, 5], [1, 6], [1, 7]}. I3-V applies to each original position at or beyond p that is *not* in this set:

- [1, 3]: not in {[1, 5], [1, 6], [1, 7]} → I3-V vacates: [1, 3] ∉ dom(M'(d)).
- [1, 4]: not in {[1, 5], [1, 6], [1, 7]} → I3-V vacates: [1, 4] ∉ dom(M'(d)).
- [1, 5]: *is* in the shifted-image set — [1, 5] = shift([1, 3], 2). I3-V's exclusion condition prevents vacating. I3 reassigns: M'(d)([1, 5]) = M(d)([1, 3]) = b + 2. The original value M(d)([1, 5]) = b + 4 is superseded — [1, 5] is retained at its shifted value, not its original one.

Positions [1, 3] and [1, 4] are the gap positions in [p, shift(p, n)) = [[1, 3], [1, 5]). Position [1, 5] demonstrates the overlap case: it is both an original position at or beyond p and a shifted destination, so I3 governs its post-state value while I3-V does not apply. ∎

**Boundary: insert at start.** Set p = [1, 1]. No V-position v satisfies v < p (since [1, 1] is the smallest in subspace 1), so I3-L's quantifier ranges over ∅ and holds vacuously. I3 shifts all five positions: shift([1, 1], 2) = [1, 3], ..., shift([1, 5], 2) = [1, 7], each preserving its I-address. ∎

**Boundary: insert past end.** Set p = [1, 6]. No V-position v satisfies v ≥ p, so I3's quantifier ranges over ∅ and holds vacuously. I3-L preserves all five positions [1, 1] through [1, 5] with unchanged I-addresses. ∎

**Boundary: empty document.** When dom(M(d)) = ∅, both I3 and I3-L quantify over ∅ and hold vacuously. The postcondition is consistent: insertion into an empty document creates no conflicts. ∎

**Cross-subspace preservation: text insertion leaves link subspace untouched.** Consider document d with both text and link subspaces populated. The text subspace S = 1 has three contiguous positions; the link subspace S = 2 has two sparse positions (allowed by the foundation's frame note on D-CTG for V_2). All positions have depth 2.

M(d) = {[1, 1] → b, [1, 2] → b + 1, [1, 3] → b + 2,  [2, 5] → ℓ₁, [2, 9] → ℓ₂}

Insert two text positions at p = [1, 2]. Parameters: n = 2, S = subspace(p) = 1, m = #p = 2, δ₂ = [0, 2].

By the depth-compatibility precondition on I3 (`#p = #v` for any v in subspace S of dom(M(d))), the comparison `v ≥ p` is between equal-length tumblers within subspace S = 1. Since v < p for v = [1, 1] and v ≥ p for v ∈ {[1, 2], [1, 3]}, I3-L preserves [1, 1] and I3 shifts the other two text positions:

- shift([1, 2], 2) = [1, 4]
- shift([1, 3], 2) = [1, 5]

The link-subspace positions [2, 5] and [2, 9] have subspace 2 ≠ S, so they fall under I3-X, which preserves both their positions and their I-address mappings:

| V (before) | I (before) | V (after) | I (after) | Region |
|---|---|---|---|---|
| [1, 1] | b | [1, 1] | b | left (I3-L) |
| [1, 2] | b + 1 | [1, 4] | b + 1 | shifted (I3) |
| [1, 3] | b + 2 | [1, 5] | b + 2 | shifted (I3) |
| [2, 5] | ℓ₁ | [2, 5] | ℓ₁ | cross-subspace (I3-X) |
| [2, 9] | ℓ₂ | [2, 9] | ℓ₂ | cross-subspace (I3-X) |

**Verification:**

- *I3-L:* [1, 1] < p = [1, 2] (T1, divergence at component 2 with 1 < 2); M'(d)([1, 1]) = b = M(d)([1, 1]). ✓
- *I3:* M'(d)([1, 4]) = b + 1 = M(d)([1, 2]); M'(d)([1, 5]) = b + 2 = M(d)([1, 3]). ✓
- *I3-X:* For v ∈ {[2, 5], [2, 9]}, subspace(v) = 2 ≠ 1 = S; v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v) by I3-X. ✓
- *I3-V:* Positions [1, 2] and [1, 3] are in dom(M(d)), have subspace 1, and ≥ p; the shifted-image set is {[1, 4], [1, 5]}. Neither [1, 2] nor [1, 3] is in this set, so I3-V vacates both: [1, 2] ∉ dom(M'(d)) and [1, 3] ∉ dom(M'(d)). ✓
- *I3-CS:* dom(M'(d)) ∩ subspace 1 = {[1, 1], [1, 4], [1, 5]} — exactly the left-region position and the shifted images. No gap positions [1, 2] or [1, 3] are in dom(M'(d)). ✓
- *I3-CX:* dom(M'(d)) ∩ subspace 2 = {[2, 5], [2, 9]} = dom(M(d)) ∩ subspace 2. The sparse link subspace is preserved verbatim — the tombstone gap at [2, 6], [2, 7], [2, 8] remains. ✓
- *I3-C:* dom(C') = dom(C) and values unchanged. The shift sub-operation modifies only M(d); no I-addresses are allocated. ✓

The example exercises I3-X concretely: the link subspace V_2(d) — which is sparse with a tombstone gap, exempt from D-CTG by the foundation — is unaffected by a text-subspace insertion. The text-subspace shift's δ₂ displacement acts only on positions with subspace identifier equal to S = 1; link-subspace positions, having subspace identifier 2 ≠ 1, lie outside the quantifier ranges of I3 and I3-V. ∎


## Span Width Preservation

The point-level shift I3 lifts to a span-level property connecting this ASN to the span algebra framework of ASN-0053. Consider a level-uniform span σ = (s, ℓ) within the shifted region — that is, s ≥ p, subspace(s) = S, and #s = #ℓ = m with actionPoint(ℓ) = m. We call a span *ordinal-level* when its width acts purely at the deepest component: actionPoint(ℓ) = m. This is the natural class for I3-S — the ordinal shift δₙ acts at position m, and the commutativity argument requires the width to act at the same position. A width with actionPoint(ℓ) < m would change structure above the deepest ordinal: for the typical m = 2 case this changes the subspace identifier; for m > 2 it changes intermediate sub-structure within the subspace. In either case the width operates on a different axis than the shift, and the commutativity that I3-S depends on does not apply. The precondition is therefore definitional — it selects spans whose displacement arithmetic is compatible with ordinal shift. Define the shifted span σ' = (shift(s, n), ℓ). We verify that σ' is a well-formed span (T12, ASN-0034): ℓ > 0 is inherited from σ, and actionPoint(ℓ) = m ≤ #shift(s, n) = m (by TumblerAdd's result-length identity: #shift(s, n) = #δₙ = m).

**I3-S** — *SpanShiftPreservation* (LEMMA, introduced). For a level-uniform span σ = (s, ℓ) with s ≥ p, subspace(s) = S, #s = #ℓ = m, and actionPoint(ℓ) = m, the shifted span σ' = (shift(s, n), ℓ) satisfies:

(a) reach(σ') = shift(reach(σ), n)

(b) width(σ') = ℓ

*Derivation of (a).* We have reach(σ) = s ⊕ ℓ and reach(σ') = shift(s, n) ⊕ ℓ (SpanReach, ASN-0053). Expanding: reach(σ') = (s ⊕ δₙ) ⊕ ℓ. Both δₙ and ℓ have action point m, and m ≤ #s = m, m ≤ #δₙ = m, so TA-assoc (ASN-0034) applies: (s ⊕ δₙ) ⊕ ℓ = s ⊕ (δₙ ⊕ ℓ). By TumblerAdd, δₙ ⊕ ℓ = [0, …, 0, n + ℓₘ] since both operands have all zeros before position m; similarly ℓ ⊕ δₙ = [0, …, 0, ℓₘ + n]. These are equal by commutativity of natural-number addition. The reverse TA-assoc application (a = s, b = ℓ, c = δₙ) requires actionPoint(ℓ) ≤ #s and actionPoint(δₙ) ≤ #ℓ; both are m ≤ m. Applying: s ⊕ (ℓ ⊕ δₙ) = (s ⊕ ℓ) ⊕ δₙ = reach(σ) ⊕ δₙ. By S6 (LevelConstraint, ASN-0053), #reach(σ) = #s = m for level-uniform σ, so δₙ = δ(n, m) = δ(n, #reach(σ)) and reach(σ) ⊕ δₙ = shift(reach(σ), n). ∎

*Derivation of (b).* The span σ' is level-uniform: #shift(s, n) = m = #ℓ by the result-length identity of TumblerAdd. By D2 (WidthRecovery, ASN-0053), width(σ') = reach(σ') ⊖ start(σ'). From (a), reach(σ') = shift(reach(σ), n) and start(σ') = shift(s, n). Both shifted tumblers agree at positions 1 through m − 1 — shift copies these from the originals, and reach(σ) agrees with s at these positions since actionPoint(ℓ) = m — and differ at position m by (sₘ + ℓₘ + n) − (sₘ + n) = ℓₘ. By TumblerSub, the result is [0, …, 0, ℓₘ] = ℓ. ∎

*Verification against worked example.* From the insertion example above (p = [1, 3], n = 2, m = 2), take the span σ = ([1, 3], [0, 3]) covering the three pre-insertion positions [1, 3] through [1, 5]. Then reach(σ) = [1, 3] ⊕ [0, 3] = [1, 6], and the shifted span is σ' = (shift([1, 3], 2), [0, 3]) = ([1, 5], [0, 3]). For (a): reach(σ') = [1, 5] ⊕ [0, 3] = [1, 8], and shift(reach(σ), 2) = shift([1, 6], 2) = [1, 6] ⊕ [0, 2] = [1, 8]. ✓ For (b): width(σ') = [0, 3] = ℓ. ✓

Both endpoints of a within-subspace span shift by the same displacement δₙ; the width — the displacement between them — is invariant. This connects I3's point-level shift to ASN-0053's span framework: the displacement arithmetic underlying span endpoints (SpanReach) commutes with uniform ordinal translation.


## Ordinal Extraction

We frequently need to separate a V-position into its subspace identifier and its ordinal within that subspace. The foundation supplies the extraction, reconstruction, and projection functions.

**OrdinalExtraction** — *ord(v)* (cited, ASN-0036). For a V-position v with `#v = m ≥ 2`, `ord(v) = [v₂, ..., vₘ]` — the tumbler of length m − 1 obtained by stripping the subspace identifier. When v satisfies S8a, every component of ord(v) is positive.

**VPositionReconstruction** — *vpos(S, o)* (cited, ASN-0036). For subspace identifier `S ≥ 1` and ordinal `o = [o₁, ..., oₖ]` with `#o ≥ 1`, `vpos(S, o) = [S, o₁, ..., oₖ]`. These are inverses: `ord(vpos(S, o)) = o` and `vpos(subspace(v), ord(v)) = v`.

**OrdinalDisplacementProjection** — *w_ord* (cited, ASN-0036). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, `w_ord = [w₂, ..., wₘ]` — the tumbler of length m − 1 obtained by stripping the (zero) first component. When `Pos(w)` (TA-Pos, ASN-0034), `Pos(w_ord)` and `actionPoint(w_ord) = actionPoint(w) − 1`. At the restricted depth m = 2 (see D-SHIFT below), w = [0, c] for positive integer c, and w_ord = [c] with `Pos([c])`.

**Lemma — OrdinalOrderEquivalence** (LEMMA, derived). For V-positions v₁, v₂ with subspace(v₁) = subspace(v₂) = S and #v₁ = #v₂ = m ≥ 2:

`v₁ < v₂ ⟺ ord(v₁) < ord(v₂)`

*Derivation from T1.* The structure shared by v and ord is: (v₁)₁ = (v₂)₁ = S agrees at v's position 1, and ord(vᵢ)_j = (vᵢ)_{j+1} for 1 ≤ j ≤ m − 1 by the definition of ord — an index shift of +1 from ord-coordinates to v-coordinates. Both ordinals have length m − 1 since #v₁ = #v₂ = m.

For (⟹): if v₁ < v₂, T1 (ASN-0034) places the leftmost divergence at some v-position k. Position 1 agrees by hypothesis, so k ≥ 2, with (v₁)ₖ < (v₂)ₖ and (v₁)_j = (v₂)_j for 2 ≤ j < k. Translating through ord: ord(v₁) and ord(v₂) agree at ord-positions 1..k − 2 (carrying values (v₁)₂..(v₁)_{k − 1} = (v₂)₂..(v₂)_{k − 1}) and diverge at ord-position k − 1, where ord(v₁)_{k − 1} = (v₁)ₖ < (v₂)ₖ = ord(v₂)_{k − 1}. T1 on the length-(m − 1) ordinals delivers ord(v₁) < ord(v₂).

For (⟸): the argument is symmetric. If ord(v₁) < ord(v₂), T1 places the divergence at some ord-position j ≥ 1 with ord(v₁)_j < ord(v₂)_j, which corresponds to v-position j + 1 ≥ 2 with (v₁)_{j + 1} < (v₂)_{j + 1}. Position 1 of v already agrees, so this is the leftmost divergence in v, and T1 on v gives v₁ < v₂. ∎

**OrdAddHom** — *OrdinalAdditionHomomorphism* (cited, ASN-0036). For a V-position p with `#p = m ≥ 2` and a displacement w with `w₁ = 0`, `#w = m`, and `Pos(w)`:

- (a) `ord(p ⊕ w) = ord(p) ⊕ w_ord` — whole-tumbler addition commutes with ordinal extraction when the displacement has a zero first component.
- (b) `subspace(p ⊕ w) = subspace(p)` — the subspace identifier is preserved under any ordinal-zero-prefixed displacement.
- (c) `p ⊕ w = vpos(subspace(p), ord(p) ⊕ w_ord)` — the addition lifts cleanly through ord/vpos.

This three-part contract is the bridge between full-address arithmetic and ordinal-level arithmetic: clauses (a) and (c) license computation in either form, and (b) licenses the V-position reconstruction in D-SHIFT.


## Post-Contraction Shift

We work with V-positions in the text subspace of a document's arrangement. Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions to I-addresses. The text-subspace identifier is `S = 1`, and V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1} is the set of text-subspace V-positions of document d. Throughout this section we write `V_S(d)` with the understanding that `S = 1`; the symbol S is retained in formulas so the proofs make their subspace argument explicit, but the scope is fixed to the text subspace by the scoping axioms below. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**Scoping axioms.** Throughout this section, two restrictions apply.

*Subspace axiom: S = 1.* The contraction operation is defined only on the text subspace. The foundation's contiguity invariants D-CTG, D-MIN, and D-SEQ are explicit text-subspace constraints (ASN-0036): the link subspace V_2(d) is exempt and may be sparse with tombstones, so the shift-to-close-gap semantics that contraction implements is not the appropriate mutation for non-text subspaces (link-subspace mutation uses tombstoning instead, deferred to a future ASN). All citations of D-CTG, D-MIN, and D-SEQ below apply to V_1(d) by direct quotation of the foundation. The D-SHIFT well-definedness argument and the lemmas D-BJ, D-SEP, D-DP, D-CTG-post, D-MIN-post, D-SEQ-post, and S8-depth-post are likewise scoped to S = 1.

*Depth axiom: #p = 2.* V-positions in the text subspace have depth 2 (ordinal depth 1). This restricts the analysis to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially. The asymmetry with I3 (which is established at arbitrary m ≥ 2) is intentional, on three grounds.

*Structural necessity from TA4.* D-SEP's algebraic identity `ord(r) ⊖ w_ord = ord(p)` reduces to `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)`, an instance of TA4 (PartialInverse, ASN-0034). TA4's zero-prefix precondition `(A i : 1 ≤ i < k : aᵢ = 0)` — where a = ord(p) and k = actionPoint(w_ord) — requires zeros in ord(p) at positions before the action point. But S8a's componentwise positivity gives ord(p)ᵢ > 0 for all i, so the zero-prefix precondition is *only* vacuous when k = 1, i.e., when #ord(p) = 1, i.e., when #p = 2. The insertion proof of I3, by contrast, never invokes TA4: it relies only on TumblerAdd's prefix-copy behavior, which copies any prefix positions (zero or nonzero) unchanged. The two proofs use different arithmetic primitives with different preconditions, and the asymmetry is in those primitives.

*Design intent.* In Literary Machines, DELETEVSPAN is defined on byte-stream spans — sequences of bytes in a document's virtual byte stream (LM 4/11, 4/66). The "vspan" prefix on the operation name binds DELETE to the byte subspace, which corresponds to depth-2 ordinal V-positions in this formalism. Companion operations — INSERT shifting byte positions (LM 4/66), REARRANGE on regions of text (LM 4/67) — all operate at byte granularity within a single subspace. Hierarchical or cross-subspace contraction is not part of the FEBE operation set.

*Implementation reality.* In udanax-green, V-space addresses are hardcoded to two depths: depth-1 for text content (`mantissa[1] == 0`, `is1story(width)`) and depth-2 `N.1` for link endpoints (`setlinkvsas` at do2.c:169–183 always produces depth-2 tumblers). The two-blade knife mechanism (`findaddressofsecondcutforinsert`) computes the second blade as `(N+1).1` — a depth-2 address — regardless of insertion-point complexity, and `retrievevspansetpm` strips the second story unconditionally (correct only for depth 2). No code path constructs or contracts V-addresses at depth > 2; the `beheadtumbler` operation is applied only to depth-2 inputs and has no iteration mechanism for deeper addresses.

Generalization to deeper ordinals is noted as an open question. Deeper-depth contraction would require either a strengthened TA4 (admitting non-zero prefixes when the action point matches #a, which is not the lemma proved in ASN-0034) or a separate derivation of the partial-inverse identity from first principles using TumblerAdd and TumblerSub directly. Either route is substantive new analysis, and neither would correspond to any operation in the Xanadu design.

A contraction takes a document d and a contraction span (p, w) within the text subspace (S = 1, by the subspace scoping axiom) specifying the contiguous range of V-positions to remove. Let r = p ⊕ w denote the right cut point — the exclusive upper bound of the contraction.

**Contraction formal contract.**

*Preconditions:*

- `S = 1` (subspace scoping axiom) — contraction is defined only on the text subspace; the foundation's D-CTG, D-MIN, D-SEQ supply the contiguity preconditions only for V_1(d).
- `p ∈ V_1(d)` — p is a current V-position in the text subspace of document d.
- `Pos(w)` (TA-Pos, ASN-0034) — the contraction width is positive.
- `#w = #p` — the displacement has the same depth as p.
- `w₁ = 0` — the displacement preserves the subspace identifier under addition.
- `#p = 2` (depth scoping axiom) — V-positions have depth 2, restricting to single-component ordinals.
- Containment: with D-SEQ giving `V_1(d) = {[1, k] : 1 ≤ k ≤ N}` (ASN-0036, text subspace), the condition `p₂ + w₂ − 1 ≤ N` — the contraction span lies entirely within the current arrangement.

The contraction span (p, w) partitions V_S(d) into three disjoint, exhaustive regions.

**Definition — ThreeRegions.**

```
L = {v ∈ V_S(d) : v < p}            — left of contraction
X = {v ∈ V_S(d) : p ≤ v < r}        — the contracted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of contraction
```

By trichotomy of the total order (T1, ASN-0034), every v ∈ V_S(d) falls in exactly one region. Define Q₃ = {σ(v) : v ∈ R} as the set of shifted right-region positions, where σ is defined in D-SHIFT below. The post-state arrangement M'(d) is the arrangement after the contraction has been applied.

**D-SHIFT** — *RightShift* (POST, postcondition). Every position in the right region survives with its I-address mapping intact, but its V-position shifts left by w_ord. Define the shift function: for v ∈ R, let σ(v) = vpos(S, ord(v) ⊖ w_ord) — TumblerSub applied to the ordinal component, then reconstructed as a V-position.

*Preconditions:* As stated in the contraction formal contract: p ∈ V_S(d), #p = 2, Pos(w), #w = #p, w₁ = 0, containment satisfied. r = p ⊕ w; R = {v ∈ V_S(d) : v ≥ r}; M'(d) is the post-contraction arrangement.

*Postconditions:*

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

The shift is well-defined. For any v ∈ R, ord(v) ≥ ord(r) (since v ≥ r, by OrdinalOrderEquivalence). Since r = p ⊕ w, OrdAddHom (a) gives ord(r) = ord(p) ⊕ w_ord. The subtraction ord(v) ⊖ w_ord is well-defined by TA2 (SubtractionWellDefined, ASN-0034), which requires ord(v) ≥ w_ord. We establish this step by step. At depth #p = 2: ord(v) = [v₂], ord(p) = [p₂], w_ord = [c] with c = w₂ ≥ 1, and ord(r) = ord(p) ⊕ w_ord = [p₂ + c] (TumblerAdd). From v ≥ r and OrdinalOrderEquivalence, ord(v) ≥ ord(r) = [p₂ + c], i.e., v₂ ≥ p₂ + c (T1 at depth 1). Since p ∈ V_1(d), S8a gives p₂ ≥ 1, hence p₂ + c ≥ 1 + c > c (NAT-addcompat, ASN-0034). Transitivity of ≥ on ℕ yields v₂ ≥ c, equivalently ord(v) = [v₂] ≥ [c] = w_ord (T1 at depth 1). So TA2 applies and `[v₂] ⊖ [c] = [v₂ − c]` is well-defined. The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p) (verified in D-SEP below). Since p ∈ V_1(d) and S8a's componentwise positivity gives p₂ ≥ 1, ord(p) = [p₂] is positive. The reconstructed V-position σ(v) = vpos(S, ord(v) ⊖ w_ord) then satisfies S8a by vpos's S8a-closure postcondition (ASN-0036): S = 1 ≥ 1 and the ordinal is componentwise positive.

What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap. This is the two-space separation in action: the arrangement (Vstream) is modified while the content (Istream) remains invariant. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].

The contraction's effect on regions L and X, and on state outside subspace S and document d, must be stated explicitly.

**D-L** — *LeftPreservation* (FRAME, introduced). Positions in the left region are preserved unchanged:

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

**D-DOM** — *DomainCharacterization* (POST, introduced). The post-state arrangement within subspace S consists of exactly the preserved left region and the shifted right region:

`{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃`

Combined with D-L and D-SHIFT, this fully characterizes M'(d) within subspace S: positions in L retain their original I-address mappings, positions in Q₃ hold shifted mappings from R, and no other subspace-S positions exist in dom(M'(d)). The original X mappings are not preserved — any X address that reappears in Q₃ carries the shifted I-address from the corresponding R position, not its pre-contraction content.

D-DOM is needed as an independent closure clause, just as I3-CS is for insertion: without it, D-L and D-SHIFT alone would only constrain positions that were in the pre-state domain via the L and R partitions of V_S(d), leaving dom(M'(d)) ∩ subspace S underdetermined above — an M'(d) satisfying D-L and D-SHIFT could contain additional subspace-S positions at arbitrary depth or arbitrary X-positions carrying their pre-state I-addresses. D-DOM closes the domain from above by fixing exactly L ∪ Q₃; D-CS plays the parallel role for non-S subspaces of d, and D-CD for other documents.

**D-CS** — *CrossSubspaceFrame* (FRAME, introduced). Other subspaces are unchanged — their position sets are exactly the pre-state sets with the same mappings:

`(A S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'})`

`∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v))`

The first conjunct establishes domain equality per non-S subspace (no positions added or removed); the second establishes mapping equality (no values changed). Together they give the biconditional that the invariant proofs (D-CTG-post, D-MIN-post, S8-depth-post, S8a-post) require when citing D-CS for "unchanged" non-S subspaces.

**D-CD** — *CrossDocumentFrame* (FRAME, introduced). Other documents are unchanged:

`(A d' ≠ d : M'(d') = M(d'))`

**D-I** — *ContentStoreFrame* (FRAME, introduced). The content store is unchanged:

`Σ'.C = Σ.C`

That is, `dom(Σ'.C) = dom(Σ.C)` and `(A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`. Contraction modifies only the arrangement M(d); no I-addresses are allocated or deallocated, and no content values change. This is strictly stronger than S0 (ContentImmutability, ASN-0036), which permits `dom(Σ'.C) ⊃ dom(Σ.C)`. The exact equality matches the strength of D-CD and D-CS, and ensures that invariants over dom(Σ.C) — in particular S7a, S7b, S7c — are trivially preserved.

**Shift correctness.** We verify that the shift σ defined by D-SHIFT is well-behaved: order-preserving, injective, and gap-closing.

**D-BJ** — *ShiftBijectivity* (LEMMA, lemma). The map σ : R → Q₃ is an order-preserving bijection.

*Preconditions:* #p = 2 (scoping axiom); v₁, v₂ ∈ R with v₁ ≠ v₂ (for injectivity) or v₁ < v₂ (for order-preservation).

*Postconditions:*

- (a) Order-preservation: `v₁ < v₂ ⟹ σ(v₁) < σ(v₂)`
- (b) Injectivity: `v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂)`
- (c) Surjectivity: `Q₃ = {σ(v) : v ∈ R}`

*Proof of (a).* All ordinals in R share the same depth (S8-depth), giving #ord(v₁) = #ord(v₂). For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (by OrdinalOrderEquivalence — both share subspace S = 1 and depth m = 2).

We derive `ord(v) ≥ w_ord` step by step for every v ∈ R. At depth #p = 2 we have ord(p) = [p₂], w_ord = [c] with c = w₂ ≥ 1 (since Pos(w) and w₁ = 0 imply w₂ ≥ 1), and ord(r) = ord(p ⊕ w) = ord(p) ⊕ w_ord = [p₂ + c] by OrdAddHom(a). For any v ∈ R, v ≥ r (definition of R), so by OrdinalOrderEquivalence ord(v) ≥ ord(r) = [p₂ + c]. The ordinal comparison `[v₂] ≥ [p₂ + c]` at depth 1 is the natural-number comparison `v₂ ≥ p₂ + c` (by T1 at depth 1, which reduces to component-wise comparison). From p₂ ≥ 1 (S8a's componentwise positivity applied to p ∈ V_1(d) at position 2), we get `p₂ + c ≥ 1 + c > c` (NAT-addcompat, ASN-0034). Combining with `v₂ ≥ p₂ + c`, transitivity of ≥ on ℕ gives `v₂ ≥ c`. The depth-1 ordinal comparison `[v₂] ≥ [c]` is exactly this natural-number inequality, so `ord(v) = [v₂] ≥ [c] = w_ord`. ∎(derivation of `ord(v) ≥ w_ord`)

By TA3-strict (OrderPreservationSubtractionStrict, ASN-0034) — a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — with a = ord(v₁), b = ord(v₂), w = w_ord, and both `ord(v₁) ≥ w_ord` and `ord(v₂) ≥ w_ord` established by the derivation above, we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord. Now σ(v₁) and σ(v₂) share subspace S = 1 and depth m = 2, and ord(σ(v₁)) = ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord = ord(σ(v₂)); by the reverse direction of OrdinalOrderEquivalence, σ(v₁) < σ(v₂). ∎

*Proof of (b).* For v₁ ≠ v₂ in R, trichotomy (T1) gives v₁ < v₂ or v₂ < v₁. In either case, part (a) yields σ(v₁) < σ(v₂) or σ(v₂) < σ(v₁), so σ(v₁) ≠ σ(v₂). ∎

*Proof of (c).* Q₃ is defined as {σ(v) : v ∈ R}, so surjectivity holds by construction. ∎

**D-SEP** — *GapClosure* (LEMMA, lemma). The contraction width exactly bridges the ordinal distance between p and r, so shifting the right cut point back by the width recovers the ordinal of the left cut point. When R ≠ ∅, D-CTG ensures this algebraic identity has the semantic consequence that the shifted right region begins exactly where the left region ends.

*Preconditions:* #p = 2 (scoping axiom); r = p ⊕ w.

*Postconditions:*

- (a) Algebraic identity: `ord(r) ⊖ w_ord = ord(p)`.
- (b) When R ≠ ∅: by D-CTG, r = min(R) — the last element of X and some v ∈ R bracket r in V_S(d), so contiguity forces r ∈ V_S(d). Then σ(r) is well-defined and ord(σ(r)) = ord(p), i.e., min({ord(u) : u ∈ Q₃}) = ord(p).

*Proof of (a).* Since r = p ⊕ w, OrdAddHom (a) gives ord(r) = ord(p) ⊕ w_ord. The claim ord(r) ⊖ w_ord = ord(p) thus reduces to (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At our restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c]: the two sequences have equal length 1, divergence at position 1 where (p₂ + c) > c, giving r₁ = (p₂ + c) − c = p₂. Result: [p₂] = ord(p). ✓

This applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when Pos(w), the action point k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0). Here a = ord(p) and w = w_ord. The positivity Pos(w_ord) holds by the OrdinalDisplacementProjection postcondition (Pos(w) and w₁ = 0 imply Pos(w_ord)). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied.

*Proof of (b).* Suppose R ≠ ∅, so there exists v ∈ V_S(d) with v ≥ r. Two cases on the comparison of v with r.

*Case 1: v = r.* Then r = v ∈ V_S(d) directly.

*Case 2: v > r.* We establish r ∈ V_S(d) via D-CTG, using the last element of X as the lower bracket.

First, X is non-empty. Trivially p ≥ p, and p < r since r = p ⊕ w with Pos(w): by TumblerAdd, r differs from p only at position m where rₘ = pₘ + wₘ, and Pos(w) with w₁ = 0 forces wₘ ≥ 1 (the action point of w is at position m), so rₘ > pₘ, giving r > p (T1, divergence at position m). Hence p ∈ X, and X is non-empty.

Second, X has the explicit form `X = {[1, k] : p₂ ≤ k < p₂ + c}`, with c = w₂ ≥ 1. By D-SEQ on the pre-state V_1(d) (text subspace, ASN-0036), V_1(d) = {[1, k] : 1 ≤ k ≤ N}. The defining condition `p ≤ v < r` at depth 2 is, via OrdinalOrderEquivalence and T1 at depth 1, the natural-number condition `p₂ ≤ v₂ < p₂ + c` (since ord(r) = ord(p) ⊕ w_ord = [p₂ + c]). Intersecting with V_1(d) yields X = {[1, k] : p₂ ≤ k < p₂ + c, 1 ≤ k ≤ N}. The containment precondition `p₂ + w₂ − 1 ≤ N` ensures that all c values from p₂ through p₂ + c − 1 lie within [1, N], so X = {[1, k] : p₂ ≤ k < p₂ + c}.

Third, X has a last element under T1. Since c ≥ 1, the natural-number range [p₂, p₂ + c) is non-empty with maximum p₂ + c − 1, so the last element of X is [1, p₂ + c − 1]. We have [1, p₂ + c − 1] < r = [1, p₂ + c] by T1 at position 2 (p₂ + c − 1 < p₂ + c).

Fourth, applying D-CTG (text subspace, ASN-0036): with u = [1, p₂ + c − 1] ∈ V_1(d) and q = v ∈ V_1(d), where u < r < v (the first inequality just shown, the second by Case 2), D-CTG quantifies over all V-positions strictly between u and q with the same depth, demanding their membership in V_1(d). Since #r = 2 = #u and u < r < v = q with subspace(r) = 1, D-CTG gives r ∈ V_1(d) = V_S(d).

In both cases r ∈ R and r = min(R) (since r ≤ v for all v ∈ R by definition). By D-BJ, σ is order-preserving, so σ(r) = min(Q₃). By part (a), ord(σ(r)) = ord(p). ∎

**D-DP** — *DensePartition* (LEMMA, lemma). The post-state arrangement in subspace S is exactly the union of the preserved left region and the shifted right region, with no overlap and no gap at the contraction boundary.

*Preconditions:* #p = 2 (scoping axiom); L, X, R as defined by ThreeRegions; D-L, D-DOM, D-SHIFT, D-SEP, and D-CTG hold.

*Postconditions:*

- (a) No overlap: `L ∩ Q₃ = ∅`
- (b) Boundary adjacency: when R ≠ ∅, `min({ord(u) : u ∈ Q₃}) = ord(p)`, and `(A v ∈ L : ord(v) < ord(p))`

*Proof.* *Case R = ∅:* Q₃ = ∅ by definition, so L ∩ Q₃ = ∅ trivially. *Case R ≠ ∅:* Every v ∈ L satisfies v < p, hence ord(v) < ord(p) (by OrdinalOrderEquivalence — both share subspace S and depth m). By D-SEP(b), when R ≠ ∅ the minimum ordinal in Q₃ is ord(p), and by D-BJ every other element of Q₃ has ordinal strictly greater than ord(p). So every element of L has ordinal strictly less than ord(p) and every element of Q₃ has ordinal ≥ ord(p), giving L ∩ Q₃ = ∅.

The boundary is tight. At depth 2 with contiguous allocation (D-CTG), L contains exactly the positions with ordinals below ord(p), and Q₃ begins at ordinal ord(p) (D-SEP). The ordinals ord(p) − 1 and ord(p) are consecutive natural numbers; no ordinal falls between them. D-DOM confirms that the post-state domain in subspace S is exactly L ∪ Q₃. ∎

**Invariant preservation.** The postconditions and frame conditions above characterize the post-state arrangement. We now verify that the post-state satisfies the system invariants established in ASN-0036. The lemmas are ordered so that each cites only earlier ones: typing invariants (S8-depth-post, S8a-post) first, then the contiguity triple (D-CTG-post, D-MIN-post, D-SEQ-post), then finiteness (S8-fin-post), then functionality (S2-post), referential integrity (S3-post), and allocation invariants (S7-post).

**S8-depth-post** — *FixedDepthPreservation* (LEMMA, introduced). The post-state satisfies S8-depth: all V-positions within subspace S share the same depth.

*Proof.* Positions in L retain depth 2 (unchanged by D-L). Positions in Q₃ have depth 2: for v ∈ R, σ(v) = vpos(S, [vₘ − c]) = [S, vₘ − c], which has depth 2. By D-CS, other subspaces are unchanged and retain their pre-state depths. By D-CD, other documents are unchanged. ∎

**S8a-post** — *WellFormednessPreservation* (LEMMA, introduced). The post-state satisfies S8a: all V-positions are zero-free, of depth at least 2, and componentwise positive.

*Proof.* Positions in L satisfy S8a by the pre-state invariant and D-L (unchanged). Positions in Q₃: σ(v) = [S, vₘ − c] with S ≥ 1 (subspace identifier, S8a's componentwise positivity on v) and vₘ − c ≥ p₂ ≥ 1 (since vₘ ≥ p₂ + c for v ∈ R, and p₂ ≥ 1 by S8a on p). Both components are strictly positive, so zeros(σ(v)) = 0, #σ(v) = 2, and σ(v) is componentwise positive — full S8a. By D-CS, other subspaces are unchanged. By D-CD, other documents are unchanged. ∎

**D-CTG-post** — *VContiguityPreservation* (LEMMA, introduced). At S = 1 (subspace scoping axiom): the post-state V_1(d) is contiguous. For non-text subspaces, no D-CTG obligation is asserted (the foundation's D-CTG is text-subspace only); D-CS preserves V_S(d) (S ≠ 1) verbatim.

*Proof.* By D-SEQ (ASN-0036, text subspace), the pre-state V_1(d) = {[1, k] : 1 ≤ k ≤ N}. From the definition of L and D-SEQ on the pre-state,

`L = {[1, k] : 1 ≤ k < p₂}`.

By D-BJ, Q₃ is the order-preserving image of R under σ; applying σ([1, k]) = [1, k − c] to D-SEQ's R = {[1, k] : p₂ + c ≤ k ≤ N} gives

`Q₃ = {[1, k − c] : p₂ + c ≤ k ≤ N} = {[1, k] : p₂ ≤ k ≤ N − c}`.

The two index ranges are disjoint (k < p₂ in L, k ≥ p₂ in Q₃), and the natural numbers p₂ − 1 (the maximum of L's index range) and p₂ (the minimum of Q₃'s) are consecutive — no integer lies strictly between them — so

`L ∪ Q₃ = {[1, k] : 1 ≤ k < p₂} ∪ {[1, k] : p₂ ≤ k ≤ N − c} = {[1, k] : 1 ≤ k ≤ N − c}`.

The closed form covers all boundary configurations. When L = ∅: D-MIN (ASN-0036) gives min V_1(d) = [1, 1], so L = ∅ forces p = min V_1(d) = [1, 1] and p₂ = 1, vacating the L range and reducing the union to Q₃ = {[1, k] : 1 ≤ k ≤ N − c}. When R = ∅: no k ∈ [1, N] satisfies k ≥ p₂ + c, i.e., N < p₂ + c; combined with the containment precondition p₂ + c − 1 ≤ N this forces N = p₂ + c − 1, so N − c = p₂ − 1 and the union reduces to L = {[1, k] : 1 ≤ k ≤ p₂ − 1} = {[1, k] : 1 ≤ k ≤ N − c}. When both are empty, N − c = 0 and the set is empty.

We verify D-CTG's quantifier directly against V_1(d') = L ∪ Q₃ = {[1, k] : 1 ≤ k ≤ N − c}. Take u, q ∈ V_1(d') with u < q (both of depth 2 by S8-depth-post and subspace identifier 1 by S8a-post applied to V_1(d')), and any V-position v with subspace(v) = 1, #v = 2, and u < v < q. Write u = [1, kᵤ], q = [1, k_q], v = [1, k_v]. From u < v < q at depth 2 with shared subspace identifier 1, T1 reduces to the natural-number chain kᵤ < k_v < k_q. Membership of u and q in {[1, k] : 1 ≤ k ≤ N − c} gives 1 ≤ kᵤ and k_q ≤ N − c, so transitivity yields 1 ≤ k_v ≤ N − c, hence v = [1, k_v] ∈ V_1(d'). The interior point lies in V_1(d'), satisfying D-CTG.

Non-text subspaces: D-CS preserves V_S(d) (S ≠ 1) verbatim; the foundation imposes no D-CTG obligation there. By D-CD, other documents are unchanged. ∎

**D-MIN-post** — *VMinimumPreservation* (LEMMA, introduced). At S = 1 (subspace scoping axiom): when the post-state V_1(d) is non-empty, min(V_1(d)) = [1, 1]. When the post-state V_1(d) is empty, D-MIN holds vacuously. For non-text subspaces V_S(d) with S ≠ 1, no D-MIN obligation is asserted — the foundation's D-MIN is text-subspace only (ASN-0036), so cross-subspace preservation under D-CS suffices (any pre-state property of V_S(d), S ≠ 1, is preserved verbatim since D-CS fixes those positions and their mappings).

*Proof.* Three cases for S = 1. When L ≠ ∅: the pre-state minimum is min(V_1(d)) = [1, 1] (D-MIN, ASN-0036, text subspace). Since p > min(V_1(d)), we have min(V_1(d)) ∈ L. D-L preserves it, so min(L ∪ Q₃) = [1, 1]. When L = ∅ and R ≠ ∅: p = min(V_1(d)) = [1, 1] by D-MIN, so ord(p) = [1]. By D-SEP(b), min Q₃ has ordinal ord(p) = [1], giving min Q₃ = [1, 1]. When L = ∅ and R = ∅: V_1(d') = L ∪ Q₃ = ∅, so D-MIN holds vacuously. Non-text subspaces: D-CS preserves V_S(d) (S ≠ 1) verbatim; the foundation imposes no D-MIN obligation there, so nothing to verify. By D-CD, other documents are unchanged. ∎

**D-SEQ-post** — *SequentialPositionsPreservation* (LEMMA, introduced). At S = 1 (subspace scoping axiom): when the post-state V_1(d) is non-empty, V_1(d) = {[1, k] : 1 ≤ k ≤ N − c}. For non-text subspaces, no D-SEQ obligation is asserted (the foundation's D-SEQ is text-subspace only); D-CS preserves V_S(d) (S ≠ 1) verbatim.

*Proof.* The foundation's D-SEQ derivation (ASN-0036) takes four preconditions on V_1(d): contiguity (D-CTG), minimum at [1, 1] (D-MIN), uniform depth (S8-depth), and componentwise positivity (S8a). We verify each for the post-state, then derive n locally rather than re-invoking the foundation's text-only proof on what is now the post-state.

1. *Contiguity.* By D-CTG-post, V_1(d') = L ∪ Q₃ is contiguous.
2. *Minimum.* By D-MIN-post, when non-empty, min(V_1(d')) = [1, 1].
3. *Uniform depth.* By S8-depth-post, all V-positions in V_1(d') have depth 2.
4. *Componentwise positivity (S8a).* By S8a-post, every position in V_1(d') is zero-free, of depth ≥ 2, and componentwise positive — in particular, the position-2 component of every element is ≥ 1.

These four conditions reproduce the four preconditions cited in ASN-0036's D-SEQ derivation (Step 1 used S8a's componentwise positivity to validate the constructed intermediate w; Step 3 used contiguity (D-CTG) for the k-value range; Step 2 used D-MIN; and the depth uniformity threads throughout). Replaying the derivation locally at depth m = 2: L ∪ Q₃ is a contiguous set of depth-2 positions in subspace 1 with minimum [1, 1] and all components positive. Every position has the form [1, k] for some k ≥ 1 (Step 1: at m = 2 the shared-prefix component range is empty, vacuous). The k-values include 1 (Step 2, from D-MIN-post). The k-values form a contiguous range (Step 3, from D-CTG-post on L ∪ Q₃). The set is finite by S8-fin-post (proved below; D-SEQ-post does not depend on the value of n delivered by S8-fin-post, only on finiteness, so the forward citation is non-circular). Setting n = max(k-values), we get V_1(d') = {[1, k] : 1 ≤ k ≤ n}. It remains to identify n. The pre-state has N positions; the contraction removes c positions (the set X with |X| = c), so |L ∪ Q₃| = N − c. Hence n = N − c, and V_1(d') = {[1, k] : 1 ≤ k ≤ N − c}. When V_1(d') is empty (N − c = 0, i.e., the entire text subspace was contracted), D-SEQ holds vacuously.

Non-text subspaces: D-CS preserves V_S(d) (S ≠ 1) verbatim; the foundation imposes no D-SEQ obligation there. By D-CD, other documents are unchanged. ∎

**S8-fin-post** — *FiniteArrangementPreservation* (LEMMA, introduced). The post-state satisfies S8-fin: `dom(M'(d))` is finite.

*Proof.* By D-DOM, the subspace-S positions in dom(M'(d)) are L ∪ Q₃. L ⊆ V_S(d) and Q₃ = σ(R) with R ⊆ V_S(d), so |L ∪ Q₃| ≤ |V_S(d)|, which is finite by S8-fin on the pre-state. By D-CS, other subspaces of d retain their pre-state domains (finite by S8-fin). By D-CD, other documents are unchanged. ∎

**S2-post** — *ArrangementFunctionality* (LEMMA, introduced). The post-state M'(d) is a function.

*Proof.* By D-DOM, dom(M'(d)) within subspace S is L ∪ Q₃. By D-DP(a), L ∩ Q₃ = ∅. For v ∈ L, M'(d)(v) is uniquely determined by D-L. For v ∈ Q₃, v = σ(u) for a unique u ∈ R (D-BJ, injectivity), and M'(d)(v) = M(d)(u) is uniquely determined by D-SHIFT and S2 on the pre-state. Since the two regions are disjoint and each assigns a unique value, M'(d) is a function within subspace S. By D-CS, positions in other subspaces retain their pre-state mappings, functional by S2 on the pre-state. By D-CD, other documents are unchanged, and S2 holds by the pre-state invariant. ∎

**S3-post** — *ReferentialIntegrity* (LEMMA, introduced). The post-state satisfies `ran(M'(d)) ⊆ dom(Σ'.C)`.

*Proof.* Every I-address in ran(M'(d)) was an I-address in ran(M(d)): positions in L map to the same I-addresses as before (D-L), and positions in Q₃ map to I-addresses from R (D-SHIFT). By S3 on the pre-state, ran(M(d)) ⊆ dom(Σ.C). By D-I (content store frame), dom(Σ.C) ⊆ dom(Σ'.C). Hence the subspace-S contribution to ran(M'(d)) is contained in dom(Σ'.C). By D-CS, other subspaces of d retain their pre-state mappings, so their I-addresses are in ran(M(d)) ⊆ dom(Σ.C) ⊆ dom(Σ'.C). By D-CD, other documents are unchanged, so ran(M'(d')) = ran(M(d')) ⊆ dom(Σ'.C) by S3 on the pre-state. ∎

**S7-post** — *AllocationInvariantsPreservation* (LEMMA, introduced). The post-state satisfies S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), and S7c (ElementFieldDepth).

*Proof.* By D-I, `Σ'.C = Σ.C`, so `dom(Σ'.C) = dom(Σ.C)`. No new I-addresses exist in the post-state. S7a, S7b, and S7c are predicates over `dom(Σ.C)`; since this set is unchanged and the pre-state satisfies all three, the post-state satisfies them identically. ∎

### Worked Example

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

**Boundary case: R = ∅.** Same five-position arrangement. Contract at p = [1,4] with w = [0,2], so c = 2 and r = p ⊕ w = [1,6].

**Three-region partition.** L = {[1,1], [1,2], [1,3]}, X = {[1,4], [1,5]}, R = ∅.

**Shift computation.** R = ∅, so Q₃ = ∅.

**Post-state.** M'(d) = {[1,1] → i₁,  [1,2] → i₂,  [1,3] → i₃}

**Verification:**

- *D-L:* M'(d)([1,k]) = iₖ = M(d)([1,k]) for k ∈ {1,2,3}. ✓
- *D-SHIFT:* R = ∅, vacuously satisfied. ✓
- *D-DOM:* {v ∈ dom(M'(d)) : subspace(v) = 1} = {[1,1], [1,2], [1,3]} = L ∪ ∅ = L. ✓
- *D-DP:* L ∩ Q₃ = ∅ (Q₃ = ∅ since R = ∅). ✓
- *D-CTG-post:* {[1,1], [1,2], [1,3]} = {[1,k] : 1 ≤ k ≤ 3}, contiguous. ✓
- *D-MIN-post:* min L = [1,1] = [S, 1]. ✓
- *S8-depth-post:* All positions have depth 2 (unchanged from pre-state). ✓
- *S8a-post:* All positions in L satisfy S8a by pre-state invariant. ✓
- *S2-post:* Three distinct V-positions, each assigned a unique I-address. ✓
- *S3-post:* {i₁, i₂, i₃} ⊆ ran(M(d)) ⊆ dom(Σ.C) ⊆ dom(Σ'.C). ✓

**Boundary case: L = ∅ and R = ∅ (full deletion).** Same five-position arrangement. Contract at p = [1,1] with w = [0,5], so c = 5 and r = p ⊕ w = [1,6].

**Three-region partition.** L = ∅, X = {[1,1], [1,2], [1,3], [1,4], [1,5]}, R = ∅.

**Shift computation.** R = ∅, so Q₃ = ∅.

**Post-state.** M'(d) restricted to subspace 1 is empty: dom(M'(d)) ∩ {v : subspace(v) = 1} = ∅.

**Verification:**

- *D-L:* L = ∅, vacuously satisfied. ✓
- *D-SHIFT:* R = ∅, vacuously satisfied. ✓
- *D-DOM:* {v ∈ dom(M'(d)) : subspace(v) = 1} = ∅ = ∅ ∪ ∅ = L ∪ Q₃. ✓
- *D-DP:* L ∩ Q₃ = ∅ (Q₃ = ∅ since R = ∅). ✓
- *D-CTG-post:* V_S(d') = ∅, vacuously contiguous. ✓
- *D-MIN-post:* V_S(d') = ∅, D-MIN holds vacuously. ✓
- *S8-depth-post:* V_S(d') = ∅, S8-depth holds vacuously. ✓
- *S8a-post:* V_S(d') = ∅, S8a holds vacuously. ✓
- *S2-post:* No subspace-1 positions exist. ✓
- *S3-post:* No subspace-1 I-addresses to check. ✓

**Cross-subspace preservation: text contraction leaves link subspace untouched.** Consider document d with both text and link subspaces populated. The text subspace S = 1 has five contiguous positions; the link subspace S = 2 has two sparse positions (allowed by the foundation's frame note on D-CTG for V_2 — link positions may carry tombstones and need not be contiguous). All positions have depth 2.

M(d) = {[1,1] → i₁, [1,2] → i₂, [1,3] → i₃, [1,4] → i₄, [1,5] → i₅,  [2,5] → ℓ₁, [2,9] → ℓ₂}

Contract at p = [1,2] with w = [0,2]. Parameters: S = 1 (subspace scoping axiom), c = w₂ = 2, r = p ⊕ w = [1,4], #p = 2 (depth scoping axiom), Pos(w), w₁ = 0, containment p₂ + w₂ − 1 = 3 ≤ 5 = N. ✓

The contraction is defined only on the text subspace (subspace scoping axiom). The link subspace V_2(d) = {[2,5], [2,9]} is exempt from D-CTG, D-MIN, D-SEQ — it lies outside the contraction's quantifier ranges (D-SHIFT's R, D-L's L) since those are subsets of V_S(d) with S = 1. D-CS asserts both per-subspace domain equality and mapping equality across non-S subspaces.

**Three-region partition (text subspace only).** L = {[1,1]}, X = {[1,2], [1,3]}, R = {[1,4], [1,5]}.

**Shift computation.** w_ord = [2]. For each v ∈ R:

- σ([1,4]) = vpos(1, [4] ⊖ [2]) = vpos(1, [2]) = [1,2]
- σ([1,5]) = vpos(1, [5] ⊖ [2]) = vpos(1, [3]) = [1,3]

Q₃ = {[1,2], [1,3]}.

**Post-state.** M'(d) = {[1,1] → i₁, [1,2] → i₄, [1,3] → i₅,  [2,5] → ℓ₁, [2,9] → ℓ₂}

| V (before) | I (before) | V (after) | I (after) | Region |
|---|---|---|---|---|
| [1,1] | i₁ | [1,1] | i₁ | left (D-L) |
| [1,2] | i₂ | — (vacated) | — | contracted (X) |
| [1,3] | i₃ | — (vacated) | — | contracted (X) |
| [1,4] | i₄ | [1,2] | i₄ | shifted (D-SHIFT) |
| [1,5] | i₅ | [1,3] | i₅ | shifted (D-SHIFT) |
| [2,5] | ℓ₁ | [2,5] | ℓ₁ | cross-subspace (D-CS) |
| [2,9] | ℓ₂ | [2,9] | ℓ₂ | cross-subspace (D-CS) |

**Verification:**

- *D-L:* M'(d)([1,1]) = i₁ = M(d)([1,1]). ✓
- *D-SHIFT:* M'(d)([1,2]) = i₄ = M(d)([1,4]); M'(d)([1,3]) = i₅ = M(d)([1,5]). ✓
- *D-DOM:* {v ∈ dom(M'(d)) : subspace(v) = 1} = {[1,1], [1,2], [1,3]} = L ∪ Q₃. ✓
- *D-CS:* {v ∈ dom(M'(d)) : subspace(v) = 2} = {[2,5], [2,9]} = {v ∈ dom(M(d)) : subspace(v) = 2}; per-position mapping equality M'(d)([2,5]) = ℓ₁ = M(d)([2,5]) and M'(d)([2,9]) = ℓ₂ = M(d)([2,9]). The sparse link subspace is preserved verbatim — the tombstone gap at [2,6], [2,7], [2,8] remains. ✓
- *D-I:* dom(Σ'.C) = dom(Σ.C) and per-address values unchanged. The contraction modifies only M(d); no I-addresses are allocated or deallocated, and no link payloads are touched. ✓
- *D-BJ:* [1,4] < [1,5] and σ([1,4]) = [1,2] < [1,3] = σ([1,5]). ✓
- *D-SEP(a):* ord(r) ⊖ w_ord = [4] ⊖ [2] = [2] = ord(p). ✓
- *D-SEP(b):* min Q₃ = [1,2], ord([1,2]) = [2] = ord(p). ✓
- *D-DP:* L ∩ Q₃ = ∅; min Q₃ ordinal = [2] = ord(p); all L ordinals < ord(p). ✓
- *D-CTG-post:* V_1(d') = {[1,1], [1,2], [1,3]} = {[1,k] : 1 ≤ k ≤ 3}, contiguous. Non-text V_2(d') = {[2,5], [2,9]} preserved verbatim by D-CS — the foundation imposes no D-CTG obligation on V_2. ✓
- *D-MIN-post:* min V_1(d') = [1,1] = [S, 1]. Non-text V_2(d') preserved by D-CS — the foundation imposes no D-MIN obligation on V_2 ([2,5] is not [2,1] but D-MIN does not apply). ✓
- *D-SEQ-post:* V_1(d') = {[1,k] : 1 ≤ k ≤ N − c} = {[1,k] : 1 ≤ k ≤ 3}. Non-text V_2(d') preserved by D-CS — the foundation imposes no D-SEQ obligation on V_2 (the sparse {[2,5], [2,9]} is not of the form {[2,k] : 1 ≤ k ≤ n} but D-SEQ does not apply). ✓
- *S2-post:* Five distinct V-positions in dom(M'(d)), each assigned a unique I-address. ✓
- *S3-post:* {i₁, i₄, i₅, ℓ₁, ℓ₂} ⊆ ran(M(d)) ⊆ dom(Σ.C) (S3) = dom(Σ'.C) (D-I). ✓
- *S8-depth-post:* All seven post-state V-positions have depth 2 — text positions by D-L and shift's depth preservation, link positions by D-CS retaining pre-state depths. ✓
- *S8a-post:* All post-state V-positions are zero-free, depth 2, componentwise positive. ✓

The example exercises D-CS concretely: the link subspace V_2(d) — sparse with a tombstone gap, exempt from D-CTG/D-MIN/D-SEQ by the foundation — is unaffected by a text-subspace contraction. The text-subspace shift's `⊖ w_ord` displacement acts only on positions with subspace identifier equal to S = 1; link-subspace positions, having subspace identifier 2 ≠ 1, lie outside the quantifier ranges of D-SHIFT and D-L, and D-CS pins both their position set and their I-address mappings to the pre-state (D-DOM closes dom(M'(d)) within subspace S to L ∪ Q₃, while D-CS handles non-S subspaces). The contrast with the post-text-contraction text subspace V_1(d') = {[1,1], [1,2], [1,3]} (now contiguous and reindexed) versus the post-contraction link subspace V_2(d') = {[2,5], [2,9]} (still sparse, still tombstone-bearing) makes the per-subspace mutation discipline visible: one subspace shifts to close gaps, the other carries gaps as durable structure. ∎


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| M(d) | definition | M(d) : T ⇀ T — arrangement function mapping V-positions to I-addresses for document d | cited (ASN-0036) |
| subspace(v) | definition | subspace(v) = v₁ — the first component of a V-position, identifying its subspace | cited (ASN-0036) |
| ordinal-level | definition | A span σ = (s, ℓ) is ordinal-level when actionPoint(ℓ) = #s = #ℓ | introduced (local) |
| S8-depth | invariant | (A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂) — uniform V-position depth per subspace | cited (ASN-0036) |
| S8a | axiom | (A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0)) — V-position well-formedness | cited (ASN-0036) |
| I3 | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v)) | introduced |
| I3-L | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-X | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-D | frame | (A d' ≠ d : M'(d') = M(d')) | introduced |
| I3-V | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d))) | introduced |
| I3-C | frame | dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a)) — content store unchanged | introduced |
| I3-CS | postcondition | (A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : left-region ∨ shifted-image) — domain closure within subspace S | introduced |
| I3-CX | postcondition | (A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d))) — domain closure across subspaces | introduced |
| I3-VD | lemma | S8-depth preserved post-insertion across all subspaces: subspace S by left/shifted region analysis, other subspaces by I3-CX | derived |
| I3-VP | lemma | (A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0)) — S8a preserved post-insertion | derived |
| I3-S3 | lemma | (A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C')) — referential integrity preserved post-insertion | derived |
| I3-S2 | lemma | M'(d) is a function — S2 preserved post-insertion; pairwise disjointness of assignment regions ensures no double-assignment | derived |
| I3-fin | lemma | dom(M'(d)) is finite — S8-fin preserved post-insertion; domain closure (I3-CS, I3-CX) and injectivity (TS2) bound M'(d) by pre-state | derived |
| I3-S7 | lemma | S7a, S7b, S7c preserved post-insertion — trivially by I3-C (dom(C') = dom(C) and per-address values unchanged) | derived |
| I3-S | lemma | For level-uniform σ = (s, ℓ) with s ≥ p and actionPoint(ℓ) = m: reach((shift(s, n), ℓ)) = shift(reach(σ), n) and width preserved | introduced |
| OrdinalDisplacement | definition | δ(n, m) = [0, ..., 0, n] of length m, action point m | cited (ASN-0034) |
| OrdinalShift | definition | shift(v, n) = v ⊕ δ(n, #v) | cited (ASN-0034) |
| TS1 | lemma | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | cited (ASN-0034) |
| TS2 | lemma | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | cited (ASN-0034) |
| SpanReach | definition | reach(σ) = start(σ) ⊕ width(σ) | cited (ASN-0053) |
| TS4 | lemma | shift(v, n) > v for n ≥ 1 | cited (ASN-0034) |
| TA-assoc | lemma | (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) when both sides are well-defined | cited (ASN-0034) |
| TumblerAdd | definition | a ⊕ w: copy prefix, advance at action point, copy tail from w | cited (ASN-0034) |
| TumblerSub | definition | a ⊖ w: zero prefix, reverse at divergence, copy tail from a | cited (ASN-0034) |
| D2 | lemma | For level-uniform σ: reach(σ) ⊖ start(σ) = width(σ) | cited (ASN-0053) |
| S6 | lemma | For level-uniform σ: #reach(σ) = #s | cited (ASN-0053) |
| T12 | precondition | span(s, ℓ) well-formed when ℓ > 0 and actionPoint(ℓ) ≤ #s | cited (ASN-0034) |
| S2 | axiom | (A d, v : v ∈ dom(M(d)) : M(d)(v) is uniquely determined) — arrangement functionality | cited (ASN-0036) |
| S3 | invariant | (A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C)) — referential integrity | cited (ASN-0036) |
| S8-fin | invariant | For each document d, dom(M(d)) is finite | cited (ASN-0036) |
| S9 | lemma | Arrangement changes preserve content store (preservation direction) | cited (ASN-0036) |
| D-CTG | invariant | V_1(d) contiguity (text subspace only; V_2(d) exempt) — NOT preserved by shift alone | cited (ASN-0036) |
| D-MIN | invariant | min(V_1(d)) = [1, 1, ..., 1] (text subspace only) — NOT preserved by shift when p = min(V_1(d)) | cited (ASN-0036) |
| D-SEQ | lemma | V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n} (text subspace only) — NOT preserved by shift alone | cited (ASN-0036) |
| T4 | axiom | Address tumblers have ≤ 3 zeros as field separators; every field component strictly positive | cited (ASN-0034) |
| S0 | invariant | a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) — content immutability | cited (ASN-0036) |
| T1 | axiom | Lexicographic total order on tumblers | cited (ASN-0034) |
| TA2 | lemma | Subtraction well-defined when a ≥ w | cited (ASN-0034) |
| TA3-strict | lemma | a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — strict order preservation under subtraction | cited (ASN-0034) |
| TA4 | lemma | (a ⊕ w) ⊖ w = a — partial inverse of addition by subtraction | cited (ASN-0034) |
| ord(v) | definition | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier; precondition #v ≥ 2 | cited (ASN-0036) |
| vpos(S, o) | definition | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; preconditions #o ≥ 1, S ≥ 1; inverse of ord | cited (ASN-0036) |
| w_ord | definition | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0; preconditions #w ≥ 2, w₁ = 0 | cited (ASN-0036) |
| OrdinalOrderEquivalence | lemma | v₁ < v₂ ⟺ ord(v₁) < ord(v₂) when subspace(v₁) = subspace(v₂) ∧ #v₁ = #v₂ | introduced (derived from T1) |
| OrdAddHom | lemma | (a) ord(p ⊕ w) = ord(p) ⊕ w_ord; (b) subspace(p ⊕ w) = subspace(p); (c) p ⊕ w = vpos(subspace(p), ord(p) ⊕ w_ord). Preconditions: #p = m ≥ 2, w₁ = 0, #w = m, Pos(w) | cited (ASN-0036) |
| Contraction | operation | Remove span (p, w) from the text subspace of document d (S = 1 scoping axiom); preconditions: S = 1, p ∈ V_1(d), Pos(w), #w = #p, w₁ = 0, #p = 2, containment (p₂ + w₂ − 1 ≤ N); postconditions: D-SHIFT, D-DOM; frame: D-L, D-CS, D-CD, D-I | introduced |
| ThreeRegions | definition | L = {v ∈ V_S(d) : v < p}, X = {v ∈ V_S(d) : p ≤ v < r}, R = {v ∈ V_S(d) : v ≥ r}; partition of V_S(d) | introduced |
| Q₃ | definition | Q₃ = {σ(v) : v ∈ R} — the set of shifted right-region positions in the post-state | introduced |
| D-SHIFT | postcondition | (A v ∈ R : M'(d)(σ(v)) = M(d)(v)) where σ(v) = vpos(S, ord(v) ⊖ w_ord) | introduced |
| D-L | frame | (A v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| D-DOM | postcondition | {v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃ | introduced |
| D-CS | frame | (A S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'}) ∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v)) | introduced |
| D-CD | frame | Cross-document arrangements unchanged | introduced |
| D-I | frame | Σ'.C = Σ.C — content store unchanged (exact equality, strictly stronger than S0) | introduced |
| D-BJ | lemma | σ : R → Q₃ is an order-preserving bijection: (a) v₁ < v₂ ⟹ σ(v₁) < σ(v₂), (b) v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂), (c) Q₃ = {σ(v) : v ∈ R} | introduced |
| D-SEP | lemma | ord(r) ⊖ w_ord = ord(p); when R ≠ ∅, min Q₃ ordinal = ord(p) | introduced |
| D-DP | lemma | L ∩ Q₃ = ∅ and no residual gap at contraction boundary | introduced |
| S8-depth-post | lemma | Post-state V-positions in subspace S share depth 2 | introduced |
| S8a-post | lemma | Post-state V-positions are zero-free, of depth at least 2, and componentwise positive | introduced |
| D-CTG-post | lemma | At S = 1: post-state V_1(d) is contiguous; non-text subspaces preserved verbatim by D-CS | introduced |
| D-MIN-post | lemma | At S = 1: post-state min V_1(d) = [1, 1] when non-empty; vacuous when empty; non-text subspaces preserved verbatim by D-CS | introduced |
| D-SEQ-post | lemma | At S = 1: when post-state V_1(d) non-empty, V_1(d) = {[1, k] : 1 ≤ k ≤ N − c}; non-text subspaces preserved verbatim by D-CS | introduced |
| S8-fin-post | lemma | Post-state dom(M'(d)) is finite | introduced |
| S2-post | lemma | Post-state M'(d) is a function | introduced |
| S3-post | lemma | Post-state ran(M'(d)) ⊆ dom(Σ'.C) | introduced |
| S7-post | lemma | Post-state satisfies S7a, S7b, S7c — trivially by D-I (Σ'.C = Σ.C) | introduced |


## Open Questions

- When external state records a V-position, what must the system provide to allow that reference to be updated after a shift repositions it?
- Can the gap-closure formula (D-SEP) and dense partition (D-DP) be generalized to ordinals of depth greater than one while preserving the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment?
