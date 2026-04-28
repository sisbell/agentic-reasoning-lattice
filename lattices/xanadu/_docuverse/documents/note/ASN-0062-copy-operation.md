# ASN-0062: COPY Operation

*2026-03-21*

We are looking for the precise effect of placing existing Istream content at a position in a document's Vstream. The key word is *existing*: the content already holds permanent addresses in C; we are not creating new content but establishing a new arrangement over what is already there. Nelson variously calls this "inclusion," "virtual copy," or "transclusion" — the mechanism by which documents share content through reference rather than duplication.

The question decomposes: how is the source content identified, what happens to content already at the target position, what is preserved about the placed content's identity, and what invariants must the completed operation maintain?

We work with system state Σ = (C, E, M, R) per ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The content store is append-only (S0, P0). The arrangement M(d) is the mutable layer. COPY must specify exactly how it extends M(d) while leaving C untouched.


## The Fundamental Constraint

The Istream/Vstream separation (ASN-0036) distinguishes permanent content storage from mutable arrangement. An operation that modifies arrangement without creating content is, in the framework of ASN-0047, a composite of K.μ⁺ (arrangement extension), K.μ~ (arrangement reordering), and K.ρ (provenance recording) — with no K.α (content allocation) step. COPY is exactly such an operation.

Nelson: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents" [LM 2/36]. The word "copy" misleads — nothing is duplicated. A new arrangement is created over content that already exists and will exist forever.

**C0 — ArrangementOnly (INV).** A COPY transition Σ → Σ' satisfies:

`C' = C`

No content is created, modified, or removed. The content store is entirely in the frame. This follows from the absence of K.α in the composite. Since C grows only through K.α (ASN-0047, P0) and COPY includes none, C is unchanged.

C0 is not merely "happens to allocate nothing" — it is the *definition* of COPY's relationship to the content store. Any transition that allocates content is not a COPY; it is an INSERT or some other content-creating operation. Gregory's implementation confirms: `docopy` does not call `inserttextingranf` (the content allocator); it takes pre-existing I-address spans from the source and maps them into the target's arrangement.


## Source Resolution

COPY reads content from one or more source documents. The source is specified as an ordered sequence of content references, each naming a V-span in some document's current arrangement.

**Definition — ContentReference.** A *content reference* is a pair (d_s, σ) where d_s ∈ E_doc and σ = (u, ℓ) is a well-formed V-span (T12, ASN-0034) with ⟦σ⟧ ⊆ dom(M(d_s)). The V-positions named must lie within the source document's current arrangement.

**Definition — ContentReferenceSequence.** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₘ⟩ of content references with m ≥ 1. Different references may name different source documents.

To resolve a content reference, we extract the I-address runs corresponding to the named V-span. The source document's mapping may not be ordinal-contiguous across the full span — prior editing may have interleaved content from multiple allocations, fragmenting the V→I mapping into several contiguous I-address runs.

**Definition — Resolution.** Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧. By M11 and M12 (ASN-0058), f admits a unique maximally merged block decomposition ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

For a content reference sequence R = ⟨r₁, ..., rₘ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₘ)`

Each reference is resolved independently against its own source document. The total width is:

`w(R) = (+ j : 1 ≤ j ≤ k : nⱼ)`

where ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R).

The ordering of runs within each resolution preserves the source document's V-ordering: if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence. This is a consequence of the block decomposition being V-ordered (B1, ASN-0058).

**C1 — ResolutionIntegrity (LEMMA).** Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* S3 (ReferentialIntegrity, ASN-0036) guarantees M(d_s)(v) ∈ dom(C) for every v ∈ dom(M(d_s)). The resolution extracts exactly these I-addresses from the source arrangement. ∎


## Arrangement Contiguity

To specify COPY's displacement effect, we require the contiguity invariant introduced in ASN-0061. Write V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the V-positions in subspace S of document d.

**D-CTG — VContiguity (INV).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, w : u ∈ V_S(d) ∧ w ∈ V_S(d) ∧ u < w : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < w : v ∈ V_S(d)))`

Nelson states this directly: V-stream addresses run contiguously from position 1 through N [LM 4/30]. Without contiguity, displacement could create overlaps with content at gap positions, violating S2 (ArrangementFunctionality, ASN-0036).

When V_S(d) is contiguous with |V_S(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1.

**Definition — ValidInsertionPosition.** Given document d satisfying D-CTG with text-subspace positions {v₀, ..., v_{N−1}}, a V-position v is a *valid insertion position* when v = v₀ + j for some j with 0 ≤ j ≤ N. When N = 0, any v satisfying S8a and S8-depth for d's text subspace is valid.

There are N + 1 valid insertion positions: N positions targeting existing content (which will be displaced), plus one append position past the end.


## The COPY Transition

We now define COPY as a composite state transition. The definition proceeds in two phases: resolution (reading the source) and mutation (modifying the target).

**Definition — COPY.** A COPY into document d at position v from content reference sequence R is a composite transition Σ → Σ'.

*Preconditions.*

(P.1) d ∈ E_doc.

(P.2) M(d) satisfies D-CTG.

(P.3) v is a valid insertion position in d.

(P.4) Each rⱼ = (d_sⱼ, σⱼ) in R is a well-formed content reference.

(P.5) resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is evaluated in state Σ.

(P.6) w = w(R) ≥ 1.

*Phase 1 — Resolution.* The resolution is computed from the pre-state Σ. Specifically, resolve(R) reads M(d_sⱼ) from Σ for each source document d_sⱼ. The resulting I-address sequence is immutable for the remainder of the transition. No state modification occurs in this phase.

*Phase 2 — Mutation.* Let B be the maximally merged block decomposition of M(d) in state Σ. The new arrangement M'(d) is defined by a block decomposition B' constructed in five steps.

(i) *Split.* If v is interior to some block β = (v_β, a_β, n_β) ∈ B — meaning v_β < v < v_β + n_β — let c be the natural number with v = v_β + c. Split β at c (M4, ASN-0058) into β_L = (v_β, a_β, c) and β_R = (v, a_β + c, n_β − c). Replace β with β_L, β_R in B. If v is not interior to any block, no split occurs.

(ii) *Classify.* Partition B (after step i) into:

```
B_pre  = {β ∈ B : v_β + n_β ≤ v}     (blocks entirely before v)
B_post = {β ∈ B : v_β ≥ v}            (blocks at or after v)
```

After the split, these are disjoint and exhaustive.

(iii) *Shift.* For each β = (v_β, a_β, n_β) ∈ B_post, define the displaced block:

`β↑w = (v_β + w, a_β, n_β)`

The V-start advances by w; the I-start and width are unchanged. The I-addresses of displaced content are identical to those before displacement.

(iv) *Place.* From resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩, define placed blocks at consecutive V-positions starting from v:

`γⱼ = (v + (n₁ + ... + nⱼ₋₁), aⱼ, nⱼ)   for j = 1, ..., k`

with the convention n₁ + ... + n₀ = 0, so γ₁ = (v, a₁, n₁).

(v) *Compose.*

`B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post}`

*Effects.*

```
C' = C                                              (C0)
E' = E
M'(d) is the arrangement defined by B'
(A d' : d' ≠ d : M'(d') = M(d'))
R' = R ∪ {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}
```

The provenance extension records that d now contains certain I-addresses. By J1 (ASN-0047), this is required for every I-address newly appearing in d's arrangement. By J1', this is the only permitted extension.


## Well-Formedness of B'

We verify that B' is a valid block decomposition.

**B2 (Disjointness).** The three groups occupy non-overlapping V-ranges. B_pre blocks have V-reaches ≤ v (every v_β + n_β ≤ v by classification). Placed blocks γⱼ have V-positions in [v, v + w) — the first starts at v and the last ends at v + w by width summation. Shifted B_post blocks have V-starts ≥ v + w (each had v_β ≥ v, so v_β + w ≥ v + w). Within each group, pairwise disjointness is inherited: B_pre and B_post retain pairwise disjointness from B (M5, ASN-0058 for the split); the shift is an order-preserving injection on V-starts (TS1, ASN-0034); the γⱼ are pairwise disjoint by construction (consecutive, non-overlapping ranges).

**B1 (Coverage).** Let N = |dom_text(M(d))| and v₀ be the base. The pre-range [v₀, v) is covered by B_pre. The placed range [v, v + w) is partitioned by γ₁, ..., γₖ. The post-range [v + w, v₀ + N + w) is covered by B_post↑w. Together they cover all N + w positions.

**B3 (Consistency).** Pre-blocks: M'(d)(p) = M(d)(p) for p < v (unchanged). Placed blocks: M'(d)(v + offset) = aⱼ + (offset − offsetⱼ) for the appropriate j (by construction). Shifted post-blocks: for β = (v_β, a_β, n_β) ∈ B_post, M'(d)(v_β + w + i) = a_β + i = M(d)(v_β + i) for 0 ≤ i < n_β (same I-addresses at shifted V-positions).

**C2 — ContiguityPreservation (LEMMA).** COPY preserves D-CTG. If dom_text(M(d)) = {v₀ + j : 0 ≤ j < N}, then dom_text(M'(d)) = {v₀ + j : 0 ≤ j < N + w}.

*Derivation.* The pre-range contributes positions v₀ through v − 1 (contiguous by assumption). The placed range contributes positions v through v + w − 1 (contiguous by construction of the γⱼ — each begins where the previous ends). The post-range contributes positions v + w through v₀ + N + w − 1 (contiguous because shifting a contiguous range by a constant preserves contiguity, by TS1, ASN-0034). The three ranges are adjacent: v immediately follows v − 1, and v + w immediately follows v + w − 1. The union is contiguous with N + w elements. ∎

**Observation — Canonicalization.** B' may not be maximally merged. A placed block γⱼ might be I-adjacent to a neighboring block in B_pre or in B_post↑w. When this occurs, the canonical decomposition of M'(d) merges the adjacent blocks (M7, ASN-0058). The merged result is indistinguishable from one that was never separated (M8, ASN-0058). Gregory's implementation confirms: `isanextensionnd` silently merges I-adjacent crums when their homedoc fields match.


## Invariant Preservation

**C3 — InvariantPreservation (THEOREM).** The COPY composite preserves every foundational invariant.

*Derivation.*

P0 (ContentPermanence): C' = C by C0. P1 (EntityPermanence): E' = E. P2 (ProvenancePermanence): R' ⊇ R by construction. S0 (ContentImmutability): immediate from C' = C. These four are trivial consequences of the frame.

S2 (ArrangementFunctionality): M'(d) is a function because B' satisfies B2 — each V-position maps to exactly one I-address.

S3 (ReferentialIntegrity): we must show ran(M'(d)) ⊆ dom(C'). Pre-blocks and shifted post-blocks reference the same I-addresses as B, which satisfy S3 by assumption. The γⱼ blocks reference I-addresses satisfying C1 (ResolutionIntegrity). Since C' = C, all references are valid.

S8a (VPositionWellFormedness): new V-positions in the γⱼ blocks have the form v + offset, where v satisfies S8a and offset is an ordinal increment. Shift preserves zeros(v) = 0 and positivity (TS4, ASN-0034). Shifted post-block V-positions satisfy S8a by the same argument.

S8-depth (FixedDepthVPositions): ordinal shift preserves depth: #shift(v, n) = #v (OrdinalShift definition, ASN-0034). All new and shifted V-positions share the depth of the existing ones.

S8-fin (FiniteArrangement): |dom(M'(d))| = N + w, which is finite.

P4 (ProvenanceBounds): Contains(Σ') ⊆ R'. For d: every a ∈ ran(M'(d)) is either in ran(M(d)) — hence (a, d) ∈ R by P4 in the pre-state, hence in R' — or in ran(M'(d)) \ ran(M(d)) — hence (a, d) ∈ R' by the provenance extension. For d' ≠ d: M'(d') = M(d'), so Contains entries are unchanged, and R' ⊇ R covers them.

J0 (AllocationRequiresPlacement): no new content allocated (dom(C') \ dom(C) = ∅), so the condition is vacuously satisfied. ∎

**Observation — Atomicity.** The COPY transition is a composite of elementary steps (K.μ~ shifting the post-blocks, K.μ⁺ placing the new blocks, K.ρ recording provenance). By the ValidComposite definition (ASN-0047), a composite either completes with all coupling constraints holding at the final state, or does not occur. Nelson captures this as "canonical order" being "an internal mandate of the system" [LM 1/34]: after any change, the system is in a consistent state.


## Displacement

The construction makes displacement explicit, but we state it as a named property.

**C4 — Displacement (POST).** After COPY at position v with total width w:

`(A p ∈ dom(M(d)) : p ≥ v : M'(d)(p + w) = M(d)(p))`

`(A p ∈ dom(M(d)) : p < v : M'(d)(p) = M(d)(p))`

Every position at or after v shifts forward by w; every position before v is unchanged. Content is displaced, never overwritten.

Nelson specifies this for INSERT: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66]. COPY follows the same pattern. Since V-addresses form a dense, gapless sequence (D-CTG), placing material at position v necessarily shifts everything from v onward — there is no alternative.

**C5 — NoOverwrite (LEMMA).** COPY removes no existing V→I mapping from M(d):

`(A p ∈ dom(M(d)) :: (E q ∈ dom(M'(d)) : M'(d)(q) = M(d)(p)))`

*Derivation.* If p < v, take q = p; M'(d)(p) = M(d)(p) by C4. If p ≥ v, take q = p + w; M'(d)(p + w) = M(d)(p) by C4. In both cases the witness q exists in dom(M'(d)). ∎

C5 captures Nelson's absolute prohibition on overwrite. There is no OVERWRITE, REPLACE, or PUT operation in Xanadu. If one wishes to "replace" content, one DELETEs the old span and INSERTs or COPYs new content — two operations, preserving the old content in Istream for historical backtrack. The architecture permits only displacement (INSERT, COPY), removal (DELETE), and transposition (REARRANGE).


## Structural Identity

We arrive at the property that distinguishes COPY from all content-creating operations. The I-addresses placed in the target are *the same addresses* as in the source. This is not a runtime property the system must enforce — it is a structural consequence of how COPY is defined.

**C6 — IdentityPreservation (INV).** Let resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩. For each placed block γⱼ = (v + offset_j, aⱼ, nⱼ):

`(A i : 0 ≤ i < nⱼ : M'(d)(v + offset_j + i) = aⱼ + i)`

and each aⱼ + i appears in the source document's arrangement:

`(A i : 0 ≤ i < nⱼ : aⱼ + i ∈ ran(M(d_sⱼ)))`

where d_sⱼ is the source document from which (aⱼ, nⱼ) was resolved.

The I-address *is* the identity. Two documents sharing I-addresses share content in the strongest possible sense — not merely equal bytes, but the same bytes at the same permanent addresses. Nelson: "Non-native byte-spans are called inclusions or virtual copies" [LM 4/11]. The word "virtual" does essential work: these are not actual copies but references that resolve to the original I-addresses.

Content identity is based on creation, not value. Two users who independently type identical text create different Istream content at different I-addresses — those bytes are equal in value but distinct in identity. When one user transcludes the other's text via COPY, both documents share the same I-addresses. The system can distinguish "wrote the same words independently" from "quoted from the original" — because COPY shares I-addresses while independent creation allocates fresh ones.

**C7 — OriginInvariance (LEMMA).** For every I-address a in the placed content:

`origin(a) = origin(a_source)`

where a_source is the same address in the source document's arrangement. Since COPY does not transform I-addresses — it extracts them from the source and places them unchanged into the target — the origin of each placed byte identifies the document that *originally created* it, not the source document that was read, not the target document that now arranges it.

*Derivation.* The resolution function extracts I-addresses directly from the source POOM. The placement function writes them into the target POOM. At no point is an I-address modified. The origin function (ASN-0036) extracts the document-level prefix from the I-address, which is a structural property of the address itself (S7, ASN-0036). Since the address is unchanged, the origin is unchanged. ∎

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This is not an inspection capability layered atop COPY; it is a structural consequence of the I-address encoding the creating document's tumbler prefix. No separate provenance metadata is required — the address *is* the provenance.


## Source Isolation

COPY reads the source arrangement but does not modify it.

**C8 — SourceIsolation (POST).** For every document d' ≠ d (including every source document d_sⱼ where d_sⱼ ≠ d):

`M'(d') = M(d')`

*Derivation.* The COPY composite modifies only M(d). By the frame conditions of K.μ⁺ and K.μ~ (ASN-0047): M'(d') = M(d') for all d' ≠ d. ∎

Nelson states this guarantee unconditionally: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals" [LM 2/45]. The source document's content, arrangement, version history, and ownership are unaffected. The only system-wide effect beyond the target's arrangement is the provenance extension R' ⊇ R, which records that the target now contains certain I-addresses — but this modifies R, not the source document.

The reverse also holds. The source owner may subsequently modify their own arrangement — removing the copied content from their Vstream via DELETE — and the target's arrangement is unaffected. Both documents operate independently on their own Vstreams over shared Istream content. The shared I-addresses persist in C regardless of what either document does to its arrangement (S0, S6 from ASN-0036). Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].


## Transitive Identity

If document B acquired content from document A through COPY, and document C then copies that content from B, does C end up with A's original I-addresses? Yes — necessarily.

**C9 — TransitiveIdentity (LEMMA).** Let Σ₀ →^{COPY₁} Σ₁ →^{COPY₂} Σ₂ be two successive COPY transitions where COPY₁ places content from A into B, and COPY₂ places that content from B into C. The I-addresses placed in C are the same I-addresses that A's arrangement contained in Σ₀.

*Derivation.* COPY₁ extracts I-addresses from M₀(A) and places them in M₁(B) without modification (C6). COPY₂ extracts I-addresses from M₁(B) — which include the addresses placed by COPY₁ — and places them in M₂(C) without modification (C6 again). At every step, the addresses are permanent values from dom(C), never transformed. The resolution function at each hop reads I-addresses out of the source's POOM and passes them through unchanged; no address translation occurs at any point in the chain. ∎

The transitivity holds to arbitrary depth. Each hop is structurally identical: resolution extracts I-addresses from the arrangement; placement writes them into a new arrangement. The I-address propagates unchanged because COPY *cannot* transform it — the address is an input to the arrangement, not a computed output. If D copies from C, E from D, and so on, every document in the chain holds the same I-addresses that A originally allocated.

Gregory's implementation confirms this at the code level: `specset2ispanset` walks the source POOM and returns I-coordinates stored in the crums; `insertpm` writes those same coordinates into the target POOM. No intermediate representation translates or re-allocates I-addresses. The POOM is a coordinate-mapping structure, and COPY propagates coordinates by value.

**Corollary.** For any I-address a appearing in N documents through any chain of COPY operations:

`(A d₁, d₂ : a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂)) : origin(a) computed from d₁ = origin(a) computed from d₂)`

The origin is a function of the I-address alone. All N documents agree on the home document of every shared byte.


## Multi-Source Composition

When a content reference sequence names multiple source documents, each source is resolved independently and the results are concatenated.

**C10 — MultiSourceContiguity (LEMMA).** Let R = ⟨r₁, ..., rₘ⟩ with resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ and total width w. The placed blocks γ₁, ..., γₖ occupy a single contiguous V-range [v, v + w) in the target.

*Derivation.* By step (iv) of the COPY definition, each γⱼ starts immediately where the previous one ends: γⱼ starts at v + (n₁ + ... + nⱼ₋₁) and has width nⱼ, so it ends at v + (n₁ + ... + nⱼ). The last block γₖ ends at v + w. The placed blocks partition [v, v + w) into consecutive sub-ranges with no gaps. ∎

**Observation — Cross-Origin Block Boundaries.** Mapping blocks from different origin documents cannot merge, even when V-adjacent in the target. If γᵢ and γᵢ₊₁ have origin(aᵢ) ≠ origin(aᵢ₊₁), then by M16 (CrossOriginMergeImpossibility, ASN-0058), they cannot be I-adjacent and therefore cannot merge. The canonical decomposition necessarily preserves their boundary.

The number of blocks in the canonical decomposition of M'(d) is bounded below by the number of distinct-origin I-address runs in the placed content. Content from different creating documents remains structurally distinguishable through the block decomposition, even though the V-space presents a seamless sequence to the reader.


## Self-Transclusion

When a source document equals the target (d_s = d), the resolution reads M(d) while the mutation modifies M(d). The COPY definition resolves this by construction.

**C11 — SnapshotResolution (INV).** When d_s = d in a content reference, resolve(d, σ) is evaluated on M(d) in the pre-state Σ. The mutation phase may shift V-positions within M(d) that overlap with ⟦σ⟧, but the resolved I-address sequence is immutable once computed.

This is not an additional constraint — it follows from COPY being defined as a composite transition whose resolution is a function of the pre-state. Phase 1 (resolution) reads; Phase 2 (mutation) writes. Gregory's implementation confirms this ordering: `specset2ispanset` (resolution) runs to completion at `do1.c:54` before `insertpm` (mutation) begins at `do1.c:60`. The I-address sequence is computed and held in task-local memory; subsequent POOM shifts cannot affect it.

After self-transclusion, the target document may contain the same I-addresses at multiple V-positions. This is within-document sharing, consistent with S5 (UnrestrictedSharing, ASN-0036). The shared I-addresses cannot merge across their distinct V-occurrences because the merge condition (M7, ASN-0058) requires I-adjacency: a₂ = a₁ + n₁. When two blocks share the same I-start (a₂ = a₁), the condition requires a₁ = a₁ + n₁, which fails for n₁ ≥ 1 by TA-strict (ASN-0034). The distinct occurrences remain permanently distinguishable in the block decomposition (M14, ASN-0058).


## Provenance Completeness

The provenance relation R records which documents have ever contained which I-addresses. COPY extends R by adding (a, d) for every I-address a that is newly present in d's arrangement.

**C12 — ProvenanceCompleteness (POST).** After COPY:

`(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

*Derivation.* By J1 (ExtensionRecordsProvenance, ASN-0047), every I-address that newly appears in a document's arrangement must be recorded in R'. The COPY definition adds exactly these pairs. ∎

This ensures that content discovery — finding all documents that share a given I-address — immediately reflects the COPY result. Given any I-address a, the system can query R to find every document that has ever arranged a into its Vstream. Gregory's implementation creates one DOCISPAN entry per I-address run at `do1.c:62`, indexed by the target document's ISA.

**Observation — Provenance Records the Target, Not the Source.** The pair (a, d) records that document d contains I-address a. It does *not* record where d obtained a from. The chain of custody (A transcluded to B, B transcluded to C) is not stored in R; it is reconstructable from the I-addresses themselves, because all documents in the chain share the same addresses (C9) and origin(a) identifies the creating document (C7).

Provenance recording is monotonic: R' ⊇ R, and once (a, d) ∈ R, it remains in R forever (P2, ASN-0047). Even if d subsequently DELETEs the content from its arrangement, the provenance record persists — recording the historical fact that d once contained a. This is consistent with Nelson's "append-only" philosophy: the system remembers what was, even when the current arrangement has moved on.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ContentReference | (d_s, σ) with d_s ∈ E_doc, ⟦σ⟧ ⊆ dom(M(d_s)) | introduced |
| ContentReferenceSequence | ordered list ⟨r₁, ..., rₘ⟩ with m ≥ 1 | introduced |
| resolve(d_s, σ) | maximally merged I-address runs from M(d_s)\|⟦σ⟧ | introduced |
| COPY | composite transition: resolve then displace-and-place | introduced |
| C0 | C' = C — no content allocation | introduced |
| C1 | every resolved I-address is in dom(C) | introduced |
| C2 | COPY preserves D-CTG: N + w positions after, N before | introduced |
| C3 | COPY preserves all foundational invariants | introduced |
| C4 | positions ≥ v shift by w; positions < v unchanged | introduced |
| C5 | no existing V→I mapping is removed | introduced |
| C6 | placed I-addresses are the same addresses as in the source | introduced |
| C7 | origin(a) is unchanged — determined solely by the I-address | introduced |
| C8 | source documents' arrangements are unmodified | introduced |
| C9 | I-address identity propagates transitively through copy chains | introduced |
| C10 | multiple source references produce one contiguous V-range in target | introduced |
| C11 | self-transclusion resolves source in pre-state before mutation | introduced |
| C12 | provenance recorded for every newly-arranged I-address | introduced |


## Open Questions

- Must link endpoints anchored within the displaced V-range shift together with the displaced content, or may they remain at their original V-positions?
- What invariants distinguish a location-fixed transclusion (showing the source's current state) from a time-fixed transclusion (pinned to a specific version)?
- Must the provenance relation R support complete enumeration of all documents sharing a given I-address, and if so, with what completeness and latency guarantees?
- What authorization invariants must hold when content is copied from a document not owned by the copier?
- Must every version of a document independently satisfy D-CTG, or may historical versions contain gaps after content has been deleted from the current version?
- What serialization guarantees must the system provide when multiple COPY operations target the same document in concurrent requests?
- May the system compact the provenance relation R by removing entries (a, d) where a ∉ ran(M(d)), or must historical provenance persist indefinitely?
