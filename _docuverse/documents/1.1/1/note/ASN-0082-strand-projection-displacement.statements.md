# ASN-0082 Claim Statements

*Source: ASN-0082-strand-projection-displacement.md (revised 2026-04-09) — Extracted: 2026-05-15*

## Definition — ArrangementFunction

M(d) : T ⇀ T — arrangement function mapping V-positions to I-addresses for document d

## Definition — SubspaceOf

subspace(v) = v₁ — the first component of a V-position, identifying its subspace

## Definition — OrdinalLevel

A span σ = (s, ℓ) is ordinal-level when actionPoint(ℓ) = #ℓ (the width acts at the deepest component of ℓ); level-uniformity #s = #ℓ is a separate condition stated where invoked (e.g., I3-S and D-S)

## Definition — OrdinalDisplacement

δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m.

When the depth is determined by context (typically m = #p for insertion position p), written δₙ.

## Definition — OrdinalShift

shift(v, n) = v ⊕ δ(n, #v)

By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. Precondition: n ≥ 1, #v = m.

## Definition — TumblerAdd

a ⊕ w: copy prefix, advance at action point, copy tail from w.

Explicitly: (a ⊕ w)ᵢ = aᵢ for i < actionPoint(w); (a ⊕ w)_{actionPoint(w)} = a_{actionPoint(w)} + w_{actionPoint(w)}; result length = #w.

## Definition — TumblerSub

a ⊖ w: zero prefix, reverse at divergence, copy tail from a.

Explicitly: result has zero prefix up to the point of divergence, (a ⊖ w)_{div} = a_{div} − w_{div} at the divergence position, and copies of a at positions after the action point.

## Definition — SpanReach

reach(σ) = start(σ) ⊕ width(σ)

## Definition — OrdinalExtraction

For a V-position v with #v = m ≥ 2: ord(v) = [v₂, ..., vₘ] — the tumbler of length m − 1 obtained by stripping the subspace identifier.

Postcondition: when v satisfies S8a, every component of ord(v) is positive.

## Definition — VPositionReconstruction

For subspace identifier S ≥ 1 and ordinal o = [o₁, ..., oₖ] with #o ≥ 1: vpos(S, o) = [S, o₁, ..., oₖ].

Inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

## Definition — OrdinalDisplacementProjection

For a displacement w with w₁ = 0 and #w = m ≥ 2: w_ord = [w₂, ..., wₘ] — the tumbler of length m − 1 obtained by stripping the (zero) first component.

When Pos(w): Pos(w_ord) and actionPoint(w_ord) = actionPoint(w) − 1. At depth m = 2: w = [0, c] for positive integer c, and w_ord = [c] with Pos([c]).

## Definition — ThreeRegions

```
L = {v ∈ V_1(d) : v < p}            — left of contraction
X = {v ∈ V_1(d) : p ≤ v < r}        — the contracted interval
R = {v ∈ V_1(d) : v ≥ r}            — right of contraction
```

By trichotomy of the total order (T1), every v ∈ V_1(d) falls in exactly one region.

## Definition — ShiftedRightRegion

Q₃ = {σ(v) : v ∈ R} — the set of shifted right-region positions in the post-state.

---

## S8-depth — FixedDepthVPositions (invariant, INVARIANT)

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

All V-positions within a given subspace of a document share the same tumbler depth.

## S8a — VPositionWellFormedness (axiom, AXIOM)

`(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

V-positions are zero-free, have depth at least 2, and have every component strictly positive. Specializations: v₁ ≥ 1 (positive subspace identifier) and v > 0 (positive as a tumbler under lexicographic order).

## S0 — ContentImmutability (invariant, INVARIANT)

`a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`

## S2 — ArrangementFunctionality (axiom, AXIOM)

`(A d, v : v ∈ dom(M(d)) : M(d)(v) is uniquely determined)` — each V-position in dom(M(d)) has a uniquely determined I-address.

## S3 — ReferentialIntegrity (invariant, INVARIANT)

`(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` — equivalently `ran(M(d)) ⊆ dom(Σ.C)`

## S8-fin — FiniteArrangement (invariant, INVARIANT)

For each document d, dom(M(d)) is finite.

## S9 — TwoStreamSeparation (lemma, LEMMA)

Arrangement changes preserve content store (preservation direction): dom(C) ⊆ dom(C') and values unchanged.

## D-CTG — VContiguity (invariant, INVARIANT)

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`

Text subspace only; the link subspace V_2(d) is exempt — sparse with tombstones is permitted.

## D-MIN — VMinimumPosition (invariant, INVARIANT)

When V_1(d) is non-empty, min(V_1(d)) = [1, 1, ..., 1] of length m.

Text subspace only; link positions need not begin at [2, 1, ..., 1].

NOT preserved by shift when p = min(V_1(d)).

## D-SEQ — SequentialPositions (lemma, LEMMA)

When V_1(d) is non-empty with common depth m ≥ 2, there exists n ≥ 1 such that V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}.

Text subspace only. NOT preserved by shift alone.

## T1 — LexicographicOrder (axiom, AXIOM)

Lexicographic total order on tumblers: for tumblers a, b of equal length, a < b at the leftmost position where they differ.

## T4 — AddressTumblerStructure (axiom, AXIOM)

Address tumblers have ≤ 3 zeros as field separators; every field component strictly positive.

## T12 — SpanWellFormed (precondition, PRE)

span(s, ℓ) well-formed when ℓ > 0 and actionPoint(ℓ) ≤ #s.

## TS1 — ShiftOrderPreservation (lemma, LEMMA)

shift preserves strict order: for v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂,

`shift(v₁, n) < shift(v₂, n)`

## TS2 — ShiftInjectivity (lemma, LEMMA)

shift is injective: for v₁, v₂ with #v₁ = #v₂ = m,

`shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂`

## TS4 — ShiftStrictIncrease (lemma, LEMMA)

`shift(v, n) > v` for n ≥ 1.

## TA-assoc — TumblerAddAssoc (lemma, LEMMA)

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` when both sides are well-defined.

## TA2 — SubtractionWellDefined (lemma, LEMMA)

Subtraction a ⊖ w is well-defined when a ≥ w.

## TA3-strict — OrderPreservationSubtractionStrict (lemma, LEMMA)

`a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w`

## TA4 — PartialInverse (lemma, LEMMA)

`(a ⊕ w) ⊖ w = a`

Preconditions: Pos(w), actionPoint(w) = k = #a, #w = k, and (A i : 1 ≤ i < k : aᵢ = 0).

## D2 — WidthRecovery (lemma, LEMMA)

For level-uniform σ: `reach(σ) ⊖ start(σ) = width(σ)`

## S6 — LevelConstraint (lemma, LEMMA)

For level-uniform σ: `#reach(σ) = #s`

---

## OrdinalOrderEquivalence — OrdinalOrderEquivalence (lemma, LEMMA)

For V-positions v₁, v₂ with subspace(v₁) = subspace(v₂) = S and #v₁ = #v₂ = m ≥ 2:

`v₁ < v₂ ⟺ ord(v₁) < ord(v₂)`

## OrdAddHom — OrdinalAdditionHomomorphism (lemma, LEMMA)

For a V-position p with #p = m ≥ 2 and a displacement w with w₁ = 0, #w = m, and Pos(w):

- (a) `ord(p ⊕ w) = ord(p) ⊕ w_ord`
- (b) `subspace(p ⊕ w) = subspace(p)`
- (c) `p ⊕ w = vpos(subspace(p), ord(p) ⊕ w_ord)`

## PositiveOffsetExceeds — PositiveOffsetExceeds (lemma, LEMMA)

For natural numbers a, b ∈ ℕ with a ≥ 1:

`a + b > b` and `b + a > b`

---

## I3 — PostInsertionShift (postcondition, POSTCONDITION)

*Preconditions:* d is a document; M(d) : T ⇀ T; p ∈ T with #p ≥ 2 and subspace(p) = S ≥ 1; depth-compatible: if {v ∈ dom(M(d)) : subspace(v) = S} ≠ ∅ then #p = #v for any such v; n ≥ 1; M'(d) is the post-insertion arrangement.

*Statement:*

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## I3-V — PostInsertionVacating (postcondition, POSTCONDITION)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d)))`

## I3-CS — PostInsertionDomainClosureSubspace (postcondition, POSTCONDITION)

`(A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : (v < p ∧ v ∈ dom(M(d))) ∨ (E u : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p : v = shift(u, n)))`

— domain closure within subspace S.

## I3-CX — PostInsertionDomainClosureCross (postcondition, POSTCONDITION)

`(A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d)))`

— domain closure across subspaces.

## I3-L — PostInsertionLeftFrame (frame, FRAME)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I3-X — PostInsertionCrossSubspaceFrame (frame, FRAME)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I3-D — PostInsertionCrossDocumentFrame (frame, FRAME)

`(A d' ≠ d : M'(d') = M(d'))`

## I3-C — PostInsertionContentFrame (frame, FRAME)

`dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))`

— content store unchanged.

## I3-VD — PostInsertionDepthUniformity (lemma, LEMMA)

S8-depth holds for the post-state M'(d) across all subspaces.

For subspace S: `(A v₁, v₂ ∈ dom(M'(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂ = m)`

For any subspace S' ≠ S: positions in dom(M'(d)) with subspace S' are exactly the positions in dom(M(d)) with subspace S', on which S8-depth holds by hypothesis.

## I3-VP — PostInsertionWellFormedness (lemma, LEMMA)

`(A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

— S8a preserved post-insertion.

## I3-S3 — PostInsertionReferentialIntegrity (lemma, LEMMA)

`(A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C'))`

— referential integrity preserved post-insertion.

## I3-S2 — PostInsertionFunctionality (lemma, LEMMA)

M'(d) is a function — S2 (ArrangementFunctionality) holds for the post-state.

Pairwise disjointness of assignment regions (shifted, left, cross-subspace) ensures no double-assignment: each region assigns exactly one value per position.

## I3-fin — PostInsertionFiniteness (lemma, LEMMA)

dom(M'(d)) is finite — S8-fin (FiniteArrangement) holds for the post-state.

By I3-CS and I3-CX, every position in dom(M'(d)) either belongs to dom(M(d)) directly or is shift(v, n) for some v ∈ dom(M(d)) with subspace(v) = S and v ≥ p. The shifted-image set is at most as large as the source set by injectivity (TS2).

## I3-S7 — PostInsertionAllocationInvariants (lemma, LEMMA)

The post-state satisfies S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), S7c (ElementFieldDepth), S7d (DocumentAllocationDiscipline), and the derived theorem S7 (StructuralAttribution).

Trivially by I3-C (dom(C') = dom(C), per-address values unchanged) and I3-D (document set unchanged): S7a, S7b, S7c are predicates over dom(C) which is unchanged; S7d is a predicate over the document set which is unchanged; S7 follows as a corollary.

## I3-S — SpanShiftPreservation (lemma, LEMMA)

*Preconditions:* level-uniform span σ = (s, ℓ) with s ≥ p, subspace(s) = S, #s = #ℓ = m, and actionPoint(ℓ) = m. Define shifted span σ' = (shift(s, n), ℓ).

*Postconditions:*

- (a) `reach(σ') = shift(reach(σ), n)`
- (b) `width(σ') = ℓ`

---

## Contraction — Contraction (operation, OPERATION)

Remove span (p, w) from the text subspace of document d.

*Preconditions:*
- `S = 1` (subspace scoping axiom)
- `p ∈ V_1(d)`
- `Pos(w)`
- `#w = #p`
- `w₁ = 0`
- `#p = 2` (depth scoping axiom)
- Containment: with D-SEQ giving V_1(d) = {[1, k] : 1 ≤ k ≤ N}, `p₂ + w₂ − 1 ≤ N`

*Postconditions:* D-SHIFT, D-DOM

*Frame:* D-L, D-CS, D-CD, D-I

## D-SHIFT — RightShift (postcondition, POSTCONDITION)

*Preconditions:* as stated in the contraction formal contract; r = p ⊕ w; R = {v ∈ V_1(d) : v ≥ r}; M'(d) is the post-contraction arrangement.

*Shift function:* for v ∈ R, σ(v) = vpos(S, ord(v) ⊖ w_ord)

*Statement:*

`(A v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

## D-DOM — DomainCharacterization (postcondition, POSTCONDITION)

`{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃`

## D-L — LeftPreservation (frame, FRAME)

`(A v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-CS — CrossSubspaceFrame (frame, FRAME)

`(A S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'})`

`∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v))`

## D-CD — CrossDocumentFrame (frame, FRAME)

`(A d' ≠ d : M'(d') = M(d'))`

## D-I — ContentStoreFrame (frame, FRAME)

`Σ'.C = Σ.C`

That is, `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`.

Exact equality, strictly stronger than S0.

## D-BJ — ShiftBijectivity (lemma, LEMMA)

σ : R → Q₃ is an order-preserving bijection.

*Preconditions:* #p = 2; v₁, v₂ ∈ R.

*Postconditions:*

- (a) Order-preservation: `v₁ < v₂ ⟹ σ(v₁) < σ(v₂)`
- (b) Injectivity: `v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂)`
- (c) Surjectivity: `Q₃ = {σ(v) : v ∈ R}`

## D-SEP — GapClosure (lemma, LEMMA)

*Preconditions:* #p = 2; r = p ⊕ w.

*Postconditions:*

- (a) Algebraic identity: `ord(r) ⊖ w_ord = ord(p)`
- (b) When R ≠ ∅: r = min(R), σ(r) is well-defined, and `min({ord(u) : u ∈ Q₃}) = ord(p)`

## D-DP — DensePartition (lemma, LEMMA)

*Preconditions:* #p = 2; L, X, R as defined by ThreeRegions; D-L, D-DOM, D-SHIFT, D-SEP, and D-CTG hold.

*Postconditions:*

- (a) No overlap: `L ∩ Q₃ = ∅`
- (b) Boundary adjacency: when R ≠ ∅, `min({ord(u) : u ∈ Q₃}) = ord(p)` and `(A v ∈ L : ord(v) < ord(p))`

## S8-depth-post — FixedDepthPreservation (lemma, LEMMA)

Post-state V-positions in subspace S share depth 2.

`(A v₁, v₂ ∈ dom(M'(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂ = 2)`

Positions in L retain depth 2 (unchanged by D-L). Positions in Q₃: σ(v) = [S, vₘ − c] has depth 2. By D-CS, other subspaces unchanged; by D-CD, other documents unchanged.

## S8a-post — WellFormednessPreservation (lemma, LEMMA)

Post-state V-positions are zero-free, of depth at least 2, and componentwise positive.

`(A v ∈ dom(M'(d)) : zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

For positions in Q₃: σ(v) = [S, vₘ − c] with S ≥ 1 and vₘ − c ≥ p₂ ≥ 1 (since vₘ ≥ p₂ + c for v ∈ R, and p₂ ≥ 1 by S8a on p).

## D-CTG-post — VContiguityPreservation (lemma, LEMMA)

At S = 1: the post-state V_1(d) is contiguous; non-text subspaces preserved verbatim by D-CS.

Derived form: `L ∪ Q₃ = {[1, k] : 1 ≤ k ≤ N − c}` — contiguous by direct verification of D-CTG's quantifier.

## D-MIN-post — VMinimumPreservation (lemma, LEMMA)

At S = 1: when the post-state V_1(d) is non-empty, `min(V_1(d)) = [1, 1]`; when empty, D-MIN holds vacuously.

Non-text subspaces preserved verbatim by D-CS (foundation imposes no D-MIN obligation on V_S(d) with S ≠ 1).

## D-SEQ-post — SequentialPositionsPreservation (lemma, LEMMA)

At S = 1: when the post-state V_1(d) is non-empty, `V_1(d) = {[1, k] : 1 ≤ k ≤ N − c}`.

When V_1(d') is empty (N − c = 0), D-SEQ holds vacuously. Non-text subspaces preserved verbatim by D-CS.

## S8-fin-post — FiniteArrangementPreservation (lemma, LEMMA)

Post-state dom(M'(d)) is finite.

By D-DOM: subspace-1 positions L ∪ Q₃ with |L ∪ Q₃| ≤ |V_1(d)|, finite by S8-fin on the pre-state. By D-CS: other subspaces retain finite pre-state domains. By D-CD: other documents unchanged.

## S2-post — ArrangementFunctionalityPost (lemma, LEMMA)

Post-state M'(d) is a function.

By D-DOM: dom(M'(d)) within subspace S is L ∪ Q₃. By D-DP(a): L ∩ Q₃ = ∅. For v ∈ L, M'(d)(v) uniquely determined by D-L. For v ∈ Q₃, v = σ(u) for unique u ∈ R (D-BJ injectivity), M'(d)(v) = M(d)(u) uniquely determined by D-SHIFT and pre-state S2.

## S3-post — ReferentialIntegrityPost (lemma, LEMMA)

Post-state `ran(M'(d)) ⊆ dom(Σ'.C)`.

Every I-address in ran(M'(d)) was an I-address in ran(M(d)) (L-positions via D-L, Q₃-positions via D-SHIFT from R). By pre-state S3: ran(M(d)) ⊆ dom(Σ.C). By D-I: dom(Σ.C) = dom(Σ'.C).

## S7-post — AllocationInvariantsPreservation (lemma, LEMMA)

Post-state satisfies S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), S7c (ElementFieldDepth), S7d (DocumentAllocationDiscipline), and the derived theorem S7 (StructuralAttribution).

Trivially by D-I (Σ'.C = Σ.C, so dom(Σ'.C) = dom(Σ.C), preserving S7a, S7b, S7c pointwise) and D-CD (other documents unchanged, preserving S7d and the document set). S7 follows as a corollary since all its dependencies hold of the post-state.

## D-S — SpanContractionPreservation (lemma, LEMMA)

*Preconditions:* level-uniform span σₛ = (s, ℓ) with s ∈ R, subspace(s) = 1, #s = #ℓ = 2, actionPoint(ℓ) = 2. Define contracted span σ'ₛ = (σ(s), ℓ).

*Postconditions:*

- (a) `reach(σ'ₛ) = σ(reach(σₛ))`
- (b) `width(σ'ₛ) = ℓ`

Span-level dual of I3-S for contraction.
