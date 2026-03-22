# ASN-0067 Formal Statements

*Source: ASN-0067-copy-operation.md (revised 2026-03-21) — Extracted: 2026-03-21*

## Definition — ContentReference

A *content reference* is a pair (d_s, σ) where d_s ∈ E_doc and σ = (u, ℓ) is a level-uniform V-span — that is, T12 (ASN-0034) holds and `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036). The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

## Definition — ContentReferenceSequence

A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.

## Definition — Resolution

Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧. The decomposition yields ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

For a content reference sequence R = ⟨r₁, ..., rₚ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

The total width is:

`w(R) = (+ j : 1 ≤ j ≤ k : nⱼ)`

where ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R).

## Definition — NativeContent

A V-position v in document d maps to *native* content when origin(M(d)(v)) = d — the I-address was allocated under d's tumbler prefix.

## Definition — IncludedContent

A V-position v in document d maps to *included* (non-native) content when origin(M(d)(v)) ≠ d — the I-address was allocated under some other document's prefix.

## Definition — ValidInsertionPosition

A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Then v = min(V_S(d)) + j for some j with 0 ≤ j ≤ N, and #v equals the existing subspace depth (S8-depth).

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. This is the canonical minimum position required by D-MIN (ASN-0036).

In both cases, S = v₁ is the subspace identifier. There are N + 1 valid insertion positions: N positions targeting existing content (which will be displaced), plus one append position past the end.

## Definition — COPY

A COPY into document d at position v from content reference sequence R is a composite transition Σ → Σ'.

*Preconditions.*

(P.1) d ∈ E_doc.

(P.2) M(d) satisfies D-CTG (ASN-0036).

(P.3) v is a valid insertion position in d.

(P.4) Each rⱼ = (d_sⱼ, σⱼ) in R is a well-formed content reference.

(P.5) resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is evaluated in state Σ.

(P.6) w = w(R) ≥ 1.

(P.7) v₁ ≥ 1 (text subspace).

*Phase 1 — Resolution.* The resolution is computed from the pre-state Σ. No state modification occurs in this phase.

*Phase 2 — Mutation.* Let B be the maximally merged block decomposition of M(d) in state Σ. The new arrangement M'(d) is defined by a block decomposition B' constructed in five steps.

(i) *Split.* If v is interior to some block β = (v_β, a_β, n_β) ∈ B — meaning v_β < v < v_β + n_β — let c be the natural number with v = v_β + c. Split β at c (M4) into β_L = (v_β, a_β, c) and β_R = (v, a_β + c, n_β − c). If v is not interior to any block, no split occurs.

(ii) *Classify.* Let S = v₁. Partition B (after step i) by subspace:
```
B_S     = {β ∈ B : (v_β)₁ = S}
B_other = {β ∈ B : (v_β)₁ ≠ S}
```
Then partition B_S into:
```
B_pre  = {β ∈ B_S : v_β + n_β ≤ v}
B_post = {β ∈ B_S : v_β ≥ v}
```

(iii) *Shift.* For each β = (v_β, a_β, n_β) ∈ B_post, define:

`β↑w = (v_β + w, a_β, n_β)`

(iv) *Place.* From resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩:

`γⱼ = (v + (+ i : 1 ≤ i < j : nᵢ), aⱼ, nⱼ)   for j = 1, ..., k`

with the convention that the empty sum is 0, so γ₁ = (v, a₁, n₁).

(v) *Compose.*

`B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post} ∪ B_other`

*Effects.*
```
C' = C
E' = E
M'(d) is the arrangement defined by B'
(A p : p ∈ dom(M(d)) ∧ subspace(p) ≠ S : M'(d)(p) = M(d)(p))
(A d' : d' ≠ d : M'(d') = M(d'))
R' = R ∪ {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}
```

---

## P.7 — TextSubspacePrecondition (PRE)

`v₁ ≥ 1`

COPY targets the text subspace only.

---

## C0 — ArrangementOnly (FRAME)

`C' = C`

No content is created, modified, or removed. The content store is entirely in the frame.

---

## C0a — AllocationInvariance (LEMMA)

For any document d', the set of I-addresses allocated under d' is unchanged by COPY:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

---

## C1 — ResolutionIntegrity (LEMMA)

Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

---

## C1a — RestrictionDecomposition (COROLLARY)

M11 and M12 (ASN-0058) hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.*

(i) S2 (functionality): f is a restriction of M(d_s), which is functional by S2; a restriction of a function is a function.

(ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), which is finite by S8-fin; a subset of a finite set is finite.

(iii) S8-depth (fixed depth): every position in dom(f) belongs to dom(M(d_s)), so all share the common depth m of subspace u₁ in d_s.

---

## C2 — ContiguityPreservation (LEMMA)

COPY preserves D-CTG. Within subspace S, if V_S(d) = {v₀ + j : 0 ≤ j < N}, then after COPY V_S(d) = {v₀ + j : 0 ≤ j < N + w}. For non-target subspaces S' ≠ S, V_{S'}(d) is unchanged (B_other is in the frame).

---

## C2a — MinimumPreservation (LEMMA)

COPY preserves D-MIN for every subspace.

- For the target subspace S: when N > 0, if v > v₀ then the minimum v₀ = [S, 1, ..., 1] is in B_pre (unchanged); if v = v₀ then the first placed block γ₁ starts at v = v₀ = [S, 1, ..., 1]. When N = 0: by ValidInsertionPosition, v = [S, 1, ..., 1], so the first placed block starts at the canonical minimum.
- For non-target subspaces S' ≠ S: B_other is unmodified, so V_{S'}(d) is unchanged and D-MIN is preserved trivially.

---

## C3 — InvariantPreservation (THEOREM)

The COPY composite preserves every foundational invariant:

P0 (ContentPermanence): C' = C by C0.

P1 (EntityPermanence): E' = E.

P2 (ProvenancePermanence): R' ⊇ R by construction.

P3 (ArrangementMutabilityOnly): the composite uses only K.μ⁻, K.μ⁺, and K.ρ.

P4a (HistoricalFidelity): every new pair (a, d) ∈ R' \ R has a ∈ ran(M'(d)) in the post-state Σ'.

P5 (DestructionConfinement): dom(C') ⊇ dom(C) with unchanged values; E' = E ⊇ E; R' ⊇ R. Only M admits contraction (K.μ⁻ step).

S0 (ContentImmutability): immediate from C' = C.

S2 (ArrangementFunctionality): M'(d) is a function because B' satisfies B2.

S3 (ReferentialIntegrity): ran(M'(d)) ⊆ dom(C'). Pre-blocks and shifted post-blocks reference same I-addresses as B (satisfy S3 by assumption); placed blocks γⱼ reference I-addresses satisfying C1; C' = C.

S8a (VPositionWellFormedness): new V-positions in γⱼ blocks have the form v + offset, where v satisfies S8a and offset is an ordinal increment; shift preserves positivity of all components; shifted post-block V-positions satisfy S8a by same argument.

S8-depth (FixedDepthVPositions): `#shift(v, n) = #v`; all new and shifted V-positions share the depth of the existing ones.

S8-fin (FiniteArrangement): |dom(M'(d))| = N + w, which is finite.

P4 (ProvenanceBounds): Contains(Σ') ⊆ R'. For d: every a ∈ ran(M'(d)) is either in ran(M(d)) — hence (a, d) ∈ R ⊆ R' — or in ran(M'(d)) \ ran(M(d)) — hence (a, d) ∈ R' by provenance extension. For d' ≠ d: M'(d') = M(d'), so Contains entries are unchanged, and R' ⊇ R covers them.

J0 (AllocationRequiresPlacement): dom(C') \ dom(C) = ∅, so vacuously satisfied.

J1 (ExtensionRecordsProvenance): every I-address in ran(M'(d)) \ ran(M(d)) has (a, d) ∈ R' by provenance extension.

J1' (ProvenanceRequiresExtension): every (a, d) ∈ R' \ R was added by the provenance extension for some a ∈ ran(M'(d)) \ ran(M(d)).

P6 (ExistentialCoherence): dom(C') = dom(C) and E' = E, so `(A a ∈ dom(C') :: origin(a) ∈ E'_doc)` is unchanged.

P7 (ProvenanceGrounding): every new pair (a, d) ∈ R' \ R has a ∈ ran(M'(d)); by S3 on the post-state, a ∈ dom(C') = dom(C).

P7a (ProvenanceCoverage): dom(C') = dom(C) and R' ⊇ R, so every a ∈ dom(C') retains its pre-existing provenance witness.

P8 (EntityHierarchy): E' = E, so the hierarchy is unchanged.

D-CTG: preserved by C2.

D-MIN: preserved by C2a.

---

## C4 — Displacement (POST)

After COPY at position v in subspace S with total width w:

`(A p ∈ dom(M(d)) : subspace(p) = S ∧ p ≥ v : M'(d)(p + w) = M(d)(p))`

`(A p ∈ dom(M(d)) : subspace(p) = S ∧ p < v : M'(d)(p) = M(d)(p))`

`(A p ∈ dom(M(d)) : subspace(p) ≠ S : M'(d)(p) = M(d)(p))`

---

## C5 — NoOverwrite (LEMMA)

Every I-address in the pre-state arrangement is preserved in the post-state arrangement:

`(A p ∈ dom(M(d)) :: (E q ∈ dom(M'(d)) : M'(d)(q) = M(d)(p)))`

Three cases:
- subspace(p) ≠ S: take q = p; M'(d)(p) = M(d)(p) by C4 (non-target frame).
- subspace(p) = S and p < v: take q = p; M'(d)(p) = M(d)(p) by C4 (before v).
- subspace(p) = S and p ≥ v: take q = p + w; M'(d)(p + w) = M(d)(p) by C4 (at/after v).

---

## C6 — IdentityPreservation (POST)

Let resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩. For each placed block γⱼ = (v + offset_j, aⱼ, nⱼ):

`(A i : 0 ≤ i < nⱼ : M'(d)(v + offset_j + i) = aⱼ + i)`

and each aⱼ + i appears in the source document's arrangement:

`(A i : 0 ≤ i < nⱼ : aⱼ + i ∈ ran(M(d_sⱼ)))`

where d_sⱼ is the source document from which (aⱼ, nⱼ) was resolved.

---

## C7 — OriginInvariance (LEMMA)

For every I-address a placed by COPY:

`origin(a) is unchanged`

origin(a) identifies the document that first allocated a via K.α, regardless of how many COPY operations have arranged a into various documents' Vstreams.

---

## C7a — NativeStability (LEMMA)

COPY does not alter the native/included classification of any pre-existing V-position in d. For every p ∈ dom(M(d)):

```
subspace(p) = S ∧ p < v   ⟹  origin(M'(d)(p)) = origin(M(d)(p))
subspace(p) = S ∧ p ≥ v   ⟹  origin(M'(d)(p + w)) = origin(M(d)(p))
subspace(p) ≠ S            ⟹  origin(M'(d)(p)) = origin(M(d)(p))
```

---

## C8 — SourceIsolation (POST)

For every document d' ≠ d (including every source document d_sⱼ where d_sⱼ ≠ d):

`M'(d') = M(d')`

---

## C8a — BidirectionalIsolation (LEMMA)

For two documents d₁, d₂ sharing I-addresses through COPY:

(a) Modifications to M(d₁) do not affect M(d₂), and conversely.

(b) The shared I-addresses persist in dom(C) regardless of what either document does to its arrangement.

(a) follows from the frame conditions of K.μ⁺, K.μ⁻, K.μ~ — each modifies M(d) for exactly one d.

(b) follows from S0 (ContentImmutability) and S6 (PersistenceIndependence): a ∈ dom(C) implies a ∈ dom(C') for every subsequent state, unconditionally.

---

## C9 — TransitiveIdentity (LEMMA)

Let Σ₀ →^{COPY₁} Σ₁ →^{COPY₂} Σ₂ be two successive COPY transitions where COPY₁ places content from A into B, and COPY₂ places that content from B into C. The I-addresses placed in C are the same I-addresses that A's arrangement contained in Σ₀.

**Corollary (UniversalOriginAgreement).** For any I-address a appearing in N documents through any chain of COPY operations:

`(A d₁, d₂ : a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂)) : origin(a) computed from d₁ = origin(a) computed from d₂)`

---

## C10 — MultiSourceContiguity (LEMMA)

Let R = ⟨r₁, ..., rₚ⟩ with resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ and total width w. The placed blocks γ₁, ..., γₖ occupy a single contiguous V-range [v, v + w) in the target.

Each γⱼ starts immediately where the previous one ends: γⱼ starts at v + (n₁ + ... + nⱼ₋₁) and has width nⱼ, so it ends at v + (n₁ + ... + nⱼ). The last block γₖ ends at v + w. The placed blocks partition [v, v + w) into consecutive sub-ranges with no gaps.

---

## C10a — DistinctOriginPreservation (LEMMA)

Mapping blocks from different origin documents cannot merge, even when V-adjacent in the target. If γᵢ and γᵢ₊₁ have origin(aᵢ) ≠ origin(aᵢ₊₁), then by M16 (CrossOriginMergeImpossibility, ASN-0058), they cannot be I-adjacent and therefore cannot satisfy the merge condition (M7, ASN-0058).

M16 requires origin(a₂) = origin(a₁) for the I-adjacency condition a₂ = a₁ + n₁ to hold. When origin(aᵢ) ≠ origin(aᵢ₊₁), I-adjacency is impossible, so the blocks remain distinct in any maximally merged decomposition.

---

## C11 — SnapshotResolution (POST)

When d_s = d in a content reference, resolve(d, σ) is evaluated on M(d) in the pre-state Σ. The mutation phase may shift V-positions within M(d) that overlap with ⟦σ⟧, but the resolved I-address sequence is immutable once computed.

---

## C12 — ProvenanceCompleteness (POST)

After COPY:

`(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

---

## C12a — ProvenanceGranularity (LEMMA)

The number of provenance entries created is bounded by the total width of the resolved content:

`|{(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}| ≤ (+ j : 1 ≤ j ≤ k : nⱼ)`

with equality when no resolved I-address already appeared in ran(M(d)) and no I-address appears in more than one resolved block.

---

## C13 — SequentialCorrectness (POST)

The COPY composite either completes with all coupling constraints (J0, J1, J1') holding at the final state, or does not occur.

By the ValidComposite definition (ASN-0047), a composite transition must satisfy coupling constraints between initial and final states. If any step cannot satisfy its precondition at the intermediate state, the composite does not occur.

Consequences of partial application:

(a) *Contiguity violation.* D-CTG is a design constraint that complete operations preserve at their endpoints. A partial shift creates a gap, violating D-CTG at the intermediate state. A partial placement creates an overlap.

(b) *Coupling violation.* If placement occurred without the corresponding provenance recording, J1 would be violated. If provenance were recorded without placement, J1' would be violated.
