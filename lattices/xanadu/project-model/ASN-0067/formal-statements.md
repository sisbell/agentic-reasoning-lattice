# ASN-0067 Formal Statements

*Source: ASN-0067-copy-operation.md (revised 2026-03-22) — Extracted: 2026-03-23*

## Definition — ContentReference

A *content reference* `(d_s, σ)` pairs a source document `d_s ∈ E_doc` with a level-uniform V-span `σ = (u, ℓ)` satisfying `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d_s`; the reference is well-formed when `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`.

## Definition — ContentReferenceSequence

A *content reference sequence* is an ordered list `R = ⟨r₁, ..., rₚ⟩` with `p ≥ 1`; different references may name different source documents.

## Definition — Resolution

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` where the restriction `f = M(d_s)|⟦σ⟧` admits a unique maximally merged block decomposition `⟨β₁, ..., βₖ⟩` ordered by V-start, and `βⱼ = (vⱼ, aⱼ, nⱼ)` (V-coordinates discarded).

For a content reference sequence:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

Total width: `w(R) = (+ j : 1 ≤ j ≤ k : nⱼ)` where `⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R)`.

## Definition — NativeContent

A V-position `v` in document `d` maps to *native* content when `origin(M(d)(v)) = d`.

## Definition — IncludedContent

A V-position `v` in document `d` maps to *included* (non-native) content when `origin(M(d)(v)) ≠ d`.

## Definition — ValidInsertionPosition

A V-position `v` is a *valid insertion position* in subspace `S` of document `d` when:
- for non-empty `V_S(d)` with `|V_S(d)| = N`: either `v = min(V_S(d))` or `v = shift(min(V_S(d)), j)` for some `1 ≤ j ≤ N`, with `#v = m`
- for empty `V_S(d)`: `v = [S, 1, ..., 1]` of depth `m ≥ 2`

In both cases, `S = v₁`.

## Definition — CopyTransition

**Preconditions.**

- (P.1) `d ∈ E_doc`
- (P.2) `M(d)` satisfies D-CTG
- (P.3) `v` is a valid insertion position in `d`
- (P.4) Each `rⱼ = (d_sⱼ, σⱼ)` in `R` is a well-formed content reference
- (P.4a) For each `rⱼ = (d_sⱼ, σⱼ)` with `σⱼ = (uⱼ, ℓⱼ)`: `subspace(uⱼ) = s_C`
- (P.5) `resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` is evaluated in state `Σ`
- (P.6) `w = w(R) ≥ 1`
- (P.7) `subspace(v) = s_C`

**Phase 2 — Mutation.** Let `B` be the maximally merged block decomposition of `M(d)` in state `Σ`. The new arrangement `M'(d)` is defined by block decomposition `B'`:

(i) *Split.* If `v` is interior to some `β = (v_β, a_β, n_β) ∈ B` — meaning `v_β < v < v_β + n_β` — let `c` be the natural number with `v = v_β + c`. Split `β` at `c` into `β_L = (v_β, a_β, c)` and `β_R = (v, a_β + c, n_β − c)`.

(ii) *Classify.* Let `S = v₁`. Partition:

```
B_S     = {β ∈ B : (v_β)₁ = S}
B_other = {β ∈ B : (v_β)₁ ≠ S}
B_pre   = {β ∈ B_S : v_β + n_β ≤ v}
B_post  = {β ∈ B_S : v_β ≥ v}
```

(iii) *Shift.* For each `β = (v_β, a_β, n_β) ∈ B_post`:

`β↑w = (v_β + w, a_β, n_β)`

(iv) *Place.* From `resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`:

`γⱼ = (v + (+ i : 1 ≤ i < j : nᵢ), aⱼ, nⱼ)   for j = 1, ..., k`

(with the convention that the empty sum is 0, so `γ₁ = (v, a₁, n₁)`).

(v) *Compose.*

`B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post} ∪ B_other`

**Effects.**

```
C' = C
L' = L
E' = E
M'(d) is the arrangement defined by B'
(A p : p ∈ dom(M(d)) ∧ subspace(p) ≠ S : M'(d)(p) = M(d)(p))
(A d' : d' ≠ d : M'(d') = M(d'))
R' = R ∪ {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}
```

---

## P.4a — SourceSubspaceContent (PRE, requires)

For each `rⱼ = (d_sⱼ, σⱼ)` in `R` with `σⱼ = (uⱼ, ℓⱼ)`:

`subspace(uⱼ) = s_C`

## P.7 — TargetSubspaceContent (PRE, requires)

`subspace(v) = s_C`

---

## C0 — ArrangementOnly (FRAME, ensures)

`C' = C`

## C0a — AllocationInvariance (LEMMA, lemma)

For any document `d'`, the set of I-addresses allocated under `d'` is unchanged by COPY:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

## C1 — ResolutionIntegrity (INV, predicate)

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

## C1a — BlockDecompositionExistence (LEMMA, lemma)

M11 and M12 hold for any finite partial function `f : T ⇀ T` satisfying S2, S8-fin, and S8-depth; in particular `M(d_s)|⟦σ⟧`.

## C2 — ContiguityPreservation (LEMMA, lemma)

COPY preserves D-CTG. Within subspace `S`, if `V_S(d) = {v₀ + j : 0 ≤ j < N}`, then after COPY `V_S(d) = {v₀ + j : 0 ≤ j < N + w}`. For non-target subspaces `S' ≠ S`, `V_{S'}(d)` is unchanged (B_other is in the frame).

## C2a — MinimumPreservation (LEMMA, lemma)

COPY preserves D-MIN for every subspace:
- For target subspace `S` with `N > 0`: `min(V_S(d)) = [S, 1, ..., 1]` is preserved after COPY.
- For target subspace `S` with `N = 0`: the first placed block `γ₁` starts at `v = [S, 1, ..., 1]`.
- For non-target subspaces `S' ≠ S`: `V_{S'}(d)` is unchanged, so D-MIN is preserved.

## C3 — InvariantPreservation (THEOREM, lemma)

The COPY composite preserves every foundational invariant: P0, P1, P2, P3, P4a, P5, P4, P6, P7, P7a, P8, S0, S1, S2, S3, S8, S8a, S8-depth, S8-fin, J0, J1, J1', D-CTG, D-MIN, L0, L1, L1a, L3, L12, L14, S3★, S3★-aux, P3★, P4★, P5★, CL-OWN, J1★, J1'★.

## C4 — Displacement (POST, ensures)

```
(A p ∈ dom(M(d)) : subspace(p) = S ∧ p ≥ v : M'(d)(p + w) = M(d)(p))
(A p ∈ dom(M(d)) : subspace(p) = S ∧ p < v : M'(d)(p) = M(d)(p))
(A p ∈ dom(M(d)) : subspace(p) ≠ S : M'(d)(p) = M(d)(p))
```

## C5 — NoOverwrite (LEMMA, lemma)

`(A p ∈ dom(M(d)) :: (E q ∈ dom(M'(d)) : M'(d)(q) = M(d)(p)))`

## C6 — IdentityPreservation (POST, ensures)

Let `resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` with `offset_j = (+ i : 1 ≤ i < j : nᵢ)`. For each placed block `γⱼ = (v + offset_j, aⱼ, nⱼ)`:

```
(A i : 0 ≤ i < nⱼ : M'(d)(v + offset_j + i) = aⱼ + i)
(A i : 0 ≤ i < nⱼ : aⱼ + i ∈ ran(M(d_sⱼ)))
```

where `d_sⱼ` is the source document from which `(aⱼ, nⱼ)` was resolved.

## C7 — OriginInvariance (LEMMA, lemma)

For every I-address `a` placed by COPY:

`origin(a) is unchanged`

That is, `origin(a)` identifies the document that first allocated `a` via K.α, regardless of how many COPY operations have arranged `a` into various documents' Vstreams.

## C7a — NativeStability (LEMMA, lemma)

COPY does not alter the native/included classification of any pre-existing V-position in `d`. For every `p ∈ dom(M(d))`:

```
subspace(p) = S ∧ p < v   ⟹  origin(M'(d)(p)) = origin(M(d)(p))
subspace(p) = S ∧ p ≥ v   ⟹  origin(M'(d)(p + w)) = origin(M(d)(p))
subspace(p) ≠ S            ⟹  origin(M'(d)(p)) = origin(M(d)(p))
```

## C8 — SourceIsolation (POST, ensures)

For every document `d' ≠ d` (including every source document `d_sⱼ` where `d_sⱼ ≠ d`):

`M'(d') = M(d')`

## C8a — BidirectionalIsolation (LEMMA, lemma)

For two documents `d₁`, `d₂` sharing I-addresses through COPY:

(a) `(A d' : d' ≠ d : M'(d') = M(d'))` — frame conditions of K.μ⁻ and K.μ⁺ applied to each of `d₁`, `d₂`.

(b) `a ∈ dom(C) ⟹ a ∈ dom(C')` for every subsequent state — by S0 (ContentImmutability) and S6 (PersistenceIndependence); the shared I-addresses persist in `dom(C)` regardless of what either document does to its arrangement.

## C9 — TransitiveIdentity (LEMMA, lemma)

Let `Σ₀ →^{COPY₁} Σ₁ →^{COPY₂} Σ₂` be two successive COPY transitions where COPY₁ places content from `A` into `B`, and COPY₂ places that content from `B` into `C`. The I-addresses placed in `C` are the same I-addresses that `A`'s arrangement contained in `Σ₀`.

**Corollary — UniversalOriginAgreement.** For any I-address `a` appearing in `N` documents through any chain of COPY operations:

`(A d₁, d₂ : a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂)) : origin(a) computed from d₁ = origin(a) computed from d₂)`

## C10 — MultiSourceContiguity (LEMMA, lemma)

Let `R = ⟨r₁, ..., rₚ⟩` with `resolve(R) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` and total width `w`. The placed blocks `γ₁, ..., γₖ` occupy a single contiguous V-range `[v, v + w)` in the target.

## C10a — DistinctOriginPreservation (LEMMA, lemma)

Mapping blocks from different origin documents cannot merge, even when V-adjacent in the target. If `γᵢ` and `γᵢ₊₁` have `origin(aᵢ) ≠ origin(aᵢ₊₁)`, then by M16 (CrossOriginMergeImpossibility), they cannot be I-adjacent and therefore cannot satisfy the merge condition (M7).

## C11 — SnapshotResolution (POST, ensures)

When `d_s = d` in a content reference, `resolve(d, σ)` is evaluated on `M(d)` in the pre-state `Σ`. The mutation phase may shift V-positions within `M(d)` that overlap with `⟦σ⟧`, but the resolved I-address sequence is immutable once computed.

## C12 — ProvenanceCompleteness (POST, ensures)

`(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

## C12a — ProvenanceGranularity (LEMMA, lemma)

`|{(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}| ≤ (+ j : 1 ≤ j ≤ k : nⱼ)`

with equality when no resolved I-address already appeared in `ran(M(d))` and no I-address appears in more than one resolved block.

## C13 — SequentialCorrectness (POST, ensures)

The COPY composite either completes with all coupling constraints (J0, J1, J1') holding at the final state, or does not occur. Formally, by ValidComposite (ASN-0047): a composite transition must satisfy coupling constraints between initial and final states; if any elementary step cannot satisfy its precondition at the intermediate state, the composite does not occur.
