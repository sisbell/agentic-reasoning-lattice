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

*Working reference frame.* This ASN operates in the ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate.

## The Coverage of an Endset

For an endset `e ⊆ Span`, the *coverage* `coverage(e)` is the set of I-addresses denoted by `e`'s spans, defined in ASN-0043 as

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
```

Each span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}` by T12 of ASN-0034, where `s ⊕ ℓ ∈ T` exists by TA0 because `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are well-formedness conditions of the span. Coverage is a set of I-addresses in `T`. Some of these I-addresses may be in `dom(Σ.C)` at the time the endset was constructed; some may not. Crucially, coverage is a *purely combinatorial* property of the endset's span representation — it does not consult any state component. Coverage depends on the spans; nothing else.

By L5 (EndsetSetSemantics, ASN-0043), an endset is an unordered set. Two endsets with the same set of spans have the same coverage. The lossy projection `Endset → 2^T` defined by `coverage` is not injective: distinct span decompositions can have identical coverage (for instance, splitting a single span at an interior point produces two spans whose coverage equals the original).

## The Projection Operation

For an endset `e`, a document `d ∈ dom(Σ.M)`, and a state `Σ`, define the *projection of `e` through `d` at `Σ`* as the set of V-positions in `d`'s arrangement whose I-addresses lie within `e`'s coverage:

```
project(e, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

The precondition `d ∈ dom(Σ.M)` is what makes `Σ.M(d)` well-defined; `project(e, d, Σ)` is left undefined when `d ∉ dom(Σ.M)`. For a link `a ∈ dom(Σ.L)` with slot `i ∈ {1, …, |Σ.L(a)|}`, write `project(a, i, d, Σ) ≡ project(Σ.L(a).eᵢ, d, Σ)`, defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`.

The definition reads from two inputs:
- The endset, fixed once and for all by the link's creation (and immune to subsequent transitions, by L12).
- The arrangement `Σ.M(d)`, mutable and reflecting whatever edits `d` has undergone.

Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still — and the definition consults neither `Σ.C` nor `Σ.L` separately. Therefore every change in projection must be attributable to a change in `Σ.M(d)` — and we can characterise the change by examining what each editing operation does to `Σ.M(d)`.

Three degenerate configurations follow directly from the definition and require no separate treatment in subsequent claims. The projection of the empty endset is uniformly empty: `project(∅, d, Σ) = ∅` for every `d ∈ dom(Σ.M), Σ` (i.e., wherever `project` is defined), since `coverage(∅)` is the empty union over an empty index set. The projection through an empty arrangement is uniformly empty: `project(e, d, Σ) = ∅` for every `d ∈ dom(Σ.M), Σ` with `dom(Σ.M(d)) = ∅`, since the set comprehension ranges over the empty domain. A link with empty from/to endsets but a non-empty type endset (admitted by L3 of ASN-0043, which requires only the type slot to be non-empty) has empty projections at slots 1 and 2 regardless of any document's state; only the type slot's projection can be non-empty.

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

This is the reflexive-transitive closure of LP2 under the following schema, which we state once and reuse.

*Closure schema (★).* Let `P(Σ, Σ')` be a finite conjunction of membership-persistence clauses (`x ∈ dom(Σ.X) ⟹ x ∈ dom(Σ'.X)`) and value-preservation clauses (`f(Σ') = f(Σ)`, each accessor `f` well-defined once its accompanying membership clause holds). If the single-step guarantee `Σ → Σ' ⟹ P(Σ, Σ')` holds, then so does its closure `Σ →* Σ' ⟹ P(Σ, Σ')`. Proof by induction on the length of the transition sequence: the empty sequence (`Σ = Σ'`) discharges every clause — memberships by reflexivity of `∈`, equalities by reflexivity of `=`; the inductive step `Σ →* Σ_n → Σ'` composes the induction hypothesis `P(Σ, Σ_n)` with the single step `P(Σ_n, Σ')` — memberships chain through `Σ_n`, value-equalities by transitivity of `=`.

LP2★ is schema (★) applied to LP2, with `P(Σ, Σ') ≡ a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ`.

**LP3 — CoverageInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

LP2 supplies both conjuncts: `a ∈ dom(Σ'.L)` directly (so the slot accessor on the left-hand side of the coverage equation is well-defined), and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` from which the coverage equation follows by applying `coverage` to both sides. The set of I-addresses the link refers to is computed from its endsets; if the endsets are byte-identical between states, the coverage is identical between states. Combining L12 with LP2 and LP3: the link, the slot, and the I-addresses it reaches are all permanent. What can vary is only which of those I-addresses are currently arranged in any given document.

**LP3★ — MultiStepCoverageInvariance**: For every reachable state sequence `Σ →* Σ'`, every `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

Schema (★) of LP2★ applied to LP3, with `P(Σ, Σ') ≡ a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`.

**Store Monotonicity★**: For every reachable state sequence `Σ →* Σ'`:
```
dom(Σ.C) ⊆ dom(Σ'.C)  ∧  dom(Σ.L) ⊆ dom(Σ'.L)
```

Schema (★) of LP2★ applied to the single-step monotonicity guarantees C0 of ASN-0093 (content) and L12 of ASN-0093 (links, in its membership-persistence consequence), with `P(Σ, Σ') ≡ dom(Σ.C) ⊆ dom(Σ'.C) ∧ dom(Σ.L) ⊆ dom(Σ'.L)` (the containment clauses are the set-valued instance of the schema's membership-persistence form).

These invariants pin down what a link holder owns. Subsequent operations by any party — even the holder, even the original creator — cannot rewrite the endsets. The link is, in this strict sense, a permanent record.

## Frame Conditions: When Projection Does Not Move

A projection moves only if its inputs move. Since the endset (and therefore its coverage) is fixed by LP3, the projection through a document moves only if that document's arrangement is modified — and even then, only if the modification affects V-positions whose I-addresses lie in the endset's coverage.

**LP4 — ArrangementSpecificity**: For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

The projection function depends on exactly two inputs: `coverage(e)` and `Σ.M(d)`. The first is a pure function of the endset `e`, which appears unchanged on both sides of the equality — `coverage(e)` is therefore identical between the two projections. The second is the arrangement, equal by hypothesis. Both inputs agree pointwise, so the set comprehension produces identical results. The projection cannot displace without `Σ.M(d)` displacing.

*Frame note.* LP4 quantifies `d` over `dom(Σ.M) ∩ dom(Σ'.M)` so that both sides of the hypothesis and conclusion are well-defined under the same membership obligation.

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

Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them. This is the precise sense in which "insertion at the boundary of a linked passage" cannot extend the link's reach: insertion as a composite (allocate + arrange) splits into a K.α step (no projection effect) and a K.μ⁺ step. The K.μ⁺ step might add a V-position to the projection, but only if the new V-position's I-address is in `coverage(e)`. By T10a (AllocatorDiscipline, ASN-0034), each new K.α-allocated I-address is structurally distinct from all prior allocations.

**LP7 — Link-Allocation Invariance**: The K.λ operation modifies only `Σ.L`; its frame is `(A d :: M'(d) = M(d))`, and K.λ preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`. Creating a new link cannot retroactively affect the projection of any other link.

**LP8 — Document-Registration Invariance**: For any document-registration transition `Σ → Σ'` — either K.σ (ASN-0093) or K.δ in the IsDocument case (ASN-0047) — registering a fresh document `d_new` (with `d_new ∉ dom(Σ.M)`, `dom(Σ'.M) = dom(Σ.M) ∪ {d_new}`, `Σ'.M(d_new) = ∅`, and `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`) and any endset `e`, both:

(a) Pre-state preservation: `(A d ∈ dom(Σ.M) :: project(e, d, Σ') = project(e, d, Σ))`.

(b) Newly-registered emptiness: `project(e, d_new, Σ') = ∅`.

Both K.σ (ASN-0093) and K.δ-IsDocument (ASN-0047) satisfy the document-registration form named in the hypothesis: both extend `dom(M)` by one fresh document, initialise the new document's arrangement to `∅`, and preserve every pre-existing arrangement pointwise. Their effects on the `Σ.M` component are structurally identical for the purposes of projection.

Postcondition (a) follows by LP4 applied to each `d ∈ dom(Σ.M)`: the document-registration frame holds `Σ'.M(d) = Σ.M(d)` for every such `d`. Postcondition (b) follows from the definition of `project`: with `d_new ∈ dom(Σ'.M)` (so the projection is defined) and `dom(Σ'.M(d_new)) = ∅`, the set comprehension `{v ∈ dom(Σ'.M(d_new)) : Σ'.M(d_new)(v) ∈ coverage(e)}` ranges over the empty domain and is empty.

*Remark on K.δ.* K.δ-IsNode and K.δ-IsAccount have frame `M' = M`, so LP4 covers them; K.δ-IsDocument is the document-registration case of LP8.

**LP14 — ProvenanceRecording Invariance**: The K.ρ operation (ASN-0047), which records provenance by adding a pair to `Σ.R`, has frame `(A d :: M'(d) = M(d))` — it leaves every document's arrangement intact — and preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.ρ transition. Provenance bookkeeping does not displace any projection.

## Operation Effects on Projection

We now examine each operation that *can* displace a projection. The pattern is uniform: each K.μ operation modifies `Σ.M(d)` in a constrained way, and the projection follows mechanically.

**LP9 — Extension under K.μ⁺ and K.μ⁺_L**: For every extension transition `Σ → Σ'` operating on document `d` — either K.μ⁺ (content-subspace extension) or K.μ⁺_L (link-subspace extension) — and every endset `e`:
```
project(e, d, Σ) ⊆ project(e, d, Σ')
```

The proof relies on exactly two structural facts about the post-state arrangement:
- (E1) *Strict domain extension:* `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))`.
- (E2) *Prior-domain agreement:* `(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`.

Both K.μ⁺ and K.μ⁺_L (ASN-0047) supply (E1) and (E2) directly in their effect clauses, so the projection-level argument is identical for both: for any `v ∈ project(e, d, Σ)`, `v ∈ dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` by (E1), and `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)` by (E2) and the definition of `project`, so `v ∈ project(e, d, Σ')`. The projection can only grow.

The new V-positions that enter the projection are exactly the new arrangement entries whose I-addresses fall in the coverage:
```
project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}
```

The forward inclusion (⊆): suppose `v ∈ project(e, d, Σ') ∖ project(e, d, Σ)`. Then `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ coverage(e)` by the first conjunct. For the second, either `v ∉ dom(Σ.M(d))` or `Σ.M(d)(v) ∉ coverage(e)`. The second alternative is excluded: if `v ∈ dom(Σ.M(d))`, the agreement clause gives `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, contradicting `v ∉ project(e, d, Σ)`. So `v ∉ dom(Σ.M(d))`, placing `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))`. The reverse inclusion (⊇): if `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))` with `Σ'.M(d)(v) ∈ coverage(e)`, then `v ∈ project(e, d, Σ')` directly; and `v ∉ project(e, d, Σ)` since `v ∉ dom(Σ.M(d))`.

When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, whether the projection grows depends on the endset's construction discipline. When K.μ⁺ adds entries mapping V-positions to *existing* I-addresses (the transclusion case), the projection grows by precisely those new V-positions whose mappings fall in coverage. This is the mechanism by which a link "comes into view" in a document that newly transcludes its target content. K.μ⁺_L exhibits the same growth behaviour for link-subspace V-positions when an existing link address is admitted into a home-document arrangement.

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

*Boundary case — empty arrangement.* K.μ⁻'s precondition admits retention `n'_S = 0` for every subspace `S`, provided the pre-state has at least one position so that the strict-shrink clause `(E S :: n'_S < n_S)` is discharged (the pre-state condition `dom(Σ.M(d)) ≠ ∅` is required by the operation regardless). When `n'_S = 0` holds for both `s_C` and `s_L`, the post-state arrangement is empty: `dom(Σ'.M(d)) = ∅`. In this case `project(e, d, Σ') = ∅` for every endset `e`, since the comprehension ranges over the empty domain. The exact-difference formula above specialises directly: with `dom(Σ'.M(d)) = ∅`, the set-difference `dom(Σ.M(d)) ∖ dom(Σ'.M(d)) = dom(Σ.M(d))`, so the formula's right-hand side becomes `{v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)} = project(e, d, Σ)`; substituting `project(e, d, Σ') = ∅` on the left-hand side, the formula reads `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)` — every V-position that was in the pre-state projection has departed. The lemma's inclusion `project(e, d, Σ') ⊆ project(e, d, Σ)` holds vacuously.

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

The atomic per-step lemmas LP4–LP10 and LP14 cover every *atomic* operation kind of the working frame. Since reachable sequences `Σ →* Σ'` decompose into finite chains of atomic transitions (SequentialTransitionAxiom of ASN-0093), any multi-step argument is analysed step-by-step, each atomic step governed by one of these lemmas. LP11 is composite-level (K.μ~ = K.μ⁻ + K.μ⁺ per ASN-0047); the atomic decomposition is governed by LP10 then LP9, and LP11 supplies the net effect `project' = π(project)`.

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

Direct from definitions. Per-slot first: `v ∈ project(a, i, d, Σ)` requires `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, which requires some I-address in the coverage to be in the range. Conversely, any I-address `a*` in `coverage(eᵢ) ∩ ran(Σ.M(d))` is reached by some `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a*`, and that `v` lies in `project(a, i, d, Σ)`. This gives the per-slot biconditional `project(a, i, d, Σ) ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`. Lifting existentially over `i ∈ {1, …, |Σ.L(a)|}` preserves the biconditional: `(E i : project(a, i, d, Σ) ≠ ∅) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)`. Unfolding the left-hand side via the `discoverable_from` definition completes the biconditional.

LP12 characterises discoverability at a fixed state. The matching question for *displacement* is: given a particular editing operation, what must already hold at the pre-state for discoverability to survive into the post-state? K.μ⁻ is the only K.μ family member that can *destroy* discoverability (K.μ⁺ and K.μ⁺_L can only enlarge projections by LP9; K.μ~ rebinds without altering the I-addresses reached by LP11), so it is the natural site for a weakest-precondition derivation. We compute wp explicitly.

**LP12a — ContractionDiscoverabilityWP**: Fix a K.μ⁻ operation on document `d ∈ dom(Σ.M)` with retention parameters `(n'_{s_C}, n'_{s_L})` admissible under K.μ⁻'s precondition, and let
```
R := ⋃ {[S, 1, ..., 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}
```
denote the resulting retention set — determined by the parameters and the per-subspace V-position depths, fixed before the transition fires. For every link `a ∈ dom(Σ.L)`, the weakest precondition on the pre-state `Σ` under which `discoverable_from(a, d, Σ')` holds in the post-state `Σ' = K.μ⁻[d, R](Σ)` is:
```
wp(K.μ⁻[d, R], discoverable_from(a, d, ·))
  ≡ enabled(K.μ⁻[d, R]) ∧ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ∩ R ≠ ∅)
```
where `enabled(K.μ⁻[d, R])` is K.μ⁻'s applicability predicate — `d ∈ E_doc`, `dom(Σ.M(d)) ≠ ∅`, the strict-shrink admissibility `(E S :: n'_S < n_S)`, and `R` a valid D-SEQ★ prefix set — under which the post-state `Σ' = K.μ⁻[d, R](Σ)` exists. The enabledness conjunct is required for total correctness: at a state where K.μ⁻ is not applicable, no post-state exists, so the second conjunct (the postcondition pullback derived below) can hold vacuously while `discoverable_from(a, d, Σ')` is unrealisable. The derivation below establishes the pullback conjunct under the standing assumption that K.μ⁻ is enabled at `Σ`.

Derivation. We work backward from the postcondition. By the discoverable_from definition applied at `Σ'`, and using LP2 (which fixes both `a ∈ dom(Σ'.L)` and `|Σ'.L(a)| = |Σ.L(a)|`) to keep the slot index range stable:
```
discoverable_from(a, d, Σ')
  ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ') ≠ ∅)
```

We reduce `project(a, i, d, Σ')` to a predicate on the pre-state. K.μ⁻'s effect clause (ASN-0047) supplies the *form* `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` together with the *agreement* `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ'.M(d))`; K.μ⁻'s contracted-arrangement definition (ASN-0047, "The contracted arrangement: `M'(d) = M(d) ↾ R`") identifies the post-state domain as `dom(Σ'.M(d)) = dom(Σ.M(d)) ∩ R`. The retention set's subspace structure — each component is a D-SEQ★-prefix `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` of `V_S(d) ⊆ dom(Σ.M(d))` with `n'_S ≤ n_S = |V_S(d)|` (K.μ⁻'s admissibility precondition combined with D-SEQ★ of ASN-0047) — yields `R ⊆ dom(Σ.M(d))`, so the intersection collapses to `dom(Σ'.M(d)) = R`, with the agreement clause now applying to every `v ∈ R`. LP10's exact-difference formula, applied to the endset `Σ.L(a).eᵢ` (with `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` by LP2 so the coverage is unchanged), yields:
```
project(a, i, d, Σ) ∖ project(a, i, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ R : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}
```
Since `project(a, i, d, Σ) ⊆ dom(Σ.M(d))` by the projection definition, the difference is precisely the subset of the pre-state projection that fell outside `R`. The complement within the pre-state projection — `project(a, i, d, Σ) ∩ R` — is exactly the post-state projection: for `v ∈ project(a, i, d, Σ) ∩ R`, the agreement clause gives `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)` with `v ∈ dom(Σ'.M(d))`, so `v ∈ project(a, i, d, Σ')`; conversely, every `v ∈ project(a, i, d, Σ')` satisfies `v ∈ R ⊆ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, so `v ∈ project(a, i, d, Σ) ∩ R`. Hence:
```
project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R
```
The per-slot non-emptiness biconditional `project(a, i, d, Σ') ≠ ∅ ⟺ project(a, i, d, Σ) ∩ R ≠ ∅` then lifts existentially over slots — preserving the biconditional because the slot range is unchanged — to produce the pullback conjunct of the wp statement.

*Boundary case — empty retention.* K.μ⁻ admits maximal contraction with `n'_{s_C} = n'_{s_L} = 0`, producing `R = ∅`, provided the pre-state has at least one position so that the strict-shrink clause `(E S :: n'_S < n_S)` is discharged. At `R = ∅` the wp specialises:
```
(E i : project(a, i, d, Σ) ∩ ∅ ≠ ∅) ≡ (E i : ∅ ≠ ∅) ≡ false
```
The wp evaluates to false unconditionally — no pre-state projection, however large, can render discoverability preservable when the entire arrangement of `d` is deleted. The link `a` itself persists by LP13, but discoverability from this specific document is unrecoverable until a subsequent K.μ⁺ or K.μ⁺_L re-introduces a coverage I-address (LP18, resurrection). This boundary case isolates the precise sense in which storage and discoverability are independently regulated: storage cannot be undone by any contraction, but discoverability from a specific document can be — by exhaustive deletion of that document's arrangement.

The phrase "anything is left at each end" can now be stated formally: discoverability from `d` requires that, for at least one slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`. For mere existence of the link, nothing is required at all — this is the substantive content of the next claim.

**LP13 — UnconditionalLinkPersistence**: For every reachable state sequence `Σ →* Σ'` and every link `a ∈ dom(Σ.L)`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)
```

LP2★ gives `a ∈ dom(Σ'.L)` and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` for every slot `i ∈ {1, …, |Σ.L(a)|}`, and fixes the arity `|Σ'.L(a)| = |Σ.L(a)|` (value preservation under L12 forces equal-length sequences). Slot-wise equality at every position of a common arity is full value equality, so `Σ'.L(a) = Σ.L(a)`. The conclusion holds independently of `Σ.M`, `Σ'.M`, `dom(Σ.M)`, `dom(Σ'.M)`, and any document's range; the hypothesis `a ∈ dom(Σ.L)` is the only requirement, and the conclusion never consults whether `a` is discoverable from any document.

LP13 is independent of every `Σ.M` term, so a link's persistence does not depend on its discoverability from any document: a holder can rely on the stored object permanently, but not on discoverability from any particular document without further conditions on that document's arrangement (LP9–LP11 govern how those conditions evolve).

## Discovery Independence of Origin

We have characterised discoverability *from* a particular document. Now we ask: how does this relate to which document created the link, which document allocated the linked content, and which document the holder is following the link from?

Three documents may be in play for any given link reference:
- The *home document* of the link, `home(a)` = `origin(a)` — the document under whose tumbler prefix the link's address was allocated (L1a, ASN-0093).
- The *origin document* of each I-address in coverage, `origin(a*)` — the document under whose tumbler prefix `a*` was allocated.
- The *navigating document* `d` from which the holder follows the link.

These three may be the same, all different, or any combination. The discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement. This is visible by inspection of LP12: the right-hand side references `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))` and nothing else. The characterisation contains no reference to `home(a)` or to the origin documents of coverage I-addresses. The home document is a metadata property of the link's address (recoverable by tumbler projection — S7 of ASN-0036), not a constraint on where the link can be reached from. Similarly, origin is a metadata property of each coverage I-address, indifferent to whether `d` was the document that allocated the address or some unrelated document that has since transcluded it. A link can therefore be discovered from any document whose arrangement currently maps to any I-address in any of the link's endsets' coverage, regardless of provenance. The system commits to indifference of provenance at the point of discovery.

The transclusion mechanism is the architectural lever that activates this provenance-indifference.

**LP16 — TransclusionDiscoverability**: For any link `a ∈ dom(Σ.L)`, slot `i ∈ {1, …, |Σ.L(a)|}`, and documents `d_src, d_new ∈ dom(Σ.M)` at state `Σ`:
```
coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new)) ≠ ∅
  ⟹  discoverable_from(a, d_src, Σ) ∧ discoverable_from(a, d_new, Σ)
```

Let `a*` be any I-address in the triple intersection: `a* ∈ coverage(Σ.L(a).eᵢ)`, `a* ∈ ran(Σ.M(d_src))`, and `a* ∈ ran(Σ.M(d_new))`. By `a* ∈ ran(Σ.M(d_src))`, there exists `v_src ∈ dom(Σ.M(d_src))` with `Σ.M(d_src)(v_src) = a*`, so `v_src ∈ project(a, i, d_src, Σ)`, hence `project(a, i, d_src, Σ) ≠ ∅`. Symmetrically `v_new ∈ project(a, i, d_new, Σ)` for some `v_new`. By the discoverable_from definition (witnessed at slot `i`), both `discoverable_from(a, d_src, Σ)` and `discoverable_from(a, d_new, Σ)` hold.

The triple intersection is exactly the condition transclusion produces: when `d_new` transcludes some content from `d_src` (via a fork composite or any K.μ⁺ that adds arrangement entries mapping V-positions to I-addresses already in `ran(Σ.M(d_src))`), the shared I-addresses are members of `ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new))`. If any of these shared I-addresses also lies in `coverage(Σ.L(a).eᵢ)` for some link `a` and slot `i`, the lemma's hypothesis is met. Discoverability extends to every document that transcludes any I-address in coverage. No notification of the link is required; the link is *passively* discoverable from `d_new` simply because `d_new` arranges the I-address.

This is the architectural mechanism behind Nelson's "a link to one version is a link to all versions" claim and the cross-document discovery property: link discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition.

## Ghost Projection and Resurrection

We consider two corner cases: when nothing in the system reaches a link's coverage, and when re-introduction of content restores reachability.

**LP17 — GhostProjection**: Suppose at state `Σ` no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`:
```
(A d ∈ dom(Σ.M), i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)
```

Then by LP12, `project(a, i, d, Σ) = ∅` for every `d, i`. The link is *orphaned*: not discoverable from any document. By L12 (ASN-0043), `a` remains in `dom(Σ.L)` and `Σ.L(a)` is unchanged. The link is not destroyed; it is invisible to forward navigation, but its stored endsets continue to identify the I-addresses it once reached, and the I-addresses themselves continue to exist in `dom(Σ.C)` by S0.

**LP18 — Resurrection**: If `a` is orphaned at `Σ` and a subsequent transition sequence `Σ →* Σ'` introduces an arrangement entry `Σ'.M(d)(v) = a*` for some `d, v, a*` with `a* ∈ coverage(Σ.L(a).eᵢ)`, then `a` is discoverable from `d` at `Σ'`.

The transition sequence may include any document-registration operation (K.σ of ASN-0093 or K.δ in the IsDocument case of ASN-0047 — unified by LP8 as having structurally identical effects on `Σ.M`), K.μ⁺ or K.μ⁺_L (extending an existing arrangement, possibly via fork), or any other combination of operations that preserves the link store. The orphan premise supplies `a ∈ dom(Σ.L)`. Store Monotonicity★ applied to `Σ →* Σ'` lifts this to `a ∈ dom(Σ'.L)`, making the slot accessor `Σ'.L(a).eᵢ` well-defined at the post-state. Because LP3★ keeps the link's coverage fixed across the entire sequence, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`, so the membership `a* ∈ coverage(Σ.L(a).eᵢ)` carries through to `a* ∈ coverage(Σ'.L(a).eᵢ)`. By the definition of `project`, `v ∈ project(a, i, d, Σ')` since `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) = a* ∈ coverage(Σ'.L(a).eᵢ)`. The link is resurrected.

This is the formal expression of Nelson's "reaching back through to a superseding version" mechanism. The system architecture admits resurrection because (i) the link's stored state is permanent (L12 of ASN-0043), (ii) the I-addresses it references are permanent (S0), (iii) the projection is a live computation that consults the current arrangement at the moment of query, and (iv) discovery is purely I-address-based, indifferent to provenance (LP12 references only coverage and range).

A link can pass through arbitrarily many states of orphanage and resurrection without any modification to its stored data. The link does not "know" that the content has been removed and re-introduced; it does not need to.

## Boundary and Width Behaviour

We address two further questions about the structural behaviour of projection under specific operation patterns.

The set `F` of *substrate-emittable addresses* is the domain against which the "boundary insertion does not extend the link" property is formalised — the addresses the substrate could K.α/K.λ-emit within a span's reach, excluding the T4-invalid zero-extensions `s.0`, `s.0.0`, … that a raw span includes but no allocator chain can emit (T10a.4, ASN-0034).

By ASN-0093, every K.α/K.λ-allocated address is a chain element of some sub-allocator `A_C(d)` or `A_L(d)`, with structural form `[d, 0, s_C, k]` (resp. `[d, 0, s_L, k]`) for some T4-valid document tumbler `d` (i.e., `d ∈ T` with `zeros(d) = 2`) and some `k ≥ 1`. The set of *substrate-emittable addresses* is the union of all such chain elements across all T4-valid document tumblers — including those not yet registered, since future K.σ transitions can activate their chains — and both subspaces, defined formally as:
```
F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: zeros(d) = 2 ∧ d satisfies T4 ∧ a = [d, 0, s, k])}
```
Every `a ∈ F` has `#a = #d + 3`, `zeros(a) = 3`, and `#E(a) = 2` by direct inspection of the structural form. Moreover, every `a ∈ F` satisfies T4 (HierarchicalParsing, ASN-0034). An address of the form `[d, 0, s, k]` with `d` T4-valid, `zeros(d) = 2`, `s ∈ {s_C, s_L}`, and `k ≥ 1` is exactly the structural form FirstEmission and ChainDiscipline (ASN-0093) fix for a chain element of the sub-allocator `A_C(d)` (resp. `A_L(d)`), so its T4-validity is delivered directly by ChainElementT4Validity (ASN-0093). An address outside `F` cannot be the target of any K.α/K.λ emission. In particular, the sub-allocator anchors `b_C(d) = [d, 0, s_C]` and `b_L(d) = [d, 0, s_L]` of ASN-0093 have `#E = 1` and so lie outside `F`; they are anchors of chains, not chain elements.

Conversely, every allocated address belongs to `F`:

**LP-Sub — SubstrateContainment**: At every reachable state `Σ`, `dom(Σ.C) ∪ dom(Σ.L) ⊆ F`. Every `a ∈ dom(Σ.C) ∪ dom(Σ.L)` inhabits a sub-allocator chain `A_C(d)` or `A_L(d)` of its origin `d = origin(a)` (ChainMembershipForOrigin, ASN-0093), whose elements FirstEmission and ChainDiscipline (ASN-0093) fix in the structural form `[d, 0, s, k]` with `s ∈ {s_C, s_L}` and `k ≥ 1`; the origin `d` is a T4-valid document tumbler with `zeros(d) = 2` (M0, ASN-0093). These are exactly `F`'s membership conjuncts, so `a ∈ F`.

**LP-Fin — IntervalFinitude for Canonical Spans**: For every canonical span `(s, ℓ)` — `ℓ = δ(n, #s)` for some `n ≥ 1` (the displacement-shape condition shared with the tight definition below) — whose start lies in `F` — `s ∈ F`, so `s = [d_0, 0, s', k_s]` for some T4-valid `d_0` with `zeros(d_0) = 2`, subspace `s' ∈ {s_C, s_L}`, chain index `k_s ≥ 1` — the set `F ∩ [s, s ⊕ ℓ)` is finite.

Compute `s ⊕ ℓ` first. By OrdinalDisplacement (ASN-0034), `actionPoint(ℓ) = #s = #d_0 + 3`. By TumblerAdd's piecewise rule (ASN-0034), positions `1..#s - 1` of `s ⊕ ℓ` are prefix-copied from `s` and position `#s` becomes `s_{#s} + ℓ_{#s} = k_s + n`. Hence `s ⊕ ℓ = [d_0, 0, s', k_s + n]` with `#(s ⊕ ℓ) = #s = #d_0 + 3`.

Let `a = [d, 0, s'', k] ∈ F ∩ [s, s ⊕ ℓ)`; then `#a = #d + 3`. We first establish a *prefix-agreement claim*, then use it both to bound `#d` and to pin `d` down.

*Prefix-agreement claim: `d` agrees with `d_0` on every position `1 ≤ j ≤ min(#d, #d_0)`.* Suppose not, and let `j` be the first position `≤ min(#d, #d_0)` at which `d` disagrees with `d_0`. Positions `1..j − 1` of `a` (which are `d_1..d_{j-1}`) equal positions `1..j − 1` of both `s` and `s ⊕ ℓ`: they equal `d_{0,1}..d_{0,j-1}` by `s`'s structural form, and the agreement transfers to `s ⊕ ℓ` through TumblerAdd's prefix-copy region, since `j − 1 < j ≤ #d_0 < #s = actionPoint(ℓ)`. At position `j`, `a_j = d_j`, while `s_j = d_{0,j}` (structural form) and `(s ⊕ ℓ)_j = s_j = d_{0,j}` (prefix-copy, as `j ≤ #d_0 < #s`); the disagreement gives `a_j = d_j ≠ d_{0,j} = s_j = (s ⊕ ℓ)_j`. By T1 case (i) at position `j`, either `d_j < d_{0,j}` (yielding `a < s`, contradicting `a ≥ s`) or `d_j > d_{0,j}` (yielding `a > s ⊕ ℓ`, contradicting `a < s ⊕ ℓ`). Contradiction either way, establishing the claim.

*Bound `#d ≤ #d_0`.* Suppose `#d > #d_0`. Then `min(#d, #d_0) = #d_0`, so the prefix-agreement claim gives `d_0 ≼ d`. Position `#d_0 + 1` of `a` is `d_{#d_0 + 1}` — well-defined since `#d > #d_0`. The constraint `zeros(d) = 2 = zeros(d_0)` combined with `d_0 ≼ d` forces every position of `d` strictly beyond `#d_0` to be non-zero: `d_0` already contributes both of `d`'s permitted zeros at positions `≤ #d_0`. By T0's carrier ℕ, `d_{#d_0 + 1} ≥ 1`. Position `#d_0 + 1` of `s ⊕ ℓ` is `0` — the separator in `s`'s structural form, preserved by TumblerAdd's prefix-copy region since `#d_0 + 1 < #s = actionPoint(ℓ)`. So `a_{#d_0 + 1} ≥ 1 > 0 = (s ⊕ ℓ)_{#d_0 + 1}` with agreement on positions `1..#d_0`, and by T1 case (i) at position `#d_0 + 1`, `a > s ⊕ ℓ` — contradicting `a < s ⊕ ℓ`. Hence `#d ≤ #d_0`.

*`d` is the length-`#d` prefix of `d_0`.* With `#d ≤ #d_0` in hand, `min(#d, #d_0) = #d`, so the prefix-agreement claim gives that `d` agrees with `d_0` on positions `1..#d`: `d` is the length-`#d` prefix of `d_0`, uniquely determined by `#d`.

Admissibility further requires `d` to be T4-valid with `zeros(d) = 2`. By F's structural definition (the conjunct `zeros(d) = 2 ∧ d satisfies T4` in F's set-builder formula above) applied to the canonical-span hypothesis `s ∈ F`, `d_0` is T4-valid with `zeros(d_0) = 2`; let `z_1 < z_2 ≤ #d_0` denote `d_0`'s two zero positions. For `d` (a prefix of `d_0`) to satisfy `zeros(d) = 2`, both zero positions must lie within `d`'s index range, so `#d ≥ z_2`. T4's endpoint clause `d_{#d} ≠ 0` excludes `#d = z_2` (since `d_{z_2} = d_{0, z_2} = 0`), forcing `#d > z_2`. Combined with `#d ≤ #d_0`, the admissible range is `#d ∈ {z_2 + 1, …, #d_0}`.

We split this range into two sub-cases.

*Sub-case A — `z_2 < #d < #d_0` contributes zero candidates.* Suppose `z_2 < #d < #d_0`. Position `#d + 1` of `d_0` is a non-zero component: the only zeros of `d_0` lie at `z_1, z_2 ≤ z_2`, and `#d + 1 ≥ z_2 + 2 > z_2`, so `d_0[#d + 1] ≠ 0`, hence `d_0[#d + 1] ≥ 1` by T0's carrier ℕ. The candidate `a = [d, 0, s'', k] ∈ F` has `a_{#d + 1} = 0` (the separator zero introduced by the structural form). Position `#d + 1 ≤ #d_0` lies within `d_0`'s prefix in `s = [d_0, 0, s', k_s]` (writing `s' = X ∈ {s_C, s_L}` for the span's subspace), giving `s_{#d + 1} = d_0[#d + 1] ≥ 1`. Position `#d + 1` of `s ⊕ ℓ` agrees with `s` by prefix-copy: the canonical assumption `ℓ = δ(n, #s)` gives `actionPoint(ℓ) = #s = #d_0 + 3` (OrdinalDisplacement, ASN-0034), and `#d + 1 ≤ #d_0 < #s` places this position in TumblerAdd's prefix-copy region, so `(s ⊕ ℓ)_{#d + 1} = s_{#d + 1} ≥ 1`. With prior-position agreement on `1..#d` (since `d` is the length-#d prefix of `d_0`), T1 case (i) at divergence position `#d + 1` yields `a < s` from `a_{#d + 1} = 0 < s_{#d + 1}` — contradicting `a ≥ s`. The sub-case admits no candidates.

*Sub-case B — `#d = #d_0` contributes exactly `n` candidates.* Suppose `#d = #d_0`. Then `d = d_0`, and the candidate has form `a = [d_0, 0, s'', k]` with `#a = #d_0 + 3 = #s`. Compare `a` with `s = [d_0, 0, X, k_s]` and `s ⊕ ℓ`:

- Positions `1..#d_0 + 1`: all three coincide. `a` and `s` carry `d_0` on positions `1..#d_0` and zero at position `#d_0 + 1` (the separator in both structural forms); `s ⊕ ℓ` agrees with `s` by prefix-copy on positions `1..#s − 1`, and `#d_0 + 1 < #s`.
- Position `#d_0 + 2`: `a` has `s''`, `s` has `X`, `s ⊕ ℓ` has `X` (prefix-copy, `#d_0 + 2 < #s`).
- Position `#s = #d_0 + 3`: `a` has `k`, `s` has `k_s`, `s ⊕ ℓ` has `k_s + n` (TumblerAdd at the action point: `s_{#s} + ℓ_{#s} = k_s + n`).

*Subspace component (position `#d_0 + 2`).* If `s'' ≠ X`, T1 case (i) at position `#d_0 + 2` with prior-position agreement decides the order. By SubspaceConventionAxiom (ASN-0093), `s_C = 1 < 2 = s_L`. If `s'' < X`, then `a < s` (contradicting `a ≥ s`); if `s'' > X`, then `a > s ⊕ ℓ` (contradicting `a < s ⊕ ℓ`). Either branch excludes the candidate, forcing `s'' = X` for any admissible candidate.

*Chain index (position `#s`).* With `s'' = X`, the comparison reduces to position `#s`, where `a_{#s} = k`, `s_{#s} = k_s`, and `(s ⊕ ℓ)_{#s} = k_s + n`. The equivalence `a ∈ [s, s ⊕ ℓ) ⟺ k_s ≤ k < k_s + n` splits into four sub-cases on the relation between `k` and `k_s`, exhausting `k ≥ 1`. (a) *Equality at the lower bound* — `k = k_s`: then `a` agrees with `s` at every position of the common length `#s`, so by T3 (CanonicalRepresentation, ASN-0034) `a = s`, and `a ∈ [s, s ⊕ ℓ)` by T12 (the half-open interval contains its left endpoint, established via TA-strict on `s ⊕ ℓ > s`). (b) *Interior* — `k_s < k < k_s + n`: prior-position agreement and `a_{#s} = k > k_s = s_{#s}` give `a > s` by T1 case (i); prior-position agreement and `a_{#s} = k < k_s + n = (s ⊕ ℓ)_{#s}` give `a < s ⊕ ℓ` by T1 case (i); together `a ∈ [s, s ⊕ ℓ)`. (c) *Above the upper bound* — `k ≥ k_s + n`: prior-position agreement and `a_{#s} = k ≥ k_s + n = (s ⊕ ℓ)_{#s}` give `a ≥ s ⊕ ℓ` (strict when `k > k_s + n` by T1 case (i); equality when `k = k_s + n` by T3), so `a ∉ [s, s ⊕ ℓ)`. (d) *Below the lower bound* — `k < k_s`: prior-position agreement and `a_{#s} = k < k_s = s_{#s}` give `a < s` by T1 case (i), so `a ∉ [s, s ⊕ ℓ)`. The four sub-cases combine to the stated equivalence, and exactly `n` integer values of `k` (namely `k_s, k_s + 1, …, k_s + n − 1`) satisfy `k_s ≤ k < k_s + n`.

*Total.* Sub-case A contributes `0` candidates at each admissible `#d` in the open range `(z_2, #d_0)`; sub-case B contributes exactly `n` candidates at `#d = #d_0`. Summing across the admissible range:
```
|F ∩ [s, s ⊕ ℓ)| = 0 + ⋯ + 0 + n = n
```
which is finite. (When `#d_0 = z_2 + 1`, sub-case A's range is empty and the sum reduces directly to `n`.)

**LP-Fin Corollary — CanonicalIntervalCharacterisation.** For canonical span `(s, ℓ)` with `s = [d_0, 0, X, k_s]` (where `X ∈ {s_C, s_L}`) and `ℓ = δ(n, #s)`:
```
F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}
```
Every `t ∈ F ∩ [s, s ⊕ ℓ)` satisfies `subspace_I(t) = X` and `origin(t) = d_0`. The interval contains no F-candidates from any chain other than `A_X(d_0)`: cross-document chains are excluded by the proof's `#d ≤ #d_0` bound (sub-cases (i) and (ii) of the bound argument) together with sub-case A's separator argument at lengths `z_2 < #d < #d_0`; the same-document cross-subspace chain `A_Y(d_0)` with `Y ≠ X` is excluded by sub-case B's subspace-component step (which forces `s'' = X`).

**LP12b — ContentCanonicalLinkSubspaceWPFalse.** This treats the K.μ⁻ boundary case in which a transition on document `d` uses retention parameters `n'_{s_C} = 0` and `n'_{s_L} > 0` — the content subspace is emptied while link-subspace V-positions are retained, so the retention set is `R = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n'_{s_L}} ⊆ V_{s_L}(d)`. We show LP12a's wp evaluates to false on this pattern for any link whose endsets are canonically constructed in the content subspace. Let `a ∈ dom(Σ.L)` be a link such that every span `(s, ℓ) ∈ Σ.L(a).eᵢ` (for every slot `i`) is canonical (`ℓ = δ(n, #s)` for some `n ≥ 1`) with `s = [d_s, 0, s_C, k_s]` for some T4-valid document `d_s` and chain index `k_s ≥ 1`. We show `project(a, i, d, Σ) ⊆ V_{s_C}(d)`, from which `project(a, i, d, Σ) ∩ R ⊆ V_{s_C}(d) ∩ V_{s_L}(d) = ∅` follows, and the wp evaluates to false.

The argument turns on the absence of link addresses from coverage: `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅`. We derive `dom(Σ.L) ⊆ F` via an explicit three-step citation chain. First, by ChainMembershipForOrigin (ASN-0093), every `ℓ' ∈ dom(Σ.L)` is a chain element of the link sub-allocator `A_L(d')` where `d' = origin(ℓ')` — link-store membership is *populated* from sub-allocator chains, not from arbitrary tumblers. Second, by FirstEmission and ChainDiscipline (ASN-0093), every chain element of `A_L(d')` has structural form `[d', 0, s_L, k']` for some `k' ≥ 1`: FirstEmission fixes the chain's first element at `[d', 0, s_L, 1]`, and ChainDiscipline supplies the recurrence `t_{n+1} = inc(t_n, 0)`, which by TA5(c) of ASN-0034 advances only the final component, preserving the prefix `[d', 0, s_L, ·]` across all subsequent elements. Third, the document parameter `d'` is T4-valid with `zeros(d') = 2`: ChainMembershipForOrigin (ASN-0093) ties `ℓ'` to the chain of `d' = origin(ℓ')`, L1a (ASN-0093) gives `origin(ℓ') ∈ dom(Σ.M)`, and M0 (ASN-0093) makes every allocated document tumbler T4-valid with two zeros. Substituting into `F`'s set-builder (with `d = d'`, `s = s_L`, `k = k'`), every `ℓ' ∈ dom(Σ.L)` satisfies the membership condition of `F`, so `dom(Σ.L) ⊆ F`. (StoreT4Validity additionally supplies that each `ℓ' ∈ dom(Σ.L)` is T4-valid, which is consistent with — but not required for — the chain-derived structural form to inhabit `F`.) For a single span `(s, ℓ) ∈ Σ.L(a).eᵢ` with `s = [d_s, 0, s_C, k_s]` and `ℓ = δ(n, #s)`, the coverage is the interval `[s, s ⊕ ℓ)`; rewriting via `dom(Σ.L) ⊆ F`:
```
[s, s ⊕ ℓ) ∩ dom(Σ.L) = F ∩ [s, s ⊕ ℓ) ∩ dom(Σ.L)
```
LP-Fin Corollary applied at `X = s_C` gives `F ∩ [s, s ⊕ ℓ) = {[d_s, 0, s_C, k] : k_s ≤ k < k_s + n}` — every F-candidate in the interval has subspace identifier `s_C`. By L0 (ASN-0093), every element of `dom(Σ.L)` has subspace identifier `s_L`; by SubspaceConventionAxiom (`s_C ≠ s_L`), no address with subspace identifier `s_C` can inhabit `dom(Σ.L)`. Hence `F ∩ [s, s ⊕ ℓ) ∩ dom(Σ.L) = ∅`, and so `[s, s ⊕ ℓ) ∩ dom(Σ.L) = ∅` per span. Taking the union over the spans of the endset, `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅`.

Now constrain the projection by subspace. Suppose `v ∈ project(a, i, d, Σ)` with `subspace(v) = s_L`. By S3★ (ASN-0047), `Σ.M(d)(v) ∈ dom(Σ.L)`; by the projection definition, `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`. Hence `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅` — contradiction. So no link-subspace V-position lies in the projection, and `project(a, i, d, Σ) ⊆ V_{s_C}(d)`. The wp then yields `project(a, i, d, Σ) ∩ R ⊆ V_{s_C}(d) ∩ V_{s_L}(d) = ∅` (the two subspace V-position sets are disjoint by S3★-aux and SC-NEQ: every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}` by S3★-aux, but no `v` can carry both identifiers). Existentially over slots, `(E i : project(a, i, d, Σ) ∩ R ≠ ∅)` is false — discharging LP12a's wp on this retention pattern for the canonical-content-subspace class of links.

The case exhibits the wp's *per-subspace sensitivity*: the retention set's subspace partition — not merely its total cardinality — determines whether the wp is satisfiable for a given link.

The achievability arguments below proceed under the canonical assumption — every span exhibited has `ℓ = δ(n, #s)` — and exhaust `F ∩ [s, s ⊕ ℓ)` by structural partition. The count within each structural case is finite by LP-Fin (in its canonical form), and the case analysis is decidable from `s`, `ℓ`, and the structural form of `F`-candidates without enumerating `F`.

An endset `e` is *tight at state `Σ_e`* iff every span `(s, ℓ) ∈ e` is *canonical* — `ℓ = δ(n, #s)` for some `n ≥ 1`, equivalently `#ℓ = #s` with `ℓ` an ordinal displacement (OrdinalDisplacement, ASN-0034) — and satisfies:
```
s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)  ∧  (A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))
```

The first conjunct says the span starts at an allocated address; the second says every substrate-emittable address in the span's reach is already allocated. The canonical-span requirement is *definitional*: a non-canonical span is fixed at false before any quantifier evaluation, so no state can render it tight. The first conjunct gives `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`, whence `s ∈ F` by LP-Sub; together with the canonical shape `ℓ = δ(n, #s)` this discharges LP-Fin's hypotheses, so LP-Fin confines the universal quantifier to the finite set `F ∩ [s, s ⊕ ℓ)` and the predicate is decidable at every state. Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state.

*Achievability.* The non-empty case is reached by the canonical construction. Span endpoints are drawn from currently-allocated content, and the displacement is the canonical ordinal displacement `ℓ = δ(n, #s)`; by OrdinalDisplacement's postcondition, `actionPoint(ℓ) = #s`. The reach is set at or before the relevant chain's next emission point. By LP-Fin (in its canonical form), only finitely many `F`-candidates can interfere with any such span; LP-Fin Corollary identifies exactly which.

Cross-chain interference is excluded by LP-Fin Corollary, which already establishes `F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}` — every F-candidate in a canonical span's reach shares the span's subspace identifier `X` and origin `d_0`, so no chain other than `A_X(d_0)` (whether same-document cross-subspace or cross-document) contributes a candidate. What remains, and is not implied by the corollary, is tightness against `A_X(d_0)`'s own *future* emissions: the corollary characterises interval membership but does not say which of those chain indices are allocated at `Σ_e`. The emission-frontier choice below supplies that.

Choose `ℓ = δ(n, #s)` with `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` where `X ∈ {C, L}` is the span's subspace and `m` is `A_X(d_0)`'s currently-allocated chain-index maximum at `Σ_e`. The constraint `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` ensures every F-candidate from `A_X(d_0)` in `[s, s ⊕ ℓ)` is at chain index `≤ m`, hence already emitted at `Σ_e` — discharging tightness against this chain at `Σ_e`. Tightness is a state-relative predicate evaluated at `Σ_e`; what it requires here is that every F-candidate from `A_X(d_0)` lying in `[s, s ⊕ ℓ)` is already in `dom(Σ_e.C) ∪ dom(Σ_e.L)`, and the constraint just stated discharges exactly that obligation.

*Worked numerical example.* Let `d` be a T4-valid document with `s_C = 1`, and write `m = #d + 3` for the common length of `A_C(d)`'s chain-element addresses (so for every span `s = [d.0.1.k_s]` rooted on this chain, `#s = m`). Suppose `A_C(d)` has emitted three chain elements at the current state `Σ_e`:
```
t_1^C(d) = [d.0.1.1],  t_2^C(d) = [d.0.1.2],  t_3^C(d) = [d.0.1.3]   — all in dom(Σ_e.C)
```
All three have length `m`. The next chain element (not yet emitted) is `t_4^C(d) = [d.0.1.4]`; subsequent elements are `t_5^C(d) = [d.0.1.5]`, and so on.

*Tight example.* Construct the endset `e = {(s, ℓ)}` with `s = [d.0.1.1]` and `ℓ = δ(3, m) = [0, 0, …, 0, 3]` of length `m` — a length-`m` ordinal displacement (OrdinalDisplacement, ASN-0034) that is zero everywhere except at the final position, which holds 3. Its action point is `m`, so `actionPoint(ℓ) = m = #s`, and by TA0 (ASN-0034) `s ⊕ ℓ ∈ T` with `#(s ⊕ ℓ) = m`; TumblerAdd's prefix-copy region preserves positions `1..m-1` of `s`, and position `m` is summed to `s_m + ℓ_m = 1 + 3 = 4`. Hence `s ⊕ ℓ = [d.0.1.4]`, and `coverage(e) = {t ∈ T : [d.0.1.1] ≤ t < [d.0.1.4]}`. The substrate-emittable addresses in `[s, s ⊕ ℓ)` are exactly `t_1^C(d), t_2^C(d), t_3^C(d)` (chain elements of `A_C(d)` with index in `{1, 2, 3}`; index `≥ 4` is excluded by the half-open upper bound `< [d.0.1.4]`, and cross-document chain elements are excluded by the cross-chain interference arguments above). All three are in `dom(Σ_e.C)`, so the tightness condition holds: `e` is tight at `Σ_e`. Now suppose a K.α transition fires next on `A_C(d)`, producing `a_new = t_4^C(d) = [d.0.1.4]`. By half-open semantics, `a_new = s ⊕ ℓ ∉ [s, s ⊕ ℓ) = coverage(e)` — LP19a holds, and any subsequent K.μ⁺ mapping a V-position to `a_new` does not extend the projection of `e` (LP19).

*Non-tight contrast.* Construct instead `e' = {(s, ℓ')}` with the same `s = [d.0.1.1]` but `ℓ' = δ(4, m) = [0, 0, …, 0, 4]` of length `m`. Then `s ⊕ ℓ' = [d.0.1.5]` (same prefix-copy reasoning, with the final summed component now `1 + 4 = 5`), and `coverage(e') = {t ∈ T : [d.0.1.1] ≤ t < [d.0.1.5]}`. The substrate-emittable addresses in this interval are `t_1^C(d), t_2^C(d), t_3^C(d), t_4^C(d)`. At `Σ_e`, `t_4^C(d) ∈ F` but `t_4^C(d) ∉ dom(Σ_e.C)` — so the tightness condition's second conjunct fails on the witness `t_4^C(d) ∈ F ∩ [s, s ⊕ ℓ')`. The endset `e'` is *not* tight at `Σ_e`. After K.α fires producing `a_new = t_4^C(d) = [d.0.1.4]`, we have `a_new ∈ [s, s ⊕ ℓ') = coverage(e')`. If a subsequent K.μ⁺ maps a V-position `v_new` to `a_new`, then `v_new` enters `project(e', d, ·)` by LP9 — boundary insertion extends the (non-tight) reach. The single integer-component difference between `ℓ = δ(3, m)` and `ℓ' = δ(4, m)` is the entire difference between tight construction and a span whose reach extends past the current emission frontier; the architecture admits both, but only the first is immune to absorbing fresh allocations.

We separate two claims: first, that fresh allocations cannot enter a tight endset's coverage; second, that the consequent K.μ⁺/K.μ⁺_L step cannot grow the projection by the resulting V-position.

**LP19a — TightFreshness**: For any endset `e` tight at `Σ_e`, any reachable state sequence `Σ_e →* Σ`, and any K.α (or K.λ) transition `Σ → Σ'` allocating a fresh address `a_new`:
```
a_new ∉ coverage(e)
```

The K.α step emits `a_new` from sub-allocator `A_C(d_alloc)` for some `d_alloc ∈ dom(Σ.M)`; symmetrically K.λ emits from `A_L(d_alloc)`. By the chain structure of ASN-0093, `a_new` is a chain element of `A_C(d_alloc)` (resp. `A_L(d_alloc)`), so `a_new ∈ F`. K.α's precondition (ASN-0093) requires `a_new ∉ dom(Σ.C) ∪ dom(Σ.L)`; K.λ's precondition requires `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)` — the same freshness condition with operand order swapped. By Store Monotonicity★ applied to `Σ_e →* Σ`, `dom(Σ.C) ⊇ dom(Σ_e.C)` and `dom(Σ.L) ⊇ dom(Σ_e.L)`. So `a_new ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)`.

Suppose for contradiction `a_new ∈ coverage(e)`. Then `a_new ∈ [s, s ⊕ ℓ)` for some span `(s, ℓ) ∈ e`. The tightness condition at `Σ_e`, applied with the substrate-emittable `a_new ∈ F` lying in `[s, s ⊕ ℓ)`, yields `a_new ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)` — contradicting the freshness conclusion. Therefore `a_new ∉ coverage(e)`.

**LP19 — TightEndsetBoundaryExclusion**: Let `e` be an endset tight at `Σ_e`, and let `Σ_e →* Σ_n → Σ_{n+1}` be a reachable transition sequence whose final step is a K.μ⁺ (or K.μ⁺_L) transition operating on document `d`. K.μ⁺ may add multiple V-positions `dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` in a single step, each carrying its own I-address image; LP19's hypothesis selects, *per V-position*, only those whose image was freshly K.α/K.λ-allocated on the prefix. Formally, for every `v_new ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))`, letting `a_new := Σ_{n+1}.M(d)(v_new)`, if `a_new` was freshly allocated by a K.α (or K.λ) step on the prefix `Σ_e →* Σ_n`:
```
v_new ∉ project(e, d, Σ_{n+1})
```

The K.α (or K.λ) step that allocated `a_new` lies on the prefix `Σ_e →* Σ_n`, so LP19a applied at that step yields `a_new ∉ coverage(e)`. Since `coverage(e)` is a deterministic function of `e`'s spans (per the coverage definition of ASN-0043) and `e` is a fixed endset value across the entire sequence — `coverage` consults no state component — the membership `a_new ∉ coverage(e)` carries through unchanged to `Σ_{n+1}`. The K.μ⁺ (or K.μ⁺_L) transition `Σ_n → Σ_{n+1}` adds the mapping at `v_new`, giving `v_new ∈ dom(Σ_{n+1}.M(d))` and `Σ_{n+1}.M(d)(v_new) = a_new ∉ coverage(e)`. The projection definition then excludes `v_new` from `project(e, d, Σ_{n+1})`.

Tightness is a construction discipline, not a structural invariant the system enforces. The system permits endsets whose spans extend past the relevant sub-allocator's current emission frontier; such endsets are not tight, and an `a_new` allocated within their forward extent (a substrate-emittable address inside `[s, s ⊕ ℓ)`) would in fact enter the coverage — LP9's growth behaviour then applies. The architectural significance of LP19 is that the canonical construction — selecting span endpoints among I-addresses resident at construction time, with reach at or before the chain's next emission point — produces tight endsets, and tight endsets are immune to absorbing addresses produced by subsequent K.α or K.λ. Boundary insertion as a composite (K.α + K.μ⁺) cannot enlarge a tight link's reach.

**LP20 — RangeConfinement**: For every endset `e`, document `d`, state `Σ`:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))
```

The equality follows directly from the projection definition. Unfold:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)}
  = {Σ.M(d)(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) ∈ coverage(e)}
  = {a : a ∈ ran(Σ.M(d)) ∧ a ∈ coverage(e)}
  = coverage(e) ∩ ran(Σ.M(d))
```
The first step is the definition of `project`; the second renames `a = Σ.M(d)(v)` and observes that the image set equals `ran(Σ.M(d))` filtered by coverage membership; the third is set intersection.

*Corollary (store-confinement form).* Composing the equality with S3★ (GeneralizedReferentialIntegrity, ASN-0047) yields the weaker inclusion:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))
```

Split by V-position subspace, the corollary refines to:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C} ⊆ coverage(e) ∩ dom(Σ.C)
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L} ⊆ coverage(e) ∩ dom(Σ.L)
```

Furthermore, the two per-subspace inclusions *partition* the projection's full range. By S3★-aux (SubspaceExhaustiveness), every `v ∈ dom(Σ.M(d))` satisfies `subspace(v) ∈ {s_C, s_L}`; restricting to `project(e, d, Σ) ⊆ dom(Σ.M(d))`, the same dichotomy holds. Hence:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C}
                                   ∪ {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L}
```
The union is exhaustive by S3★-aux; the two summands are jointly the full projection range. The two summands are also disjoint — making this a genuine partition rather than a mere exhaustive union — because their containing stores are disjoint: the content-subspace component lies in `dom(Σ.C)`, the link-subspace component in `dom(Σ.L)`, and `dom(Σ.C) ∩ dom(Σ.L) = ∅` (SD, ASN-0093; equivalently L14, ASN-0047). Together with the per-subspace inclusions above, this gives a complete characterisation of `{Σ.M(d)(v) : v ∈ project(e, d, Σ)}` as a partition into a content-subspace component (contained in `coverage(e) ∩ dom(Σ.C)`) and a link-subspace component (contained in `coverage(e) ∩ dom(Σ.L)`), with no other contributions.

The V-positions in the projection always correspond to I-addresses that have been allocated: the projection cannot "see" hypothetical future addresses. The equality is the precise statement of what is reached, and the per-subspace inclusion records what store the reached addresses inhabit.

**LP21 — RepresentationInvariance**: For any two endsets `e₁, e₂` with `coverage(e₁) = coverage(e₂)`:
```
project(e₁, d, Σ) = project(e₂, d, Σ)
```

The projection depends only on coverage, not on the span decomposition of the endset. Two endsets with the same coverage are interchangeable for projection purposes. This is a direct corollary of the definition: the set comprehension references `coverage(e)`, not the spans within `e`.

## A Worked Trace

To make the displacement concrete, we trace a small example. Consider:

- A link `a` with endset `e₁ = {(i₁, δ(5, #i₁))}` — pinning the span's start at `i₀ := i₁` (the first traced chain element) and its width at the canonical ordinal displacement `ℓ := δ(5, #i₁)` (OrdinalDisplacement, ASN-0034) of depth `#i₁` and value 5, so that `i₀ ⊕ ℓ = shift(i₁, 5)`. The span is well-formed by T12 since `Pos(δ(5, #i₁))` holds and `actionPoint(δ(5, #i₁)) = #i₁ ≤ #i₁`. By T12, `coverage(e₁) = {t ∈ T : i₁ ≤ t < shift(i₁, 5)}` — the entire half-open T1-interval, not merely a discrete set. The I-addresses `i₁, i₂, i₃, i₄` are pairwise sibling chain elements of a single content sub-allocator `A_C(d_alloc)` for some `d_alloc ∈ dom(Σ.M)`. All four share the common chain length `#d_alloc + 3`: FirstEmission (ASN-0093) fixes the chain's first element at `[d_alloc, 0, s_C, 1]` with `#E = 2`, hence length `#d_alloc + 3`, and ChainDiscipline (ASN-0093) advances each subsequent element by `inc(·, 0)`, which by TA5(c) of ASN-0034 modifies only the significant position and preserves length. By ChainEnumerationInjectivity (ASN-0093) the enumeration `n ↦ tₙ` is strictly increasing under T1, so distinct chain indices yield distinct addresses ordered consistently with chain-index order. Concretely, the chain is rooted so that `iₖ = shift(i₁, k − 1)` for `k = 1, 2, 3, 4` — each `inc(·, 0)` step advances the final chain component by one (TA5(c) on the trailing nonzero significant position, ASN-0034) — and the same enumeration carries `i₁` to `shift(i₁, 4)` (the would-be fifth chain element, whether or not emitted) at a strictly smaller T1 position than `shift(i₁, 5)`. Hence `i₁ < i₂ < i₃ < i₄ < shift(i₁, 5)` and `i₁, …, i₄ ∈ dom(Σ.C)`; the interval `coverage(e₁)` contains these four addresses (along with any other tumbler lying strictly below `shift(i₁, 5)`).
- A document `d₁` whose content subspace arranges these four I-addresses in order: `Σ.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃, v₄ ↦ i₄}`, with `v_k = [s_C, 1, …, 1, k]` so the sequence `(v₁, v₂, v₃, v₄)` satisfies D-SEQ★ at content-subspace count `n_{s_C} = 4`. By inspection of this arrangement, `ran(Σ.M(d₁)) = {i₁, i₂, i₃, i₄}` — in particular `shift(i₁, 4) ∉ ran(Σ.M(d₁))`, so the would-be fifth chain element (whether or not emitted into `dom(Σ.C)` more broadly) is not arranged in `d₁`. Therefore `coverage(e₁) ∩ ran(Σ.M(d₁)) = {i₁, i₂, i₃, i₄}`, and by LP12 the projection through `d₁` is governed by this intersection, not by the full coverage.

At state `Σ`:
```
project(a, 1, d₁, Σ) = {v₁, v₂, v₃, v₄}
```

Apply K.μ⁻ retaining the first three content-subspace positions (so `n'_{s_C} = 3`), producing state `Σ_1`:
```
Σ_1.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃}
project(a, 1, d₁, Σ_1) = {v₁, v₂, v₃}
```

The projection has shrunk by `{v₄}` (per LP10's exact characterisation), and the retained set `{v₁, v₂, v₃}` is the D-SEQ★-admissible prefix permitted by K.μ⁻. The I-address `i₄` is still in `dom(Σ.C)` by S0, but no longer in `ran(Σ_1.M(d₁))`. The link's coverage is unchanged — still the half-open interval `{t ∈ T : i₁ ≤ t < shift(i₁, 5)}`, of which `{i₁, i₂, i₃, i₄}` remain the traced members.

Now suppose another document `d₂` is registered and transcludes `i₄` via K.σ followed by K.μ⁺ (the accompanying K.ρ step required by ValidComposite★'s J1★ coupling, which records `(i₄, d₂) ∈ R`, is elided from the displayed arrangement since projection does not consult `R`), producing state `Σ_2`:
```
Σ_2.M(d₂) = {w₁ ↦ i₄}
project(a, 1, d₂, Σ_2) = {w₁}
```

The link is now discoverable from both `d₁` (where the projection is `{v₁, v₂, v₃}` reaching `{i₁, i₂, i₃}`) and `d₂` (where the projection is `{w₁}` reaching `{i₄}`). Together the two projections reach the four traced I-addresses `{i₁, i₂, i₃, i₄}` — the entirety of `coverage(e₁)` that bears on these documents' ranges — despite no single document containing all four.

*Branch point — alternative continuation from `Σ_1`.* Returning to `Σ_1`, apply K.μ~ to `d₁` (call the result `Σ_3`).

To exhibit projection motion clearly under K.μ~, consider slot 2 of the link, with endset `e₂ = {(i₁, δ(1, #i₁))}` — a single unit-width span (PrefixSpanCoverage form, ASN-0043) starting at `i₁`, where `δ(1, #i₁) = [0, ..., 0, 1]` of length `#i₁` is the canonical unit-depth ordinal displacement (OrdinalDisplacement, ASN-0034). The span `(i₁, δ(1, #i₁))` is well-formed by T12 since `Pos(δ(1, #i₁))` holds and `actionPoint(δ(1, #i₁)) = #i₁ ≤ #i₁`. By PrefixSpanCoverage (ASN-0043), `coverage(e₂) = {t ∈ T : i₁ ≼ t}`. Since `i₂, i₃, i₄` are sibling chain elements of `i₁` (sharing length `#i₁` but differing at the last component, by ASN-0093's chain enumeration via `inc(·, 0)`), none of them satisfies `i₁ ≼ ·` (a proper-prefix relation between equal-length tumblers would require equality by T3, which is ruled out by the distinct chain indices). Hence `coverage(e₂) ∩ {i₁, i₂, i₃, i₄} = {i₁}`, and so `coverage(e₂) ∩ ran(Σ_1.M(d₁)) = {i₁}` — only the I-address `i₁` from `d₁`'s current range lies in this slot's coverage. The construction is admissible by L4 of ASN-0043, which imposes no constraint on which I-addresses an endset references; we follow only the intersection with `d₁`'s range, since by LP12 that intersection is what governs projection through `d₁`. At `Σ_1`:
```
project(a, 2, d₁, Σ_1) = {v₁}
```
— a strict subset of `dom(Σ_1.M(d₁)) = {v₁, v₂, v₃}`, because among the V-positions of `Σ_1.M(d₁)` only `v₁` maps to an I-address in `coverage(e₂)`.

Now (still in this alternative branch from `Σ_1`) apply K.μ~ to `d₁` via a bijection `π` that permutes the V-positions, fixing `dom(Σ_1.M(d₁))` setwise (per K.μ~-FIX of ASN-0047). The K.μ~ operates on the `Σ_1`-state arrangement directly, so the references to `Σ_1.M(d₁)` on both sides of the bijection equation point to the same source state:
```
π(v₁) = v₃, π(v₂) = v₂, π(v₃) = v₁
Σ_3.M(d₁) = {v₃ ↦ i₁, v₂ ↦ i₂, v₁ ↦ i₃}
project(a, 1, d₁, Σ_3) = {v₃, v₂, v₁} = π(project(a, 1, d₁, Σ_1))
project(a, 2, d₁, Σ_3) = {v₃} = π({v₁}) = π(project(a, 2, d₁, Σ_1))
```

*Admissibility check.* K.μ~'s precondition (ASN-0047) requires that `π` induce a post-state satisfying S8a, S8-depth, D-CTG★, D-MIN★, and S3★, and that `π ≠ id`. With the concrete V-position values `v_k = [s_C, 1, …, 1, k]` already fixed by the D-SEQ★ enumeration above, we verify each conjunct in turn. K.μ~-FIX gives `dom(Σ_3.M(d₁)) = dom(Σ_1.M(d₁)) = {v₁, v₂, v₃}` — the V-position *set* is preserved; only the mapping changes. Therefore `V_{s_C}(Σ_3.M(d₁)) = {v₁, v₂, v₃}` (subspace identifier `s_C` is fixed at each `v_k`'s first component by the explicit form, independent of the mapping), and `V_{s_L}(Σ_3.M(d₁)) = ∅`. *S8a* (zero-count and positivity) and *S8-depth* (common depth) hold of every `v_k = [s_C, 1, …, 1, k]` by direct inspection of the structural form — these are properties of the V-positions themselves, unaffected by reordering. *D-MIN★* requires `min(V_{s_C}(Σ_3.M(d₁))) = [s_C, 1, …, 1]`; the minimum of `{[s_C, 1, …, 1, k] : k ∈ {1, 2, 3}}` under T1 is `[s_C, 1, …, 1, 1] = v₁`, which has the required form. *D-CTG★* and *D-SEQ★* require `V_{s_C}(Σ_3.M(d₁)) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ 3}` — exactly the set we have, since the V-position set is unchanged from `Σ_1`. *S3★* requires that each post-state mapping target the correct subspace: `Σ_3.M(d₁)(v₃) = i₁ ∈ dom(Σ_3.C)` with `subspace(v₃) = s_C` (V-position's first component) matching the content subspace, and similarly for `v₂ ↦ i₂` and `v₁ ↦ i₃` — all three I-addresses are content-subspace by hypothesis, and all three V-positions have `subspace(·) = s_C`. *π ≠ id*: `π(v₁) = v₃ ≠ v₁`. All admissibility conjuncts hold, so `π` is admissible under K.μ~.

The slot-2 projection moves: it was `{v₁}` at `Σ_1`, it is `{v₃}` at `Σ_3`. The I-address `i₁` is now carried at V-position `v₃` rather than `v₁` — the projection followed its content from `v₁` to `π(v₁) = v₃`. The slot-1 projection set looks unchanged ({v₁, v₂, v₃} as a set) only because it happens to coincide with the entire domain; per-V-position, the binding has shifted (v₁ now carries i₃ rather than i₁, etc.).

Per LP11, both projections' V-positions are permuted by `π`, and the set of I-addresses reached is unchanged within each slot. The link "followed its content" through the reordering.

At no point during either branch of this trace did the link itself change. The link's address, endsets, coverage, and slot ordering remained byte-identical from `Σ` through `Σ_2` (the transclusion branch) and from `Σ` through `Σ_3` (the reordering branch). What displaced was the projection, and the displacement was entirely a function of the operations applied to the documents' arrangements.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LP2 | `(A Σ → Σ', a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| : Σ'.L(a).eᵢ = Σ.L(a).eᵢ)` — slot invariance | introduced |
| LP2★ | Multi-step slot invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ` | introduced |
| LP3 | `(A Σ → Σ', a, i : a ∈ dom(Σ.L) : coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))` — coverage invariance | introduced |
| LP3★ | Multi-step coverage invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` | introduced |
| Store Monotonicity★ | `Σ →* Σ' ⟹ dom(Σ.C) ⊆ dom(Σ'.C) ∧ dom(Σ.L) ⊆ dom(Σ'.L)` | introduced |
| project | `project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}` (defined when `d ∈ dom(Σ.M)`) — the live projection function | introduced |
| LP4 | For `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`: `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)` — arrangement specificity (downstream lifts via M1 from `d ∈ dom(Σ.M)`) | introduced |
| LP5 | Cross-document independence: projection through `d` unaffected by edits to `d' ≠ d` (frames over K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) | introduced |
| LP6 | K.α (content allocation) does not displace any projection | introduced |
| LP7 | K.λ (link allocation) does not displace existing projections | introduced |
| LP8 | Document-registration invariance (K.σ of ASN-0093 or K.δ-IsDocument of ASN-0047): (a) `(A d ∈ dom(Σ.M) : project(e, d, Σ') = project(e, d, Σ))`; (b) `project(e, d_new, Σ') = ∅` | introduced |
| LP14 | K.ρ (provenance recording) does not displace any projection | introduced |
| LP9 | K.μ⁺ and K.μ⁺_L can only enlarge projection; new V-positions come from new arrangement entries | introduced |
| LP10 | K.μ⁻ can only shrink projection; lost V-positions come from removed arrangement entries | introduced |
| LP11 | K.μ~ rebinds projection: `project(e, d, Σ') = π(project(e, d, Σ))` via bijection π | introduced |
| discoverable_from | `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)` (defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`) | introduced |
| LP12 | `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` | introduced |
| LP12a | Contraction discoverability wp: `wp(K.μ⁻[d, R], discoverable_from(a, d, ·)) ≡ enabled(K.μ⁻[d, R]) ∧ (E i : project(a, i, d, Σ) ∩ R ≠ ∅)`, where `R` is the K.μ⁻ retention set; reduces to `false` at `R = ∅` | introduced |
| LP12b | Discharges LP12a's content-canonical-link-subspace boundary case: for `a ∈ dom(Σ.L)` whose every span is canonical with `s = [d_s, 0, s_C, k_s]`, and any K.μ⁻ retention parameters `n'_{s_C} = 0, n'_{s_L} > 0`, the wp evaluates to `false` — derived via LP-Fin Corollary applied at `X = s_C` to give `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅`. | introduced |
| LP13 | Unconditional link persistence: `Σ →* Σ' ∧ a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` — independent of any discoverability | introduced |
| LP16 | Transclusion confers discoverability: shared I-addresses transfer discoverability across documents | introduced |
| LP17 | Ghost projection: orphaned links persist in `dom(Σ.L)` with empty projections everywhere | introduced |
| LP18 | Resurrection: re-introducing a coverage I-address via K.μ⁺ or K.μ⁺_L restores discoverability | introduced |
| tight | `tight(e, Σ_e)` ≡ every span `(s, ℓ) ∈ e` is canonical (`ℓ = δ(n, #s)` for some `n ≥ 1`), `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`, and every substrate-emittable address in `[s, s ⊕ ℓ)` is allocated at `Σ_e`. Non-canonical spans are unconditionally non-tight at every state. | introduced |
| LP-Sub | Substrate containment: `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` at every reachable state — every allocated address is a sub-allocator chain element of structural form `[d, 0, s, k]`, hence in `F`. | introduced |
| LP-Fin | Interval finitude (canonical): `(A s, ℓ : s ∈ F ∧ ℓ = δ(n, #s) for some n ≥ 1 : |F ∩ [s, s ⊕ ℓ)| < ∞)` — only finitely many `F`-candidates fall within any canonical span's reach. Covers only the canonical case (the tightness domain, per the tight definition's canonical-form requirement). | introduced |
| LP-Fin Corollary | Canonical interval characterisation: for canonical `(s, ℓ)` with `s = [d_0, 0, X, k_s]` and `ℓ = δ(n, #s)`, `F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}` — every F-candidate in the interval inherits the span's subspace identifier `X` and origin `d_0`. | introduced |
| LP19a | Tight freshness: under tight construction, K.α/K.λ-allocated addresses fall outside `coverage(e)` | introduced |
| LP19 | Tight endset boundary exclusion: K.μ⁺/K.μ⁺_L mapping to such an address cannot grow `project(e, d, ·)` | introduced |
| LP20 | Range confinement: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`; corollary via S3★ gives `⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))`; per-subspace refinement partitions the range into content-subspace and link-subspace components via S3★-aux | introduced |
| LP21 | Representation invariance: equal coverage implies equal projection | introduced |

## Open Questions

What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?

Under what conditions must the projection of an endset through a document be expressible as a finite union of contiguous V-ranges, given that K.μ~ can scatter formerly contiguous projections into arbitrary subsets of the V-domain?

What guarantees must the system provide about the *V-order* of positions within a single projection — does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?

What invariants must the system maintain when a link's endset references the address of another link (rather than content) — under what conditions must the discovery of one link induce the discovery of the other?

Under what conditions must the system commit to producing identical projections for two documents that have undergone "the same" sequence of editing operations, given that arrangement state is per-document and operations are not directly comparable across documents?

What invariants must hold across a fork composite when the source document's link-subspace V-positions are not transcluded into the new document — how does this affect the projection of the source document's home-document-allocated links through the new document?

What must discoverability preservation guarantee for a link-canonical endset (every span resident in the link subspace) under a contraction that empties the content subspace but retains link-subspace positions, given that the content-canonical disjointness argument inverts there (LP-Fin Corollary at the link subspace does not yield disjointness from the link store)?
