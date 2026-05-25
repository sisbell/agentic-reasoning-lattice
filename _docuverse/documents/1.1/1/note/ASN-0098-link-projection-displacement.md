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

For each document `d ∈ dom(Σ.M)`, the arrangement `Σ.M(d) : T ⇀ T` is a partial function from V-positions to I-addresses. The arrangement is mutable: the operations K.μ⁺ (extension), K.μ⁻ (contraction), and K.μ~ (reordering) of ASN-0047 modify it. The set of allocated documents `dom(Σ.M)` is non-decreasing (M1 of ASN-0093).

The link store `Σ.L : T ⇀ Link` binds link addresses to link values (ASN-0043). A link value is a sequence of endsets `Σ.L(a) = (e₁, e₂, …, eₙ)` with `N ≥ 3` and a non-empty type endset at slot 3 (L3). Each endset `eᵢ ∈ Endset` is a finite set of well-formed spans. The link store is immutable: by L12, `(A Σ → Σ', a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`.

The two address spaces communicate through the `Σ.M(d)` mappings: V-positions in V-space resolve to I-addresses in I-space. Links inhabit a third role — stored at link-subspace I-addresses but referencing content-subspace I-addresses through their endsets — but for the projection question this role-distinction is immaterial. What matters is that endsets reference I-addresses, and arrangements map V-positions to I-addresses, and the bridge between them is computed live.

## The Coverage of an Endset

For an endset `e ⊆ Span`, the coverage is the set of I-addresses denoted by its spans. From T12 (SpanWellDefinedness, ASN-0034), each span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}`, where `s ⊕ ℓ ∈ T` exists by TA0 because `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are well-formedness conditions of the span. The coverage of the endset is the union:

```
coverage(e) = ⋃ {(s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ}}
```

This is a set of I-addresses in `T`. Some of these I-addresses may be in `dom(Σ.C)` at the time the endset was constructed; some may not. Crucially, coverage is a *purely combinatorial* property of the endset's span representation — it does not consult any state component. Coverage depends on the spans; nothing else.

By L5 (EndsetSetSemantics, ASN-0043), an endset is an unordered set. Two endsets with the same set of spans have the same coverage. The lossy projection `Endset → 2^T` defined by `coverage` is not injective: distinct span decompositions can have identical coverage (for instance, splitting a single span at an interior point produces two spans whose coverage equals the original).

## The Projection Operation

For an endset `e`, a document `d ∈ dom(Σ.M)`, and a state `Σ`, define the *projection of `e` through `d` at `Σ`* as the set of V-positions in `d`'s arrangement whose I-addresses lie within `e`'s coverage:

**project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}**

For a link `a ∈ dom(Σ.L)` with slot `i ∈ {1, …, |Σ.L(a)|}`, write `project(a, i, d, Σ) ≡ project(Σ.L(a).eᵢ, d, Σ)`.

The definition reads from two inputs:
- The endset, fixed once and for all by the link's creation (and immune to subsequent transitions, by L12).
- The arrangement `Σ.M(d)`, mutable and reflecting whatever edits `d` has undergone.

Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still. Therefore every change in projection must be attributable to a change in `Σ.M(d)` — and we can characterise the change by examining what each editing operation does to `Σ.M(d)`.

The definition does not separately consult `Σ.C` or `Σ.L`. Content allocation that does not modify any `Σ.M(d)` cannot affect any projection. Link allocation that does not modify `Σ.M(d)` cannot affect existing projections. Entity registration (K.σ, K.δ) that only updates `dom(Σ.M)` and initialises arrangements to empty cannot retroactively affect existing projections through existing documents. The projection is sensitive only to its two inputs, and only one of them moves.

## Immutability of the Stored Link

Before we can reason about how projection displaces, we must pin down what does *not* move. The link's stored content — its address, its sequence of endsets, the spans within each endset — is structurally immutable.

**LP1 — LinkValuePersistence**: For every state transition `Σ → Σ'`:
```
(A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))
```

This is L12 of ASN-0043, restated. The address persists; the sequence of endsets is preserved verbatim. There is no operation in the transition vocabulary that overwrites a link's value or removes a link from the store.

**LP2 — SlotInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

This follows from LP1 by component projection on the sequence. Equal sequences have equal entries at every position. In particular, the slot-position assignment fixed at link creation — from-set at slot 1, to-set at slot 2, type-set at slot 3, and any additional slots — is structurally preserved. No editing operation can swap, relabel, or alter which slot carries which endset. The directionality of a standard triple (which end is "from", which is "to") is encoded in slot position alone, and slot position is immutable.

**LP3 — CoverageInvariance**: For every transition `Σ → Σ'`, every link `a`, and every slot `i`:
```
coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

This follows from LP2 by applying `coverage` to both sides. The set of I-addresses the link refers to is computed from its endsets; if the endsets are byte-identical between states, the coverage is identical between states. Combining LP1–LP3: the link, the slot, and the I-addresses it reaches are all permanent. What can vary is only which of those I-addresses are currently arranged in any given document.

These three invariants pin down what a link holder owns. Subsequent operations by any party — even the holder, even the original creator — cannot rewrite the endsets. The link is, in this strict sense, a permanent record.

## Frame Conditions: When Projection Does Not Move

A projection moves only if its inputs move. Since the endset (and therefore its coverage) is fixed by LP3, the projection through a document moves only if that document's arrangement is modified — and even then, only if the modification affects V-positions whose I-addresses lie in the endset's coverage.

**LP4 — ArrangementSpecificity**: For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

The proof is immediate from the definition. If both inputs to the comparison agree pointwise (same domain, same mapping), then the set comprehension produces identical results. The projection cannot displace without `Σ.M(d)` displacing.

**LP5 — Cross-Document Independence**: Every operation in the K.μ family (K.μ⁺, K.μ⁻, K.μ~) has frame `(A d' : d' ≠ d : M'(d') = M(d'))` — it modifies at most one document's arrangement per transition. By LP4 applied to each unmodified document:
```
(A d' ∈ dom(Σ.M), d' ≠ d : project(e, d', Σ') = project(e, d', Σ))
```

A link's projection through one document is unaffected by editing operations on a different document. Projections are *per-document* facts. The link itself is a single global object, but the V-positions it reaches in any given document depend only on that document's local state.

**LP6 — Content-Allocation Invariance**: The K.α operation (ASN-0093) modifies only `Σ.C` and has frame `(A d :: M'(d) = M(d))`. By LP4 applied to every `d`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every `d`, whenever `Σ → Σ'` is a K.α transition.

Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them. This is the precise sense in which "insertion at the boundary of a linked passage" cannot extend the link's reach: insertion as a composite (allocate + arrange) splits into a K.α step (no projection effect) and a K.μ⁺ step. The K.μ⁺ step might add a V-position to the projection, but only if the new V-position's I-address is in `coverage(e)`. Since K.α allocates fresh I-addresses outside any existing range — by T10a (AllocatorDiscipline, ASN-0034), each new I-address is structurally distinct from all prior allocations — the new V-position's I-address typically lies outside `coverage(e)`, and the projection does not grow.

The abstract guarantee is sharper than the "outside the strap" metaphor: the projection depends on coverage and arrangement alone, and content allocation alone (K.α) affects neither.

**LP7 — Link-Allocation Invariance**: The K.λ operation modifies only `Σ.L`; its frame is `(A d :: M'(d) = M(d))`. By LP4, K.λ does not displace any existing projection. Creating a new link cannot retroactively affect the projection of any other link.

**LP8 — Entity-Registration Invariance**: K.σ (document registration) extends `dom(Σ.M)` by adding a fresh document `d_new` with `M'(d_new) = ∅` and preserves all existing arrangements. For every endset `e` and every `d ∈ dom(Σ.M)` (the pre-state domain), `project(e, d, Σ') = project(e, d, Σ)` by LP4. The newly created `d_new` has `project(e, d_new, Σ') = ∅` since `dom(Σ'.M(d_new)) = ∅`.

## Operation Effects on Projection

We now examine each operation that *can* displace a projection. The pattern is uniform: each K.μ operation modifies `Σ.M(d)` in a constrained way, and the projection follows mechanically.

**LP9 — Extension under K.μ⁺**: For every K.μ⁺ transition `Σ → Σ'` operating on document `d`, and every endset `e`:
```
project(e, d, Σ) ⊆ project(e, d, Σ')
```

K.μ⁺ extends `Σ.M(d)`: `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))` with agreement on the prior domain (`(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`, by the K.μ⁺ definition). For any `v ∈ project(e, d, Σ)`, we have `v ∈ dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` and `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)`, so `v ∈ project(e, d, Σ')`. The projection can only grow.

The new V-positions that enter the projection are exactly the new arrangement entries whose I-addresses fall in the coverage:
```
project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}
```

When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, those I-addresses lie outside any existing endset's coverage (the typical case), and the projection does not grow. When K.μ⁺ adds entries mapping V-positions to *existing* I-addresses (the transclusion case), the projection grows by precisely those new V-positions whose mappings fall in coverage. This is the mechanism by which a link "comes into view" in a document that newly transcludes its target content.

**LP10 — Contraction under K.μ⁻**: For every K.μ⁻ transition `Σ → Σ'` operating on `d`, and every endset `e`:
```
project(e, d, Σ') ⊆ project(e, d, Σ)
```

K.μ⁻ contracts `Σ.M(d)`: `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` with agreement on the retained domain. For any `v ∈ project(e, d, Σ')`, we have `v ∈ dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, so `v ∈ project(e, d, Σ)`. The projection can only shrink.

The V-positions that leave the projection are exactly the arrangement entries removed by the operation:
```
project(e, d, Σ) ∖ project(e, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

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

So the projection's V-positions move *with* the content they reach: `project(e, d, Σ') = π(project(e, d, Σ))`. The cardinality is preserved: `|project(e, d, Σ')| = |project(e, d, Σ)|`. The set of I-addresses reached by the projection is preserved exactly: `{Σ'.M(d)(v') : v' ∈ project(e, d, Σ')} = {Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`.

The displacement under K.μ~ is therefore a *rebinding*: same I-addresses, same number of V-positions, but at new locations in V-space. A projection that was contiguous in V-order before the reordering may become fragmented after; conversely, a fragmented projection may become contiguous. The shape of the projection is a property of the current arrangement, not of the link.

## Discoverability and Survival

We are now in a position to state Nelson's survivability guarantee precisely. The vague claim "links survive editing if anything is left at each end" becomes a sharp condition on `coverage ∩ ran`.

**Definition — Discoverability**: A link `a ∈ dom(Σ.L)` is *discoverable from document `d`* at state `Σ` iff some slot's projection through `d` is non-empty:
```
discoverable_from(a, d, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)
```

The link is *discoverable* at `Σ` iff there exists some document from which it is discoverable.

**LP12 — DiscoverabilityCharacterisation**: For every link `a ∈ dom(Σ.L)`, document `d ∈ dom(Σ.M)`, and state `Σ`:
```
discoverable_from(a, d, Σ) ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

Direct from definitions. `v ∈ project(a, i, d, Σ)` requires `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, which requires some I-address in the coverage to be in the range. Conversely, any I-address `a*` in `coverage(eᵢ) ∩ ran(Σ.M(d))` is reached by some `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a*`, and that `v` lies in `project(a, i, d, Σ)`.

**LP13 — PartialSurvival**: A link's discoverability from `d` requires only that *some* I-address from *some* endset persist in `d`'s range. The link survives deletion as long as the deletion does not exhaust the coverage-range intersection of every slot.

The standard triple `(F, G, Θ)` gives a sharper reading. The link is *bidirectionally usable* from `d` when both `coverage(F) ∩ ran(Σ.M(d)) ≠ ∅` and `coverage(G) ∩ ran(Σ.M(d)) ≠ ∅` — both ends have at least one surviving I-address arranged in `d`. The link is *unidirectionally usable* when exactly one of these holds. It is *type-only* when only `coverage(Θ) ∩ ran(Σ.M(d)) ≠ ∅`. (We do not interpret the type semantics here; this is the only structural distinction the survival condition can support.) In each case the link still exists in `dom(Σ.L)` by LP1; it is only the *navigational usability from `d`* that varies.

The phrase "anything is left at each end" can now be stated formally: for bidirectional usability of a standard triple from `d`, both source-coverage and target-coverage must non-trivially intersect `d`'s range. For mere existence of the link, nothing is required at all.

## Discovery Independence of Origin

We have characterised discoverability *from* a particular document. Now we ask: how does this relate to which document created the link, which document allocated the linked content, and which document the holder is following the link from?

Three documents may be in play for any given link reference:
- The *home document* of the link, `home(a)` = `origin(a)` — the document under whose tumbler prefix the link's address was allocated (L1a, ASN-0093).
- The *origin document* of each I-address in coverage, `origin(a*)` — the document under whose tumbler prefix `a*` was allocated.
- The *navigating document* `d` from which the holder follows the link.

These three may be the same, all different, or any combination. We claim the discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement.

**LP14 — DiscoveryIndependenceOfHome**: Whether `a` is discoverable from `d` depends only on `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))`. It does not depend on `home(a)`. A link can be discovered from a document that has no relation to where the link itself was allocated.

The justification is that LP12 references only `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))`. Neither quantity references `home(a)`. The home document of the link is a metadata property of the link's address (recoverable by tumbler projection — S7 of ASN-0036), not a constraint on where the link can be reached from.

**LP15 — DiscoveryIndependenceOfOrigin**: Whether `a` is discoverable from `d` depends only on `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))`. It does not depend on the origin documents of the I-addresses in `coverage(Σ.L(a).eᵢ)`. A link can be discovered from a document that has no relation to where the linked content was originally allocated, as long as that document's arrangement currently maps to those I-addresses.

The justification is the same: LP12's characterisation uses set intersection of I-address sets, indifferent to the addresses' allocation provenance.

**LP16 — TransclusionDiscoverability**: If a document `d_new` transcludes content from another document `d_src` (via a fork composite or any K.μ⁺ that adds arrangement entries mapping V-positions to I-addresses already in `dom(Σ.C)`), then every link discoverable from `d_src` via those I-addresses is also discoverable from `d_new` via the corresponding V-positions in `d_new`.

Let `a*` be an I-address with `a* ∈ ran(Σ.M(d_src))` and `a* ∈ ran(Σ.M(d_new))`. For any link `a` and slot `i` with `a* ∈ coverage(Σ.L(a).eᵢ)`, both projections `project(a, i, d_src, Σ)` and `project(a, i, d_new, Σ)` are non-empty — the former by some `v_src` with `Σ.M(d_src)(v_src) = a*`, the latter by some `v_new` with `Σ.M(d_new)(v_new) = a*`. Discoverability extends to every document that transcludes any I-address in coverage. No notification of the link is required; the link is *passively* discoverable from `d_new` simply because `d_new` arranges the I-address.

This is the architectural mechanism behind Nelson's "a link to one version is a link to all versions" claim and the cross-document discovery property: link discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition.

## Ghost Projection and Resurrection

We consider two corner cases: when nothing in the system reaches a link's coverage, and when re-introduction of content restores reachability.

**LP17 — GhostProjection**: Suppose at state `Σ` no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`:
```
(A d ∈ dom(Σ.M), i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)
```

Then by LP12, `project(a, i, d, Σ) = ∅` for every `d, i`. The link is *orphaned*: not discoverable from any document. By LP1, `a` remains in `dom(Σ.L)` and `Σ.L(a)` is unchanged. The link is not destroyed; it is invisible to forward navigation, but its stored endsets continue to identify the I-addresses it once reached, and the I-addresses themselves continue to exist in `dom(Σ.C)` by S0.

**LP18 — Resurrection**: If `a` is orphaned at `Σ` and a subsequent transition sequence `Σ →* Σ'` introduces an arrangement entry `Σ'.M(d)(v) = a*` for some `d, v, a*` with `a* ∈ coverage(Σ.L(a).eᵢ)`, then `a` is discoverable from `d` at `Σ'`.

The transition sequence may include K.σ (registering a new document), K.μ⁺ (extending an existing arrangement, possibly via fork), or any combination. Because LP1 keeps the link's coverage fixed across the entire sequence, the new arrangement entry contributes to the projection through `d` as soon as it appears. By LP9, `v ∈ project(a, i, d, Σ')` since `Σ'.M(d)(v) = a* ∈ coverage(eᵢ)`. The link is resurrected.

This is the formal expression of Nelson's "reaching back through to a superseding version" mechanism. The system architecture admits resurrection because (i) the link's stored state is permanent (LP1), (ii) the I-addresses it references are permanent (S0), (iii) the projection is a live computation that consults the current arrangement at the moment of query, and (iv) discovery is purely I-address-based, indifferent to provenance (LP14, LP15).

A link can pass through arbitrarily many states of orphanage and resurrection without any modification to its stored data. The link does not "know" that the content has been removed and re-introduced; it does not need to.

## Boundary and Width Behaviour

We address two further questions about the structural behaviour of projection under specific operation patterns.

**LP19 — BoundaryInsertionExclusion**: Suppose `Σ → Σ'` is a K.μ⁺ extending `Σ.M(d)` by a single new mapping `(v_new, a_new)` with `a_new` freshly allocated by a preceding K.α (so `a_new ∉ dom(Σ.C)` before the K.α step). Then for any endset `e` whose spans were entirely constructed against I-addresses in `dom(Σ.C)` at the time of `e`'s construction:
```
v_new ∉ project(e, d, Σ') unless a_new ∈ coverage(e) by structural inclusion
```

The qualifier "by structural inclusion" reflects that coverage is defined denotationally on spans: a span `(s, ℓ)` denotes a half-open interval in `T`. A freshly allocated I-address `a_new` falls in this denotation iff `s ≤ a_new < s ⊕ ℓ` as tumblers, regardless of which I-addresses were allocated when the span was constructed. The typical case is that endset spans are constructed tightly against existing content (the endset's spans cover exactly the I-addresses that were `dom(Σ.C)`-resident at construction time), and freshly allocated I-addresses fall outside these tight intervals — so the projection does not grow upon boundary insertion. But the abstract guarantee is purely denotational: the link's coverage is exactly what the spans denote, no more and no less. A user who constructs an endset whose spans deliberately reach past existing content cannot expect future allocations within that range to be excluded.

**LP20 — RangeConfinement**: For every endset `e`, document `d`, state `Σ`:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ dom(Σ.C)
```

The projection only reaches V-positions mapping to allocated content. Addresses in `coverage(e) ∖ dom(Σ.C)` (yet-unallocated I-addresses within the endset's spans) are never in `ran(Σ.M(d))` — by S3 (ReferentialIntegrity), `ran(Σ.M(d)) ⊆ dom(Σ.C)` for content-subspace V-positions, and L14 gives the analogous confinement for link-subspace V-positions to `dom(Σ.L)`. Either way, the V-positions in the projection always correspond to I-addresses that have been allocated. The projection cannot "see" hypothetical future addresses.

**LP21 — RepresentationInvariance**: For any two endsets `e₁, e₂` with `coverage(e₁) = coverage(e₂)`:
```
project(e₁, d, Σ) = project(e₂, d, Σ)
```

The projection depends only on coverage, not on the span decomposition of the endset. Two endsets with the same coverage are interchangeable for projection purposes. This is a direct corollary of the definition: the set comprehension references `coverage(e)`, not the spans within `e`.

## What the Link Holder Can Rely On

We have established a catalogue of guarantees. We now consolidate them into a holder-facing summary.

The holder owns the link `a` and possesses, at minimum, knowledge of its address and the endsets at each slot. Across any state evolution `Σ →* Σ'`:

- The address `a` remains in `dom(Σ'.L)` (LP1).
- The endsets `Σ'.L(a).eᵢ` are byte-identical to `Σ.L(a).eᵢ` for every slot (LP2).
- The slot ordering is preserved — what was at slot 1 is still at slot 1, the type endset is still at slot 3 (LP2).
- The coverage of each endset is fixed — `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (LP3).
- The I-addresses in coverage all remain in `dom(Σ'.C)` if they were ever in `dom(Σ.C)`, with their content values unchanged (S0, S1).

What can vary:

- Which documents the link can be discovered from. This depends on which documents currently arrange any I-address in any endset's coverage (LP12). Documents may transclude the linked content (gaining discoverability — LP9, LP16), or delete it (losing discoverability — LP10), at any time.
- The specific V-positions of any projection. These reflect the document's current arrangement and shift as the document is edited (LP9, LP10, LP11).
- The shape of any projection — contiguous, fragmented, partial — depends on the arrangement, not on the link.

What is *not* possible:

- The link cannot have its endsets rewritten (LP1).
- The link cannot have its slots permuted (LP2).
- The link cannot have its coverage altered by any external party (LP3).
- The link cannot be made un-discoverable while there exists any document arranging any I-address in any of its endsets' coverage (LP12).
- The link cannot be discovered from a document with no arrangement entry mapping to any I-address in coverage (LP12, contrapositive).
- The link's discoverability cannot be made to depend on which document created it or which document allocated its linked content (LP14, LP15).
- Boundary insertion of newly allocated content into a linked passage cannot grow the link's reach (LP19, in the typical case of tightly constructed endsets).

The trust relationship between the link holder and the system is asymmetric. The system commits unconditionally to LP1–LP3 and S0 — to the permanence of every stored object. The system commits conditionally to LP9–LP15 — to the discoverability of the link, contingent on what the document holders choose to do with their arrangements. The holder cannot prevent another document holder from deleting the linked content from their own arrangement (subject to their own ownership rules). The holder can rely on the content persisting somewhere in `dom(Σ.C)` permanently, but cannot rely on it persisting in any particular `ran(Σ.M(d))` indefinitely. Survival of discoverability requires only that *somewhere* in the system, *some* document still arranges *some* of the linked content. This is the strongest guarantee the architecture provides, and it is sufficient for the holder's purpose: the link's content can be re-introduced via transclusion at any time, and the link will then be re-projected at the new V-positions automatically and without any action by the holder.

## A Worked Trace

To make the displacement concrete, we trace a small example. Consider:

- A link `a` with endset `e₁ = {(i₀, ℓ)}` covering I-addresses `{i₁, i₂, i₃, i₄}`, where `i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ` and `i₁, …, i₄ ∈ dom(Σ.C)`.
- A document `d₁` with arrangement `Σ.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃, v₄ ↦ i₄}`.

At state `Σ`:
```
project(a, 1, d₁, Σ) = {v₁, v₂, v₃, v₄}
```

Apply K.μ⁻ removing `v₃` from `d₁`'s arrangement, producing state `Σ_1`:
```
Σ_1.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₄ ↦ i₄}
project(a, 1, d₁, Σ_1) = {v₁, v₂, v₄}
```

The projection has shrunk by `{v₃}` (per LP10's exact characterisation). The I-address `i₃` is still in `dom(Σ.C)` by S0, but no longer in `ran(Σ_1.M(d₁))`. The link's coverage is unchanged — still `{i₁, i₂, i₃, i₄}`.

Now suppose another document `d₂` is registered and transcludes `i₃` via K.σ followed by K.μ⁺, producing state `Σ_2`:
```
Σ_2.M(d₂) = {w₁ ↦ i₃}
project(a, 1, d₂, Σ_2) = {w₁}
```

The link is now discoverable from both `d₁` (where the projection is `{v₁, v₂, v₄}` reaching `{i₁, i₂, i₄}`) and `d₂` (where the projection is `{w₁}` reaching `{i₃}`). Together the two projections reach the full coverage `{i₁, i₂, i₃, i₄}` despite no single document containing all four I-addresses.

Now apply K.μ~ to `d₁` via a bijection `π` that permutes the V-positions:
```
π(v₁) = v₄, π(v₂) = v₂, π(v₄) = v₁
Σ_3.M(d₁) = {v₄ ↦ i₁, v₂ ↦ i₂, v₁ ↦ i₄}
project(a, 1, d₁, Σ_3) = {v₄, v₂, v₁} = π(project(a, 1, d₁, Σ_1))
```

Per LP11, the projection's V-positions are permuted by `π`, but the set of I-addresses reached is unchanged: still `{i₁, i₂, i₄}`. The link "followed its content" through the reordering.

At no point during this trace did the link itself change. The link's address, endsets, coverage, and slot ordering remained byte-identical from `Σ` through `Σ_3`. What displaced was the projection, and the displacement was entirely a function of the operations applied to the documents' arrangements.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LP1 | `(A Σ → Σ', a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` — link value persistence | introduced |
| LP2 | `(A Σ → Σ', a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| : Σ'.L(a).eᵢ = Σ.L(a).eᵢ)` — slot invariance | introduced |
| LP3 | `(A Σ → Σ', a, i : a ∈ dom(Σ.L) : coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))` — coverage invariance | introduced |
| project | `project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}` — the live projection function | introduced |
| LP4 | `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)` — arrangement specificity | introduced |
| LP5 | Cross-document independence: projection through `d` unaffected by edits to `d' ≠ d` | introduced |
| LP6 | K.α (content allocation) does not displace any projection | introduced |
| LP7 | K.λ (link allocation) does not displace existing projections | introduced |
| LP8 | K.σ (document registration) does not displace existing projections | introduced |
| LP9 | K.μ⁺ can only enlarge projection; new V-positions come from new arrangement entries | introduced |
| LP10 | K.μ⁻ can only shrink projection; lost V-positions come from removed arrangement entries | introduced |
| LP11 | K.μ~ rebinds projection: `project(e, d, Σ') = π(project(e, d, Σ))` via bijection π | introduced |
| LP12 | `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` | introduced |
| LP13 | Partial survival: discoverability requires only one I-address per slot to remain in range | introduced |
| LP14 | Discoverability is independent of `home(a)` — where the link was allocated | introduced |
| LP15 | Discoverability is independent of `origin(a*)` — where each coverage I-address was allocated | introduced |
| LP16 | Transclusion confers discoverability: shared I-addresses transfer discoverability across documents | introduced |
| LP17 | Ghost projection: orphaned links persist in `dom(Σ.L)` with empty projections everywhere | introduced |
| LP18 | Resurrection: re-introducing a coverage I-address via K.μ⁺ restores discoverability | introduced |
| LP19 | Boundary-insertion exclusion: freshly allocated I-addresses typically fall outside tight endset coverage | introduced |
| LP20 | Range confinement: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ dom(Σ.C)` | introduced |
| LP21 | Representation invariance: equal coverage implies equal projection | introduced |

## Open Questions

What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?

Under what conditions must the projection of an endset through a document be expressible as a finite union of contiguous V-ranges, given that K.μ~ can scatter formerly contiguous projections into arbitrary subsets of the V-domain?

What guarantees must the system provide about the *V-order* of positions within a single projection — does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?

What invariants must the system maintain when a link's endset references the address of another link (rather than content) — under what conditions must the discovery of one link induce the discovery of the other?

What does the system guarantee about a link whose coverage spans I-addresses partially outside `dom(Σ.C)` at link-creation time — what must remain true if future K.α allocations fall within the previously unallocated portion of the coverage?

Under what conditions must the system commit to producing identical projections for two documents that have undergone "the same" sequence of editing operations, given that arrangement state is per-document and operations are not directly comparable across documents?

What invariants must hold across a fork composite when the source document's link-subspace V-positions are not transcluded into the new document — how does this affect the projection of the source document's home-document-allocated links through the new document?
