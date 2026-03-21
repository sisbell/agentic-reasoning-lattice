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

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d — that is, every non-empty endset projects to at least one I-address in d's arrangement:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(We exclude the type endset from the vitality condition because type endsets may reference addresses outside dom(Σ.C), per L9, TypeGhostPermission.)

When both F = ∅ and G = ∅, both disjunctions are satisfied by the left branch, making the link bilaterally vital in every document — vacuously. Such a link (∅, ∅, Θ) is a pure type annotation with no content endpoints. This is intentional: the link has no content associations to lose, so the vitality condition is trivially satisfied. The interesting cases arise when at least one content endset is non-empty.

Nelson states the vitality condition as: "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" [LM 4/43]. Nelson's formulation presupposes something at each end to begin with — "if anything is left" implies there was something to leave. Our bilateral vitality captures this for the non-vacuous case — the link is useful when something remains at each content endset. The permanent existence of the endset spans in Σ.L is not in question; what is in question is whether those spans project to anything visible.


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

**SV2 (ExtensionMonotonicity).** (We write π_Σ(e, d) when the state at which projection is evaluated matters; the subscript selects the state whose arrangement M(d) is used.)

`(A Σ →_{K.μ⁺} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d))`

Vitality is monotonically preserved: if an endset was vital in d before extension, it remains vital afterward. Extension can only *enlarge* the projection — introducing I-addresses that were in coverage(e) but not previously in ran(M(d)). It cannot remove any.

Proof: π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (SV1) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺ frame), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*For resolution:* resolve_Σ(e, d) ⊆ resolve_{Σ'}(e, d). Let v ∈ resolve_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Since K.μ⁺ preserves existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))), we have v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ resolve_{Σ'}(e, d). New V-positions in dom(M'(d)) \ dom(M(d)) may additionally enter the resolve set when their I-addresses lie in coverage(e). ∎


### Contraction May Reduce

Arrangement contraction (K.μ⁻, ArrangementContraction) removes V→I mappings from M(d). Therefore ran(M'(d)) ⊆ ran(M(d)), and:

**SV3 (ContractionReduction).**

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d))`

Proof: π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (SV1) and ran(M'(d)) ⊆ ran(M(d)) (K.μ⁻ restricts the domain while preserving values), we have coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

Contraction can only *shrink* the projection. If the contraction removes all V-positions whose I-addresses are in coverage(e), then π_{Σ'}(e, d) = ∅ and the endset loses vitality in d. This is the mechanism by which editing can degrade a link's utility in a specific document.

The vitality loss condition is:

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

Nelson's survivability condition — "if anything is left at each end" — is precisely the negation of this: as long as at least one I-address from the endset remains in d's arrangement, the endset survives in d.

*For resolution:* resolve_{Σ'}(e, d) ⊆ resolve_Σ(e, d). Let v ∈ resolve_{Σ'}(e, d). Then v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), we have v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ resolve_Σ(e, d). ∎


### Contraction Is Document-Local

**SV4 (ArrangementIsolation).**

`(A Σ →_{K.μ⁺/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

Arrangement operations on document d do not alter any other document's arrangement (frame conditions of K.μ⁺, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`). Therefore π_{Σ'}(e, d') = coverage(e) ∩ ran(M'(d')) = coverage(e) ∩ ran(M(d')) = π_Σ(e, d').

This is a crucial survivability guarantee: one user's editing of their document cannot affect the projection of any endset in any other user's document. If Alice links to a passage in Bob's document, and Bob deletes that passage, the link's projection in *Alice's* document is unaffected. Only the projection in *Bob's* document changes.

The link itself, being in Σ.L, is untouched by either party's edits. What changes is only the observable view through a specific document's arrangement.


### Reordering Preserves Projection, Changes Resolution

Arrangement reordering (K.μ~, ArrangementReordering) is a bijection on V-positions that preserves the multiset of I-addresses: ran(M'(d)) = ran(M(d)). Therefore:

**SV5 (ReorderingProjectionInvariance).**

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

Rearrangement cannot change which I-addresses are in the projection. The endset references exactly the same content before and after. What changes is *where* that content appears. Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). The formal relationship is:

`resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)}`

*Proof.* v' ∈ resolve_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e). Since ψ is a bijection from dom(M(d)) to dom(M'(d)), every v' ∈ dom(M'(d)) equals ψ(v) for a unique v ∈ dom(M(d)), and M'(d)(ψ(v)) = M(d)(v). So M'(d)(v') ∈ coverage(e) iff M(d)(v) ∈ coverage(e) iff v ∈ resolve_Σ(e, d). ∎

In general, resolve_{Σ'}(e, d) ≠ resolve_Σ(e, d) as sets. *Witness:* let dom(M(d)) = {v₁, v₂} with M(d) = {v₁ ↦ a₁, v₂ ↦ a₂}, and let coverage(e) = {a₁} (so resolve_Σ(e, d) = {v₁}). The swap ψ(v₁) = v₂, ψ(v₂) = v₁ gives M'(d) = {v₁ ↦ a₂, v₂ ↦ a₁}, so resolve_{Σ'}(e, d) = {v₂} ≠ {v₁}. The resolve set changes whenever ψ maps a V-position inside the resolve set to one outside it, or vice versa.

This is the precise sense in which links "track content, not location." The strap-between-bytes metaphor (Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" [LM 4/42]) expresses this property: rearranging the beads on the string doesn't alter which beads the strap holds, only where they sit.


### Content Allocation and Coverage Stability

Content allocation (K.α, ContentAllocation) creates a new I-address a ∉ dom(Σ.C). Its frame holds M constant: `(A d :: M'(d) = M(d))`. So π and resolve are trivially unchanged by K.α itself.

The deeper question is: could a newly allocated I-address fall within the coverage of an existing endset? If so, a subsequent K.μ⁺ mapping a V-position to this address would enlarge the endset's projection — the endset would appear to absorb new content never part of the original link.

The answer depends on the allocation regime and the address hierarchy. We establish what is provable and identify where the answer is level-dependent.

**SV6 (CrossOriginExclusion).** For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Precondition:* s and b are element-level tumblers (zeros(s) = 3, zeros(b) = 3), so origin(s) and origin(b) are well-defined (per the origin definition in ASN-0036, which requires element-level arguments). L4 (EndsetGenerality) permits non-element-level span starts, but the origin-based exclusion applies only when the start is element-level. The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently, the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`. This ensures the action point falls within the element field — beyond all three field separators.

*Proof.* Let k be the action point of ℓ, with k > p₃ as stated. By TumblerAdd, components before k are copied from s, and (s ⊕ ℓ)ₖ = sₖ + ℓₖ, so s and s ⊕ ℓ agree on positions 1 through k−1. Now consider any t with s ≤ t < s ⊕ ℓ. We claim t agrees with s on all positions 1 through k−1. For suppose t diverges from s at position j < k. Then tⱼ ≠ sⱼ. Since t ≥ s, we have tⱼ > sⱼ (T1 case (i) at the first point of disagreement). But sⱼ = (s ⊕ ℓ)ⱼ (both copy from s at positions before k), so tⱼ > (s ⊕ ℓ)ⱼ, giving t > s ⊕ ℓ by T1 — contradicting t < s ⊕ ℓ. Hence t agrees with s on all positions 1 through k−1.

Since k > p₃, the first k−1 positions of t include all three field-separator positions of s (at the positions where sᵢ = 0). Because t agrees with s on positions 1 through k−1, the three zero components occur at the same positions in t as in s. For any element-level t with zeros(t) = 3, this means t has exactly three field separators at the same positions as s, so the field decomposition of t matches that of s, giving origin(t) = origin(s). (T5 provides supporting context: since origin(s) is a prefix of both s and s ⊕ ℓ, every t in the interval satisfies origin(s) ≼ t — but the prefix property alone does not force the separator positions to align, which is what the sandwich argument above establishes.)

Since b is element-level (S7b), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s), the contrapositive gives: any element-level b with origin(b) ≠ origin(s) satisfies b ∉ ⟦(s, ℓ)⟧. ∎

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

We observe that discover_s is defined purely as a function of an I-address set — it is parameterised by I-addresses, not by document-V-region pairs. So identical I-address sets trivially yield identical discovery results. The interesting consequence is not this definitional fact but the *transclusion discovery guarantee* it entails.

**SV7 (TransclusionCouplingAbsence).** When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself. Formally, the monotonicity result discover_s({a}) in Σ ⊆ discover_s({a}) in Σ' is a direct corollary of SV8 (DiscoveryPermanence) instantiated with A = {a}. What SV7 captures is the *absence of coupling constraints*: no K.ρ (provenance recording), no link-store operation, and no additional elementary transition is required for d₂ to inherit all of a's link associations. K.μ⁺ alone suffices, because discovery operates on I-addresses (which K.μ⁺ shares) and L12 preserves the link store across the transition.

This architectural property — that transclusion inherits link discoverability without coupling — is not formally stronger than SV8, but it is the mechanism by which shared content propagates link relationships. It applies equally to forking (J4): the new version shares I-addresses with the source by the fork's K.μ⁺ step, so it discovers the same links for all shared content without explicit link propagation.

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

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

Note that discovery through d entails non-empty projection in d: if a ∈ discover_s({M(d)(v) : v ∈ V}), then coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅, and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)), we have π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅. So within the discovering document, resolution is guaranteed non-empty.

This arises naturally. Suppose a link's from-endset covers I-addresses {i₁, i₂, i₃}. Document d's arrangement contains only i₂. Discovery succeeds (non-empty intersection). But resolution of the from-endset in d returns only the V-positions corresponding to i₂ — the other two I-addresses have no V-positions in d.

The cross-document case is starker: a link discovered through document d₁ (which shares I-addresses with the endset) may have empty resolution in a different document d₂ whose arrangement contains none of the endset's I-addresses. Discovery and resolution operate through independent documents; discovery through one does not entail resolution in another.

This asymmetry is not a deficiency. It reflects a genuine conceptual distinction: the link *exists* and *relates to* certain content (discovery); the *visibility* of that relationship depends on which document you are looking through (resolution).


## Partial Survival

When contraction removes some but not all of an endset's I-addresses from a document's arrangement, the endset survives with reduced projection. We now characterize the structure of this partial survival.

**Definition — Endset Fragment.** For an endset e and document d with block decomposition B = {β₁, ..., β_p} of M(d), a *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence. Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π(e, d).

**SV11 (PartialSurvivalDecomposition).** Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be a block decomposition of M(d) (ASN-0058, BlockDecomposition). Since B covers only text-subspace V-positions (B1 guards v₁ ≥ 1), define the *text-subspace projection* π_text(e, d) = coverage(e) ∩ ran_text(M(d)), where ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ v₁ ≥ 1} = ⋃_k I(β_k). Then:

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

(The full projection π(e, d) = coverage(e) ∩ ran(M(d)) may additionally include I-addresses reached through non-text-subspace V-positions, if any exist in M(d). The link-subspace contribution is deferred to the Link Subspace ASN. In the current foundation model, no defined operation creates non-text V-positions, so π_text(e, d) = π(e, d) for all reachable states.)

Consider each term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k). The span ⟦(sⱼ, ℓⱼ)⟧ is convex by S0 (Convexity). The set I(β_k) = {a_k + j : 0 ≤ j < n_k} is not itself convex in T — child-depth tumblers create gaps between consecutive ordinal increments — but we do not need it to be. For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by TA-strict), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence the intersection is contiguous within the ordinal sequence of I(β_k): if the first and last elements of the intersection have ordinal offsets j₁ and j₂ respectively, then every intermediate element a_k + j with j₁ ≤ j ≤ j₂ also lies in the intersection. Therefore π_text(e, d) decomposes into finitely many *fragments*, each a contiguous ordinal subsequence within some mapping block's I-extent, compactly described by its first element and count: (a_k + j₁, j₂ − j₁ + 1). The number of fragments is bounded by m · p.

We note a distinction between fragments and span denotations. A fragment is a finite set of I-addresses {a_k + j₁, ..., a_k + j₂} produced by ordinal increment. The span denotation ⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} includes all tumblers in the half-open interval, including child-depth tumblers between consecutive ordinal increments — a child c produced by inc(a, 1) satisfies a < c < a + 1, so c ∈ ⟦(a, ℓ_a)⟧ but c is not necessarily in ran(M(d)). The exact characterisation of π_text(e, d) is the union of its fragments, not a union of span denotations. If one needs to connect projections to the span algebra of ASN-0053, the correct relationship is *covering*: for each fragment with first element a_k + j₁ and last element a_k + j₂, a level-uniform span (a_k + j₁, ℓ') with reach a_k + (j₂ + 1) satisfies ⟦(a_k + j₁, ℓ')⟧ ⊇ fragment (since ordinal increment preserves tumbler length by TA5(c)). Such covering span-sets are normalizable within each tumbler-depth group (S8, NormalizationExistence).

The significance: **partial survival is well-structured.** The surviving portion of an endset in a given document decomposes into finitely many fragments, each compactly described by a start address and count within a mapping block's ordinal sequence. Convexity (S0) ensures contiguity within each block, preventing degeneration into arbitrary subsets of I-addresses.

The number of fragments can grow through repeated contractions: a single contraction that removes I-addresses from the interior of a contiguous endset region splits one fragment into two. But the fragments remain ordinal-contiguous subsequences, compactly described by start and count. The original endset's span count and the number of mapping blocks provide an upper bound: the total number of fragments cannot exceed m · p.


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

Each non-empty term is a single-element fragment — a contiguous ordinal subsequence of count 1 within its mapping block's I-extent. Together: π(F, d) = {a₂} ∪ {a₄} = {a₂, a₄}. ✓

Discovery through d still works for queries including a₂ or a₄. But discovery through the specific I-address set {a₃} — while still returning b (SV8) — no longer corresponds to anything visible in d, since a₃ ∉ ran(M'(d)). This illustrates the discovery-resolution distinction (SV10): the link is discoverable through a₃, but resolution of the from-endset in d yields no V-position for a₃.

*After reordering.* From the post-contraction state, a K.μ~ step swaps v₂ and v₄: M''(d)(v₂) = a₄, M''(d)(v₄) = a₂ (with v₁ and v₅ unchanged). Since ran(M''(d)) = ran(M'(d)):

- π(F, d) = {a₂, a₄} — unchanged (SV5)
- resolve(F, d) = {v₂, v₄} — the V-positions happen to be the same set, because π permutes within the resolve set (both v₂ and v₄ map to I-addresses in coverage(F) before and after the swap)

Note: this worked example illustrates a special case where the resolve *set* is preserved because the swap exchanges two V-positions that both belong to the resolve set. In the general case, the resolve set changes — see the witness in the SV5 discussion. The formal relationship resolve_{Σ'}(F, d) = {ψ(v) : v ∈ resolve_Σ(F, d)} holds here: ψ(v₂) = v₄ and ψ(v₄) = v₂, so {ψ(v₂), ψ(v₄)} = {v₂, v₄} = resolve_Σ(F, d).

The projection is invariant under reordering; the resolution set transforms by the reordering bijection ψ.


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
- Reordering of M(d) preserves π(e, d); resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)} where ψ is the reordering bijection from K.μ~. The resolve *set* may change. [SV5]
- Changes to M(d) cannot affect resolve(e, d') for d' ≠ d. [SV4]
- All other elementary transitions (K.α, K.δ, K.ρ) preserve M in their frame, so resolve(e, d) is unchanged.

(f) *Coverage stability is level-dependent:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field — this is formally proved from the foundations (SV6). Same-origin coverage growth depends on the allocation regime — closed at the byte level by sequential sibling allocation, open at broader address levels by design (the byte-level closure follows from allocation discipline assumptions not formalised in this ASN; see the architectural analysis in the "Content Allocation and Coverage Stability" section).

(g) *Partial survival is well-structured:* the surviving projection in any document decomposes into finitely many ordinal-contiguous fragments within mapping blocks. [SV11]

The survivability guarantee is therefore: the link, its endsets, and the content at its endset addresses are all permanent. What varies is the *visibility* of the endset content through each document's arrangement — and this variation is precisely characterised by the projection and resolution functions, which respond only to the arrangement of the specific document being queried and are immune to changes elsewhere.

Nelson's "strap between bytes" is exactly right. The strap (the link's endsets) is permanent, fastened to permanent bytes (I-addresses with immutable content). What moves is the string the bytes sit on — the document's Vstream arrangement. The strap follows the bytes, not the string.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| π(e, d) | Endset projection: `coverage(e) ∩ ran(M(d))` | introduced |
| resolve(e, d) | Endset resolution: `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` | introduced |
| Vitality | Endset e is vital in d when `π(e, d) ≠ ∅` | introduced |
| BilateralVitality | Link is bilaterally vital in d when each non-empty content endset is vital in d | introduced |
| discover_s(A) | Link discovery: `{a ∈ dom(L) : coverage(L(a).s) ∩ A ≠ ∅}` | introduced |
| SV0 | ResolutionCurrentness: resolve(e, d) is determined by coverage(e) and current M(d) | introduced |
| SV1 | ArrangementLinkFrame: arrangement changes preserve L entirely | introduced |
| SV2 | ExtensionMonotonicity: K.μ⁺ can only enlarge π(e, d) | introduced |
| SV3 | ContractionReduction: K.μ⁻ can only shrink π(e, d) | introduced |
| SV4 | ArrangementIsolation: arrangement changes to M(d) do not affect π(e, d') for d' ≠ d | introduced |
| SV5 | ReorderingProjectionInvariance: K.μ~ preserves π(e, d) exactly | introduced |
| SV6 | CrossOriginExclusion: allocations from a different document prefix cannot enter existing endset spans (within element field) | introduced |
| SV7 | TransclusionCouplingAbsence: K.μ⁺ alone suffices for d₂ to inherit link discoverability — no K.ρ or link-store coupling required (corollary of SV8) | introduced |
| SV8 | DiscoveryPermanence: once discoverable through A, always discoverable | introduced |
| SV9 | DiscoveryMonotonicity: the discoverable set is non-decreasing as links are created | introduced |
| SV10 | DiscoveryResolutionIndependence: discovery and resolution answer different questions with different filters | introduced |
| SV11 | PartialSurvivalDecomposition: the text-subspace projection decomposes into finitely many ordinal-contiguous fragments within mapping blocks | introduced |
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
