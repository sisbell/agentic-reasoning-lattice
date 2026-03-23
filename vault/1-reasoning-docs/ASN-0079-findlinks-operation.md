# ASN-0079: FINDLINKS Operation

*2026-03-23*

We are looking for a specification of link discovery — the operation that, given constraints on content identity, finds every link whose endsets reference the queried content. The reader's question is always some variant of "what connects here?" The formal question is: given a set of I-addresses, which links in the system reference any of them, and what guarantees govern completeness of the answer?

We write Σ = (C, L, E, M, R) for the system state (ASN-0047). A link at address a ∈ dom(Σ.L) has value Σ.L(a) = (F, G, Θ) — three endsets (L3, ASN-0047). Each endset is a finite set of spans; the *coverage* of endset e is coverage(e) = (∪ σ : σ ∈ e : ⟦σ⟧) (ASN-0043). The *home document* of a link at address a is home(a) = origin(a), the document-level prefix of a (L1a, L2, ASN-0043).

## From Visible Content to Content Identity

The reader selects content by pointing at a region of her document's Vstream — a V-span σ = (u, ℓ) in document d. But links do not attach to V-positions. They attach to I-addresses: endsets are span-sets over the Istream (L4, ASN-0043). Before any link search can begin, the reader's visible selection must be translated into the I-addresses it references.

This translation is the *resolution* of ASN-0058. Given a well-formed content reference (d, σ), resolution yields resolve(d, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ — an ordered sequence of I-address runs, each representing nⱼ contiguous I-addresses starting at aⱼ. We define the I-address set of the resolution:

  addresses(d, σ) = (∪ j : 1 ≤ j ≤ k : {aⱼ + i : 0 ≤ i < nⱼ})

By C1 (ResolutionIntegrity, ASN-0058), every address in this set belongs to dom(C). By C2 (ResolutionWidthPreservation, ASN-0058), the total count equals the span width ℓₘ. The resolution captures the *content identity* of the selected region — the permanent I-addresses underlying the ephemeral V-positions.

When the V-span covers content drawn from multiple original sources — a compound region assembled by transclusion — the resolution produces k > 1 runs with disjoint I-address ranges. Each run corresponds to one mapping block in the maximally merged decomposition (M11, M12, ASN-0058). The link search must handle this disjoint set as a single query.

We observe a fundamental property of the resolution step.

**F0 — ResolutionIdentityInvariance.** Let I-address a satisfy a ∈ ran(M(d₁)) ∩ ran(M(d₂)) — the same content appears in two documents (via transclusion). If v₁ ∈ dom(M(d₁)) with M(d₁)(v₁) = a, and σ₁ is any well-formed content reference spanning v₁, then a ∈ addresses(d₁, σ₁). Identically for d₂. The resolution is transparent to the viewing document — identical content produces identical I-addresses regardless of which arrangement it is viewed through.

This transparency is not a special rule for transclusion. It is a direct consequence of the two-stream separation (S9, ASN-0036): content identity lives in the Istream, arrangement lives in the Vstream, and the two are independent. The resolution step merely reveals the identity that was always there.

## The Search Specification

We now formalize the query that FINDLINKS accepts.

**Definition — SearchConstraint.** A *search constraint* is either ⊤ (unconstrained — matches any endset) or a non-empty finite set P ⊂ T.

The addresses in P need not belong to dom(C). For from-endset and to-endset queries, P is typically derived from a content reference via resolution, yielding I-addresses in dom(C). For type-endset queries, P may contain type addresses that fall outside dom(C) ∪ dom(L) entirely — L9 (TypeGhostPermission, ASN-0043) permits type endsets to reference such addresses, and L10 (TypeHierarchyByContainment, ASN-0043) uses prefix spans over the type-address space. The specification does not constrain how P is obtained — only how it is evaluated against endsets.

**Definition — HomeConstraint.** A *home constraint* is either ⊤ (the entire link store) or a non-empty set H ⊆ E_doc of document identifiers.

**Definition — QuerySpecification.** A *query specification* is a tuple Q = (H, S₁, S₂, S₃) where H is a home constraint and S₁, S₂, S₃ are search constraints. By the standard triple convention (ASN-0043), S₁ constrains the from-endset, S₂ the to-endset, S₃ the type-endset.

The typical use: the reader resolves her V-selection to I-addresses P = addresses(d, σ) and issues Q = (⊤, P, ⊤, ⊤) — "find all links whose from-endset touches this content, from anywhere." Or Q = (⊤, ⊤, P, ⊤) — "find all links pointing *to* this content." The four parameters provide a unified mechanism for all search patterns.

## The Satisfaction Predicate

We are looking for the predicate that determines whether a link matches a query. The design intent is intersection-based: a link matches when its endsets *touch* the query regions. Nelson's specification uses the phrase "all or any part of" each constraint. The formal content of this phrase is non-empty intersection.

**Definition — EndsetSatisfaction.** An endset e *satisfies* search constraint S:

  sat(e, ⊤) ≡ true

  sat(e, P) ≡ coverage(e) ∩ P ≠ ∅          when P ≠ ⊤

The unconstrained case is trivially satisfied. The constrained case requires at least one I-address in the endset's coverage to belong to the query set. When e = ∅, coverage(e) = ∅, so sat(∅, P) = false for every P ≠ ⊤: a link with an empty endset in slot i is invisible to any constrained query on that slot, though it remains discoverable by the fully unconstrained query (⊤, ⊤, ⊤, ⊤). Expanding coverage in terms of spans:

  coverage(e) ∩ P ≠ ∅  ≡  (E (s, ℓ) ∈ e : ⟦(s, ℓ)⟧ ∩ P ≠ ∅)

At least one span in the endset must share at least one I-address with the query set. This is the "OR" within an endset — any single matching span sufficing.

**F1 — SatisfactionPredicate.** A link at address a ∈ dom(Σ.L) with value Σ.L(a) = (F, G, Θ) *satisfies* query Q = (H, S₁, S₂, S₃) iff:

  satisfies(a, Q) ≡ (H = ⊤ ∨ home(a) ∈ H)
                     ∧ sat(F, S₁)
                     ∧ sat(G, S₂)
                     ∧ sat(Θ, S₃)

This is the *conjunctive composition* — the "AND" across endsets. Every constraint must be independently satisfied: the home constraint filters by ownership; each endset constraint filters by content overlap. Nelson calls this the "AND of the ORs": OR within each endset (any span matching suffices), AND across the three slots (all constrained slots must match).

Well-definedness: home(a) is defined for all a ∈ dom(L) (by L1a, ASN-0047, and the definition of origin). coverage(eᵢ) is defined for every endset (over the span algebra, ASN-0053). The intersection coverage(eᵢ) ∩ P is a set operation over T. No external state is consulted — the predicate depends only on the link's stored value and the query specification.

We verify the compound-query case. When a V-region spans content from multiple sources, the resolution produces a disjoint union P = P₁ ∪ ... ∪ Pₘ. The satisfaction predicate handles this naturally:

**F1a — CompoundQueryDecomposition.** For sets P₁, ..., Pₘ and endset e:

  sat(e, P₁ ∪ ... ∪ Pₘ)  ⟺  sat(e, P₁) ∨ ... ∨ sat(e, Pₘ)

*Proof.* coverage(e) ∩ (P₁ ∪ ... ∪ Pₘ) ≠ ∅ iff (E j : 1 ≤ j ≤ m : coverage(e) ∩ Pⱼ ≠ ∅). ∎

A link touching *any* constituent of a compound region is found. The reader need not decompose multi-source selections into separate queries. At the level of the full result (when only S₁ is constrained):

  FindLinks((H, P₁ ∪ ... ∪ Pₘ, ⊤, ⊤)) = (∪ j : 1 ≤ j ≤ m : FindLinks((H, Pⱼ, ⊤, ⊤)))

## Overlap Sufficiency

The satisfaction predicate demands intersection, not containment. We state this precisely.

**F2 — OverlapSufficiency.** For endset e and search constraint P ≠ ⊤:

  sat(e, P)  requires only  coverage(e) ∩ P ≠ ∅

Neither containment direction is required. A link whose from-endset covers I-addresses {a, a+1, ..., a+100} is found by a query for {a+50, ..., a+150}. The shared region {a+50, ..., a+100} suffices. Even a single shared I-address is enough.

*Consequence.* A query against a document that transcludes only a fragment of some content discovers every link whose endset touches that fragment — even links whose endsets extend far beyond the fragment. The reader sees the link; following it reveals the full endset, including portions outside her current view. This follows from L12 (LinkImmutability, ASN-0043): the stored endset is the complete original, never truncated to the portion that matched the query.

*Boundary.* The predicate is strict at the boundary: adjacent but non-overlapping spans do not match. For level-uniform spans α and β in the adjacent case (SC case (ii), ASN-0053), we have ⟦α⟧ ∩ ⟦β⟧ = ∅, and sat fails. Adjacency in address space does not imply shared content identity.

For two well-formed level-uniform spans α = (s_α, ℓ_α) and β = (s_β, ℓ_β) at compatible depth, the overlap predicate reduces to:

  ⟦α⟧ ∩ ⟦β⟧ ≠ ∅  ⟺  s_α < reach(β) ∧ s_β < reach(α)

where reach(σ) = start(σ) ⊕ width(σ) (ASN-0053). This is strict half-open interval intersection. The implementation confirms this predicate at the byte level: the udanax-green spanfilade uses exactly `query_start < entry_end ∧ entry_start < query_end`, excluding the adjacent case.

## Completeness and Soundness

The fundamental guarantee of link discovery.

**Definition — FindLinksResult.** The result of FINDLINKS is:

  FindLinks(Q) = {a ∈ dom(Σ.L) : satisfies(a, Q)}

**F3 — Completeness.** FindLinks(Q) contains every link in dom(L) that satisfies Q:

  [a ∈ dom(Σ.L) ∧ satisfies(a, Q) ⟹ a ∈ FindLinks(Q)]

**F4 — Soundness.** FindLinks(Q) contains only links that satisfy Q:

  [a ∈ FindLinks(Q) ⟹ satisfies(a, Q)]

Together, F3 and F4 establish that FindLinks(Q) is *exactly* the set of satisfying links — a deterministic function of the system state Σ and the query specification Q. Nelson is explicit about this: the operation returns "all links" satisfying the criteria, not "some" or "a sample."

This is a semantic guarantee, not a delivery guarantee. The system may deliver results in pages via a cursor mechanism — the FINDNEXTNLINKSFROMTOTHREE variant returns "no more than N items past that link on that list." But pagination is a delivery mechanism over a complete result set. The underlying set is logically determined at query time.

**Definition — FindLinksCount.** |FindLinks(Q)| denotes the cardinality of the result set. The existence of a dedicated count operation (FINDNUMOFLINKSFROMTOTHREE) presupposes that this cardinality is computable. One cannot count what one has not determined.

## Result Ordering

The result set admits a stable, permanent ordering.

**F5 — ResultOrdering.** Every link has a unique tumbler address (GlobalUniqueness, ASN-0043). Tumblers are totally ordered by T1 (LexicographicOrder, ASN-0034). Therefore FindLinks(Q) inherits a total order. Formally:

  (A a, b ∈ FindLinks(Q) : a ≠ b : a < b ∨ b < a)

This order is permanent: link addresses are allocated by T9 (ForwardAllocation, ASN-0034) and never change (T8, AllocationPermanence). Within a single document, the order reflects link creation sequence. Across documents, the tumbler-line hierarchy (node, user, document, link instance) determines order.

**F6 — PaginationDeterminism.** For fixed state Σ and query Q, let FindLinks(Q) = {a₁, a₂, ..., aₙ} with a₁ < a₂ < ... < aₙ by T1. For any cursor c ∈ T and bound N ≥ 1:

  page(Q, c, N) = ⟨⟩                       when {k : aₖ > c} = ∅
  page(Q, c, N) = ⟨aᵢ, aᵢ₊₁, ..., aⱼ⟩    when i = min{k : aₖ > c} and j = min(i + N − 1, n)

The first case covers both FindLinks(Q) = ∅ (n = 0, the set is vacuously empty) and cursor exhaustion (c ≥ aₙ, all results have been consumed). Pagination produces a deterministic, repeatable subsequence. The cursor identifies a position in a fixed ordering; advancing the cursor does not re-evaluate the query.

## Scope of Discovery

**F7 — ScopeUniversality.** When the home constraint is ⊤, the search spans the entire link store:

  FindLinks((⊤, S₁, S₂, S₃)) = {a ∈ dom(Σ.L) : sat(F, S₁) ∧ sat(G, S₂) ∧ sat(Θ, S₃)}

where Σ.L(a) = (F, G, Θ). The search is not bounded to the queried document. It covers every link in every document in the system.

Why must the default scope be universal? Because links reside in their *home document*, determined by who created the link, not by what it references (L2, ASN-0043). A link from Alice's document pointing to Bob's published text lives in Alice's document. Bob can only discover this link if the search crosses document boundaries. A system that searched only within the queried document would miss every incoming link from every other author — defeating the purpose of bidirectional linking.

The home constraint allows narrowing:

  (A H ⊆ E_doc :: FindLinks((H, S₁, S₂, S₃)) ⊆ FindLinks((⊤, S₁, S₂, S₃)))

The home constraint is a filter, never an extension. Nelson provides this for managing the "avalanche" of cross-document results — "what links come in from Spain? From last week? From persons of importance to me?" Filtering presupposes a global search that returns too much.

## Transclusion Transparency

We derive the property that makes link discovery meaningful across shared content.

**F8 — TransclusionTransparency.** Let I-address a satisfy a ∈ ran(M(d₁)) ∩ ran(M(d₂)) — the same content appears in documents d₁ and d₂. Let link ℓ satisfy coverage(Σ.L(ℓ).eᵢ) ∋ a for some endset slot i. Then for any query Q constraining slot i with a set P ∋ a (and all other slots unconstrained):

  ℓ ∈ FindLinks(Q)

regardless of whether the query's P was derived from d₁ or d₂.

*Proof.* The satisfaction predicate tests coverage(Σ.L(ℓ).eᵢ) ∩ P ≠ ∅. Since a ∈ coverage(Σ.L(ℓ).eᵢ) and a ∈ P, the intersection contains at least {a}. The predicate holds independently of which document contributed a to P. The link is equally discoverable from either viewing context. ∎

This property does *not* hold for content that is semantically identical but structurally distinct. Two authors who independently type "to be or not to be" create content at different I-addresses (S4, OriginBasedIdentity, ASN-0036). Links to one are invisible from the other. Identity is structural — determined by origin — not semantic. This distinction is by design: it is what makes content identity permanent, unseverable, and independent of value.

The architectural consequence is deep. A link created against a paragraph in its home document is automatically discoverable from every document that transcludes that paragraph. The link does not need to know about the transclusion; the transclusion does not need to know about the link. Both follow from the fact that they reference the same I-addresses.

## Symmetric Searchability

**F9 — SymmetricSearchability.** The three endset slots are structurally interchangeable in the satisfaction predicate. For each slot i ∈ {1, 2, 3}, the single-slot query:

  Qᵢ(P) = (⊤, S'₁, S'₂, S'₃)  where  S'ᵢ = P, S'ⱼ = ⊤ for j ≠ i

finds all links whose slot i has coverage intersecting P:

  FindLinks(Qᵢ(P)) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).eᵢ) ∩ P ≠ ∅}

The search mechanism makes no structural distinction between from-search, to-search, and type-search. Each slot is queried by the same predicate (sat), using the same intersection test, with the same completeness guarantee.

*Consequence.* "Find links FROM this content" and "find links TO this content" are the same operation with different argument positions. The reader's question "what links point here?" (incoming links, or *in-links*) is answered with the same completeness and efficiency as "what links originate here?" (outgoing links, or *out-links*). The distinction between in-links and out-links is one of ownership (home(a)), not of discoverability.

This extends to combined queries: "find all citation-type links from this paragraph to that source" constrains all three slots simultaneously. The conjunctive model (F1) handles arbitrary combinations uniformly.

## Arrangement Independence

We observe that the FINDLINKS result depends on the link store and the query specification, not on the arrangement of any document.

**F10 — ArrangementIndependence.** For fixed Σ.L and Q:

  FindLinks(Q) depends only on (Σ.L, Q)

*Proof.* The satisfaction predicate (F1) references only Σ.L(a), home(a), and Q. The function home(a) = origin(a) depends on the link address a alone (L2, ASN-0043) — not on any arrangement. The endset coverages coverage(Σ.L(a).eᵢ) depend on Σ.L alone (L12, LinkImmutability, ASN-0043). The search constraints Sᵢ are provided as input. No component of the predicate references M(d) for any d. ∎

The arrangement enters at two points *outside* the satisfaction predicate: the resolution step that *produces* the query (translating V-regions to I-address sets), and the projection step that *interprets* the results (translating endsets back to V-positions for display). But the search itself — the determination of which links satisfy the query — is arrangement-independent.

*Consequence.* If a document's Vstream is edited (content inserted, deleted, rearranged), the set of links matching a given I-address query is unchanged. Only the resolution step — mapping the reader's new V-selection to I-addresses — may produce a different query. The search is a stable function of its inputs.

## Endset Projection

Link discovery yields link addresses. The reader wants to see where the link *points* — which V-positions in her current document correspond to the link's endsets. This requires an operation inverse to resolution: given a link's endset (a set of I-address spans), find the V-positions in a given document's arrangement that map to those I-addresses.

**Definition — EndsetProjection.** For link at address a ∈ dom(Σ.L), endset slot i ∈ {1, 2, 3}, and document d ∈ E_doc:

  project(a, i, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}

This is the preimage of the endset's coverage under M(d) — the set of V-positions in d whose I-addresses fall within the endset.

**F11 — ProjectionSubset.** The projection recovers at most the endset's coverage:

  {M(d)(v) : v ∈ project(a, i, d)} ⊆ coverage(Σ.L(a).eᵢ)

Equality holds only when every I-address in the coverage has at least one V-position in d's arrangement. The gap reflects content not currently arranged in d — content that has been removed from d's Vstream, or content that was never in d.

**F12 — ProjectionMultiplicity.** When a single I-address maps to multiple V-positions in d (from self-transclusion — the same content appearing at multiple positions), all are returned:

  [M(d)(v₁) = M(d)(v₂) = a ∧ v₁ ≠ v₂ ∧ a ∈ coverage(Σ.L(ℓ).eᵢ) ⟹ v₁ ∈ project(ℓ, i, d) ∧ v₂ ∈ project(ℓ, i, d)]

The projection reports every V-occurrence of the referenced content. This is the multimap nature of the I→V inversion: multiple V-positions may share an I-address, and the projection must enumerate them all.

**F13 — ProjectionMayBeEmpty.** The projection may return the empty set:

  project(a, i, d) = ∅  when  coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) = ∅

This occurs when none of the endset's referenced content is currently arranged in d. The link persists (L12, ASN-0043) and remains discoverable via FINDLINKS, but its endset has no V-manifestation in d. This is a structural possibility, not an error: the two-stream separation (S9, ASN-0036) permits arrangements to contract (P3, ASN-0047) without affecting the link store.

**F14 — ProjectionOpacity.** From the projection alone, a partial result — where some endset I-addresses are present in d and others are absent — is indistinguishable from a projection of a genuinely smaller endset. The system provides no completeness signal. Determining whether the projection represents the full endset requires independent knowledge of coverage(Σ.L(a).eᵢ), which is accessible by reading the link's stored value directly.

This opacity is a consequence of the preimage definition: project(a, i, d) is defined entirely by what M(d) maps, not by what the endset claims. No additional metadata is produced.

## Access Filtering

Links reside in documents. Documents may be private. A link in a private document is invisible to users who cannot access that document, even if the content the link references is publicly accessible. This is not a special rule for links — it is an emergent property of document privacy applied to links-as-document-contents.

The chain of reasoning: links are contents of their home document; private document contents are accessible only to the owner and designees; therefore links in private documents are accessible only to the owner and designees. Nelson reinforces this through the privacy principle: the network must not monitor what is written in private documents. Revealing the *existence* of links in private documents would leak information about private writing activity.

**Definition — Accessible.** For user u, let accessible(u) ⊆ E_doc denote the set of documents u is authorized to read.

**F15 — AccessFilter.** The *visible* result for user u is:

  FindLinks_u(Q) = {a ∈ FindLinks(Q) : home(a) ∈ accessible(u)}

**F16 — AccessMonotonicity.**

  [accessible(u₁) ⊆ accessible(u₂) ⟹ FindLinks_{u₁}(Q) ⊆ FindLinks_{u₂}(Q)]

Broader access yields a superset of visible links.

*Consequence.* Different users querying the same content may see different link sets. The system guarantees completeness *within the user's access domain*: every link satisfying Q whose home document u can read is returned. The semantic result (F3) is the ceiling; the access filter determines what each user actually sees.

The interaction with the home-set constraint is conjunctive: a link at address a appears in FindLinks_u((H, S₁, S₂, S₃)) only when (H = ⊤ ∨ home(a) ∈ H) ∧ home(a) ∈ accessible(u) ∧ sat(F, S₁) ∧ sat(G, S₂) ∧ sat(Θ, S₃). The home-set constrains *which* links the query seeks; access control constrains which links the user may see.

## FINDLINKS as a Derived Operation

We verify that link discovery introduces no state changes and that discovered links are permanently discoverable.

**F17 — StateInvariance.** FINDLINKS does not modify the system state:

  Σ' = Σ  after executing FindLinks(Q)

No transition kind (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ from ASN-0047) is triggered. FINDLINKS is a pure query — a read of existing state.

**F18 — MonotonicDiscoverability.** Once a link satisfies a query, it satisfies that query in every subsequent state:

  [a ∈ FindLinks_Σ(Q) ⟹ a ∈ FindLinks_{Σ'}(Q)]  for all Σ' reachable from Σ

*Proof.* L12 (LinkImmutability, ASN-0043) preserves Σ'.L(a) = Σ.L(a). T8 (AllocationPermanence, ASN-0034) preserves a ∈ dom(Σ'.L). The function home(a) = origin(a) is determined by a alone and a is permanent. The satisfaction predicate evaluated at Σ' uses the same L(a), the same home(a), and the same Q. Therefore satisfies(a, Q) holds at Σ' whenever it held at Σ. ∎

The set of satisfying links can only grow over time — new links may be created that satisfy Q, but existing matches are never lost. This is the link-discovery analogue of content permanence (S0, ASN-0036).

## Scale

The abstract specification includes one performance-class design constraint. Nelson states: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." We record this as a requirement on any conforming implementation.

**F19 — ScaleIndependence (design constraint).** The cost of locating candidate links for FindLinks(Q) must be sublinear in |dom(Σ.L)| — the total number of links in the system. Nelson states that the quantity of non-satisfying links must not "in principle impede" search on satisfying ones. The phrase admits logarithmic dependence on total link count — the overhead inherent in tree-based indexing — while excluding linear scans through the non-matching population.

This constraint is architecturally necessary. Without it, the universal scope guarantee (F7) — searching the entire link store — would become impractical as the link population grows. Any conforming implementation must maintain index structures enabling sublinear candidate location — at minimum O(log |dom(Σ.L)|) to reach the matching region.

The implementation achieves this through a spanfilade — a 2D enfilade (branching factor 4–6) indexing link endsets by I-address range. Tree traversal to the matching region is O(log n), where n is the number of spanfilade entries. Three independent index traversals (one per endset type) are intersected to produce the final result. The dominant cost beyond tree traversal is result-set processing, which scales with the number of candidate matches rather than the total link population. The abstract property F19 demands that *any* implementation achieve comparable sublinear index traversal — the result-set processing cost is necessarily at least linear in |FindLinks(Q)|.

## Worked Example

We construct a concrete scenario and verify the key properties against it. Let documents d₁ and d₂ inhabit the system, with content addresses a₁ < a₂ < a₃ satisfying aᵢ ∈ dom(C) and origin(aᵢ) = d₁ for each i. Document d₁ arranges all three:

  M(d₁) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₃}

where v₁ < v₂ < v₃ are text-subspace V-positions. Document d₂ transcludes only the middle piece:

  M(d₂) = {w₁ ↦ a₂}

where w₁ is a text-subspace V-position in d₂. The I-address a₂ is the *same* address in both arrangements — a₂ ∈ ran(M(d₁)) ∩ ran(M(d₂)).

Now let link ℓ ∈ dom(L) have value L(ℓ) = (F, G, Θ) where the from-endset F contains a single span covering all three addresses: coverage(F) ⊇ {a₁, a₂, a₃}. (Concretely, F = {(a₁, δ(3, m))} when a₁, a₂, a₃ are contiguous at common depth m — three addresses require width 3, since ⟦(a₁, δ(2, m))⟧ = [a₁, a₃) would exclude a₃ by half-open interval semantics.) The to-endset and type-endset are arbitrary.

**Verifying F1 (satisfaction).** Consider the query Q = (⊤, {a₂}, ⊤, ⊤) — "find links whose from-endset touches a₂." We evaluate:

  satisfies(ℓ, Q) ≡ (⊤ = ⊤) ∧ sat(F, {a₂}) ∧ sat(G, ⊤) ∧ sat(Θ, ⊤)

The home constraint is trivially satisfied. sat(G, ⊤) = true and sat(Θ, ⊤) = true by definition. For the from-endset: sat(F, {a₂}) ≡ coverage(F) ∩ {a₂} ≠ ∅. Since a₂ ∈ coverage(F), the intersection is {a₂} ≠ ∅. Therefore satisfies(ℓ, Q) holds. The link is found despite the query naming only one of the three covered addresses.

**Verifying F8 (transclusion transparency).** The query set {a₂} can be derived from either document. From d₁: the reader selects the V-span covering v₂, and resolution yields addresses(d₁, σ₁) ∋ a₂. From d₂: the reader selects the V-span covering w₁, and resolution yields addresses(d₂, σ₂) ∋ a₂. In both cases the resulting query set contains a₂, and the satisfaction predicate produces the same outcome — ℓ ∈ FindLinks(Q). The link is equally discoverable from d₁ and d₂. The viewing document is irrelevant to discovery.

**Verifying F11 and F13 (projection).** We project the from-endset of ℓ onto each document:

  project(ℓ, 1, d₁) = {v ∈ dom(M(d₁)) : M(d₁)(v) ∈ coverage(F)}

Since M(d₁)(v₁) = a₁, M(d₁)(v₂) = a₂, M(d₁)(v₃) = a₃, and all three belong to coverage(F), we get project(ℓ, 1, d₁) = {v₁, v₂, v₃}. The full endset is visible in d₁.

  project(ℓ, 1, d₂) = {v ∈ dom(M(d₂)) : M(d₂)(v) ∈ coverage(F)}

Since M(d₂)(w₁) = a₂ ∈ coverage(F), and no other V-position exists in M(d₂), we get project(ℓ, 1, d₂) = {w₁}. Only the transcluded fragment is visible. The I-addresses a₁ and a₃ belong to coverage(F) but have no preimage in M(d₂), confirming F11 (projection is a subset) and illustrating the partial-coverage case. The projection is not empty (F13's condition does not hold here, since coverage(F) ∩ ran(M(d₂)) = {a₂} ≠ ∅), but it is strictly smaller than the full endset — confirming F14 (no completeness signal from the projection alone).

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.L | L : T ⇀ Link — link store (from ASN-0047) | cited |
| QuerySpecification | Q = (H, S₁, S₂, S₃) — home constraint and three endset constraints | introduced |
| SearchConstraint | ⊤ or non-empty P ⊂ T (addresses need not belong to dom(C)) | introduced |
| HomeConstraint | ⊤ or non-empty H ⊆ E_doc | introduced |
| EndsetSatisfaction | sat(e, P) ≡ coverage(e) ∩ P ≠ ∅ | introduced |
| FindLinksResult | FindLinks(Q) = {a ∈ dom(L) : satisfies(a, Q)} | introduced |
| EndsetProjection | project(a, i, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(L(a).eᵢ)} | introduced |
| FindLinksCount | \|FindLinks(Q)\| — cardinality of result set | introduced |
| F0 | Resolution is transparent to the viewing document — identical content produces identical I-addresses | introduced |
| F1 | satisfies(a, Q) ≡ home-constraint ∧ sat(F, S₁) ∧ sat(G, S₂) ∧ sat(Θ, S₃) | introduced |
| F1a | sat(e, P₁ ∪ ... ∪ Pₘ) ⟺ sat(e, P₁) ∨ ... ∨ sat(e, Pₘ) | introduced |
| F2 | Partial overlap suffices: coverage(e) ∩ P ≠ ∅ requires only one shared I-address | introduced |
| F3 | Completeness: every satisfying link is in FindLinks(Q) | introduced |
| F4 | Soundness: every link in FindLinks(Q) satisfies Q | introduced |
| F5 | FindLinks(Q) is totally ordered by T1 on link addresses | introduced |
| F6 | Pagination is deterministic for fixed Σ and Q | introduced |
| F7 | When H = ⊤, search spans all of dom(L) | introduced |
| F8 | Transclusion transparency: same I-address ⟹ same discoverability | introduced |
| F9 | Symmetric searchability: all three endset slots use the same mechanism | introduced |
| F10 | FindLinks(Q) depends only on (L, Q), not on any M(d) | introduced |
| F11 | Endset projection returns a subset of the endset's coverage | introduced |
| F12 | Projection returns all V-positions for self-transcluded content | introduced |
| F13 | Projection may be empty when endset content is not in the target arrangement | introduced |
| F14 | Projection provides no incompleteness signal | introduced |
| F15 | Visible result is FindLinks(Q) filtered by accessible(u) | introduced |
| F16 | Access monotonicity: broader access ⟹ superset of visible links | introduced |
| F17 | FINDLINKS is a pure query: Σ' = Σ | introduced |
| F18 | Monotonic discoverability: once satisfied, always satisfied | introduced |
| F19 | Scale independence: candidate location must be sublinear in total link count (design constraint) | introduced |

## Open Questions

What invariants must an index of link endsets maintain to guarantee that no satisfying link is omitted from FindLinks(Q)?

Must FINDLINKS provide isolation guarantees when link creation and link search execute concurrently within the same system state?

Should the system reveal the existence of access-restricted links to the querying user, or must it conceal even the fact that additional matching links exist behind the access boundary?

Must endset projection signal whether the returned V-positions represent the complete endset or a proper subset, and if so, what form should that signal take?

What guarantees must pagination provide when the link store grows — links are created — between successive page requests against the same query cursor?

Must the cardinality |FindLinks(Q)| be computable without materializing the full result set, and if so, what index properties does this require?
