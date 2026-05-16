# ASN-0051: Link Projection and Discovery Survivability

*2026-03-23*

*Editorial note (revision).* The original title "Link Projection Displacement" did not match the body, which formalises no "displacement" concept. The retitle "Link Projection and Discovery Survivability" reflects what the body actually develops — the survivability of a link's projection (where its endset content appears in a document's arrangement) and of its discovery (which links a content query reaches), under elementary state transitions. The inquiry's framing question — "what survives, what changes, and what can a link holder rely on?" — is the survivability question, and the SV-labelled claims throughout (SV0–SV13) are the survivability properties. The filename `ASN-0051-link-projection-displacement.md` is retained for stability of external references and lattice paths.

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

The two are related by M(d)'s function property (S2, ArrangementFunctionality): for all v ∈ dom(M(d)), v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d). The restriction to dom(M(d)) is essential — M(d)(v) is undefined when v ∉ dom(M(d)), so the biconditional is well-formed only on this domain; and locate(e, d) ⊆ dom(M(d)) by definition, so no V-position outside dom(M(d)) is lost to the relation. Since M(d) need not be injective — within-document sharing is permitted (S5, UnrestrictedSharing) — we may have |locate(e, d)| ≥ |π(e, d)|. Multiple V-positions in d can show the same I-address, and a reader sees each occurrence.

We observe that locate(e, d) is fully determined by two quantities: coverage(e), which is fixed at link creation by L12 (LinkImmutability), and M(d), which is the document's current arrangement at the moment of evaluation. No prior V-position is retained; no creation-time arrangement participates. The resolution is always *fresh* — computed from the current state.

This observation is definitional — locate is defined as `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`, so the input dependency is built into the function itself. The substantive claim worth stating is about *what the algebra forbids*: no state component external to (coverage(e), M(d)) participates in resolution, because no such component exists in the link store.

**SV0 (NoStaleResolutionState).** *Schema observation, not derivation.* SV0 records a property of the state-space Σ and the transition system K that is read off directly from the foundation definitions. Each of clauses (i)–(iii) below is a *citation* of an existing schema fact; the meta-observation that follows is an *inspection* of which inputs a function defined over Σ can possibly consult, not a theorem requiring proof. We label SV0 with an SV number because its survivability content matters to a link holder reasoning about resolution; we do not equip it with a proof because none is required.

*Schema citations.*

(i) *Link-store signature [L3, ASN-0043; K.λ, ASN-0047].* The link value Σ.L(a) = (F, G, Θ) stores I-space content only — endsets are sets of spans (s, ℓ) over T (L3, TripleEndsetStructure). No V-address, no per-document arrangement, no creation-time snapshot is recorded in the link value at allocation (K.λ).

(ii) *State-schema closure [Σ = (C, L, E, M, R), ASN-0047].* The extended state is Σ = (C, L, E, M, R). M(d) is the *current* arrangement; no component carries a historical M_k. R holds per-mapping provenance over I-addresses only (J0/J1/J1★, ASN-0047), not over V-addresses. The schema admits no auxiliary V-cache field.

(iii) *Operational closure [K = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}, ASN-0047].* No elementary transition writes a V-address into Σ.L, into a link value, or into any historical-M slot — direct inspection of each transition's effect (ASN-0047) confirms this. There is consequently no operation that *could* establish a stale V-position field, even if one were notionally desired.

*Meta-observation — every conforming resolution function depends on Σ only through (Σ.L applied to extract coverage(e), Σ.M(d)).* This is not a derivation; it is an inspection of what (i)–(iii) make available. A function R(Σ, e, d) defined over the schema described by those clauses can consult only the components those clauses name. The schema contains no historical M_k, no V-cache, no per-link arrangement snapshot — there is nothing for a resolution function to read that would yield a stale V-position. Since coverage(e) is determined directly by the endset argument e when e is supplied as a set of spans, the dependence reduces further to (e, Σ.M(d)).

The substantive content of SV0 is *architectural*: a naive implementation might intend to cache V-positions at link creation time, leaving stale entries when the document is rearranged. SV0 records that this is *structurally precluded* by the link-store and state-schema signatures of (i)–(iii) — there is no field in which a stale V-position could persist, and no transition that could populate one. The corresponding functional fact about locate is the immediate definitional reading: `Σ₁.M(d) = Σ₂.M(d) ⇒ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)` for any endset e, since `locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` references only M(d) and the supplied endset. No L-equality precondition is needed — and adding one would carry no force, since locate does not consult Σ.L. The architectural content of SV0 is what guarantees this functional triviality is not undermined by some schema field we forgot about.

**Definition — Endset Vitality.** An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, locate(e, d) ≠ ∅.

*Scoping note.* For the remainder of this note we work within the standard-triple framework of ASN-0043: every link value is treated as Σ.L(a) = (F, G, Θ) — from-endset F, to-endset G, type-endset Θ — which is the arity-3 floor admitted by L3 (NEndsetStructure, ASN-0043). L3 admits higher-arity links with |Σ.L(a)| ≥ 3; treatment of those additional endset slots is deferred to ASN-0043. All claims below — bilateral vitality, SV2–SV13, the wp analysis — are stated for the standard triple; the generalisation to arity N > 3 follows the same projection/discovery machinery applied slot-wise, with content/type slot status determined by L3's slot-3 convention.

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d — that is, every non-empty endset projects to at least one I-address in d's arrangement:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(We exclude the type endset from the vitality condition because type endsets may reference addresses outside dom(Σ.C), per L9, TypeGhostPermission.)

*Term scope.* The word "bilateral" refers to the link's two content slots F and G. The substantive content of bilateral vitality arises when both slots are non-empty — only then does the conjunction impose a non-trivial requirement on each side. When one or both content endsets are empty, the corresponding disjunction is satisfied by its left branch — this is *degenerate satisfaction* of the formal condition, not a substantive claim of vitality on the empty side, where there is no side to be vital on. We state the degenerate cases explicitly so that subsequent usage of "bilaterally vital" need not carry separate side-conditions, but the reader should not read those cases as asserting that an empty endset is "vital" in any substantive sense.

*Both endsets empty (vacuous case).* When F = ∅ and G = ∅, both disjunctions are satisfied by their left branches, so the link (∅, ∅, Θ) — a pure type annotation with no content endpoints — counts as bilaterally vital in every document by degenerate satisfaction. The term "bilateral" is vacuous here: there are no content sides on which vitality could be substantive. The link has no content associations to lose, so its formal vitality status is trivially true; no claim about endpoint visibility is being made. The interesting cases arise when at least one content endset is non-empty.

*Asymmetric empty endsets.* The asymmetric cases — exactly one of F, G empty — likewise rest on degenerate satisfaction of the disjunction on the empty side. When F = ∅ but G ≠ ∅, coverage(F) = ∅, so π(F, d) = ∅ ∩ ran(M(d)) = ∅ and locate(F, d) = ∅ for every document d. The from-endset is non-vital in every document, but bilateral vitality requires only that the non-empty endset G be vital — the disjunction `F = ∅ ∨ π(F, d) ≠ ∅` is satisfied by its left branch. The substantive content of the predicate reduces here to the unilateral claim that G is vital in d; the term "bilateral" overstates what is being asserted, since only one side carries content and only that side carries a vitality claim. Such a link is unidirectional in its content anchoring; it asserts an association anchored only at G. The symmetric case (F ≠ ∅, G = ∅) is identical with the roles of F and G interchanged. More generally, the empty case warrants explicit treatment, and it presents differently for projection/location (whose arguments include an *endset* e) than for discovery (whose argument is an *address set* A, not an endset). *Empty endset.* For any endset e with coverage(e) = ∅: π(e, d) = coverage(e) ∩ ran(M(d)) = ∅ ∩ ran(M(d)) = ∅, and locate(e, d) = ∅, in every document d. *Empty coverage on the link side, for discovery.* Since discover_s takes an address set A and filters links by `coverage(L(a).s) ∩ A ≠ ∅`, the analogue of the empty-endset case here concerns a *link* a ∈ dom(Σ.L) whose slot-s endset has empty coverage: for a link a with coverage(Σ.L(a).s) = ∅, a ∉ discover_s(A) for any A, since coverage(Σ.L(a).s) ∩ A = ∅ ∩ A = ∅. (Separately, on the query side, discover_s(∅) = ∅ in any state — for every a ∈ dom(Σ.L), coverage(Σ.L(a).s) ∩ ∅ = ∅, so the membership condition fails universally.) The substantive survivability analysis below concerns the non-trivial case where the queried endset is non-empty for π and locate, and where both the link's slot coverage and the query address set are non-empty for discover_s; the empty cases are stated explicitly here so that subsequent formulas need not carry empty-endset side conditions.

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

Proof: π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (L12, ASN-0043) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺/K.μ⁺_L effect — both transitions extend dom(M(d)) while preserving existing V↦I mappings, so the post-state range contains the pre-state range), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

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

*Precondition.* The span start s and the candidate address b are *T4-valid* element-level tumblers — they admit the hierarchical parsing of T4 (HierarchicalParsing, ASN-0034) into the projections (N, U, D, E), with element-level depth zeros(s) = zeros(b) = 3 placing each address in the element field per T4b (UniqueParse, ASN-0034). T4-validity ensures the projections N(s), U(s), D(s), N(b), U(b), D(b) are well-defined, and consequently `origin(s) = N(s).0.U(s).0.D(s)` and `origin(b) = N(b).0.U(b).0.D(b)` are well-defined (per the origin definition in ASN-0036, which presupposes T4-valid element-level arguments). L4 (EndsetGenerality, ASN-0043) permits non-element-level span starts, but the origin-based exclusion applies only when the start is a T4-valid element-level tumbler. The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently, the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`. This ensures the action point falls within the element field — beyond all three field separators.

*Proof.* Let k be the action point of ℓ, with k > p₃ as stated. By TumblerAdd, components before k are copied from s, and (s ⊕ ℓ)ₖ = sₖ + ℓₖ, so s and s ⊕ ℓ agree on positions 1 through k−1. Consider any t with s ≤ t < s ⊕ ℓ.

*Sub-lemma (no early divergence).* t cannot first diverge from s at any position j < k. Suppose for contradiction that the first position where tⱼ ≠ sⱼ is some j with j < k.

*Prefix exclusion (#t ≥ j, so T1(i) applies).* T1(i) requires both t and s to have a component at position j. Span well-formedness (ASN-0034, span precondition `actionPoint(ℓ) ≤ #s`) gives k ≤ #s, so j < k ≤ #s and sⱼ is well-defined. For tⱼ, suppose for contradiction that #t < j. Then t and s agree on every position 1 through #t (because j is the *first* position of divergence and #t < j), and #t < j ≤ #s, so t is a proper prefix of s. By T1(ii) (a proper prefix is strictly less in the lex order), t < s — contradicting s ≤ t. Hence #t ≥ j, so tⱼ is well-defined.

*Divergence is upward.* Since t ≥ s and t agrees with s on positions 1 through j−1, T1(i) gives tⱼ > sⱼ. By TumblerAdd, (s ⊕ ℓ)ⱼ = sⱼ for j < k. Since t and s ⊕ ℓ each agree with s on positions 1 through j−1, and s ⊕ ℓ agrees with s on positions 1 through k−1 (with j−1 < k−1), the first divergence of t and s ⊕ ℓ is at position j with tⱼ > sⱼ = (s ⊕ ℓ)ⱼ. By T1(i), t > s ⊕ ℓ — contradicting t < s ⊕ ℓ. □

The two structural conclusions follow as parallel applications of the sub-lemma:

(a) *#t ≥ k.* Suppose #t < k. Then the sub-lemma excludes any first-divergence at j ≤ #t < k, so t agrees with s on all positions 1 through #t — making t a proper prefix of s, hence t < s by T1(ii), contradicting s ≤ t.

(b) *t agrees with s on positions 1 through k−1.* If t did not agree with s on some position in [1, k−1], the first such position would be a divergence at some j < k — excluded by the sub-lemma.

Since k > p₃, the first k−1 positions of t include all three field-separator positions of s — call them p₁, p₂, p₃ (the positions where sᵢ = 0). Because t agrees with s on positions 1 through k−1, we have t_{p₁} = t_{p₂} = t_{p₃} = 0, so t has at least three zero components, all located within positions 1 through k−1: zeros(t) ≥ 3, with at least three zeros at positions p₁, p₂, p₃.

*Restricting to element-level t.* For element-level t — those with zeros(t) = 3 — the inequality is tight. The three zeros at p₁, p₂, p₃ already account for all zero components of t, so t has *exactly* three zeros and they sit at exactly the positions p₁, p₂, p₃. In particular, no zero component lies at any position j with k ≤ j ≤ #t — every component beyond position k − 1 is nonzero.

*T4-validity of t.* The origin function `origin(t) = N(t).0.U(t).0.D(t)` (ASN-0036, S7) presupposes that t is T4-valid — no adjacent zeros, t₁ ≠ 0, t_#t ≠ 0 (T4, ASN-0034). We verify each conjunct from properties established above:
- *t₁ ≠ 0.* Position 1 lies in [1, k − 1] (since k > p₃ ≥ 6, so k ≥ 7 ≥ 2). Conclusion (b) gives t₁ = s₁, and s is T4-valid, so t₁ = s₁ ≠ 0.
- *t_#t ≠ 0.* By conclusion (a), #t ≥ k, so position #t lies in [k, #t] — the element-field range. Every component in that range is nonzero (since the three zeros of element-level t are confined to p₁, p₂, p₃ ≤ k − 1), so t_#t ≠ 0.
- *No adjacent zeros.* Positions 1 through k − 1 inherit s's no-adjacent-zeros property since t agrees with s on that range (conclusion (b)) and s is T4-valid. Positions k through #t are all nonzero, so no pair of adjacent positions in [k, #t] is doubly zero. The only remaining boundary is the pair (k − 1, k): if t_{k−1} = 0 — i.e., k − 1 is one of p₁, p₂, p₃ — then t_k lies in the element field and is nonzero, so the pair is not doubly zero.

So t is T4-valid, and origin(t) is well-defined. The field decomposition of t — the partition of its components by the three field-separator positions p₁, p₂, p₃ — matches the field decomposition of s component-by-component up to position p₃. The first three fields (node, user, document) of t are identical to those of s, so origin(t) = N(t).0.U(t).0.D(t) = N(s).0.U(s).0.D(s) = origin(s) (per the origin definition in ASN-0036, S7).

Since b is element-level (S7b — `zeros(b) = 3`), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s), the contrapositive gives: any element-level b with origin(b) ≠ origin(s) satisfies b ∉ ⟦(s, ℓ)⟧. ∎

*Note.* T5 gives the weaker result origin(s) ≼ t for every t in the interval, but this prefix containment does not force separator positions to align — the sandwich argument above establishes the stronger claim.

*Note on scope — what k ≤ p₃ permits.* The precondition k > p₃ is not a technical artifact of the proof; it tracks a structural feature of the tumbler field layout that the proof relies on. When k ≤ p₃, the action-point lies at or before the third field separator, so reach = s ⊕ ℓ can advance a component within s's document-prefix — placing reach in a different prefix-field configuration from s, with the interval [s, reach) covering tumblers whose own document-prefix components differ from those of s. Such tumblers have different origin values, and SV6's exclusion does not apply to them. This is by design: Nelson's docuverse admits spans whose endpoints lie at server, account, or document field positions, with the interval implicit between them — "There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25] — so that a span "may range in possible size from one byte to the whole docuverse on the whole network" [LM 4/24]. A k ≤ p₃ span is the formal vehicle for broader-level coverage: the same span machinery, applied with an action-point inside the document-prefix region rather than within the element field, yields the cross-document, cross-account, or cross-node reach that the design contemplates. The boundary at k = p₃ — between element-field action-points (covered by SV6) and document-prefix-or-earlier action-points (broader-level spanning) — is *structurally consequential but not nominally designated* in Nelson's writing. It emerges from the field structure (four fields separated by three major dividers, with the third divider at position p₃ between Document and Element [LM 4/26, LM 4/28]) rather than being introduced by Nelson as a named action-point boundary; the boundary is a consequence of the field layout, not a stipulation about where action-points may sit. Detailed treatment of broader-level spans is deferred to ASN-0034's allocator and address-hierarchy machinery.

This property is robust — it depends only on the structural separation of document-level prefixes, not on any allocation discipline.

**Same-origin coverage growth.** Under the same document prefix, two mechanisms can place a new I-address within an existing endset span's denotation. *Scope.* We make no formal SV claim about same-origin coverage growth in this ASN. The analysis below is descriptive: it identifies the mechanisms (sequential overshoot, child-depth entry) by which TA5 and T10a allocations can enter existing endset coverage under a shared document prefix, but the precise allocator-discipline conditions that determine *which* same-origin allocations enter *which* spans are deferred to the allocator-discipline treatment in ASN-0034. The descriptive content here motivates the SV6 formal exclusion at element-level depth from cross-origin allocations and clarifies why endset coverage stability is *architectural*, not definitional.

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

We observe that discover_s is defined purely as a function of an I-address set — it is parameterised by I-addresses, not by document-V-region pairs. So identical I-address sets trivially yield identical discovery results. The interesting consequence is not this definitional fact but the *discovery invariance under L-frame transitions* it entails — and, as a corollary, the *transclusion discovery guarantee* that follows from instantiating that invariance to K.μ⁺.

**SV7 (DiscoveryInvarianceUnderLFrame).** For every elementary transition Σ → Σ' that holds L in frame — K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ — and for every fixed set of I-addresses A:

`discover_s(A) in Σ' = discover_s(A) in Σ`

*Proof.* Each L-frame transition holds dom(L') = dom(L) and L'(a) = L(a) for all a ∈ dom(L). Therefore coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) for every a ∈ dom(Σ.L), and dom(Σ'.L) = dom(Σ.L). Both inputs to discover_s — coverage and dom(L) — are identical in Σ and Σ', so the discovery sets are equal. ∎

The claim is an equality, not merely monotonicity: no L-frame transition introduces new discovery relationships and none removes any. The discovery mechanism itself — discover_s operating on coverage and dom(L) — is coupling-free under L-frame: the link store is untouched, and the I-address inputs to coverage are fixed by L12. The only elementary transition that can change discover_s is K.λ, which adds a new link to dom(L) and yields the strict inclusion recorded in SV9.

*Corollary (TransclusionCouplingAbsence).* When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself: by SV7 instantiated to K.μ⁺, discover_s(A) is unchanged across the transition for every A, so d₂ inherits every link association of a without any additional link-store operation. The same reasoning applies to forking (J4): the new version shares I-addresses with the source by the fork's K.μ⁺ step, so it discovers the same links for all shared content without explicit link propagation. This is the architecturally significant application of SV7 — the equality has substantive consequence for transclusion and versioning because arrangement extension provides the I-address sharing that enables discovery in the new document. (A valid composite transition containing K.μ⁺ may additionally require K.ρ to satisfy J1★ (ExtensionRecordsProvenanceContent, ASN-0047), but K.ρ modifies R only — it does not alter L or M, so the discovery result is unaffected; SV7 covers K.ρ directly as one of the L-frame transitions.)

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

*Concrete witness.* We exhibit a state Σ, link a, document d, slot s = from, and V ⊆ dom(Σ.M(d)) satisfying the existential. Take origin O = 1.0.1.0.1 and three element-level sibling addresses i₁ = O.0.1.1, i₂ = O.0.1.2, i₃ = O.0.1.3 — each T4-valid with zeros(i_k) = 3 (the three zeros sit at positions 2, 4, 6, all in the prefix), origin(i_k) = N(i_k).0.U(i_k).0.D(i_k) = 1.0.1.0.1 = O, and element field E(i_k) = [1, k] of length 2 (satisfying S7c, ASN-0036, which requires #E(a) ≥ 2 for every a ∈ dom(Σ.C)). Let s_span = i₁ and ℓ_span = 0.0.0.0.0.0.0.3 (action point k = 8, the first nonzero component, with k = 8 > 6 = p₃ so the action point lies strictly within the element field). Then s_span ⊕ ℓ_span: positions 1–7 are copied from s_span (yielding 1.0.1.0.1.0.1), and position 8 advances by 3 (1 + 3 = 4), so the reach is s_span ⊕ ℓ_span = 1.0.1.0.1.0.1.4 = O.0.1.4. The span coverage `⟦(i₁, ℓ_span)⟧ = {t : i₁ ≤ t < O.0.1.4}` contains the element-level allocated addresses i₁, i₂, i₃ — each agrees with i₁ on positions 1–7 and has position-8 value in {1, 2, 3} ⊆ [1, 4). Set Σ.M(d) = {v₁ ↦ i₂}, and let a ∈ dom(Σ.L) carry F = {(i₁, ℓ_span)} so coverage(F) ⊇ {i₁, i₂, i₃} ∋ i₂. Then with V = {v₁} and A = {Σ.M(d)(v₁)} = {i₂}:

- *Discovery succeeds:* coverage(F) ∩ A = {i₂} ≠ ∅, so a ∈ discover_from(A).
- *Projection is proper:* π(F, d) = coverage(F) ∩ ran(Σ.M(d)) = coverage(F) ∩ {i₂} = {i₂}, but coverage(F) ⊇ {i₁, i₂, i₃} ⊋ {i₂}, so π(F, d) ⊊ coverage(F).

The link is discoverable through d via the shared address i₂, yet resolves to only that one I-address — i₁ and i₃ remain in coverage(F) but are absent from ran(Σ.M(d)). ∎

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

*Derivation of the formula.* The endset's coverage decomposes as `coverage(e) = ⋃_{j=1}^{m} ⟦(sⱼ, ℓⱼ)⟧` (L3/L4, ASN-0043: the endset is a set of spans and its coverage is the union of their denotations). The text-subspace range decomposes as `ran_text(M(d)) = ⋃_{k=1}^{p} I(β_k)` (B1 applied to the restriction together with M11/M12, ASN-0058: the block decomposition's I-extents exhaust the content-subspace range). Substituting both into π_text(e, d) = coverage(e) ∩ ran_text(M(d)) and distributing intersection over union (set algebra, applied twice):

`π_text(e, d) = (⋃_j ⟦(sⱼ, ℓⱼ)⟧) ∩ (⋃_k I(β_k)) = ⋃_j ⋃_k (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

— which is the formula stated above. The remainder of this section establishes the structural properties of the m · p decomposition terms: each is contiguous within its block's ordinal sequence (S0 convexity, below), the terms may overlap or coalesce into fewer maximal fragments (fragment-count discussion), and the collection forms a cover rather than a partition under non-injective arrangements.

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

*Two-span, non-injective scenario.* The preceding subcases used a single span (m = 1) and an injective arrangement. We now exercise SV11 with m = 2 spans and a non-injective Σ.M(d) to expose the cover-not-partition behaviour and the m · p decomposition bound.

Re-take the initial five-address content store with a₁ < a₂ < a₃ < a₄ < a₅ all sharing one origin and one tumbler length. Extend the document's arrangement with two additional V-positions v₆, v₇ that share I-addresses with v₂ and v₃ (within-document sharing, S5):

`M(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₃, v₄ ↦ a₄, v₅ ↦ a₅, v₆ ↦ a₂, v₇ ↦ a₃}`

with v₁ < v₂ < v₃ < v₄ < v₅ < v₆ < v₇. The maximally merged block decomposition of this restriction has p = 2 blocks: β₁ = (v₁, a₁, 5) covering v₁..v₅ with I-extent {a₁, a₂, a₃, a₄, a₅}, and β₂ = (v₆, a₂, 2) covering v₆..v₇ with I-extent {a₂, a₃}. The block boundary at v₅ → v₆ is enforced by a discontinuity in M(d)'s I-address sequence (a₅ → a₂ is not a +1 step), forcing M12's split rule. The two blocks share I-addresses {a₂, a₃} — this is the non-injective signature.

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

*Cross-origin exclusion (SV6).* We now verify SV6 with explicit tumbler values. Let s = 1.0.1.0.1.0.1.2.3 — nine components; the zeros at positions 2, 4, 6 are field separators, so p₃ = 6. Let ℓ = 0.0.0.0.0.0.0.0.5 — action point k = 9 (the first nonzero component), and k = 9 > 6 = p₃. By TumblerAdd, positions 1 through 8 are copied from s, and position 9 advances: reach = s ⊕ ℓ = 1.0.1.0.1.0.1.2.8. We verify the sandwich: reach agrees with s on positions 1 through 8, confirming that the three field separators (positions 2, 4, 6) are preserved.

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

- **wp(K.μ⁻ removing V_rm ⊆ dom(Σ.M(d)), π(e, d) ≠ ∅) = `(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(e))`** — *under the domain-of-applicability precondition that V_rm is D-SEQ-admissible:* for every subspace S, V_rm ∩ V_S(d) is either an upward tail `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` of V_S(d) for some 0 ≤ n'_S ≤ n_S, or empty (D-SEQ, ASN-0047). Arbitrary V_rm that violate D-SEQ are not valid K.μ⁻ parameters in the first place — the transition is not enabled — and the wp expression is meaningful only on the admissible parameter space. So K.μ⁻ removes a non-empty set V_rm of V-positions from the maximum end of V_S(d) per subspace, as enforced by D-SEQ, and vitality is preserved iff some V-position *not* in V_rm carries an I-address in coverage(e). The contrapositive — the *vitality-loss* condition — is `(A v : v ∈ dom(Σ.M(d)) \ V_rm :: Σ.M(d)(v) ∉ coverage(e))` together with `(E v : v ∈ V_rm : Σ.M(d)(v) ∈ coverage(e))` (so the endset was vital pre-transition but every contributing V-position was removed). Both conjuncts are pre-state predicates over Σ and the D-SEQ-admissible removal parameter V_rm. This is Nelson's "if anything is left at each end" condition in formal dress.

- **wp(K.μ⁺ adding extension Δ = M'(d) ↾ (dom(M'(d)) \ dom(Σ.M(d))) with new I-address set I_new = ran(Δ) ⊆ dom(Σ.C), π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ coverage(e) ∩ I_new ≠ ∅`** where Δ is the set of new V↦I mappings introduced by the transition (K.μ⁺ in ASN-0047 admits any extension `dom(M'(d)) ⊃ dom(M(d))` with value preservation at existing positions, so Δ may contain one or many new mappings; the precondition `(A v ∈ dom(Δ) : Δ(v) ∈ dom(Σ.C))` is required by K.μ⁺'s referential integrity). Extension preserves vitality if it already held in the pre-state *or* if at least one new I-address lies in coverage(e). The single-mapping specialisation Δ = {(v_new, i_new)} yields I_new = {i_new} and the formula reduces to `π(e, d) ≠ ∅ ∨ i_new ∈ coverage(e)`. For the typical case of an endset already vital before the extension, the first disjunct is satisfied and the wp reduces to the pre-state vitality regardless of the size of Δ.

- **wp(K.μ⁺_L adding v_ℓ ↦ ℓ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ ℓ ∈ coverage(e)`** where ℓ is the link address added by the transition. For endsets whose coverage lies entirely in dom(Σ.C) (the typical content endset), the second disjunct is unreachable and the wp reduces to pre-state vitality.

- **wp(K.μ~ under bijection ψ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`.** Reordering preserves ran(M(d)) (SV5), so the precondition is identical to the postcondition and does not depend on ψ.

- **wp(K.α, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.δ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** (for any d carried over by the frame) and **wp(K.ρ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** and **wp(K.λ, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅`** for every pre-existing endset e. Each of these transitions preserves M in its frame, so π is unchanged for every endset that existed prior to the transition.

The aggregate observation: only K.μ⁻ can falsify vitality, and only by a specific characterised action — every pre-state V-position contributing to coverage(e) being among the set V_rm removed by the contraction. Every other elementary transition either trivially preserves vitality (M-frame: K.α, K.δ, K.λ, K.ρ, K.μ~) or can only enlarge the projection (K.μ⁺, K.μ⁺_L). The wp framework therefore localises the *single* operation that places vitality at risk and gives the *exact* pre-state condition under which the risk materialises.

For discovery, the corresponding wp values follow the same pattern with discover_s in place of π. Because discover_s depends only on coverage(e) and dom(Σ.L), every transition that holds L in frame preserves discover_s pointwise:

- **wp(K, a ∈ discover_s(A)) = `a ∈ discover_s(A)`** for every K ∈ {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} and every fixed A. Discovery is invariant under arrangement and content operations.

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
- Reordering of M(d) preserves π(e, d); locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)} where ψ is the reordering bijection from K.μ~. The locate *set* may change. [SV5]
- Changes to M(d) cannot affect locate(e, d') for d' ≠ d. [SV4]
- K.α, K.δ, K.ρ preserve M in their frame, so locate(e, d) is unchanged for every existing endset e.
- K.λ (LinkAllocation) has a dual character. It preserves M in its frame (every existing v ↦ i mapping in M(d) for every d), so locate(e, d) is unchanged for every endset e that existed prior to the transition. But K.λ also adds a new entry to dom(L) — extending the link store by exactly one new link with endsets (F_new, G_new, Θ_new) — and the locate sets of those *new* endsets come into existence for the first time, evaluated against the unchanged M. Resolution for previously-existing endsets is invariant under K.λ; resolution for newly-created endsets is computed against the current M for the first time. Discovery exhibits the same duality: discover_s(A) is invariant under K.λ for any A that does not require the new link (a ∈ discover_s(A) in Σ implies a ∈ discover_s(A) in Σ'), and may gain a new member (the newly-allocated link) when coverage(L_new.s) ∩ A ≠ ∅. SV9 records the resulting monotonic growth of discover_s; SV7 captures invariance under every transition *except* K.λ.

(f) *Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field. [SV6]

*Remark (same-origin coverage growth).* Same-origin coverage growth depends on the allocation regime. At the byte level, sequential sibling allocation closes existing spans whose coverage is fully allocated (tight spans) to future sibling allocations; spans whose reach extends beyond the current allocation maximum remain open to sequential overshoot, and child-depth allocation (TA5(d) with k' > 0) can enter any span containing the parent address. At broader address levels, coverage growth is open by design. See the detailed analysis in the "Content Allocation and Coverage Stability" section.

(g) *Partial survival is well-structured:* the surviving text-subspace projection in any document is the union of *exactly* m · p decomposition terms `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` (some possibly empty), equal as a set to the union of *at most* m · p maximal ordinal-contiguous fragments within mapping blocks. The count inequality is strict under coalescence — when adjacent or overlapping decomposition terms within a block merge into fewer maximal fragments, as exhibited by the two-span non-injective worked example (4 decomposition terms coalescing to 2 maximal fragments). The collection is a cover — not necessarily a partition — due to non-injective arrangements. [SV11]

The survivability guarantee is therefore: the link, its endsets, and the content at its endset addresses are all permanent. What varies is the *visibility* of the endset content through each document's arrangement — and this variation is precisely characterised by the projection and resolution functions, which respond only to the arrangement of the specific document being queried and are immune to changes elsewhere.

Nelson's "strap between bytes" is exactly right. The strap (the link's endsets) is permanent, fastened to permanent bytes (I-addresses with immutable content). What moves is the string the bytes sit on — the document's Vstream arrangement. The strap follows the bytes, not the string.


## Properties Introduced

*Withdrawn labels.* SV1 and SV12 were used in earlier drafts and have been withdrawn during revision: SV1's content was absorbed into the SV0 (NoStaleResolutionState) statement, and SV12's content was absorbed into SV7 (DiscoveryInvarianceUnderLFrame) when transclusion-coupling absence was demoted from a standalone property to a corollary of L-frame invariance. The labels are not reused; the surviving SV labels retain their historical numbering so that external citations (consultations, reviews, downstream ASNs) remain stable.

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
| SV7 | DiscoveryInvarianceUnderLFrame: `discover_s(A) in Σ' = discover_s(A) in Σ` for every L-frame elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) — discovery is invariant, not merely monotonic; transclusion-coupling absence is the corollary instance under K.μ⁺ | introduced |
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
