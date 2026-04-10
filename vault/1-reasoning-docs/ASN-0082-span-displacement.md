# ASN-0082: Span Displacement

*2026-04-09*

This ASN extends ASN-0053 (Span Algebra) with the post-insertion shift property: the guarantee that ordinal shift applied uniformly to arrangement positions at or beyond an insertion point preserves mapping values while relocating V-positions forward by a fixed displacement. The ordinal shift — defined by OrdinalShift and OrdinalDisplacement (ASN-0034) — is a fundamental operation on the tumbler line whose interaction with arrangement mappings determines how contiguous regions of mapped positions are repositioned without altering the content they reference. The property belongs in the span algebra domain because it characterizes how the displacement arithmetic underlying span endpoints (reach(σ) = start(σ) ⊕ width(σ)) behaves when applied as a uniform translation to a region of a partial function over the tumbler line.


## Foundation Invariants

This ASN relies on two foundation invariants from ASN-0036 governing V-position structure:

**S8-depth** — *FixedDepthVPositions* (cited, ASN-0036). `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`. All V-positions within a given subspace of a document share the same tumbler depth.

**S8a** — *VPositionWellFormedness* (cited, ASN-0036). `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`. V-positions are zero-free, have a positive subspace identifier, and are positive tumblers.


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

Both endpoints of a within-subspace span shift by the same displacement δₙ; the width — the displacement between them — is invariant. This connects I3's point-level shift to ASN-0053's span framework: the displacement arithmetic underlying span endpoints (SpanReach) commutes with uniform ordinal translation.


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


## Open Questions

- When external state records a V-position, what must the system provide to allow that reference to be updated after a shift repositions it?
