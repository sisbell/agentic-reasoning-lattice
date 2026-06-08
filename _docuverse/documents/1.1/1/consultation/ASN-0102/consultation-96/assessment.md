# Channel Assignment — ASN-0102 review-96

**Date:** 2026-06-08 04:51

## Issue 1: X2 restates ASN-0093's K.α allocation mechanics rather than using them
Reason: Fully internal. The fix collapses X2 to a corollary of X1 and X6 (`D_d` unchanged ⟹ K.α identical), which are both already established in this ASN; it removes a restatement of ASN-0093 mechanics rather than needing any new fact about what the allocator does or was meant to do.

## Issue 2: X14's label understates its scope, obscuring the invariant-maintenance argument
Reason: Fully internal. This is a presentational split/rename — separating the invariant-maintenance discharge (per-state + boundary + P3) from the containment-recording claim. No design intent or implementation evidence is involved; the proof content already exists and only its organization changes.
