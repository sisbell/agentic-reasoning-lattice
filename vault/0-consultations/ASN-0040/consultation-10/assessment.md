# Revision Categorization — ASN-0040 review-10

**Date:** 2026-04-09 11:50



## Issue 1: B6 biconditional is false — condition (i) is not necessary for T4 preservation
Category: INTERNAL
Reason: The fix is fully derivable from the ASN's own content. The review already identifies both repair options: weaken to implication, or replace the necessity argument with the correct B7-based one. All definitions needed (B6, B7, T4, S(p,d)) are present in this ASN and ASN-0034.

## Issue 2: B1 proof invokes B7 without checking its preconditions
Category: INTERNAL
Reason: The gap is in proof coverage, not in missing design intent or implementation evidence. The two unaddressed sub-cases (vacuous via B10, shadow via stream identity) are derivable from definitions already in the ASN. The review even sketches the repair arguments.

## Issue 3: Finiteness of B₀ not explicitly required
Category: INTERNAL
Reason: The fix is adding an explicit finiteness clause to B₀ conf. or the Σ.B definition. The ASN already assumes finiteness in the next function's formal contract — this is a missing explicit statement, not a design or implementation question.
