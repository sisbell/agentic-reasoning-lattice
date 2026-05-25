# ASN-0098: Link Projection Displacement

*2026-05-24*

## The Question

A link was created at some past state. Its endsets were fixed at that moment against the I-addresses then visible. The documents through which a holder might follow the link have since been edited — passages inserted, removed, rearranged. A new document may have transcluded some of the linked content. The original document may have lost it entirely. The holder asks: "Where, in the current state, does my link reach? What can I rely on?"

We are looking for abstract guarantees. What stays fixed about the link itself? Which V-positions do its endsets reach in any given document? How do those V-positions move under each kind of editing operation? Under what conditions does the link survive — and what, exactly, does "survive" mean when the link's stored data and the document's current state are two different things?

We must distinguish three things that the literature often runs together:
- The *link* — a stored value at an address in `dom(Σ.L)`.
- The *coverage* of an endset — the set of I-addresses the endset denotes.
- The *projection* of an endset through a document — the V-positions in that document's current arrangement whose I-addresses lie in the coverage.

The first two are static once the link is created. The third is a live computation: it consults the document's mutable arrangement. Every interesting guarantee about "link behaviour under editing" is, on examination, a guarantee about how this third quantity displaces — gains or loses V-positions, rearranges them — as the arrangement changes.

## State Components

We work over the state structure inherited from the foundations. Three components matter here.

The content store `Σ.C : T ⇀ Val` is append-only with immutable values (S0, S1 of ASN-0036). Once an I-address `a` is bound, `Σ.C(a)` cannot be removed or rewritten. The set `dom(Σ.C)` only grows.

For each document `d ∈ dom(Σ.M)`, the arrangement `Σ.M(d) : T ⇀ T` is a partial function from V-positions to I-addresses. The arrangement is mutable: the operations K.μ⁺ (content-subspace extension), K.μ⁺_L (link-subspace extension), K.μ⁻ (contraction), and K.μ~ (reordering) of ASN-0047 modify it. The set of allocated documents `dom(Σ.M)` is non-decreasing (M1 of ASN-0093).

The link store `Σ.L : T ⇀ Link` binds link addresses to link values (ASN-0043). A link value is a sequence of endsets `Σ.L(a) = (e₁, e₂, …, eₙ)` with `N ≥ 3` and a non-empty type endset at slot 3 (L3). Each endset `eᵢ ∈ Endset` is a finite set of well-formed spans. The link store is immutable: by L12, `(A Σ → Σ', a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`.

The two address spaces communicate through the `Σ.M(d)` mappings: V-positions in V-space resolve to I-addresses in I-space. Links inhabit a third role — stored at link-subspace I-addresses but referencing content-subspace I-addresses through their endsets — but for the projection question this role-distinction is immaterial. What matters is that endsets reference I-addresses, and arrangements map V-positions to I-addresses, and the bridge between them is computed live.

*Reference-frame robustness.* The projection function defined in the next section consults only `coverage(e)` and `Σ.M(d)`. Neither input depends on additional state components present in extended reference frames — the provenance relation `R` and entity set `E` of ASN-0047, for instance. Operations drawn from either reference frame — K.σ from ASN-0093, K.ρ and K.δ from ASN-0047 — therefore admit uniform treatment for projection purposes; the frame conditions on `Σ.M(d)` and `dom(Σ.M)` are what the projection responds to, and those conditions are stated identically in both reference frames. We will cite operations from whichever frame names them most directly without further reconciliation, since projection-level claims are invariant under the choice.

## The Coverage of an Endset

For an endset `e ⊆ Span`, the *coverage* `coverage(e)` is the set of I-addresses denoted by `e`'s spans, defined in ASN-0043 as

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
```

Each span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}` by T12 of ASN-0034, where `s ⊕ ℓ ∈ T` exists by TA0 because `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are well-formedness conditions of the span. Coverage is a set of I-addresses in `T`. Some of these I-addresses may be in `dom(Σ.C)` at the time the endset was constructed; some may not. Crucially, coverage is a *purely combinatorial* property of the endset's span representation — it does not consult any state component. Coverage depends on the spans; nothing else.

By L5 (EndsetSetSemantics, ASN-0043), an endset is an unordered set. Two endsets with the same set of spans have the same coverage. The lossy projection `Endset → 2^T` defined by `coverage` is not injective: distinct span decompositions can have identical coverage (for instance, splitting a single span at an interior point produces two spans whose coverage equals the original).

## The Projection Operation

For an endset `e`, a document `d ∈ dom(Σ.M)`, and a state `Σ`, define the *projection of `e` through `d` at `Σ`* as the set of V-positions in `d`'s arrangement whose I-addresses lie within `e`'s coverage:

**project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}**

For a link `a ∈ dom(Σ.L)` with slot `i ∈ {1, …, |Σ.L(a)|}`, write `project(a, i, d, Σ) ≡ project(Σ.L(a).eᵢ, d, Σ)`.

The definition reads from two inputs:
- The endset, fixed once and for all by the link's creation (and immune to subsequent transitions, by L12).
- The arrangement `Σ.M(d)`, mutable and reflecting whatever edits `d` has undergone.

Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still. Therefore every change in projection must be attributable to a change in `Σ.M(d)` — and we can characterise the change by examining what each editing operation does to `Σ.M(d)`.

The definition does not separately consult `Σ.C` or `Σ.L`. Content allocation that does not modify any `Σ.M(d)` cannot affect any projection. Link allocation that does not modify `Σ.M(d)` cannot affect existing projections. Document registration (K.σ) that only updates `dom(Σ.M)` and initialises arrangements to empty cannot retroactively affect existing projections through existing documents. The projection is sensitive only to its two inputs, and only one of them moves.

Three degenerate configurations follow directly from the definition and require no separate treatment in subsequent claims. The projection of the empty endset is uniformly empty: `project(∅, d, Σ) = ∅` for every `d, Σ`, since `coverage(∅)` is the empty union over an empty index set. The projection through an empty arrangement is uniformly empty: `project(e, d, Σ) = ∅` when `dom(Σ.M(d)) = ∅`, since the set comprehension ranges over the empty domain. A link with empty from/to endsets but a non-empty type endset (admitted by L3 of ASN-0043, which requires only the type slot to be non-empty) has empty projections at slots 1 and 2 regardless of any document's state; only the type slot's projection can be non-empty.

## Immutability of the Stored Link

Before we can reason about how projection displaces, we must pin down what does *not* move. The link's stored content — its address, its sequence of endsets, the spans within each endset — is structurally immutable. By L12 of ASN-0043, for every state transition `Σ → Σ'`, every `a ∈ dom(Σ.L)` persists in `dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)`: the address persists, and the sequence of endsets is preserved verbatim. No operation in the transition vocabulary overwrites a link's value or removes a link from the store. Two consequences specialise L12 to the slot- and coverage-level reasoning this ASN requires.

**LP2 — SlotInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

L12 (ASN-0043) supplies two conclusions on the hypothesis `a ∈ dom(Σ.L)`: address persistence `a ∈ dom(Σ'.L)` (which makes the slot accessor on the left-hand side well-defined) and value preservation `Σ'.L(a) = Σ.L(a)`. The slot equation then follows by component projection on the sequence: equal sequences have equal entries at every position. In particular, the slot-position assignment fixed at link creation — from-set at slot 1, to-set at slot 2, type-set at slot 3, and any additional slots — is structurally preserved. No editing operation can swap, relabel, or alter which slot carries which endset. The directionality of a standard triple (which end is "from", which is "to") is encoded in slot position alone, and slot position is immutable.

**LP2★ — MultiStepSlotInvariance**: For every reachable state sequence `Σ →* Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

This is the reflexive-transitive closure of LP2. Proof by induction on the length of the transition sequence. The empty sequence (`Σ = Σ'`) gives the conjunction by reflexivity. For the inductive step, suppose `Σ →* Σ_n → Σ'` with `Σ_n.L(a).eᵢ = Σ.L(a).eᵢ` and `a ∈ dom(Σ_n.L)` by induction hypothesis. The single step `Σ_n → Σ'` gives `a ∈ dom(Σ'.L)` and `Σ'.L(a).eᵢ = Σ_n.L(a).eᵢ` by LP2, so by transitivity of equality the full chain holds.

**LP3 — CoverageInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

LP2 supplies both conjuncts: `a ∈ dom(Σ'.L)` directly (so the slot accessor on the left-hand side of the coverage equation is well-defined), and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` from which the coverage equation follows by applying `coverage` to both sides. The set of I-addresses the link refers to is computed from its endsets; if the endsets are byte-identical between states, the coverage is identical between states. Combining L12 with LP2 and LP3: the link, the slot, and the I-addresses it reaches are all permanent. What can vary is only which of those I-addresses are currently arranged in any given document.

**LP3★ — MultiStepCoverageInvariance**: For every reachable state sequence `Σ →* Σ'`, every `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

This is the reflexive-transitive closure of LP3. Proof by induction on the length of the transition sequence. The empty sequence (`Σ = Σ'`) gives equality trivially. For the inductive step, suppose `Σ →* Σ_n → Σ'` with `coverage(Σ_n.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` and `a ∈ dom(Σ_n.L)` by induction hypothesis. The single step `Σ_n → Σ'` gives `a ∈ dom(Σ'.L)` and `coverage(Σ'.L(a).eᵢ) = coverage(Σ_n.L(a).eᵢ)` by LP3, so by transitivity of equality the full chain holds.

**Store Monotonicity★**: For every reachable state sequence `Σ →* Σ'`:
```
dom(Σ.C) ⊆ dom(Σ'.C)  ∧  dom(Σ.L) ⊆ dom(Σ'.L)
```

Each is the reflexive-transitive closure of the corresponding single-step monotonicity guarantee (C0 of ASN-0093 for content; L12 of ASN-0093 for links, in its membership-persistence consequence). The base case is the empty sequence (reflexive containment); the inductive step composes containments transitively.

These invariants pin down what a link holder owns. Subsequent operations by any party — even the holder, even the original creator — cannot rewrite the endsets. The link is, in this strict sense, a permanent record.

## Frame Conditions: When Projection Does Not Move

A projection moves only if its inputs move. Since the endset (and therefore its coverage) is fixed by LP3, the projection through a document moves only if that document's arrangement is modified — and even then, only if the modification affects V-positions whose I-addresses lie in the endset's coverage.

**LP4 — ArrangementSpecificity**: For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

The projection function depends on exactly two inputs: `coverage(e)` and `Σ.M(d)`. The first is a pure function of the endset `e`, which appears unchanged on both sides of the equality — `coverage(e)` is therefore identical between the two projections. The second is the arrangement, equal by hypothesis. Both inputs agree pointwise, so the set comprehension produces identical results. The projection cannot displace without `Σ.M(d)` displacing.

**LP5 — Cross-Document Independence**: Every operation in the K.μ family (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) has frame `(A d' : d' ≠ d : M'(d') = M(d'))` — it modifies at most one document's arrangement per transition. By LP4 applied to each unmodified document:
```
(A d' ∈ dom(Σ.M), d' ≠ d : project(e, d', Σ') = project(e, d', Σ))
```

A link's projection through one document is unaffected by editing operations on a different document. Projections are *per-document* facts. The link itself is a single global object, but the V-positions it reaches in any given document depend only on that document's local state.

**LP6 — Content-Allocation Invariance**: The K.α operation (ASN-0093) modifies only `Σ.C` and has frame `(A d :: M'(d) = M(d))`; K.α also preserves `dom(Σ.M)`, so `dom(Σ.M) = dom(Σ'.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.α transition.

Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them. This is the precise sense in which "insertion at the boundary of a linked passage" cannot extend the link's reach: insertion as a composite (allocate + arrange) splits into a K.α step (no projection effect) and a K.μ⁺ step. The K.μ⁺ step might add a V-position to the projection, but only if the new V-position's I-address is in `coverage(e)`. By T10a (AllocatorDiscipline, ASN-0034), each new K.α-allocated I-address is structurally distinct from all prior allocations; the new V-position's I-address lies outside `coverage(e)` whenever `e` was tightly constructed (LP19 below formalises this), and in that case the projection does not grow. Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content; the precise condition under which boundary insertion is excluded is therefore tightness, not allocator behaviour alone.

The abstract guarantee is sharper than the "outside the strap" metaphor: the projection depends on coverage and arrangement alone, and content allocation alone (K.α) affects neither.

**LP7 — Link-Allocation Invariance**: The K.λ operation modifies only `Σ.L`; its frame is `(A d :: M'(d) = M(d))`, and K.λ preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`. Creating a new link cannot retroactively affect the projection of any other link.

**LP8 — Entity-Registration Invariance**: K.σ (document registration) extends `dom(Σ.M)` by adding a fresh document `d_new` with `M'(d_new) = ∅` and preserves all existing arrangements. For every endset `e` and every `d ∈ dom(Σ.M)` (the pre-state domain), `project(e, d, Σ') = project(e, d, Σ)` by LP4. The newly created `d_new` has `project(e, d_new, Σ') = ∅` since `dom(Σ'.M(d_new)) = ∅`.

*Remark on K.δ.* ASN-0047 includes K.δ as a unified entity-creation operation spanning nodes, accounts, and documents. The K.δ-IsNode and K.δ-IsAccount cases have frame `(A d :: M'(d) = M(d))` — no arrangement is modified — so LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)` yields projection invariance. The K.δ-IsDocument case creates a new document `d_new` with `M'(d_new) = ∅`, which is the same scenario as LP8 above; in this ASN's reference frame K.σ (ASN-0093) is the document-registration operation, and K.δ-IsDocument is subsumed by the LP8 argument. Each K.δ kind therefore reduces to either LP4 or LP8, and no separate displacement claim is required.

**LP14 — ProvenanceRecording Invariance**: The K.ρ operation (ASN-0047), which records provenance by adding a pair to `Σ.R`, has frame `(A d :: M'(d) = M(d))` — it leaves every document's arrangement intact — and preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.ρ transition. Provenance bookkeeping does not displace any projection.

## Operation Effects on Projection

We now examine each operation that *can* displace a projection. The pattern is uniform: each K.μ operation modifies `Σ.M(d)` in a constrained way, and the projection follows mechanically.

**LP9 — Extension under K.μ⁺ and K.μ⁺_L**: For every extension transition `Σ → Σ'` operating on document `d` — either K.μ⁺ (content-subspace extension) or K.μ⁺_L (link-subspace extension) — and every endset `e`:
```
project(e, d, Σ) ⊆ project(e, d, Σ')
```

Both K.μ⁺ and K.μ⁺_L extend `Σ.M(d)`: `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))` with agreement on the prior domain (`(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`). For any `v ∈ project(e, d, Σ)`, we have `v ∈ dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` and `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)`, so `v ∈ project(e, d, Σ')`. The projection can only grow. The argument is identical for both extension operations because each shares the same structural form on `Σ.M(d)`; what differs between them is only the subspace of the new V-positions and the store (`dom(Σ.C)` vs `dom(Σ.L)`) of their targets.

The new V-positions that enter the projection are exactly the new arrangement entries whose I-addresses fall in the coverage:
```
project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}
```

The forward inclusion (⊆): suppose `v ∈ project(e, d, Σ') ∖ project(e, d, Σ)`. Then `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ coverage(e)` by the first conjunct. For the second, either `v ∉ dom(Σ.M(d))` or `Σ.M(d)(v) ∉ coverage(e)`. The second alternative is excluded: if `v ∈ dom(Σ.M(d))`, the agreement clause gives `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, contradicting `v ∉ project(e, d, Σ)`. So `v ∉ dom(Σ.M(d))`, placing `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))`. The reverse inclusion (⊇): if `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))` with `Σ'.M(d)(v) ∈ coverage(e)`, then `v ∈ project(e, d, Σ')` directly; and `v ∉ project(e, d, Σ)` since `v ∉ dom(Σ.M(d))`.

When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, the projection's behaviour depends on the construction discipline of the endset. For endsets *tightly constructed* — whose coverage was entirely populated at construction time (formalised below as LP19) — the newly allocated I-address lies outside coverage, and the projection does not grow. Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content, in which case the projection grows by that V-position. When K.μ⁺ adds entries mapping V-positions to *existing* I-addresses (the transclusion case), the projection grows by precisely those new V-positions whose mappings fall in coverage. This is the mechanism by which a link "comes into view" in a document that newly transcludes its target content. K.μ⁺_L exhibits the same growth behaviour for link-subspace V-positions when an existing link address is admitted into a home-document arrangement.

**LP10 — Contraction under K.μ⁻**: For every K.μ⁻ transition `Σ → Σ'` operating on `d`, and every endset `e`:
```
project(e, d, Σ') ⊆ project(e, d, Σ)
```

K.μ⁻ contracts `Σ.M(d)`: `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` with agreement on the retained domain. For any `v ∈ project(e, d, Σ')`, we have `v ∈ dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, so `v ∈ project(e, d, Σ)`. The projection can only shrink.

The V-positions that leave the projection are exactly the arrangement entries removed by the operation:
```
project(e, d, Σ) ∖ project(e, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

The forward inclusion (⊆): if `v ∈ project(e, d, Σ) ∖ project(e, d, Σ')`, then `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ coverage(e)` by the first conjunct, while the second forces either `v ∉ dom(Σ'.M(d))` or `Σ'.M(d)(v) ∉ coverage(e)`. The second alternative is excluded: if `v ∈ dom(Σ'.M(d)) ⊆ dom(Σ.M(d))`, the agreement clause gives `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)`, contradicting `v ∉ project(e, d, Σ')`. So `v ∉ dom(Σ'.M(d))`, placing `v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d))`. The reverse inclusion (⊇): if `v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d))` with `Σ.M(d)(v) ∈ coverage(e)`, then `v ∈ project(e, d, Σ)` directly; and `v ∉ project(e, d, Σ')` since `v ∉ dom(Σ'.M(d))`.

When deletion removes V-positions whose I-addresses are in coverage, those V-positions leave the projection. The I-addresses themselves persist in `dom(Σ.C)` by S0; they are merely no longer in `ran(Σ.M(d))`. Other documents that still arrange those I-addresses are unaffected (LP5) — the link can still be projected through them.

The "partial deletion" case follows immediately: if some but not all V-positions of a contiguous projection are removed, the remaining V-positions stay in the projection. The link survives on whatever V-positions remain. This is Nelson's "if anything is left at each end" condition made precise.

**LP11 — Reordering under K.μ~**: For every K.μ~ transition `Σ → Σ'` operating on `d` via the witnessing bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))`, and every endset `e`:
```
project(e, d, Σ') = π(project(e, d, Σ))
```
and
```
ran(Σ'.M(d)) = ran(Σ.M(d))
```

The K.μ~ definition (ASN-0047) gives the bijection equation `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))`. By K.μ~-FIX, `dom(Σ'.M(d)) = dom(Σ.M(d))`, so π permutes the domain. For any `v ∈ dom(Σ.M(d))`:

```
v ∈ project(e, d, Σ)
  ⟺ Σ.M(d)(v) ∈ coverage(e)               -- definition
  ⟺ Σ'.M(d)(π(v)) ∈ coverage(e)            -- bijection equation
  ⟺ π(v) ∈ project(e, d, Σ')              -- definition (π(v) ∈ dom(Σ'.M(d)))
```

The forward inclusion `π(project(e, d, Σ)) ⊆ project(e, d, Σ')` follows directly from the biconditional. For the reverse inclusion `project(e, d, Σ') ⊆ π(project(e, d, Σ))`, any `v' ∈ project(e, d, Σ') ⊆ dom(Σ'.M(d)) = dom(Σ.M(d))` has a unique preimage `v = π⁻¹(v')` under π's bijectivity on `dom(Σ.M(d))`; the biconditional applied to `v` gives `v ∈ project(e, d, Σ)`, so `v' = π(v) ∈ π(project(e, d, Σ))`. Both inclusions combine to the equality.

So the projection's V-positions move *with* the content they reach: `project(e, d, Σ') = π(project(e, d, Σ))`. The cardinality is preserved: `|project(e, d, Σ')| = |project(e, d, Σ)|`. The set of I-addresses reached by the projection is preserved exactly: `{Σ'.M(d)(v') : v' ∈ project(e, d, Σ')} = {Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`.

The second postcondition `ran(Σ'.M(d)) = ran(Σ.M(d))` is derived by taking images on both sides of the bijection equation. For every `v ∈ dom(Σ.M(d))`, the equation gives `Σ'.M(d)(π(v)) = Σ.M(d)(v)`. Therefore `{Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))} = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))} = ran(Σ.M(d))`. By K.μ~-FIX, `dom(Σ'.M(d)) = dom(Σ.M(d))`, so π is a bijection from `dom(Σ.M(d))` onto `dom(Σ'.M(d))`, hence `{π(v) : v ∈ dom(Σ.M(d))} = dom(Σ'.M(d))`. Substituting `v' = π(v)` and re-indexing the image set, `{Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))} = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))} = ran(Σ'.M(d))`. Combining the two equalities yields `ran(Σ.M(d)) = ran(Σ'.M(d))`.

The displacement under K.μ~ is therefore a *rebinding*: same I-addresses, same number of V-positions, but at new locations in V-space. A projection that was contiguous in V-order before the reordering may become fragmented after; conversely, a fragmented projection may become contiguous. The shape of the projection is a property of the current arrangement, not of the link.

## Discoverability and Survival

We are now in a position to state Nelson's survivability guarantee precisely. The vague claim "links survive editing if anything is left at each end" becomes a sharp condition on `coverage ∩ ran`.

**Definition — Discoverability**: For `a ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`, the link `a` is *discoverable from document `d`* at state `Σ` iff some slot's projection through `d` is non-empty:
```
discoverable_from(a, d, Σ)
  defined when  a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)
  ≡             (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)
```

The precondition `a ∈ dom(Σ.L)` is what makes `|Σ.L(a)|` and the slot accessor `Σ.L(a).eᵢ` well-defined; the precondition `d ∈ dom(Σ.M)` is what makes `project(a, i, d, Σ)` well-defined. The link is *discoverable* at `Σ` iff there exists some document from which it is discoverable.

**LP12 — DiscoverabilityCharacterisation**: For every link `a ∈ dom(Σ.L)`, document `d ∈ dom(Σ.M)`, and state `Σ`:
```
discoverable_from(a, d, Σ) ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

Direct from definitions. `v ∈ project(a, i, d, Σ)` requires `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, which requires some I-address in the coverage to be in the range. Conversely, any I-address `a*` in `coverage(eᵢ) ∩ ran(Σ.M(d))` is reached by some `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a*`, and that `v` lies in `project(a, i, d, Σ)`.

**LP13 — PartialSurvival**: A link's discoverability from `d` requires only that *some* I-address from *some* endset persist in `d`'s range. The link survives deletion as long as the deletion does not exhaust the coverage-range intersection of every slot. The link continues to exist in `dom(Σ.L)` (by L12, ASN-0043) regardless of arrangement state; only its *navigational usability from `d`* depends on the coverage-range intersection.

The phrase "anything is left at each end" can now be stated formally: discoverability from `d` requires that, for at least one slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`. For mere existence of the link, nothing is required at all.

## Discovery Independence of Origin

We have characterised discoverability *from* a particular document. Now we ask: how does this relate to which document created the link, which document allocated the linked content, and which document the holder is following the link from?

Three documents may be in play for any given link reference:
- The *home document* of the link, `home(a)` = `origin(a)` — the document under whose tumbler prefix the link's address was allocated (L1a, ASN-0093).
- The *origin document* of each I-address in coverage, `origin(a*)` — the document under whose tumbler prefix `a*` was allocated.
- The *navigating document* `d` from which the holder follows the link.

These three may be the same, all different, or any combination. The discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement. This is visible by inspection of LP12: the right-hand side references `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))` and nothing else. The characterisation contains no reference to `home(a)` or to the origin documents of coverage I-addresses. The home document is a metadata property of the link's address (recoverable by tumbler projection — S7 of ASN-0036), not a constraint on where the link can be reached from. Similarly, origin is a metadata property of each coverage I-address, indifferent to whether `d` was the document that allocated the address or some unrelated document that has since transcluded it. A link can therefore be discovered from any document whose arrangement currently maps to any I-address in any of the link's endsets' coverage, regardless of provenance. The system commits to indifference of provenance at the point of discovery.

The transclusion mechanism is the architectural lever that activates this provenance-indifference.

**LP16 — TransclusionDiscoverability**: If a document `d_new` transcludes content from another document `d_src` (via a fork composite or any K.μ⁺ that adds arrangement entries mapping V-positions to I-addresses already in `dom(Σ.C)`), then every link discoverable from `d_src` via those I-addresses is also discoverable from `d_new` via the corresponding V-positions in `d_new`.

Let `a*` be an I-address with `a* ∈ ran(Σ.M(d_src))` and `a* ∈ ran(Σ.M(d_new))`. For any link `a` and slot `i` with `a* ∈ coverage(Σ.L(a).eᵢ)`, both projections `project(a, i, d_src, Σ)` and `project(a, i, d_new, Σ)` are non-empty — the former by some `v_src` with `Σ.M(d_src)(v_src) = a*`, the latter by some `v_new` with `Σ.M(d_new)(v_new) = a*`. Discoverability extends to every document that transcludes any I-address in coverage. No notification of the link is required; the link is *passively* discoverable from `d_new` simply because `d_new` arranges the I-address.

This is the architectural mechanism behind Nelson's "a link to one version is a link to all versions" claim and the cross-document discovery property: link discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition.

## Ghost Projection and Resurrection

We consider two corner cases: when nothing in the system reaches a link's coverage, and when re-introduction of content restores reachability.

**LP17 — GhostProjection**: Suppose at state `Σ` no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`:
```
(A d ∈ dom(Σ.M), i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)
```

Then by LP12, `project(a, i, d, Σ) = ∅` for every `d, i`. The link is *orphaned*: not discoverable from any document. By L12 (ASN-0043), `a` remains in `dom(Σ.L)` and `Σ.L(a)` is unchanged. The link is not destroyed; it is invisible to forward navigation, but its stored endsets continue to identify the I-addresses it once reached, and the I-addresses themselves continue to exist in `dom(Σ.C)` by S0.

**LP18 — Resurrection**: If `a` is orphaned at `Σ` and a subsequent transition sequence `Σ →* Σ'` introduces an arrangement entry `Σ'.M(d)(v) = a*` for some `d, v, a*` with `a* ∈ coverage(Σ.L(a).eᵢ)`, then `a` is discoverable from `d` at `Σ'`.

The transition sequence may include K.σ (registering a new document), K.μ⁺ or K.μ⁺_L (extending an existing arrangement, possibly via fork), or any other combination of operations that preserves the link store. Because LP3★ keeps the link's coverage fixed across the entire sequence, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`, so the membership `a* ∈ coverage(Σ.L(a).eᵢ)` carries through to `a* ∈ coverage(Σ'.L(a).eᵢ)`. By the definition of `project`, `v ∈ project(a, i, d, Σ')` since `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) = a* ∈ coverage(Σ'.L(a).eᵢ)`. The link is resurrected.

This is the formal expression of Nelson's "reaching back through to a superseding version" mechanism. The system architecture admits resurrection because (i) the link's stored state is permanent (L12 of ASN-0043), (ii) the I-addresses it references are permanent (S0), (iii) the projection is a live computation that consults the current arrangement at the moment of query, and (iv) discovery is purely I-address-based, indifferent to provenance (LP12 references only coverage and range).

A link can pass through arbitrarily many states of orphanage and resurrection without any modification to its stored data. The link does not "know" that the content has been removed and re-introduced; it does not need to.

## Boundary and Width Behaviour

We address two further questions about the structural behaviour of projection under specific operation patterns.

**LP19 — TightEndsetBoundaryExclusion**: We formalise the "boundary insertion does not extend the link" property by isolating the construction discipline that makes it hold. An endset `e` is *tight at state `Σ_e`* when its coverage is entirely populated at `Σ_e`:
```
tight(e, Σ_e)  ≡  coverage(e) ⊆ dom(Σ_e.C) ∪ dom(Σ_e.L)
```

Equivalently: every I-address denoted by an endset span is allocated as content or as a link at `Σ_e`. Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state. Under tight construction, the link's reach cannot be extended by subsequent allocations:

For any endset `e` tight at `Σ_e`, any state sequence `Σ_e →* Σ →* Σ_post`, and any K.α (or K.λ) transition `Σ → Σ_post` allocating a fresh address `a_new`:
```
a_new ∉ coverage(e)
```

Consequently, if any later K.μ⁺ or K.μ⁺_L transition `Σ_n → Σ_{n+1}` (with `Σ_post →* Σ_n`) extends `Σ_n.M(d)` by a mapping `(v_new, a_new)`, then `v_new ∉ project(e, d, Σ_{n+1})`.

The proof is direct. Each operation supplies the required freshness as a per-call precondition. K.α's precondition (ASN-0093) requires `a_new ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state `Σ` immediately before allocation; K.λ's precondition (ASN-0093) requires `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)`, the same freshness condition with operand order swapped. In both cases the allocated address is fresh against the union `dom(Σ.C) ∪ dom(Σ.L)` at `Σ`. By Store Monotonicity★ applied to the prefix `Σ_e →* Σ`, `dom(Σ.C) ⊇ dom(Σ_e.C)` and `dom(Σ.L) ⊇ dom(Σ_e.L)`. So `a_new ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)`. By the tightness condition, `coverage(e) ⊆ dom(Σ_e.C) ∪ dom(Σ_e.L)`, so `a_new ∉ coverage(e)`. For the consequence: a later K.μ⁺ or K.μ⁺_L transition `Σ_n → Σ_{n+1}` adds the mapping `(v_new, a_new)`, giving `v_new ∈ dom(Σ_{n+1}.M(d))` and `Σ_{n+1}.M(d)(v_new) = a_new`. Since `coverage(e)` is a deterministic function of `e`'s spans (per the coverage definition of ASN-0043) and `e` is a fixed endset value across the entire sequence — `coverage` consults no state component — the membership `a_new ∉ coverage(e)` carries through unchanged to `Σ_{n+1}`. The projection definition then excludes `v_new` from `project(e, d, Σ_{n+1})`.

Tightness is a construction discipline, not a structural invariant the system enforces. The system permits endsets whose spans denote half-open intervals reaching past existing content; such endsets are not tight, and an `a_new` allocated within their forward extent would in fact enter the coverage. The architectural significance of LP19 is that the canonical endset construction — selecting spans whose start and width capture exactly the I-addresses resident at construction time — produces tight endsets, and tight endsets are immune to absorbing addresses produced by subsequent K.α or K.λ. Boundary insertion as a composite (K.α + K.μ⁺) cannot enlarge a tight link's reach.

**LP20 — RangeConfinement**: For every endset `e`, document `d`, state `Σ`:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))
```

Split by V-position subspace, the confinement reads:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C} ⊆ coverage(e) ∩ dom(Σ.C)
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L} ⊆ coverage(e) ∩ dom(Σ.L)
```

The projection only reaches V-positions mapping to allocated content or links. Addresses in `coverage(e) ∖ (dom(Σ.C) ∪ dom(Σ.L))` (I-addresses denoted by endset spans but not yet allocated, or never to be allocated) are never in `ran(Σ.M(d))`. The argument splits by subspace, drawing two facts from ASN-0047. S3★-aux (SubspaceExhaustiveness) discharges exhaustiveness — every `v ∈ dom(Σ.M(d))` satisfies `subspace(v) ∈ {s_C, s_L}`, so no V-position escapes the two-case analysis. S3★ (GeneralizedReferentialIntegrity) supplies the per-subspace targets: for content-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.C)`; for link-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.L)`. Either way, the V-positions in the projection always correspond to I-addresses that have been allocated. The projection cannot "see" hypothetical future addresses.

**LP21 — RepresentationInvariance**: For any two endsets `e₁, e₂` with `coverage(e₁) = coverage(e₂)`:
```
project(e₁, d, Σ) = project(e₂, d, Σ)
```

The projection depends only on coverage, not on the span decomposition of the endset. Two endsets with the same coverage are interchangeable for projection purposes. This is a direct corollary of the definition: the set comprehension references `coverage(e)`, not the spans within `e`.

## What the Link Holder Can Rely On

We have established a catalogue of guarantees. We now consolidate them into a holder-facing summary.

The holder owns the link `a` and possesses, at minimum, knowledge of its address and the endsets at each slot. Across any state evolution `Σ →* Σ'`:

- The address `a` remains in `dom(Σ'.L)` (Store Monotonicity★).
- The endsets `Σ'.L(a).eᵢ` are byte-identical to `Σ.L(a).eᵢ` for every slot (LP2★).
- The slot ordering is preserved — what was at slot 1 is still at slot 1, the type endset is still at slot 3 (LP2★).
- The coverage of each endset is fixed — `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (LP3★).
- The I-addresses in coverage all remain in `dom(Σ'.C)` if they were ever in `dom(Σ.C)` (Store Monotonicity★), with their content values unchanged (S0, applied step-wise across the sequence).

What can vary:

- Which documents the link can be discovered from. This depends on which documents currently arrange any I-address in any endset's coverage (LP12). Documents may transclude the linked content (gaining discoverability — LP9, LP16), or delete it (losing discoverability — LP10), at any time.
- The specific V-positions of any projection. These reflect the document's current arrangement and shift as the document is edited (LP9, LP10, LP11).
- The shape of any projection — contiguous, fragmented, partial — depends on the arrangement, not on the link.

What is *not* possible:

- The link cannot have its endsets rewritten (L12, ASN-0043).
- The link cannot have its slots permuted (LP2).
- The link cannot have its coverage altered by any external party (LP3).
- The link cannot be made un-discoverable while there exists any document arranging any I-address in any of its endsets' coverage (LP12).
- The link cannot be discovered from a document with no arrangement entry mapping to any I-address in coverage (LP12, contrapositive).
- The link's discoverability cannot be made to depend on which document created it or which document allocated its linked content (LP12 references only coverage and range, indifferent to provenance).
- Boundary insertion of newly allocated content into a tightly constructed link's reach cannot grow that reach (LP19).

The trust relationship between the link holder and the system is asymmetric. The system commits unconditionally to LP2, LP3, and S0 (together with L12 of ASN-0043) — to the permanence of every stored object. The system commits conditionally to LP9–LP18 — to the discoverability of the link, contingent on what the document holders choose to do with their arrangements. The holder cannot prevent another document holder from deleting the linked content from their own arrangement (subject to their own ownership rules). The holder can rely on the content persisting somewhere in `dom(Σ.C)` permanently, but cannot rely on it persisting in any particular `ran(Σ.M(d))` indefinitely. Survival of discoverability requires only that *somewhere* in the system, *some* document still arranges *some* of the linked content. This is the strongest guarantee the architecture provides, and it is sufficient for the holder's purpose: the link's content can be re-introduced via transclusion at any time, and the link will then be re-projected at the new V-positions automatically and without any action by the holder.

## A Worked Trace

To make the displacement concrete, we trace a small example. Consider:

- A link `a` with endset `e₁ = {(i₀, ℓ)}`. By T12 (ASN-0034), `coverage(e₁) = {t ∈ T : i₀ ≤ t < i₀ ⊕ ℓ}` — the entire half-open interval, not merely a discrete set. The I-addresses `i₁, i₂, i₃, i₄` satisfy `i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ` and `i₁, …, i₄ ∈ dom(Σ.C)`; the interval `coverage(e₁)` contains these four addresses (along with any other tumbler lying in the interval). For trace clarity we follow only these four, since they are precisely the addresses in `coverage(e₁) ∩ ran(Σ.M(d₁))` for the document considered below — and by LP12 the projection through `d₁` is governed by that intersection, not by the full coverage.
- A document `d₁` whose content subspace arranges these four I-addresses in order: `Σ.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃, v₄ ↦ i₄}`, with `v_k = [s_C, 1, …, 1, k]` so the sequence `(v₁, v₂, v₃, v₄)` satisfies D-SEQ★ at content-subspace count `n_{s_C} = 4`.

At state `Σ`:
```
project(a, 1, d₁, Σ) = {v₁, v₂, v₃, v₄}
```

Apply K.μ⁻ retaining the first three content-subspace positions (so `n'_{s_C} = 3`), producing state `Σ_1`:
```
Σ_1.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃}
project(a, 1, d₁, Σ_1) = {v₁, v₂, v₃}
```

The projection has shrunk by `{v₄}` (per LP10's exact characterisation), and the retained set `{v₁, v₂, v₃}` is the D-SEQ★-admissible prefix permitted by K.μ⁻. The I-address `i₄` is still in `dom(Σ.C)` by S0, but no longer in `ran(Σ_1.M(d₁))`. The link's coverage is unchanged — still the half-open interval `{t ∈ T : i₀ ≤ t < i₀ ⊕ ℓ}`, of which `{i₁, i₂, i₃, i₄}` remain the traced members.

Now suppose another document `d₂` is registered and transcludes `i₄` via K.σ followed by K.μ⁺, producing state `Σ_2`:
```
Σ_2.M(d₂) = {w₁ ↦ i₄}
project(a, 1, d₂, Σ_2) = {w₁}
```

The link is now discoverable from both `d₁` (where the projection is `{v₁, v₂, v₃}` reaching `{i₁, i₂, i₃}`) and `d₂` (where the projection is `{w₁}` reaching `{i₄}`). Together the two projections reach the four traced I-addresses `{i₁, i₂, i₃, i₄}` — the entirety of `coverage(e₁)` that bears on these documents' ranges — despite no single document containing all four.

To exhibit projection motion clearly under K.μ~, consider slot 2 of the link, with endset `e₂` chosen so that `coverage(e₂) ∩ ran(Σ_1.M(d₁)) = {i₁}` — only the I-address `i₁` from `d₁`'s current range lies in this slot's coverage (admissible by L4 of ASN-0043, which imposes no constraint on which I-addresses an endset references; for trace clarity we follow only the intersection with `d₁`'s range, since by LP12 that intersection is what governs projection through `d₁`). At `Σ_1`:
```
project(a, 2, d₁, Σ_1) = {v₁}
```
— a strict subset of `dom(Σ_1.M(d₁)) = {v₁, v₂, v₃}`, because among the V-positions of `Σ_1.M(d₁)` only `v₁` maps to an I-address in `coverage(e₂)`.

Now apply K.μ~ to `d₁` via a bijection `π` that permutes the V-positions, fixing `dom(Σ_1.M(d₁))` setwise (per K.μ~-FIX of ASN-0047):
```
π(v₁) = v₃, π(v₂) = v₂, π(v₃) = v₁
Σ_3.M(d₁) = {v₃ ↦ i₁, v₂ ↦ i₂, v₁ ↦ i₃}
project(a, 1, d₁, Σ_3) = {v₃, v₂, v₁} = π(project(a, 1, d₁, Σ_1))
project(a, 2, d₁, Σ_3) = {v₃} = π({v₁}) = π(project(a, 2, d₁, Σ_1))
```

The slot-2 projection moves: it was `{v₁}` at `Σ_1`, it is `{v₃}` at `Σ_3`. The I-address `i₁` is now carried at V-position `v₃` rather than `v₁` — the projection followed its content from `v₁` to `π(v₁) = v₃`. The slot-1 projection set looks unchanged ({v₁, v₂, v₃} as a set) only because it happens to coincide with the entire domain; per-V-position, the binding has shifted (v₁ now carries i₃ rather than i₁, etc.).

Per LP11, both projections' V-positions are permuted by `π`, and the set of I-addresses reached is unchanged within each slot. The link "followed its content" through the reordering.

At no point during this trace did the link itself change. The link's address, endsets, coverage, and slot ordering remained byte-identical from `Σ` through `Σ_3`. What displaced was the projection, and the displacement was entirely a function of the operations applied to the documents' arrangements.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LP2 | `(A Σ → Σ', a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| : Σ'.L(a).eᵢ = Σ.L(a).eᵢ)` — slot invariance | introduced |
| LP2★ | Multi-step slot invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ` | introduced |
| LP3 | `(A Σ → Σ', a, i : a ∈ dom(Σ.L) : coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))` — coverage invariance | introduced |
| LP3★ | Multi-step coverage invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` | introduced |
| Store Monotonicity★ | `Σ →* Σ' ⟹ dom(Σ.C) ⊆ dom(Σ'.C) ∧ dom(Σ.L) ⊆ dom(Σ'.L)` | introduced |
| project | `project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}` — the live projection function | introduced |
| LP4 | `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)` — arrangement specificity | introduced |
| LP5 | Cross-document independence: projection through `d` unaffected by edits to `d' ≠ d` (frames over K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) | introduced |
| LP6 | K.α (content allocation) does not displace any projection | introduced |
| LP7 | K.λ (link allocation) does not displace existing projections | introduced |
| LP8 | K.σ (document registration) does not displace existing projections | introduced |
| LP14 | K.ρ (provenance recording) does not displace any projection | introduced |
| LP9 | K.μ⁺ and K.μ⁺_L can only enlarge projection; new V-positions come from new arrangement entries | introduced |
| LP10 | K.μ⁻ can only shrink projection; lost V-positions come from removed arrangement entries | introduced |
| LP11 | K.μ~ rebinds projection: `project(e, d, Σ') = π(project(e, d, Σ))` via bijection π | introduced |
| discoverable_from | `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)` (defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`) | introduced |
| LP12 | `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` | introduced |
| LP13 | Partial survival: discoverability requires only that some I-address in some slot's coverage-range intersection remain | introduced |
| LP16 | Transclusion confers discoverability: shared I-addresses transfer discoverability across documents | introduced |
| LP17 | Ghost projection: orphaned links persist in `dom(Σ.L)` with empty projections everywhere | introduced |
| LP18 | Resurrection: re-introducing a coverage I-address via K.μ⁺ or K.μ⁺_L restores discoverability | introduced |
| tight | `tight(e, Σ_e) ≡ coverage(e) ⊆ dom(Σ_e.C) ∪ dom(Σ_e.L)` — tight endset construction predicate | introduced |
| LP19 | Tight endset boundary exclusion: under tight construction, K.α/K.λ-allocated addresses fall outside coverage | introduced |
| LP20 | Range confinement: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))` | introduced |
| LP21 | Representation invariance: equal coverage implies equal projection | introduced |

*Numbering note.* Labels LP1, LP15 are deliberately absent. LP14 and LP15 from earlier drafts of this ASN were collapsed in revision; LP14 has been reclaimed here to label the K.ρ frame lemma added in this revision. LP1 was never assigned. Other labels (LP2 through LP21, omitting LP15) preserve their revision-history identities.

## Open Questions

What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?

Under what conditions must the projection of an endset through a document be expressible as a finite union of contiguous V-ranges, given that K.μ~ can scatter formerly contiguous projections into arbitrary subsets of the V-domain?

What guarantees must the system provide about the *V-order* of positions within a single projection — does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?

What invariants must the system maintain when a link's endset references the address of another link (rather than content) — under what conditions must the discovery of one link induce the discovery of the other?

What does the system guarantee about a link whose coverage spans I-addresses partially outside `dom(Σ.C)` at link-creation time — what must remain true if future K.α allocations fall within the previously unallocated portion of the coverage?

Under what conditions must the system commit to producing identical projections for two documents that have undergone "the same" sequence of editing operations, given that arrangement state is per-document and operations are not directly comparable across documents?

What invariants must hold across a fork composite when the source document's link-subspace V-positions are not transcluded into the new document — how does this affect the projection of the source document's home-document-allocated links through the new document?
