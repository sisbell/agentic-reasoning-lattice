# ASN-0063: CREATELINK Operation

*2026-03-21*

We know what a link is — a permanent, immutable triple of endsets at an element-level address in the link subspace (ASN-0043, L0–L14). We know what content is — values at permanent I-addresses in an append-only store (ASN-0036, S0). We know how arrangements bridge permanent identity and mutable structure (ASN-0058). The question before us is operational: what must happen, precisely, when a new link enters the docuverse? What is allocated, what is indexed, and what must remain untouched?

We work backward from the desired end-state. After CREATELINK succeeds, three things must hold: a new link exists in the link store with endsets correctly capturing the referenced content; the link is discoverable from any content it references; and no pre-existing content or link has been modified. These requirements — existence, discoverability, non-interference — determine everything that follows.

We begin with the gap that every link creation must bridge.


## The Resolution Bridge

A link's endsets are sets of I-spans — they address content by permanent identity (ASN-0043, L3). The user, however, selects content by position in a document's current arrangement — a V-space reference. CREATELINK must translate V-references into I-references at creation time.

This translation is not incidental. It is the mechanism by which links survive editing. Nelson: links are "straps between bytes" that survive "deletions, insertions and rearrangements, if anything is left at each end." An endset that stored V-positions would break whenever the target document was rearranged. An endset that stores I-addresses persists through all arrangement changes — the same bytes carry the same I-addresses forever (S0, ASN-0036), regardless of where they sit in any document's Vstream.

The question that opens our investigation is: given a V-span in a document, what I-spans correspond to it?

**Definition — VSpanImage.** For document d with arrangement M(d) and V-span σ_v = (v_s, w_v):

  `image(d, σ_v) = {M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d))}`

For a V-span-set Ψ = {σ₁, ..., σₖ}: `image(d, Ψ) = (∪ i : 1 ≤ i ≤ k : image(d, σᵢ))`.

The image is well-defined: M(d) is a function (S2, ASN-0036), ⟦σ_v⟧ is determined by the span's start and width (SpanDenotation, ASN-0053), and the intersection with dom(M(d)) is finite (S8-fin, ASN-0036). V-positions outside dom(M(d)) — gaps from prior content removal — contribute nothing to the image.

We need this set expressible as an endset: a finite set of well-formed I-spans. The block decomposition (ASN-0058) provides the structure.


## Endset Resolution

**Lemma CL0 — BlockProjection.** Let β = (v_β, a_β, n) be a mapping block (ASN-0058) and σ_v a V-span in the same subspace. If `V(β) ∩ ⟦σ_v⟧ ≠ ∅`, then the image of their overlap through β is a single well-formed I-span.

*Proof.* The V-extent V(β) is contiguous by M1 (ASN-0058), and ⟦σ_v⟧ is convex by S0 (ASN-0053). Their non-empty intersection is convex, hence of the form `{v_β + k : c ≤ k < c'}` for some `0 ≤ c < c' ≤ n`. By B3 (Consistency, ASN-0058), `M(d)(v_β + k) = a_β + k`, so the image is `{a_β + k : c ≤ k < c'}`. Define the I-span `ρ = (shift(a_β, c), δ(c' − c, #a_β))`. Its reach is `shift(a_β, c) ⊕ δ(c' − c, #a_β) = shift(a_β, c')` by TS3 (ShiftComposition, ASN-0034). The displacement `δ(c' − c, #a_β)` is positive since `c' − c ≥ 1`, and its action point equals `#a_β = #shift(a_β, c)` (ordinal shift preserves depth), satisfying T12 (SpanWellDefined, ASN-0034). ∎

A single V-span crossing multiple mapping blocks produces multiple I-spans — one per overlapping block. This is not a degenerate case; it is the *normal* case when the selected content was assembled from multiple sources through transclusion. Each transcluded portion retains its original I-address — that is the definition of transclusion — so a contiguous V-selection may cover a discontiguous set of I-addresses. A selection of "AABB" where "AA" was transcluded from document X and "BB" from document Y produces two I-spans: one addressing the "AA" bytes in X's I-space, another addressing "BB" in Y's I-space.

**Lemma CL1 — ResolutionExistence.** For any document d with M(d) satisfying the arrangement invariants (S2, S8-fin, ASN-0036) and any V-span-set Ψ, there exists an endset `E ∈ Endset` with `coverage(E) = image(d, Ψ)`.

*Proof.* Let B be the canonical block decomposition of M(d) (exists by M11, ASN-0058). For each σ ∈ Ψ and each β ∈ B with `V(β) ∩ ⟦σ⟧ ≠ ∅`, CL0 yields one I-span. By B1 and B2 (Coverage, Disjointness, ASN-0058), each V-position in dom(M(d)) falls in exactly one block. The image of each V-position is therefore accounted for exactly once across all block projections. The finite collection of resulting I-spans is a well-formed endset (each span satisfies T12, the set is finite) with coverage equal to `image(d, Ψ)`. ∎

We observe that I-spans arising from distinct blocks in the canonical decomposition are non-adjacent. If consecutive blocks β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) produced I-adjacent output (a₂ = a₁ + n₁), they would also be V-adjacent (v₂ = v₁ + n₁, since they partition a contiguous V-range by D-CTG, ASN-0036). But V-adjacent and I-adjacent blocks satisfy the merge condition M7 (ASN-0058), contradicting the decomposition being maximally merged (M12). So the endset from CL1, sorted by start position, is already normalized (N1, N2, ASN-0053) within each V-span's contribution.

**Definition — Resolve.** `resolve(d, Ψ)` is the normalized endset (per S8, ASN-0053) with:

**CL2 — ResolutionFaithfulness.** `coverage(resolve(d, Ψ)) = image(d, Ψ)`.

Immediate from CL1 and the normalization equivalence (S8, ASN-0053).

Endset specifications may reference content across multiple documents — the from-endset might address content in document X, the to-endset content in document Y, while the link itself lives in document Z. For a cross-document specification S = {(d₁, Ψ₁), ..., (dₘ, Ψₘ)}, define `resolve(S) = normalize(resolve(d₁, Ψ₁) ∪ ... ∪ resolve(dₘ, Ψₘ))`. Each (document, V-spans) pair resolves independently; the union captures the cross-document endsets permitted by L4(a) (ASN-0043).

One final observation on resolution. When a V-span-set covers V-positions outside dom(M(d)) — content that was removed from the arrangement but persists in the Istream (by S0) — those positions contribute nothing to the image. The resolved endset captures only content *currently arranged* in the source documents. Content that exists in the Istream but has no current arrangement mapping is unreachable through V-space resolution. It can, however, be referenced directly by I-address: the system supports raw I-span endsets that bypass resolution entirely. In that case the endsets are taken as-is — no arrangement is consulted, no validation against dom(C) is performed. The link is created with whatever I-addresses are provided.


## Extending the Transition Framework

ASN-0047 defines the system state as Σ = (C, E, M, R) with elementary transitions K.α (content), K.δ (entity), K.μ⁺/K.μ⁻/K.μ~ (arrangement), and K.ρ (provenance). ASN-0043 introduces the link store Σ.L but does not define transitions for it. We now integrate links into the transition framework.

The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store (ASN-0043). All existing elementary transitions from ASN-0047 hold L in their frame: L' = L. We introduce a new elementary transition for link creation.

**K.λ — LinkAllocation.** Creates a new entry in the link store.

*Precondition:*
- d ∈ E_doc  (home document exists)
- ℓ ∉ dom(L) ∪ dom(C)  (fresh address — L14, ASN-0043)
- zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L  (element-level, link subspace — L0, L1)
- origin(ℓ) = d  (scoped to home document — L1a)
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`  (forward allocation — T9)
- (F, G, Θ) ∈ Link  (well-formed link value — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

The address ℓ is produced by the same forward-allocation discipline as content addresses (T9, ASN-0034): within each document's link subspace, addresses are monotonically increasing. By T7 (SubspaceDisjointness, ASN-0034), the link subspace s_L is disjoint from the content subspace s_C, so ℓ cannot collide with any content address. By T10 (PartitionIndependence, ASN-0034), link addresses in different documents cannot collide either.


## The CREATELINK Composite

CREATELINK combines resolution and allocation. The user provides a home document d and endset specifications for three roles: from, to, and type. Each specification is either a set of (document, V-spans) pairs or a set of direct I-spans. The system resolves V-references, allocates a fresh link, and stores the result.

**CREATELINK(d, S_F, S_G, S_Θ):**

Let F = resolve(S_F), G = resolve(S_G), Θ = resolve(S_Θ).

*Precondition:*
- d ∈ E_doc
- A fresh link address ℓ is available satisfying K.λ's preconditions

*Composite steps:*
1. K.λ: allocate ℓ in dom(L) with value (F, G, Θ)
2. Extend M(d) at a fresh V-position v_ℓ in the link subspace, mapping v_ℓ to ℓ

*Postcondition CL3:*

  (a) `ℓ ∈ dom(L') ∧ ℓ ∉ dom(L)` — a new link exists

  (b) `L'(ℓ) = (F, G, Θ)` — with the resolved endsets

  (c) `home(ℓ) = origin(ℓ) = d` — determined by the address alone (L2, ASN-0043)

  (d) `(A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))` — existing links unchanged (L12)

  (e) `C' = C` — content unchanged

Step 2 places ℓ into d's arrangement, making the link an *out-link* of d. Nelson draws a sharp distinction: "a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not" (LM 2/31). An out-link lives in its home document's arrangement; an in-link is merely discoverable from the referenced document. CREATELINK produces one out-link (in d) and zero or more in-link relationships (one for each document whose content the endsets reference).

Step 2 parallels K.μ⁺ (ArrangementExtension, ASN-0047) but maps a V-position to a link address in dom(L) rather than a content address in dom(C). The referential integrity requirement for the link subspace is `M'(d)(v_ℓ) ∈ dom(L')` rather than the text-subspace requirement `M(d)(v) ∈ dom(C)` (S3, ASN-0036). The link subspace V-positions form their own contiguous range within d's arrangement (by the same contiguity reasoning as D-CTG, ASN-0036, applied to a distinct subspace), and new links are appended at the next available V-position.

Note that the home document determines link ownership — not what the link points to. "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to" (Nelson, LM 4/12). A link in document Z whose endsets reference content in documents X and Y is owned by Z's owner. Neither X's nor Y's owner can modify or withdraw it.


## What Is Preserved

The most important property of CREATELINK is what it does *not* do.

**CL4 — ContentNonInterference.** CREATELINK preserves the content store: `C' = C`.

*Proof.* K.λ has C' = C in its frame. Step 2 modifies only M(d), which is independent of C by S9 (TwoStreamSeparation, ASN-0036). No step in the composite writes to C. ∎

We arrive at this guarantee from five independent architectural principles, any one of which would suffice:

*Separate storage.* The link is stored at the creator's address in the creator's document — `origin(ℓ) = d` — not at the referenced content's address. The link's home document "indicates who owns it, and not what it points to" (Nelson, LM 4/12).

*Istream immutability.* Content at I-addresses is permanent (S0, ASN-0036). No operation can modify existing content values. CREATELINK is not special; it inherits this guarantee.

*Owner-only modification.* Only the document owner can modify their content (Nelson, LM 2/29). Creating a link to someone else's published content is a non-owner action on the target, which cannot alter the target.

*K.λ isolation.* K.λ writes to L; its frame explicitly leaves C, E, M, R unchanged. There is no mechanism in K.λ for altering C.

*Structural separation.* Links are "meta-virtual structures connecting parts of documents" (Nelson, LM 4/41) — a layer above content, not a modification of it.

The convergence of these five principles means content non-interference is not a fragile property that might be weakened by future extensions. It is overdetermined — removing any one guarantee still leaves four others in place.

**CL5 — LinkPreservation.** CREATELINK preserves all existing links:

  `dom(L) ⊆ dom(L') ∧ (A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))`

Immediate from K.λ's effect: L' = L ∪ {ℓ ↦ (F, G, Θ)} with ℓ ∉ dom(L).

**CL6 — ArrangementConfinement.** CREATELINK modifies only M(d) for the home document d:

  `(A d' : d' ≠ d : M'(d') = M(d'))`

*Proof.* K.λ has M in frame. Step 2 modifies only M(d). ∎

Moreover, step 2 modifies only the *link subspace* of M(d). The text-subspace mappings — `{(v, M(d)(v)) : v ∈ dom(M(d)) ∧ subspace(v) = s_C^V}` — are invariant.

The conjunction of CL4, CL5, and CL6 gives the full frame of CREATELINK: content unchanged, existing links unchanged, other documents' arrangements unchanged, and the home document's text-subspace arrangement unchanged. The only new state is one entry in L and one link-subspace mapping in M(d).


## What Is Indexed: The Discovery Function

After CREATELINK, the system must answer: "What links reference this content?" Nelson requires that the reader "be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay" (LM 2/46). Moreover, "the quantity of links not satisfying a request does not in principle impede search on others" (LM 4/60) — discovery must scale sub-linearly in the total number of links.

We formalize this as a derived function on the system state.

**Definition — DiscoveryFunction.** For I-address a and role r ∈ {from, to, type}:

  `disc(a, r) = {ℓ ∈ dom(L) : a ∈ coverage(L(ℓ).r)}`

For a set of I-addresses S:

  `disc(S, r) = {ℓ ∈ dom(L) : S ∩ coverage(L(ℓ).r) ≠ ∅}`

The function disc is well-defined in every reachable state: L is a partial function, coverage is computable from the span-set definition (ASN-0053), and dom(L) is finite by the finitely many transitions from the initial state (ASN-0047).

**CL7 — DiscoveryMonotonicity.** For every state transition Σ → Σ':

  `(A a, r :: disc_Σ(a, r) ⊆ disc_Σ'(a, r))`

*Proof.* By L12a (LinkStoreMonotonicity, ASN-0043), dom(L) ⊆ dom(L'). By L12 (LinkImmutability), L'(ℓ) = L(ℓ) for all ℓ ∈ dom(L). Every ℓ in disc_Σ(a, r) satisfies a ∈ coverage(L(ℓ).r) = coverage(L'(ℓ).r), so ℓ ∈ disc_Σ'(a, r). ∎

Discovery only grows. Once a link is discoverable from an I-address, it remains discoverable forever. No operation can remove a link from disc — not even "deletion," which in Nelson's design removes the link from the current *arrangement* but does not remove it from L (the link "remains in Istream, recoverable through historical backtrack," LM 4/9).

**CL8 — DiscoveryCompleteness.** After CREATELINK produces link ℓ with value (F, G, Θ):

  `(A a : a ∈ coverage(F) : ℓ ∈ disc(a, from))`

  `(A a : a ∈ coverage(G) : ℓ ∈ disc(a, to))`

  `(A a : a ∈ coverage(Θ) : ℓ ∈ disc(a, type))`

*Proof.* After K.λ, ℓ ∈ dom(L') and L'(ℓ) = (F, G, Θ). For any a ∈ coverage(F), we have a ∈ coverage(L'(ℓ).from), so ℓ ∈ {ℓ' ∈ dom(L') : a ∈ coverage(L'(ℓ').from)} = disc_Σ'(a, from). Symmetrically for G and Θ. ∎

Since disc is derived from L, completeness is automatic: the link's existence in L with the correct value is sufficient. The operational challenge — maintaining data structures for efficient evaluation of disc — is an implementation concern. Nelson specifies that the back end maintains "inter-indexing mechanisms" for this purpose (LM 4/41); the implementation uses a two-dimensional enfilade keyed by I-address range and link identity, with one entry per I-span per endset role. What the abstract specification requires is only this: the system must support evaluation of disc(S, r) for arbitrary finite S, and CREATELINK must leave the system in a state where every covered address returns the new link. The implementation must ensure that the transition from pre-state to post-state is atomic — no observable intermediate state exists where ℓ ∈ dom(L) but disc has not yet been updated. Nelson: "all changes, once made, left the file remaining in canonical order, which was an internal mandate of the system" (LM 1/34).

**CL9 — DiscoveryIndependence.** disc(a, r) depends only on the I-address a and the role r, not on any document or arrangement:

  `(A d₁, d₂, v₁, v₂ : M(d₁)(v₁) = a ∧ M(d₂)(v₂) = a : disc(a, r) is identical)`

This is immediate from the definition — disc consults L, not M. Its architectural consequence, however, is profound.

Transclusion creates arrangement mappings to existing I-addresses — that is its nature. When document Z transcludes content from document X, Z's arrangement maps some of Z's V-positions to the same I-addresses as X's arrangement. By CL9, any link whose endsets cover those I-addresses is equally discoverable from Z as from X. The discovery mechanism does not need to be notified of the transclusion; the shared I-addresses carry the information.

This means that CREATELINK's effects propagate through the docuverse automatically. A link created today between content in documents A and B will be discoverable tomorrow from document C, if C transcludes any content whose I-addresses overlap the link's endsets — even though C did not exist when the link was created. No update to the link, the index, or any data structure is required. The link was always discoverable from those I-addresses; C merely provides a new path to reach them.


## Latent Links

**CL10 — LatentLinks.** A link whose endsets cover I-addresses not currently in any document's arrangement — `a ∈ dom(C)` but `(A d :: a ∉ ran(M(d)))` — is *latent*. It exists in L. disc(a, r) includes it. But no document-scoped query encounters it, because no arrangement provides a path to a.

If a later operation adds a mapping `v ↦ a` to some document d' (through transclusion or content restoration), the link becomes discoverable from d'. Nothing about the link changed — disc(a, r) was always the same. What changed is that d' now has a V-position whose I-address falls in the link's endset coverage.

This follows directly from disc's independence from arrangements. disc is constant with respect to M. The link is always present in the discovery function; the question is whether any arrangement currently reaches the covered I-addresses. Latent links are not broken links — they are links whose endpoints have no current arrangement, waiting to be reactivated by any operation that maps new V-positions to the covered I-addresses.

The system also permits CREATELINK with endsets that reference I-addresses in dom(C) but outside all current arrangements (via direct I-span endsets that bypass V-space resolution). The resulting link is latent from birth — discoverable in principle but unreachable in practice until some arrangement maps to the covered I-addresses. This is permitted by the invariants: L3 and L4 (ASN-0043) place no requirement on endset I-addresses being currently arranged, and the discovery function operates purely on I-addresses without consulting arrangements.


## Invariant Preservation

**Theorem CL11 — InvariantPreservation.** CREATELINK preserves all foundation invariants.

*Content invariants (ASN-0036).* S0 (ContentImmutability): C' = C by CL4. S1 (StoreMonotonicity): dom(C) ⊆ dom(C') since C' = C. S2 (ArrangementFunctionality): M'(d') = M(d') for d' ≠ d by CL6; M'(d) extends M(d) with one V-position in the link subspace, preserving functionality for both subspaces. S3 (ReferentialIntegrity): holds for text-subspace mappings since those are unchanged; the link-subspace mapping v_ℓ ↦ ℓ satisfies ℓ ∈ dom(L'), the link-subspace analogue. S8-fin, S8a, S8-depth, D-CTG, D-SEQ: these are scoped to the text subspace and are unaffected by link-subspace extension. ✓

*Link invariants (ASN-0043).* L0 (SubspacePartition): ℓ has fields(ℓ).E₁ = s_L by K.λ precondition. dom(L') ∩ dom(C') = (dom(L) ∪ {ℓ}) ∩ dom(C). Since ℓ ∉ dom(C) and dom(L) ∩ dom(C) = ∅ (L0 pre-state), the intersection is empty. L1 (LinkElementLevel): zeros(ℓ) = 3 by K.λ precondition. L1a (LinkScopedAllocation): origin(ℓ) = d by K.λ precondition. L12 (LinkImmutability): existing entries are unchanged; the transition adds ℓ without modifying any existing L entry. L12a (LinkStoreMonotonicity): dom(L) ⊂ dom(L'). L14 (DualPrimitive): dom(C') ∪ dom(L') = dom(C) ∪ dom(L) ∪ {ℓ}; disjointness holds since ℓ ∉ dom(C). ✓

*Transition invariants (ASN-0047).* P0 (ContentPermanence): C' = C. P1 (EntityPermanence): E' = E. P2 (ProvenancePermanence): R' = R. P5 (DestructionConfinement): only M and L change, both by extension — no information is lost. P6 (ExistentialCoherence): unchanged since dom(C) is unchanged. P7, P7a (Provenance): R is unchanged and dom(C) is unchanged. P8 (EntityHierarchy): E is unchanged. ✓


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| image(d, Ψ) | `{M(d)(v) : v ∈ ⟦Ψ⟧ ∩ dom(M(d))}` — V-span image through arrangement | introduced |
| CL0 | Each mapping block / V-span overlap produces a single well-formed I-span | introduced |
| CL1 | For any d and Ψ, there exists E ∈ Endset with coverage(E) = image(d, Ψ) | introduced |
| resolve(d, Ψ) | Normalized endset with coverage = image(d, Ψ) | introduced |
| CL2 | coverage(resolve(d, Ψ)) = image(d, Ψ) — resolution faithfulness | introduced |
| K.λ | Elementary transition: L' = L ∪ {ℓ ↦ (F, G, Θ)}, frame C' = C, E' = E, M' = M, R' = R | introduced |
| CL3 | CREATELINK postcondition: ℓ ∈ dom(L'), home(ℓ) = d, L'(ℓ) = (F, G, Θ), existing state preserved | introduced |
| CL4 | ContentNonInterference: C' = C under CREATELINK | introduced |
| CL5 | LinkPreservation: dom(L) ⊆ dom(L') and existing entries unchanged | introduced |
| CL6 | ArrangementConfinement: only M(d) for home document d is modified | introduced |
| disc(a, r) | `{ℓ ∈ dom(L) : a ∈ coverage(L(ℓ).r)}` — discovery function | introduced |
| CL7 | DiscoveryMonotonicity: disc only grows across all state transitions | introduced |
| CL8 | DiscoveryCompleteness: after CREATELINK, ℓ ∈ disc(a, r) for all covered a | introduced |
| CL9 | DiscoveryIndependence: disc depends only on I-address and role, not on any document | introduced |
| CL10 | LatentLinks: links with no currently-arranged endset coverage are discoverable when content is later transcluded | introduced |
| CL11 | InvariantPreservation: CREATELINK preserves all foundation invariants | introduced |


## Open Questions

What invariants must the link subspace of a document's arrangement satisfy — must it exhibit contiguity, depth uniformity, and minimum-position properties parallel to D-CTG, D-MIN, D-SEQ for the text subspace?

Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?

What must the system guarantee when concurrent CREATELINK operations target the same home document — must link address allocation be serialized, or can concurrent allocations produce distinct addresses without coordination?

What abstract properties must the discovery mechanism satisfy beyond completeness — must it support range queries over I-address intervals, or is point-level query sufficient?

Must the type endset reference content in a designated type namespace, or is any well-formed span valid as a type reference regardless of what the I-addresses contain?

When a link's from-endset and to-endset cover overlapping I-address ranges, what must the discovery function report — must it distinguish the endset role in which the address was found, or may it return the link once without role attribution?

What must the system guarantee about the ordering of links returned by discovery — creation order, address order, or is the result unordered?

What invariants must link withdrawal (removal from the current version of the home document) maintain with respect to the discovery function — must withdrawn links remain discoverable, or does withdrawal remove them from disc?

What must resolution guarantee when the arrangement changes between the moment the user selects content and the moment resolution executes — must it capture the selection-time arrangement, or is the resolution-time arrangement acceptable?
