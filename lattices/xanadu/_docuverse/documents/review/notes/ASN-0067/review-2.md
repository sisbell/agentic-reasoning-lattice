# Review of ASN-0067

## REVISE

### Issue 1: C3 claims "every foundational invariant" but the proof omits three

**ASN-0067, Invariant Preservation**: "C3 — InvariantPreservation (THEOREM). The COPY composite preserves every foundational invariant."

**Problem**: The derivation checks 17 specific invariants. Three foundational invariants from ASN-0047 receive no verification:

- **P4a (HistoricalFidelity)**: Every `(a, d) ∈ R'` requires a historical witness state where `a ∈ ran(M_k(d))`. For new pairs, the post-state Σ' is the witness. Trivial but unstated.
- **P5 (DestructionConfinement)**: `dom(C') ⊇ dom(C)` with unchanged values (C0), `E' ⊇ E` (equality), `R' ⊇ R` (construction). Trivial but unstated.
- **P3 (ArrangementMutabilityOnly)**: The composite uses only K.μ⁺, K.μ~, and K.ρ — permitted modes. Could be acknowledged as automatically satisfied by the elementary transition vocabulary.

**Required**: Either verify P4a and P5 (each is one sentence) and acknowledge P3, or narrow the claim from "every foundational invariant" to the specific list verified.

### Issue 2: C12a text–formula mismatch

**ASN-0067, Provenance Completeness**: "C12a — ProvenanceGranularity (LEMMA). The number of provenance entries created is bounded by the number of I-address runs in the resolved content: `|{(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}| ≤ (+ j : 1 ≤ j ≤ k : nⱼ)`"

**Problem**: The text says "bounded by the number of I-address runs" — that is `k`. The formula gives `Σ nⱼ`, the total width. These are different quantities. The formula is a valid but weaker bound; the text describes a stronger one it does not prove.

**Required**: Align text and formula. Either change the text to "bounded by the total width of the resolved content" or change the formula to `≤ k` with a supporting argument.

### Issue 3: Elementary Decomposition uses K.μ~ as if elementary

**ASN-0067, Elementary Decomposition**: "ValidComposite (ASN-0047) requires a finite sequence of elementary transitions where each step satisfies its precondition at the intermediate state. The COPY composite decomposes as Σ = Σ₀ →^{K.μ~} Σ₁ →^{K.μ⁺} Σ₂ →^{K.ρ} Σ₃ = Σ'"

**Problem**: K.μ~ is defined in ASN-0047 as a "Distinguished composite (K.μ⁻ + K.μ⁺)" — not an elementary transition. The section invokes the ValidComposite definition requiring elementary transitions, then presents a decomposition containing a composite step. The correct elementary decomposition is: K.μ⁻ (remove B_post) → K.μ⁺ (add shifted B_post) → K.μ⁺ (add placed blocks) → K.ρ* (provenance). The K.μ⁻ precondition at Σ₀ is simply `d ∈ E_doc`.

**Required**: Either unfold K.μ~ into its two elementary parts and verify the K.μ⁻ precondition, or explicitly note that K.μ~ is shorthand for its constituent elementary steps.

### Issue 4: ContentReference does not require level-uniform V-spans

**ASN-0067, Source Resolution**: "σ = (u, ℓ) is a well-formed V-span (T12, ASN-0034)"

**Problem**: T12 permits `#ℓ ≠ #u`. When `#ℓ < m = #u`, `reach(σ)` has depth `< m`, and the range `{t : u ≤ t < reach(σ)}` contains infinitely many depth-`m` tumblers (by T0(a)), so the well-formedness check always fails for finite documents — but for the wrong reason. When `#ℓ > m`, the reach has depth `> m`, and the depth-`m` positions in the range may not correspond to what the span width suggests. The span algebra (ASN-0053 S1–S11) is developed for level-uniform spans; its operations do not apply cleanly otherwise.

**Required**: Require `#ℓ = m` in the ContentReference definition. This ensures `reach(σ)` has depth `m`, the position range is well-bounded, and the span algebra applies.

### Issue 5: Five-step construction omits non-text-subspace frame

**ASN-0067, The COPY Transition, Phase 2**: "B' = B_pre ∪ {γ₁, ..., γₖ} ∪ {β↑w : β ∈ B_post}" and "M'(d) is the arrangement defined by B'"

**Problem**: B and B' are text-subspace block decompositions (v₁ ≥ 1, per ASN-0058 B1). If M(d) contains link-subspace V-positions (v₁ = 0), they appear in neither B nor B'. The statement "M'(d) is the arrangement defined by B'" specifies only the text-subspace portion, leaving non-text V-positions undefined. The elementary decomposition handles this correctly — link-subspace positions have v₁ = 0, which is less than the text-subspace insertion point under T1, so the K.μ~ bijection maps them to themselves — but the five-step construction, which is the primary definition, does not state this.

**Required**: Add to step (v) or the effects: "For non-text-subspace positions: `M'(d)(p) = M(d)(p)`."

### Issue 6: ValidInsertionPosition depth underdetermined for empty documents

**ASN-0067, Displacement**: "When N = 0, v = [S, 1, ..., 1] of depth m ≥ 2 — the canonical minimum position required by D-MIN — where S is the text subspace identifier and m is the chosen V-position depth."

**Problem**: "The chosen V-position depth" implies m is a free parameter, but the COPY definition's parameters are (d, v, R) — m does not appear explicitly. Implicitly `m = #v`. But the first COPY into an empty text subspace permanently establishes the subspace's V-position depth (S8-depth requires all subsequent V-positions to match). This architectural consequence is not stated.

**Required**: State that `m = #v`, and note that when N = 0, the choice of v establishes the text subspace's permanent V-position depth.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics
**Why out of scope**: C13's observation correctly identifies that ValidComposite provides only sequential correctness. Intermediate-state visibility and serialization for concurrent COPY operations require a concurrency model not yet in the foundation.

### Topic 2: V-position depth establishment convention
**Why out of scope**: S8-depth (ASN-0036) defines the fixed-depth property but not how a subspace's depth is initially established. This foundational gap is shared by any operation that first populates an empty subspace, not specific to COPY.

### Topic 3: Authorization for cross-document COPY
**Why out of scope**: Correctly listed as an open question. Permission semantics are a policy layer above the state-transition model.

VERDICT: REVISE
