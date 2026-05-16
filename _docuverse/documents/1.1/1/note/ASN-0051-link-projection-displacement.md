# ASN-0051: Link Projection and Discovery Survivability

*2026-03-23*

*Editorial note (revision).* The original title "Link Projection Displacement" did not match the body, which formalises no "displacement" concept. The retitle "Link Projection and Discovery Survivability" reflects what the body actually develops — the survivability of a link's projection (where its endset content appears in a document's arrangement) and of its discovery (which links a content query reaches), under elementary state transitions. The inquiry's framing question — "what survives, what changes, and what can a link holder rely on?" — is the survivability question, and the SV-labelled claims throughout (SV2–SV11, SV13; SV0/SV1/SV12 withdrawn — see Properties Introduced) are the survivability properties. The filename `ASN-0051-link-projection-displacement.md` is retained for stability of external references and lattice paths.

We are looking for the invariants that govern what a link holder can rely on across state changes. A link has been created — its endsets are fixed (L12, LinkImmutability), its address is permanent (T8, AllocationPermanence). The endsets reference I-addresses in the content store, which is itself immutable (S0, ContentImmutability). So the link, structurally, is as permanent as anything in the system.

Yet the question of survivability is not about the link's *structure*. It is about the link's *utility*. A link is useful when its endpoints can be resolved to observable content in some document's current arrangement. Arrangements change — content is inserted, deleted, rearranged. What do these changes do to the link's observable behaviour?

The answer has two parts: a *discovery* question (can the link be found?) and a *resolution* question (can the link's endpoints be followed to visible content?). These are independent questions with independent answers. We develop each in turn.

*Notation.* Throughout the body, the symbol `+` between a tumbler and a nonnegative integer denotes the OrdinalShiftBase numeric shift from ASN-0058 (M-auxiliary): `a + k = shift(a, k)`, the k-th ordinal advance of a within its parent's sequence (TumblerAdd applied at the position of a's last nonzero component (position #a for T4-valid a); at k = 1 the result is the next sibling under a's prefix). The `⊕` symbol denotes TumblerAdd of a tumbler and a span-length: `s ⊕ ℓ` reaches the post-end of the span (s, ℓ). Component-wise natural-number addition on integers — e.g., `sₖ + ℓₖ` appearing inside TumblerAdd's definition — is written `+` as on ordinary numbers. The two `+` usages are disambiguated throughout by argument types: tumbler + integer is OrdinalShiftBase; integer + integer is natural-number addition.


## Endset Projection

To reason about survivability we need to formalize how a link's endsets relate to a document's current state. The link's endsets are sets of spans over I-addresses (L3, TripleEndsetStructure; L4, EndsetGenerality). A document's arrangement M(d) maps V-positions to I-addresses (ASN-0036). The question "what does this endset look like in document d right now?" has a precise answer.

**Definition — Endset Projection.** For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

This is the set of I-addresses that the endset references and that d currently contains in its arrangement. Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

**Definition — Endset Location.** For an endset e and document d, the *location* of e in d is:

`locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

These are the V-positions in d whose content is part of the endset.

**Definition — Resolution.** The *resolution* of endset e in document d is the function `locate(e, d)` — the set of V-positions in d whose content is part of e. Throughout this note, "resolution" names this function (and, by extension, the act of evaluating it); "projection" names π(e, d). The two answer different questions: resolution gives the positions a reader would see; projection gives the underlying content identities. Section titles and SV-claim names that refer to "resolution" (e.g., SV10 *DiscoveryResolutionIndependence*, SV13(e) "*Resolution is arrangement-dependent*") read this function-name definition, not an informal gloss.

The two are related by M(d)'s function property (S2, ArrangementFunctionality): for all v ∈ dom(M(d)), v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d). The restriction to dom(M(d)) is essential — M(d)(v) is undefined when v ∉ dom(M(d)), so the biconditional is well-formed only on this domain; and locate(e, d) ⊆ dom(M(d)) by definition, so no V-position outside dom(M(d)) is lost to the relation. Since M(d) need not be injective — within-document sharing is permitted (S5, UnrestrictedSharing) — we may have |locate(e, d)| ≥ |π(e, d)|. Multiple V-positions in d can show the same I-address, and a reader sees each occurrence.

**Definition — Text-Subspace Projection.** A document's arrangement may span more than one subspace (content under K.μ⁺, link under K.μ⁺_L; ASN-0047). For analyses that need the content-subspace contribution in isolation, define the *text-subspace projection* of e onto d:

`π_text(e, d) = coverage(e) ∩ ran_text(M(d))`

where `ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C}` is the content-subspace portion of M(d)'s range. Here s_C is the content-subspace identifier supplied by ASN-0047's K.μ⁺ amendment, and `subspace(v)` selects the subspace component of a V-position (ASN-0036, S8a). The text-subspace projection is a sub-projection of the full projection — `π_text(e, d) ⊆ π(e, d)` since `ran_text(M(d)) ⊆ ran(M(d))` by definition — with equality when ran(M(d)) carries no link-subspace addresses (the typical case for content-only arrangements). The block decomposition `ran_text(M(d)) = ⋃_k I(β_k)` used in the Partial Survival section is established there once B is in scope; the definition itself does not depend on B.

The architectural status of resolution state deserves explicit treatment. A naive implementation might intend to cache V-positions at link creation time, leaving stale entries when the document is rearranged. The schema precludes any such cache by three converging foundation facts.

*Schema closure (NoStaleResolutionState).* (i) *Link-store signature [L3, ASN-0043; K.λ, ASN-0047].* The link value Σ.L(a) = (F, G, Θ) stores I-space content only — endsets are sets of spans (s, ℓ) over T (L3, TripleEndsetStructure); no V-address, no per-document arrangement, no creation-time snapshot is recorded in the link value at allocation (K.λ). (ii) *State-schema closure [Σ = (C, L, E, M, R), ASN-0047].* M(d) is the *current* arrangement; no component carries a historical M_k. R holds per-mapping provenance over I-addresses only (J0/J1/J1★, ASN-0047), not over V-addresses. The schema admits no auxiliary V-cache field. (iii) *Operational closure [K = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}, ASN-0047].* No elementary transition writes a V-address into Σ.L, into a link value, or into any historical-M slot — direct inspection of each transition's effect (ASN-0047) confirms this. The per-transition checks, one line each: K.α modifies C only; K.δ modifies E and seeds M(d_new) = ∅; K.λ writes Σ.L(a_new) = (F, G, Θ), which by L3 (TripleEndsetStructure, ASN-0043) carries spans over T with no V-fields; K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ modify M only (and only at its current slot); K.ρ modifies R only. No transition writes into a link value, into a historical-M slot, or into any auxiliary V-cache field — there is consequently no operation that *could* establish a stale V-position field.

The structural conclusion: there is no field in which a stale V-position could persist, and no transition that could populate one. No state component external to (coverage(e), current M(d)) participates in resolution, because no such component exists in the schema. This is an *architectural* claim — a reading of the foundation schema rather than a transition-induced property — and is therefore not assigned an SV label.

*Functional consequence.* Definitionally, `locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` references only M(d) and the supplied endset, so `Σ₁.M(d) = Σ₂.M(d) ⇒ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)` is immediate from the definition; no L-equality precondition is required, since locate does not consult Σ.L. The resolution is always *fresh* — computed from the current state, with no creation-time arrangement participating. The architectural content above is what guarantees this definitional reading is not undermined by some schema field overlooked.

**Definition — Endset Vitality.** An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, locate(e, d) ≠ ∅.

*Scoping note.* For the remainder of this note we work within the standard-triple framework of ASN-0043: every link value is treated as Σ.L(a) = (F, G, Θ) — from-endset F, to-endset G, type-endset Θ — which is the arity-3 floor admitted by L3 (NEndsetStructure, ASN-0043). L3 admits higher-arity links with |Σ.L(a)| ≥ 3; treatment of those additional endset slots is deferred to ASN-0043. All claims below — slotwise vitality, bilateral vitality, SV2–SV13, the wp analysis — are stated for the standard triple; the generalisation to arity N > 3 follows the same projection/discovery machinery applied slot-wise, with content/type slot status determined by L3's slot-3 convention.

We define two related vitality predicates over a link's content endset slots — a liberal *slotwise* form that admits empty endsets vacuously, and a strict *bilateral* form that asserts visibility on both sides. The split avoids overloading the word "bilateral" with cases where one side is empty by construction.

A link at address a with Σ.L(a) = (F, G, Θ) is *slotwise vital in d* when each non-empty content endset is vital in d — every non-empty endset projects to at least one I-address in d's arrangement:

`F = ∅ ∨ π(F, d) ≠ ∅`   and   `G = ∅ ∨ π(G, d) ≠ ∅`

It is *bilaterally vital in d* when both content endsets are non-empty *and* each projects non-emptily — Nelson's "anything left at each end" condition read literally, with both ends required to exist:

`F ≠ ∅ ∧ π(F, d) ≠ ∅`   and   `G ≠ ∅ ∧ π(G, d) ≠ ∅`

Bilateral vitality is strictly stronger than slotwise vitality: every bilaterally vital link is slotwise vital, but a slotwise-vital link with one empty content endset (e.g., a link (∅, G, Θ) acting as a one-sided annotation on G) is not bilaterally vital. The two predicates coincide on the substantive case where both content endsets are non-empty — which is the case the survivability analysis below targets.

*Consumer note — bilateral vitality has no internal use in this ASN.* The SV claims below state per-side vitality conditions directly (e.g., `π(F, d) ≠ ∅`, `π(G, d) ≠ ∅`, `coverage(e) ∩ ran(M'(d)) = ∅`) rather than invoking BilateralVitality as a packaged predicate. We introduce the predicate here for downstream consumers — link-semantics ASNs and link-discovery policy notes that require the literal-Nelson reading "anything left at each end" demanding both ends to be non-empty *and* both to project — without forcing those consumers to re-derive the conjunction at use site. Internal proofs in this ASN therefore work with `π(e, d) ≠ ∅` slot-by-slot; readers tracking a strict bilateral guarantee should compose BilateralVitality from the slotwise SV2–SV5 conclusions per side.

*Exclusion of the type endset.* We exclude Θ from both vitality predicates for a semantic, not a structural, reason. L4 (EndsetGenerality, ASN-0043) permits any endset — including F and G — to reference any I-address, ghost or otherwise, so the mere admissibility of ghost addresses in Θ (codified separately as L9, TypeGhostPermission) does not by itself distinguish Θ from F or G. The distinction is the slot's *role*: F and G are endpoints — Nelson's "links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" [LM 4/43] — whose content visibility in d is what makes the link useful as a navigable connection. Θ is a type annotation — Nelson: "the system needs to apply a TYPE to a span, in order to associate it with a STAGE: the time of the user's history when that span appeared" [LM 4/44]; "all things stored in the docuverse are typed within it, by means of explicit assignments" [LM 4/45] — whose role is to classify the link's relationship rather than to be visible content at one of the link's ends. Each vitality predicate asks whether the link's endpoints are observable; Θ is not an endpoint, so its vitality is not part of either predicate. L9 explains why ghost references are *admissible* in type slots (the type hierarchy can be populated forward in time), but the exclusion of Θ from vitality rests on Θ's semantic role, not on L9's permission.

*Empty-endset cases.* Slotwise vitality is satisfied vacuously by F = ∅'s left branch when F is empty, and symmetrically for G. So a link (∅, ∅, Θ) — a pure type annotation — is *slotwise vital* in every document but is *not* bilaterally vital in any (both strict conjuncts F ≠ ∅, G ≠ ∅ fail); a link with exactly one empty content endset is slotwise vital iff its non-empty side projects, and is never bilaterally vital. This is the asymmetry the split records: slotwise vitality treats the empty endset as "no visibility claim to make on that side" and lets the predicate pass; bilateral vitality treats it as "no end to project," failing the literal-Nelson reading. The corresponding identities: for any endset e with coverage(e) = ∅, π(e, d) = locate(e, d) = ∅ in every d; for a link a with coverage(Σ.L(a).s) = ∅, a ∉ discover_s(A) for any A; and discover_s(∅) = ∅ in every state. The substantive analysis below concerns links with at least one non-empty content endset and non-empty query sets for discovery, so subsequent formulas omit empty-side conditions.

Nelson states the vitality condition as: "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" [LM 4/43]. Nelson's formulation presupposes something at each end to begin with — "if anything is left" implies there was something to leave. Bilateral vitality captures Nelson's reading literally — both ends are required to be non-empty, and each must project. Slotwise vitality captures the strictly weaker form usable in proofs that must also admit annotation-style links (one or both content endsets empty by construction) without case splits. The permanent existence of the endset spans in Σ.L is not in question; what is in question is whether those spans project to anything visible.


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

`(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d) ∧ locate_Σ(e, d) ⊆ locate_{Σ'}(e, d))`

Vitality is monotonically preserved: if an endset was vital in d before extension, it remains vital afterward. Extension can only *enlarge* the projection — introducing I-addresses that were in coverage(e) but not previously in ran(M(d)). It cannot remove any. The resolution conjunct says the same on the V-side: every pre-existing locate-position survives, and additional V-positions introduced by the extension may enter the locate set when their I-addresses lie in coverage(e).

*Projection.* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (L12, ASN-0043) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺/K.μ⁺_L effect — both transitions extend dom(M(d)) while preserving existing V↦I mappings, so the post-state range contains the pre-state range), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*Resolution.* Let v ∈ locate_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Both K.μ⁺ and K.μ⁺_L preserve existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))). So v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ locate_{Σ'}(e, d). New V-positions in dom(M'(d)) \ dom(M(d)) may additionally enter the locate set when their I-addresses lie in coverage(e). ∎

*Distinct architectural roles.* The two transitions enlarge different parts of ran(M(d)) and so contribute to different parts of π(e, d). For an endset e whose coverage lies entirely in dom(Σ.C) (the typical content endset, with spans over content I-addresses), only K.μ⁺ can strictly enlarge π(e, d) — the new I-address introduced by K.μ⁺_L is a link address in dom(Σ.L), disjoint from coverage(e). Conversely, for an endset whose coverage contains link addresses — permitted by L4 (EndsetGenerality) and the reflexive-addressing case of L13 (ReflexiveAddressing) — K.μ⁺_L can strictly enlarge π(e, d) while K.μ⁺ cannot reach those coverage members at all. The unified SV2 statement remains correct for both cases (the inclusion is reflexive when neither extension touches coverage(e)); the strictness of the inclusion depends on which subspace the endset references. We defer the detailed analysis of link-referencing endsets and reflexive addressing to the Link Subspace ASN; SV2 here captures the monotonicity that both transitions share without committing to a particular subspace.


### Contraction May Reduce

Arrangement contraction (K.μ⁻, ArrangementContraction) removes V→I mappings from M(d). Therefore ran(M'(d)) ⊆ ran(M(d)), and:

**SV3 (ContractionReduction).**

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d) ∧ locate_{Σ'}(e, d) ⊆ locate_Σ(e, d))`

*Projection.* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (L12, ASN-0043) and ran(M'(d)) ⊆ ran(M(d)) (K.μ⁻ restricts the domain while preserving values), we have coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

Contraction can only *shrink* the projection. If the contraction removes all V-positions whose I-addresses are in coverage(e), then π_{Σ'}(e, d) = ∅ and the endset loses vitality in d. This is the mechanism by which editing can degrade a link's utility in a specific document.

The vitality loss condition is:

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

Nelson's survivability condition — "if anything is left at each end" — is precisely the negation of this: as long as at least one I-address from the endset remains in d's arrangement, the endset survives in d.

*Resolution.* Let v ∈ locate_{Σ'}(e, d). Then v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), we have v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ locate_Σ(e, d). ∎


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

Rearrangement cannot change which I-addresses are in the projection. The endset references exactly the same content before and after. What changes is *where* that content appears. Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). By K.μ~-FIX (ASN-0047), ψ acts on a *fixed* V-position arena — dom(M'(d)) = dom(M(d)) — and acts *within* each subspace partition, so for every v ∈ dom(M(d)), subspace(ψ(v)) = subspace(v); only the V↦I assignment is permuted, not the V-position domain or its subspace structure. The formal relationship is:

`locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`

*Proof.* v' ∈ locate_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e). By K.μ~-FIX, dom(M'(d)) = dom(M(d)) and ψ is a bijection on this common domain (subspace-respecting), so every v' ∈ dom(M'(d)) equals ψ(v) for a unique v ∈ dom(M(d)), and M'(d)(ψ(v)) = M(d)(v). So M'(d)(v') ∈ coverage(e) iff M(d)(v) ∈ coverage(e) iff v ∈ locate_Σ(e, d). ∎

*Composite-level scope of SV5.* K.μ~ is a *distinguished composite* in ASN-0047, not an elementary transition: when dom_C(M(d)) ≠ ∅ it expands into two consecutive elementary steps K.μ⁻ + K.μ⁺, each satisfying its own precondition at the respective intermediate state. Between Σ and Σ', therefore, there is an intermediate state Σ_int in which K.μ⁻ has executed but K.μ⁺ has not. At Σ_int we have `ran(M_int(d)) ⊊ ran(M(d))`, so π_{Σ_int}(e, d) ⊆ π_Σ(e, d) by SV3 and the inclusion may be strict (the K.μ⁻ stage of K.μ~ removes the source V-position(s) of the permutation before the K.μ⁺ stage rewrites the target with the moved I-address). The K.μ⁺ stage then satisfies SV2 against Σ_int, restoring ran(M'(d)) = ran(M(d)) and recovering π_{Σ'}(e, d) = π_Σ(e, d). SV5's stated equality is therefore the *composite-level* π-invariance at K.μ~'s endpoints (Σ and Σ' bracketing the full composite); per-step π is not claimed to be invariant — it shrinks at the K.μ⁻ midpoint and recovers at the K.μ⁺ endpoint. Composite-level discovery (SV7) is similarly recovered at endpoints, since both K.μ⁻ and K.μ⁺ are L-frame and L-frame composes; the intermediate state is L-frame-equivalent throughout.

In general, locate_{Σ'}(e, d) ≠ locate_Σ(e, d) as sets. *Witness:* let dom(M(d)) = {v₁, v₂} with M(d) = {v₁ ↦ a₁, v₂ ↦ a₂}, and let coverage(e) = {a₁} (so locate_Σ(e, d) = {v₁}). The swap ψ(v₁) = v₂, ψ(v₂) = v₁ gives M'(d) = {v₁ ↦ a₂, v₂ ↦ a₁}, so locate_{Σ'}(e, d) = {v₂} ≠ {v₁}. The locate set changes whenever ψ maps a V-position inside the locate set to one outside it, or vice versa.

This is the precise sense in which links "track content, not location." The strap-between-bytes metaphor (Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" [LM 4/42]) expresses this property: rearranging the beads on the string doesn't alter which beads the strap holds, only where they sit.


### Content Allocation and Coverage Stability

Content allocation (K.α, ContentAllocation) creates a new I-address a ∉ dom(Σ.C). Its frame holds M constant: `(A d :: M'(d) = M(d))`. So π and locate are trivially unchanged by K.α itself.

The deeper question is: could a newly allocated I-address fall within the coverage of an existing endset? If so, a subsequent K.μ⁺ mapping a V-position to this address would enlarge the endset's projection — the endset would appear to absorb new content never part of the original link.

The answer depends on the allocation regime and the address hierarchy. We establish what is provable and identify where the answer is level-dependent.

**SV6 (CrossOriginExclusion).** For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Precondition.*
- `s, b ∈ T`
- `(s, ℓ)` is T12-well-formed (T12, SpanWellDefinedness, ASN-0034: `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`)
- `zeros(s) = 3 ∧ zeros(b) = 3`
- `s, b` are T4-valid
- `origin(b) ≠ origin(s)`
- `k > p₃`, where `k = actionPoint(ℓ)` and `p₃` is the position of the third zero component in s

*Note on "newly allocated".* The formal claim is structural: the precondition list above contains no allocation requirement, and the conclusion `b ∉ ⟦(s, ℓ)⟧` holds for any T4-valid element-level b with `origin(b) ≠ origin(s)`, regardless of whether b ∈ dom(Σ.C). The phrase "newly allocated" in the informal statement names the typical application context — K.α producing a fresh I-address whose origin differs from an existing span's start (as used in the CrossDocumentDecoupling witness below) — not a precondition of the claim.

Equivalently, the last condition `k > p₃` says the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`. This places the action point within the element field — beyond all three field separators.

T4-validity is the conjunction of the conditions in T4 (HierarchicalParsing, ASN-0034); it is required so that the projections N(s), U(s), D(s), N(b), U(b), D(b) are well-defined, and consequently `origin(s) = N(s).0.U(s).0.D(s)` and `origin(b) = N(b).0.U(b).0.D(b)` are well-defined (per the origin definition in ASN-0036, which presupposes T4-valid element-level arguments). The element-level depth condition `zeros(s) = zeros(b) = 3` places each address in the element field per T4b (UniqueParse, ASN-0034). L4 (EndsetGenerality, ASN-0043) permits non-element-level span starts, but the origin-based exclusion stated by SV6 applies only when the start is a T4-valid element-level tumbler.

*Proof.* Let k be the action point of ℓ, with k > p₃ as stated. By TumblerAdd, components before k are copied from s, and (s ⊕ ℓ)ₖ = sₖ + ℓₖ, so s and s ⊕ ℓ agree on positions 1 through k−1. Consider any t with s ≤ t < s ⊕ ℓ.

*Sub-lemma (no early divergence).* t cannot first diverge from s at any position j < k. Suppose for contradiction that the first position where tⱼ ≠ sⱼ is some j with j < k.

*Prefix exclusion (#t ≥ j, so T1(i) applies).* T1(i) requires both t and s to have a component at position j. Span well-formedness (ASN-0034, span precondition `actionPoint(ℓ) ≤ #s`) gives k ≤ #s, so j < k ≤ #s and sⱼ is well-defined. For tⱼ, suppose for contradiction that #t < j. Then t and s agree on every position 1 through #t (because j is the *first* position of divergence and #t < j), and #t < j ≤ #s, so t is a proper prefix of s. By T1(ii) (a proper prefix is strictly less in the lex order), t < s — contradicting s ≤ t. Hence #t ≥ j, so tⱼ is well-defined.

*Divergence is upward.* Since t ≥ s and t agrees with s on positions 1 through j−1, T1(i) gives tⱼ > sⱼ. By TumblerAdd, (s ⊕ ℓ)ⱼ = sⱼ for j < k. Since t agrees with s on positions 1..j−1 (first divergence at j) and s ⊕ ℓ agrees with s on positions 1..k−1 (TumblerAdd with k as action point), and j−1 < k−1, t agrees with s ⊕ ℓ on positions 1..j−1. So the first divergence of t and s ⊕ ℓ is at position j with tⱼ > sⱼ = (s ⊕ ℓ)ⱼ. Since k = actionPoint(ℓ) ≤ #ℓ (ActionPoint codomain bound) and `#(s ⊕ ℓ) = #ℓ` (TA0 result-length), j < k gives j < #(s ⊕ ℓ), so position j is within range for s ⊕ ℓ as well — T1(i) applies symmetrically. By T1(i), t > s ⊕ ℓ — contradicting t < s ⊕ ℓ. □

The two structural conclusions follow as parallel applications of the sub-lemma:

(a) *#t ≥ k.* Suppose #t < k. Then the sub-lemma excludes any first-divergence at j ≤ #t < k, so t agrees with s on all positions 1 through #t — making t a proper prefix of s, hence t < s by T1(ii), contradicting s ≤ t.

(b) *t agrees with s on positions 1 through k−1.* The sub-lemma's hypothesis ("the first position where tⱼ ≠ sⱼ is some j with j < k") presupposes that *some* position of divergence exists, i.e., t ≠ s. So we split:
- *t = s.* Trivially, t agrees with s on every position, in particular on positions 1 through k−1.
- *t ≠ s.* Then t has a first position of divergence from s. If that position lay in [1, k−1], it would be a first divergence at some j < k — excluded by the sub-lemma. So the first position of divergence lies at or beyond k, and t agrees with s on positions 1 through k−1.

In either case, t agrees with s on positions 1 through k−1.

Since k > p₃, the first k−1 positions of t include all three field-separator positions of s — call them p₁, p₂, p₃ (the positions where sᵢ = 0). Because t agrees with s on positions 1 through k−1, we have t_{p₁} = t_{p₂} = t_{p₃} = 0, so t has at least three zero components, all located within positions 1 through k−1: zeros(t) ≥ 3, with at least three zeros at positions p₁, p₂, p₃.

*Restricting to element-level t.* For element-level t — those with zeros(t) = 3 — the inequality is tight. The three zeros at p₁, p₂, p₃ already account for all zero components of t, so t has *exactly* three zeros and they sit at exactly the positions p₁, p₂, p₃. In particular, no zero component lies at any position j with k ≤ j ≤ #t — every component beyond position k − 1 is nonzero.

*T4-validity of t.* The origin function `origin(t) = N(t).0.U(t).0.D(t)` (ASN-0036, S7) presupposes that t is T4-valid — no adjacent zeros, t₁ ≠ 0, t_#t ≠ 0 (T4, ASN-0034). We verify each conjunct from properties established above:
- *t₁ ≠ 0.* Position 1 lies in [1, k − 1] (since k > p₃ ≥ 6, so k ≥ 7 ≥ 2). (`p₃ ≥ 6` follows from T4-validity of s: `s₁ ≠ 0` gives `p₁ ≥ 2`, no adjacent zeros gives `p₂ ≥ 4` and `p₃ ≥ 6`.) Conclusion (b) gives t₁ = s₁, and s is T4-valid, so t₁ = s₁ ≠ 0.
- *t_#t ≠ 0.* By conclusion (a), #t ≥ k, so position #t lies in [k, #t] — the element-field range. Every component in that range is nonzero (since the three zeros of element-level t are confined to p₁, p₂, p₃ ≤ k − 1), so t_#t ≠ 0.
- *No adjacent zeros.* Positions 1 through k − 1 inherit s's no-adjacent-zeros property since t agrees with s on that range (conclusion (b)) and s is T4-valid. Positions k through #t are all nonzero, so no pair of adjacent positions in [k, #t] is doubly zero. The only remaining boundary is the pair (k − 1, k): if t_{k−1} = 0 — i.e., k − 1 is one of p₁, p₂, p₃ — then t_k lies in the element field and is nonzero, so the pair is not doubly zero. Among the three cases k − 1 ∈ {p₁, p₂, p₃}, only k − 1 = p₃ is possible, since k > p₃ > p₂ > p₁ forces k − 1 ≥ p₃; the live boundary case is therefore the single one in which position k − 1 is the third field separator and position k is the first component of the element field.

So t is T4-valid, and origin(t) is well-defined. The field decomposition of t — the partition of its components by the three field-separator positions p₁, p₂, p₃ — matches the field decomposition of s component-by-component up to position p₃. The first three fields (node, user, document) of t are identical to those of s, so origin(t) = N(t).0.U(t).0.D(t) = N(s).0.U(s).0.D(s) = origin(s) (per the origin definition in ASN-0036, S7).

Since b is element-level by the SV6 precondition (`zeros(b) = 3`, supplied directly by the precondition rather than by appeal to S7b — S7b's `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` characterises content-store entries specifically, but SV6 makes no `b ∈ dom(Σ.C)` assumption and the conclusion holds for any T4-valid element-level b), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s), the contrapositive gives: any element-level b with origin(b) ≠ origin(s) satisfies b ∉ ⟦(s, ℓ)⟧. ∎

*Note.* T5 gives the weaker result origin(s) ≼ t for every t in the interval, but this prefix containment does not force separator positions to align — the sandwich argument above establishes the stronger claim.

*Note on scope — what k ≤ p₃ permits.* The precondition k > p₃ is not a technical artifact of the proof; it tracks a structural feature of the tumbler field layout that the proof relies on. When k ≤ p₃, the action-point lies at or before the third field separator, so reach = s ⊕ ℓ can advance a component within s's document-prefix — placing reach in a different prefix-field configuration from s, with the interval [s, reach) covering tumblers whose own document-prefix components differ from those of s. Such tumblers have different origin values, and SV6's exclusion does not apply to them. This is by design: Nelson's docuverse admits spans whose endpoints lie at server, account, or document field positions, with the interval implicit between them — "There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25] — so that a span "may range in possible size from one byte to the whole docuverse on the whole network" [LM 4/24]. A k ≤ p₃ span is the formal vehicle for broader-level coverage: the same span machinery, applied with an action-point inside the document-prefix region rather than within the element field, yields the cross-document, cross-account, or cross-node reach that the design contemplates. The boundary at k = p₃ — between element-field action-points (covered by SV6) and document-prefix-or-earlier action-points (broader-level spanning) — is *structurally consequential but not nominally designated* in Nelson's writing. It emerges from the field structure (four fields separated by three major dividers, with the third divider at position p₃ between Document and Element [LM 4/26, LM 4/28]) rather than being introduced by Nelson as a named action-point boundary; the boundary is a consequence of the field layout, not a stipulation about where action-points may sit. Detailed treatment of broader-level spans is deferred to ASN-0034's allocator and address-hierarchy machinery.

This property is robust — it depends only on the structural separation of document-level prefixes, not on any allocation discipline.

**Same-origin coverage growth.** Under the same document prefix, two mechanisms can place a new I-address within an existing endset span's denotation. *Scope.* We make no formal SV claim about same-origin coverage growth in this ASN. The analysis below is descriptive: it identifies the mechanisms (sequential overshoot, child-depth entry) by which TA5 and T10a allocations can enter existing endset coverage under a shared document prefix, but the precise allocator-discipline conditions that determine *which* same-origin allocations enter *which* spans are deferred to the allocator-discipline treatment in ASN-0034. The descriptive content here motivates the SV6 formal exclusion at element-level depth from cross-origin allocations and clarifies why endset coverage stability is *architectural*, not definitional.

*Sequential overshoot.* If a span's reach extends beyond the current allocation maximum — i.e., the span references addresses not yet allocated — future sibling allocations (TA5(c)) will enter the span as they advance through the ordinal sequence. This is the mechanism by which type endsets referencing ghost addresses (L9, TypeGhostPermission) acquire content: a link whose type endset spans a range in the type hierarchy will match future type addresses as they are allocated within that range.

*Child-depth entry.* The allocator discipline (T10a) permits child-spawning — inc(t, k') with k' > 0 — to create addresses at greater tumbler depth. By the prefix rule (T1 case (ii)), a child-depth address c produced by inc(t, 1) satisfies t < c < t+1, because t is a proper prefix of c (case (ii) gives t < c) and c and t+1 diverge at the position where c has a value less than (t+1)'s (case (i) gives c < t+1). If an endset span contains t and has reach ≥ t+1, the child-depth address c falls within the span. Crucially, when k' = 1, the result has zeros(c) = zeros(t) — the appended component is nonzero (set to 1 by TA5(d)), so no new field separator is introduced, and c remains a valid element-level tumbler (T4 preserved).

*Counterexample to a universal exclusion claim.* Suppose a document D allocates element-level content at ordinals a₁ < a₂ < ... < aₙ, all of the same tumbler length. A link is created with an endset span (a₁, ℓ) where the reach a₁ ⊕ ℓ = aₙ + 1 (one ordinal step beyond the last allocation). If the allocator later spawns a child via inc(aₙ, 1) = c, then c is element-level (zeros(c) = 3) and has origin(c) = origin(a₁) = D. We verify the sandwich aₙ < c < aₙ + 1 = a₁ ⊕ ℓ by explicit divergence positions. Let n = #aₙ. By TA5(d), inc(aₙ, 1) appends a single component 1 at position n + 1, so c agrees with aₙ on positions 1 through n and has c_{n+1} = 1, with #c = n + 1. Since aₙ is a proper prefix of c (c extends aₙ by one position), T1(ii) gives aₙ < c. For the upper inequality, aₙ + 1 = shift(aₙ, 1) is the next sibling under aₙ's prefix: by OrdinalShiftBase (ASN-0058), since aₙ is T4-valid and element-level its last component aₙ_n is nonzero, so the action point of + 1 sits at position n, and (aₙ + 1)_n = aₙ_n + 1 with the prefix on positions 1..n−1 copied from aₙ; #(aₙ + 1) = n. The two tumblers c and aₙ + 1 first diverge at position n: positions 1..n−1 agree (both copy aₙ's prefix), and c_n = aₙ_n < aₙ_n + 1 = (aₙ + 1)_n. T1(i) — both have a component at position n, prior positions agree, and c_n < (aₙ + 1)_n — gives c < aₙ + 1. So c ∈ ⟦(a₁, ℓ)⟧ — the newly allocated address falls within the existing endset's coverage.

**The architectural resolution.** Nelson's design distinguishes these levels explicitly. At the byte level within a document, content allocation is sequential and append-only — new bytes get the next ordinal position in the Istream: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14]. The "strap between bytes" is effectively closed to future allocations as an architectural consequence of this sequential discipline. Gregory's implementation in udanax-green operates byte-level text allocation in two regimes (via `findisatoinsertmolecule`, `granf2.c:165-167`): the *steady-state regime* uses sibling increment (`tumblerincrement(..., rightshift=0, 1, ...)`) to produce strictly monotonic same-length addresses that cannot enter a tight span over previously allocated content; and a *first-insertion regime* — when content is first written into a freshly created document with no prior allocations — uses two child-depth increments (rightshift=2 then rightshift=1) to descend into the element field and seed the first ordinal position. Once the first-insertion bootstrap is complete, all subsequent text allocation under that document prefix is sibling increment, and the steady-state closure property applies. The first-insertion case does not contradict the closure: it occurs before any span over that prefix could exist, since the link's endset spans presuppose addresses that the link can reference, and those addresses are themselves the product of the bootstrap.

At broader address levels — documents, accounts, servers — Nelson explicitly designs for coverage growth: "A span that contains nothing today may at a later time contain a million documents" [LM 4/25]. Links to accounts and nodes find "any of the documents under it" [LM 4/23], including documents not yet created. This is not a deficiency but a feature: ghost elements and hierarchical spanning are fundamental to the design. The intended discipline is *owner-gated append-only growth* within the prefix region — new documents under an account, new accounts under a node — governed by the baptism rule of the responsible allocator, so that broader-level span coverage grows monotonically as new entries are baptised under existing prefixes.

*Scope — broader-level spans are admitted but not formally characterised here.* This ASN makes no SV claim about broader-level spans (spans with action point at or before p₃, reaching across document, account, or node prefixes). Three reasons: (1) the survivability analysis below applies symmetrically — coverage is invariant, projection is determined by ran(M(d)) ∩ coverage(e), and the SV2/SV3/SV4/SV5/SV11 forms carry through unchanged for any endset — so no new claim is required to extend the analysis to broader spans. (2) The cross-origin exclusion SV6 explicitly does *not* hold at broader levels by design: a broader span over a document prefix admits future child-document allocations under that prefix, so the exclusion structure that closes element-level spans against cross-origin growth is replaced by an opt-in growth structure governed by the allocator. The allocator-discipline conditions for *which* prefix-level allocations land within *which* broader spans are the proper subject of ASN-0034's address-hierarchy treatment, not this ASN. (3) udanax-green does *not* implement broader-level spans: the span value carries only stream and width tumblers (no level or action-point field), and the address representation uses only mantissa[0] (identity/type) and mantissa[1] (character offset), with mantissa[2+] declared but dead in the allocator and span machinery. The udanax codebase therefore offers no implementation-side evidence for broader-level span survivability beyond the SV6 element-level treatment given here; a future implementation that activates broader-level spans would require the survivability analysis to be re-stated against the prefix-region allocator discipline of that implementation. Subject to these scope limits, the projection and discovery machinery developed here applies term-for-term to any endset (L4, EndsetGenerality), broader-level or element-level alike.

The survivability implication: **endset coverage stability is architectural, not definitional.** The coverage *set* is fixed forever (L12, ASN-0043). What varies is whether that fixed set intersects the growing set of allocated I-addresses — and this intersection can only grow (S1, StoreMonotonicity), never shrink. At the byte level, the intersection is typically closed at creation because sequential allocation ensures new addresses fall beyond existing spans; at broader levels, the intersection is open by design, enabling links that discover future content.


## Link Discovery

We have established what happens to a link's *resolution* under state changes. The other half of survivability concerns *discovery*: finding which links relate to given content.

**Definition — Link Discovery.** For a set of I-addresses A ⊆ T and an endset slot s ∈ {from, to, type}, define:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

This is the set of links whose endset at slot s shares at least one I-address with A. Note that partial overlap suffices — a single shared I-address is enough to discover the link.

In practice, the query set A is derived from a document's arrangement: a reader examines some V-region of document d, the system converts those V-positions to I-addresses via M(d), and then searches for links whose endsets intersect those I-addresses. But the discovery function itself is defined purely in I-space, independent of any particular document.

**Definition — Discovery Through a Document.** When the query set A is taken to be the I-addresses currently provided by document d's arrangement, define the *document-derived discovery set*:

`discover_through_s(d) = discover_s(ran(M(d)))`

— the set of links whose slot-s endset shares at least one I-address with d's current arrangement. This is the document-derived specialisation of discover_s. The argument is the *current* ran(M(d)), so unlike discover_s(A) on a fixed A — which is permanent by SV8 below — discover_through_s(d) varies with M(d): K.μ⁺/K.μ⁺_L can enlarge it (SV2 applied to coverage(e) for each link e), and K.μ⁻ can shrink it (the link's contributing I-addresses may leave ran(M(d))).

*Domain of A.* The query domain is the full I-space T, not the content subspace alone. L4 (EndsetGenerality, ASN-0043) admits any I-address in any endset, and L13 (ReflexiveAddressing, ASN-0043) explicitly licenses link addresses as endset members; correspondingly K.μ⁺_L (LinkSubspaceExtension, ASN-0047) places link addresses into ran(M(d)), so an A derived from a document's arrangement may legitimately contain link addresses when the arrangement spans the link subspace. Restricting A to dom(Σ.C) would exclude the reflexive-addressing case by definition rather than by argument, and would render discover_s partial on inputs the rest of the schema admits. The wider domain leaves SV7–SV9 and the K.μ⁺ transclusion corollary stated below unchanged — each is established for arbitrary fixed A — and is consistent with every concrete A used in this note (each is a subset of dom(Σ.C) ⊆ T).

We observe that discover_s is defined purely as a function of an I-address set — it is parameterised by I-addresses, not by document-V-region pairs. So identical I-address sets trivially yield identical discovery results. The interesting consequence is not this definitional fact but the *discovery invariance under L-frame transitions* it entails — and, as a corollary, the *transclusion discovery guarantee* that follows from instantiating that invariance to K.μ⁺.

**SV7 (DiscoveryInvarianceUnderLFrame).** For every transition Σ → Σ' that holds L in frame — every L-frame elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) and the distinguished composite K.μ~ — and for every fixed set of I-addresses A:

`discover_s(A) in Σ' = discover_s(A) in Σ`

*Proof.* Each L-frame transition holds dom(L') = dom(L) and L'(a) = L(a) for all a ∈ dom(L). For the elementaries this is direct (per-transition effect, ASN-0047); for the distinguished composite K.μ~ it follows because both constituents K.μ⁻ and K.μ⁺ hold L in frame, so their sequential composition does. Therefore coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) for every a ∈ dom(Σ.L), and dom(Σ'.L) = dom(Σ.L). Both inputs to discover_s — coverage and dom(L) — are identical in Σ and Σ', so the discovery sets are equal. ∎

The claim is an equality, not merely monotonicity: no L-frame transition introduces new discovery relationships and none removes any. The discovery mechanism itself — discover_s operating on coverage and dom(L) — is coupling-free under L-frame: the link store is untouched, and the I-address inputs to coverage are fixed by L12. The only elementary transition that can change discover_s is K.λ, which adds a new link to dom(L) and yields the strict inclusion recorded in SV9. (K.μ~ is a distinguished composite of K.μ⁻ + K.μ⁺, both L-frame, hence L-frame itself; the elementary/composite distinction does not affect the L-frame-induced invariance.)

*Corollary (TransclusionCouplingAbsence).* When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself. The argument distinguishes two different address-set arguments to discover_s, the *fixed-A* invariance carried by SV7 and the *document-derived* set that changes with the arrangement:

- *Fixed-A invariance (SV7).* For every fixed I-address set A, discover_s(A) evaluated in Σ' equals discover_s(A) evaluated in Σ. In particular, discover_s({a}) in Σ' = discover_s({a}) in Σ — call this set L_a, the set of links whose slot-s endset covers a. L_a was already determined in Σ; K.μ⁺ does not alter it.

- *Document-derived set change.* The address set d₂ contributes to discovery is A_{Σ}(d₂) = ran(Σ.M(d₂)) in Σ and A_{Σ'}(d₂) = ran(Σ'.M(d₂)) = A_{Σ}(d₂) ∪ {a} in Σ'. These are *different* sets — the transition extends d₂'s contributed addresses by {a}. Discovery through d₂ in Σ' is discover_s(A_{Σ'}(d₂)) = discover_s(A_{Σ}(d₂) ∪ {a}), which by set-theoretic distribution of discover_s over union equals discover_s(A_{Σ}(d₂)) ∪ discover_s({a}) = discover_s(A_{Σ}(d₂)) ∪ L_a.

The inheritance is therefore: d₂ in Σ' discovers everything it already discovered in Σ, plus exactly L_a — the link set that was already discoverable through a in Σ (e.g., via d₁, which had a in its arrangement). No link-store operation participates; the new discovery membership is supplied entirely by the K.μ⁺ extension of d₂'s arrangement together with the pre-existing coverage of L_a. The same reasoning applies to forking (J4): the new version's arrangement extension by K.μ⁺ provides the shared addresses, and discovery through the new version inherits L_a for each shared a without explicit link propagation. (A valid composite transition containing K.μ⁺ may additionally require K.ρ to satisfy J1★ (ExtensionRecordsProvenanceContent, ASN-0047), but K.ρ modifies R only — it does not alter L or M, so the discovery argument above is unaffected; SV7 covers K.ρ directly as one of the L-frame transitions.)

**SV8 (DiscoveryPermanence).** For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

Once a link is discoverable through a set of I-addresses, it remains discoverable through that set in all subsequent states.

Proof: a ∈ discover_s(A) means coverage(Σ.L(a).s) ∩ A ≠ ∅. By L12, a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a). So coverage(Σ'.L(a).s) = coverage(Σ.L(a).s), and the intersection with A is unchanged. ∎

*Caveat — document-derived discovery is not permanent.* SV8 quantifies over a fixed I-address set A; the document-derived specialisation discover_through_s(d) = discover_s(ran(M(d))) is not preserved across arrangement edits, because its argument ran(M(d)) is not fixed. Formally: under a K.μ⁻ transition Σ → Σ' on d, `discover_through_s(d) in Σ' ⊆ discover_through_s(d) in Σ` (SV3 applied to coverage(Σ.L(a).s) for each link a), and the inclusion is strict whenever the contraction removes the last V-position contributing an I-address in some link's endset coverage. A link a that exits discover_through_s(d) in this way remains in discover_s(A) for the unchanged A (by SV8 on the fixed I-address set whose membership SV8 records), and remains in discover_through_s(d') for any other document d' whose current arrangement still maps a contributing I-address.

**SV9 (DiscoveryMonotonicity).**

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

for any fixed A. *Proof.* The inclusion has two sources, corresponding to the two ways the membership of discover_s(A) can change across Σ → Σ':

- *Existing discoverers persist [SV8, equivalently L12].* For every a ∈ discover_s(A) in Σ, SV8 (DiscoveryPermanence) gives a ∈ discover_s(A) in Σ'. Equivalently, L12 (LinkImmutability, ASN-0043) preserves Σ.L(a) entry-by-entry — Σ'.L(a) = Σ.L(a) — so coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) and its intersection with A is unchanged, retaining a in discover_s(A).

- *New discoverers may join via link allocation [L12a].* L12a (LinkStoreMonotonicity, ASN-0043) admits dom(Σ'.L) ⊇ dom(Σ.L); any newly allocated link a_new ∈ dom(Σ'.L) \ dom(Σ.L) whose endset at slot s shares an I-address with A enters discover_s(A) in Σ'. Only K.λ realises this dom-growth — every other elementary transition is L-frame (SV7) and adds no new link addresses.

The two parts together: existing entries are preserved by the value-preservation half (SV8/L12), and any new entries are introduced only by the dom-growth half (L12a). The discoverable set is therefore monotonically non-decreasing in the link population. ∎

**SV14 (DocumentDerivedDiscoverySurvivability).** The document-derived specialisation `discover_through_s(d) = discover_s(ran(M(d)))` inherits the projection-style survivability of SV2–SV4 per-link, with the non-permanence already noted as the caveat above promoted to a labelled witness clause:

(a) *Monotonicity under extension.* `(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', d, s :: discover_through_s(d) in Σ ⊆ discover_through_s(d) in Σ')`. *Proof.* K.μ⁺/K.μ⁺_L satisfy `ran(Σ.M(d)) ⊆ ran(Σ'.M(d))` (per the extension effect, ASN-0047). For every a ∈ discover_through_s(d) in Σ, coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ≠ ∅, so by L12 (coverage invariance) coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ⊇ coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ≠ ∅, giving a ∈ discover_through_s(d) in Σ'. ∎

(b) *Reduction under contraction.* `(A Σ →_{K.μ⁻} Σ', d, s :: discover_through_s(d) in Σ' ⊆ discover_through_s(d) in Σ)`. *Proof.* K.μ⁻ satisfies `ran(Σ'.M(d)) ⊆ ran(Σ.M(d))` (per the contraction effect, ASN-0047). For every a ∈ discover_through_s(d) in Σ', coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ≠ ∅, so by L12 coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ⊇ coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ≠ ∅, giving a ∈ discover_through_s(d) in Σ. ∎

(c) *Cross-document isolation.* `(A Σ →_{K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~} Σ', d, d', s : d ≠ d' :: discover_through_s(d') in Σ' = discover_through_s(d') in Σ)`. *Proof.* All four transitions hold M(d') in frame for d' ≠ d (per their frame conditions, ASN-0047); together with L12 (coverage invariance) the two inputs to discover_s — coverage and ran(M(d')) — are unchanged across Σ → Σ', so the discovery set evaluated against ran(M(d')) is identical in both states. ∎

(d) *Non-permanence witness — strict shrinkage under contraction.* The inclusion (b) is strict when the contraction removes the last V-position whose I-address is in some link's endset coverage: `(E Σ →_{K.μ⁻} Σ', d, s, a ∈ dom(Σ.L) :: a ∈ discover_through_s(d) in Σ ∧ a ∉ discover_through_s(d) in Σ')`. *Witness.* We extend the Worked Example. Before the arrangement-edit composite, K.λ (LinkAllocation, ASN-0047) allocates a fresh link a' with `Σ.L(a') = (F', ∅, Θ')` carrying `F' = {(a₃, ℓ_a')}` for `ℓ_a' = a₄ ⊖ a₃` — well-defined by D0 (a₃ < a₄, equal lengths) with reach `a₃ ⊕ ℓ_a' = a₄` (D1 inverse) and coverage `⟦(a₃, ℓ_a')⟧ = {t : a₃ ≤ t < a₄}`, which contains a₃ — and any non-empty type slot `Θ' = {(τ', ℓ_τ')}` satisfying L3. (L4 admits the from-slot span and the empty to-slot; the empty-endset case is treated elsewhere in this note.) Set s = from. The Worked Example's after-removing-a₃ composite proceeds in two elementary steps — Step 1, K.μ~, and Step 2, K.μ⁻; instantiate SV14(d)'s `Σ →_{K.μ⁻} Σ'` existential with the elementary K.μ⁻ step `Σ_int →_{K.μ⁻} Σ'`, where Σ_int is the post-K.μ~ intermediate state with `M_int(d) = {v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅, v₅↦a₃}` and Σ' has `M'(d) = {v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅}` (D-SEQ-admissible because v₅ is the maximum V-position in Σ_int; the K.μ~ step preceding it is preparation that brings a₃ to v₅). Pre-state Σ_int: ran(Σ_int.M(d)) = ran(Σ.M(d)) = {a₁, a₂, a₃, a₄, a₅} (K.μ~ preserves the I-range per SV5; K.λ ran before K.μ~ and is M-frame), so a₃ ∈ coverage(F') ∩ ran(Σ_int.M(d)) and a' ∈ discover_through_from(d) in Σ_int. Post-state Σ': ran(Σ'.M(d)) = {a₁, a₂, a₄, a₅}; under the sibling ordering a₁ < a₂ < a₃ < a₄ < a₅, the elements a₁, a₂ lie strictly below a₃ and the elements a₄, a₅ lie at or beyond the reach a₄, so none lies in the half-open interval [a₃, a₄) = coverage(F') ∩ {a₁, a₂, a₄, a₅}; the intersection is empty, and a' ∉ discover_through_from(d) in Σ' (L12 carries coverage(F') through unchanged across the K.μ⁻ step). The exit is local to d: a' remains in discover_from({a₃}) (the fixed I-address set is unchanged, SV8), and remains in discover_through_from(d'') for any d'' ≠ d whose arrangement still maps a₃. ∎

The caveat above (preceding SV9) records the same non-permanence informally; SV14(b) and SV14(d) supply the formal claim and witness that downstream consumers can cite. SV14(a)–(c) are direct corollaries of SV2–SV4 read per-link, packaged for the document-derived query that downstream link-discovery policy notes will use most often.


## The Discovery-Resolution Distinction

We have now defined two independent operations — discovery and resolution — and we observe that they answer fundamentally different questions:

- **Discovery** asks: "which links relate to this content?" It operates on I-address intersection (coverage(e) ∩ A ≠ ∅), is independent of any particular document's arrangement, and is permanent (SV8).

- **Resolution** asks: "where in document d are this link's endpoints visible?" It operates on I-to-V conversion through d's current arrangement, depends entirely on M(d), and changes as M(d) changes.

**SV10 (DiscoveryResolutionIndependence).** A link may be discoverable through a set of I-addresses A yet have only partial resolution in a particular document — the projection covers a proper subset of the endset's full coverage:

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

Note that discovery through d entails non-empty projection in d: if a ∈ discover_s({M(d)(v) : v ∈ V}), then coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅, and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)), we have π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅. So within the discovering document, resolution is guaranteed non-empty.

This arises naturally. Suppose a link's from-endset covers I-addresses {i₁, i₂, i₃}. Document d's arrangement contains only i₂. Discovery succeeds (non-empty intersection). But resolution of the from-endset in d returns only the V-positions corresponding to i₂ — the other two I-addresses have no V-positions in d.

*Concrete witness.* We exhibit a state Σ, link a, document d, slot s = from, and V ⊆ dom(Σ.M(d)) satisfying the existential. Fix the content subspace identifier s_C = 1 throughout — this is the value that the K.α amendment (ASN-0047) requires the first element-field component of every content-store allocation to carry (`fields(a).E₁ = s_C`), and is correspondingly the first component of every depth-2 V-position in the content subspace. Take origin O = 1.0.1.0.1 and three element-level sibling tumblers i₁ = O.0.1.1, i₂ = O.0.1.2, i₃ = O.0.1.3 — each T4-valid with zeros(i_k) = 3 (the three zeros sit at positions 2, 4, 6, all in the prefix), origin(i_k) = N(i_k).0.U(i_k).0.D(i_k) = 1.0.1.0.1 = O, and element field E(i_k) = [1, k] of length 2. Of these three tumblers, only i₂ will be allocated by K.α in the chain below; i₁ and i₃ remain well-defined T4-valid tumblers in T but are *not* placed into dom(Σ.C). This is essential for J0 (AllocationRequiresPlacement, ASN-0047) compliance — J0 obligates placement in some M(d) *only* for newly allocated content addresses, so allocating i₁ or i₃ without also placing them via K.μ⁺ would falsify the composite against J0. For the allocated i₂, S7c (ASN-0036) requires #E(i₂) ≥ 2 — satisfied as #E(i₂) = 2 — and the K.α amendment requires E(i₂)₁ = 1 = s_C; the unallocated i₁ and i₃ satisfy the same #E = 2 size and leading-component value by construction but bear no dom(Σ.C) obligation. Let s_span = i₁ and ℓ_span = 0.0.0.0.0.0.0.3 (action point k = 8, the first nonzero component, with k = 8 > 6 = p₃ so the action point lies strictly within the element field). Then s_span ⊕ ℓ_span: positions 1–7 are copied from s_span (yielding 1.0.1.0.1.0.1), and position 8 advances by 3 (1 + 3 = 4), so the reach is s_span ⊕ ℓ_span = 1.0.1.0.1.0.1.4 = O.0.1.4. The span coverage `⟦(i₁, ℓ_span)⟧ = {t : i₁ ≤ t < O.0.1.4}` contains the element-level tumblers i₁, i₂, i₃ — each agrees with i₁ on positions 1–7 and has position-8 value in {1, 2, 3} ⊆ [1, 4) — independently of allocation status, since `⟦(s, ℓ)⟧` is a subset of T determined by the tumbler structure of (s, ℓ) and is well-formed under T12 (SpanWellDefinedness, ASN-0034) regardless of whether s ∈ dom(Σ.C). Take v₁ = [s_C, 1] — the depth-2 D-MIN V-position in d's content subspace: #v₁ = 2 (satisfying S8a's depth-≥-2 requirement for V-positions in dom(M(d))), every component is strictly positive (S8a positivity), and v₁ = [s_C, 1, ..., 1] of depth m_C = 2 is the unique minimum of V_{s_C}(d) (D-MIN, ASN-0047). The state Σ is reachable from the empty state by a *standard composite chain* of elementary transitions whose existence we now make explicit (omitted, this would be the "single K.μ⁺ step" misreading that conflates the final extension with the full witness): the node entity at 1 is supplied by InitialState (we fix the bootstrap-node system parameter `n₀ = 1` throughout this ASN's witnesses; `E₀ = {n₀}` with `IsNode(n₀)` by ASN-0047's InitialState, so node 1 inhabits E from Σ₀ onward without any K.δ node-allocation step); K.δ then allocates the account entity at 1.0.1 under the now-existing node n₀ = 1 (K.δ ¬IsNode case), and the document d itself by a further K.δ step under the now-existing account (per-level K.δ steps under ASN-0047, each discharging its prefix-existence precondition against the entities already in E); K.α allocates the single element-level content address i₂ under d's prefix with fields(i₂).E₁ = s_C (per the K.α amendment) — i₁ and i₃ remain unallocated tumblers in T per the J0 discussion above, since the chain places only i₂; K.λ allocates the link at the link-subspace address `a = 1.0.1.0.1.0.s_L.1` — under the same node/account/document prefix `1.0.1.0.1` as the i_k, with the element field beginning with the link-subspace identifier `s_L` per the K.λ amendment (ASN-0047) and terminal component `1` ensuring T4-validity (zeros at positions 2, 4, 6 only; a₁ = 1 ≠ 0; a_#a = 1 ≠ 0; no adjacent zeros), with `a ∉ dom(Σ.L)` in the pre-state (freshness) — carrying the standard triple `Σ.L(a) = (F, G, Θ)` where `F = {(i₁, ℓ_span)}` is the content span constructed above, `G = ∅` (the to-endset is empty; L4 (EndsetGenerality, ASN-0043) admits empty endsets, and the ASN's "Empty-endset cases" discussion explicitly treats one-sided links of the form `(F, ∅, Θ)`), and `Θ = {(τ, ℓ_τ)}` for any single non-empty type span (the specific T4-valid `τ` and the non-zero `ℓ_τ` are immaterial to the projection computation, which reads only F; their existence is what L3's requirement `|Σ.L(a)| ≥ 3 ∧ Σ.L(a).e₃ ≠ ∅` demands of the type slot). This link value satisfies L0–L14: L3 holds because the triple has exactly three slots with `Θ ≠ ∅`; L4 admits both `(i₁, ℓ_span)` as a content span and `(τ, ℓ_τ)` as a type span; L0/L14 hold because `fields(a).E₁ = s_L` places a in the link-subspace partition disjoint from dom(Σ.C); the remaining L-properties carry through by direct inspection of the allocation. K.μ⁺ extends M(d) from V_{s_C}(d) = ∅ by adding v₁ ↦ i₂ (the value i₂ ∈ dom(Σ.C) satisfying K.μ⁺'s referential-integrity precondition, v₁ admissible as D-MIN by D-CTG with the empty prior content-subspace); and K.ρ records the provenance mapping required to satisfy J1★ (ExtensionRecordsProvenanceContent, ASN-0047) — the K.μ⁺ extension of a content-subspace mapping must be accompanied by a K.ρ step that records v₁'s I-value in R for J1★ to hold in the composite post-state. The per-step preconditions are pairwise independent up to the prefix ordering required by K.δ (account-allocation before document-allocation, with the node n₀ = 1 supplied by InitialState rather than by K.δ) and the referential-integrity ordering required by K.μ⁺ (K.α before K.μ⁺); D-CTG and S8-depth hold trivially for the singleton V_{s_C}(d) = {v₁} at the post-state. With a, F, G, Θ as constructed, coverage(F) ⊇ {i₁, i₂, i₃} ∋ i₂. Then with V = {v₁} and A = {Σ.M(d)(v₁)} = {i₂}:

- *Discovery succeeds:* coverage(F) ∩ A = {i₂} ≠ ∅, so a ∈ discover_from(A).
- *Projection is proper:* π(F, d) = coverage(F) ∩ ran(Σ.M(d)) = coverage(F) ∩ {i₂} = {i₂}, but coverage(F) ⊇ {i₁, i₂, i₃} ⊋ {i₂}, so π(F, d) ⊊ coverage(F).

The link is discoverable through d via the shared address i₂, yet resolves to only that one I-address — i₁ and i₃ remain in coverage(F) but are absent from ran(Σ.M(d)). ∎

The cross-document case is starker: a link discovered through document d₁ (which shares I-addresses with the endset) may have empty resolution in a different document d₂ whose arrangement contains none of the endset's I-addresses. Discovery and resolution operate through independent documents; discovery through one does not entail resolution in another. We state this formally.

**Corollary (CrossDocumentDecoupling, from SV10).** Discovery in one document and empty resolution in another are simultaneously realisable:

`(E Σ, a, d₁, d₂, s, A :: d₁ ≠ d₂ ∧ a ∈ discover_s(A) ∧ A ⊆ ran(Σ.M(d₁)) ∧ π(Σ.L(a).s, d₂) = ∅)`

*Witness.* Extend the SV10 witness. Σ already contains link a with F = {(i₁, ℓ_span)} and coverage(F) ⊇ {i₁, i₂, i₃}; let d₁ = d with Σ.M(d₁) = {v₁ ↦ i₂}, so the SV10 discovery clause supplies A = {i₂} ⊆ ran(Σ.M(d₁)) and a ∈ discover_from(A). We now reach, by a chain of elementary transitions enabled in Σ, a successor state Σ⁺ in which the existential's remaining clauses (d₂ ≠ d₁, π(Σ⁺.L(a).from, d₂) = ∅) are witnessed; the existential is over states reachable from Σ, so exhibiting Σ⁺ suffices.

*Setup precondition (inherited from SV10).* The SV10 base state Σ presupposes that d₁ ∈ E_doc with origin(d₁) = O = 1.0.1.0.1; for d₁'s address to be well-formed under K.δ, the prefix entities — a node entity at 1 and an account entity at 1.0.1 (under K.δ's per-level preconditions, ASN-0047) — must already inhabit E. We discharge the node requirement by identifying the bootstrap node `n₀` with address `1`: by InitialState (ASN-0047), `E₀ = {n₀}` with `IsNode(n₀)`, and the choice of n₀ is a system parameter (not a state transition); we fix this parameter at `n₀ = 1` throughout this ASN's witnesses, so the node entity at 1 inhabits E from Σ₀ onward without any K.δ node-allocation step. The account entity at 1.0.1 is then allocated by K.δ under the now-existing node n₀ = 1 (K.δ ¬IsNode case, ASN-0047), and d₁ = 1.0.1.0.1 by a further K.δ step under the now-existing account. We assume these two K.δ allocations have taken place prior to Σ (equivalently, the SV10 witness chain is implicitly preceded by K.δ steps that allocate the account at 1.0.1 and the document d₁ itself; the node 1 is supplied by InitialState, not by K.δ). Under this base state, Step 1 below allocates a *sibling* document d₂ = 1.0.1.0.2 under the *same* account 1.0.1 — the node n₀ = 1 and the account 1.0.1 are already in E, so K.δ's prefix-existence preconditions are discharged by Σ's setup and only the document-level admissibility (T4-validity, freshness) is checked in Step 1.

- *Step 1 — K.δ allocates d₂ under a node/account prefix yielding origin(d₂) ≠ O.* The SV10 origin used was O = 1.0.1.0.1. Pick any node/account/document prefix `d₂ = 1.0.1.0.2` — agreeing with O on the node and account fields (positions 1–4: 1.0.1.0) but differing at the document component (position 5: 2 vs 1), so origin(d₂) = 1.0.1.0.2 ≠ O. K.δ (DocumentAllocation, ASN-0047) allocates d₂ ∈ E_doc \ dom(Σ.M) and seeds Σ.M(d₂) = ∅. The document address d₂ is T4-valid by construction, and the prefix-entity precondition — that the node entity at 1 and the account entity at 1.0.1 inhabit E at the Σ-state where this K.δ fires — is discharged by P1 (EntityPermanence, ASN-0047) together with the setup precondition: the setup precondition places node 1 in E from Σ₀ (by InitialState) and the account 1.0.1 in E by an earlier K.δ step, and P1's `E ⊆ E'` invariant carries both entries forward through every intervening transition of the SV10 witness chain (K.δ on d₁, K.α on i₂, K.λ on a, K.μ⁺ on v₁ ↦ i₂, K.ρ — none of which can remove entries from E), so both remain in E at Σ. Freshness — `d₂ ∉ dom(Σ.M)` — holds because the SV10 chain placed only d₁ in dom(M), so the sibling-document address d₂ = 1.0.1.0.2 lies outside it. K.δ's preconditions are therefore satisfied.
- *Step 2 — K.α allocates j under d₂'s prefix with fields(j).E₁ = s_C.* Apply K.α (ContentAllocation, ASN-0047) to allocate a fresh element-level address j with prefix d₂ and element field beginning at s_C: take j = 1.0.1.0.2.0.1.1 — T4-valid (zeros at positions 2, 4, 6 only; j₁ = 1 ≠ 0; j_#j = 1 ≠ 0; no adjacent zeros), with origin(j) = N(j).0.U(j).0.D(j) = 1.0.1.0.2 = origin(d₂) ≠ O, and with fields(j).E₁ = j₇ = 1 = s_C (per the K.α amendment, ASN-0047). The post-state has j ∈ dom(Σ.C).
- *Step 3 — K.μ⁺ places v₁ ↦ j in M(d₂), composed with K.ρ for J1★.* Apply K.μ⁺ (ArrangementExtension, ASN-0047) to add the mapping v₁ ↦ j to M(d₂). The precondition v₁ ∈ V_{s_C}(d₂) is satisfied (v₁ = [s_C, 1] is the D-MIN of the content subspace, available because M(d₂) = ∅ pre-step — the `v₁ = [s_C, 1]` here is the D-MIN position of d₂'s content subspace, distinct from but co-named with d₁'s D-MIN; V-positions are document-local, so the symbol `v₁` from the SV10 witness for d₁ and the `v₁` introduced here for d₂ inhabit disjoint per-document V-arenas and refer to different V-positions despite the shared coordinate tuple), and the referential-integrity precondition j ∈ dom(Σ.C) holds by Step 2. Compose with K.ρ (ProvenanceRecording, ASN-0047) recording the provenance of the v₁ ↦ j mapping into R; this is required by ValidCompositeExtended for J1★ (ExtensionRecordsProvenanceContent, ASN-0047) to hold in the post-state, since K.μ⁺ alone would extend M(d₂) without an accompanying R-entry. K.ρ modifies R only — it preserves L and M — so the SV6 application below, which depends only on origin(j) ≠ O and the post-state Σ⁺.M(d₂), is unaffected. Post-state Σ⁺ satisfies Σ⁺.M(d₂) = {v₁ ↦ j} and the J1★ coupling.

By SV6 (CrossOriginExclusion), since origin(j) ≠ O = origin(i₁), the span's start i₁ is element-level, and ℓ_span's action point lies in the element field (k = 8 > 6 = p₃), we have j ∉ ⟦(i₁, ℓ_span)⟧. So coverage(F) ∩ {j} = ∅ and π(Σ⁺.L(a).from, d₂) = coverage(F) ∩ ran(Σ⁺.M(d₂)) = coverage(F) ∩ {j} = ∅. The link-store-frame transitions (K.δ, K.α, K.μ⁺, K.ρ) preserve Σ.L by L12, so the discovery clause and coverage(F) are unchanged in Σ⁺, and the SV10-supplied a ∈ discover_from(A) with A ⊆ ran(Σ⁺.M(d₁)) carries forward. ∎

This asymmetry is not a deficiency. It reflects a genuine conceptual distinction: the link *exists* and *relates to* certain content (discovery); the *visibility* of that relationship depends on which document you are looking through (resolution).


## Partial Survival

When contraction removes some but not all of an endset's I-addresses from a document's arrangement, the endset survives with reduced projection. We now characterize the structure of this partial survival.

We distinguish two related concepts that the decomposition produces: *decomposition terms* — the individual set intersections that appear in the union formula — and *maximal fragments* — the maximal contiguous ordinal subsequences that the union as a whole presents in each mapping block. The two coincide when each span contributes a disjoint contiguous region; they diverge when adjacent or overlapping spans coalesce.

**Definition — Decomposition Term.** For each pair (j, k) with 1 ≤ j ≤ m and 1 ≤ k ≤ p, the *(j, k)-decomposition term* is the set `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)`. The number of decomposition terms is exactly m · p (possibly with empty terms).

**Definition — Maximal Endset Fragment.** For an endset e and document d, let B = {β₁, ..., β_p} be the maximally merged block decomposition (C1a, ASN-0058) of the restriction M(d)|_{V_{s_C}(d)}. A *maximal fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence taken within the *text-subspace projection* π_text(e, d) — fragments are by construction confined to the content subspace s_C, since B partitions only the content-subspace V-positions and I(β_k) ⊆ ran_text(M(d)). The link-subspace contribution to π(e, d) is deferred to the Link Subspace ASN (see the parenthetical after SV11). Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π_text(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π_text(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π_text(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π_text(e, d).

A decomposition term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is itself contiguous in the ordinal sequence of I(β_k) (by the convexity argument below) but need not be maximal: two terms with the same k may overlap or be adjacent, in which case their union forms a single maximal fragment.

**SV11 (PartialSurvivalDecomposition).** Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be the maximally merged block decomposition of the restriction M(d)|_{V_{s_C}(d)} — the content-subspace portion of d's arrangement. This restriction satisfies C1a's conditions: functionality from S2, finiteness from S8-fin, and fixed depth from S8-depth within subspace s_C. The text-subspace projection π_text(e, d) (Endset Projection section) admits the block-indexed expansion `ran_text(M(d)) = ⋃_k I(β_k)` under B — the equality holds because B covers exactly the content-subspace V-positions (B1 applied to the restriction), so the I-extents of B's blocks are precisely the content-subspace I-addresses. Two count claims hold simultaneously:

(a) *Decomposition-term cover — exactly m · p terms.*

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

The union is over *exactly* m · p decomposition terms (one per (span, block) pair), some possibly empty. Here "exactly m · p decomposition terms" counts (span, block)-indexed positions in the Cartesian product, not distinct subsets of π_text(e, d); two terms may coincide as sets.

(b) *Maximal-fragment count — at most m · p fragments.* The same set π_text(e, d) is also the disjoint union (within each block) of its maximal ordinal-contiguous fragments, totalling *at most* m · p of them across all blocks. The inequality is strict whenever (a) some decomposition term `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` is empty, or (b) two non-empty decomposition terms within a single block are ordinally adjacent or overlap, coalescing into a single maximal fragment. The bound m · p is attained iff every (j, k) pair yields a non-empty decomposition term *and* these terms are pairwise non-adjacent and non-overlapping within each block. *Proof of the biconditional.* (⇒) Suppose the maximal-fragment count equals m · p. The fragment count is bounded above by the non-empty-term count (each non-empty term is contiguous within its block by the S0-convexity argument below, hence lies in exactly one maximal fragment within its block; distinct fragments therefore arise from distinct or non-coalescing terms), which is in turn bounded by m · p (the total term count); equality with m · p therefore forces (i) the non-empty-term count to equal m · p — every (j, k) yields a non-empty term, ruling out condition (a) — and (ii) each non-empty term to be itself a maximal fragment, ruling out condition (b)'s adjacency or overlap of distinct non-empty terms within a block (any adjacency *or overlap* would coalesce two terms into one fragment, dropping the count below m · p; the overlap half holds because two overlapping non-empty terms within a single block — each contiguous in I(β_k)'s ordinal sequence by the S0-convexity argument — share at least one ordinal position, so their union is itself ordinal-contiguous in I(β_k) and forms a single maximal fragment). (⇐) Conversely, suppose every (j, k) yields a non-empty term and no two non-empty terms within any single block are ordinally adjacent or overlap. Within each block β_k, the m terms (one per span) are pairwise non-adjacent and non-overlapping, and each is contiguous (by the S0-convexity argument below), so no two coalesce: the maximal fragments inside β_k are exactly the m non-empty terms restricted to β_k. Summing across the p blocks gives exactly m · p maximal fragments. ∎

(The full projection π(e, d) = coverage(e) ∩ ran(M(d)) may additionally include I-addresses reached through link-subspace V-positions. K.μ⁺_L (LinkSubspaceExtension, ASN-0047) creates link-subspace V-positions `v_ℓ ↦ ℓ` where `subspace(v_ℓ) = s_L`, so π_text(e, d) ⊆ π(e, d) in general. The link-subspace contribution to projection — including links whose endsets reference other link addresses (L13, ReflexiveAddressing) — is deferred to the Link Subspace ASN.)

*Derivation of the formula.* The endset's coverage decomposes as `coverage(e) = ⋃_{j=1}^{m} ⟦(sⱼ, ℓⱼ)⟧` (L3/L4, ASN-0043: the endset is a set of spans and its coverage is the union of their denotations). The text-subspace range decomposes as `ran_text(M(d)) = ⋃_{k=1}^{p} I(β_k)` (B1 applied to the restriction together with C1a, ASN-0058: C1a lifts M11/M12's existence-and-uniqueness of the maximally merged decomposition to the restriction `M(d)|_{V_{s_C}(d)}`, and the block decomposition's I-extents exhaust the content-subspace range). Substituting both into π_text(e, d) = coverage(e) ∩ ran_text(M(d)) and distributing intersection over union (set algebra, applied twice):

`π_text(e, d) = (⋃_j ⟦(sⱼ, ℓⱼ)⟧) ∩ (⋃_k I(β_k)) = ⋃_j ⋃_k (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

— which is the formula stated above. The remainder of this section establishes the structural properties of the m · p decomposition terms: each is contiguous within its block's ordinal sequence (S0 convexity, below), the terms may overlap or coalesce into fewer maximal fragments (fragment-count discussion), and the collection forms a cover rather than a partition under non-injective arrangements.

Consider each decomposition term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k). The span ⟦(sⱼ, ℓⱼ)⟧ is convex by S0 (Convexity). The set I(β_k) = {a_k + j : 0 ≤ j < n_k} is not itself convex in T — child-depth tumblers create gaps between consecutive ordinal increments — but we do not need it to be. For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by M1 (OrderPreservation, ASN-0058)), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence each decomposition term is contiguous within the ordinal sequence of I(β_k): if its first and last elements have ordinal offsets j₁ and j₂, every intermediate a_k + j with j₁ ≤ j ≤ j₂ also lies in the term.

*Decomposition terms versus maximal fragments.* The number of decomposition terms is m · p exactly — one per (span, block) pair, including empty terms. Within a single block β_k, the m terms `⟦(s₁, ℓ₁)⟧ ∩ I(β_k), ..., ⟦(s_m, ℓ_m)⟧ ∩ I(β_k)` are each contiguous in the ordinal sequence of I(β_k), but they may overlap or be adjacent; their union π_text(e, d) ∩ I(β_k) may therefore consist of fewer maximal contiguous regions than there are non-empty terms. A maximal fragment is one such maximal contiguous region. Hence the number of maximal fragments within a single block is at most the number of non-empty decomposition terms in that block, which is at most m. Across p blocks, the number of maximal fragments is bounded by m · p — the same upper bound as for decomposition terms, attained when every non-empty term is itself a maximal fragment (when the spans contribute pairwise non-adjacent regions within each block). Each maximal fragment is compactly described by its first element and count: (a_k + j₁, j₂ − j₁ + 1).

When M(d) is non-injective — within-document sharing (S5, UnrestrictedSharing) — two blocks may have overlapping I-extents, so maximal fragments from distinct blocks may share I-addresses. The fragment collection is therefore a *cover* of π_text(e, d), not necessarily a partition; summing fragment widths may overcount distinct I-addresses. The set-union formula `π_text(e, d) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))` remains correct (set union is idempotent), and it does not depend on the term/fragment distinction.

We note a distinction between maximal fragments (or decomposition terms — both are contiguous ordinal subsequences) and span denotations. A maximal fragment is a finite set of I-addresses {a_k + j₁, ..., a_k + j₂} produced by ordinal increment within an actually-allocated block. The span denotation ⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} includes all tumblers in the half-open interval, including child-depth tumblers between consecutive ordinal increments — a child c produced by inc(a, 1) satisfies a < c < a + 1, so c ∈ ⟦(a, ℓ)⟧ for any span (a, ℓ) whose reach satisfies a ⊕ ℓ > a + 1, but c is not necessarily in ran(M(d)). The exact characterisation of π_text(e, d) is the union of its maximal fragments (equivalently, the union of its decomposition terms), not a union of span denotations. If one needs to connect projections to the span algebra of ASN-0053, the correct relationship is *covering*: for each maximal fragment with first element a_k + j₁ and last element a_k + j₂, a level-uniform span (a_k + j₁, ℓ') with reach a_k + (j₂ + 1) satisfies ⟦(a_k + j₁, ℓ')⟧ ⊇ fragment (since ordinal increment preserves tumbler length by TA5(c)). Such covering span-sets are normalizable within each tumbler-depth group (S8, NormalizationExistence).

The significance: **partial survival is well-structured.** The surviving portion of an endset in a given document decomposes into finitely many maximal fragments — at most m · p of them, where m is the endset's span count and p is the block count — each compactly described by a start address and count within a mapping block's ordinal sequence. Convexity (S0) ensures contiguity within each block, preventing degeneration into arbitrary subsets of I-addresses. The m · p bound moves with the state: a composite edit that splits an existing block (e.g., K.μ~ + K.μ⁻ excising interior content) raises p and therefore raises the bound; the same bound applies at the post-edit state under its post-edit p.


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

The from-endset is vital in d: π(F, d) ≠ ∅. Both π and locate are determined entirely by coverage(F) and the current M(d) (NoStaleResolutionState architectural remark).

*After removing a₃.* The net effect of removing a₃ from ran(M(d)) while satisfying D-CTG requires a composite of two elementary transitions, because K.μ⁻ alone cannot remove an interior V-position — by D-SEQ, valid contractions remove from the maximum end of V_S(d) only.

*Step 1 — K.μ~ rearranges d so that a₃ occupies the maximum V-position.* Apply the bijection ψ on dom(M(d)) = {v₁, v₂, v₃, v₄, v₅} given by ψ(v₃) = v₅, ψ(v₄) = v₃, ψ(v₅) = v₄, ψ(v_i) = v_i for i ∈ {1, 2} (a cyclic shift of the three rightmost positions sending a₃ to v₅). The intermediate state is:

`M_int(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅, v₅ ↦ a₃}`

At this point, dom(M_int(d)) = dom(M(d)) (reordering preserves the domain) and ran(M_int(d)) = ran(M(d)) = {a₁, a₂, a₃, a₄, a₅} (SV5: reordering preserves the I-range, so π(F, d) = {a₂, a₃, a₄} is unchanged at this step; only locate has changed — locate_{M_int}(F, d) = {ψ(v₂), ψ(v₃), ψ(v₄)} = {v₂, v₅, v₃}).

*Step 2 — K.μ⁻ removes v₅.* By D-SEQ, v₅ is now the maximum V-position and is admissible for contraction. The post-contraction state is:

`M'(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅}`

with dom(M'(d)) = {v₁, v₂, v₃, v₄} and ran(M'(d)) = {a₁, a₂, a₄, a₅}. Reading projection, location, and discovery at this final state:

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

*Degeneracy note.* This swap is degenerate w.r.t. demonstrating the SV5 locate-set-change behaviour: both v₂ and v₃ lie inside the pre-swap locate set {v₂, v₃}, so ψ permutes *within* the locate set rather than crossing its boundary, and the locate set is preserved as a set. The formal relationship locate_{Σ'}(F, d) = {ψ(v) : v ∈ locate_Σ(F, d)} still holds here (ψ(v₂) = v₃ and ψ(v₃) = v₂, so {ψ(v₂), ψ(v₃)} = {v₂, v₃} = locate_Σ(F, d)) — it just reduces to an automorphism of the locate set in this case. The general case where the locate *set* strictly changes — ψ mapping a V-position inside the locate set to one outside, or vice versa — is exhibited by the next subsection. SV5's primary claim (π-invariance under reordering) is itself demonstrated by the example regardless of this degeneracy.

The projection is invariant under reordering; the resolution set transforms by the reordering bijection ψ.

*Reordering that changes locate.* Return to the post-removal state `M'(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅}` with locate(F, d) = {v₂, v₃} as established above (F = {(a₂, ℓ)}, coverage(F) = {t : a₂ ≤ t < a₅}). Apply a K.μ~ step whose reordering bijection ψ swaps v₁ and v₂ (and fixes v₃, v₄), so the post-state arrangement is:

`M'''(d) = {v₁ ↦ a₂, v₂ ↦ a₁, v₃ ↦ a₄, v₄ ↦ a₅}`

Reading at this final state:

- π(F, d) = coverage(F) ∩ ran(M'''(d)) = coverage(F) ∩ {a₁, a₂, a₄, a₅} = {a₂, a₄} — unchanged from M'(d) (SV5: reordering preserves the I-range)
- locate(F, d) = {v ∈ dom(M'''(d)) : M'''(d)(v) ∈ coverage(F)} = {v₁, v₃} — since M'''(d)(v₁) = a₂ ∈ coverage(F) and M'''(d)(v₃) = a₄ ∈ coverage(F), and M'''(d)(v₂) = a₁ ∉ coverage(F)

The locate *set* strictly changed: {v₂, v₃} pre-swap, {v₁, v₃} post-swap. The two sets differ — v₂ exited locate (its newly assigned I-address a₁ is outside coverage(F)) and v₁ entered locate (its newly assigned I-address a₂ is inside coverage(F)) — because ψ crossed the locate boundary: ψ(v₁) = v₂ takes v₁ ∉ locate_{M'(d)} to v₂ ∈ locate_{M'(d)}, and symmetrically ψ(v₂) = v₁ moves the locate-membership the other way. Per the SV5 formal relationship `locate_{Σ'}(F, d) = {ψ(v) : v ∈ locate_Σ(F, d)}`, we verify: {ψ(v₂), ψ(v₃)} = {v₁, v₃} = locate(F, d) at M'''(d). ✓

This subsection exhibits the substantive content of SV5 that the "After reordering" subsection's within-locate swap could not: the *I-addresses* in the projection are invariant under K.μ~, but the *V-positions* through which the reader observes those addresses are reshuffled by ψ. A reader navigating d after this K.μ~ step would find the from-endset's content at V-positions v₁ and v₃ — different from the V-positions v₂ and v₃ where they were found before — even though the underlying I-addresses {a₂, a₄} reached are unchanged.

*Two-span, non-injective scenario.* The preceding subcases used a single span (m = 1) and an injective arrangement. We now exercise SV11 with m = 2 spans and a non-injective Σ.M(d) to expose the cover-not-partition behaviour and the m · p decomposition bound.

Re-take the initial five-address content store with a₁ < a₂ < a₃ < a₄ < a₅ all sharing one origin and one tumbler length. Extend the document's arrangement with two additional V-positions v₆, v₇ that share I-addresses with v₂ and v₃ (within-document sharing, S5):

`M(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₃, v₄ ↦ a₄, v₅ ↦ a₅, v₆ ↦ a₂, v₇ ↦ a₃}`

with v₁ < v₂ < v₃ < v₄ < v₅ < v₆ < v₇. The maximally merged block decomposition of this restriction has p = 2 blocks: β₁ = (v₁, a₁, 5) covering v₁..v₅ with I-extent {a₁, a₂, a₃, a₄, a₅}, and β₂ = (v₆, a₂, 2) covering v₆..v₇ with I-extent {a₂, a₃}. We verify the M7 merge condition for β₁ and β₂ fails. *V-adjacency holds:* v₆ = shift(v₁, 5), i.e., v₆ is the V-position immediately after β₁'s last covered position v₅, so the V-side of M7 is satisfied. *I-adjacency fails:* M7 would require a₂ = a₁ + 5, but a₁ + 5 = a₅ + 1 ≠ a₂ (a₂ falls strictly inside the a₁..a₅ sequence, not past it; here `+ n` denotes the OrdinalShiftBase numeric shift on I-side tumblers, matching the convention used elsewhere in this section). With one of the two adjacency conjuncts violated, M7 cannot succeed and M12's split rule forces the block boundary at v₅ → v₆. The two blocks share I-addresses {a₂, a₃} — this is the non-injective signature.

Define a two-span endset `e = {(s₁, ℓ₁), (s₂, ℓ₂)}` with s₁ = a₁, ℓ₁ = a₃ ⊖ a₁ (reach a₃) and s₂ = a₃, ℓ₂ = a₅ ⊖ a₃ (reach a₅). Then `coverage(e) = ⟦(a₁, ℓ₁)⟧ ∪ ⟦(a₃, ℓ₂)⟧` and among the allocated I-addresses this contains {a₁, a₂, a₃, a₄}. The two spans abut at a₃: the first contains a₁, a₂ (interval `[a₁, a₃)`), the second contains a₃, a₄ (interval `[a₃, a₅)`).

*SV11 decomposition.* With m = 2 and p = 2 there are m · p = 4 decomposition terms:

- ⟦(a₁, ℓ₁)⟧ ∩ I(β₁) = {a₁, a₂} (span 1 within block 1)
- ⟦(a₃, ℓ₂)⟧ ∩ I(β₁) = {a₃, a₄} (span 2 within block 1)
- ⟦(a₁, ℓ₁)⟧ ∩ I(β₂) = {a₂} (span 1 within block 2; β₂'s extent is {a₂, a₃}, intersected with `[a₁, a₃)`)
- ⟦(a₃, ℓ₂)⟧ ∩ I(β₂) = {a₃} (span 2 within block 2)

Union: `π_text(e, d) = {a₁, a₂} ∪ {a₃, a₄} ∪ {a₂} ∪ {a₃} = {a₁, a₂, a₃, a₄}`. ✓

*Cover, not partition.* Summed term widths: 2 + 2 + 1 + 1 = 6, but |π_text(e, d)| = 4. The addresses a₂ and a₃ each occur in two terms — once per block — because the non-injective arrangement places these I-addresses in both β₁ and β₂. The fragments are not disjoint as sets; the set-union formula remains correct because set union is idempotent.

*Maximal fragments.* Within β₁, the two terms {a₁, a₂} and {a₃, a₄} are adjacent in the ordinal sequence of I(β₁) (which is a₁ < a₂ < a₃ < a₄ < a₅), so they coalesce into a single maximal fragment {a₁, a₂, a₃, a₄}. Within β₂, the terms {a₂} and {a₃} are adjacent in the ordinal sequence of I(β₂) (a₂ < a₃) and coalesce into {a₂, a₃}. The fragment count is 2 — strictly less than the non-empty-term count (4) and the m · p upper bound (4) — because adjacency within blocks merges term-level contiguous regions, while non-injective sharing introduces no new fragments beyond those each block independently contributes.

*Resolution.* `locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)} = {v₁, v₂, v₃, v₄, v₆, v₇}` — both occurrences of a₂ (at v₂ and v₆) and both occurrences of a₃ (at v₃ and v₇) enter the locate set, while v₅ ↦ a₅ does not (a₅ ∉ coverage(e)). Thus |locate(e, d)| = 6 > 4 = |π(e, d)|, exhibiting the inequality `|locate(e, d)| ≥ |π(e, d)|` from the Endset Projection section under within-document sharing.

*Three-span variant exhibiting mechanism (a).* The scenario above realises strictness via mechanism (b) only (coalescence within blocks). We now extend the endset to three spans so that mechanism (a) — some decomposition term `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` empty — appears as well. Let a₆ and a₇ be two further T4-valid sibling tumblers past a₅ (with a₅ + 1 = a₆ and a₆ + 1 = a₇ in the ordinal sequence at the same tumbler length, sharing origin and tumbler length with a₁..a₅), *not* placed into dom(Σ.C) — no K.α step allocates them, paralleling the J0 (AllocationRequiresPlacement, ASN-0047) discipline used in the SV10 witness above, where sibling tumblers not destined for an M(d) mapping are left as well-defined tumblers in T rather than allocated by K.α and left orphaned (K.α without an accompanying K.μ⁺ for the freshly allocated address would falsify the composite against J0). Σ.C, M(d), and B = {β₁, β₂} are therefore all unchanged from the two-span case: dom(Σ.C) is still {a₁, ..., a₅}, ran_text(M(d)) is still {a₁, ..., a₅}, the maximally merged block decomposition B = {β₁, β₂} is unchanged (M11/M12 evaluate on M(d), not on Σ.C), and the I-extents are still I(β₁) = {a₁, ..., a₅} and I(β₂) = {a₂, a₃}. Define a third span (s₃, ℓ₃) = (a₆, a₈ ⊖ a₆) with reach a₈ — the next ordinal sibling beyond a₇; D0 is satisfied since a₆ and a₈ share origin and tumbler length, and neither a₆ nor a₈ need be allocated for the span to be well-formed: L4 (EndsetGenerality, ASN-0043) admits span endpoints regardless of allocation status, and T12 (SpanWellDefinedness, ASN-0034) requires only T4-validity of the start and reach tumblers, both of which hold by construction. Then `⟦(s₃, ℓ₃)⟧ = [a₆, a₈)` in the ordinal sequence, an interval strictly past a₅ and therefore disjoint from both I(β₁) and I(β₂); the SV11 decomposition below depends only on the span denotations (determined by tumbler arithmetic under T12) and the block I-extents (determined by M(d), unchanged here), so the unallocated status of a₆, a₇, a₈ does not affect any decomposition term.

The extended endset e′ = {(s₁, ℓ₁), (s₂, ℓ₂), (s₃, ℓ₃)} has m = 3 spans and p = 2 blocks, so m · p = 6 decomposition terms:

- ⟦(s₁, ℓ₁)⟧ ∩ I(β₁) = {a₁, a₂}
- ⟦(s₂, ℓ₂)⟧ ∩ I(β₁) = {a₃, a₄}
- ⟦(s₃, ℓ₃)⟧ ∩ I(β₁) = ∅       *(empty — mechanism (a))*
- ⟦(s₁, ℓ₁)⟧ ∩ I(β₂) = {a₂}
- ⟦(s₂, ℓ₂)⟧ ∩ I(β₂) = {a₃}
- ⟦(s₃, ℓ₃)⟧ ∩ I(β₂) = ∅       *(empty — mechanism (a))*

The union remains `π_text(e′, d) = {a₁, a₂, a₃, a₄}` — the third span contributes nothing because its coverage interval is disjoint from every block's I-extent. The maximal fragment count is still 2 (the within-block coalescences from the two-span case persist unchanged), strictly below the m · p = 6 ceiling. The strictness gap (6 − 2 = 4) is now jointly attributable: 2 terms vanish by mechanism (a) (the (3, 1) and (3, 2) terms), and 2 further units of slack come from mechanism (b) (each block coalesces its 2 non-empty terms into 1 fragment). This variant exhibits both mechanisms simultaneously and confirms SV11's biconditional in its sharpest reading — either source of strictness suffices on its own; here both are present.

*Cross-origin exclusion (SV6).* We now verify SV6 with explicit tumbler values. *Subspace note.* SV6's statement and proof are *structural* — they rest on the four-field tumbler decomposition (T4, ASN-0034) and the origin function `origin(t) = N(t).0.U(t).0.D(t)` (ASN-0036, S7), which act on T4-valid element-level tumblers regardless of subspace. The first component of an I-address selects the subspace (content vs. link, per the K.α / K.λ amendments of ASN-0047), but the field-separator-and-element-field layout that SV6 reasons about begins at the *node* field — the same in every subspace. The example below uses tumblers with first component 1; this aligns with the content subspace s_C = 1 used in the SV10 witness for consistency across worked examples, but no part of the verification depends on the subspace choice. The same arithmetic with first component s_L (link subspace) would produce an analogous cross-origin exclusion within the link subspace; SV6 is subspace-agnostic. Let s = 1.0.1.0.1.0.1.2.3 — nine components; the zeros at positions 2, 4, 6 are field separators, so p₃ = 6. Let ℓ = 0.0.0.0.0.0.0.0.5 — action point k = 9 (the first nonzero component), and k = 9 > 6 = p₃. By TumblerAdd, positions 1 through 8 are copied from s, and position 9 advances: reach = s ⊕ ℓ = 1.0.1.0.1.0.1.2.8. We verify the sandwich: reach agrees with s on positions 1 through 8, confirming that the three field separators (positions 2, 4, 6) are preserved.

Consider t = 1.0.1.0.1.0.1.2.5. We have s ≤ t (agree on positions 1–8; at position 9, t₉ = 5 > 3 = s₉) and t < reach (agree on positions 1–8; at position 9, t₉ = 5 < 8 = reach₉). So t ∈ ⟦(s, ℓ)⟧. The field separators of t are at positions 2, 4, 6 — matching s — so origin(t) = 1.0.1.0.1 = origin(s). ✓

Now consider b = 1.0.1.0.2.0.1.2.5, a different-origin address with origin(b) = 1.0.1.0.2. We compare b with reach = 1.0.1.0.1.0.1.2.8: they agree on positions 1–4; at position 5, b₅ = 2 > 1 = reach₅. By T1(i), b > reach, so b ∉ ⟦(s, ℓ)⟧. The SV6 precondition k > p₃ ensures that the element-field action point cannot advance the document-prefix components: reach differs from s only at positions ≥ k = 9 > 6 = p₃, so no different-origin address can slip between s and reach. ✓


## Content Fidelity

The preceding analysis addresses the *extent* of what survives — how many I-addresses remain in the projection. We now address the *identity* of what survives: is the content at those addresses the same as when the link was created?

**Corollary (ContentFidelity, from S0, ASN-0036).** Content fidelity is guaranteed directly by the foundation: for every a ∈ dom(Σ.C) and every state transition Σ → Σ', a ∈ dom(Σ'.C) and Σ'.C(a) = Σ.C(a). We do not assign this a new SV label because it introduces no new content beyond S0 — it is S0 read for its survivability content. Applied to endset I-addresses: for any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k, `(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))` for every endset slot s. The survivability implication merits emphasis: whatever portion of the endset remains visible in a document's arrangement, the content at those I-addresses is *exactly* what was there when the link was created. No edit, no revision, no amount of rearrangement can alter the content the link references. The surviving fragment may be smaller than the original endset, but each byte in the fragment is identical to the original.

The guarantee is the strongest possible short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation.

The guarantee is architectural rather than cryptographic — there is no hash or signature that a client can verify independently. The guarantee rests on the structural property that the content store is append-only (S1, StoreMonotonicity) and values are frozen at allocation (S0). Nelson explicitly acknowledges this is contractual trust, not mathematical proof of non-tampering [LM 5/17–18].


## Weakest Precondition Analysis

The forward claims SV2–SV5 each have a natural reading as a *weakest precondition*. Given an elementary transition K and a postcondition R, write wp(K, R) for the weakest predicate on the *pre-state Σ and the transition's parameters* such that R holds in every reachable post-state. Each elementary transition in K is parameterised by what it adds or removes (an inserted V↦I mapping, a set of removed V-positions, an allocated address, a reordering bijection), and the wp expression names those parameters explicitly so that the predicate is evaluated entirely in the pre-state. The wp form makes precise what an editor must guarantee *before* acting in order not to falsify R afterward. The forward claims SV2–SV5 give us each wp by direct rearrangement; we are recasting, not introducing new content. The "vitality loss condition" already developed in the SV3 discussion is essentially the wp of K.μ⁻ for non-vitality.

We take the postcondition R = "endset e remains vital in d after the transition", formally `π_{Σ'}(e, d) ≠ ∅`, and read off wp for each elementary transition. We restrict to non-empty endsets, as the empty case is degenerate (the section above).

- **wp(K.μ⁻ removing V_rm ⊆ dom(Σ.M(d)), π(e, d) ≠ ∅) = `(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(e))`** — *under the domain-of-applicability precondition that V_rm is D-SEQ-admissible:* for every subspace S, V_rm ∩ V_S(d) is either an upward tail `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` of V_S(d) for some 0 ≤ n'_S ≤ n_S, or empty (D-SEQ, ASN-0047). Arbitrary V_rm that violate D-SEQ are not valid K.μ⁻ parameters in the first place — the transition is not enabled — and the wp expression is meaningful only on the admissible parameter space. So K.μ⁻ removes a non-empty set V_rm of V-positions from the maximum end of V_S(d) per subspace, as enforced by D-SEQ, and vitality is preserved iff some V-position *not* in V_rm carries an I-address in coverage(e). The negation — the *vitality-loss* condition — is `(A v : v ∈ dom(Σ.M(d)) \ V_rm :: Σ.M(d)(v) ∉ coverage(e))` together with `(E v : v ∈ V_rm : Σ.M(d)(v) ∈ coverage(e))` (so the endset was vital pre-transition but every contributing V-position was removed). Both conjuncts are pre-state predicates over Σ and the D-SEQ-admissible removal parameter V_rm. This is Nelson's "if anything is left at each end" condition in formal dress. The wp form applies uniformly to content-subspace and link-subspace contractions: K.μ⁻ acts per-subspace on dom(M(d)) with D-SEQ enforcing upward-tail removal in each V_S(d) independently, and the coverage predicate `Σ.M(d)(v) ∈ coverage(e)` is well-formed for any endset whose coverage may include link addresses (admitted by L4, EndsetGenerality, with the reflexive-addressing case isolated by L13, ReflexiveAddressing). So V_rm ⊆ V_{s_L}(d) contracting a link-subspace tail can falsify vitality of an endset whose coverage references those link addresses by the same condition stated above for content-subspace tails — the formula is subspace-agnostic.

- **wp(K.μ⁺ adding extension Δ = M'(d) ↾ (dom(M'(d)) \ dom(Σ.M(d))) with new I-address set I_new = ran(Δ) ⊆ dom(Σ.C), π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ coverage(e) ∩ I_new ≠ ∅`** where Δ is the set of new V↦I mappings introduced by the transition (K.μ⁺ in ASN-0047 admits any extension `dom(M'(d)) ⊃ dom(M(d))` with value preservation at existing positions, so Δ may contain one or many new mappings; the precondition `(A v ∈ dom(Δ) : Δ(v) ∈ dom(Σ.C))` is required by K.μ⁺'s referential integrity). Extension preserves vitality if it already held in the pre-state *or* if at least one new I-address lies in coverage(e). The single-mapping specialisation Δ = {(v_new, i_new)} yields I_new = {i_new} and the formula reduces to `π(e, d) ≠ ∅ ∨ i_new ∈ coverage(e)`. For the typical case of an endset already vital before the extension, the first disjunct is satisfied and the wp reduces to the pre-state vitality regardless of the size of Δ.

- **wp(K.μ⁺_L adding v_ℓ ↦ ℓ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ ℓ ∈ coverage(e)`** where ℓ is the link address added by the transition. For endsets whose coverage lies entirely in dom(Σ.C) (the typical content endset), the second disjunct is unreachable and the wp reduces to pre-state vitality.

- **wp(K.μ~ under bijection ψ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`.** Reordering preserves ran(M(d)) (SV5), so the precondition is identical to the postcondition and does not depend on ψ.

- **wp(K.α, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.δ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** (for any d carried over by the frame) and **wp(K.ρ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.λ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** for every pre-existing endset e. Each of these transitions preserves M in its frame, so π is unchanged for every endset that existed prior to the transition.

The aggregate observation: only K.μ⁻ can falsify vitality, and only by a specific characterised action — every pre-state V-position contributing to coverage(e) being among the set V_rm removed by the contraction. Every other elementary transition either trivially preserves vitality (M-frame: K.α, K.δ, K.λ, K.ρ) or can only enlarge the projection (K.μ⁺, K.μ⁺_L). The distinguished composite K.μ~ preserves vitality at composite endpoints (its K.μ⁻ stage may shrink π and the K.μ⁺ stage restores it), so its composite-level wp is also `π(e, d) ≠ ∅`. The wp framework therefore localises the *single* operation that places vitality at risk and gives the *exact* pre-state condition under which the risk materialises.

For discovery, the corresponding wp values follow the same pattern with discover_s in place of π. Because discover_s depends only on coverage(e) and dom(Σ.L), every transition that holds L in frame preserves discover_s pointwise:

- **wp(K, a ∈ discover_s(A)) = `a ∈ discover_s(A)`** for every L-frame elementary K ∈ {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ} and for the distinguished composite K.μ~ (L-frame as a composite of L-frame elementaries), for every fixed A. Discovery is invariant under arrangement and content operations.

- **wp(K.λ allocating a_new with L_new(a_new) = (F_new, G_new, Θ_new), a ∈ discover_s(A)) = `a ∈ discover_s(A) ∨ (a = a_new ∧ coverage(L_new.s) ∩ A ≠ ∅)`** where a_new is the newly allocated link address and L_new is the corresponding endset tuple. K.λ can extend dom(L) by exactly one entry, so a previously-non-discoverable a becomes discoverable only when it is the newly allocated link and the new link's endset shares an I-address with A.

The discovery wp formalises SV7–SV9: invariance under L-frame transitions, monotonic growth under K.λ, permanence (SV8) as wp instance for any K. Nothing new is established beyond the forward claims; the reformulation makes the *direction of dependency* explicit — for a postcondition concerning resolution or discovery, we can read off the corresponding pre-state requirement directly from the transition's parameters and frame.


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
- Reordering of M(d) — via the *distinguished composite* K.μ~, which expands into a K.μ⁻ + K.μ⁺ pair under ASN-0047, not an elementary transition — preserves π(e, d) exactly: the I-addresses present in the projection are unchanged at the composite endpoints (per-step π may shrink at the K.μ⁻ stage and recover at the K.μ⁺ stage; see SV5's intermediate-state note). The locate *set* may change, and the transformation is fully characterised by `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` where ψ is the reordering bijection from K.μ~. By K.μ~-FIX (ASN-0047), ψ acts on a fixed domain — dom(M'(d)) = dom(M(d)) — so the V-position arena is invariant and only the V↦I assignment is permuted. The locate set changes whenever ψ maps a V-position inside locate_Σ(e, d) to one outside it, or vice versa; otherwise the {ψ(v) : v ∈ locate_Σ(e, d)} expression reduces to an automorphism of the locate set. [SV5]
- Changes to M(d) cannot affect locate(e, d') for d' ≠ d. [SV4]
- K.α, K.δ, K.ρ, and K.λ all preserve M-values in their frame, so locate(e, d) is unchanged for every endset e and every pre-existing document d ∈ dom(Σ.M) carried over the transition. (K.μ⁺_L is *not* M-frame — it adds a V↦I mapping in the link subspace — and is covered by the extension bullet above; the M-frame list here is the complement of the M-modifying transitions enumerated in the four preceding bullets.) *K.δ caveat.* K.δ enlarges the M-domain by allocating a new document d_new and seeding Σ'.M(d_new) = ∅ (ASN-0047); for every endset e, locate_{Σ'}(e, d_new) = ∅ trivially, since dom(Σ'.M(d_new)) = ∅. K.δ is M-frame in the sense that M-values at every pre-existing d ∈ dom(Σ.M) are unchanged (Σ'.M(d) = Σ.M(d) for d ≠ d_new) — the locate-preservation claim refers to that pre-existing slice; the newly seeded empty arrangement is well-defined immediately and yields empty locate for every endset until a subsequent K.μ⁺ extends it. K.λ additionally creates a new link, and the locate and discover_s sets for its *new* endsets are evaluated against the unchanged M for the first time — see SV9 for the resulting monotonic growth of discover_s and SV7 for invariance under every transition *except* K.λ.

  *Corollary (NewLinkEvaluationDefinedness).* For a link a_new allocated by K.λ at Σ → Σ' with Σ'.L(a_new) = (F_new, G_new, Θ_new), every slot s ∈ {from, to, type} and every document d ∈ dom(Σ'.M) yield well-defined values `locate(Σ'.L(a_new).s, d)` and `discover_s(A)` (with a_new admissible to enter) immediately at Σ' — the former by evaluation against the K.λ-unchanged M(d) and the new endset's coverage, the latter by evaluation against the K.λ-extended dom(L). No additional state-priming step is required to read the new link's projection, location, or discoverability; the read is well-defined as soon as K.λ commits.

  *Proof.* The two evaluation forms each decompose into four definedness obligations, each discharged by a one-line citation.

  - *`Σ'.L(a_new)` is defined at Σ'.* K.λ's effect (LinkAllocation, ASN-0047) is exactly `Σ'.L = Σ.L ⊕ {a_new ↦ (F_new, G_new, Θ_new)}`, so a_new ∈ dom(Σ'.L) and Σ'.L(a_new) = (F_new, G_new, Θ_new) immediately at Σ'.
  - *`.s` is well-defined for s ∈ {from, to, type}.* L3 (NEndsetStructure, ASN-0043) requires `|Σ'.L(a_new)| ≥ 3`, and the K.λ-amendment of ASN-0047 records the value as a standard triple `(F_new, G_new, Θ_new)`, so the slot projection `.from`, `.to`, `.type` is defined as the first, second, and third tuple component respectively.
  - *`coverage(Σ'.L(a_new).s)` is a well-defined subset of T.* L4 (EndsetGenerality, ASN-0043) makes each slot value a set of spans over T, and `coverage(e) = ⋃_{(s, ℓ) ∈ e} ⟦(s, ℓ)⟧` is well-defined under T12 (SpanWellDefinedness, ASN-0034) for every span; the union is well-defined as a set operation.
  - *`Σ'.M(d)` is well-defined for d ∈ dom(Σ'.M).* K.λ holds M in frame (per K.λ's per-document frame in ASN-0047: `(A d' :: Σ'.M(d') = Σ.M(d'))`), so `Σ'.M(d) = Σ.M(d)` for every d ∈ dom(Σ.M) = dom(Σ'.M), and `Σ'.M(d)` is well-defined at every d in the post-state arrangement domain.

  These four supply the well-definedness of `locate(Σ'.L(a_new).s, d) = {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(a_new).s)}` immediately at Σ'. For `discover_s(A)` with a_new admissible to enter: `discover_s(A) in Σ' = {a ∈ dom(Σ'.L) : coverage(Σ'.L(a).s) ∩ A ≠ ∅}` is well-defined because dom(Σ'.L) is well-defined (K.λ extends dom(L) by exactly one entry), the coverage of every slot value is well-defined by L4/T12 as above, and set membership against the fixed I-address set A is decidable; whether a_new ∈ discover_s(A) is then determined by `coverage(F_new).s ∩ A ≠ ∅` per the discover_s definition. No state-priming step (between K.λ committing and the evaluation read) is referenced by any of the four citations, so the read is well-defined at the immediate post-state. ∎

(f) *Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the span's action point `k` satisfies `k > p₃` (strictly beyond the third field separator — i.e., the leading `k − 1` components of the span start contain all three field separators, placing the action point structurally within the element field rather than within the node/account/document prefix). [SV6]

*Remark (same-origin coverage growth).* Same-origin coverage growth depends on the allocation regime. At the byte level, sequential sibling allocation closes existing spans whose coverage is fully allocated (tight spans) to future sibling allocations; spans whose reach extends beyond the current allocation maximum remain open to sequential overshoot, and child-depth allocation (TA5(d) with k' > 0) can enter any span containing the parent address. At broader address levels, coverage growth is open by design. See the detailed analysis in the "Content Allocation and Coverage Stability" section.

(g) *Partial survival is well-structured:* the surviving text-subspace projection in any document is the union of *exactly* m · p decomposition terms `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` (some possibly empty), equal as a set to the union of *at most* m · p maximal ordinal-contiguous fragments within mapping blocks. The count inequality is strict whenever (a) some decomposition term is empty or (b) two non-empty terms within a single block are ordinally adjacent or overlap, coalescing into a single maximal fragment. The two-span non-injective worked example below exhibits mechanism (b) — 4 non-empty terms coalescing to 2 maximal fragments — and its three-span extension additionally exhibits mechanism (a), with two empty decomposition terms contributed by a span whose reach lies in an interval disjoint from both block I-extents. The collection is a cover — not necessarily a partition — due to non-injective arrangements. [SV11]

*Caveat — m · p is state-dependent, not a system-level fragment-count invariant.* The bound m · p applies at each state under that state's own values of m and p, not as a fixed quantity across the lifetime of the link or document. The span count m is frozen at link creation by L12 (LinkImmutability), but the block count p is a property of the *current* arrangement M(d): composite edits that fragment an existing block — e.g., a K.μ~ + K.μ⁻ sequence excising interior content, which can replace a single block by two — raise p, and the m · p ceiling at the new state rises accordingly. The same applies in reverse: a composite that merges adjacent blocks lowers p and lowers the ceiling. Two consequences worth recording: (i) one cannot quote a fragment-count upper bound for a link in isolation; the bound must be quoted against the document state at which it is read. (ii) the per-state bound never claims that *some* fragment count survives across transitions — only that whatever count is realised lies under m · p evaluated at the *post*-transition state.

The survivability guarantee is therefore: the link, its endsets, and the content at its endset addresses are all permanent. What varies is the *visibility* of the endset content through each document's arrangement — and this variation is precisely characterised by the projection and resolution functions, which respond only to the arrangement of the specific document being queried and are immune to changes elsewhere.

Nelson's "strap between bytes" is exactly right. The strap (the link's endsets) is permanent, fastened to permanent bytes (I-addresses with immutable content). What moves is the string the bytes sit on — the document's Vstream arrangement. The strap follows the bytes, not the string.


## Properties Introduced

*Withdrawn labels.* SV0, SV1, and SV12 were used in earlier drafts and have been withdrawn during revision: SV0 was demoted to the NoStaleResolutionState architectural remark — its content is a schema inspection rather than a transition-induced survivability claim, and an SV number is no longer attached; SV1's content was absorbed into that architectural remark; SV12's content was absorbed into SV7 (DiscoveryInvarianceUnderLFrame) when transclusion-coupling absence was demoted from a standalone property to a corollary of L-frame invariance. The labels are not reused; the surviving SV labels retain their historical numbering so that external citations (consultations, reviews, downstream ASNs) remain stable.

| Label | Statement | Status |
|-------|-----------|--------|
| π(e, d) | Endset projection: `coverage(e) ∩ ran(M(d))` | introduced |
| locate(e, d) | Endset location: `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` | introduced |
| Resolution | Resolution of endset e in document d is the function `locate(e, d)`; "resolution" throughout the note refers to this function (distinct from "projection" which refers to π(e, d)) | introduced |
| Vitality | Endset e is vital in d when `π(e, d) ≠ ∅` | introduced |
| SlotwiseVitality | Link is slotwise vital in d when each non-empty content endset is vital in d (disjunctive form: `F = ∅ ∨ π(F, d) ≠ ∅` and symmetrically for G) — passes vacuously on empty sides | introduced |
| BilateralVitality | Link is bilaterally vital in d when both content endsets are non-empty *and* each projects non-emptily (`F ≠ ∅ ∧ π(F, d) ≠ ∅` and symmetrically for G) — strict form, Nelson's "anything left at each end" read literally | introduced |
| discover_s(A) | Link discovery: `{a ∈ dom(L) : coverage(L(a).s) ∩ A ≠ ∅}` | introduced |
| Decomposition term | `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` — one per (span, block) pair, contiguous in I(β_k)'s ordinal sequence | introduced |
| Maximal fragment | maximal contiguous ordinal subsequence within a single mapping block's I-extent | introduced |
| NoStaleResolutionState | Architectural remark (not SV-labelled): no state component external to (coverage(e), current M(d)) participates in resolution; caching of historical V-positions is structurally precluded by the link-store and state-schema signatures | introduced |
| ArrangementLinkFrame | Corollary of L12 (ASN-0043): arrangement changes preserve L entirely | cited |
| TransclusionCouplingAbsence | Corollary of SV7: K.μ⁺ extending M(d₂) with v ↦ a (a ∈ ran(M(d₁))) inherits the link set L_a discoverable through a without any link-store coupling step | introduced |
| SV2 | ExtensionMonotonicity: K.μ⁺/K.μ⁺_L can only enlarge π(e, d) and locate(e, d) | introduced |
| SV3 | ContractionReduction: K.μ⁻ can only shrink π(e, d) and locate(e, d) | introduced |
| SV4 | ArrangementIsolation: arrangement changes to M(d) do not affect π(e, d') or locate(e, d') for d' ≠ d | introduced |
| SV5 | ReorderingProjectionInvariance: K.μ~ preserves π(e, d) exactly | introduced |
| SV6 | CrossOriginExclusion: allocations from a different document prefix cannot enter existing endset spans (within element field) | introduced |
| SV7 | DiscoveryInvarianceUnderLFrame: `discover_s(A) in Σ' = discover_s(A) in Σ` for every L-frame elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) and for the distinguished composite K.μ~ — discovery is invariant, not merely monotonic; transclusion-coupling absence is the corollary instance under K.μ⁺ | introduced |
| SV8 | DiscoveryPermanence: once discoverable through A, always discoverable | introduced |
| SV9 | DiscoveryMonotonicity: the discoverable set is non-decreasing as links are created | introduced |
| SV10 | DiscoveryResolutionIndependence: discovery and resolution answer different questions with different filters | introduced |
| SV11 | PartialSurvivalDecomposition: the text-subspace projection equals the union of *exactly* m·p decomposition terms (one per span-block pair, some possibly empty), equivalently the union of *at most* m·p maximal ordinal-contiguous fragments (strict whenever some term is empty or non-empty adjacent/overlapping terms coalesce within a block); the bound m·p is attained iff every (j,k) yields a non-empty term and these terms are pairwise non-adjacent and non-overlapping within each block; the collection is a cover, not necessarily a partition, under non-injective arrangements | introduced |
| SV14 | DocumentDerivedDiscoverySurvivability: discover_through_s(d) is monotonic under K.μ⁺/K.μ⁺_L (a), reduced under K.μ⁻ (b), isolated across documents under K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~ (c), and not permanent — strict shrinkage realised when contraction removes the last V-position carrying a contributing I-address (d) | introduced |
| ContentFidelity | Corollary of S0 (ASN-0036): content at endset I-addresses is immutable | cited |
| CrossDocumentDecoupling | Corollary of SV10: discovery in one document and empty resolution in another are simultaneously realisable (witness extends the SV10 base state with a sibling document and a different-origin I-address) | introduced |
| SV13 | SurvivabilityTheorem: synthesis of the complete guarantee | introduced |
| NewLinkEvaluationDefinedness | Corollary of SV13(e): for a link a_new allocated by K.λ, every slot s and every d ∈ dom(Σ'.M) yield well-defined `locate(Σ'.L(a_new).s, d)` and `discover_s(A)` immediately at Σ' without any state-priming step | introduced |
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
