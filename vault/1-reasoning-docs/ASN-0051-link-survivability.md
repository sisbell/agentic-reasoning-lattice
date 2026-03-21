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


### Content Allocation and Coverage Stability

Content allocation (K.α, ContentAllocation) creates a new I-address a ∉ dom(Σ.C). Its frame holds M constant: `(A d :: M'(d) = M(d))`. So π and resolve are trivially unchanged by K.α itself.

The deeper question is: could a newly allocated I-address fall within the coverage of an existing endset? If so, a subsequent K.μ⁺ mapping a V-position to this address would enlarge the endset's projection — the endset would appear to absorb new content never part of the original link.

The answer depends on the allocation regime and the address hierarchy. We establish what is provable and identify where the answer is level-dependent.

**SV6 (CrossOriginExclusion).** For a span (s, ℓ) in an existing endset and a newly allocated address b with origin(b) ≠ origin(s), when the action point of ℓ falls within the element field (i.e., beyond the three field separators):

`b ∉ ⟦(s, ℓ)⟧`

*Proof.* By TumblerAdd, components before the action point are copied from s. When the action point is within the element field, the full document prefix (node, user, document fields and their separators) is copied, so the reach s ⊕ ℓ shares origin(s). Since origin(s) is a prefix of both s and s ⊕ ℓ, by T5 (ContiguousSubtrees) every tumbler t with s ≤ t ≤ s ⊕ ℓ satisfies origin(s) ≼ t, hence origin(t) = origin(s). In particular, every t ∈ ⟦(s, ℓ)⟧ = {t : s ≤ t < s ⊕ ℓ} shares origin(s). Since origin(b) ≠ origin(s), b cannot be equal to any such tumbler (T10, PartitionIndependence). ∎

This property is robust — it depends only on the structural separation of document-level prefixes, not on any allocation discipline.

**Same-origin coverage growth.** Under the same document prefix, two mechanisms can place a new I-address within an existing endset span's denotation.

*Sequential overshoot.* If a span's reach extends beyond the current allocation maximum — i.e., the span references addresses not yet allocated — future sibling allocations (TA5(c)) will enter the span as they advance through the ordinal sequence. This is the mechanism by which type endsets referencing ghost addresses (L9, TypeGhostPermission) acquire content: a link whose type endset spans a range in the type hierarchy will match future type addresses as they are allocated within that range.

*Child-depth entry.* The allocator discipline (T10a) permits child-spawning — inc(t, k') with k' > 0 — to create addresses at greater tumbler depth. By the prefix rule (T1 case (ii)), a child-depth address c produced by inc(t, 1) satisfies t < c < t+1, because t is a proper prefix of c (case (ii) gives t < c) and c and t+1 diverge at the position where c has a value less than (t+1)'s (case (i) gives c < t+1). If an endset span contains t and has reach ≥ t+1, the child-depth address c falls within the span. Crucially, when k' = 1, the result has zeros(c) = zeros(t) — the appended component is nonzero (set to 1 by TA5(d)), so no new field separator is introduced, and c remains a valid element-level tumbler (T4 preserved).

*Counterexample to a universal exclusion claim.* Suppose a document D allocates element-level content at ordinals a₁ < a₂ < ... < aₙ, all of the same tumbler length. A link is created with an endset span (a₁, ℓ) where the reach a₁ ⊕ ℓ = aₙ + 1 (one ordinal step beyond the last allocation). If the allocator later spawns a child via inc(aₙ, 1) = c, then c is element-level (zeros(c) = 3), has origin(c) = origin(a₁) = D, and satisfies aₙ < c < aₙ + 1 = a₁ ⊕ ℓ. So c ∈ ⟦(a₁, ℓ)⟧ — the newly allocated address falls within the existing endset's coverage.

**The architectural resolution.** Nelson's design distinguishes these levels explicitly. At the byte level within a document, content allocation is sequential and append-only — new bytes get the next ordinal position in the Istream: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14]. The "strap between bytes" is effectively closed to future allocations as an architectural consequence of this sequential discipline. Gregory's implementation confirms this for text content: the green allocator uses sibling increment exclusively (`tumblerincrement(&lowerbound, rightshift=0, 1, isaptr)`) for text I-address allocation, producing strictly monotonic same-length addresses that cannot enter a tight span over previously allocated content.

At broader address levels — documents, accounts, servers — Nelson explicitly designs for coverage growth: "A span that contains nothing today may at a later time contain a million documents" [LM 4/25]. Links to accounts and nodes find "any of the documents under it" [LM 4/23], including documents not yet created. This is not a deficiency but a feature: ghost elements and hierarchical spanning are fundamental to the design.

The survivability implication: **endset coverage stability is architectural, not definitional.** The coverage *set* is fixed forever (SV1, from L12). What varies is whether that fixed set intersects the growing set of allocated I-addresses — and this intersection can only grow (S1, StoreMonotonicity), never shrink. At the byte level, the intersection is typically closed at creation because sequential allocation ensures new addresses fall beyond existing spans; at broader levels, the intersection is open by design, enabling links that discover future content.


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

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

for any fixed A. New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow. Discovery is monotonically non-decreasing in the link population.


## The Discovery-Resolution Distinction

We have now defined two independent operations — discovery and resolution — and we observe that they answer fundamentally different questions:

- **Discovery** asks: "which links relate to this content?" It operates on I-address intersection (coverage(e) ∩ A ≠ ∅), is independent of any particular document's arrangement, and is permanent (SV8).

- **Resolution** asks: "where in document d are this link's endpoints visible?" It operates on I-to-V conversion through d's current arrangement, depends entirely on M(d), and changes as M(d) changes.

**SV10 (DiscoveryResolutionIndependence).** A link may be discoverable through a set of I-addresses A yet have only partial resolution in a particular document — the projection covers a proper subset of the endset's full coverage:

`(E Σ, a, d, s :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ resolve(Σ.L(a).s, d) ≠ ∅ ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

This arises naturally. Suppose a link's from-endset covers I-addresses {i₁, i₂, i₃}. Document d's arrangement contains only i₂. Discovery succeeds (non-empty intersection). But resolution of the from-endset in d returns only the V-positions corresponding to i₂ — the other two I-addresses have no V-positions in d.

Concretely: a link might be discovered from a version or transclusion that shares only a subset of the endset's I-addresses. The link is found, but resolution (in any given document) may return a partial or even empty result, depending on which document's arrangement is used.

This asymmetry is not a deficiency. It reflects a genuine conceptual distinction: the link *exists* and *relates to* certain content (discovery); the *visibility* of that relationship depends on which document you are looking through (resolution).


## Partial Survival

When contraction removes some but not all of an endset's I-addresses from a document's arrangement, the endset survives with reduced projection. We now characterize the structure of this partial survival.

**Definition — Endset Fragment.** For an endset e and document d with block decomposition B = {β₁, ..., β_p} of M(d), a *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence. Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π(e, d).

**SV11 (PartialSurvivalDecomposition).** Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be a block decomposition of M(d) (ASN-0058, BlockDecomposition). The projection π(e, d) can be decomposed as:

`π(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

Consider each term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k). The span ⟦(sⱼ, ℓⱼ)⟧ is convex by S0 (Convexity). The set I(β_k) = {a_k + j : 0 ≤ j < n_k} is not itself convex in T — child-depth tumblers create gaps between consecutive ordinal increments — but we do not need it to be. For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by TA-strict), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence the intersection is contiguous within the ordinal sequence of I(β_k): if the first and last elements of the intersection have ordinal offsets j₁ and j₂ respectively, then every intermediate element a_k + j with j₁ ≤ j ≤ j₂ also lies in the intersection. Since ordinal increment preserves tumbler length (TA5(c)), all elements of I(β_k) share the same length, and each contiguous subsequence is expressible as a level-uniform span.

Therefore π(e, d) is a finite union of level-uniform spans. However, S8 (NormalizationExistence) requires mutual level-compatibility among spans: all component spans must have starts of the same tumbler length. Each covering span's start has length #a_k, the I-start length of its mapping block. When a document transcludes content from sources at different allocation depths, mapping blocks may have I-starts of different lengths. In that case, normalization applies within each tumbler-depth group independently: the spans can be partitioned by start length, and S8 applies within each partition.

The significance: **partial survival is well-structured.** The surviving portion of an endset in a given document is always representable as a finite, normalizable span-set. It does not degenerate into an arbitrary subset of I-addresses that defies compact representation.

The number of fragments can grow through repeated contractions: a single contraction that removes I-addresses from the interior of a contiguous endset span splits one fragment into two. But the fragments remain spans, and their union remains a span-set. The original endset's spans provide an upper bound: the number of fragments cannot exceed the number of mapping blocks that overlap the endset's coverage.


## Worked Example

We verify the key definitions against a specific scenario with explicit tumbler values.

*Setup.* Consider a document d with five I-addresses a₁ < a₂ < a₃ < a₄ < a₅ in the text subspace, allocated sequentially by sibling increment. All five share the same origin and tumbler length. The document's initial arrangement maps five V-positions in order:

`M(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₃, v₄ ↦ a₄, v₅ ↦ a₅}`

where v₁ < v₂ < v₃ < v₄ < v₅. This is a single mapping block β = (v₁, a₁, 5) in ASN-0058's notation.

A link at address b is created with from-endset F = {(a₂, ℓ)}, where ℓ = a₅ ⊖ a₂ (well-defined by D0, since a₂ < a₅ and both have the same length). The reach is a₂ ⊕ ℓ = a₅ (by D1). So coverage(F) = {t : a₂ ≤ t < a₅}. Among the allocated I-addresses, this interval contains exactly a₂, a₃, a₄.

*Initial state — projection, resolution, discovery.*

- π(F, d) = coverage(F) ∩ ran(M(d)) = {a₂, a₃, a₄}
- resolve(F, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(F)} = {v₂, v₃, v₄}
- discover_from({a₃}) = {b}, since coverage(F) ∩ {a₃} = {a₃} ≠ ∅

The from-endset is vital in d: π(F, d) ≠ ∅. Both π and resolve are determined entirely by coverage(F) and the current M(d) (SV0).

*After contraction.* A K.μ⁻ step removes the mapping at v₃, producing M'(d) with dom(M'(d)) = {v₁, v₂, v₄, v₅} and ran(M'(d)) = {a₁, a₂, a₄, a₅}:

- π(F, d) = coverage(F) ∩ ran(M'(d)) = {a₂, a₄} — reduced (SV3)
- resolve(F, d) = {v₂, v₄}
- discover_from({a₃}) = {b} — unchanged, because coverage(F) is invariant (SV1) and a₃ ∈ coverage(F) regardless of M(d) (SV8)

The endset remains vital but with reduced projection. The removal of a₃ from M(d) has split the endset's visible region into two fragments. To see the decomposition of SV11: the post-contraction arrangement has two mapping blocks — β₁ = (v₁, a₁, 2) covering {v₁, v₂} with I-extent {a₁, a₂}, and β₂ = (v₄, a₄, 2) covering {v₄, v₅} with I-extent {a₄, a₅}. The SV11 terms are:

- ⟦(a₂, ℓ)⟧ ∩ I(β₁) = {t : a₂ ≤ t < a₅} ∩ {a₁, a₂} = {a₂}
- ⟦(a₂, ℓ)⟧ ∩ I(β₂) = {t : a₂ ≤ t < a₅} ∩ {a₄, a₅} = {a₄}

Each non-empty term is a single-element contiguous subsequence of its mapping block's I-extent — trivially a level-uniform span. Together: π(F, d) = {a₂} ∪ {a₄} = {a₂, a₄}. ✓

Discovery through d still works for queries including a₂ or a₄. But discovery through the specific I-address set {a₃} — while still returning b (SV8) — no longer corresponds to anything visible in d, since a₃ ∉ ran(M'(d)). This illustrates the discovery-resolution distinction (SV10): the link is discoverable through a₃, but resolution of the from-endset in d yields no V-position for a₃.

*After reordering.* From the post-contraction state, a K.μ~ step swaps v₂ and v₄: M''(d)(v₂) = a₄, M''(d)(v₄) = a₂ (with v₁ and v₅ unchanged). Since ran(M''(d)) = ran(M'(d)):

- π(F, d) = {a₂, a₄} — unchanged (SV5)
- resolve(F, d) = {v₂, v₄} — same V-positions, but v₂ now shows a₄ and v₄ shows a₂

The projection is invariant under reordering; only the V-position ↦ I-address mapping within the resolution set has changed.


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

(f) *Coverage stability is level-dependent:* new allocations from a different origin cannot enter existing endset spans when the action point is within the element field (SV6). Same-origin coverage growth depends on the allocation regime — closed at the byte level by sequential sibling allocation, open at broader address levels by design. [SV6]

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
| SV6 | CrossOriginExclusion: allocations from a different document prefix cannot enter existing endset spans (within element field) | introduced |
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
