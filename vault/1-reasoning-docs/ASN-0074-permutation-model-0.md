# ASN-0074: Permutation Model 0

*2026-03-22*

The permutation model (ASN-0058) defines block decompositions for document arrangements and proves existence and uniqueness of maximally merged canonical forms. This ASN extends the model with content references — a mechanism for identifying a span of positions within a document's arrangement — and resolution, which extracts the I-address runs from the block decomposition restricted to that span. The extension establishes that the canonical decomposition (M11, M12) applies to any restriction of an arrangement satisfying the structural preconditions, and that every resolved I-address satisfies referential integrity. We work with the content store C : T ⇀ Val and per-document arrangement M(d) : T ⇀ T from ASN-0036. Let D be the set of documents for which an arrangement is defined. The extension references properties from the foundation: S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S8-fin (FiniteArrangement), S8-depth (FixedDepthVPositions) from ASN-0036; T12 (SpanWellDefinedness) from ASN-0034; S6 (LevelConstraint) and ⟦σ⟧ (SpanDenotation) from ASN-0053.


## Content References

**Definition — ContentReference.** A *content reference* is a pair (d_s, σ) where d_s ∈ D and σ = (u, ℓ) is a level-uniform V-span satisfying: (i) V_{u₁}(d_s) ≠ ∅ — the subspace contains at least one V-position; (ii) T12 (ASN-0034) holds; and (iii) `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036). Precondition (i) is necessary: S8-depth is vacuously true for an empty subspace and does not determine a common depth, so m is well-defined only when at least one V-position exists. The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies. The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

Since `#u = #ℓ = m`, dom(M(d_s)) contains only depth-m V-positions in subspace u₁ (S8-depth), and reach(σ) has depth m (S6), the depth-m restriction is structurally guaranteed.

**C0 — OrdinalDisplacementNecessity (LEMMA).** For a well-formed content reference (d_s, σ) with σ = (u, ℓ), common depth m, and action point k of ℓ: k = m. Equivalently, ℓ = δ(ℓₘ, m) — an ordinal displacement.

*Derivation.* Suppose for contradiction that k < m. Consider the family of depth-m tumblers wⱼ = [u₁, ..., uₖ, uₖ₊₁, ..., u_{m−1}, j] for j > uₘ. Each wⱼ satisfies u < wⱼ: the two agree on components 1 through m − 1 and j > uₘ at component m, so wⱼ > u by T1(i) (ASN-0034). Each wⱼ satisfies wⱼ < reach(σ): at component k, uₖ < uₖ + ℓₖ (since ℓₖ ≥ 1, k being the action point), so wⱼ < reach(σ) by T1(i). Thus wⱼ ∈ ⟦σ⟧ for every j > uₘ. By T0(a) (ASN-0034), j ranges over unboundedly many values, yielding infinitely many depth-m tumblers in ⟦σ⟧. Well-formedness requires each to be in dom(M(d_s)), contradicting S8-fin (ASN-0036). Therefore k = m, and ℓ = [0, ..., 0, ℓₘ] = δ(ℓₘ, m). ∎

**Definition — ContentReferenceSequence.** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.


## Resolution

To resolve a content reference, we extract the I-address runs corresponding to the named V-span. The source document's mapping may not be ordinal-contiguous across the full span — prior editing may have interleaved content from multiple allocations, fragmenting the V→I mapping into several contiguous I-address runs.

**Definition — Resolution.** Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧.

**C1a — RestrictionDecomposition (COROLLARY).** M11 and M12 (ASN-0058) hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.* (i) S2 (functionality): f is a restriction of M(d_s), which is functional by S2; a restriction of a function is a function. (ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), which is finite by S8-fin; a subset of a finite set is finite. (iii) S8-depth (fixed depth): every position in dom(f) belongs to dom(M(d_s)), so all share the common depth m of subspace u₁ in d_s.

*Extension of M11/M12.* M11 (CanonicalExistence) constructs a maximally merged decomposition by iterating: while any two blocks satisfy the merge condition (M7), merge them. The initial singleton-block decomposition — one block (v, f(v), 1) per v ∈ dom(f) — satisfies B3 directly from S2 (f is a function, so each singleton block's I-address is uniquely determined). Termination follows from S8-fin since the block count is at most |dom(f)|. Each merge step preserves B3: if β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) each satisfy B3 and M7 holds (v₂ = v₁ + n₁, a₂ = a₁ + n₁), then β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂) satisfies B3 by case split — for 0 ≤ i < n₁, f(v₁ + i) = a₁ + i by B3 for β₁; for n₁ ≤ i < n₁ + n₂, f(v₁ + i) = f(v₂ + (i − n₁)) = a₂ + (i − n₁) = (a₁ + n₁) + (i − n₁) = a₁ + i, using B3 for β₂ and M-aux (ASN-0058). M12 (CanonicalUniqueness) identifies the maximally merged decomposition with the set of maximal runs of f, using only pointwise evaluation of f — independent of whether f is a full arrangement or a restriction. Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth; they apply to f verbatim. ∎

The decomposition yields ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

The ordering of runs within each resolution preserves the source document's V-ordering: if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence. This follows from the definition of resolve, which specifies the blocks ordered by V-start. The ordering is well-defined because V-extents are disjoint (B2, ASN-0058), so the V-starts induce a total order on the blocks.

For a content reference sequence R = ⟨r₁, ..., rₚ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

Each reference is resolved independently against its own source document's POOM. The total width is:

`w(R) = (+ j : 1 ≤ j ≤ k : nⱼ)`

where ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R).

**C1 — ResolutionIntegrity (LEMMA).** Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* Fix any run (aⱼ, nⱼ) in the resolution and any i with 0 ≤ i < nⱼ. The corresponding block βⱼ = (vⱼ, aⱼ, nⱼ) satisfies B3 (ASN-0058): M(d_s)(vⱼ + i) = aⱼ + i. Since vⱼ + i ∈ dom(M(d_s)), S3 (ReferentialIntegrity, ASN-0036) gives M(d_s)(vⱼ + i) ∈ dom(C), hence aⱼ + i ∈ dom(C). ∎


## Worked Example

We verify the definitions against a concrete scenario. Let document d have depth-2 V-positions in subspace 1 (m = 2) with canonical decomposition:

`B = {β₁ = ([1,1], a, 3),  β₂ = ([1,4], b, 2),  β₃ = ([1,6], c, 1)}`

where a, b, c are distinct I-addresses from separate allocations. The arrangement maps six V-positions: M(d)([1,1]) = a, M(d)([1,2]) = a+1, M(d)([1,3]) = a+2, M(d)([1,4]) = b, M(d)([1,5]) = b+1, M(d)([1,6]) = c.

**Content reference.** Take σ = ([1,2], δ(4, 2)) — start at V-position [1,2] with ordinal displacement [0,4]. Then reach(σ) = [1,2] ⊕ [0,4] = [1,6]. The span range is {v : [1,2] ≤ v < [1,6] ∧ #v = 2} = {[1,2], [1,3], [1,4], [1,5]}. Each is in dom(M(d)), so the reference is well-formed. The displacement is ordinal (action point 2 = m), consistent with C0.

**Restriction.** f = M(d)|⟦σ⟧ has domain {[1,2], [1,3], [1,4], [1,5]} with f([1,2]) = a+1, f([1,3]) = a+2, f([1,4]) = b, f([1,5]) = b+1.

**Decomposition (C1a).** We verify f satisfies the preconditions: (i) f is functional (restriction of a function); (ii) dom(f) has 4 elements (finite); (iii) all V-positions have depth 2. Starting from singleton blocks {([1,2], a+1, 1), ([1,3], a+2, 1), ([1,4], b, 1), ([1,5], b+1, 1)}, we merge:

- [1,2] and [1,3]: V-adjacent ([1,3] = [1,2]+1) and I-adjacent (a+2 = (a+1)+1). Merge → ([1,2], a+1, 2).
- [1,4] and [1,5]: V-adjacent ([1,5] = [1,4]+1) and I-adjacent (b+1 = b+1). Merge → ([1,4], b, 2).

No further merges: ([1,2], a+1, 2) and ([1,4], b, 2) are V-adjacent ([1,4] = [1,2]+2) but not I-adjacent (b ≠ (a+1)+2 since a and b are from distinct allocations — M16, ASN-0058). The decomposition is maximally merged.

**Resolution.** resolve(d, σ) = ⟨(a+1, 2), (b, 2)⟩, ordered by V-start.

**C1 verification.** For run (a+1, 2): B3 gives M(d)([1,2]) = a+1 and M(d)([1,3]) = a+2; S3 gives a+1 ∈ dom(C) and a+2 ∈ dom(C). For run (b, 2): B3 gives M(d)([1,4]) = b and M(d)([1,5]) = b+1; S3 gives b ∈ dom(C) and b+1 ∈ dom(C). ✓

Total width: 2 + 2 = 4, matching the span width ℓₘ = 4 of the original content reference.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ContentReference | (d_s, σ) with d_s ∈ D, V_{u₁}(d_s) ≠ ∅; σ level-uniform with #u = #ℓ = m; depth-m V-positions in span range ⊆ dom(M(d_s)) | introduced |
| C0 | well-formed content references have ordinal displacements: action point of ℓ equals m | introduced |
| ContentReferenceSequence | ordered list ⟨r₁, ..., rₚ⟩ with p ≥ 1 | introduced |
| resolve(d_s, σ) | maximally merged I-address runs from M(d_s)\|⟦σ⟧, V-ordered | introduced |
| C1a | M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, S8-depth; in particular M(d_s)\|⟦σ⟧ | introduced |
| C1 | every resolved I-address is in dom(C) | introduced |


## Open Questions

- Must the resolution ordering across a multi-source content reference sequence preserve the sequence order, or may an implementation reorder source references provided the placed content lands at the correct V-positions?
