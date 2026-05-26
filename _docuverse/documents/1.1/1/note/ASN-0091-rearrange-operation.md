# ASN-0091: REARRANGE Operation
*2026-05-26*

We seek a precise account of rearrangement — the operation by which segments of a document's content stream are reordered without altering the content itself. The naive picture — that moving text "creates new positions" and "destroys old ones" — implies catastrophic consequences: every link attached to the moved content would break, every cross-document transclusion would dangle, and the historical record of what was contained where would dissolve. None of these failures may occur. Our task is to derive precisely why, and to identify what does change and what cannot.

Our starting commitment is the separation of two streams. The content store `Σ.C : T ⇀ Val` is permanent and append-only: once an address `a` enters `dom(Σ.C)`, it remains there bound forever to its initial value (foundation invariant C0/S0). The arrangement `Σ.M(d) : T ⇀ T` for each document `d ∈ dom(Σ.M)` is a partial function from V-positions to I-addresses recording how the document currently presents its contents in linear order. The arrangement is mutable; the content store is not. The link store `Σ.L : T ⇀ EndsetSequence` is also append-only and immutable on existing keys (foundation invariant L12). Rearrangement, by its name, can affect only the arrangement — the entire question is what this restriction lets us prove.

## REARRANGE as Vstream-Only Operation

Let us define the class of transitions REARRANGE belongs to. A transition `Σ → Σ'` is *Vstream-only on `d`* when there exists a bijection
```
π : dom(Σ.M(d)) → dom(Σ.M(d))
```
satisfying
```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```
together with the frame conditions
```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  (A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))                     (RA-frame)
```

The bijection π is the *rearrangement permutation*. The defining equation RA-π says that for every V-position `v` populated in `Σ.M(d)`, the same I-address `Σ.M(d)(v)` lives in `Σ'.M(d)` — but at the V-position `π(v)`. The (V, I) pairs are permuted; no pair is created, destroyed, or modified.

REARRANGE_K (the cut-sequence operation of ASN-0084) realizes this class: ASN-0084's R-PPERM and R-SPERM construct π explicitly for 3-cut pivot and 4-cut swap respectively, and ASN-0084's R-FRAME-P/S discharge RA-frame. The cut sequence further restricts the bijection — π acts as identity on V-positions outside the affected range `[c₀, c_{n−1})` and on V-positions in subspaces other than the cut subspace S — but the abstract claims below are derivable from RA-π and RA-frame alone, independent of how π was generated.

The cut subspace is fixed at S = s_C by ASN-0084's CS3, so REARRANGE_K rearranges the content subspace alone. We will examine the consequences for the link subspace as a separate frame property below.

## What the Content Store Sees: Nothing

The first consequence of RA-frame is immediate. **Content-Store Invariance**:
```
Σ'.C = Σ.C                                                                              (RE-C)
```
No content is allocated, freed, or modified by rearrangement. Every I-address in `dom(Σ.C)` retains its bound value; no new I-address enters `dom(Σ.C)`; the function `Σ.C` is literally unchanged. This is the architectural reason rearrangement cannot disturb content identity: the layer where identity lives is untouched.

The same observation applies symmetrically to the link store via RA-frame. We will exploit this when reasoning about links below.

## Domain Stability and Range Invariance

RA-π's signature `dom(Σ.M(d)) → dom(Σ.M(d))` forces equality of domains across the transition. Every V-position that was populated in d remains populated; every V-position that was unpopulated remains unpopulated.

**Domain Stability**:
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RE-dom)
```

This distinguishes rearrangement from contraction (which removes V-positions) and from extension (which adds them). Rearrangement is the unique transition class that touches the arrangement's *structure* without changing its *support*.

The bijection further makes the range — viewed as a set or as a multiset — a permutation of itself. Compute:
```
ran(Σ'.M(d)) = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))}
             = {Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))}        [π bijects dom onto itself]
             = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}             [RA-π]
             = ran(Σ.M(d))
```

**Range Invariance**:
```
ran(Σ'.M(d)) = ran(Σ.M(d))                                                              (RE-ran)
```

Lifting to multisets: for each I-address `a`, define `μ_a(M) = |{v : v ∈ dom(M) ∧ M(v) = a}|`. By injectivity of π on a finite set (dom(M(d)) is finite by S8-fin):
```
μ_a(Σ'.M(d)) = |{v' : v' ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v') = a}|
             = |{π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|       [substitute v' = π(v)]
             = |{v : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|           [π injective]
             = μ_a(Σ.M(d))
```

**Per-Address Multiplicity Invariance**:
```
(A a ∈ T :: μ_a(Σ'.M(d)) = μ_a(Σ.M(d)))                                                (RE-μ)
```

Together, RE-ran and RE-μ are the formal content of Nelson's "the document afterward contains exactly the same set of content as before — no additions, no losses, no duplications." Range invariance says the set is identical. Multiplicity invariance says each I-address appears the same number of times. The arrangement is a permutation, not a transformation.

## Where Position Lives After Rearrangement

Every (V, I) pair in the pre-state has an image (V, I) pair in the post-state: the pre-state pair `(v, M(d)(v))` corresponds to the post-state pair `(π(v), M(d)(v))`. The I-address is the same; the V-position has moved. This is the precise sense in which "every byte retains its identity": the byte associated with I-address `M(d)(v)` is still in d, now at V-position `π(v)`.

Conversely, for each post-state V-position `v'`, the pre-image `π⁻¹(v')` is the V-position that previously held the I-address now at `v'`. The map π⁻¹ recovers, for each post-state V-position, the V-position it migrated from.

What changed is not which I-addresses are in d, nor which V-positions are populated, but which V-position holds which I-address. The bijection π is the entire content of the rearrangement.

## Links Persist; Their Coverage Cannot Move

The link store is fixed by RA-frame:
```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))                          (RE-L)
```

Every link persists across rearrangement with its full endset sequence intact. No link is added, removed, or modified.

Coverage of an endset is a function of the endset's span representation alone — it consults no state component beyond the endset itself (per the definition in ASN-0098). Since the endset is preserved verbatim, its coverage is preserved:
```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))   (RE-cov)
```

This is the formal precipitate of Nelson's "links between bytes can survive rearrangements." A link's reference structure is keyed to I-addresses (via spans on the I-address space). The I-addresses are unchanged. So the reference structure is unchanged.

## Discoverability Is Preserved

A link is *discoverable from* document `d` at state `Σ` when some endset's coverage intersects the document's I-address range — when there exists a slot `i` with `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` (the characterisation supplied by foundation lemma LP12 of ASN-0098). Combining RE-cov and RE-ran:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

**Discoverability Invariance**:
```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))    (RE-disc)
```

The set of links that can be found from d is exactly the same before and after rearrangement. This is the strong sense of link survivability: not merely that links persist as objects, but that their *relationships* to documents — the answer to "is this link reachable from here?" — are unchanged.

## Projection Transports Along π

Where a link's coverage strikes the arrangement is the set `project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`. The bijection π carries this set faithfully to the post-state. For each `v ∈ project(e, d, Σ)`, the V-position `π(v)` holds the same I-address (RA-π), and that address remains in coverage (RE-cov), so `π(v) ∈ project(e, d, Σ')`. The reverse inclusion holds by π⁻¹, which exists because π is a bijection on a finite set. Therefore
```
project(e, d, Σ') = π(project(e, d, Σ))                                                 (RE-proj)
```

A reader who follows the link arrives at the same I-address it always identified — but its V-position in d's current arrangement may have changed. This is Nelson's "arrive at the same content, regardless of its new position": the link follows content identity, not arrangement.

## Run Decomposition Is Not Invariant

Up to now every property has been preserved. The bijection's effect lies elsewhere: the *structure* of the (V, I) mapping — the way contiguous V-intervals correspond to contiguous I-intervals — can change.

A maximal run in `M(d)` is a triple `(v, a, n)` with `M(d)(v + k) = a + k` for `0 ≤ k < n`, maximal in the sense that it cannot be extended at either end. The canonical maximal-run decomposition is unique (per the foundation's bundle algebra in ASN-0058). Its cardinality measures how "structured" the arrangement is — fewer runs means longer contiguous mappings.

Rearrangement can fragment runs. Take a maximal run `(v, a, n)` with `n ≥ 2` in `Σ.M(d)`, and suppose π displaces position `v` to a location not adjacent to π(v + 1). Then the post-state arrangement no longer has a contiguous V-interval mapping to the I-interval `[a, a + n)`. The single pre-state run resolves into multiple post-state runs.

> **Fragmentation Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`. (RE-frag)

A direct witness: a 3-cut pivot on a single maximal run of length `n ≥ 3`, with cuts placed at the run's first V-position, one position later, and just past the run's end, displaces the first I-address to the far end of the affected range. The single pre-state run becomes two post-state runs — a long run of `n − 1` consecutive (V, I) pairs and a singleton at the displaced position. The maximal-run-decomposition cardinality increases by one.

A consequence for endset projection: if a pre-state contiguous V-interval `[v, v + n)` is in `project(e, d, Σ)`, the post-state image `π([v, v + n))` may consist of multiple disjoint V-intervals. The set is preserved (RE-proj), but its geometry — its decomposition into contiguous V-runs — is not. This is the formal account of Nelson's "the endset becomes a discontiguous set of bytes" when a linked span is split.

The reverse direction can also occur: rearrangement can bring previously separated V-runs into adjacency, reducing the decomposition's cardinality. Run-decomposition cardinality is neither monotone nor invariant under rearrangement — it tracks the *visible structure* of the arrangement, which is exactly what rearrangement reshapes.

## Cross-Document Independence

Among d's siblings, nothing happens. RA-frame guarantees `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d`:
```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))                                       (RE-other)
```

This is the formal precipitate of Nelson's "REARRANGE is document-scoped — the cuts are V-addresses within the target document." Rearrangement cannot move content between documents, cannot deplete or extend any other document's arrangement, and cannot affect any projection evaluated against any other document. The operation's scope is fully named by the document parameter `d`.

## Cross-Document Transclusion Preserved

When `a ∈ ran(Σ.M(d))` with `origin(a) ≠ d`, the I-address `a` is foreign content displayed in d — a transclusion from d's perspective. The transclusion relationship has three components: (a) `a` is in d's arrangement; (b) `a`'s home document `origin(a)` is present and undisturbed; (c) the origin function — which document allocated `a` — is unchanged.

By RE-ran, the multiset of foreign addresses `{a ∈ ran(Σ.M(d)) : origin(a) ≠ d}` is preserved. By RE-other applied to `d' = origin(a)`, the source arrangement is unchanged. By RE-C, the address `a` remains in `dom(Σ'.C)` with its original value. Origin itself is a function of the address (per S7 of ASN-0036) — not of state — so it is invariant unconditionally.

> **Transclusion Preservation.** For every transclusion relationship at Σ — every pair (a, d) with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d` — the same relationship holds at Σ', with the same multiplicity, and the home document `origin(a)`'s arrangement is unchanged. (RE-trans)

Even when REARRANGE fragments d's view of the transcluded span (RE-frag), each piece independently carries its foreign origin. Splitting at a cut point does not turn one transclusion into two distinct relationships; it produces two contiguous V-intervals that *jointly* refer to the same span at the source. The transcluding document still finds its borrowed content; the home document is undisturbed; and the function answering "where did this byte come from?" is invariant.

## Subspace Frame

ASN-0084's R-FRAME-P/S(a) restricts the cut sequence's effect to the content subspace S = s_C. V-positions in any other subspace are untouched:
```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: Σ'.M(d)(v) = Σ.M(d)(v))                     (RE-sub)
```

When the cut subspace is the content subspace, the link subspace is wholly preserved — both its set of populated V-positions and its V→I mapping. Rearrangement of content does not perturb the link arrangement.

This is structurally necessary. If REARRANGE could carry content-subspace V-positions into link-subspace V-positions or vice versa, the typed referential integrity invariant (foundation S3★: content-subspace V-positions map to `dom(C)`, link-subspace V-positions map to `dom(L)`) would be violable by rearrangement. The subspace restriction is what makes typed referential integrity stable under arrangement permutations.

## Origin and Provenance Invariance

The function `origin(a) = N(a).0.U(a).0.D(a)` (S7 of ASN-0036) projects an I-address to the document-level prefix encoding its allocator. Origin consults only the address `a`. It is a structural projection on T, independent of any state component. Therefore origin is invariant across every state transition, including REARRANGE:
```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)                                           (RE-origin)
```

(More precisely: origin is a function on tumblers, not state, so it has no temporal dimension at all. RE-origin records the fact that REARRANGE consumes no degree of freedom that origin depends on.)

The provenance relation `Σ.R ⊆ T × E_doc` records which documents have, at some point in their history, contained which I-addresses. ASN-0047's J3 (Reordering Isolation) places R in K.μ~'s frame:
```
Σ'.R = Σ.R                                                                              (RE-R)
```

The historical record is intact across rearrangement. The bytes that have ever lived in d are exactly the bytes that live in d after the rearrangement (since REARRANGE adds and removes nothing — RE-ran), and the records of their past containments in other documents are unchanged.

## What Rearrangement Is Not

We collect the negations. Rearrangement does not:

- modify the content store (RE-C);
- modify the link store (RE-L);
- change which V-positions are populated (RE-dom);
- change the multiset of I-addresses in d (RE-ran, RE-μ);
- change link coverage (RE-cov);
- change link discoverability from any document (RE-disc);
- change the set of V-positions where any link projects onto d (RE-proj transports a set along π, preserving its cardinality and content-identity);
- modify any other document's arrangement (RE-other);
- modify V-positions in subspaces other than the cut subspace (RE-sub);
- change origin of any I-address (RE-origin);
- modify the provenance relation (RE-R).

What rearrangement does is exactly one thing: it permutes which V-positions hold which I-addresses, via a bijection π that exhausts d's V-stream domain. Everything else follows — including the cost (run-decomposition cardinality can grow under fragmentation) and the guarantees (link survivability, transclusion preservation, content permanence).

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| RA-π | Rearrangement equation: π : dom(M(d)) → dom(M(d)) is a bijection with M'(d)(π(v)) = M(d)(v) for every v ∈ dom(M(d)) | introduced |
| RA-frame | Rearrangement frame: Σ'.C = Σ.C, Σ'.L = Σ.L, and Σ'.M(d') = Σ.M(d') for every d' ≠ d | introduced |
| RE-C | Content-store invariance: Σ'.C = Σ.C under REARRANGE | introduced |
| RE-dom | Domain stability: dom(Σ'.M(d)) = dom(Σ.M(d)) | introduced |
| RE-ran | Range invariance: ran(Σ'.M(d)) = ran(Σ.M(d)) | introduced |
| RE-μ | Per-address multiplicity invariance: μ_a(Σ'.M(d)) = μ_a(Σ.M(d)) for every I-address a | introduced |
| RE-L | Link store invariance: dom(Σ'.L) = dom(Σ.L) and Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L) | introduced |
| RE-cov | Coverage invariance: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ) for every link a and slot i | introduced |
| RE-disc | Discoverability invariance: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ) for every link a and document d | introduced |
| RE-proj | Projection transport: project(e, d, Σ') = π(project(e, d, Σ)) for every endset e | introduced |
| RE-frag | Fragmentation possibility: there exist REARRANGE instances where the maximal-run-decomposition cardinality of M(d) strictly increases | introduced |
| RE-other | Other-document invariance: Σ'.M(d') = Σ.M(d') for every d' ≠ d | introduced |
| RE-trans | Transclusion preservation: for every (a, d) with a ∈ ran(Σ.M(d)) and origin(a) ≠ d, the transclusion relationship and its multiplicity persist at Σ', and origin(a)'s arrangement is unchanged | introduced |
| RE-sub | Subspace frame: for every v ∈ dom(M(d)) with subspace(v) ≠ S, Σ'.M(d)(v) = Σ.M(d)(v) | introduced |
| RE-origin | Origin invariance: origin(a) is unchanged across REARRANGE for every a | introduced |
| RE-R | Provenance invariance: Σ'.R = Σ.R under REARRANGE | introduced |

## Open Questions

What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?
What semantics, if any, should rearrangement carry on the link subspace, and what invariants would such an operation be required to preserve?
Under what conditions are two distinct rearrangement transitions observationally equivalent at the level of link discoverability rather than at the level of arrangement equality?
What upper bound, if any, can be placed on the increase in maximal-run-decomposition cardinality from a single rearrangement invocation?
Can every bijection of dom(M(d)) that preserves the arrangement well-formedness invariants be realized by a finite composition of cut-sequence rearrangements?
