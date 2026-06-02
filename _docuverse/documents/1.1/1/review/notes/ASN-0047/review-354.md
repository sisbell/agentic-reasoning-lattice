# Review of ASN-0047

This ASN is mathematically mature — I checked the coupling self-consistency (J1'★ correctly invalidates place-then-remove composites within one boundary; P4a's trace-witnessing survives), the K.μ~ admissibility/full-clearance equivalence (clause (iii) length-preservation correctly pins the rebuild to the original content depth via post-state D-SEQ★), the Bridging lemma (empty allocated documents stay in `dom(M) = E_doc`), and the entity/version/sibling allocator dispatch. These hold. The note carries `review-mode.anti-bloat`, and the remaining findings are accreted meta-prose, not correctness.

## REVISE

### Issue 1: Mid-proof concrete trace duplicates the general derivation it sits inside
**ASN-0047, *Amendments to existing transitions*, D-SEQ★ derivation, Step 1**: The "*Concrete trace (m = 3)*" paragraph re-runs Step 1's construction (`u_M = [s_C, 1, M]`, the bracketing `v_min < u_M < v`, the S8-fin contradiction) for the specific depth `m = 3`, immediately after Step 1 has already proved the identical argument for all `m ≥ 3`.
**Problem**: This is a concrete example placed in a proof slot, restating the general case's reasoning in instantiated form. The anti-bloat guidance says concrete examples are fine but to flag their *placement*: the general Step 1 already discharges `m = 3`, and the worked-example sections elsewhere already exercise small depths, so the embedded trace adds no reasoning the reader cannot reconstruct.
**Required**: Remove the "*Concrete trace (m = 3)*" paragraph (Step 1 covers it), or relocate the instantiation to a worked example if a depth-3 demonstration is judged independently valuable.

### Issue 2: Multiple sections defer to the same downstream location for the K.μ⁻ contraction-shape equivalence
**ASN-0047, K.μ⁻ precondition; K.μ⁻ amendment; worked examples**: The claim that the per-subspace suffix-prefix shape is *derived* (not a separate precondition) is deferred forward identically from at least three sites — K.μ⁻'s precondition ("derived consequences of the restriction form `M'(d) = M(d) ↾ R`, proved in *K.μ⁻ admissible contraction shape* below"), the K.μ⁻ amendment paragraph, and the interior-replacement / link worked examples ("forced … as a *derived consequence*", "the contraction shape at the K.μ⁻ definition").
**Problem**: This matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The reader chasing the shape claim is bounced between sites that each restate the deferral rather than the content.
**Required**: State the derived-shape relationship once at the K.μ⁻ definition (the equivalence proof), and replace the repeated forward pointers elsewhere with a single citation, removing the restated justifications at each call site.

### Issue 3: J2's wp "analysis" is a frame restatement, not analysis
**ASN-0047, *Coupling and isolation*, J2**: "The wp analysis confirms this. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For L12: does not touch L."
**Problem**: Per the review standard on weakest-precondition depth, a wp computed only for cases where the answer is "trivially true (frame)" is not analysis. The four bullets restate the frame `C' = C ∧ L' = L ∧ E' = E ∧ R' = R` already given in J2's own statement. The single non-trivial line is the P4★ subset argument (`Contains_C(Σ') ⊆ Contains_C(Σ)`); the frame-restatement bullets surrounding it are essay content in a structural slot.
**Required**: Keep the P4★ subset reasoning (the only load-bearing case) and drop the four "does not touch X" restatements, which the frame line already asserts.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal, transclusion-chain provenance, concurrency
**Why out of scope**: The Open Questions (interior `DELETEVSPAN` compaction, transitive transclusion provenance, concurrent home-document allocation, node-baptism protocol mechanism, type-only/one-sided links) are correctly deferred — they concern named operations, the inter-server protocol, and authority model, all listed OUT OF SCOPE for this transition-taxonomy ASN. No revision is owed here.

VERDICT: REVISE
