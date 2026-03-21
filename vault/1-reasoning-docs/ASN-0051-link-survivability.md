# ASN-0051: Link Survivability

*2026-03-20*

We are looking for the invariants that govern what a link holder can rely on across state changes. A link has been created — its endsets are fixed (L12, LinkImmutability), its address is permanent (T8, AllocationPermanence). The endsets reference I-addresses in the content store, which is itself immutable (S0, ContentImmutability). So the link, structurally, is as permanent as anything in the system.

Yet the question of survivability is not about the link's *structure*. It is about the link's *utility*. A link is useful when its endpoints can be resolved to observable content in some document's current arrangement. Arrangements change — content is inserted, deleted, rearranged. What do these changes do to the link's observable behaviour?

The answer has two parts: a *discovery* question (can the link be found?) and a *resolution* question (can the link's endpoints be followed to visible content?). These are independent questions with independent answers. We develop each in turn.


## Endset Projection

To reason about survivability we need to formalize how a link's endsets relate to a document's current state. The link's endsets are sets of spans over I-addresses (L3, TripleEndsetStructure; L4, EndsetGenerality). A document's arrangement M(d) maps V-positions to I-addresses (ASN-0036). The question "what does this endset look like in document d right now?" has a precise answer.

**Definition — Endset Projection.** For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

This is the set of I-addresses that the endset references and that d currently contains in its arrangement. Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

**Definition — Endset Resolution.** For an endset e and document d, the *resolution* of e in d is:

`resolve(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

These are the V-positions in d whose content is part of the endset. Resolution gives the positions a reader would see; projection gives the underlying content identities.

The two are related by M(d)'s function property (S2, ArrangementFunctionality): v ∈ resolve(e, d) iff M(d)(v) ∈ π(e, d). Since M(d) need not be injective — within-document sharing is permitted (S5, UnrestrictedSharing) — we may have |resolve(e, d)| ≥ |π(e, d)|. Multiple V-positions in d can show the same I-address, and a reader sees each occurrence.

We observe that resolve(e, d) is fully determined by two quantities: coverage(e), which is fixed at link creation by L12 (LinkImmutability), and M(d), which is the document's current arrangement at the moment of evaluation. No prior V-position is retained; no creation-time arrangement participates. The resolution is always *fresh* — computed from the current state.

**SV0 (ResolutionCurrentness).** For any endset e and document d:

`resolve(e, d) is determined entirely by coverage(e) and the current M(d)`

There is no mechanism by which stale arrangement information could participate, because the link stores only I-addresses (via its endset spans), and V-addresses are derived from them through the current arrangement. This is a structural consequence, not an implementation choice — the link's data simply does not contain V-addresses to cache.

**Definition — Endset Vitality.** An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, resolve(e, d) ≠ ∅.

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when both its from-endset and to-endset are vital in d:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(We exclude the type endset from the vitality condition because type endsets may reference addresses outside dom(Σ.C), per L9, TypeGhostPermission.)

Nelson states the vitality condition as: "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" [LM 4/43]. Our bilateral vitality captures this — the link is useful when something remains at each content endset. The permanent existence of the endset spans in Σ.L is not in question; what is in question is whether those spans project to anything visible.


## The Frame of Link Permanence

Before analysing what arrangement changes do to projection, we establish what they *cannot* do to the link itself.

**SV1 (ArrangementLinkFrame).** For every state transition Σ → Σ':

`(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

This is L12 (LinkImmutability) restated. But the survivability implication is worth making explicit: no arrangement change — no insertion, deletion, rearrangement, or version creation — can alter a link's endsets, its address, or its existence. The link store Σ.L is entirely outside the reach of arrangement operations.

*Consequence for coverage:*

`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

Endset coverage is frozen at creation. This is the pillar on which survivability rests.

*Consequence for directionality:* The from/to/type slot assignment is a structural property of the link value (L6, SlotDistinction). Since L12 preserves the entire link value, the directional assignment — which endset is "from" and which is "to" — is permanent. No operation in the system can swap, reassign, or modify the endset ordering. This is not merely a convention; it is a consequence of the link value's immutability.


## Survivability Under Arrangement Changes

With coverage frozen and arrangements mutable, the survivability question reduces to: how do arrangement changes affect π(e, d) = coverage(e) ∩ ran(M(d))?

Since coverage(e) is invariant, the question is entirely about ran(M(d)) — the set of I-addresses currently referenced by document d. We examine each kind of arrangement change.


### Extension Preserves and May Enlarge

Arrangement extension (K.μ⁺, ArrangementExtension) adds new V→I mappings to M(d) while preserving all existing ones. Therefore ran(M'(d)) ⊇ ran(M(d)), and:

**SV2 (ExtensionMonotonicity).**

`(A Σ →_{K.μ⁺} Σ', e, d :: π(e, d) ⊆ π(e, d'))`

where π(e, d') denotes π in the successor state. Vitality is monotonically preserved: if an endset was vital in d before extension, it remains vital afterward. Extension can only *enlarge* the projection — introducing I-addresses that were in coverage(e) but not previously in ran(M(d)). It cannot remove any.

Proof: π(e, d') = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (SV1) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺ frame), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π(e, d). ∎

*For resolution:* resolve(e, d) ⊆ resolve(e, d'), because every old V-position is preserved (K.μ⁺ preserves existing mappings), and new V-positions may be added.


### Contraction May Reduce

Arrangement contraction (K.μ⁻, ArrangementContraction) removes V→I mappings from M(d). Therefore ran(M'(d)) ⊆ ran(M(d)), and:

**SV3 (ContractionReduction).**

`(A Σ →_{K.μ⁻} Σ', e, d :: π(e, d') ⊆ π(e, d))`

Contraction can only *shrink* the projection. If the contraction removes all V-positions whose I-addresses are in coverage(e), then π(e, d') = ∅ and the endset loses vitality in d. This is the mechanism by which editing can degrade a link's utility in a specific document.

The vitality loss condition is:

`π(e, d) ≠ ∅ ∧ π(e, d') = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

Nelson's survivability condition — "if anything is left at each end" — is precisely the negation of this: as long as at least one I-address from the endset remains in d's arrangement, the endset survives in d.


### Contraction Is Document-Local

**SV4 (ContractionIsolation).**

`(A Σ →_{K.μ⁺/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π(e, d') is unchanged)`

Arrangement operations on document d do not alter any other document's arrangement (frame conditions of K.μ⁺, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`). Therefore π(e, d') = coverage(e) ∩ ran(M(d')) = coverage(e) ∩ ran(M'(d')) is unchanged.

This is a crucial survivability guarantee: one user's editing of their document cannot affect the projection of any endset in any other user's document. If Alice links to a passage in Bob's document, and Bob deletes that passage, the link's projection in *Alice's* document is unaffected. Only the projection in *Bob's* document changes.

The link itself, being in Σ.L, is untouched by either party's edits. What changes is only the observable view through a specific document's arrangement.


### Reordering Preserves Projection, Changes Resolution

Arrangement reordering (K.μ~, ArrangementReordering) is a bijection on V-positions that preserves the multiset of I-addresses: ran(M'(d)) = ran(M(d)). Therefore:

**SV5 (ReorderingProjectionInvariance).**

`(A Σ →_{K.μ~} Σ', e, d :: π(e, d') = π(e, d))`

Rearrangement cannot change which I-addresses are in the projection. The endset references exactly the same content before and after. What changes is *where* that content appears: resolve(e, d') ≠ resolve(e, d) in general, because the V-positions have been remapped.

This is the precise sense in which links "track content, not location." The strap-between-bytes metaphor (Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" [LM 4/42]) expresses this property: rearranging the beads on the string doesn't alter which beads the strap holds, only where they sit.


### Content Allocation and the Boundary Theorem

Content allocation (K.α, ContentAllocation) creates a new I-address a ∉ dom(Σ.C) with content value v. Its frame holds M constant: `(A d :: M'(d) = M(d))`. So π and resolve are trivially unchanged.

But the deeper question is: could the new I-address *coincidentally* fall within the coverage of an existing endset? If so, then a subsequent K.μ⁺ adding a V→I mapping to this new address would enlarge the projection of that endset — the endset would appear to "absorb" new content that was never part of the original link.

We show this cannot happen.

**SV6 (BoundaryExclusion).** Let (s, ℓ) be a span in the endset of some link a ∈ dom(Σ_k.L) at state Σ_k. Let b be any I-address allocated at a later state Σ_j with j > k. Then:

`b ∉ ⟦(s, ℓ)⟧`

*Proof.* The denotation ⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} is a half-open interval under the tumbler ordering T1. We must show that no future I-address allocation can produce a tumbler in this interval. Every I-address in dom(Σ_k.C) is an element-level tumbler (S7b, ElementLevelIAddresses), so zeros(a) = 3 for every content address. The span's start s is such an address.

We reason by cases on the relationship between b and s.

*Case 1: same origin.* Suppose origin(b) = origin(s) — the new address is allocated under the same document prefix. By T9 (ForwardAllocation), allocations within a single allocator's stream are strictly monotonically increasing. Every I-address in ⟦(s, ℓ)⟧ ∩ dom(Σ_k.C) was allocated at or before state k. The maximum such address, call it s_max, satisfies s_max < s ⊕ ℓ (it is the last allocated address within the span). Since b is allocated after state k, T9 gives b > s_max. We need b ≥ s ⊕ ℓ.

Now, I-addresses are element-level tumblers, and the allocator produces them by sibling increment — TA5(c), which increments only the last significant component. By T4 (HierarchicalParsing), an element-level tumbler has exactly three zero separators, so no further child-spawning (TA5 with k > 0) can produce a valid element-level address — it would exceed the three-separator limit. The allocator therefore produces a sequence s, s+1, s+2, ... of ordinal successors, each of the same tumbler length (TA5(c) preserves length). If the span covers n ordinal positions, the last is s+(n−1), and the next allocation produces s+n.

We claim s+n = s ⊕ ℓ when the span (s, ℓ) was constructed from n consecutively allocated I-addresses. In this case ℓ has action point k = #s (the last component), ℓ_k = n, and all earlier components of ℓ are zero. By TumblerAdd: (s ⊕ ℓ)_i = s_i for i < k, (s ⊕ ℓ)_k = s_k + n. This is precisely s+n (n ordinal increments at the last component). So b ≥ s+n = s ⊕ ℓ, meaning b ∉ [s, s ⊕ ℓ).

*Case 2: different origin.* Suppose origin(b) ≠ origin(s). By TA7a (SubspaceClosure), the span (s, ℓ) — when its action point is within the element field — has ⟦(s, ℓ)⟧ contained entirely within the partition of tumblers sharing origin(s). By T10 (PartitionIndependence), b, having a different document prefix, cannot equal any tumbler with origin(s)'s prefix. So b ∉ ⟦(s, ℓ)⟧. ∎

This result has a striking consequence: **endset coverage is intrinsically closed to future allocations.** New content cannot accidentally enter an existing endset. The link's coverage at creation time is its coverage for all time — not merely because the endset data structure is immutable (L12), but because the address space itself is structured so that new allocations cannot fall within existing span intervals.

Nelson's "strap between bytes" metaphor gains formal force: new beads threaded onto the string after the strap was fastened cannot end up under the strap. The geometry of the address space forbids it.


## Link Discovery

We have established what happens to a link's *resolution* under state changes. The other half of survivability concerns *discovery*: finding which links relate to given content.

**Definition — Link Discovery.** For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}, define:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

This is the set of links whose endset at slot s shares at least one I-address with A. Note that partial overlap suffices — a single shared I-address is enough to discover the link.

In practice, the query set A is derived from a document's arrangement: a reader examines some V-region of document d, the system converts those V-positions to I-addresses via M(d), and then searches for links whose endsets intersect those I-addresses. But the discovery function itself is defined purely in I-space, independent of any particular document.

**SV7 (DiscoveryByContentIdentity).** Discovery depends only on the I-address intersection, not on document identity:

`(A d₁, d₂, V₁, V₂ : {M(d₁)(v) : v ∈ V₁} = {M(d₂)(v) : v ∈ V₂} :: discover_s({M(d₁)(v) : v ∈ V₁}) = discover_s({M(d₂)(v) : v ∈ V₂}))`

If two documents (or two regions of the same document) contain the same I-addresses, they discover the same links. Discovery is a property of content identity, not of document identity or arrangement.

This has a powerful consequence: when a document is versioned (J4, Fork), the new version shares I-addresses with the source (by the fork's K.μ⁺ step, which copies V→I mappings from the source). Therefore the version discovers the same links as the source, for any content that both share. No explicit "link copying" is needed; discovery follows automatically from shared content identity.

Similarly, when content is transcluded (K.μ⁺ mapping a V-position to an existing I-address), the target document immediately discovers all links that reference that I-address — without any action by the link creator.

**SV8 (DiscoveryPermanence).** For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

Once a link is discoverable through a set of I-addresses, it remains discoverable through that set in all subsequent states.

Proof: a ∈ discover_s(A) means coverage(Σ.L(a).s) ∩ A ≠ ∅. By L12, a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a). So coverage(Σ'.L(a).s) = coverage(Σ.L(a).s), and the intersection with A is unchanged. ∎

*Caveat:* Discovery through a specific *document* may change, because the document's contribution of I-addresses changes with its arrangement. If d deletes all content that overlapped with a link's endset, discovery through d ceases — not because the link became less discoverable, but because d no longer provides the I-addresses needed for the query. The link remains discoverable through any other document that still contains those I-addresses.

**SV9 (DiscoveryMonotonicity).**

`(A Σ → Σ' :: dom(discover_s(A) in Σ) ⊆ dom(discover_s(A) in Σ'))`

for any fixed A. New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow. Discovery is monotonically non-decreasing in the link population.


## The Discovery-Resolution Distinction

We have now defined two independent operations — discovery and resolution — and we observe that they answer fundamentally different questions:

- **Discovery** asks: "which links relate to this content?" It operates on I-address intersection (coverage(e) ∩ A ≠ ∅), is independent of any particular document's arrangement, and is permanent (SV8).

- **Resolution** asks: "where in document d are this link's endpoints visible?" It operates on I-to-V conversion through d's current arrangement, depends entirely on M(d), and changes as M(d) changes.

**SV10 (DiscoveryResolutionIndependence).** A link may be discoverable through a set of I-addresses A yet have empty resolution in a particular document:

`(E Σ, a, d, s :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ resolve(Σ.L(a).s, d) yields only partial coverage)`

This arises naturally. Suppose a link's from-endset covers I-addresses {i₁, i₂, i₃}. Document d's arrangement contains only i₂. Discovery succeeds (non-empty intersection). But resolution of the from-endset in d returns only the V-positions corresponding to i₂ — the other two I-addresses have no V-positions in d.

Concretely: a link might be discovered from a version or transclusion that shares only a subset of the endset's I-addresses. The link is found, but resolution (in any given document) may return a partial or even empty result, depending on which document's arrangement is used.

This asymmetry is not a deficiency. It reflects a genuine conceptual distinction: the link *exists* and *relates to* certain content (discovery); the *visibility* of that relationship depends on which document you are looking through (resolution).


## Partial Survival

When contraction removes some but not all of an endset's I-addresses from a document's arrangement, the endset survives with reduced projection. We now characterize the structure of this partial survival.

**Definition — Endset Fragment.** For an endset e and document d, a *fragment* of e in d is a maximal contiguous subsequence of I-addresses in π(e, d). That is, a maximal set F ⊆ π(e, d) such that F = ⟦σ⟧ for some span σ, and F cannot be extended to a larger contiguous set within π(e, d).

**SV11 (PartialSurvivalDecomposition).** Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be a block decomposition of M(d) (ASN-0058, BlockDecomposition). The projection π(e, d) can be decomposed as:

`π(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

Each term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is the intersection of two contiguous intervals under the tumbler ordering — a contiguous interval in ⟦(sⱼ, ℓⱼ)⟧ is convex (S0, Convexity), and I(β_k) is contiguous by the definition of mapping blocks (ASN-0058, MappingBlock). The intersection of two convex sets under a total order is convex, so each non-empty term is itself a contiguous set expressible as a span (S1, IntersectionClosure, under level-compatibility).

Therefore π(e, d) is a finite union of spans, expressible as a span-set. By S8 (NormalizationExistence), this span-set can be normalized: sorted by start position with no overlaps or adjacencies.

The significance: **partial survival is well-structured.** The surviving portion of an endset in a given document is always representable as a finite, normalizable span-set. It does not degenerate into an arbitrary subset of I-addresses that defies compact representation.

The number of fragments can grow through repeated contractions: a single contraction that removes I-addresses from the interior of a contiguous endset span splits one fragment into two. But the fragments remain spans, and their union remains a span-set. The original endset's spans provide an upper bound: the number of fragments cannot exceed the number of mapping blocks that overlap the endset's coverage.


## Content Fidelity

The preceding analysis addresses the *extent* of what survives — how many I-addresses remain in the projection. We now address the *identity* of what survives: is the content at those addresses the same as when the link was created?

**SV12 (ContentFidelity).** For any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k:

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))`

for every endset slot s.

This follows immediately from S0 (ContentImmutability): content at an I-address never changes. But the survivability implication merits emphasis: whatever portion of the endset remains visible in a document's arrangement, the content at those I-addresses is *exactly* what was there when the link was created. No edit, no revision, no amount of rearrangement can alter the content the link references. The surviving fragment may be smaller than the original endset, but each byte in the fragment is identical to the original.

Nelson: "The link holder can rely on the strongest possible content guarantee short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation."

The guarantee is architectural rather than cryptographic — there is no hash or signature that a client can verify independently. The guarantee rests on the structural property that the content store is append-only (S1, StoreMonotonicity) and values are frozen at allocation (S0). Nelson explicitly acknowledges this is contractual trust, not mathematical proof of non-tampering [LM 5/17–18].


## The Complete Guarantee

We can now synthesize the survivability guarantee into a single coherent statement.

**SV13 (SurvivabilityTheorem).** For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

(a) *The link persists:* a ∈ dom(Σ'.L) and Σ'.L(a) = (F, G, Θ). [L12]

(b) *Endset coverage is invariant:* coverage(F), coverage(G), coverage(Θ) are the same in Σ' as in Σ. [SV1, from L12]

(c) *Content at endset addresses is unchanged:* for every I-address i in any endset's coverage, Σ'.C(i) = Σ.C(i) when i ∈ dom(Σ.C). [SV12, from S0]

(d) *Discovery is permanent:* if a ∈ discover_s(A) in Σ for some fixed A, then a ∈ discover_s(A) in Σ'. [SV8]

(e) *Resolution is arrangement-dependent:*
- Extension of M(d) can only enlarge resolve(e, d). [SV2]
- Contraction of M(d) can only shrink resolve(e, d). [SV3]
- Reordering of M(d) preserves π(e, d) but changes resolve(e, d). [SV5]
- Changes to M(d) cannot affect resolve(e, d') for d' ≠ d. [SV4]

(f) *New content cannot enter existing endsets:* for any I-address b allocated after the link's creation, b ∉ coverage(F) ∪ coverage(G) ∪ coverage(Θ). [SV6]

(g) *Partial survival is well-structured:* the surviving projection in any document is a finite span-set. [SV11]

The survivability guarantee is therefore: the link, its endsets, and the content at its endset addresses are all permanent. What varies is the *visibility* of the endset content through each document's arrangement — and this variation is precisely characterised by the projection and resolution functions, which respond only to the arrangement of the specific document being queried and are immune to changes elsewhere.

Nelson's "strap between bytes" is exactly right. The strap (the link's endsets) is permanent, fastened to permanent bytes (I-addresses with immutable content). What moves is the string the bytes sit on — the document's Vstream arrangement. The strap follows the bytes, not the string.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| π(e, d) | Endset projection: `coverage(e) ∩ ran(M(d))` | introduced |
| resolve(e, d) | Endset resolution: `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` | introduced |
| Vitality | Endset e is vital in d when `π(e, d) ≠ ∅` | introduced |
| BilateralVitality | Link is bilaterally vital in d when both content endsets are vital or empty | introduced |
| discover_s(A) | Link discovery: `{a ∈ dom(L) : coverage(L(a).s) ∩ A ≠ ∅}` | introduced |
| SV0 | ResolutionCurrentness: resolve(e, d) is determined by coverage(e) and current M(d) | introduced |
| SV1 | ArrangementLinkFrame: arrangement changes preserve L entirely | introduced |
| SV2 | ExtensionMonotonicity: K.μ⁺ can only enlarge π(e, d) | introduced |
| SV3 | ContractionReduction: K.μ⁻ can only shrink π(e, d) | introduced |
| SV4 | ContractionIsolation: changes to M(d) do not affect π(e, d') for d' ≠ d | introduced |
| SV5 | ReorderingProjectionInvariance: K.μ~ preserves π(e, d) exactly | introduced |
| SV6 | BoundaryExclusion: new I-address allocations cannot enter existing endset coverage | introduced |
| SV7 | DiscoveryByContentIdentity: discovery depends on I-address intersection, not document identity | introduced |
| SV8 | DiscoveryPermanence: once discoverable through A, always discoverable | introduced |
| SV9 | DiscoveryMonotonicity: the discoverable set is non-decreasing as links are created | introduced |
| SV10 | DiscoveryResolutionIndependence: discovery and resolution answer different questions with different filters | introduced |
| SV11 | PartialSurvivalDecomposition: the surviving projection is a finite span-set | introduced |
| SV12 | ContentFidelity: content at endset I-addresses is immutable | introduced |
| SV13 | SurvivabilityTheorem: synthesis of the complete guarantee | introduced |


## Open Questions

- What must the system guarantee about resolution when the same I-address appears at multiple V-positions within a single document through within-document sharing?
- Must the system provide a mechanism to transition a dormant link (vital in no document) back to vitality, and if so, what operation achieves this?
- What must the system guarantee about the ordering of fragments in a partially surviving endset — is there a canonical ordering that all implementations must respect?
- When two independent links share overlapping endset coverage, what invariants govern their independent partial survival under the same contraction?
- Must the system guarantee an upper bound on the number of fragments that a single endset can produce in any given document?
- What must the system guarantee about discovery latency — must newly created links be discoverable immediately, or is eventual consistency permitted?
- Under what conditions must bilateral vitality be preserved across a fork (version creation), given that the fork copies only a subset of the source's arrangement?
- What must the system guarantee about the relationship between a link's home document and the documents where its endsets are vital — can these be entirely disjoint?
