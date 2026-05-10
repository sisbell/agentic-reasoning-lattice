# Revision Categorization — ASN-0065 review-3

**Date:** 2026-03-21 21:08

## Issue 1: 3-cut worked example claims three canonical blocks; there are four
Category: INTERNAL
Reason: The worked example contains all the data — position [1,5] → E is explicitly computed under R-EXT. The missing fourth block is a counting error fixable from the ASN's own content.

## Issue 2: Misidentified cut position in 3-cut block narrative
Category: INTERNAL
Reason: The cut sequence C = ([1,2], [1,4], [1,5]) and block β₁ = ([1,1], A, 3) are both stated in the ASN. That c₀ = [1,2] is interior to β₁ follows directly from these definitions.

## Issue 3: Cross-ASN reference to non-foundation ASN-0061
Category: INTERNAL
Reason: The fix is to remove the cross-reference or restate the property inline. The review provides the replacement wording, and no external evidence is needed.

## Issue 4: Incomplete coupling constraint verification
Category: INTERNAL
Reason: J0 and J1' are both vacuously satisfied by properties already proven in the ASN (R-CF(a) and R-CF(c)/J3). The J2 correction follows from ASN-0047's definitions of elementary vs. composite transitions, already referenced.

## Issue 5: Open question about depth-2 generalization is already resolved
Category: INTERNAL
Reason: D-CTG-depth and D-SEQ are foundation ASNs already cited in the ASN. The generalization follows mechanically from their statements — only the last ordinal component varies at any depth.

## Issue 6: Vacuously true 3-cut/4-cut equivalence claim
Category: INTERNAL
Reason: CS2 (strict ordering) is defined in the ASN and immediately implies w_μ ≥ 1. The fix is a rewording derivable entirely from the ASN's own preconditions.
