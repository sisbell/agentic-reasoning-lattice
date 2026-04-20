# Revision Categorization — ASN-0053 review-11

**Date:** 2026-03-19 07:42



## Issue 1: Level-uniformity closure not stated as postcondition
Category: INTERNAL
Reason: The review itself notes that "the facts are in the proofs; the conclusions are not." The fix is adding explicit postcondition sentences derived from length calculations already present in S1, S3, S4, and S8.

## Issue 2: S11 asserts representability without construction
Category: INTERNAL
Reason: The span constructions, T12 verifications, and concrete example all follow from definitions and properties already established in the ASN (D1, level-uniformity, TumblerSubtract). No external design intent or implementation evidence is needed.

## Issue 3: Split-merge inverse claimed without derivation
Category: INTERNAL
Reason: The full derivation chains through S3's merge construction, S4's split outputs, and D1's round-trip — all properties already stated and proved within the ASN. The fix is assembling existing results into an explicit proof.
