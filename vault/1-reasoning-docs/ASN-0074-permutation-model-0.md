# ASN-0074: Permutation Model 0

*2026-03-22*

The permutation model (ASN-0058) defines block decompositions for document arrangements and proves existence and uniqueness of maximally merged canonical forms. This ASN extends the model with content references — a mechanism for identifying a span of positions within a document's arrangement — and resolution, which extracts the I-address runs from the block decomposition restricted to that span. The extension establishes that the canonical decomposition (M11, M12) applies to any restriction of an arrangement satisfying the structural preconditions, and that every resolved I-address satisfies referential integrity. We work with system state Σ = (C, E, M, R) per ASN-0047: C is the content store (T ⇀ Val), E the entity set with E_doc the set of documents, and M the arrangement function with M(d) : T ⇀ T for each document d. The extension references properties from the foundation: S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S8-fin (FiniteArrangement), S8-depth (FixedDepthVPositions) from ASN-0036; T12 (SpanWellDefinedness) from ASN-0034; S6 (LevelConstraint) and ⟦σ⟧ (SpanDenotation) from ASN-0053.


## Content References

**Definition — ContentReference.** A *content reference* is a pair (d_s, σ) where d_s ∈ E_doc and σ = (u, ℓ) is a level-uniform V-span — that is, T12 (ASN-0034) holds and `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036). The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies. The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

Since `#u = #ℓ = m`, dom(M(d_s)) contains only depth-m V-positions (S8-depth), and reach(σ) has depth m (S6), the depth-m restriction is structurally guaranteed.

**Definition — ContentReferenceSequence.** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.


## Resolution

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


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ContentReference | DEF | (d_s, σ) with d_s ∈ E_doc; σ level-uniform with #u = #ℓ = m; depth-m V-positions in span range ⊆ dom(M(d_s)) | introduced |
| ContentReferenceSequence | DEF | ordered list ⟨r₁, ..., rₚ⟩ with p ≥ 1 | introduced |
| resolve(d_s, σ) | DEF | maximally merged I-address runs from M(d_s)\|⟦σ⟧, V-ordered | introduced |
| C1a | COROLLARY | M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, S8-depth; in particular M(d_s)\|⟦σ⟧ | introduced |
| C1 | LEMMA | every resolved I-address is in dom(C) | introduced |


## Open Questions

- Must the resolution ordering across a multi-source content reference sequence preserve the sequence order, or may an implementation reorder source references provided the placed content lands at the correct V-positions?
