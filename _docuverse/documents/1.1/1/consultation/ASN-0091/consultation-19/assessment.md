# Channel Assignment — ASN-0091 review-19

**Date:** 2026-05-26 19:27

## Issue 1: S8★ (PerSubspaceSpanDecomposition, ASN-0047) not explicitly discharged at Σ'
Reason: The fix is derivable from the ASN's own content — content-subspace clause from R-SP's discharge of ASN-0036's S8, link-subspace clause from RE-sub's pointwise preservation. All cited mechanisms are already in scope.

## Issue 2: ChainDisjointAdjacency inline lemma proof is incomplete in the prefix case
Reason: Pure structural argument using TA5(c) and ASN-0093's chain-element shape, both already cited. The corrected proof recasts the exclusion via tuple-equality on (d, s, k), no external evidence needed.

## Issue 3: In-cut-subspace exterior pointwise fixity is exercised but not lifted to a named RE-* claim
Reason: The property is already prose-exercised in Worked Example 3 and the mechanisms (R-PPERM/R-SPERM exterior branch, R-EXT from ASN-0084) are already cited. Lifting to a named RE-ext + RE-ext★ is a table-and-claim editorial operation internal to the ASN.
