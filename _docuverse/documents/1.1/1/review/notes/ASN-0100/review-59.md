# Review of ASN-0100

This note is mathematically thorough and, on the proofs I checked (S2 region-disjointness, INS.chain-shift via TA5-SigValid, the closed-interval D-CTG★ reduction, the K.μ⁻/K.μ⁺ forced-ordering, the multi-step LP4/LP5 chaining for `d' ≠ d`, S8★ via C1a, the provenance coupling discharge), the reasoning holds and edge cases (empty doc, `j=0`, append, non-tight endset) are covered. My findings are residual meta-prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Forward-reference pointer in a structural slot, repeated downstream
**ASN-0100, §The Operation: Formal Contract (Composite atomicity)**: "The component-by-component uniqueness argument, and the atomicity of the composite boundary, are established once in §Atomicity."
**Problem**: The first sentence of this mini-paragraph ("Σ' is uniquely determined ... though the substrate decomposition ... is not") is a substantive claim; the quoted second sentence carries no reasoning — it is a pure deferral. The same deferral recurs in the INS.atomicity claim row ("composite-level atomicity is definitional (argued once in §Atomicity)") and the object argument lives in §Atomicity. This is the "multiple paragraphs defer to the same downstream location" pattern, with essay/pointer content occupying the slot between preconditions and effects.
**Required**: Keep the uniqueness statement (it is the carrier of INS.atomicity / the uniqueness claim) and delete the "established once in §Atomicity" pointer. Likewise drop "(argued once in §Atomicity)" from the claim row — the row should state what the claim *is*, not where it is proved.

### Issue 2: Citation-strategy narration around (INS.μ⁻-fires)
**ASN-0100, §The Operation: Formal Contract, step 2**: "We record this firing condition and its case split once, as (INS.μ⁻-fires), and cite it throughout the rest of the ASN rather than re-deriving it: K.μ⁻ fires iff Right ≠ ∅; ..."
**Problem**: The clause "and cite it throughout the rest of the ASN rather than re-deriving it" is process narration about how the label will be reused, not content advancing the claim. The label and the iff/two-case body are substantive and correctly reused at §Position Constraints, §Atomicity, and the worked example; the framing is the noise the reader skips past.
**Required**: Reduce to the label introduction and its definition: "(INS.μ⁻-fires): K.μ⁻ fires iff Right ≠ ∅; it is omitted in exactly two cases ...". Drop the citation-strategy clause.

### Issue 3: Re-derivation of the K.μ⁻-omission despite the established label
**ASN-0100, §A Worked Example (Empty-document first insertion)**: "K.μ⁻ is omitted because the content-subspace Right region is empty (`V_{s_C}(d) = ∅`, so no `v ≥ p`)."
**Problem**: Once (INS.μ⁻-fires) exists precisely to record this case split once, re-deriving the omission rather than citing the label (as §Position Constraints does — "this is the empty-content-subspace case of (INS.μ⁻-fires)") reintroduces the redundancy the label was created to remove.
**Required**: Cite the label, as the parallel append/empty cases elsewhere already do, rather than re-justifying `Right = ∅`.

## OUT_OF_SCOPE

None. The Open Questions and §Bounding the Scope already partition future territory (link-subspace insertion, COPY/DELETE/REARRANGE, versioning, replication) correctly.

VERDICT: REVISE
