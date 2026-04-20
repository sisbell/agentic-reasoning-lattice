# Revision Categorization — ASN-0054 review-1

**Date:** 2026-03-19 23:48

## Issue 1: Notation collision in A0
Category: INTERNAL
Reason: The fix is renaming bound variables and clarifying component-access notation — purely a presentation issue resolvable from the formula itself.

## Issue 2: wp direction reversed in preservation arguments
Category: INTERNAL
Reason: The intended logical claim is clear from context; the fix is reversing the implication arrow or switching to a Hoare triple. No design or implementation evidence needed.

## Issue 3: Zero-displacement in run formula
Category: INTERNAL
Reason: The ASN already states the base case is "immediate" and references ASN-0036's identical convention. The fix is restricting the quantifier range or adding the explicit i=0 convention, both derivable from existing content.

## Issue 4: COPY absent from preservation section
Category: INTERNAL
Reason: The ASN already treats transclusion as placing content at V-positions (A8, A9), and the review itself identifies that COPY's V-space effect is structurally identical to INSERT. The fix is a single sentence noting this subsumption.

## Issue 5: Break causes enumeration incomplete
Category: INTERNAL
Reason: The formal break predicate (`M_j ≠ M_{j-1} ⊕ u_I(M_{j-1})`) is already stated in the ASN and covers all three cases including depth mismatch. The fix is aligning the prose enumeration with the formal definition already present.
