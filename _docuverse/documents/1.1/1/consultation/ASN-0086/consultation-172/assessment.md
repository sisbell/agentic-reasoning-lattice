# Channel Assignment — ASN-0086 review-172

**Date:** 2026-06-01 09:58

## Issue 1: Non-circularity justification embedded in R0
Reason: Purely an editorial/dependency-ordering fix — cite L-ContiguousPrefix plainly or reorder lemmas. No design intent or implementation evidence is at stake; derivable from the ASN's own structure.

## Issue 2: Scope-justifying forward pointer in R0's L1b discharge
Reason: A deletion of a self-disclaiming parenthetical; the `#E(a) ≥ 2` fact is already established locally. Entirely internal.

## Issue 3: Premise-inventory preamble in R0a
Reason: Removing a duplicative preview that the case headers already carry. No external input needed.

## Issue 4: CoverageEqualityDecidable partition omits exterior cells
Reason: The missing fact (both coverages lie within `[c₁, c_m)` since all interval endpoints are in `P`) follows from the lemma's own construction; a one-sentence addition closes it internally.
