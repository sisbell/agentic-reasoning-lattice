# Revision Categorization — ASN-0040 review-4

**Date:** 2026-03-15 13:22

## Issue 1: T4 validity is required but not enforced
Category: INTERNAL
Reason: The fix adds T4 as a precondition to B6, requires T4 for B₀, and derives a closure guarantee — all from definitions already present in the ASN (T4, B6, B7, B₀ conformance, IncrementPreservesValidity from ASN-0034). No external evidence needed.

## Issue 2: Freshness derivation omits streamless seed elements
Category: INTERNAL
Reason: The review itself notes the gap is "trivially closeable" — adding the third case (streamless seed elements ∉ S(p,d) by definition) completes the partition using only facts already established in the ASN.

## Issue 3: Citation error in B7 Case 3 verification
Category: INTERNAL
Reason: Wrong TA5 sub-clause cited (c instead of d). The computation is correct; only the reference needs changing. Purely internal notation fix.
