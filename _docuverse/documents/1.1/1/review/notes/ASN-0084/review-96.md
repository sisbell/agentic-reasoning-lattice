# Review of ASN-0084

The mathematics is sound. I traced all five worked examples and the R-PIV/R-SWP coverage arithmetic, R-PPERM/R-SPERM bijectivity, R-COMM commutation, and the R-BLK Split/Merge inheritance — each checks out, including the boundary (empty-exterior) and non-S cases. The OrdShiftHom citations are all clause (a), and the non-S "carried verbatim" claim now sits in Phase 3, so the two previously-declined findings do not recur. My findings are confined to the prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: "Interaction between successive cuts" duplicates Phase 2's justification
**ASN-0084, R-BLK, Phase 1 (Split)**: "Interaction between successive cuts. After all cuts are processed, no run straddles any cut position cᵢ for 0 ≤ i ≤ n − 1, since Phase 1 splits at every cut interior to a run."
**Problem**: This labeled sub-claim restates the immediate consequence of the splitting rule that Phase 1 just described, and the same fact is re-asserted in Phase 2's parenthetical "no run crosses a cut boundary (subspace-S runs are split at S-subspace cuts, and non-S runs are entirely contained in their subspace...)". Two paragraphs say the same thing; the reader must hold the restatement without new reasoning.
**Required**: Delete the "Interaction between successive cuts" paragraph; Phase 2 already carries the no-straddle fact where it is used.

### Issue 2: Phase 2 closing sentence is garbled and redundant
**ASN-0084, R-BLK, Phase 2 (Classify)**: "The classification by Phase 1 of the remaining cuts together with the subspace separation of non-S runs covers all runs."
**Problem**: Phase 1 performs *splitting*, not classification, so "classification by Phase 1" misnames the step; "the remaining cuts" has no antecedent. The sentence also merely re-summarizes the preceding sentence ("Each run... lies entirely within one region... because no run crosses a cut boundary"). It adds confusion, not coverage.
**Required**: Remove the sentence; the preceding sentence already establishes that every post-split run is classified into exactly one region.

### Issue 3: Phase 3 re-establishes "π is identity on non-S/exterior" twice
**ASN-0084, R-BLK, Phase 3 (Reassemble)**: the per-region bullets already state it — "Non-S runs: carried through unchanged. By the non-S clause of R-PPERM/R-SPERM, π is the identity on V(b)..." and "Exterior runs: π(vₖ) = vₖ by the subspace-S exterior clause..." — and the paragraph immediately following repeats it: "The non-S and exterior runs carry through with their widths intact because π is the identity on them (the non-S and exterior clauses of R-PPERM/R-SPERM)..."
**Problem**: The identity-on-non-S/exterior fact is asserted in the bullets and then re-asserted in the next paragraph. The only new content in that paragraph is the commutation note π(vₖ + k) = π(vₖ) + k holds trivially; the rest is restatement the reader must skip past.
**Required**: Drop the redundant "π is the identity on them" clause from the follow-on paragraph and keep only the commutation point (trivial on non-S/exterior, R-COMM on α/μ/β).

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements (k > 4), composition of rearrangements, run-count growth bounds, canonical-partition recovery procedure
**Why out of scope**: These are correctly deferred to the Open Questions; they are new territory (additional operations and their algebra), not defects in the cut-point class this ASN specifies.

VERDICT: REVISE
