# ASN-0063: CREATELINK Operation

*2026-03-21*

We know what a link is — a permanent, immutable triple of endsets at an element-level address in the link subspace (ASN-0043, L0–L14). We know what content is — values at permanent I-addresses in an append-only store (ASN-0036, S0). We know how arrangements bridge permanent identity and mutable structure (ASN-0058). The question before us is operational: what must happen, precisely, when a new link enters the docuverse? What is allocated, what is indexed, and what must remain untouched?

We work backward from the desired end-state. After CREATELINK succeeds, three things must hold: a new link exists in the link store with endsets correctly capturing the referenced content; the link is discoverable from any content it references; and no pre-existing content or link has been modified. These requirements — existence, discoverability, non-interference — determine everything that follows.

We begin with the gap that every link creation must bridge.


## The Resolution Bridge

A link's endsets are sets of I-spans — they address content by permanent identity (ASN-0043, L3). The user, however, selects content by position in a document's current arrangement — a V-space reference. CREATELINK must translate V-references into I-references at creation time.

This translation is not incidental. It is the mechanism by which links survive editing. Nelson: links are "straps between bytes" that survive "deletions, insertions and rearrangements, if anything is left at each end." An endset that stored V-positions would break whenever the target document was rearranged. An endset that stores I-addresses persists through all arrangement changes — the same bytes carry the same I-addresses forever (S0, ASN-0036), regardless of where they sit in any document's Vstream.

The question that opens our investigation is: given a V-span in a document, what I-spans correspond to it?

**Definition — VSpanImage.** For document d with arrangement M(d) and V-span σ_v = (v_s, w_v) satisfying T12 (SpanWellDefined, ASN-0034):

  `image(d, σ_v) = {M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d))}`

For a V-span-set Ψ = {σ₁, ..., σₖ} where each σᵢ satisfies T12: `image(d, Ψ) = (∪ i : 1 ≤ i ≤ k : image(d, σᵢ))`.

The image is well-defined: each σ_v satisfies T12 — `w_v > 0` and action point `k ≤ #v_s` — so `reach(σ_v) = v_s ⊕ w_v` exists (TA0, ASN-0034) and ⟦σ_v⟧ is determined by the span's start and width (SpanDenotation, ASN-0053). M(d) is a function (S2, ASN-0036), and the intersection with dom(M(d)) is finite (S8-fin, ASN-0036). V-positions outside dom(M(d)) — gaps from prior content removal — contribute nothing to the image.

We need this set expressible as an endset: a finite set of well-formed I-spans. The block decomposition (ASN-0058) provides the structure.


## Endset Resolution

**Lemma CL0 — BlockProjection.** Let β = (v_β, a_β, n) be a mapping block (ASN-0058) and σ_v a V-span in the same subspace. If `V(β) ∩ ⟦σ_v⟧ ≠ ∅`, then the image of their overlap through β is representable by a single well-formed I-span — that is, it is contained in the denotation of a span whose element-level members are exactly the image.

*Proof.* The V-extent `V(β) = {v_β + k : 0 ≤ k < n}` is a sequence of ordinal increments at fixed depth (S8-depth, ASN-0036), with consecutive last components (D-SEQ, ASN-0036). Convex subsets of such sequences correspond to contiguous index sub-ranges, since the only depth-`#v_β` tumbler between `v_β + k` and `v_β + (k + 1)` is `v_β + k` itself. The span denotation ⟦σ_v⟧ is convex by S0 (ASN-0053). Their non-empty intersection is therefore convex and of the form `{v_β + k : c ≤ k < c'}` for some `0 ≤ c < c' ≤ n`. By B3 (Consistency, ASN-0058), `M(d)(v_β + k) = a_β + k`, so the image is `{a_β + k : c ≤ k < c'}`. Define the I-span `ρ = (a_β + c, δ(c' − c, #a_β))`, where `a_β + c` follows the M-aux convention (ASN-0058): when `c = 0`, `a_β + 0 = a_β`; when `c ≥ 1`, `a_β + c` is the `c`-th ordinal increment. The reach is `(a_β + c) ⊕ δ(c' − c, #a_β) = a_β + c'` by M-aux associativity and the definition of ordinal displacement. The displacement `δ(c' − c, #a_β)` is positive since `c' − c ≥ 1`, and its action point equals `#a_β = #(a_β + c)` (ordinal increment preserves depth), satisfying T12 (SpanWellDefined, ASN-0034). The image `{a_β + k : c ≤ k < c'} ⊆ ⟦ρ⟧`, with equality at element level (depth `#a_β`). ∎

A single V-span crossing multiple mapping blocks produces multiple I-spans — one per overlapping block. This is not a degenerate case; it is the *normal* case when the selected content was assembled from multiple sources through transclusion. Each transcluded portion retains its original I-address — that is the definition of transclusion — so a contiguous V-selection may cover a discontiguous set of I-addresses. A selection of "AABB" where "AA" was transcluded from document X and "BB" from document Y produces two I-spans: one addressing the "AA" bytes in X's I-space, another addressing "BB" in Y's I-space.

**Lemma CL1 — ResolutionExistence.** For any document d with M(d) satisfying the arrangement invariants (S2, S8-fin, ASN-0036) and any V-span-set Ψ, there exists an endset `E ∈ Endset` with `image(d, Ψ) ⊆ coverage(E)`.

*Proof.* Let B be the canonical block decomposition of M(d) (exists by M11, ASN-0058). For each σ ∈ Ψ and each β ∈ B with `V(β) ∩ ⟦σ⟧ ≠ ∅`, CL0 yields one I-span. By B1 and B2 (Coverage, Disjointness, ASN-0058), each V-position in dom(M(d)) falls in exactly one block. The image of each V-position is therefore accounted for exactly once across all block projections. The finite collection of resulting I-spans is a well-formed endset (each span satisfies T12, the set is finite). Every address in `image(d, Ψ)` lies in the denotation of at least one CL0 I-span (at least one, since shared content may produce overlapping I-spans from distinct blocks — see S5, UnrestrictedSharing), establishing `image(d, Ψ) ⊆ coverage(E)`. ∎

The containment is strict in general: each CL0 I-span `(a_β + c, δ(c' − c, #a_β))` denotes an interval that includes tumblers deeper than `#a_β` — proper extensions of the element-level addresses in the image. By T0(b) and T1(ii), every element-level tumbler has infinitely many proper extensions within any span's range, so the coverage of any non-empty endset is infinite, while `image(d, Ψ)` is finite (S8-fin). Equality cannot hold.

The coverage *is* tight at element level. Within a single CL0 I-span arising from block β = (v_β, a_β, n) with overlap range [c, c'), the depth-`#a_β` members of the denotation are exactly `{a_β + k : c ≤ k < c'}`. Between consecutive ordinal increments `a_β + k` and `a_β + (k + 1)`, the only tumbler of depth `#a_β` in the half-open interval is `a_β + k` itself — the integer constraint at the last component forces `t_{#a_β} = (a_β)_{#a_β} + k`. These are precisely the I-addresses produced by M(d) for the overlapping V-positions.

We observe that I-spans from V-adjacent blocks in the canonical decomposition are non-adjacent in I-space. If consecutive blocks β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) produced I-adjacent output (a₂ = a₁ + n₁), they would also be V-adjacent (v₂ = v₁ + n₁, since they partition a contiguous V-range by D-CTG, ASN-0036). But V-adjacent and I-adjacent blocks satisfy the merge condition M7 (ASN-0058), contradicting the decomposition being maximally merged (M12). Non-adjacent blocks, however, may produce I-spans with overlapping coverage: if block β₁ maps V-positions to I-addresses a through a + 2 and a non-adjacent block β₃ maps different V-positions to I-addresses a + 1 through a + 3 (permitted by S5, UnrestrictedSharing, ASN-0036), the CL0 I-spans overlap at a + 1 and a + 2. The CL0 I-span collection is therefore not necessarily normalized — overlapping spans may arise from transcluded content.

**Definition — Resolve.** `resolve(d, Ψ)` is the finite endset constructed by collecting all CL0 I-spans from the canonical block decomposition of M(d):

  `resolve(d, Ψ) = {ρ_{β,σ} : σ ∈ Ψ, β ∈ B, V(β) ∩ ⟦σ⟧ ≠ ∅}`

where each `ρ_{β,σ}` is the I-span produced by CL0 for block β and V-span σ. This is a well-formed endset: a finite set of spans each satisfying T12 (ASN-0034). No normalization is required — `Endset = 𝒫_fin(Span)` (ASN-0043) admits any finite set of well-formed spans. CL0 I-spans from blocks with I-addresses of different depths are automatically disjoint: by T10 (PartitionIndependence, ASN-0034), tumblers under incomparable prefixes cannot coincide, so spans over I-addresses from different document origins occupy non-overlapping regions of T regardless of depth differences.

**CL2 — ResolutionContainment.** `image(d, Ψ) ⊆ coverage(resolve(d, Ψ))`.

Immediate from CL1: each element of `image(d, Ψ)` is an I-address `M(d)(v)` for some `v ∈ ⟦Ψ⟧ ∩ dom(M(d))`, which falls in exactly one CL0 I-span by B1 and B2.

Endset specifications may reference content across multiple documents — the from-endset might address content in document X, the to-endset content in document Y, while the link itself lives in document Z. For a V-space specification S = {(d₁, Ψ₁), ..., (dₘ, Ψₘ)}, define `resolve(S) = resolve(d₁, Ψ₁) ∪ ... ∪ resolve(dₘ, Ψₘ)`. Each (document, V-spans) pair resolves independently; the union captures the cross-document endsets permitted by L4(a) (ASN-0043).

One final observation on resolution. When a V-span-set covers V-positions outside dom(M(d)) — content that was removed from the arrangement but persists in the Istream (by S0) — those positions contribute nothing to the image. The resolved endset captures only content *currently arranged* in the source documents. Content that exists in the Istream but has no current arrangement mapping is unreachable through V-space resolution. It can, however, be referenced directly by I-address.

We extend `resolve` to handle both input forms uniformly. An *endset specification* is either a set of (document, V-spans) pairs `{(d₁, Ψ₁), ..., (dₘ, Ψₘ)}` or a direct I-span-set `E_I ∈ Endset`. For the V-space form, `resolve` operates as defined above. For the direct form:

  `resolve(E_I) = E_I`

The identity: no arrangement is consulted, no validation against dom(C) is performed. The link is created with whatever I-spans are provided. CL1 and CL2 apply only to the V-space form — they are stated in terms of a document d and V-span-set Ψ, which the direct form does not have. The direct form needs no resolution guarantee: the user provides the endset directly, so no V-to-I translation occurs and no containment claim arises. The CREATELINK postconditions CL3 and CL11 cover both input paths without case splitting because they are stated in terms of the resolved endsets (F, G, Θ), which are well-formed endsets regardless of which input form produced them.


## Extending the Transition Framework

ASN-0047 defines the system state as Σ = (C, E, M, R) with elementary transitions K.α (content), K.δ (entity), K.μ⁺/K.μ⁻/K.μ~ (arrangement), and K.ρ (provenance). ASN-0043 introduces the link store Σ.L but does not define transitions for it. We now integrate links into the transition framework.

The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store (ASN-0043).

**Extended initial state.** Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L12, L14 are satisfied by empty L; S3★'s link-subspace clause is vacuous (no link-subspace V-positions exist in M₀); P4★ reduces to P4 (which holds at Σ₀ per ASN-0047). This closes the inductive base for CL11.

All existing elementary transitions from ASN-0047 hold L in their frame: L' = L. In the extended state, **K.μ⁺ is amended with a content-subspace restriction**: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. We introduce two new elementary transitions for link creation.

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

**S3★ — GeneralizedReferentialIntegrity.** The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the pre-extension states of ASN-0047 have only content-subspace V-positions, for which S3★ reduces to S3. Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses; K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺ (ASN-0047) with a bijection `π : dom(M(d)) → dom(M'(d))` satisfying `M'(d)(π(v)) = M(d)(v)`. Since K.μ⁺ (amended) requires `subspace(v) = s_C` for new V-positions, K.μ⁺ cannot create link-subspace V-positions. We show K.μ~ fixes all link-subspace mappings by a cardinality argument. Let `dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_L}` denote the link-subspace V-positions. First, S3★ forces π to map link-subspace positions to link-subspace positions: if `v ∈ dom_L(M(d))` then `M(d)(v) ∈ dom(L)`, and `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`, so `subspace(π(v)) = s_L` by S3★ (a content-subspace position mapping to dom(L) would violate the content clause). Thus `π` restricted to `dom_L(M(d))` is an injection into `dom_L(M'(d))`. Now, since K.μ⁺ cannot create link-subspace V-positions, `|dom_L(M'(d))| ≤ |dom_L(M(d))|`. If K.μ⁻ removed `r ≥ 1` link-subspace positions, then `|dom_L(M'(d))| ≤ |dom_L(M(d))| − r`, and the injection from `dom_L(M(d))` (size N) into `dom_L(M'(d))` (size at most N − r) cannot exist. Therefore `r = 0` — no link-subspace positions are removed, and the bijection π acts as the identity on `dom_L(M(d))`. Content-subspace mappings are reordered within dom(C), preserving S3★'s content clause.

**K.μ⁺_L — LinkSubspaceExtension.** Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist — K.λ must precede this step)
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - m_L ≥ 2, where: if V_{s_L}(d) ≠ ∅, m_L is the common depth of existing link-subspace V-positions (determined by S8-depth); if V_{s_L}(d) = ∅, m_L is a parameter of the transition, subject only to m_L ≥ 2. The lower bound is structural: ordinal shift at depth 1 alters the subspace identifier (`shift([s_L], 1) = [s_L + 1]`, violating subspace closure TA7a), so the link subspace requires depth at least 2
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG)
  - #v_ℓ = m_L (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality). When `V_{s_L}(d) = ∅`: no link-subspace V-position exists in dom(M(d)), and `subspace(v_ℓ) = s_L`, so `v_ℓ ∉ dom(M(d))`. When `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), placing v_ℓ beyond all existing link-subspace positions. In both cases, `subspace(v_ℓ) = s_L ≠ s_C` ensures no collision with text-subspace positions (T7, SubspaceDisjointness). Therefore `v_ℓ ∉ dom(M(d))`.

The preconditions ensure that after the extension, D-CTG (contiguity), D-MIN (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

**Containment scoping.** The containment relation `Contains(Σ)` (ASN-0047) is defined as `{(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}` — unscoped across all subspaces. With link-subspace mappings, `Contains(Σ')` includes `(ℓ, d)` for every link ℓ mapped in d's arrangement. P4 requires `Contains(Σ) ⊆ R`, but provenance entries satisfy P7: `(A (a, d) ∈ R :: a ∈ dom(C))`. Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist. We define the content-scoped containment:

**Definition — ContentContainment.** `Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

**P4★ — ProvenanceBounds (content-subspace).** `Contains_C(Σ) ⊆ R`

P4★ supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4. Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ extends only content-subspace positions (by its amended precondition) and is coupled with K.ρ by J1★; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C.

**Coupling constraint scoping.** The coupling constraints J1, J1' (ASN-0047) were formulated before link-subspace mappings existed. They must be scoped to content-subspace arrangement extensions; otherwise J1 and P7 are mutually unsatisfiable — J1 would require provenance recording for the link address ℓ entering ran(M'(d)), but P7 requires every provenance entry to reference dom(C), and ℓ ∈ dom(L) with dom(L) ∩ dom(C) = ∅ (L14).

**J1★ — ExtensionRecordsProvenance (content-subspace).** `(A Σ → Σ', d, v, a : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C ∧ M'(d)(v) = a : (a, d) ∈ R')`

**J1'★ — ProvenanceRequiresExtension (content-subspace).** `(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C : M'(d)(v) = a))`

Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording: the link address ℓ enters ran(M'(d)) but `subspace(v_ℓ) = s_L ≠ s_C`, so J1★ does not apply. P7 (ProvenanceGrounding) — `(A (a, d) ∈ R :: a ∈ dom(C))` — is preserved because R is unchanged (K.μ⁺_L holds R in frame).

The coupling constraints for valid composites in the extended state Σ = (C, L, E, M, R) are J0, J1★, J1'★. J1★ and J1'★ replace J1 and J1' (ASN-0047) by scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.

We observe that these coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions." Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same state — a link present in L but absent from all current arrangements — but is constrained by D-CTG: removing an interior link-subspace V-position creates a gap in the contiguous range, and K.μ~ cannot close it (link-subspace mappings are fixed, as shown above). Only the maximum V-position can be removed without violating D-CTG (removing the minimum would violate D-MIN). Nelson's design suggests a different mechanism: link addresses are permanent and "not currently addressable" when withdrawn (LM 4/9), paralleling deleted bytes — the link transitions to inactive status while preserving its arrangement position, rather than being removed from M(d). The precise withdrawal mechanism is deferred to the open question on withdrawal invariants. The disc function still includes orphan links: `disc(a, r)` queries dom(L) directly, not arrangements. An orphan link is discoverable by I-address but unreachable through any document's current structure, paralleling deleted bytes that persist in the Istream after Vstream removal. We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29).


## The CREATELINK Composite

CREATELINK combines resolution and allocation. The user provides a home document d and endset specifications for three roles: from, to, and type. Each specification is an endset specification — either a set of (document, V-spans) pairs or a direct I-span-set. The system resolves each specification (V-space resolution or identity for direct I-spans), allocates a fresh link, and stores the result.

**CREATELINK(d, S_F, S_G, S_Θ):**

Let F = resolve(S_F), G = resolve(S_G), Θ = resolve(S_Θ), where each resolve dispatches according to the specification form.

*Precondition:*
- d ∈ E_doc
- A fresh link address ℓ is available satisfying K.λ's preconditions
- m_L ≥ 2, chosen by the operation when V_{s_L}(d) = ∅, determined by S8-depth when V_{s_L}(d) ≠ ∅
- Every V-span in each endset specification satisfies T12 (SpanWellDefined, ASN-0034): width > 0 and action point k ≤ #start — ensuring ⟦σ⟧ is well-defined for each input span

*Composite steps:*
1. K.λ: allocate ℓ in dom(L) with value (F, G, Θ)
2. K.μ⁺_L: extend M(d) at the next V-position v_ℓ in d's link subspace, mapping v_ℓ to ℓ

*Postcondition CL3:*

  (a) `ℓ ∈ dom(L') ∧ ℓ ∉ dom(L)` — a new link exists

  (b) `L'(ℓ) = (F, G, Θ)` — with the resolved endsets

  (c) `home(ℓ) = origin(ℓ) = d` — determined by the address alone (L2, ASN-0043)

  (d) `(A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))` — existing links unchanged (L12)

  (e) `C' = C` — content unchanged

  (f) `v_ℓ ∈ dom(M'(d)) ∧ M'(d)(v_ℓ) = ℓ` — the new link is placed in d's link subspace, where `v_ℓ = [s_L, 1, ..., 1]` (depth m_L, by D-MIN) when V_{s_L}(d) was empty, or `v_ℓ = shift(max(V_{s_L}(d)), 1)` (by D-CTG) otherwise

  (g) `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — the existing arrangement of d is unchanged

Step 2 places ℓ into d's arrangement, making the link an *out-link* of d. Nelson draws a sharp distinction: "a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not" (LM 2/31). An out-link lives in its home document's arrangement; an in-link is merely discoverable from the referenced document. CREATELINK produces one out-link (in d) and zero or more in-link relationships (one for each document whose content the endsets reference).

Step 2 is the elementary transition K.μ⁺_L defined above. Its preconditions ensure that v_ℓ maintains the link subspace's contiguity (D-CTG), minimum position (D-MIN), and depth uniformity (S8-depth). The referential integrity requirement is subspace-conditional (S3★): link-subspace mappings target dom(L), while text-subspace mappings target dom(C). Since K.λ in step 1 places ℓ into dom(L') before K.μ⁺_L executes, the precondition `ℓ ∈ dom(L')` is satisfied.

Note that the home document determines link ownership — not what the link points to. "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to" (Nelson, LM 4/12). A link in document Z whose endsets reference content in documents X and Y is owned by Z's owner. Neither X's nor Y's owner can modify or withdraw it.


## What Is Preserved

The most important property of CREATELINK is what it does *not* do.

**CL4 — ContentNonInterference.** CREATELINK preserves the content store: `C' = C`.

*Proof.* K.λ has C' = C in its frame. Step 2 modifies only M(d), which is independent of C by S9 (TwoStreamSeparation, ASN-0036). No step in the composite writes to C. ∎

The formal proof above is complete and sufficient. We observe that this guarantee is reinforced by five independent architectural principles, two of which (#2 and #4) are independently sufficient as formal proofs, while the remaining three provide design-level assurance:

*Separate storage.* The link is stored at the creator's address in the creator's document — `origin(ℓ) = d` — not at the referenced content's address. The link's home document "indicates who owns it, and not what it points to" (Nelson, LM 4/12).

*Istream immutability.* Content at I-addresses is permanent (S0, ASN-0036). No operation can modify existing content values. CREATELINK is not special; it inherits this guarantee.

*Owner-only modification (design intent).* The system is designed so that only the document owner can modify their content (Nelson, LM 2/29: "Only the owner has a right to withdraw a document or change it"). This principle is not yet formalized in the transition framework — K.α, K.μ⁺, and other transitions constrain structural validity but do not gate operations on ownership. Nevertheless, creating a link to someone else's published content is architecturally a non-owner action on the target, reinforcing the expectation that the target is unaffected.

*K.λ isolation.* K.λ writes to L; its frame explicitly leaves C, E, M, R unchanged. There is no mechanism in K.λ for altering C.

*Structural separation.* Links are "meta-virtual structures connecting parts of documents" (Nelson, LM 4/41) — a layer above content, not a modification of it.

The convergence of these five principles means content non-interference is not a fragile property that might be weakened by future extensions. It is overdetermined — the two formal guarantees (S0 and K.λ's frame) are independently sufficient, and the three design principles reinforce the architectural intent.

**CL5 — LinkPreservation.** CREATELINK preserves all existing links:

  `dom(L) ⊆ dom(L') ∧ (A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))`

Immediate from K.λ's effect: L' = L ∪ {ℓ ↦ (F, G, Θ)} with ℓ ∉ dom(L).

**CL6 — ArrangementConfinement.** CREATELINK modifies only M(d) for the home document d:

  `(A d' : d' ≠ d : M'(d') = M(d'))`

*Proof.* K.λ has M in frame. Step 2 modifies only M(d). ∎

Moreover, step 2 modifies only the *link subspace* of M(d). The text-subspace mappings — `{(v, M(d)(v)) : v ∈ dom(M(d)) ∧ subspace(v) = s_C}` — are invariant.

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

*Content invariants (ASN-0036).* S0 (ContentImmutability): C' = C by CL4. S1 (StoreMonotonicity): dom(C) ⊆ dom(C') since C' = C. S2 (ArrangementFunctionality): M'(d') = M(d') for d' ≠ d by CL6; M'(d) extends M(d) with one V-position in the link subspace, preserving functionality for both subspaces. S3★ (GeneralizedReferentialIntegrity): text-subspace mappings are unchanged, so `M(d)(v) ∈ dom(C)` holds for all `subspace(v) = s_C`; the new link-subspace mapping satisfies `M'(d)(v_ℓ) = ℓ ∈ dom(L')` with `subspace(v_ℓ) = s_L`. ✓

*Per-subspace arrangement invariants.* S8a (VPositionWellFormedness): the quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)` covers *all* V-positions with `v₁ ≥ 1`, including link-subspace positions. We must establish that `s_L ≥ 1`: by L1 (ASN-0043), every link address is element-level (`zeros(ℓ) = 3`), so by T4 (ASN-0034), every element-field component is strictly positive — in particular `fields(ℓ).E₁ = s_L > 0`. Since K.μ⁺_L uses the same identifier s_L for V-positions, link-subspace V-positions have `v₁ = s_L ≥ 1` and fall under S8a's quantifier. For text-subspace positions: unchanged. For the new link-subspace position v_ℓ: K.μ⁺_L places `v_ℓ = [s_L, 1, ..., 1]` (D-MIN) or `shift(max(V_{s_L}(d)), 1)` (D-CTG). In either case, every component of v_ℓ is strictly positive — s_L > 0 by the above, and the remaining components are 1 or incremented from positive values — so `zeros(v_ℓ) = 0 ∧ v_ℓ > 0`. ✓ S8-fin: adding one position to a finite set preserves finiteness. For the link subspace specifically: S8-depth is satisfied by K.μ⁺_L's precondition (`#v_ℓ = m_L`). D-CTG (VContiguity) and D-MIN (VMinimumPosition) are quantified over *all* subspaces S. For the text subspace (S = s_C): V_{s_C}(d) is unchanged. For the link subspace (S = s_L): K.μ⁺_L's precondition places v_ℓ at the minimum position if V_{s_L}(d) was empty, or at the next contiguous position if non-empty, satisfying both D-CTG and D-MIN. D-SEQ follows from D-CTG, D-MIN, S8-fin, and S8-depth (as derived in ASN-0036). ✓

*Link invariants (ASN-0043).* L0 (SubspacePartition): ℓ has fields(ℓ).E₁ = s_L by K.λ precondition. dom(L') ∩ dom(C') = (dom(L) ∪ {ℓ}) ∩ dom(C). Since ℓ ∉ dom(C) and dom(L) ∩ dom(C) = ∅ (L0 pre-state), the intersection is empty. L1 (LinkElementLevel): zeros(ℓ) = 3 by K.λ precondition. L1a (LinkScopedAllocation): origin(ℓ) = d by K.λ precondition. L12 (LinkImmutability): existing entries are unchanged; the transition adds ℓ without modifying any existing L entry. L12a (LinkStoreMonotonicity): dom(L) ⊂ dom(L'). L14 (DualPrimitive): dom(C') ∪ dom(L') = dom(C) ∪ dom(L) ∪ {ℓ}; disjointness holds since ℓ ∉ dom(C). ✓

*Transition invariants (ASN-0047).* P0 (ContentPermanence): C' = C. P1 (EntityPermanence): E' = E. P2 (ProvenancePermanence): R' = R. P3 (ArrangementMutabilityOnly): M(d) is extended by one link-subspace mapping (permitted by P3's extension clause); L is extended by one entry — L is a new state component not addressed by P3, but the extension is monotonic, consistent with P3's design. P4a (HistoricalFidelity): R' = R and dom(C') = dom(C), so all existing provenance entries `(a, d) ∈ R` retain their historical witnesses unchanged. P4★ (ProvenanceBounds, content-subspace): K.μ⁺_L adds ℓ to ran(M'(d)), but `subspace(v_ℓ) = s_L ≠ s_C`, so ℓ does not appear in Contains_C(Σ'). Text-subspace mappings are unchanged, so Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'. P5 (DestructionConfinement): only M and L change, both by extension — no information is lost. P6 (ExistentialCoherence): unchanged since dom(C) is unchanged. J1★, J1'★ (Provenance coupling): K.μ⁺_L adds ℓ to ran(M'(d)), but `subspace(v_ℓ) = s_L ≠ s_C`, so J1★ does not require provenance recording; R' = R. P7 (ProvenanceGrounding): `(A (a, d) ∈ R' :: a ∈ dom(C'))` holds since R' = R and dom(C') = dom(C). P7a (ProvenanceCoverage): unchanged since dom(C) is unchanged. P8 (EntityHierarchy): E is unchanged. ✓


## Worked Example

We verify CREATELINK against a concrete scenario. Let d_Z = `1.0.1.0.1` be a document whose text-subspace arrangement contains four positions — content "AABB" — assembled from two sources via transclusion.

**Setup.** The canonical block decomposition is B = {β₁, β₂}:

- β₁ = ([1, 1], `2.0.1.0.1.0.1.1`, 2): V-positions [1, 1] and [1, 2] map to content from document X at node 2
- β₂ = ([1, 3], `3.0.1.0.1.0.1.1`, 2): V-positions [1, 3] and [1, 4] map to content from document Y at node 3

The arrangement M(d_Z):

  M(d_Z)([1, 1]) = `2.0.1.0.1.0.1.1`,  M(d_Z)([1, 2]) = `2.0.1.0.1.0.1.2`

  M(d_Z)([1, 3]) = `3.0.1.0.1.0.1.1`,  M(d_Z)([1, 4]) = `3.0.1.0.1.0.1.2`

All I-addresses have depth 8 (zeros = 3, element-level). V-positions have depth 2 (s_C = 1). The decomposition is maximally merged: β₁ and β₂ are V-adjacent but not I-adjacent (origin(`2.0.1.0.1.0.1.1`) ≠ origin(`3.0.1.0.1.0.1.1`), so M16 applies).

**Resolution.** The user selects all four positions: V-span σ = ([1, 1], [0, 4]) with reach [1, 5]. CL0 produces two I-spans:

- ρ₁ from β₁: V-overlap [1, 1] through [1, 2], giving c = 0, c' = 2. I-span ρ₁ = (`2.0.1.0.1.0.1.1`, [0, 0, 0, 0, 0, 0, 0, 2]), reach `2.0.1.0.1.0.1.3`. Width is δ(2, 8), action point 8 ≤ 8. T12 satisfied. ✓
- ρ₂ from β₂: V-overlap [1, 3] through [1, 4], giving c = 0, c' = 2. I-span ρ₂ = (`3.0.1.0.1.0.1.1`, [0, 0, 0, 0, 0, 0, 0, 2]), reach `3.0.1.0.1.0.1.3`. ✓

resolve(d_Z, {σ}) = {ρ₁, ρ₂}. The two I-spans have different origins (T10), so their coverage is disjoint.

CL2 verification: image(d_Z, {σ}) = {`2.0.1.0.1.0.1.1`, `2.0.1.0.1.0.1.2`, `3.0.1.0.1.0.1.1`, `3.0.1.0.1.0.1.2`}. Each address falls in exactly one span's denotation: the first two in ⟦ρ₁⟧, the second two in ⟦ρ₂⟧. Containment holds. ✓

**Composite execution.** Suppose this is d_Z's first link. The link subspace identifier is s_L; link V-positions have depth m_L = 2.

Step 1 (K.λ): allocate ℓ with origin(ℓ) = `1.0.1.0.1` = d_Z, element field `s_L.1` (link subspace, first ordinal). Thus ℓ is element-level (zeros = 3), fields(ℓ).E₁ = s_L. Link value L'(ℓ) = (F, G, Θ) where F = {ρ₁, ρ₂}, G = ∅, Θ = ∅.

Step 2 (K.μ⁺_L): V_{s_L}(d_Z) was empty, so v_ℓ = [s_L, 1] (D-MIN, depth 2). M'(d_Z) = M(d_Z) ∪ {[s_L, 1] ↦ ℓ}.

**Postcondition verification.**

CL3(a): ℓ ∈ dom(L') ∧ ℓ ∉ dom(L). ✓ — K.λ adds ℓ.

CL3(b): L'(ℓ) = ({ρ₁, ρ₂}, ∅, ∅). ✓

CL3(c): home(ℓ) = origin(ℓ) = `1.0.1.0.1` = d_Z. ✓ — from T4, the document prefix is `1.0.1.0.1`.

CL3(d): existing links unchanged. ✓ — K.λ adds without modifying.

CL3(e): C' = C. ✓ — neither K.λ nor K.μ⁺_L modify C.

**Discovery verification (CL8).** For a_X = `2.0.1.0.1.0.1.1`: a_X ∈ coverage(F), since `2.0.1.0.1.0.1.1 ∈ ⟦ρ₁⟧ = {t : 2.0.1.0.1.0.1.1 ≤ t < 2.0.1.0.1.0.1.3}`. So ℓ ∈ disc(a_X, from). ✓ Similarly for `2.0.1.0.1.0.1.2` (in ⟦ρ₁⟧), `3.0.1.0.1.0.1.1` and `3.0.1.0.1.0.1.2` (in ⟦ρ₂⟧). ✓

**Invariant verification.** S3★: text-subspace mappings unchanged (target dom(C)); link-subspace mapping [s_L, 1] ↦ ℓ satisfies ℓ ∈ dom(L'). D-CTG for s_L: V_{s_L}(d_Z) = {[s_L, 1]}, a singleton — trivially contiguous. D-MIN for s_L: min = [s_L, 1]. S8-depth for s_L: one position — trivially uniform. P4★: subspace(v_ℓ) = s_L ≠ s_C, so ℓ ∉ Contains_C(Σ'); text-subspace unchanged, so Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'. J1★: subspace(v_ℓ) = s_L ≠ s_C, so no provenance recording required; R' = R. P7: R unchanged, dom(C) unchanged. ✓


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| image(d, Ψ) | `{M(d)(v) : v ∈ ⟦Ψ⟧ ∩ dom(M(d))}` — V-span image through arrangement | introduced |
| CL0 | Each mapping block / V-span overlap is representable by a single well-formed I-span | introduced |
| CL1 | For any d and Ψ, there exists E ∈ Endset with image(d, Ψ) ⊆ coverage(E) | introduced |
| resolve(d, Ψ) | Finite endset of CL0 I-spans from canonical block decomposition | introduced |
| CL2 | image(d, Ψ) ⊆ coverage(resolve(d, Ψ)) — resolution containment | introduced |
| S3★ | Subspace-conditional referential integrity: text → dom(C), link → dom(L); supersedes S3 | introduced |
| Contains_C(Σ) | `{(a, d) : d ∈ E_doc ∧ (E v : subspace(v) = s_C ∧ M(d)(v) = a)}` — content-scoped containment | introduced |
| P4★ | `Contains_C(Σ) ⊆ R` — provenance bounds scoped to content subspace; supersedes P4 | introduced |
| K.λ | Elementary transition: L' = L ∪ {ℓ ↦ (F, G, Θ)}, frame C' = C, E' = E, M' = M, R' = R | introduced |
| K.μ⁺_L | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ} | introduced |
| J1★ | Content-subspace scoping of J1: provenance recording only for subspace(v) = s_C | introduced |
| J1'★ | Content-subspace scoping of J1': provenance entries only from subspace(v) = s_C | introduced |
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

What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth — are there link-specific ordering constraints, capacity bounds, or structural properties that D-SEQ does not capture?

Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?

What must the system guarantee when concurrent CREATELINK operations target the same home document — must link address allocation be serialized, or can concurrent allocations produce distinct addresses without coordination?

What abstract properties must the discovery mechanism satisfy beyond completeness — must it support range queries over I-address intervals, or is point-level query sufficient?

Must the type endset reference content in a designated type namespace, or is any well-formed span valid as a type reference regardless of what the I-addresses contain?

When a link's from-endset and to-endset cover overlapping I-address ranges, what must the discovery function report — must it distinguish the endset role in which the address was found, or may it return the link once without role attribution?

What must the system guarantee about the ordering of links returned by discovery — creation order, address order, or is the result unordered?

What invariants must link withdrawal (removal from the current version of the home document) maintain with respect to the discovery function — must withdrawn links remain discoverable, or does withdrawal remove them from disc?

What must resolution guarantee when the arrangement changes between the moment the user selects content and the moment resolution executes — must it capture the selection-time arrangement, or is the resolution-time arrangement acceptable?
