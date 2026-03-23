# Revision Categorization — ASN-0061 review-11

**Date:** 2026-03-22 23:49

## Issue 1: S1 and S8 omitted from invariant verification
Category: INTERNAL
Reason: Both invariants follow directly from properties already verified in the ASN (S1 from C' = C, S8 from S8-fin/S8a/S2/S8-depth). The fix is adding two one-liner entries.

## Issue 2: Dangling reference to non-existent cases in D-DP
Category: INTERNAL
Reason: The fix is removing a stale cross-reference and replacing it with the plain-language description already present in the same sentence. No external evidence needed.
