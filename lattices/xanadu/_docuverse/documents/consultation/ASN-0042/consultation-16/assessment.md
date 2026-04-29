# Revision Categorization — ASN-0042 review-16

**Date:** 2026-03-16 07:20



## Issue 1: Delegation ordering permits unauthorized nesting — Account-level permanence Corollary unsupported
Category: INTERNAL
Reason: The fix is a logical constraint derivable from the ASN's own definitions. The counterexample and the required sixth condition (vi) are stated in the review itself, and the delegation relation's structure already contains the pattern — the missing condition closes a gap in the formal machinery without requiring new design intent or implementation evidence.

## Issue 2: Primitive relation "allocated by" undeclared
Category: INTERNAL
Reason: The relation is already used in two formal properties (O5, O16) and follows the same declaration pattern as `delegated_Σ` which is fully specified in the ASN. Declaring the signature and adding it to the Properties Introduced table requires only the ASN's own conventions, no external evidence.

## Issue 3: O12 motivation overstates orphaning risk
Category: INTERNAL
Reason: The correction replaces an inaccurate formal claim with the accurate one (O3 monotonic refinement, O8 irrevocability), both of which are already derived in the ASN. The Nelson/Gregory evidence cited in the existing text is already correct and sufficient — only the orphaning sentence needs rewording using properties already present.
