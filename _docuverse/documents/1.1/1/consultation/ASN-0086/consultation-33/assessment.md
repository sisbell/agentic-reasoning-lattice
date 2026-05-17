# Channel Assignment — ASN-0086 review-33

**Date:** 2026-05-17 06:16

## Issue 1: Hypothesis tagging conflates Setup with Subspace-distinctness
Reason: The fix is purely a bookkeeping/tagging convention internal to the ASN — both hypotheses (Setup and Subspace-distinctness) are already explicitly introduced in the ASN's Setup section, and the consumption sites are already noted. The author needs to decide between options (a) extend tagging or (b) bundle as shorthand; either is fully derivable from existing ASN content.

## Issue 2: R6c's chain application of R3 elides transitivity
Reason: Pure proof-rigor fix — add an explicit inductive statement parallel to the `nullified` induction already present. The mathematical content (R3 single-step + transitivity of `⊆`) is unambiguous and entirely within the ASN.

## Issue 3: Sibling-frontier discipline not formally labeled as DEF
Reason: Pure formatting fix — promote bold prose to a labeled DEF block, matching the lemma-labeling pattern already used elsewhere in the ASN. The content of the discipline is fully specified.

## Issue 4: R0a's proof structure interleaves induction and corollary
Reason: Pure restructuring of proof presentation — reorder existing pieces (Case 2 sub-argument, sibling-stream induction, antichain corollary) into logical dependency order. All content is already present.

## Issue 5: FramePreservation's specialization (e) lacks a precise predicate-form check
Reason: Rephrasing to make explicit what `→`-admissibility depends on — `dom(Σ.L)` and `dom(Σ.M)` but not the endset values. This is derivable from L1c (definition in ASN-0043, cited by the ASN), the State transition relation section, and Appendix A.2's coarsening discussion, all already in ASN-0086.

## Issue 6: Step 5.2's abstraction acknowledged but not fully justified
Reason: The reviewer's option (a) — trim the meta-discussion and present the substitution chain tersely — is fully internal, and the ASN already establishes that arrangement-modifying transitions are out of scope. Option (b) would require pulling in a "forthcoming ASN-0036-extending operation" that doesn't yet exist; option (a) is the natural in-scope fix.

## Issue 7: Emit_K's A_K membership analysis depends on retraction discipline not made operational
Reason: The regime (i)/(ii) distinction is already fully articulated in Emit_K's Definition; the fix is to label regime (ii) as a discipline (parallel to sibling-frontier) and/or add consequence notes — all structural/labeling work derivable from the ASN's own content. The non-monotonicity of `A_K` is already in Consequence R6c(e).

## Issue 8: SharedDepthOneAllocator's "extending d's rightmost element-field" terminology
Reason: Pure terminology clarification — disambiguate "element-field" as a generic zero-delimited field vs. T4's specific E-field. The ASN already cites T4b's N/U/D/E projections, so the corrected phrasing follows from existing references.
