# Revision Categorization — ASN-0051 review-7

**Date:** 2026-03-20 22:07



## Issue 1: SV5 proof asserts domain equality not guaranteed by K.μ~
Category: INTERNAL
Reason: The fix is explicitly stated in the review — replace a false intermediate claim with the correct bijection statement. All needed information (K.μ~ definition, the proof structure) is already in the ASN.

## Issue 2: π overloaded between projection and reordering bijection
Category: INTERNAL
Reason: This is a notation choice internal to the ASN. The fix requires selecting a distinct symbol and performing a mechanical substitution throughout the SV5 section and SV13(e) — no external design intent or implementation evidence needed.
