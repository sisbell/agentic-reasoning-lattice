# ASN-0067: COPY Operation

*2026-03-21*

We are looking for the precise effect of placing existing Istream content at a position in a document's Vstream. The key word is *existing*: the content already holds permanent addresses in C; we are not creating new content but establishing a new arrangement over what is already there. Nelson variously calls this "inclusion," "virtual copy," or "transclusion" — the mechanism by which documents share content through reference rather than duplication. The word "copy" misleads; nothing is duplicated.

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

The question decomposes: how is the source content identified, what happens to content already at the target position, what is preserved about the placed content's identity, and what invariants must the completed operation maintain?

We work with system state Σ = (C, E, M, R) per ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The content store is append-only (S0, P0). The arrangement M(d) is the mutable layer. COPY must specify exactly how it extends M(d) while leaving C untouched.


## The Fundamental Constraint

The Istream/Vstream separation (ASN-0036) distinguishes permanent content storage from mutable arrangement. An operation that modifies arrangement without creating content is, in the framework of ASN-0047, a composite of K.μ⁺ (arrangement extension), K.μ~ (arrangement reordering), and K.ρ (provenance recording) — with no K.α (content allocation) step. COPY is exactly such an operation.

**C0 — ArrangementOnly (FRAME).** A COPY transition Σ → Σ' satisfies:

`C' = C`

No content is created, modified, or removed. The content store is entirely in the frame. This follows from the absence of K.α in the composite. Since C grows only through K.α (ASN-0047, P0) and COPY includes none, C is unchanged.

C0 is not merely "happens to allocate nothing" — it is the *definition* of COPY's relationship to the content store. Any transition that allocates content is not a COPY; it is an INSERT or some other content-creating operation. Nelson makes the distinction sharp:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The placed content *appears* as part of the document — it has an ordinal position in the byte stream "just as if" it were native. But it is not native. The connection to the original is structural and permanent.

We observe an immediate consequence. Since C' = C and the I-address allocation mechanism produces addresses in dom(C) only through K.α, the set dom(C) is unchanged. Any allocator that determines the "next available" I-address by scanning existing content finds no change after COPY. Gregory confirms: `docopy` does not call `inserttextingranf` (the allocation function that appends to the content store). A subsequent content-creating operation in the target document receives I-addresses contiguous with whatever was last allocated there, as if the COPY had never occurred.

**C0a — AllocationInvariance (LEMMA).** For any document d', the set of I-addresses allocated under d' is unchanged by COPY:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

*Derivation.* dom(C') = dom(C) by C0. The origin function (S7, ASN-0036) depends only on the I-address itself. Every element of the left set appears in the right and conversely. ∎


## Source Resolution

COPY reads content from one or more source documents. The source is specified as an ordered sequence of content references, each naming a V-span in some document's current arrangement.

**Definition — ContentReference.** A *content reference* is a pair (d_s, σ) where d_s ∈ E_doc and σ = (u, ℓ) is a level-uniform V-span — that is, T12 (ASN-0034) holds and `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036). The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies. The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

Since `#u = #ℓ = m`, dom(M(d_s)) contains only depth-m V-positions (S8-depth), and reach(σ) has depth m (S6), the depth-m restriction is structurally guaranteed.

**Definition — ContentReferenceSequence.** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.

To resolve a content reference, we extract the I-address runs corresponding to the named V-span. The source document's mapping may not be ordinal-contiguous across the full span — prior editing may have interleaved content from multiple allocations, fragmenting the V→I mapping into several contiguous I-address runs.

**Definition — Resolution.** Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧.

**C1a — RestrictionDecomposition (COROLLARY).** M11 and M12 (ASN-0058) hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.* (i) S2 (functionality): f is a restriction of M(d_s), which is functional by S2; a restriction of a function is a function. (ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), which is finite by S8-fin; a subset of a finite set is finite. (iii) S8-depth (fixed depth): every position in dom(f) belongs to dom(M(d_s)), so all share the common depth m of subspace u₁ in d_s.

*Extension of M11/M12.* M11 (CanonicalExistence) constructs a maximally merged decomposition by iterating: while any two blocks satisfy the merge condition (M7), merge them. Termination requires finiteness of the decomposition — guaranteed by S8-fin since the initial block count is at most |dom(f)|. Each merge step requires only B3 (consistency with f's values) — guaranteed by S2. M12 (CanonicalUniqueness) identifies the maximally merged decomposition with the set of maximal runs of f, using only pointwise evaluation of f — independent of whether f is a full arrangement or a restriction. Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth; they apply to f verbatim. ∎

The decomposition yields ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

The ordering of runs within each resolution preserves the source document's V-ordering: if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence. This is a consequence of the block decomposition being V-ordered (B1, ASN-0058). Gregory's implementation confirms: `incontextlistnd` (the POOM traversal function) performs insertion-sort by V-address during tree traversal, regardless of the internal sibling order that rebalancing may produce. The resulting I-span list is always V-sorted before reaching the mutation phase.

For a content reference sequence R = ⟨r₁, ..., rₚ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

Each reference is resolved independently against its own source document's POOM. The total width is:

`w(R) = (+ j : 1 ≤ j ≤ k : nⱼ)`

where ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R).

**C1 — ResolutionIntegrity (LEMMA).** Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* S3 (ReferentialIntegrity, ASN-0036) guarantees M(d_s)(v) ∈ dom(C) for every v ∈ dom(M(d_s)). The resolution extracts exactly these I-addresses from the source arrangement. ∎


## Displacement

We require the contiguity invariant from ASN-0036. Write V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the V-positions in subspace S of document d.

Nelson states that V-stream addresses run contiguously: "The digit after the one indicates the byte position in the current ordering of bytes" [LM 4/30]. Without contiguity, displacement could create overlaps with content at gap positions, violating S2 (ArrangementFunctionality, ASN-0036).

When V_S(d) is contiguous with |V_S(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN, ASN-0036) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ, ASN-0036).

**Definition — ValidInsertionPosition.** A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Then v = min(V_S(d)) + j for some j with 0 ≤ j ≤ N, and #v equals the existing subspace depth (S8-depth).

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. This is the canonical minimum position required by D-MIN (ASN-0036).

In both cases, S = v₁ is the subspace identifier.

There are N + 1 valid insertion positions: N positions targeting existing content (which will be displaced), plus one append position past the end.

Nelson is explicit about what happens to content at the target: it is displaced, never overwritten. "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66]. Though this passage describes INSERT, COPY follows the same pattern — both place content at a V-position, and both shift everything from that position onward.

Three layers of the architecture rule out overwrite:

First, Istream is append-only: "Instead, suppose we create an append-only storage system" [LM 2/14]. An overwrite would require destroying Istream content, contradicting the append-only guarantee.

Second, Vstream is an arrangement, not a container. Editing means changing the mapping. An overwrite would require removing an existing V→I entry and replacing it — but there is no atomic overwrite in the vocabulary of state transitions (ASN-0047). One must delete then insert: two operations.

Third, Nelson's non-destruction guarantee: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals" [LM 2/45]. An overwrite would "damage" whatever occupied the target position.


## The COPY Transition

We now define COPY as a composite state transition. The definition proceeds in two phases: resolution (reading the source) and mutation (modifying the target).

**Definition — COPY.** A COPY into document d at position v from content reference sequence R is a composite transition Σ → Σ'.

*Preconditions.*

(P.1) d ∈ E_doc.

(P.2) M(d) satisfies D-CTG (ASN-0036).

(P.3) v is a valid insertion position in d.

(P.4) Each rⱼ = (d_sⱼ, σⱼ) in R is a well-formed content reference.

(P.5) resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is evaluated in state Σ.

(P.6) w = w(R) ≥ 1.

*Phase 1 — Resolution.* The resolution is computed from the pre-state Σ. Specifically, resolve(R) reads M(d_sⱼ) from Σ for each source document d_sⱼ. The resulting I-address sequence is immutable for the remainder of the transition. No state modification occurs in this phase.

This is not an additional constraint bolted on for safety — it is a structural consequence of the operation being defined as a function of the pre-state. The resolution reads; the mutation writes. Gregory's implementation confirms the ordering: `specset2ispanset` (resolution) runs to completion before `insertpm` (mutation) begins. The I-address sequence is computed and held in task-local memory; subsequent POOM shifts cannot affect it.

*Phase 2 — Mutation.* Let B be the maximally merged block decomposition of M(d) in state Σ (M11, M12, ASN-0058). The new arrangement M'(d) is defined by a block decomposition B' constructed in five steps.

(i) *Split.* If v is interior to some block β = (v_β, a_β, n_β) ∈ B — meaning v_β < v < v_β + n_β — let c be the natural number with v = v_β + c. Split β at c (M4, ASN-0058) into β_L = (v_β, a_β, c) and β_R = (v, a_β + c, n_β − c). Replace β with β_L, β_R in B. If v is not interior to any block, no split occurs.

(ii) *Classify.* Let S = v₁ (the subspace identifier of the insertion position). First partition B (after step i) by subspace:

```
B_S     = {β ∈ B : (v_β)₁ = S}        (blocks in the target subspace)
B_other = {β ∈ B : (v_β)₁ ≠ S}        (blocks in other subspaces)
```

B_other is entirely in the frame — these blocks are not shifted or modified. Then partition B_S into:

```
B_pre  = {β ∈ B_S : v_β + n_β ≤ v}    (blocks before v in subspace S)
B_post = {β ∈ B_S : v_β ≥ v}           (blocks at or after v in subspace S)
```

After the split, B_pre and B_post are disjoint and exhaustive within B_S. The split in step (i) ensures no block in B_S straddles the insertion point. B_other is disjoint from both by T7 (SubspaceDisjointness, ASN-0034).

(iii) *Shift.* For each β = (v_β, a_β, n_β) ∈ B_post, define the displaced block:

`β↑w = (v_β + w, a_β, n_β)`

The V-start advances by w; the I-start and width are unchanged. The I-addresses of displaced content are identical to those before displacement. This is the "increase by the length" that Nelson specifies.

(iv) *Place.* From resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩, define placed blocks at consecutive V-positions starting from v:

`γⱼ = (v + (+ i : 1 ≤ i < j : nᵢ), aⱼ, nⱼ)   for j = 1, ..., k`

with the convention that the empty sum is 0, so γ₁ = (v, a₁, n₁).

(v) *Compose.*

`B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post} ∪ B_other`

*Effects.*

```
C' = C                                              (C0)
E' = E
M'(d) is the arrangement defined by B'
(A p : p ∈ dom(M(d)) ∧ subspace(p) ≠ S : M'(d)(p) = M(d)(p))   (non-target frame)
(A d' : d' ≠ d : M'(d') = M(d'))
R' = R ∪ {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}
```

The non-target frame condition ensures that all subspaces other than S — including the link subspace (v₁ = 0) and any other text subspaces — are preserved unchanged. This is consistent with B_other = {β ∈ B : (v_β)₁ ≠ S} being unchanged in the composition.

The provenance extension records that d now contains certain I-addresses. By J1 (ASN-0047), this is required for every I-address newly appearing in d's arrangement. By J1', this is the only permitted extension.

**Elementary Decomposition.** ValidComposite (ASN-0047) requires a finite sequence of elementary transitions where each step satisfies its precondition at the intermediate state. The decomposition depends on whether B_post is empty.

*Case 1: B_post ≠ ∅.* K.μ~ is defined in ASN-0047 as a distinguished composite of K.μ⁻ and K.μ⁺, not an elementary transition. Unfolding it, the COPY composite decomposes into four elementary steps: Σ = Σ₀ →^{K.μ⁻} Σ₁ →^{K.μ⁺} Σ₂ →^{K.μ⁺} Σ₃ →^{K.ρ} Σ₄ = Σ':

*Step 1 (K.μ⁻).* Remove B_post entries from M(d). Within subspace S, the remaining text positions are [v₀, v) only; non-target subspace positions are unchanged. Precondition at Σ₀: d ∈ E_doc (P.1); B_post ≠ ∅ ensures dom(M₁(d)) ⊂ dom(M₀(d)) (strict contraction). Frame: C₁ = C, E₁ = E, R₁ = R.

*Step 2 (K.μ⁺).* Add the shifted B_post entries {β↑w : β ∈ B_post}, placing them at V-positions [v + w, v₀ + N + w). Precondition at Σ₁: d ∈ E_doc; every I-address in the shifted blocks is in dom(C₁) = dom(C) (these are the same I-addresses as in B_post, which satisfy S3); shifted V-positions satisfy S8a (ordinal shift preserves positivity and zero-count) and S8-depth (ordinal shift preserves depth); dom(M₂(d)) is finite; B_post ≠ ∅ ensures dom(M₂(d)) ⊃ dom(M₁(d)) (strict extension). Frame: C₂ = C, E₂ = E, R₂ = R. Steps 1–2 together effect the K.μ~ reordering. Within subspace S, the intermediate arrangement after step 1 has domain {v₀, ..., v − 1}; after step 2 it is {v₀, ..., v − 1} ∪ {v + w, ..., v₀ + N + w − 1} — a gap at [v, v + w). Non-target subspaces retain their original positions throughout. This intermediate state is reachable by a valid composite. Steps 1–2 form K.μ~ whose corollary (ASN-0047) gives ran(M₂(d)) = ran(M₀(d)); J0 holds because dom(C) is unchanged; J1 holds vacuously because ran(M₂(d)) \ ran(M₀(d)) = ∅; J1' holds because R₂ = R₀. Yet the intermediate state violates D-CTG. D-CTG is thus not an invariant of all reachable states — it is a design constraint that complete operations are expected to preserve at their endpoints. COPY restores D-CTG by the end of step 3.

*Step 3 (K.μ⁺).* Fill the gap with placed blocks γ₁, ..., γₖ, extending dom(M₂(d)) by positions [v, v + w). Precondition at Σ₂: d ∈ E_doc; every new I-address aⱼ + i ∈ dom(C₂) = dom(C) (by C1); new V-positions satisfy S8a (same depth and positivity as existing positions); M₃(d) satisfies S8-depth (placed blocks share depth m); dom(M₃(d)) is finite (N + w). Frame: C₃ = C, E₃ = E, R₃ = R.

*Step 4 (K.ρ, repeated).* For each a ∈ ran(M₃(d)) \ ran(M(d)), record (a, d) ∈ R. Precondition at Σ₃: a ∈ dom(C₃) = dom(C) (by C1) and d ∈ E_doc (P.1). Frame: C₄ = C, E₄ = E, M₄ = M₃.

Coupling constraints at (Σ₀, Σ₄): J0 holds vacuously (dom(C₄) \ dom(C₀) = ∅). J1 holds by step 4 construction. J1' holds because every (a, d) ∈ R₄ \ R₀ was added in step 4 for some a ∈ ran(M₄(d)) \ ran(M₀(d)).

*Case 2: B_post = ∅.* This occurs when v = v₀ + N (append position) or when N = 0 (empty text subspace). No content exists at or after v, so no reordering is needed. The composite reduces to two steps: Σ = Σ₀ →^{K.μ⁺} Σ₁ →^{K.ρ} Σ₂ = Σ':

*Step 1 (K.μ⁺).* Add placed blocks γ₁, ..., γₖ at V-positions [v, v + w). Precondition at Σ₀: d ∈ E_doc (P.1); every I-address aⱼ + i ∈ dom(C) (by C1); new V-positions satisfy S8a (depth m, all components positive); M₁(d) satisfies S8-depth; dom(M₁(d)) = dom(M₀(d)) ∪ [v, v + w) is finite (N + w); strict extension holds since w ≥ 1 (P.6). Frame: C₁ = C, E₁ = E, R₁ = R.

*Step 2 (K.ρ, repeated).* For each a ∈ ran(M₁(d)) \ ran(M(d)), record (a, d) ∈ R. Precondition at Σ₁: a ∈ dom(C₁) = dom(C) (by C1) and d ∈ E_doc (P.1). Frame: C₂ = C, E₂ = E, M₂ = M₁.

Coupling constraints at (Σ₀, Σ₂): J0 holds vacuously (dom(C₂) \ dom(C₀) = ∅). J1 holds by step 2 construction. J1' holds because every (a, d) ∈ R₂ \ R₀ was added in step 2 for some a ∈ ran(M₂(d)) \ ran(M₀(d)).

In both cases, the high-level COPY definition (Phase 2, steps i–v) produces the same B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post} ∪ B_other — the distinction is only in how the composite is decomposed into elementary transitions for the ValidComposite verification.


## Well-Formedness of B'

We verify that B' is a valid block decomposition.

**B2 (Disjointness).** The four groups occupy non-overlapping V-ranges. B_pre blocks have V-reaches ≤ v (every v_β + n_β ≤ v by classification). Placed blocks γⱼ have V-positions in [v, v + w) — the first starts at v and the last ends at v + w by width summation. Shifted B_post blocks have V-starts ≥ v + w (each had v_β ≥ v, so v_β + w ≥ v + w). B_other blocks have (v_β)₁ ≠ S, while B_pre, placed blocks, and shifted B_post all have first component S — disjoint by T7 (SubspaceDisjointness, ASN-0034). Within each group, pairwise disjointness is inherited: B_pre and B_post retain pairwise disjointness from B (M6f, ASN-0058 — the split preserves decomposition-level B2); the shift is an order-preserving injection on V-starts (TS1, ASN-0034); the γⱼ are pairwise disjoint by construction (consecutive, non-overlapping ranges); B_other retains pairwise disjointness from B.

**B1 (Coverage).** Within subspace S, let N = |V_S(d)| and v₀ be the base. The pre-range [v₀, v) is covered by B_pre. The placed range [v, v + w) is partitioned by γ₁, ..., γₖ. The post-range [v + w, v₀ + N + w) is covered by B_post↑w. Together they cover all N + w subspace-S positions. B_other covers all text positions in subspaces S' ≠ S, unchanged.

**B3 (Consistency).** Pre-blocks: M'(d)(p) = M(d)(p) for p < v (unchanged). Placed blocks: M'(d)(v + offset) = aⱼ + (offset − offsetⱼ) for the appropriate j (by construction). Shifted post-blocks: for β = (v_β, a_β, n_β) ∈ B_post, M'(d)(v_β + w + i) = a_β + i = M(d)(v_β + i) for 0 ≤ i < n_β (same I-addresses at shifted V-positions). Other-subspace blocks: M'(d)(p) = M(d)(p) for all p in B_other (unchanged).

**C2 — ContiguityPreservation (LEMMA).** COPY preserves D-CTG. Within subspace S, if V_S(d) = {v₀ + j : 0 ≤ j < N}, then after COPY V_S(d) = {v₀ + j : 0 ≤ j < N + w}. For non-target subspaces S' ≠ S, V_{S'}(d) is unchanged (B_other is in the frame).

*Derivation.* The pre-range contributes positions v₀ through v − 1 (contiguous by assumption). The placed range contributes positions v through v + w − 1 (contiguous by construction of the γⱼ — each begins where the previous ends). The post-range contributes positions v + w through v₀ + N + w − 1 (contiguous because shifting preserves consecutiveness: for any position p in the pre-shift range, shift(shift(p, 1), w) = shift(p, 1 + w) = shift(shift(p, w), 1) by TS3 (ShiftComposition, ASN-0034), so consecutive positions remain consecutive after the shift; TS1 (ShiftOrderPreservation) then ensures the shifted range maintains its ordering). The three ranges are adjacent: v immediately follows v − 1, and v + w immediately follows v + w − 1. The union is contiguous with N + w elements. ∎

**C2a — MinimumPreservation (LEMMA).** COPY preserves D-MIN for every subspace.

*Derivation.* For the target subspace S: when N > 0, the pre-state has min(V_S(d)) = v₀ = [S, 1, ..., 1] by D-MIN. If v > v₀, then v₀ ∈ B_pre — unchanged by COPY — so the minimum is preserved. If v = v₀, the first placed block γ₁ starts at v = v₀ = [S, 1, ..., 1], which remains the minimum. When N = 0: by ValidInsertionPosition, v = [S, 1, ..., 1], so the first placed block starts at the canonical minimum. For non-target subspaces S' ≠ S: B_other is unmodified, so V_{S'}(d) is unchanged and D-MIN is preserved trivially. ∎


## Invariant Preservation

**C3 — InvariantPreservation (THEOREM).** The COPY composite preserves every foundational invariant.

*Derivation.*

P0 (ContentPermanence): C' = C by C0. ∎

P1 (EntityPermanence): E' = E. ∎

P2 (ProvenancePermanence): R' ⊇ R by construction. ∎

P3 (ArrangementMutabilityOnly): the composite uses only K.μ⁻, K.μ⁺, and K.ρ — extension, contraction, and provenance recording — which are the permitted modes of change. Satisfied by the elementary transition vocabulary. ∎

P4a (HistoricalFidelity): every new pair (a, d) ∈ R' \ R has a ∈ ran(M'(d)) in the post-state Σ', which serves as the required historical witness. ∎

P5 (DestructionConfinement): dom(C') ⊇ dom(C) with unchanged values (C0); E' = E ⊇ E; R' ⊇ R by construction. Only M admits contraction (the K.μ⁻ step), consistent with the confinement rule. ∎

S0 (ContentImmutability): immediate from C' = C. ∎

S2 (ArrangementFunctionality): M'(d) is a function because B' satisfies B2 — each V-position maps to exactly one I-address. ∎

S3 (ReferentialIntegrity): we must show ran(M'(d)) ⊆ dom(C'). Pre-blocks and shifted post-blocks reference the same I-addresses as B, which satisfy S3 by assumption. Placed blocks γⱼ reference I-addresses satisfying C1 (ResolutionIntegrity). Since C' = C, all references are valid. ∎

S8a (VPositionWellFormedness): new V-positions in the γⱼ blocks have the form v + offset, where v satisfies S8a and offset is an ordinal increment. By the OrdinalShift definition (ASN-0034), shift(v, n) changes only the last component of v (adding n to it); all other components are unchanged. Since v has all positive components (zeros(v) = 0), the shifted position also has all positive components. Shifted post-block V-positions satisfy S8a by the same component-preservation argument. ∎

S8-depth (FixedDepthVPositions): ordinal shift preserves depth: #shift(v, n) = #v (OrdinalShift definition, ASN-0034). All new and shifted V-positions share the depth of the existing ones. ∎

S8-fin (FiniteArrangement): |dom(M'(d))| = N + w, which is finite. ∎

P4 (ProvenanceBounds): Contains(Σ') ⊆ R'. For d: every a ∈ ran(M'(d)) is either in ran(M(d)) — hence (a, d) ∈ R by P4 in the pre-state, hence in R' — or in ran(M'(d)) \ ran(M(d)) — hence (a, d) ∈ R' by the provenance extension. For d' ≠ d: M'(d') = M(d'), so Contains entries are unchanged, and R' ⊇ R covers them. ∎

J0 (AllocationRequiresPlacement): no new content allocated (dom(C') \ dom(C) = ∅), so the condition is vacuously satisfied. ∎

J1 (ExtensionRecordsProvenance): every I-address in ran(M'(d)) \ ran(M(d)) has (a, d) ∈ R' by the provenance extension. ∎

J1' (ProvenanceRequiresExtension): every (a, d) ∈ R' \ R was added by the provenance extension for some a ∈ ran(M'(d)) \ ran(M(d)) — the construction adds no other provenance pairs. ∎

P6 (ExistentialCoherence): dom(C') = dom(C) and E' = E, so (A a ∈ dom(C') :: origin(a) ∈ E'_doc) is unchanged. ∎

P7 (ProvenanceGrounding): every new pair (a, d) ∈ R' \ R has a ∈ ran(M'(d)); by S3 on the post-state, a ∈ dom(C') = dom(C). ∎

P7a (ProvenanceCoverage): dom(C') = dom(C) and R' ⊇ R, so every a ∈ dom(C') retains its pre-existing provenance witness. ∎

P8 (EntityHierarchy): E' = E, so the hierarchy is unchanged. ∎

D-CTG: preserved by C2. ∎

D-MIN: preserved by C2a. ∎


## Displacement

The construction makes displacement explicit, but we state it as a named property for reference.

**C4 — Displacement (POST).** After COPY at position v in subspace S with total width w:

`(A p ∈ dom(M(d)) : subspace(p) = S ∧ p ≥ v : M'(d)(p + w) = M(d)(p))`

`(A p ∈ dom(M(d)) : subspace(p) = S ∧ p < v : M'(d)(p) = M(d)(p))`

`(A p ∈ dom(M(d)) : subspace(p) ≠ S : M'(d)(p) = M(d)(p))`

Within the target subspace S, every position at or after v shifts forward by w; every position before v is unchanged. Positions in all other subspaces are unchanged (B_other is in the frame). Content is displaced, never overwritten.

**C5 — NoOverwrite (LEMMA).** Every I-address in the pre-state arrangement is preserved in the post-state arrangement — no content is lost, only relocated:

`(A p ∈ dom(M(d)) :: (E q ∈ dom(M'(d)) : M'(d)(q) = M(d)(p)))`

*Derivation.* Three cases. If subspace(p) ≠ S, take q = p; M'(d)(p) = M(d)(p) by C4 (non-target frame). If subspace(p) = S and p < v, take q = p; M'(d)(p) = M(d)(p) by C4 (target-subspace, before v). If subspace(p) = S and p ≥ v, take q = p + w; M'(d)(p + w) = M(d)(p) by C4 (target-subspace, at/after v). In all cases the witness q exists in dom(M'(d)). ∎

C5 captures Nelson's prohibition on overwrite. There is no OVERWRITE, REPLACE, or PUT operation. To "replace" content, one must DELETE the old span and INSERT or COPY new content — two separate operations, preserving the old content in Istream for historical backtrack. Nelson: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].


## Structural Identity

We arrive at the property that distinguishes COPY from all content-creating operations. The I-addresses placed in the target are *the same addresses* as in the source. This is not a runtime property the system must enforce — it is a structural consequence of how COPY is defined.

**C6 — IdentityPreservation (POST).** Let resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩. For each placed block γⱼ = (v + offset_j, aⱼ, nⱼ):

`(A i : 0 ≤ i < nⱼ : M'(d)(v + offset_j + i) = aⱼ + i)`

and each aⱼ + i appears in the source document's arrangement:

`(A i : 0 ≤ i < nⱼ : aⱼ + i ∈ ran(M(d_sⱼ)))`

where d_sⱼ is the source document from which (aⱼ, nⱼ) was resolved.

The I-address *is* the identity. Nelson: "The virtual byte stream of a document may include bytes from any other document" [LM 4/10]. Two documents sharing I-addresses share content in the strongest possible sense — not merely equal bytes, but the same bytes at the same permanent addresses. Content identity is based on creation, not value. Two users who independently type identical text create different I-addresses — those bytes are equal in value but distinct in identity. When one user transcludes the other's text via COPY, both arrangements reference the same I-addresses. The system can distinguish "wrote the same words independently" from "quoted from the original."

Nelson puts it directly: "there is only one copy" — there is nothing to diverge from. The content exists once in the Istream; all placements are views of that single instance. His glass-pane metaphor captures this:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Painted content (from INSERT) is new I-addresses. Clear glass (from COPY) is a window through to someone else's I-addresses. The reader sees one coherent document. The system knows exactly which bytes are native and which are inclusions.

If someone were to make an actual independent copy — extracting bytes and re-storing them as new content — they would sever every connection:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The live reference participates in the network. The dead copy does not.


## Origin Invariance

Since COPY does not transform I-addresses — it extracts them from the source and places them unchanged into the target — the origin of each placed byte identifies the document that *originally created* it.

**C7 — OriginInvariance (LEMMA).** For every I-address a placed by COPY:

`origin(a) is unchanged`

That is, origin(a) identifies the document that first allocated a via K.α, regardless of how many COPY operations have arranged a into various documents' Vstreams.

*Derivation.* The resolution function extracts I-addresses from the source arrangement. The placement function writes them into the target arrangement. At no point is an I-address modified. The origin function (S7, ASN-0036) extracts the document-level prefix from the I-address, which is a structural property of the address itself. Since the address is unchanged, the origin is unchanged. ∎

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This is not an inspection capability layered atop COPY; it is a structural consequence of the I-address encoding the creating document's tumbler prefix. No separate provenance metadata is required — the address *is* the provenance.

**Definition — NativeContent.** A V-position v in document d maps to *native* content when origin(M(d)(v)) = d — the I-address was allocated under d's tumbler prefix.

**Definition — IncludedContent.** A V-position v in document d maps to *included* (non-native) content when origin(M(d)(v)) ≠ d — the I-address was allocated under some other document's prefix.

After COPY from a foreign source, the placed content is included in the sense of this definition. Nelson: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations" [LM 4/11].

**C7a — NativeStability (LEMMA).** COPY does not alter the native/included classification of any pre-existing V-position in d. For every p ∈ dom(M(d)):

```
subspace(p) = S ∧ p < v   ⟹  origin(M'(d)(p)) = origin(M(d)(p))
subspace(p) = S ∧ p ≥ v   ⟹  origin(M'(d)(p + w)) = origin(M(d)(p))
subspace(p) ≠ S            ⟹  origin(M'(d)(p)) = origin(M(d)(p))
```

*Derivation.* By C4: for target-subspace positions before v, M'(d)(p) = M(d)(p); for target-subspace positions at or after v, M'(d)(p + w) = M(d)(p); for non-target-subspace positions, M'(d)(p) = M(d)(p). In all three cases the I-address is preserved, so the origin function yields the same result. ∎


## Source Isolation

COPY reads the source arrangement but must not modify it. This is perhaps the most emphatically stated guarantee in Nelson's design.

**C8 — SourceIsolation (POST).** For every document d' ≠ d (including every source document d_sⱼ where d_sⱼ ≠ d):

`M'(d') = M(d')`

*Derivation.* The COPY composite modifies only M(d). By the frame conditions of K.μ⁺ and K.μ~ (ASN-0047): M'(d') = M(d') for all d' ≠ d. ∎

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals" [LM 2/45]. The source document's content, arrangement, version history, and ownership are unaffected. Even ownership rules would prohibit modification: "Only the owner has a right to withdraw a document or change it" [LM 2/29]. If Bob transcludes from Alice's document, Bob has no authority to modify Alice's arrangement, and COPY provides no mechanism for doing so.

The reverse also holds. The source owner may subsequently modify their own arrangement — removing content from their Vstream via DELETE — without affecting the target's arrangement. Both documents operate independently on their own Vstreams over shared Istream content. The shared I-addresses persist in C regardless of what either document does to its arrangement (S0, S6, ASN-0036). Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].

**C8a — BidirectionalIsolation (LEMMA).** For two documents d₁, d₂ sharing I-addresses through COPY:

(a) Modifications to M(d₁) do not affect M(d₂), and conversely.

(b) The shared I-addresses persist in dom(C) regardless of what either document does to its arrangement.

*Derivation.* (a) follows from the frame conditions of K.μ⁺, K.μ⁻, K.μ~ — each modifies M(d) for exactly one d. (b) follows from S0 (ContentImmutability) and S6 (PersistenceIndependence): a ∈ dom(C) implies a ∈ dom(C') for every subsequent state, unconditionally. ∎


## Transitive Identity

If document B acquired content from document A through COPY, and document C then copies that content from B, does C end up with A's original I-addresses?

Yes — necessarily. We are looking for what *could* go wrong and finding that nothing can. The key observation is that COPY at each hop performs the same structural operation: resolution extracts I-addresses from the source's arrangement; placement writes them into the target's arrangement. The I-addresses are values read from one data structure and written to another. No transformation occurs at any step.

**C9 — TransitiveIdentity (LEMMA).** Let Σ₀ →^{COPY₁} Σ₁ →^{COPY₂} Σ₂ be two successive COPY transitions where COPY₁ places content from A into B, and COPY₂ places that content from B into C. The I-addresses placed in C are the same I-addresses that A's arrangement contained in Σ₀.

*Derivation.* COPY₁ extracts I-addresses from M₀(A) and places them in M₁(B) without modification (C6). COPY₂ extracts I-addresses from M₁(B) — which include the addresses placed by COPY₁ — and places them in M₂(C) without modification (C6 again). At every step, the addresses are permanent values from dom(C), never transformed. ∎

The transitivity holds to arbitrary depth. Each hop is structurally identical. If D copies from C, E from D, and so on, every document in the chain holds the same I-addresses that A originally allocated. Gregory's code trace confirms: `specset2ispanset` reads the source POOM's stored I-coordinates; `insertpm` writes those same coordinates into the target POOM. The POOM is a coordinate-mapping structure, and COPY propagates coordinates by value. The I-address is *invariant under any number of copy hops*.

We need not worry about depth limits on this transitivity. The mechanism is purely structural: each hop reads an I-coordinate from one tree and writes it to another. There is no accumulation of state, no recursion, no stack that could overflow. The depth of the transclusion chain is invisible to the mechanism that performs each hop.

**Corollary (UniversalOriginAgreement).** For any I-address a appearing in N documents through any chain of COPY operations:

`(A d₁, d₂ : a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂)) : origin(a) computed from d₁ = origin(a) computed from d₂)`

The origin is a function of the I-address alone. All N documents agree on the home document of every shared byte. This is the mechanism by which attribution, royalty computation, and content discovery work: they query the I-address, which encodes its origin permanently. Nelson: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. "Determined automatically" means structurally — from the I-addresses.


## Multi-Source Composition

When a content reference sequence names multiple source documents, each source is resolved independently and the results are concatenated.

**C10 — MultiSourceContiguity (LEMMA).** Let R = ⟨r₁, ..., rₚ⟩ with resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ and total width w. The placed blocks γ₁, ..., γₖ occupy a single contiguous V-range [v, v + w) in the target.

*Derivation.* By step (iv) of the COPY definition, each γⱼ starts immediately where the previous one ends: γⱼ starts at v + (n₁ + ... + nⱼ₋₁) and has width nⱼ, so it ends at v + (n₁ + ... + nⱼ). The last block γₖ ends at v + w. The placed blocks partition [v, v + w) into consecutive sub-ranges with no gaps. ∎

**C10a — DistinctOriginPreservation (LEMMA).** Mapping blocks from different origin documents cannot merge, even when V-adjacent in the target. If γᵢ and γᵢ₊₁ have origin(aᵢ) ≠ origin(aᵢ₊₁), then by M16 (CrossOriginMergeImpossibility, ASN-0058), they cannot be I-adjacent and therefore cannot satisfy the merge condition (M7, ASN-0058).

*Derivation.* M16 requires origin(a₂) = origin(a₁) for the I-adjacency condition a₂ = a₁ + n₁ to hold. When origin(aᵢ) ≠ origin(aᵢ₊₁), I-adjacency is impossible, so the blocks remain distinct in any maximally merged decomposition. ∎

The number of blocks in the canonical decomposition of M'(d) is bounded below by the number of distinct-origin I-address runs in the placed content. Content from different creating documents remains structurally distinguishable through the block decomposition, even though the V-space presents a seamless sequence to the reader.

**Observation — Same-Origin Merging.** When two adjacent placed blocks share the same origin document *and* their I-address ranges are contiguous — which occurs when the source document contained a single contiguous run spanning material from the same origin — the canonical decomposition merges them into a single block (M7, ASN-0058). The merged result is indistinguishable from one that was never separated (M8, ASN-0058). Gregory confirms: `isanextensionnd` silently extends an existing POOM crum when it detects I-address contiguity with matching origin. Whether a block's width was reached in one step or through successive contiguous extensions is not recorded — the POOM is an opaque interval structure.


## Self-Transclusion

When a source document equals the target (d_s = d), the resolution reads M(d) while the mutation modifies M(d). The COPY definition resolves this by construction.

**C11 — SnapshotResolution (POST).** When d_s = d in a content reference, resolve(d, σ) is evaluated on M(d) in the pre-state Σ. The mutation phase may shift V-positions within M(d) that overlap with ⟦σ⟧, but the resolved I-address sequence is immutable once computed.

This is not an additional constraint — it follows from COPY being defined as a composite transition whose resolution is a function of the pre-state. Phase 1 reads; Phase 2 writes. The two phases are sequentially ordered.

Consider a concrete scenario: document d with content at V-positions [v₀, v₀ + N), self-transcluding the span [s, s + w) to position v where s ≤ v < s + w (the target falls within the source span). Resolution captures the I-addresses at [s, s + w) before any shift. The mutation then shifts V-positions at and after v by w, which includes V-positions in [v, s + w) — the tail of the source span. After completion:

| V-range | Content |
|---------|---------|
| [v₀, v) | original prefix (unchanged) |
| [v, v + w) | full copy of resolved I-addresses |
| [v + w, s + 2w) | original suffix (shifted from [v, s + w)) |
| [s + 2w, v₀ + N + w) | remainder (shifted from [s + w, v₀ + N)) |

The copy contains the complete source span as captured before the shift. The original source span is split at v with the copy interleaved.

After self-transclusion, the document may contain the same I-addresses at multiple V-positions. This is within-document sharing, consistent with S5 (UnrestrictedSharing, ASN-0036). The duplicate occurrences cannot merge: the merge condition (M7, ASN-0058) requires I-adjacency — a₂ = a₁ + n₁. When two blocks share the same I-start (a₂ = a₁), the condition requires a₁ = a₁ + n₁, which fails for n₁ ≥ 1 by TA-strict (ASN-0034). The distinct occurrences remain permanently distinguishable in the block decomposition (M14, ASN-0058).


## Worked Example

We ground the construction in specific arithmetic. Let document d have text-subspace V-position depth m = 2, with the canonical block decomposition:

`B = {([1,1], 1.0.1.0.1.0.1, 3), ([1,4], 1.0.1.0.1.0.7, 2)}`

Five text positions: V-range [1,1] through [1,5], N = 5. Let source document d_s have a block whose I-addresses we wish to place. Suppose resolve(R) = ⟨(1.0.2.0.1.0.4, 2)⟩ — two positions from d_s, with total width w = 2. We COPY at target position v = [1,3].

**Phase 1 — Resolution.** The I-address sequence ⟨(1.0.2.0.1.0.4, 2)⟩ is computed from d_s's arrangement in pre-state Σ and held fixed.

**Phase 2 — Mutation.**

*(i) Split.* v = [1,3] is interior to β₁ = ([1,1], 1.0.1.0.1.0.1, 3) since [1,1] < [1,3] < [1,1] + 3 = [1,4]. The split point is c = 2 (since [1,3] = [1,1] + 2). By M4:

`β_L = ([1,1], 1.0.1.0.1.0.1, 2)`
`β_R = ([1,3], 1.0.1.0.1.0.3, 1)`

After split: B = {β_L, β_R, ([1,4], 1.0.1.0.1.0.7, 2)}.

*(ii) Classify.*

`B_pre  = {([1,1], 1.0.1.0.1.0.1, 2)}      — V-reach [1,3] ≤ v = [1,3] ✓`
`B_post = {([1,3], 1.0.1.0.1.0.3, 1), ([1,4], 1.0.1.0.1.0.7, 2)}  — V-start ≥ [1,3] ✓`

*(iii) Shift.* w = 2. Each B_post block's V-start advances by 2:

`([1,3], 1.0.1.0.1.0.3, 1)↑2 = ([1,5], 1.0.1.0.1.0.3, 1)`
`([1,4], 1.0.1.0.1.0.7, 2)↑2 = ([1,6], 1.0.1.0.1.0.7, 2)`

I-starts unchanged.

*(iv) Place.* One placed block at v = [1,3]:

`γ₁ = ([1,3], 1.0.2.0.1.0.4, 2)`

*(v) Compose.*

`B' = {([1,1], 1.0.1.0.1.0.1, 2), ([1,3], 1.0.2.0.1.0.4, 2), ([1,5], 1.0.1.0.1.0.3, 1), ([1,6], 1.0.1.0.1.0.7, 2)}`

**Verification.**

C0: C' = C — no K.α step. ✓

C2 (D-CTG): dom_text(M'(d)) = {[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7]}. Contiguous range of N + w = 7 positions. ✓

C4 (Displacement): M'(d)([1,1]) = 1.0.1.0.1.0.1 = M(d)([1,1]) (p < v, unchanged). M'(d)([1,5]) = 1.0.1.0.1.0.3 = M(d)([1,3]) (p = [1,3] ≥ v, shifted by 2). ✓

C6 (IdentityPreservation): M'(d)([1,3]) = 1.0.2.0.1.0.4 and M'(d)([1,4]) = 1.0.2.0.1.0.5 — these are the same I-addresses as in d_s's arrangement. origin(1.0.2.0.1.0.4) = 1.0.2.0.1 ≠ d, confirming placed content is included (not native). ✓

We verify B' is maximally merged by checking all V-adjacent pairs. Blocks 1 and 2 — ([1,1], 1.0.1.0.1.0.1, 2) and ([1,3], 1.0.2.0.1.0.4, 2) — have origin(1.0.1.0.1.0.1) = 1.0.1.0.1 ≠ 1.0.2.0.1 = origin(1.0.2.0.1.0.4), so M16 applies. Blocks 2 and 3 — ([1,3], 1.0.2.0.1.0.4, 2) and ([1,5], 1.0.1.0.1.0.3, 1) — similarly have distinct origins, so M16 applies. Blocks 3 and 4 — ([1,5], 1.0.1.0.1.0.3, 1) and ([1,6], 1.0.1.0.1.0.7, 2) — share origin 1.0.1.0.1 and are V-adjacent ([1,5] + 1 = [1,6]), so M16 does not apply; we check I-adjacency directly. The I-reach of block 3 is 1.0.1.0.1.0.3 + 1 = 1.0.1.0.1.0.4, while block 4's I-start is 1.0.1.0.1.0.7. Since 1.0.1.0.1.0.4 ≠ 1.0.1.0.1.0.7, the merge condition (M7) is unsatisfied. B' is maximally merged.


## Provenance Completeness

The provenance relation R records which documents have ever contained which I-addresses. COPY extends R to capture the newly-arranged content.

**C12 — ProvenanceCompleteness (POST).** After COPY:

`(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

*Derivation.* By J1 (ExtensionRecordsProvenance, ASN-0047), every I-address that newly appears in a document's arrangement must be recorded in R'. The COPY definition adds exactly these pairs. ∎

Content discovery — finding all documents that share a given I-address — immediately reflects the COPY result. Given any I-address a, the system can query R to find every document that has ever arranged a into its Vstream. Gregory confirms: `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` at `do1.c:62` creates one index entry per I-address run, always using the *target* document's identifier. This call is unconditional in `docopy` — unlike the APPEND path, where a similar call is absent, COPY always records its provenance.

**C12a — ProvenanceGranularity (LEMMA).** The number of provenance entries created is bounded by the total width of the resolved content:

`|{(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}| ≤ (+ j : 1 ≤ j ≤ k : nⱼ)`

with equality when no resolved I-address already appeared in ran(M(d)) and no I-address appears in more than one resolved block.

**Observation — Provenance Records the Target, Not the Source.** The pair (a, d) records that document d contains I-address a. It does *not* record where d obtained a from. The chain of custody (A transcluded to B, B to C) is not stored in R; it is reconstructable from the I-addresses themselves, because all documents in the chain share the same addresses (C9) and origin(a) identifies the creating document (C7). The provenance relation tells you *who has it*; the I-address tells you *who made it*.

Provenance recording is monotonic: R' ⊇ R, and once (a, d) ∈ R, it remains in R forever (P2, ASN-0047). Even if d subsequently removes the content from its arrangement, the provenance record persists — recording the historical fact that d once contained a. This is consistent with the append-only philosophy: the system remembers what was, even when the current arrangement has moved on.


## Atomicity

Nelson never uses the terms "atomic" or "transaction." But the architecture mandates all-or-nothing through the canonical order mandate: "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system" [LM 1/34].

**C13 — SequentialCorrectness (POST).** The COPY composite either completes with all coupling constraints (J0, J1, J1') holding at the final state, or does not occur.

*Derivation.* By the ValidComposite definition (ASN-0047), a composite transition must satisfy coupling constraints between initial and final states. The internal elementary steps (K.μ~ for shift, K.μ⁺ for placement, K.ρ for provenance) are coupled by these constraints. If any step cannot satisfy its precondition at the intermediate state, the composite does not occur. The elementary decomposition above verifies each intermediate precondition.

The consequences of partial application would violate foundational invariants:

(a) *Contiguity violation.* D-CTG is a design constraint that complete operations preserve at their endpoints. A partial shift — V-addresses shifted but content not yet placed — creates a gap, violating D-CTG at the intermediate state. A partial placement — content placed at positions still occupied — creates an overlap.

(b) *Coupling violation.* If placement occurred without the corresponding provenance recording, J1 would be violated. If provenance were recorded without placement, J1' would be violated.

Nelson reinforces this at the system level: "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition" [LM 4/72].

**Observation — Concurrency.** Nelson's "at all times" and "canonical operating condition" suggest that no intermediate state should be visible to concurrent operations. The ValidComposite framework (ASN-0047) defines sequential correctness only — it provides no semantics for concurrent access or visibility. Formalizing the requirement that intermediate states are invisible to other operations requires a concurrency model not yet present in the foundation. ∎


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ContentReference | (d_s, σ) with d_s ∈ E_doc; σ level-uniform with #u = #ℓ = m; depth-m V-positions in span range ⊆ dom(M(d_s)) | introduced |
| ContentReferenceSequence | ordered list ⟨r₁, ..., rₚ⟩ with p ≥ 1 | introduced |
| resolve(d_s, σ) | maximally merged I-address runs from M(d_s)\|⟦σ⟧, V-ordered | introduced |
| NativeContent | V-position v where origin(M(d)(v)) = d | introduced |
| IncludedContent | V-position v where origin(M(d)(v)) ≠ d | introduced |
| ValidInsertionPosition | if V_S(d) ≠ ∅: v = min(V_S(d)) + j with 0 ≤ j ≤ N; if V_S(d) = ∅: v = [S, 1, ..., 1] of depth m ≥ 2 | introduced |
| COPY | composite transition: resolve in pre-state, then split-shift-place | introduced |
| C0 | C' = C — no content allocation (FRAME) | introduced |
| C0a | set of I-addresses allocated under any document is unchanged by COPY | introduced |
| C1 | every resolved I-address is in dom(C) | introduced |
| C1a | M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, S8-depth; in particular M(d_s)\|⟦σ⟧ | introduced |
| C2 | COPY preserves D-CTG: N + w positions after, N before | introduced |
| C2a | COPY preserves D-MIN: min(V_S(d)) = [S, 1, ..., 1] after COPY | introduced |
| C3 | COPY preserves all foundational invariants (P0–P5, P4a, P6–P8, S0, S2, S3, S8a, S8-depth, S8-fin, J0, J1, J1', D-CTG, D-MIN) | introduced |
| C4 | within target subspace S: positions ≥ v shift by w, positions < v unchanged; non-target subspaces unchanged | introduced |
| C5 | every pre-state I-address appears in the post-state arrangement; content displaced, never overwritten | introduced |
| C6 | placed I-addresses are the same addresses as in the source (POST) | introduced |
| C7 | origin(a) is unchanged — determined solely by the I-address | introduced |
| C7a | COPY does not alter native/included classification of pre-existing positions | introduced |
| C8 | source documents' arrangements are unmodified | introduced |
| C8a | bidirectional isolation: modifications to either document do not affect the other | introduced |
| C9 | I-address identity propagates transitively through arbitrary copy chains | introduced |
| C10 | multiple source references produce one contiguous V-range in target | introduced |
| C10a | blocks from different origin documents cannot merge | introduced |
| C11 | self-transclusion resolves source in pre-state before mutation (POST) | introduced |
| C12 | provenance recorded for every newly-arranged I-address | introduced |
| C12a | provenance entries bounded by total width of resolved content | introduced |
| C13 | COPY is sequentially correct: completes fully or not at all (ValidComposite, POST) | introduced |


## Open Questions

- Must the resolution ordering across a multi-source content reference sequence preserve the sequence order, or may an implementation reorder source references provided the placed content lands at the correct V-positions?
- What invariants distinguish a location-fixed transclusion (showing the source's current state) from a time-fixed transclusion (pinned to a specific version)?
- Must the provenance relation R support bounded-time enumeration of all documents sharing a given I-address, or is eventual discovery sufficient?
- What authorization invariants must hold when content is copied from a document not owned by the copier?
- Must every version of a document independently satisfy D-CTG, or may historical versions contain gaps after content has been deleted from the current version?
- What serialization guarantees must the system provide when multiple COPY operations target the same document concurrently?
- When self-transclusion creates duplicate I-address occurrences within a document, must the system preserve the distinction between original and copied occurrence through subsequent editing operations?
