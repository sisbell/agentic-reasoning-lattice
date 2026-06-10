# Channel Assignment — ASN-0127 review-24

**Date:** 2026-06-10 12:07

## Issue 1: The cardinality-changing variant's negative match check for L_2' skips slot 2
Reason: The fix is internal. The missing fact `coverage(∅) = ∅` follows immediately from the Coverage definition already cited (deterministic function of the endset's spans, ASN-0043) — an empty endset contributes an empty union of spans — and the required edit is a mechanical completion of the slot sweep to match the note's own established three-slot enumeration pattern.

## Issue 2: Two sentences of meta-prose that restate or defend rather than advance
Reason: The fix is a pure deletion of redundant prose; the review confirms all content already exists at its proper sites (LP13 discharge in E-INV, the empty boundary in F-V, the full-region equality in F-FULL's statement). No design intent or implementation evidence bears on removing restatement.
