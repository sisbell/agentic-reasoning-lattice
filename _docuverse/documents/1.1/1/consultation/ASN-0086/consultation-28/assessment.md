# Channel Assignment — ASN-0086 review-28

**Date:** 2026-05-17 04:28

## Issue 1: R0a Case 2 sub-argument wording error
Reason: Pure logical fix internal to the proof. The correction restates the prefix using L1a's definition (`N(·).0.U(·).0.D(·)`) and is fully derivable from prefix arithmetic plus the third-zero position equality that `a ≼ a'` already supplies.

## Issue 2: R6c proof omits L_K monotonicity step
Reason: Trivial citation of R3 (already proved earlier in the ASN). The propagation `(a, F, G) ∈ L_K^Σ ⊆ L_K^{Σ'}` follows directly from R3 applied along the inductive chain.

## Issue 3: Worked sketch "first four entries" wording
Reason: Pure wording fix — the set `dom(Σ_5.L)` has no canonical ordering. Rephrasing as "the four entries homed at d" is derivable from facts already enumerated in the worked sketch.

## Issue 4: R7's stipulated half buried in Step 3 narrative
Reason: Presentation restructuring of material already present in R7's proof. The proven/stipulated decomposition is fully articulated in Step 3; the fix only hoists it to R7's headline as R7a/R7b sub-claims.

## Issue 5: Setup/discipline conditionality lacks a consolidated dependency view
Reason: Compilation of tags already present in each R-claim's header and proof. The transitive dependencies (R5→R0, Nullify→R0a, etc.) are stated in the existing inline tags; the table consolidates without introducing new content.

## Issue 6: SharedDepthOneAllocator's role in worked sketch chain is implicit
Reason: Citation fix for a lemma already proved in the ASN's Setup section. The worked sketch's chain construction already invokes the lemma's content; the fix only adds the explicit citation.

## Issue 7: R0 Step 4 L11a discharge for Case A
Reason: Consolidation using Appendix A.1's sparse-allocator interpretation (already in the ASN) plus L11a's definition. The deposit-level reading of "distinct allocation events" follows from the sparse-allocator framing combined with class-(iii) atomicity, both already established.
