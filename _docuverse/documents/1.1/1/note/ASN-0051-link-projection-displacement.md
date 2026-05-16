# ASN-0051: Link Projection Displacement

*2026-03-23*

We are looking for the invariants that govern what a link holder can rely on across state changes. A link has been created — its endsets are fixed (L12, LinkImmutability), its address is permanent (T8, AllocationPermanence). The endsets reference I-addresses in the content store, which is itself immutable (S0, ContentImmutability). So the link, structurally, is as permanent as anything in the system.

Yet the question of survivability is not about the link's *structure*. It is about the link's *utility*. A link is useful when its endpoints can be resolved to observable content in some document's current arrangement. Arrangements change — content is inserted, deleted, rearranged. What do these changes do to the link's observable behaviour?

The answer has two parts: a *discovery* question (can the link be found?) and a *resolution* question (can the link's endpoints be followed to visible content?). These are independent questions with independent answers. We develop each in turn.


## Endset Projection

To reason about survivability we need to formalize how a link's endsets relate to a document's current state. The link's endsets are sets of spans over I-addresses (L3, TripleEndsetStructure; L4, EndsetGenerality). A document's arrangement M(d) maps V-positions to I-addresses (ASN-0036). The question "what does this endset look like in document d right now?" has a precise answer.

**Definition — Endset Projection.** For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

This is the set of I-addresses that the endset references and that d currently contains in its arrangement. Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

**Definition — Endset Location.** For an endset e and document d, the *location* of e in d is:

`locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

These are the V-positions in d whose content is part of the endset. Resolution gives the positions a reader would see; projection gives the underlying content identities.

The two are related by M(d)'s function property (S2, ArrangementFunctionality): v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d). Since M(d) need not be injective — within-document sharing is permitted (S5, UnrestrictedSharing) — we may have |locate(e, d)| ≥ |π(e, d)|. Multiple V-positions in d can show the same I-address, and a reader sees each occurrence.

We observe that locate(e, d) is fully determined by two quantities: coverage(e), which is fixed at link creation by L12 (LinkImmutability), and M(d), which is the document's current arrangement at the moment of evaluation. No prior V-position is retained; no creation-time arrangement participates. The resolution is always *fresh* — computed from the current state.

This observation is definitional — locate is defined as `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`, so the input dependency is built into the function itself. The substantive claim worth stating is about *what the algebra forbids*: no state component external to (coverage(e), M(d)) participates in resolution, because no such component exists in the link store.

**SV0 (NoStaleResolutionState).** For every state Σ, endset e, and document d ∈ Σ.E_doc:

`locate_Σ(e, d) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`

— that is, locate is computed against the *current* arrangement Σ.M(d), with no contribution from any earlier arrangement Σ_k.M(d) (k < current) or from any cached V-addresses derived at link creation.

The claim is architectural, not definitional. A naive implementation might cache V-positions at link creation time, leaving stale entries when the document is rearranged. SV0 states that such caching is *structurally precluded* by the link-store representation. The link value Σ.L(a) = (F, G, Θ) stores I-addresses only — via spans (s, ℓ) over T (L3, TripleEndsetStructure) — and V-addresses are derived from them through the current arrangement. There is no creation-time arrangement field in the link value, no historical-M slot in Σ, and no operation that records or returns historical V-positions. Any conforming implementation must compute resolution against the current arrangement; no other behaviour is expressible within the algebra.

**Definition — Endset Vitality.** An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, locate(e, d) ≠ ∅.

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d — that is, every non-empty endset projects to at least one I-address in d's arrangement:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(We exclude the type endset from the vitality condition because type endsets may reference addresses outside dom(Σ.C), per L9, TypeGhostPermission.)

When both F = ∅ and G = ∅, both disjunctions are satisfied by the left branch, making the link bilaterally vital in every document — vacuously. Such a link (∅, ∅, Θ) is a pure type annotation with no content endpoints. This is intentional: the link has no content associations to lose, so the vitality condition is trivially satisfied. The interesting cases arise when at least one content endset is non-empty.

*Asymmetric empty endsets.* The asymmetric cases — exactly one of F, G empty — also follow mechanically from the disjunction structure. When F = ∅ but G ≠ ∅, coverage(F) = ∅, so π(F, d) = ∅ ∩ ran(M(d)) = ∅ and locate(F, d) = ∅ for every document d. The from-endset is non-vital in every document, but bilateral vitality requires only that the non-empty endset G be vital — the disjunction `F = ∅ ∨ π(F, d) ≠ ∅` is satisfied by its left branch. Such a link is unidirectional in its content anchoring; it asserts an association anchored only at G. The symmetric case (F ≠ ∅, G = ∅) is identical with the roles of F and G interchanged. More generally, for any endset e with coverage(e) = ∅ and any address set A ⊆ dom(Σ.C): π(∅, d) = ∅, locate(∅, d) = ∅, and discover_s(∅) = ∅ — projection, location, and discovery degenerate by the empty-intersection rule. The substantive survivability analysis below concerns the non-trivial case where the queried endset and address set are non-empty; the empty cases are stated explicitly here so that subsequent formulas need not carry empty-endset side conditions.

Nelson states the vitality condition as: "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" [LM 4/43]. Nelson's formulation presupposes something at each end to begin with — "if anything is left" implies there was something to leave. Our bilateral vitality captures this for the non-vacuous case — the link is useful when something remains at each content endset. The permanent existence of the endset spans in Σ.L is not in question; what is in question is whether those spans project to anything visible.


## The Frame of Link Permanence

Before analysing what arrangement changes do to projection, we establish what they *cannot* do to the link itself.

**Corollary (ArrangementLinkFrame, from L12, ASN-0043).** Link immutability is guaranteed directly by the foundation: for every state transition Σ → Σ', `(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`. We do not assign this a new SV label because it introduces no new content beyond L12 — it is L12 read for its survivability content. The implication is worth making explicit nonetheless: no arrangement change — no insertion, deletion, rearrangement, or version creation — can alter a link's endsets, its address, or its existence. The link store Σ.L is entirely outside the reach of arrangement operations.

*Consequence for coverage:*

`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

Endset coverage is frozen at creation. This is the pillar on which survivability rests.

*Consequence for directionality:* The from/to/type slot assignment is a structural property of the link value (L6, SlotDistinction). Since L12 preserves the entire link value, the directional assignment — which endset is "from" and which is "to" — is permanent. No operation in the system can swap, reassign, or modify the endset ordering. This is not merely a convention; it is a consequence of the link value's immutability.


## Survivability Under Arrangement Changes

With coverage frozen and arrangements mutable, the survivability question reduces to: how do arrangement changes affect π(e, d) = coverage(e) ∩ ran(M(d))?

Since coverage(e) is invariant, the question is entirely about ran(M(d)) — the set of I-addresses currently referenced by document d. We examine each kind of arrangement change.


### Extension Preserves and May Enlarge

Two elementary transitions extend a document's arrangement by adding new V→I mappings while preserving all existing ones. *Content-subspace extension* K.μ⁺ (ArrangementExtension, ASN-0047) adds mappings of the form v ↦ i where v has subspace(v) = s_C and i ∈ dom(Σ.C); the new I-addresses are content addresses. *Link-subspace extension* K.μ⁺_L (LinkSubspaceExtension, ASN-0047) adds exactly one mapping v_ℓ ↦ ℓ where subspace(v_ℓ) = s_L and ℓ ∈ dom(Σ.L); the new I-address is a link address. Both transitions satisfy `ran(M'(d)) ⊇ ran(M(d))`, and the survivability argument for π is identical in both cases — it depends only on monotonic enlargement of ran(M(d)), not on which subspace the new V-positions inhabit. We therefore state one claim covering both transitions.

**SV2 (ExtensionMonotonicity).** (We write π_Σ(e, d) when the state at which projection is evaluated matters; the subscript selects the state whose arrangement M(d) is used.)

`(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d))`

Vitality is monotonically preserved: if an endset was vital in d before extension, it remains vital afterward. Extension can only *enlarge* the projection — introducing I-addresses that were in coverage(e) but not previously in ran(M(d)). It cannot remove any.

Proof: π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (L12, ASN-0043) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺/K.μ⁺_L frame), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*For resolution:* locate_Σ(e, d) ⊆ locate_{Σ'}(e, d). Let v ∈ locate_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Both K.μ⁺ and K.μ⁺_L preserve existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))). So v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ locate_{Σ'}(e, d). New V-positions in dom(M'(d)) \ dom(M(d)) may additionally enter the locate set when their I-addresses lie in coverage(e). ∎

*Distinct architectural roles.* The two transitions enlarge different parts of ran(M(d)) and so contribute to different parts of π(e, d). For an endset e whose coverage lies entirely in dom(Σ.C) (the typical content endset, with spans over content I-addresses), only K.μ⁺ can strictly enlarge π(e, d) — the new I-address introduced by K.μ⁺_L is a link address in dom(Σ.L), disjoint from coverage(e). Conversely, for an endset whose coverage contains link addresses — permitted by L4 (EndsetGenerality) and the reflexive-addressing case of L13 (ReflexiveAddressing) — K.μ⁺_L can strictly enlarge π(e, d) while K.μ⁺ cannot reach those coverage members at all. The unified SV2 statement remains correct for both cases (the inclusion is reflexive when neither extension touches coverage(e)); the strictness of the inclusion depends on which subspace the endset references. We defer the detailed analysis of link-referencing endsets and reflexive addressing to the Link Subspace ASN; SV2 here captures the monotonicity that both transitions share without committing to a particular subspace.


### Contraction May Reduce

Arrangement contraction (K.μ⁻, ArrangementContraction) removes V→I mappings from M(d). Therefore ran(M'(d)) ⊆ ran(M(d)), and:

**SV3 (ContractionReduction).**

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d))`

Proof: π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (L12, ASN-0043) and ran(M'(d)) ⊆ ran(M(d)) (K.μ⁻ restricts the domain while preserving values), we have coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

Contraction can only *shrink* the projection. If the contraction removes all V-positions whose I-addresses are in coverage(e), then π_{Σ'}(e, d) = ∅ and the endset loses vitality in d. This is the mechanism by which editing can degrade a link's utility in a specific document.

The vitality loss condition is:

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

Nelson's survivability condition — "if anything is left at each end" — is precisely the negation of this: as long as at least one I-address from the endset remains in d's arrangement, the endset survives in d.

*For resolution:* locate_{Σ'}(e, d) ⊆ locate_Σ(e, d). Let v ∈ locate_{Σ'}(e, d). Then v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), we have v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ locate_Σ(e, d). ∎


### Contraction Is Document-Local

**SV4 (ArrangementIsolation).**

`(A Σ →_{K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

Arrangement operations on document d do not alter any other document's arrangement (frame conditions of K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`). Therefore π_{Σ'}(e, d') = coverage(e) ∩ ran(M'(d')) = coverage(e) ∩ ran(M(d')) = π_Σ(e, d').

*For resolution:* `locate_{Σ'}(e, d') = locate_Σ(e, d')`. Since M'(d') = M(d') (frame), locate_{Σ'}(e, d') = {v ∈ dom(M'(d')) : M'(d')(v) ∈ coverage(e)} = {v ∈ dom(M(d')) : M(d')(v) ∈ coverage(e)} = locate_Σ(e, d'). ∎

This is a crucial survivability guarantee: one user's editing of their document cannot affect the projection of any endset in any other user's document. If Alice links to a passage in Bob's document, and Bob deletes that passage, the link's projection in *Alice's* document is unaffected. Only the projection in *Bob's* document changes.

The link itself, being in Σ.L, is untouched by either party's edits. What changes is only the observable view through a specific document's arrangement.


### Reordering Preserves Projection, Changes Resolution

Arrangement reordering (K.μ~, ArrangementReordering) is a bijection on V-positions that preserves the multiset of I-addresses: ran(M'(d)) = ran(M(d)). Therefore:

**SV5 (ReorderingProjectionInvariance).**

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

Rearrangement cannot change which I-addresses are in the projection. The endset references exactly the same content before and after. What changes is *where* that content appears. Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). The formal relationship is:

`locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`

*Proof.* v' ∈ locate_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e). Since ψ is a bijection from dom(M(d)) to dom(M'(d)), every v' ∈ dom(M'(d)) equals ψ(v) for a unique v ∈ dom(M(d)), and M'(d)(ψ(v)) = M(d)(v). So M'(d)(v') ∈ coverage(e) iff M(d)(v) ∈ coverage(e) iff v ∈ locate_Σ(e, d). ∎

In general, locate_{Σ'}(e, d) ≠ locate_Σ(e, d) as sets. *Witness:* let dom(M(d)) = {v₁, v₂} with M(d) = {v₁ ↦ a₁, v₂ ↦ a₂}, and let coverage(e) = {a₁} (so locate_Σ(e, d) = {v₁}). The swap ψ(v₁) = v₂, ψ(v₂) = v₁ gives M'(d) = {v₁ ↦ a₂, v₂ ↦ a₁}, so locate_{Σ'}(e, d) = {v₂} ≠ {v₁}. The locate set changes whenever ψ maps a V-position inside the locate set to one outside it, or vice versa.

This is the precise sense in which links "track content, not location." The strap-between-bytes metaphor (Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" [LM 4/42]) expresses this property: rearranging the beads on the string doesn't alter which beads the strap holds, only where they sit.


### Content Allocation and Coverage Stability

Content allocation (K.α, ContentAllocation) creates a new I-address a ∉ dom(Σ.C). Its frame holds M constant: `(A d :: M'(d) = M(d))`. So π and locate are trivially unchanged by K.α itself.

The deeper question is: could a newly allocated I-address fall within the coverage of an existing endset? If so, a subsequent K.μ⁺ mapping a V-position to this address would enlarge the endset's projection — the endset would appear to absorb new content never part of the original link.

The answer depends on the allocation regime and the address hierarchy. We establish what is provable and identify where the answer is level-dependent.

**SV6 (CrossOriginExclusion).** For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Precondition:* s and b are element-level tumblers (zeros(s) = 3, zeros(b) = 3), so origin(s) and origin(b) are well-defined (per the origin definition in ASN-0036, which requires element-level arguments). L4 (EndsetGenerality) permits non-element-level span starts, but the origin-based exclusion applies only when the start is element-level. The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently, the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`. This ensures the action point falls within the element field — beyond all three field separators.

*Proof.* Let k be the action point of ℓ, with k > p₃ as stated. By TumblerAdd, components before k are copied from s, and (s ⊕ ℓ)ₖ = sₖ + ℓₖ, so s and s ⊕ ℓ agree on positions 1 through k−1. Now consider any t with s ≤ t < s ⊕ ℓ. First, #t ≥ k: if #t < k, then either t agrees with s on all positions 1 through #t — making t a proper prefix of s, so t < s by T1(ii), contradicting s ≤ t — or let j be the first position where tⱼ ≠ sⱼ; since t ≥ s and j is the first divergence, T1(i) gives tⱼ > sⱼ. Since j ≤ #t < k, we have (s ⊕ ℓ)ⱼ = sⱼ (TumblerAdd copies from s at positions before k). Moreover, t agrees with s on positions 1 through j−1, and s ⊕ ℓ agrees with s on positions 1 through k−1 (with j−1 < k−1), so the first divergence of t and s ⊕ ℓ is at j. Therefore tⱼ > (s ⊕ ℓ)ⱼ, giving t > s ⊕ ℓ by T1(i) — contradicting t < s ⊕ ℓ. We claim t agrees with s on all positions 1 through k−1. For suppose there exists a position j < k where tⱼ ≠ sⱼ, and let j be the *first* such position. Since t ≥ s and t agrees with s on positions 1 through j−1, T1(i) gives tⱼ > sⱼ. But sⱼ = (s ⊕ ℓ)ⱼ (TumblerAdd copies from s at positions before k). Since t agrees with s on positions 1 through j−1 and s ⊕ ℓ agrees with s on positions 1 through k−1 (with j−1 < k−1), the first divergence of t and s ⊕ ℓ is at j. Therefore tⱼ > (s ⊕ ℓ)ⱼ, giving t > s ⊕ ℓ by T1(i) — contradicting t < s ⊕ ℓ. Hence t agrees with s on all positions 1 through k−1.

Since k > p₃, the first k−1 positions of t include all three field-separator positions of s — call them p₁, p₂, p₃ (the positions where sᵢ = 0). Because t agrees with s on positions 1 through k−1, we have t_{p₁} = t_{p₂} = t_{p₃} = 0, so t has at least three zero components, all located within positions 1 through k−1: zeros(t) ≥ 3, with at least three zeros at positions p₁, p₂, p₃.

*Restricting to element-level t.* For element-level t — those with zeros(t) = 3 — the inequality is tight. The three zeros at p₁, p₂, p₃ already account for all zero components of t, so t has *exactly* three zeros and they sit at exactly the positions p₁, p₂, p₃. In particular, no zero component lies at any position j with k ≤ j ≤ #t — every component beyond position k − 1 is nonzero. Hence the field decomposition of t — the partition of its components by the three field-separator positions p₁, p₂, p₃ — matches the field decomposition of s component-by-component up to position p₃. The first four fields (server, account, document) of t are identical to those of s, so origin(t) = origin(s).

Since b is element-level (S7b — `zeros(b) = 3`), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s), the contrapositive gives: any element-level b with origin(b) ≠ origin(s) satisfies b ∉ ⟦(s, ℓ)⟧. ∎

*Note.* T5 gives the weaker result origin(s) ≼ t for every t in the interval, but this prefix containment does not force separator positions to align — the sandwich argument above establishes the stronger claim.

This property is robust — it depends only on the structural separation of document-level prefixes, not on any allocation discipline.

**Same-origin coverage growth.** Under the same document prefix, two mechanisms can place a new I-address within an existing endset span's denotation.

*Sequential overshoot.* If a span's reach extends beyond the current allocation maximum — i.e., the span references addresses not yet allocated — future sibling allocations (TA5(c)) will enter the span as they advance through the ordinal sequence. This is the mechanism by which type endsets referencing ghost addresses (L9, TypeGhostPermission) acquire content: a link whose type endset spans a range in the type hierarchy will match future type addresses as they are allocated within that range.

*Child-depth entry.* The allocator discipline (T10a) permits child-spawning — inc(t, k') with k' > 0 — to create addresses at greater tumbler depth. By the prefix rule (T1 case (ii)), a child-depth address c produced by inc(t, 1) satisfies t < c < t+1, because t is a proper prefix of c (case (ii) gives t < c) and c and t+1 diverge at the position where c has a value less than (t+1)'s (case (i) gives c < t+1). If an endset span contains t and has reach ≥ t+1, the child-depth address c falls within the span. Crucially, when k' = 1, the result has zeros(c) = zeros(t) — the appended component is nonzero (set to 1 by TA5(d)), so no new field separator is introduced, and c remains a valid element-level tumbler (T4 preserved).

*Counterexample to a universal exclusion claim.* Suppose a document D allocates element-level content at ordinals a₁ < a₂ < ... < aₙ, all of the same tumbler length. A link is created with an endset span (a₁, ℓ) where the reach a₁ ⊕ ℓ = aₙ + 1 (one ordinal step beyond the last allocation). If the allocator later spawns a child via inc(aₙ, 1) = c, then c is element-level (zeros(c) = 3), has origin(c) = origin(a₁) = D, and satisfies aₙ < c < aₙ + 1 = a₁ ⊕ ℓ. So c ∈ ⟦(a₁, ℓ)⟧ — the newly allocated address falls within the existing endset's coverage.

**The architectural resolution.** Nelson's design distinguishes these levels explicitly. At the byte level within a document, content allocation is sequential and append-only — new bytes get the next ordinal position in the Istream: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14]. The "strap between bytes" is effectively closed to future allocations as an architectural consequence of this sequential discipline. Gregory's implementation confirms this for text content: the green allocator uses sibling increment exclusively (`tumblerincrement(&lowerbound, rightshift=0, 1, isaptr)`) for text I-address allocation, producing strictly monotonic same-length addresses that cannot enter a tight span over previously allocated content.

At broader address levels — documents, accounts, servers — Nelson explicitly designs for coverage growth: "A span that contains nothing today may at a later time contain a million documents" [LM 4/25]. Links to accounts and nodes find "any of the documents under it" [LM 4/23], including documents not yet created. This is not a deficiency but a feature: ghost elements and hierarchical spanning are fundamental to the design.

The survivability implication: **endset coverage stability is architectural, not definitional.** The coverage *set* is fixed forever (L12, ASN-0043). What varies is whether that fixed set intersects the growing set of allocated I-addresses — and this intersection can only grow (S1, StoreMonotonicity), never shrink. At the byte level, the intersection is typically closed at creation because sequential allocation ensures new addresses fall beyond existing spans; at broader levels, the intersection is open by design, enabling links that discover future content.


## Link Discovery

We have established what happens to a link's *resolution* under state changes. The other half of survivability concerns *discovery*: finding which links relate to given content.

**Definition — Link Discovery.** For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}, define:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

This is the set of links whose endset at slot s shares at least one I-address with A. Note that partial overlap suffices — a single shared I-address is enough to discover the link.

In practice, the query set A is derived from a document's arrangement: a reader examines some V-region of document d, the system converts those V-positions to I-addresses via M(d), and then searches for links whose endsets intersect those I-addresses. But the discovery function itself is defined purely in I-space, independent of any particular document.

We observe that discover_s is defined purely as a function of an I-address set — it is parameterised by I-addresses, not by document-V-region pairs. So identical I-address sets trivially yield identical discovery results. The interesting consequence is not this definitional fact but the *transclusion discovery guarantee* it entails.

**SV7 (TransclusionCouplingAbsence).** When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself. Formally, for any transition Σ → Σ' that holds L in frame and any set of I-addresses A:

`discover_s(A) in Σ' = discover_s(A) in Σ`

*Proof.* K.μ⁺ and K.μ⁺_L both hold L in their frame: dom(L') = dom(L) and L'(a) = L(a) for all a ∈ dom(L). Therefore coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) for every a ∈ dom(Σ.L), and dom(Σ'.L) = dom(Σ.L). Both inputs to discover_s — coverage and dom(L) — are identical in Σ and Σ', so the discovery sets are equal. ∎

What SV7 captures is the *absence of discovery-relevant coupling constraints*: no link-store operation and no additional elementary transition affecting L or M is required for d₂ to inherit all of a's link associations. The equality — not merely monotonicity — confirms that K.μ⁺ introduces no new discovery relationships and removes none. The discovery mechanism itself — discover_s operating on coverage and dom(L) — is coupling-free: K.μ⁺ alone provides the I-address sharing that enables discovery, and L12 preserves the link store across the transition. (A valid composite transition containing K.μ⁺ may additionally require K.ρ to satisfy J1★ (ExtensionRecordsProvenanceContent, ASN-0047), but K.ρ modifies R only — it does not alter L or M, so the discovery result is unaffected.)

This architectural property — that transclusion inherits link discoverability without coupling — is the architecturally significant application. The same equality holds for every elementary transition that holds L in frame — K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ — since the proof depends solely on L being invariant. The only transition where the inclusion of SV9 can be strict is K.λ, which adds a new link to dom(L). We highlight K.μ⁺/K.μ⁺_L because the transclusion case is the one where the equality has substantive architectural consequence: arrangement extension provides the I-address sharing that enables discovery in the new document. The same reasoning applies to forking (J4): the new version shares I-addresses with the source by the fork's K.μ⁺ step, so it discovers the same links for all shared content without explicit link propagation.

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

We distinguish two related concepts that the decomposition produces: *decomposition terms* — the individual set intersections that appear in the union formula — and *maximal fragments* — the maximal contiguous ordinal subsequences that the union as a whole presents in each mapping block. The two coincide when each span contributes a disjoint contiguous region; they diverge when adjacent or overlapping spans coalesce.

**Definition — Decomposition Term.** For each pair (j, k) with 1 ≤ j ≤ m and 1 ≤ k ≤ p, the *(j, k)-decomposition term* is the set `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)`. The number of decomposition terms is exactly m · p (possibly with empty terms).

**Definition — Maximal Endset Fragment.** For an endset e and document d, let B = {β₁, ..., β_p} be the maximally merged block decomposition (M11, M12, ASN-0058) of the restriction M(d)|_{V_{s_C}(d)}. A *maximal fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence taken within the *full* projection. Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π_text(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π_text(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π_text(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π_text(e, d).

A decomposition term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is itself contiguous in the ordinal sequence of I(β_k) (by the convexity argument below) but need not be maximal: two terms with the same k may overlap or be adjacent, in which case their union forms a single maximal fragment.

**SV11 (PartialSurvivalDecomposition).** Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be the maximally merged block decomposition of the restriction M(d)|_{V_{s_C}(d)} — the content-subspace portion of d's arrangement. This restriction satisfies C1a's conditions: functionality from S2, finiteness from S8-fin, and fixed depth from S8-depth within subspace s_C. Define the *text-subspace projection* π_text(e, d) = coverage(e) ∩ ran_text(M(d)), where ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C} = ⋃_k I(β_k). The equality holds because B covers exactly the content-subspace V-positions (B1 applied to the restriction), so the I-extents of B's blocks are precisely the content-subspace I-addresses. Then:

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

(The full projection π(e, d) = coverage(e) ∩ ran(M(d)) may additionally include I-addresses reached through link-subspace V-positions. K.μ⁺_L (LinkSubspaceExtension, ASN-0047) creates link-subspace V-positions `v_ℓ ↦ ℓ` where `subspace(v_ℓ) = s_L`, so π_text(e, d) ⊆ π(e, d) in general. The link-subspace contribution to projection — including links whose endsets reference other link addresses (L13, ReflexiveAddressing) — is deferred to the Link Subspace ASN.)

Consider each decomposition term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k). The span ⟦(sⱼ, ℓⱼ)⟧ is convex by S0 (Convexity). The set I(β_k) = {a_k + j : 0 ≤ j < n_k} is not itself convex in T — child-depth tumblers create gaps between consecutive ordinal increments — but we do not need it to be. For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by M1 (OrderPreservation, ASN-0058)), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence each decomposition term is contiguous within the ordinal sequence of I(β_k): if its first and last elements have ordinal offsets j₁ and j₂, every intermediate a_k + j with j₁ ≤ j ≤ j₂ also lies in the term.

*Decomposition terms versus maximal fragments.* The number of decomposition terms is m · p exactly — one per (span, block) pair, including empty terms. Within a single block β_k, the m terms `⟦(s₁, ℓ₁)⟧ ∩ I(β_k), ..., ⟦(s_m, ℓ_m)⟧ ∩ I(β_k)` are each contiguous in the ordinal sequence of I(β_k), but they may overlap or be adjacent; their union π_text(e, d) ∩ I(β_k) may therefore consist of fewer maximal contiguous regions than there are non-empty terms. A maximal fragment is one such maximal contiguous region. Hence the number of maximal fragments within a single block is at most the number of non-empty decomposition terms in that block, which is at most m. Across p blocks, the number of maximal fragments is bounded by m · p — the same upper bound as for decomposition terms, attained when every non-empty term is itself a maximal fragment (when the spans contribute pairwise non-adjacent regions within each block). Each maximal fragment is compactly described by its first element and count: (a_k + j₁, j₂ − j₁ + 1).

When M(d) is non-injective — within-document sharing (S5, UnrestrictedSharing) — two blocks may have overlapping I-extents, so maximal fragments from distinct blocks may share I-addresses. The fragment collection is therefore a *cover* of π_text(e, d), not necessarily a partition; summing fragment widths may overcount distinct I-addresses. The set-union formula `π_text(e, d) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))` remains correct (set union is idempotent), and it does not depend on the term/fragment distinction.

We note a distinction between maximal fragments (or decomposition terms — both are contiguous ordinal subsequences) and span denotations. A maximal fragment is a finite set of I-addresses {a_k + j₁, ..., a_k + j₂} produced by ordinal increment within an actually-allocated block. The span denotation ⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} includes all tumblers in the half-open interval, including child-depth tumblers between consecutive ordinal increments — a child c produced by inc(a, 1) satisfies a < c < a + 1, so c ∈ ⟦(a, ℓ)⟧ for any span (a, ℓ) whose reach satisfies a ⊕ ℓ > a + 1, but c is not necessarily in ran(M(d)). The exact characterisation of π_text(e, d) is the union of its maximal fragments (equivalently, the union of its decomposition terms), not a union of span denotations. If one needs to connect projections to the span algebra of ASN-0053, the correct relationship is *covering*: for each maximal fragment with first element a_k + j₁ and last element a_k + j₂, a level-uniform span (a_k + j₁, ℓ') with reach a_k + (j₂ + 1) satisfies ⟦(a_k + j₁, ℓ')⟧ ⊇ fragment (since ordinal increment preserves tumbler length by TA5(c)). Such covering span-sets are normalizable within each tumbler-depth group (S8, NormalizationExistence).

The significance: **partial survival is well-structured.** The surviving portion of an endset in a given document decomposes into finitely many maximal fragments — at most m · p of them, where m is the endset's span count and p is the block count — each compactly described by a start address and count within a mapping block's ordinal sequence. Convexity (S0) ensures contiguity within each block, preventing degeneration into arbitrary subsets of I-addresses.

The number of maximal fragments can grow through repeated edits: a composite operation (K.μ~ followed by K.μ⁻) that rearranges interior content to the maximum V-position and then removes it has the net effect of excising I-addresses from the interior of a contiguous endset region. The excision is enacted on M(d) (via the contraction), which in turn changes the block decomposition B — the single block that previously covered the contiguous region splits into two adjacent blocks. The maximal fragment that lay across the excision splits along the new block boundary into two ordinal-contiguous subsequences, one per resulting block. Compact description by (start, count) is preserved for each part. The upper bound m · p (spans times blocks) still applies after the operation, with both the block count p and the maximal-fragment count potentially increased.


## Worked Example

We verify the key definitions against a specific scenario with explicit tumbler values.

*Setup.* Consider a document d with five I-addresses a₁ < a₂ < a₃ < a₄ < a₅ in the text subspace, allocated sequentially by sibling increment. All five share the same origin and tumbler length. The document's initial arrangement maps five V-positions in order:

`M(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₃, v₄ ↦ a₄, v₅ ↦ a₅}`

where v₁ < v₂ < v₃ < v₄ < v₅. This is a single mapping block β = (v₁, a₁, 5) in ASN-0058's notation.

A link at address b is created with from-endset F = {(a₂, ℓ)}, where ℓ = a₅ ⊖ a₂ (well-defined by D0, since a₂ < a₅ and both have the same length). The reach is a₂ ⊕ ℓ = a₅ (by D1). So coverage(F) = {t : a₂ ≤ t < a₅}. Among the allocated I-addresses, this interval contains exactly a₂, a₃, a₄.

*Initial state — projection, resolution, discovery.*

- π(F, d) = coverage(F) ∩ ran(M(d)) = {a₂, a₃, a₄}
- locate(F, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(F)} = {v₂, v₃, v₄}
- discover_from({a₃}) = {b}, since coverage(F) ∩ {a₃} = {a₃} ≠ ∅

The from-endset is vital in d: π(F, d) ≠ ∅. Both π and locate are determined entirely by coverage(F) and the current M(d) (SV0).

*After removing a₃.* The net effect of removing a₃ from ran(M(d)) while satisfying D-CTG requires a composite: first a K.μ~ step rearranges d so that a₃ occupies the maximum V-position v₅, then a K.μ⁻ step removes v₅. (K.μ⁻ alone cannot remove an interior V-position — by D-SEQ, valid contractions remove from the maximum end of V_S(d) only.) The composite produces M'(d) with dom(M'(d)) = {v₁, v₂, v₃, v₄} and ran(M'(d)) = {a₁, a₂, a₄, a₅}. The specific mapping: M'(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅}:

- π(F, d) = coverage(F) ∩ ran(M'(d)) = {a₂, a₄} — reduced (SV3)
- locate(F, d) = {v₂, v₃} — since M'(d)(v₂) = a₂ and M'(d)(v₃) = a₄, both in coverage(F)
- discover_from({a₃}) = {b} — unchanged, because coverage(F) is invariant (L12, ASN-0043) and a₃ ∈ coverage(F) regardless of M(d) (SV8)

The endset remains vital but with reduced projection. The removal of a₃ from ran(M(d)) has split the endset's visible region into two maximal fragments. To see the decomposition of SV11: the post-removal arrangement has two mapping blocks — β₁ = (v₁, a₁, 2) covering {v₁, v₂} with I-extent {a₁, a₂}, and β₂ = (v₃, a₄, 2) covering {v₃, v₄} with I-extent {a₄, a₅}. With m = 1 (the single span (a₂, ℓ)) and p = 2 (the two blocks), there are m · p = 2 decomposition terms:

- ⟦(a₂, ℓ)⟧ ∩ I(β₁) = {t : a₂ ≤ t < a₅} ∩ {a₁, a₂} = {a₂}
- ⟦(a₂, ℓ)⟧ ∩ I(β₂) = {t : a₂ ≤ t < a₅} ∩ {a₄, a₅} = {a₄}

Each non-empty decomposition term coincides with a maximal fragment in this case, since each is a single-element contiguous ordinal subsequence and no two terms within the same block overlap. The fragment count equals the non-empty term count, equals m · p = 2. Together: π(F, d) = {a₂} ∪ {a₄} = {a₂, a₄}. ✓

Discovery through d still works for queries including a₂ or a₄. But discovery through the specific I-address set {a₃} — while still returning b (SV8) — no longer corresponds to anything visible in d, since a₃ ∉ ran(M'(d)). This illustrates the discovery-resolution distinction (SV10): the link is discoverable through a₃, but resolution of the from-endset in d yields no V-position for a₃.

*After reordering.* From the post-removal state, a K.μ~ step swaps v₂ and v₃: M''(d)(v₂) = a₄, M''(d)(v₃) = a₂ (with v₁ and v₄ unchanged). Since ran(M''(d)) = ran(M'(d)):

- π(F, d) = {a₂, a₄} — unchanged (SV5)
- locate(F, d) = {v₂, v₃} — the V-positions happen to be the same set, because the swap exchanges two V-positions that both belong to the locate set (both v₂ and v₃ map to I-addresses in coverage(F) before and after the swap)

Note: this worked example illustrates a special case where the locate *set* is preserved because the swap exchanges two V-positions that both belong to the locate set. In the general case, the locate set changes — see the witness in the SV5 discussion. The formal relationship locate_{Σ'}(F, d) = {ψ(v) : v ∈ locate_Σ(F, d)} holds here: ψ(v₂) = v₃ and ψ(v₃) = v₂, so {ψ(v₂), ψ(v₃)} = {v₂, v₃} = locate_Σ(F, d).

The projection is invariant under reordering; the resolution set transforms by the reordering bijection ψ.

*Cross-origin exclusion (SV6).* We now verify SV6 with explicit tumbler values. Let s = 1.0.1.0.1.0.1.2.3 — nine components; the zeros at positions 2, 4, 6 are field separators, so p₃ = 6. Let ℓ = 0.0.0.0.0.0.0.0.5 — action point k = 9 (the first nonzero component), and k = 9 > 6 = p₃. By TumblerAdd, positions 1 through 8 are copied from s, and position 9 advances: reach = s ⊕ ℓ = 1.0.1.0.1.0.1.2.8. We verify the sandwich: reach agrees with s on positions 1 through 8, confirming that the three field separators (positions 2, 4, 6) are preserved.

Consider t = 1.0.1.0.1.0.1.2.5. We have s ≤ t (agree on positions 1–8; at position 9, t₉ = 5 > 3 = s₉) and t < reach (agree on positions 1–8; at position 9, t₉ = 5 < 8 = reach₉). So t ∈ ⟦(s, ℓ)⟧. The field separators of t are at positions 2, 4, 6 — matching s — so origin(t) = 1.0.1.0.1 = origin(s). ✓

Now consider b = 1.0.1.0.2.0.1.2.5, a different-origin address with origin(b) = 1.0.1.0.2. We compare b with reach = 1.0.1.0.1.0.1.2.8: they agree on positions 1–4; at position 5, b₅ = 2 > 1 = reach₅. By T1(i), b > reach, so b ∉ ⟦(s, ℓ)⟧. The SV6 precondition k > p₃ ensures that the element-field action point cannot advance the document-prefix components: reach differs from s only at positions ≥ k = 9 > 6 = p₃, so no different-origin address can slip between s and reach. ✓


## Content Fidelity

The preceding analysis addresses the *extent* of what survives — how many I-addresses remain in the projection. We now address the *identity* of what survives: is the content at those addresses the same as when the link was created?

**Corollary (ContentFidelity, from S0, ASN-0036).** Content fidelity is guaranteed directly by the foundation: for every a ∈ dom(Σ.C) and every state transition Σ → Σ', a ∈ dom(Σ'.C) and Σ'.C(a) = Σ.C(a). We do not assign this a new SV label because it introduces no new content beyond S0 — it is S0 read for its survivability content. Applied to endset I-addresses: for any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k, `(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))` for every endset slot s. The survivability implication merits emphasis: whatever portion of the endset remains visible in a document's arrangement, the content at those I-addresses is *exactly* what was there when the link was created. No edit, no revision, no amount of rearrangement can alter the content the link references. The surviving fragment may be smaller than the original endset, but each byte in the fragment is identical to the original.

The guarantee is the strongest possible short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation.

The guarantee is architectural rather than cryptographic — there is no hash or signature that a client can verify independently. The guarantee rests on the structural property that the content store is append-only (S1, StoreMonotonicity) and values are frozen at allocation (S0). Nelson explicitly acknowledges this is contractual trust, not mathematical proof of non-tampering [LM 5/17–18].


## Weakest Precondition Analysis

The forward claims SV2–SV5 each have a natural reading as a *weakest precondition*. Given an elementary transition K and a postcondition R, write wp(K, R) for the weakest predicate on the pre-state such that R holds in every post-state reached by K. The wp form makes precise what the pre-state must guarantee for R to hold afterward — equivalently, what an editor would have to avoid in order not to falsify R. The forward claims SV2–SV5 give us each wp by direct rearrangement; we are recasting, not introducing new content. The "vitality loss condition" already developed in the SV3 discussion is essentially the wp of K.μ⁻ for non-vitality.

We take the postcondition R = "endset e remains vital in d after the transition", formally `π_{Σ'}(e, d) ≠ ∅`, and read off wp for each elementary transition. We restrict to non-empty endsets, as the empty case is degenerate (the section above).

- **wp(K.μ⁻, π(e, d) ≠ ∅) = `coverage(e) ∩ ran(M'(d)) ≠ ∅`.** Contraction preserves vitality iff at least one I-address in coverage(e) survives the contraction. The contrapositive — the *vitality loss* condition — is `coverage(e) ∩ ran(M'(d)) = ∅`, equivalent to `(A i : i ∈ coverage(e) ∩ ran(M(d)) :: i ∉ ran(M'(d)))`: the contraction removes every I-address that the endset shared with d's arrangement. This is Nelson's "if anything is left at each end" condition in formal dress.

- **wp(K.μ⁺, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ (∃ v, i : v ↦ i ∈ M' \ M ∧ i ∈ coverage(e))`.** Extension preserves vitality if it already held *or* if the extension introduces at least one I-address in coverage(e). For the typical case of an endset already vital before the extension, the first disjunct is satisfied and the wp reduces to the pre-state vitality.

- **wp(K.μ⁺_L, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ ℓ ∈ coverage(e)`** where ℓ is the link address added by the transition. For endsets whose coverage lies entirely in dom(Σ.C) (the typical content endset), the second disjunct is unreachable and the wp reduces to pre-state vitality.

- **wp(K.μ~, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`.** Reordering preserves ran(M(d)) (SV5), so the precondition is identical to the postcondition.

- **wp(K.α, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.δ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** (for any d carried over by the frame) and **wp(K.ρ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.λ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** for every pre-existing endset e. Each of these transitions preserves M in its frame, so π is unchanged for every endset that existed prior to the transition.

The aggregate observation: only K.μ⁻ can falsify vitality, and only by a specific characterized action — exhausting `coverage(e) ∩ ran(M(d))`. Every other elementary transition either trivially preserves vitality (M-frame: K.α, K.δ, K.λ, K.ρ, K.μ~) or can only enlarge the projection (K.μ⁺, K.μ⁺_L). The wp framework therefore localizes the *single* operation that places vitality at risk and gives the *exact* condition under which the risk materializes.

For discovery, the corresponding wp values follow the same pattern with discover_s in place of π. Because discover_s depends only on coverage(e) and dom(Σ.L), every transition that holds L in frame preserves discover_s pointwise:

- **wp(K, a ∈ discover_s(A)) = `a ∈ discover_s(A)`** for every K ∈ {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} and every fixed A. Discovery is invariant under arrangement and content operations.

- **wp(K.λ, a ∈ discover_s(A)) = `a ∈ discover_s(A) ∨ (a = a_new ∧ coverage(L_new.s) ∩ A ≠ ∅)`** where a_new is the newly allocated link address. K.λ can extend dom(L) by exactly one entry, so a previously-non-discoverable a becomes discoverable only when it is the newly allocated link and the new link's endset shares an I-address with A.

The discovery wp formalizes SV7–SV9: invariance under L-frame transitions, monotonic growth under K.λ, permanence (SV8) as wp instance for any K. Nothing new is established beyond the forward claims; the reformulation makes the *direction of dependency* explicit — for a postcondition concerning resolution or discovery, we can read off the corresponding pre-state requirement directly from the transition's frame.


## The Complete Guarantee

We can now synthesize the survivability guarantee into a single coherent statement.

**SV13 (SurvivabilityTheorem).** For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

(a) *The link persists:* a ∈ dom(Σ'.L) and Σ'.L(a) = (F, G, Θ). [L12]

(b) *Endset coverage is invariant:* coverage(F), coverage(G), coverage(Θ) are the same in Σ' as in Σ. [L12, ASN-0043]

(c) *Content at endset addresses is unchanged:* for every I-address i in any endset's coverage, Σ'.C(i) = Σ.C(i) when i ∈ dom(Σ.C). [S0, ASN-0036]

(d) *Discovery is permanent:* if a ∈ discover_s(A) in Σ for some fixed A, then a ∈ discover_s(A) in Σ'. [SV8]

(e) *Resolution is arrangement-dependent:*
- Extension of M(d) — whether K.μ⁺ (content subspace) or K.μ⁺_L (link subspace) — can only enlarge locate(e, d). [SV2]
- Contraction of M(d) can only shrink locate(e, d). [SV3]
- Reordering of M(d) preserves π(e, d); locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)} where ψ is the reordering bijection from K.μ~. The locate *set* may change. [SV5]
- Changes to M(d) cannot affect locate(e, d') for d' ≠ d. [SV4]
- K.α, K.δ, K.ρ preserve M in their frame, so locate(e, d) is unchanged for every existing endset e.
- K.λ (LinkAllocation) has a dual character. It preserves M in its frame (every existing v ↦ i mapping in M(d) for every d), so locate(e, d) is unchanged for every endset e that existed prior to the transition. But K.λ also adds a new entry to dom(L) — extending the link store by exactly one new link with endsets (F_new, G_new, Θ_new) — and the locate sets of those *new* endsets come into existence for the first time, evaluated against the unchanged M. Resolution for previously-existing endsets is invariant under K.λ; resolution for newly-created endsets is computed against the current M for the first time. Discovery exhibits the same duality: discover_s(A) is invariant under K.λ for any A that does not require the new link (a ∈ discover_s(A) in Σ implies a ∈ discover_s(A) in Σ'), and may gain a new member (the newly-allocated link) when coverage(L_new.s) ∩ A ≠ ∅. SV9 records the resulting monotonic growth of discover_s; SV7 captures invariance under every transition *except* K.λ.

(f) *Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field. [SV6]

*Remark (same-origin coverage growth).* Same-origin coverage growth depends on the allocation regime. At the byte level, sequential sibling allocation closes existing spans whose coverage is fully allocated (tight spans) to future sibling allocations; spans whose reach extends beyond the current allocation maximum remain open to sequential overshoot, and child-depth allocation (TA5(d) with k' > 0) can enter any span containing the parent address. At broader address levels, coverage growth is open by design. See the detailed analysis in the "Content Allocation and Coverage Stability" section.

(g) *Partial survival is well-structured:* the surviving text-subspace projection in any document is the union of m · p decomposition terms `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)`, equivalently the union of at most m · p maximal ordinal-contiguous fragments within mapping blocks (a cover, not necessarily a partition, due to non-injective arrangements). [SV11]

The survivability guarantee is therefore: the link, its endsets, and the content at its endset addresses are all permanent. What varies is the *visibility* of the endset content through each document's arrangement — and this variation is precisely characterised by the projection and resolution functions, which respond only to the arrangement of the specific document being queried and are immune to changes elsewhere.

Nelson's "strap between bytes" is exactly right. The strap (the link's endsets) is permanent, fastened to permanent bytes (I-addresses with immutable content). What moves is the string the bytes sit on — the document's Vstream arrangement. The strap follows the bytes, not the string.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| π(e, d) | Endset projection: `coverage(e) ∩ ran(M(d))` | introduced |
| locate(e, d) | Endset location: `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` | introduced |
| Vitality | Endset e is vital in d when `π(e, d) ≠ ∅` | introduced |
| BilateralVitality | Link is bilaterally vital in d when each non-empty content endset is vital in d | introduced |
| discover_s(A) | Link discovery: `{a ∈ dom(L) : coverage(L(a).s) ∩ A ≠ ∅}` | introduced |
| Decomposition term | `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` — one per (span, block) pair, contiguous in I(β_k)'s ordinal sequence | introduced |
| Maximal fragment | maximal contiguous ordinal subsequence within a single mapping block's I-extent | introduced |
| SV0 | NoStaleResolutionState: no state component external to (coverage(e), current M(d)) participates in resolution; caching of historical V-positions is structurally precluded by the link-store representation | introduced |
| ArrangementLinkFrame | Corollary of L12 (ASN-0043): arrangement changes preserve L entirely | cited |
| SV2 | ExtensionMonotonicity: K.μ⁺/K.μ⁺_L can only enlarge π(e, d) | introduced |
| SV3 | ContractionReduction: K.μ⁻ can only shrink π(e, d) | introduced |
| SV4 | ArrangementIsolation: arrangement changes to M(d) do not affect π(e, d') or locate(e, d') for d' ≠ d | introduced |
| SV5 | ReorderingProjectionInvariance: K.μ~ preserves π(e, d) exactly | introduced |
| SV6 | CrossOriginExclusion: allocations from a different document prefix cannot enter existing endset spans (within element field) | introduced |
| SV7 | TransclusionCouplingAbsence: `discover_s(A) in Σ' = discover_s(A) in Σ` for all L-preserving transitions (all except K.λ) — discovery is invariant, not merely monotonic | introduced |
| SV8 | DiscoveryPermanence: once discoverable through A, always discoverable | introduced |
| SV9 | DiscoveryMonotonicity: the discoverable set is non-decreasing as links are created | introduced |
| SV10 | DiscoveryResolutionIndependence: discovery and resolution answer different questions with different filters | introduced |
| SV11 | PartialSurvivalDecomposition: the text-subspace projection equals the union of m·p decomposition terms; the maximal fragment count is also bounded by m·p; the collection is a cover (not necessarily a partition) due to non-injective arrangements | introduced |
| ContentFidelity | Corollary of S0 (ASN-0036): content at endset I-addresses is immutable | cited |
| SV13 | SurvivabilityTheorem: synthesis of the complete guarantee | introduced |
| wp(K, R) | Weakest precondition reformulation of SV2–SV5: K.μ⁻ is the unique elementary transition whose wp for `π(e, d) ≠ ∅` is non-trivial; all other transitions preserve vitality definitionally | introduced |


## Open Questions

- What must the system guarantee about resolution when the same I-address appears at multiple V-positions within a single document through within-document sharing?
- Must the system provide a mechanism to transition a dormant link (vital in no document) back to vitality, and if so, what operation achieves this?
- What must the system guarantee about the ordering of fragments in a partially surviving endset — is there a canonical ordering that all implementations must respect?
- When two independent links share overlapping endset coverage, what invariants govern their independent partial survival under the same contraction?
- Must the system guarantee an upper bound on the number of fragments that a single endset can produce in any given document?
- What must the system guarantee about discovery latency — must newly created links be discoverable immediately, or is eventual consistency permitted?
- Under what conditions must bilateral vitality be preserved across a fork (version creation), given that the fork copies only a subset of the source's arrangement?
- What must the system guarantee about the relationship between a link's home document and the documents where its endsets are vital — can these be entirely disjoint?
