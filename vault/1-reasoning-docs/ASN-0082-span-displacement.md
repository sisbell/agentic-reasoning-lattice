# ASN-0082: Span Displacement

*2026-04-09*

This ASN extends ASN-0053 (Span Algebra) with the post-insertion shift property: the guarantee that ordinal shift applied uniformly to arrangement positions at or beyond an insertion point preserves mapping values while relocating V-positions forward by a fixed displacement. The ordinal shift — defined by OrdinalShift and OrdinalDisplacement (ASN-0034) — is a fundamental operation on the tumbler line whose interaction with arrangement mappings determines how contiguous regions of mapped positions are repositioned without altering the content they reference. The property belongs in the span algebra domain because it characterizes how the displacement arithmetic underlying span endpoints (reach(σ) = start(σ) ⊕ width(σ)) behaves when applied as a uniform translation to a region of a partial function over the tumbler line.


## Foundation Invariants

This ASN relies on two foundation invariants from ASN-0036 governing V-position structure:

**S8-depth** — *FixedDepthVPositions* (cited, ASN-0036). `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`. All V-positions within a given subspace of a document share the same tumbler depth.

**S8a** — *VPositionWellFormedness* (cited, ASN-0036). `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`. V-positions are zero-free, have a positive subspace identifier, and are positive tumblers.

The contraction operation (below) additionally cites the following ASN-0036 properties:

- **S0** (ContentImmutability): for every state transition, `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`.
- **S2** (ArrangementFunctionality): each V-position in dom(M(d)) has a uniquely determined I-address.
- **S3** (ReferentialIntegrity): `ran(M(d)) ⊆ dom(Σ.C)`.
- **S8-fin** (FiniteArrangement): for each document d, dom(M(d)) is finite.
- **D-CTG** (VContiguity): within subspace S, V_S(d) is order-contiguous — `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`.
- **D-SEQ** (SequentialPositions): when V_S(d) is non-empty with common depth m ≥ 2, there exists n ≥ 1 such that V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}.
- **D-MIN** (VMinimumPosition): when V_S(d) is non-empty, min(V_S(d)) = [S, 1, ..., 1].


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

Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions (element-field tumblers in the Vstream) to I-addresses (element-field tumblers in the Istream). An operation that places n ≥ 1 new content elements at position p in document d within subspace S = subspace(p) = p₁ (with S ≥ 1) modifies M(d) to produce M'(d).

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

**I3-VD** — *PostInsertionDepthUniformity* (POSTCONDITION, introduced). S8-depth holds for the post-state M'(d) across all subspaces. For subspace S: `(A v₁, v₂ ∈ dom(M'(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂ = m)`. By I3-CS, every v ∈ dom(M'(d)) with subspace(v) = S falls into exactly one of two regions. *Left region* (I3-L): v ∈ dom(M(d)) with subspace(v) = S and v < p; these have depth m by S8-depth on M(d). *Shifted region* (I3): shift(v, n) for v ∈ dom(M(d)) with subspace(v) = S and v ≥ p; #shift(v, n) = #δₙ = m by the result-length identity of TumblerAdd, and #v = m by S8-depth on M(d). Both regions yield depth m. For any subspace S' ≠ S: by I3-CX, the positions in dom(M'(d)) with subspace S' are exactly the positions in dom(M(d)) with subspace S', on which S8-depth holds by hypothesis. ∎

**I3-VP** — *PostInsertionWellFormedness* (POSTCONDITION, introduced). `(A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`. By I3-CS and I3-CX, every v ∈ dom(M'(d)) falls into exactly one of three regions. *Left region* (I3-L): v ∈ dom(M(d)) with subspace(v) = S and v < p; S8a on M(d) gives zeros(v) = 0, v₁ ≥ 1, v > 0. *Shifted region* (I3): shift(v, n) for v ∈ dom(M(d)) with subspace(v) = S and v ≥ p; shift copies positions 1 through m − 1 from v (all nonzero by S8a on M(d)) and produces vₘ + n > 0 at position m, giving zeros(shift(v, n)) = 0; shift(v, n)₁ = v₁ ≥ 1 since shift copies position 1 from v when m ≥ 2; and shift(v, n) > 0 follows from v₁ ≥ 1 > 0. *Cross-subspace region* (I3-X): v ∈ dom(M(d)) with subspace(v) ≠ S; S8a on M(d) gives zeros(v) = 0, v₁ ≥ 1, v > 0. ∎

**I3-S3** — *PostInsertionReferentialIntegrity* (POSTCONDITION, introduced). `(A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C'))`. By I3-C, dom(C') = dom(C). Every v ∈ dom(M'(d)) has M'(d)(v) equal to some M(d)(u) for u ∈ dom(M(d)): shifted positions have M'(d)(shift(u, n)) = M(d)(u) by I3; left-region and cross-subspace positions have M'(d)(v) = M(d)(v) by I3-L and I3-X. By S3 (ReferentialIntegrity, ASN-0036) on the pre-state, M(d)(u) ∈ dom(C) = dom(C'). ∎

**I3-S2** — *PostInsertionFunctionality* (POSTCONDITION, introduced). `M'(d)` is a function — S2 (ArrangementFunctionality, ASN-0036) holds for the post-state. The consistency check above establishes pairwise disjointness of the three assignment regions (shifted, left, cross-subspace); since each region assigns exactly one value per position, no position in dom(M'(d)) receives two values. ∎

**I3-fin** — *PostInsertionFiniteness* (POSTCONDITION, introduced). `dom(M'(d))` is finite — S8-fin (FiniteArrangement, ASN-0036) holds for the post-state. By I3-CS and I3-CX, every position in dom(M'(d)) either belongs to dom(M(d)) directly (left-region or cross-subspace) or is shift(v, n) for some v ∈ dom(M(d)) with subspace(v) = S and v ≥ p. The shifted-image set is at most as large as the source set by injectivity (TS2, ASN-0034). Both contributing sets are subsets or injective images of dom(M(d)), which is finite by S8-fin on the pre-state; their union is therefore finite. ∎

**Arrangement invariants not preserved.** The shift preserves typing invariants (S8-depth, S8a, S3) but does *not* preserve the contiguity invariants of ASN-0036. The gap created by the shift — n vacated positions between the left region and the shifted region — violates D-CTG (VContiguity): the post-state V_S(d) is not contiguous, as the worked example confirms ({[1,1], [1,2], [1,5], [1,6], [1,7]} has a gap between [1,2] and [1,5]). D-SEQ (SequentialPositions) is likewise violated, since V_S(d) is no longer {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for any n. When p = min(V_S(d)), the shift vacates the minimum position, additionally violating D-MIN (VMinimumPosition). These violations are inherent to the shift's purpose: it opens a gap for new content. The INSERT ASN must re-establish D-CTG, D-MIN, and D-SEQ by filling the gap positions, alongside re-deriving S8-depth and S8a for the complete post-state.

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

We frequently need to separate a V-position into its subspace identifier and its ordinal within that subspace. Per the ordinal-only formulation of TA7a (ASN-0034), we define the extraction and reconstruction functions.

**Definition — OrdinalExtraction.** For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier.

*Precondition:* `#v ≥ 2`. When #v = 1, the result would be the empty sequence, which is not in T (T0 requires length ≥ 1).

*Postconditions:* `ord(v) ∈ T` with `#ord(v) = #v − 1 ≥ 1`.

*Order equivalence:* For V-positions v₁, v₂ with subspace(v₁) = subspace(v₂) = S and #v₁ = #v₂ = m ≥ 2:

`v₁ < v₂ ⟺ ord(v₁) < ord(v₂)`

Derivation from T1: since (v₁)₁ = (v₂)₁ = S, the lexicographic comparison (T1, ASN-0034) finds agreement at position 1. The divergence therefore occurs at some position k ≥ 2, and the ordering is determined entirely by positions 2 through m — which are exactly the components of ord(v₁) and ord(v₂). Since #v₁ = #v₂ implies #ord(v₁) = #ord(v₂), the comparison of the ordinals under T1 examines the same positions with the same values, giving an identical outcome. The biconditional follows: the forward direction strips the shared prefix; the reverse direction (equivalently, the corresponding property of vpos) restores it.

**Definition — VPositionReconstruction.** For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

*Preconditions:* `#o ≥ 1` (so the result has length ≥ 2 and is in T); `S ≥ 1` (a valid subspace identifier per S8a).

*Postconditions:* `vpos(S, o) ∈ T` with `#vpos(S, o) = #o + 1`.

These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

**Definition — OrdinalDisplacementProjection.** For a V-depth displacement w with w₁ = 0 and #w = m, the *ordinal displacement* is:

`w_ord = [w₂, ..., wₘ]`

of depth m − 1.

*Preconditions:* `#w ≥ 2`, `w₁ = 0`.

*Postconditions:* `w_ord ∈ T`, `#w_ord = #w − 1 ≥ 1`. When `w > 0`, `w_ord > 0`. (Since w > 0 and the first component is zero, at least one of w₂, ..., wₘ is nonzero, so w_ord is positive.)

At the restricted depth m = 2 (see D-SHIFT below), w = [0, c] for positive integer c, and w_ord = [c] with [c] > 0.

**Lemma — OrdinalAdditiveCompatibility.** For a V-position p with #p = m ≥ 2 and a displacement w with w₁ = 0, #w = m, and w > 0:

`ord(p ⊕ w) = ord(p) ⊕ w_ord`

Whole-tumbler addition commutes with ordinal extraction when the displacement has a zero first component. This is the bridge between full-address arithmetic (p ⊕ w) and ordinal-level arithmetic (ord(p) ⊕ w_ord): stripping the subspace identifier before or after addition gives the same result.

*Preconditions:* p ∈ T, w ∈ T, #p = m ≥ 2, #w = m, w₁ = 0, w > 0, actionPoint(w) ≤ #p.

*Proof.* Write p = [S, p₂, ..., pₘ] and w = [0, w₂, ..., wₘ]. Since w₁ = 0 and w > 0, the action point of w is k = min{i : 1 ≤ i ≤ m ∧ wᵢ ≠ 0} with k ≥ 2.

By TumblerAdd, p ⊕ w = [r₁, ..., rₘ] where rᵢ = pᵢ for i < k, rₖ = pₖ + wₖ, and rᵢ = wᵢ for i > k. Since k ≥ 2, position 1 is copied from p: r₁ = S. So p ⊕ w = [S, p₂, ..., p_{k−1}, pₖ + wₖ, w_{k+1}, ..., wₘ], and ord(p ⊕ w) = [p₂, ..., p_{k−1}, pₖ + wₖ, w_{k+1}, ..., wₘ].

Now consider ord(p) ⊕ w_ord. We have ord(p) = [p₂, ..., pₘ] (length m − 1) and w_ord = [w₂, ..., wₘ] (length m − 1). The action point of w_ord is k − 1 ≥ 1: the first nonzero component of w_ord is at position k − 1, since (w_ord)ⱼ = w_{j+1} and the first nonzero w_{j+1} occurs at j + 1 = k, i.e., j = k − 1. The precondition actionPoint(w_ord) ≤ #ord(p) holds: k − 1 ≤ m − 1, which follows from k ≤ m (actionPoint(w) ≤ #p). By TumblerAdd, ord(p) ⊕ w_ord = [q₁, ..., q_{m−1}] where qᵢ = (ord(p))ᵢ = p_{i+1} for i < k − 1, q_{k−1} = p_k + w_k, and qᵢ = (w_ord)ᵢ = w_{i+1} for i > k − 1. This gives [p₂, ..., p_{k−1}, pₖ + wₖ, w_{k+1}, ..., wₘ].

The two expressions are identical component by component. ∎

*Verification at m = 2.* Write p = [S, p₂] and w = [0, c] for positive integer c. Then k = 2, p ⊕ w = [S, p₂ + c], ord(p ⊕ w) = [p₂ + c]. And ord(p) ⊕ w_ord = [p₂] ⊕ [c] = [p₂ + c]. ✓


## Post-Contraction Shift

We work with V-positions within a subspace of a document's arrangement. Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions to I-addresses. Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**Scoping axiom.** Throughout this section, V-positions have depth #p = 2 (ordinal depth 1). This restricts the analysis to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially. Generalization to deeper ordinals is noted as an open question.

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

**D-SHIFT** — *RightShift* (POST, postcondition). Every position in the right region survives with its I-address mapping intact, but its V-position shifts left by w_ord. Define the shift function: for v ∈ R, let σ(v) = vpos(S, ord(v) ⊖ w_ord) — TumblerSub applied to the ordinal component, then reconstructed as a V-position.

*Preconditions:* As stated in the contraction formal contract: p ∈ V_S(d), #p = 2, w > 0, #w = #p, w₁ = 0, containment satisfied. r = p ⊕ w; R = {v ∈ V_S(d) : v ≥ r}; M'(d) is the post-contraction arrangement.

*Postconditions:*

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

The shift is well-defined. For any v ∈ R, ord(v) ≥ ord(r) (since v ≥ r, by the order equivalence of ord). Since r = p ⊕ w, OrdinalAdditiveCompatibility gives ord(r) = ord(p) ⊕ w_ord. The subtraction ord(v) ⊖ w_ord is well-defined by TA2 (SubtractionWellDefined, ASN-0034). At our restricted depth #p = 2: ord(v) = [vₘ] and w_ord = [c] for positive integer c, so [vₘ] ⊖ [c] = [vₘ − c] is well-defined when vₘ ≥ c, which holds since vₘ ≥ ord(r)₁ = pₘ + c. The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p) (verified in D-SEP below). Since p ∈ V_S(d) and S8a guarantees all components of every V-position are strictly positive, we have p₂ ≥ 1, hence ord(p) = [p₂] is positive. So the shifted V-position satisfies S8a.

What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap. This is the two-space separation in action: the arrangement (Vstream) is modified while the content (Istream) remains invariant. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].

The contraction's effect on regions L and X, and on state outside subspace S and document d, must be stated explicitly.

**D-L** — *LeftPreservation* (FRAME, introduced). Positions in the left region are preserved unchanged:

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

**D-DOM** — *DomainCharacterization* (POST, introduced). The post-state arrangement within subspace S consists of exactly the preserved left region and the shifted right region:

`{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃`

Combined with D-L and D-SHIFT, this fully characterizes M'(d) within subspace S: positions in L retain their original I-address mappings, positions in Q₃ hold shifted mappings from R, and no other subspace-S positions exist in dom(M'(d)). The original X mappings are not preserved — any X address that reappears in Q₃ carries the shifted I-address from the corresponding R position, not its pre-contraction content.

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

*Proof of (a).* All ordinals in R share the same depth (S8-depth), giving #ord(v₁) = #ord(v₂). For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (by the order equivalence of ord — both share subspace S and depth m). Both ordinals satisfy ord(v) ≥ w_ord (established above). By TA3-strict (OrderPreservationSubtractionStrict, ASN-0034) — a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord. Now σ(v₁) and σ(v₂) share subspace S and depth m, and ord(σ(v₁)) = ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord = ord(σ(v₂)); by the reverse direction of the order equivalence, σ(v₁) < σ(v₂). ∎

*Proof of (b).* For v₁ ≠ v₂ in R, trichotomy (T1) gives v₁ < v₂ or v₂ < v₁. In either case, part (a) yields σ(v₁) < σ(v₂) or σ(v₂) < σ(v₁), so σ(v₁) ≠ σ(v₂). ∎

*Proof of (c).* Q₃ is defined as {σ(v) : v ∈ R}, so surjectivity holds by construction. ∎

**D-SEP** — *GapClosure* (LEMMA, lemma). The contraction width exactly bridges the ordinal distance between p and r, so shifting the right cut point back by the width recovers the ordinal of the left cut point. When R ≠ ∅, D-CTG ensures this algebraic identity has the semantic consequence that the shifted right region begins exactly where the left region ends.

*Preconditions:* #p = 2 (scoping axiom); r = p ⊕ w.

*Postconditions:*

- (a) Algebraic identity: `ord(r) ⊖ w_ord = ord(p)`.
- (b) When R ≠ ∅: by D-CTG, r = min(R) — the last element of X and some v ∈ R bracket r in V_S(d), so contiguity forces r ∈ V_S(d). Then σ(r) is well-defined and ord(σ(r)) = ord(p), i.e., min({ord(u) : u ∈ Q₃}) = ord(p).

*Proof of (a).* Since r = p ⊕ w, OrdinalAdditiveCompatibility gives ord(r) = ord(p) ⊕ w_ord. The claim ord(r) ⊖ w_ord = ord(p) thus reduces to (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At our restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c]: the two sequences have equal length 1, divergence at position 1 where (p₂ + c) > c, giving r₁ = (p₂ + c) − c = p₂. Result: [p₂] = ord(p). ✓

This applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when w > 0, the action point k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0). Here a = ord(p) and w = w_ord. The positivity w_ord > 0 holds by the OrdinalDisplacementProjection postcondition (w > 0 and w₁ = 0 imply w_ord > 0). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied.

*Proof of (b).* Suppose R ≠ ∅, so there exists v ∈ V_S(d) with v ≥ r. Either v = r, so r ∈ V_S(d) directly, or v > r, in which case the last element of X (with ordinal ord(p) + c − 1) is in V_S(d), and v ∈ V_S(d) with v > r > last element of X, so D-CTG gives r ∈ V_S(d). In both cases r ∈ R and r = min(R) (since r ≤ v for all v ∈ R by definition). By D-BJ, σ is order-preserving, so σ(r) = min(Q₃). By part (a), ord(σ(r)) = ord(p). ∎

**D-DP** — *DensePartition* (LEMMA, lemma). The post-state arrangement in subspace S is exactly the union of the preserved left region and the shifted right region, with no overlap and no gap at the contraction boundary.

*Preconditions:* #p = 2 (scoping axiom); L, X, R as defined by ThreeRegions; D-L, D-DOM, D-SHIFT, D-SEP, and D-CTG hold.

*Postconditions:*

- (a) No overlap: `L ∩ Q₃ = ∅`
- (b) Boundary adjacency: when R ≠ ∅, `min({ord(u) : u ∈ Q₃}) = ord(p)`, and `(A v ∈ L : ord(v) < ord(p))`

*Proof.* Every v ∈ L satisfies v < p, hence ord(v) < ord(p) (by the order equivalence of ord — both share subspace S and depth m). By D-SEP(b), when R ≠ ∅ the minimum ordinal in Q₃ is ord(p), and by D-BJ every other element of Q₃ has ordinal strictly greater than ord(p). So every element of L has ordinal strictly less than ord(p) and every element of Q₃ has ordinal ≥ ord(p), giving L ∩ Q₃ = ∅.

The boundary is tight. At depth 2 with contiguous allocation (D-CTG), L contains exactly the positions with ordinals below ord(p), and Q₃ begins at ordinal ord(p) (D-SEP). The ordinals ord(p) − 1 and ord(p) are consecutive natural numbers; no ordinal falls between them. D-DOM confirms that the post-state domain in subspace S is exactly L ∪ Q₃. ∎

**Invariant preservation.** The postconditions and frame conditions above characterize the post-state arrangement. We now verify that the post-state satisfies the system invariants established in ASN-0036.

**S2-post** — *ArrangementFunctionality* (LEMMA, introduced). The post-state M'(d) is a function.

*Proof.* By D-DOM, dom(M'(d)) within subspace S is L ∪ Q₃. By D-DP(a), L ∩ Q₃ = ∅. For v ∈ L, M'(d)(v) is uniquely determined by D-L. For v ∈ Q₃, v = σ(u) for a unique u ∈ R (D-BJ, injectivity), and M'(d)(v) = M(d)(u) is uniquely determined by D-SHIFT and S2 on the pre-state. Since the two regions are disjoint and each assigns a unique value, M'(d) is a function within subspace S. By D-CS, positions in other subspaces retain their pre-state mappings, functional by S2 on the pre-state. By D-CD, other documents are unchanged, and S2 holds by the pre-state invariant. ∎

**S3-post** — *ReferentialIntegrity* (LEMMA, introduced). The post-state satisfies `ran(M'(d)) ⊆ dom(Σ'.C)`.

*Proof.* Every I-address in ran(M'(d)) was an I-address in ran(M(d)): positions in L map to the same I-addresses as before (D-L), and positions in Q₃ map to I-addresses from R (D-SHIFT). By S3 on the pre-state, ran(M(d)) ⊆ dom(Σ.C). By D-I (content store frame), dom(Σ.C) ⊆ dom(Σ'.C). Hence the subspace-S contribution to ran(M'(d)) is contained in dom(Σ'.C). By D-CS, other subspaces of d retain their pre-state mappings, so their I-addresses are in ran(M(d)) ⊆ dom(Σ.C) ⊆ dom(Σ'.C). By D-CD, other documents are unchanged, so ran(M'(d')) = ran(M(d')) ⊆ dom(Σ'.C) by S3 on the pre-state. ∎

**D-CTG-post** — *VContiguityPreservation* (LEMMA, introduced). The post-state V_S(d) is contiguous.

*Proof.* By D-SEQ, the pre-state V_S(d) = {[S, k] : 1 ≤ k ≤ N}. L consists of positions with ordinals strictly less than ord(p) — by D-CTG on the pre-state, L = {[S, k] : 1 ≤ k < p₂}, which is contiguous. Q₃ is the order-preserving image of R under σ (D-BJ). R = {[S, k] : p₂ + c ≤ k ≤ N} is contiguous, and σ shifts each ordinal by −c, giving Q₃ = {[S, k − c] : p₂ + c ≤ k ≤ N} = {[S, k] : p₂ ≤ k ≤ N − c}. This is contiguous.

Three cases arise at the boundary. When L ≠ ∅ and R ≠ ∅: L's maximum ordinal is p₂ − 1 and Q₃'s minimum ordinal is p₂ (D-SEP(b)), which are adjacent, so L ∪ Q₃ is contiguous. When L = ∅ and R ≠ ∅: Q₃ alone is contiguous. When R = ∅: Q₃ = ∅, so L ∪ Q₃ = L, which is contiguous (or empty when L = ∅ as well, which is vacuously contiguous). By D-CS, other subspaces of d retain their pre-state position sets and satisfy D-CTG by the pre-state invariant. By D-CD, other documents are unchanged. ∎

**D-MIN-post** — *VMinimumPreservation* (LEMMA, introduced). When the post-state subspace S is non-empty, the minimum V-position is [S, 1, ..., 1]. When the post-state subspace S is empty, D-MIN holds vacuously.

*Proof.* Three cases. When L ≠ ∅: the pre-state minimum is min(V_S(d)) = [S, 1] (D-MIN). Since p > min(V_S(d)), we have min(V_S(d)) ∈ L. D-L preserves it, so min(L ∪ Q₃) = [S, 1]. When L = ∅ and R ≠ ∅: p = min(V_S(d)) = [S, 1] by D-MIN, so ord(p) = [1]. By D-SEP(b), min Q₃ has ordinal ord(p) = [1], giving min Q₃ = [S, 1]. When L = ∅ and R = ∅: V_S(d') = L ∪ Q₃ = ∅, so D-MIN holds vacuously — no non-empty subspace to constrain. By D-CS, other subspaces of d retain their pre-state position sets and satisfy D-MIN by the pre-state invariant. By D-CD, other documents are unchanged. ∎

**D-SEQ-post** — *SequentialPositionsPreservation* (LEMMA, introduced). When the post-state V_S(d) is non-empty, V_S(d) = {[S, k] : 1 ≤ k ≤ N − c}.

*Proof.* By D-CTG-post, the post-state V_S(d) = L ∪ Q₃ is contiguous. By D-MIN-post, when non-empty, min(V_S(d)) = [S, 1]. By S8-depth-post (below), all V-positions in subspace S have depth 2. These three conditions — contiguity, minimum at [S, 1], and uniform depth 2 — are exactly the preconditions of the D-SEQ derivation (ASN-0036): contiguity at depth 2 with minimum [S, 1] yields V_S(d) = {[S, k] : 1 ≤ k ≤ n} for some n ≥ 1. It remains to identify n. The pre-state has N positions; the contraction removes c positions (the set X with |X| = c), so |L ∪ Q₃| = N − c. Hence n = N − c, and V_S(d) = {[S, k] : 1 ≤ k ≤ N − c}. When V_S(d) is empty (N − c = 0, i.e., the entire subspace was contracted), D-SEQ holds vacuously. ∎

**S8-depth-post** — *FixedDepthPreservation* (LEMMA, introduced). The post-state satisfies S8-depth: all V-positions within subspace S share the same depth.

*Proof.* Positions in L retain depth 2 (unchanged by D-L). Positions in Q₃ have depth 2: for v ∈ R, σ(v) = vpos(S, [vₘ − c]) = [S, vₘ − c], which has depth 2. By D-CS, other subspaces are unchanged and retain their pre-state depths. By D-CD, other documents are unchanged. ∎

**S8a-post** — *WellFormednessPreservation* (LEMMA, introduced). The post-state satisfies S8a: all V-positions are zero-free and positive.

*Proof.* Positions in L satisfy S8a by the pre-state invariant and D-L (unchanged). Positions in Q₃: σ(v) = [S, vₘ − c] with S ≥ 1 (subspace identifier, S8a on v) and vₘ − c ≥ p₂ ≥ 1 (since vₘ ≥ p₂ + c for v ∈ R, and p₂ ≥ 1 by S8a on p). Both components are strictly positive, so zeros(σ(v)) = 0 and σ(v) > 0. By D-CS, other subspaces are unchanged. By D-CD, other documents are unchanged. ∎

**S8-fin-post** — *FiniteArrangementPreservation* (LEMMA, introduced). The post-state satisfies S8-fin: `dom(M'(d))` is finite.

*Proof.* By D-DOM, the subspace-S positions in dom(M'(d)) are L ∪ Q₃. L ⊆ V_S(d) and Q₃ = σ(R) with R ⊆ V_S(d), so |L ∪ Q₃| ≤ |V_S(d)|, which is finite by S8-fin on the pre-state. By D-CS, other subspaces of d retain their pre-state domains (finite by S8-fin). By D-CD, other documents are unchanged. ∎

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
- *D-CTG-post:* V_S(d') = ∅, vacuously contiguous. ✓
- *D-MIN-post:* V_S(d') = ∅, D-MIN holds vacuously. ✓
- *S8-depth-post:* V_S(d') = ∅, S8-depth holds vacuously. ✓
- *S8a-post:* V_S(d') = ∅, S8a holds vacuously. ✓
- *S2-post:* No subspace-1 positions exist. ✓
- *S3-post:* No subspace-1 I-addresses to check. ✓


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| M(d) | definition | M(d) : T ⇀ T — arrangement function mapping V-positions to I-addresses for document d | cited (ASN-0036) |
| subspace(v) | definition | subspace(v) = v₁ — the first component of a V-position, identifying its subspace | cited (ASN-0036) |
| ordinal-level | definition | A span σ = (s, ℓ) is ordinal-level when actionPoint(ℓ) = #s = #ℓ | introduced (local) |
| S8-depth | invariant | (A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂) — uniform V-position depth per subspace | cited (ASN-0036) |
| S8a | axiom | (A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0) — V-position well-formedness | cited (ASN-0036) |
| I3 | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v)) | introduced |
| I3-L | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-X | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-D | frame | (A d' ≠ d : M'(d') = M(d')) | introduced |
| I3-V | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d))) | introduced |
| I3-C | frame | dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a)) — content store unchanged | introduced |
| I3-CS | postcondition | (A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : left-region ∨ shifted-image) — domain closure within subspace S | introduced |
| I3-CX | postcondition | (A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d))) — domain closure across subspaces | introduced |
| I3-VD | postcondition | S8-depth preserved post-insertion across all subspaces: subspace S by left/shifted region analysis, other subspaces by I3-CX | introduced |
| I3-VP | postcondition | (A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0) — S8a preserved post-insertion | introduced |
| I3-S3 | postcondition | (A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C')) — referential integrity preserved post-insertion | introduced |
| I3-S2 | postcondition | M'(d) is a function — S2 preserved post-insertion; pairwise disjointness of assignment regions ensures no double-assignment | introduced |
| I3-fin | postcondition | dom(M'(d)) is finite — S8-fin preserved post-insertion; domain closure (I3-CS, I3-CX) and injectivity (TS2) bound M'(d) by pre-state | introduced |
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
| D-CTG | invariant | V-position contiguity within subspace — NOT preserved by shift alone | cited (ASN-0036) |
| D-MIN | invariant | V-position minimum at [S, 1, ..., 1] — NOT preserved by shift when p = min(V_S(d)) | cited (ASN-0036) |
| D-SEQ | lemma | Sequential V-position structure — NOT preserved by shift alone | cited (ASN-0036) |
| T4 | axiom | Address tumblers have ≤ 3 zeros as field separators; every field component strictly positive | cited (ASN-0034) |
| S0 | invariant | a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) — content immutability | cited (ASN-0036) |
| T1 | axiom | Lexicographic total order on tumblers | cited (ASN-0034) |
| TA2 | lemma | Subtraction well-defined when a ≥ w | cited (ASN-0034) |
| TA3-strict | lemma | a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w — strict order preservation under subtraction | cited (ASN-0034) |
| TA4 | lemma | (a ⊕ w) ⊖ w = a — partial inverse of addition by subtraction | cited (ASN-0034) |
| ord(v) | definition | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier; precondition #v ≥ 2; postconditions: ord(v) ∈ T with #ord(v) = #v − 1; order equivalence: v₁ < v₂ ⟺ ord(v₁) < ord(v₂) when subspace(v₁) = subspace(v₂) ∧ #v₁ = #v₂ | introduced |
| vpos(S, o) | definition | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; preconditions #o ≥ 1, S ≥ 1; postcondition vpos(S, o) ∈ T with #vpos(S, o) = #o + 1; inverse of ord | introduced |
| w_ord | definition | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0; preconditions: #w ≥ 2, w₁ = 0; postconditions: w_ord ∈ T, #w_ord = #w − 1 ≥ 1, w > 0 ⟹ w_ord > 0 | introduced |
| OrdinalAdditiveCompatibility | lemma | ord(p ⊕ w) = ord(p) ⊕ w_ord when w₁ = 0, #w = #p, w > 0, actionPoint(w) ≤ #p; holds for all m ≥ 2 | introduced |
| Contraction | operation | Remove span (p, w) from subspace S of document d; preconditions: p ∈ V_S(d), w > 0, #w = #p, w₁ = 0, #p = 2, containment (p₂ + w₂ − 1 ≤ N); postconditions: D-SHIFT, D-DOM; frame: D-L, D-CS, D-CD, D-I | introduced |
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
| S2-post | lemma | Post-state M'(d) is a function | introduced |
| S3-post | lemma | Post-state ran(M'(d)) ⊆ dom(Σ'.C) | introduced |
| D-CTG-post | lemma | Post-state V_S(d) is contiguous | introduced |
| D-MIN-post | lemma | Post-state min V_S(d) = [S, 1, ..., 1] when non-empty; vacuous when empty | introduced |
| D-SEQ-post | lemma | When post-state V_S(d) non-empty, V_S(d) = {[S, k] : 1 ≤ k ≤ N − c} | introduced |
| S8-depth-post | lemma | Post-state V-positions in subspace S share depth 2 | introduced |
| S8a-post | lemma | Post-state V-positions are zero-free and positive | introduced |
| S8-fin-post | lemma | Post-state dom(M'(d)) is finite | introduced |
| S7-post | lemma | Post-state satisfies S7a, S7b, S7c — trivially by D-I (Σ'.C = Σ.C) | introduced |


## Open Questions

- When external state records a V-position, what must the system provide to allow that reference to be updated after a shift repositions it?
- Can the gap-closure formula (D-SEP) and dense partition (D-DP) be generalized to ordinals of depth greater than one while preserving the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment?
