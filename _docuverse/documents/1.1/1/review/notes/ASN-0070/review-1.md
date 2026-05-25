# Review of ASN-0070

## REVISE

### Issue 1: Result form cannot accommodate cross-subspace R values

**ASN-0070, Result Form and the Operation**: "`follow(ℓ, d, i) = (d, Σ_V)` where `Σ_V` is a finite V-span-set with `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`."

**Problem**: When `coverage(e)` intersects both `dom(C)` and `dom(L)` (admitted by L4 of ASN-0043), the inverse image `R(d, e)` may contain V-positions from both content subspace and link subspace, which have different depths (S8-depth). A single normalized span-set per ASN-0053 requires level-uniformity (S6, S8) and cannot represent positions at distinct depths. The remark "decomposes naturally into per-subspace components, each canonicalised independently" is hand-waved and not reflected in the signature.

**Required**: Either restrict the operation to single-subspace endsets, or generalize the result type to a per-subspace family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` with each component level-uniform. Make the level-uniformity precondition explicit.

### Issue 2: F-det proof relies on canonical form, but operation does not commit to canonical form

**ASN-0070, Derived Properties (F-det) and Result Form**: F-det says "the canonical form of `Σ_V` is uniquely determined." But the postcondition only requires `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`, and the prose adds "any equivalent representation satisfies the postcondition."

**Problem**: If two invocations may return different (but equivalent) `Σ_V`, then F-det as stated ("same `Σ`, same canonical `Σ_V`") does not hold for the operation itself — only for the canonical form that callers must compute downstream. The text conflates "denotation is uniquely determined" (which follows from S2) with "the returned span-set is uniquely determined" (which requires committing to canonical form).

**Required**: Either commit the operation to canonical form in the postcondition, or restate F-det as a property of `⟦Σ_V⟧` (denotation-determinism) rather than `Σ_V` (representation-determinism).

### Issue 3: No concrete worked example

**ASN-0070, entire ASN**: No section verifies the key postconditions against a specific scenario.

**Problem**: The ASN states F-det, F-sound, F-complete, F-empty, F-multi without ever exhibiting a concrete arrangement, endset, and resulting span-set. A reader cannot verify the proofs against any instance.

**Required**: Provide at least one worked example. For instance: link `ℓ` with `L(ℓ).e₁ = {(a, δ(3, m))}` covering I-addresses `{a, a+1, a+2}`; document `d` with mapping blocks `β₁ = (v, a+1, 2)` and `β₂ = (v', a, 1)`; compute `follow(ℓ, d, 1)`, exhibit the resulting V-span-set, and verify F-sound, F-complete, F-multi (when applicable), and F-empty (with a second example where coverage misses ran(M(d))).

### Issue 4: Claims lack formal contract structure

**ASN-0070, Claims Introduced table**: Each row is a one-line summary in a table.

**Problem**: All cited foundation ASNs (ASN-0034, ASN-0036, ASN-0043, ASN-0047, ASN-0053, ASN-0058) format claims with explicit "Preconditions / Definition / Depends / Postconditions / Frame" blocks. ASN-0070 uses inline prose, making it impossible to audit each claim's premises against its conclusion. F0 and F1 are definitions; F2–F7 are derived properties; F8–F12 are observations or meta-properties — none labelled.

**Required**: Restructure each claim with a Formal Contract block including preconditions, definition (where applicable), depends, postconditions, and frame. Add explicit status labels (DEF, LEMMA, INV, COROLLARY, AXIOM) matching the foundation convention.

### Issue 5: Missing proof that I(β) ∩ ⟦σ⟧ yields a contiguous arithmetic sub-progression

**ASN-0070, Computation via Decomposition**: "If `I(β) ∩ ⟦σ⟧` is non-empty, it is a contiguous sub-range `{a + j + k : 0 ≤ k < c}` for some offset `j` and width `c`."

**Problem**: This is asserted, not proven. The I-extent `I(β) = {a, a+1, ..., a+n−1}` is an arithmetic progression under OrdinalShift; the span coverage `⟦σ⟧` is convex under T1 (T12). Convexity under T1 does not immediately imply that the intersection with an arithmetic progression of shifts is itself a contiguous sub-progression — it requires invoking TS5 (ShiftAmountMonotonicity) and T12 convexity together. This is the central computational claim and deserves an explicit proof.

**Required**: Prove the contiguity claim. Sketch: take `a+k₁, a+k₂ ∈ ⟦σ⟧` with `k₁ < k₂`. By TS5, `a+k₁ ≤ a+k ≤ a+k₂` for `k ∈ [k₁, k₂]`. By T12 convexity, `a+k ∈ ⟦σ⟧`. Hence the intersection is a contiguous sub-progression.

### Issue 6: F-sound and F-complete proofs are tautological restatements

**ASN-0070, Derived Properties**: F-sound proof: "By the definition `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`." F-complete: "Also by the definition."

**Problem**: If the postcondition is taken as given, both properties are trivial. They are not derived consequences but restatements of the postcondition. This obscures what an implementation must actually achieve.

**Required**: Either drop F-sound and F-complete as derived properties (since they are the postcondition itself), or reframe them as obligations on implementations and show what would have to be verified — e.g., that the computation in §"Computation via Decomposition" satisfies both.

### Issue 7: Missing weakest precondition analysis

**ASN-0070, entire ASN**: No wp analysis appears.

**Problem**: Review criteria explicitly require non-trivial wp analysis. Even for a pure query, wp can illuminate whether preconditions are minimal. For example: `wp(follow, ⟦Σ_V⟧ = R(d, L(ℓ).eᵢ))` should reduce to the stated preconditions (`ℓ ∈ dom(Σ.L) ∧ d ∈ E_doc ∧ 1 ≤ i ≤ |L(ℓ)|`). Verify that no implicit invariants (e.g., S2 functionality, S3★ referential integrity) need to be premised explicitly.

**Required**: Compute wp for the postcondition and for the frame condition `Σ' = Σ`. Verify minimality of preconditions or identify additional ones (e.g., `M(d)` well-defined, which is supplied by `d ∈ E_doc` plus reachable-state invariants from ASN-0047).

### Issue 8: F-det requires explicit canonical form definition for multi-subspace results

**ASN-0070, F-det proof**: Invokes S9 (NormalizationUniqueness, ASN-0053).

**Problem**: S9 establishes uniqueness only for normalised level-uniform span-sets. If `R(d, e)` spans multiple subspaces (Issue 1), no single normalised form exists. The ASN's per-subspace decomposition needs a stated canonical ordering — which subspace's span-set is listed first? — to make the result form unique.

**Required**: Define a canonical multi-subspace form (e.g., per-subspace span-sets indexed by subspace identifier in increasing order, each normalised by S9 within its subspace). Then F-det follows.

### Issue 9: Origin terminology applied to link addresses without grounding

**ASN-0070, Origin Symmetry**: "the address `M(d)(v)` is recoverable by consulting the state, and from that address `origin(M(d)(v))` is computable by the structural projection of S7 (ASN-0036)."

**Problem**: S7 (ASN-0036) defines `origin` on `dom(C)`. For `M(d)(v) ∈ dom(L)` (admitted by S3★ of ASN-0047 since L14a was superseded), the corresponding notion is `home(a) = N(a).0.U(a).0.D(a)` from ASN-0043's Definition. The terms are structurally equivalent but defined in distinct ASNs. The ASN should not extend "origin" to link addresses without grounding.

**Required**: Either invoke `home(a)` from ASN-0043 for link addresses, or note explicitly that the structural projection `N(a).0.U(a).0.D(a)` is what both `origin` (S7) and `home` (ASN-0043) name in their respective domains.

### Issue 10: Slot uniformity claim (F8) does not address L3's e₃ asymmetry

**ASN-0070, Slot Uniformity**: "The operation `follow` treats every slot identically."

**Problem**: By L3 (ASN-0043), `e₃ ≠ ∅` is required of every link, but other endsets may be empty. The ASN dismisses this in passing ("The link's *type identity* is preserved in `L(ℓ).e₃` regardless of whether it resolves") but does not explicitly note the asymmetric pre-conditions on endset population. Slot uniformity in the resolution mechanism is preserved, but the underlying endset constraints differ.

**Required**: State explicitly that resolution is symmetric across slots even though the L3 well-formedness constraint differentiates slot 3 from others. Confirm that `R(d, e_i) = ∅` is a regular outcome regardless of whether `e_i = ∅` or `e_i ≠ ∅ ∧ coverage(e_i) ∩ ran(M(d)) = ∅`.

### Issue 11: F11 (state-dependence) is not formalized as a property of follow

**ASN-0070, Claims Introduced**: "F11 — State-dependence — `follow` varies with `Σ.M` but `L(ℓ).eᵢ` is state-invariant"

**Problem**: F11 is an observation across states, not a property of a single invocation. It conflates two facts: (i) `L(ℓ)` is fixed by L12; (ii) `M(d)` may vary across transitions. Neither is a property of `follow` per se. F11 has no preconditions and no formal postcondition.

**Required**: Either restate F11 as a corollary of L12 + the absence of state in `follow`'s definition, or drop it as a claim. If kept, formalize as `(A Σ, Σ' :: L_Σ(ℓ) = L_{Σ'}(ℓ) ∧ (M_Σ(d) ≠ M_{Σ'}(d) ⟹ R_Σ(d, e) may differ from R_{Σ'}(d, e)))`.

### Issue 12: "Essentially forced" claim about span-set representation is unjustified

**ASN-0070, Result Form and the Operation**: "We argue the choice [of span-set representation] is essentially forced."

**Problem**: The argument given — that finite mapping-block decompositions yield contiguous V-runs — shows span-sets are *natural and compact*, not that they are *forced*. A characteristic function or an explicit V-position set would also satisfy the postcondition. The hyperbole obscures that this is a representational convention, not a derivation.

**Required**: Weaken to "natural" or "convenient". If a representational mandate is intended, derive it from a stated constraint (e.g., result must be O(blocks · endset-spans) in size, ruling out explicit V-position enumeration).

### Issue 13: F-multi proof too brief

**ASN-0070, Derived Properties (F-multi)**: "The inverse image of a set is the union of pre-images. Every pre-image of `a` is in the result."

**Problem**: This invokes set-theoretic identity without showing the chain `M(d)⁻¹(coverage(e)) = ⋃_{a ∈ coverage(e)} M(d)⁻¹({a})` and that S5 (UnrestrictedSharing) makes `|M(d)⁻¹({a})| > 1` realizable.

**Required**: Show the union decomposition and cite S5 explicitly to establish that multiplicity is structurally admissible, not just preserved by the inverse-image definition.

## OUT_OF_SCOPE

### Topic 1: Partial reach reporting form

The first open question — how partial reach (some I-addresses resolved, others not) should be reported to readers — is a presentation-layer concern that belongs in a future ASN on resolution reporting or UI semantics.

### Topic 2: Concurrency semantics for follow

The concurrency question is a separate concern requiring a transaction or visibility model not yet established.

### Topic 3: Relating follow across documents with shared transclusion lineage

This requires a lineage relation (derivation graph) not defined in current foundations.

VERDICT: REVISE
