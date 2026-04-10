# ASN-0082: Span Displacement

*2026-04-09*

This ASN extends ASN-0053 (Span Algebra) with the post-insertion shift property: the guarantee that ordinal shift applied uniformly to arrangement positions at or beyond an insertion point preserves mapping values while relocating V-positions forward by a fixed displacement. The ordinal shift — defined by OrdinalShift and OrdinalDisplacement (ASN-0034) — is a fundamental operation on the tumbler line whose interaction with arrangement mappings determines how contiguous regions of mapped positions are repositioned without altering the content they reference. The property belongs in the span algebra domain because it characterizes how the displacement arithmetic underlying span endpoints (reach(σ) = start(σ) ⊕ width(σ)) behaves when applied as a uniform translation to a region of a partial function over the tumbler line.


## Local Axioms

**VB** — *BootstrapDiscipline* (AXIOM, local). All V-positions in dom(M(d)) within a subspace are produced exclusively by a single allocator's sibling stream (`inc(·, 0)` only). The allocator's prefix is established by a bootstrap phase — one or more child-spawning increments (`inc(·, k')` with `k' > 0`) that create structural nesting (e.g., D.0.1 for text, establishing an atom-type discriminator and serial-counter prefix). Bootstrap-established prefixes are structural scaffolding; they do not appear in dom(M(d)). No child-spawning occurs after the bootstrap prefix is established. The nesting depth of the bootstrap is not constrained to a particular value — only the consequence matters: every V-position that enters dom(M(d)) is a sibling-stream output at the same allocator depth.

**VD** — *UniformVPositionDepth* (LEMMA, local). All V-positions within a given subspace of a document share the same tumbler depth:

`(A v₁, v₂ ∈ dom(M(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂)`

Since VB requires every V-position in dom(M(d)) within a subspace to be a sibling-stream output from a single allocator — with bootstrap prefixes excluded from dom(M(d)) — and sibling outputs have uniform length (T10a.1, ASN-0034), all V-positions within a subspace share the same depth.

**VP** — *PositiveSubspace* (AXIOM, local). The subspace identifier of every V-position is positive:

`(A v ∈ dom(M(d)) : subspace(v) = v₁ ≥ 1)`

The subspace identifier occupies the first component of the element field, which is strictly positive by the T4 positive-component constraint (ASN-0034).


## The Ordinal Shift

The *ordinal displacement* δ(n, m) is defined in the foundation: for n ≥ 1 and m ≥ 1, δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m (OrdinalDisplacement, ASN-0034).

When the depth is determined by context (typically m = #p for insertion position p), we write δₙ.

The *ordinal shift* is defined in the foundation: for a V-position v of depth m and n ≥ 1, shift(v, n) = v ⊕ δ(n, m) (OrdinalShift, ASN-0034). By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the ordinal within the V-position's subspace by exactly n, leaving all higher-level components unchanged.

We need two properties of this shift. Both are established in the foundation.

Order preservation is guaranteed: for v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂, shift(v₁, n) < shift(v₂, n) (TS1, ASN-0034).

The relative ordering of content is preserved through the shift. What was before other content remains before it after insertion — Nelson's guarantee that content appears "in its original relative order on either side" (Q2).

Injectivity is likewise guaranteed: for v₁, v₂ with #v₁ = #v₂ = m, shift(v₁, n) = shift(v₂, n) implies v₁ = v₂ (TS2, ASN-0034).

Injectivity ensures the shift creates no collisions: distinct V-positions remain distinct after shifting.

Additionally, shift preserves structural properties. Subspace preservation requires m ≥ 2: by TumblerAdd (ASN-0034), positions before the action point are copied from v — for δₙ with action point k = m, positions i < k are copied from v — so when m ≥ 2, position 1 (the subspace identifier) is preserved: shift(v, n)₁ = v₁, giving subspace(shift(v, n)) = subspace(v). When m = 1, shift([S], n) = [S + n] changes the subspace identifier; we exclude this by requiring #p ≥ 2 as an operation precondition. By VD, all V-positions in subspace S share a uniform depth d; the depth-compatibility precondition on I3 requires d = #p when such V-positions exist, so m = d = #p ≥ 2 holds for every V-position in the shifted region. This also ensures that the comparison v ≥ p in I3's quantifier is between equal-length tumblers, giving it the clean "at or to the right of p" semantics without prefix-case ambiguity. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves two distinct positivity properties: the positive-component constraint (T4) is maintained because vₘ + n > 0 whenever vₘ ≥ 1 (T4 guarantees all element-field components are positive); VP is preserved because shift copies position 1 from v when m ≥ 2, giving shift(v, n)₁ = v₁ ≥ 1.


## Post-Insertion Shift

Let M(d) : T ⇀ T denote the arrangement function for document d — a partial map from V-positions (element-field tumblers in the Vstream) to I-addresses (element-field tumblers in the Istream). An operation that places n ≥ 1 new content elements at position p in document d within subspace S = subspace(p) = p₁ (with S ≥ 1) modifies M(d) to produce M'(d).

**I3** — *PostInsertionShift* (POSTCONDITION, introduced). Content at or beyond p shifts forward by n ordinal positions.

*Preconditions:* d is a document; M(d) : T ⇀ T is its arrangement; p ∈ T with #p ≥ 2 and subspace(p) = S ≥ 1; depth-compatible: if {v ∈ dom(M(d)) : subspace(v) = S} ≠ ∅ then #p = #v for any such v (unique depth by VD); n ≥ 1; M'(d) is the post-insertion arrangement.

*Postconditions:*

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

- I3-V (vacating): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d)))`

*Frame:*

- I3-L (left region): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`
- I3-X (cross-subspace): `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`
- I3-D (cross-document): `(A d' ≠ d : M'(d') = M(d'))`

The I-address is unchanged — only the V-position moves. This is Nelson's central guarantee (Q1, Q5): the permanent identity of every existing byte is invariant under insertion. "Since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. The shift moves content in the document's arrangement without touching the content's identity in the store. The left-region frame (I3-L) ensures that content before the insertion point is undisturbed. The cross-subspace frame (I3-X) ensures that link subspaces and other subspaces are unaffected by a text-subspace insertion. The cross-document frame (I3-D) ensures that other documents are unchanged. The vacating postcondition (I3-V) completes the shift semantics: original positions at or beyond p that are not the destination of any shifted content are removed from dom(M'(d)), preventing content duplication in sparse arrangements. Without I3-V, an implementation could retain M'(d)(v) = M(d)(v) alongside M'(d)(shift(v, n)) = M(d)(v), duplicating content at both the original and shifted positions.

**Consistency.** We verify that the five clauses are mutually consistent, ensuring M'(d) is a well-defined partial function. The assignment clauses I3, I3-L, and I3-X specify positions that *are* in dom(M'(d)) with defined values; I3-V specifies positions that are *not* in dom(M'(d)). We must check both pairwise disjointness of the assignment regions and that I3-V's vacated positions do not overlap any assignment region. *Shifted vs left*: for v ≥ p in subspace S, shift(v, n) > v ≥ p by TS4 (ASN-0034), so shift(v, n) > p > u for every u < p; no shifted output coincides with a left-region position. *Shifted vs shifted*: TS2 (injectivity) guarantees distinct v's produce distinct shift(v, n)'s. *Shifted vs cross-subspace*: subspace preservation (shift(v, n)₁ = v₁ = S when m ≥ 2) ensures shifted positions remain in subspace S, disjoint from I3-X positions (subspace ≠ S). *Left vs cross-subspace*: left-region positions have subspace S, cross-subspace positions have subspace ≠ S — disjoint by definition. *Cross-document*: I3-D operates on d' ≠ d, disjoint from the other three by document identity. *Vacated vs assignment regions*: I3-V applies to positions v with subspace(v) = S and v ≥ p that are *not* shifted images; I3 assigns values only at shifted images shift(u, n), so I3-V and I3 are disjoint by the exclusion condition. I3-L applies only to v < p, while I3-V applies to v ≥ p — disjoint. I3-X applies only to subspace ≠ S, while I3-V applies to subspace S — disjoint. The five clauses are mutually consistent, so M'(d) is well-defined.

**Gap and vacated regions.** I3-V explicitly vacates original positions at or beyond p that are not the destination of any shifted content, completing the shift semantics: content departs from its original position as it arrives at the shifted one. The vacated set includes original positions within the gap [p, shift(p, n)) — which would otherwise be unaddressed — as well as, in sparse arrangements, original positions beyond the gap whose shift pre-images are absent from dom(M(d)). After accounting for all five clauses, the positions in [p, shift(p, n)) remain the only region not assigned a value by any postcondition: p is not < p (so I3-L excludes it), and for every v ≥ p, shift(v, n) > v ≥ p by TS4 (ASN-0034), so no shifted image lands in the gap. These n gap positions are where newly inserted content will be placed; the content-placement postcondition is an operation-level concern deferred to a future INSERT ASN.


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

Positions [1, 1] and [1, 2] are below p = [1, 3] and remain unchanged (I3-L). The three V-positions at or beyond p are each advanced by δ₂ = [0, 2]; their I-addresses are unchanged (I3). ∎

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
| M(d) | definition | M(d) : T ⇀ T — arrangement function mapping V-positions to I-addresses for document d | introduced (local) |
| subspace(v) | definition | subspace(v) = v₁ — the first component of a V-position, identifying its subspace | introduced (local) |
| ordinal-level | definition | A span σ = (s, ℓ) is ordinal-level when actionPoint(ℓ) = #s = #ℓ | introduced (local) |
| VB | axiom | All V-positions in dom(M(d)) within a subspace are sibling-stream outputs; bootstrap prefixes are structural and excluded from dom(M(d)) | introduced (local) |
| VD | lemma | All V-positions in a subspace share the same tumbler depth | introduced (local) |
| VP | axiom | subspace(v) = v₁ ≥ 1 for every V-position v | introduced (local) |
| I3 | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v)) | introduced |
| I3-L | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-X | frame | (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)) | introduced |
| I3-D | frame | (A d' ≠ d : M'(d') = M(d')) | introduced |
| I3-V | postcondition | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d))) | introduced |
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
| T10a.1 | lemma | All siblings from one allocator have uniform length | cited (ASN-0034) |
| T4 | axiom | Address tumblers have ≤ 3 zeros as field separators; every field component strictly positive | cited (ASN-0034) |


## Open Questions

- When external state records a V-position, what must the system provide to allow that reference to be updated after a shift repositions it?
