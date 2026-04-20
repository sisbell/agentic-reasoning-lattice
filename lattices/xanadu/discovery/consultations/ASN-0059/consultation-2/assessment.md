# Revision Categorization — ASN-0059 review-2

**Date:** 2026-03-20 21:52



## Issue 1: I9 proof sketch asserts shifted contiguity without justification
Category: INTERNAL
Reason: The missing identity `shift(v + j, n) = shift(v, n) + j` is already proven in the I10 verification within this same ASN. The fix is adding a reference to it or deriving it inline from commutativity of ℕ addition — no external evidence needed.

## Issue 2: P8 (EntityHierarchy) omitted from invariant preservation
Category: INTERNAL
Reason: P8 is defined in ASN-0047 and its preservation follows trivially from `E' = E`, which is already stated in the ASN. This is a mechanical gap in an enumeration, fixable by adding one line.
