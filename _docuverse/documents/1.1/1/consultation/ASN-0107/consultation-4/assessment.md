# Channel Assignment — ASN-0107 review-4

**Date:** 2026-06-07 22:01

## Issue 1: A1's justification asserts a false dependency for the existence count
Reason: Fully internal. The fix follows from the ASN's own definitions of `match`/`sat` and E3: existence-count invariance under K.α depends only on permanent coverages and fixed `Q`, both independent of where content is stored, so the "unless it lies in Q" qualifier is removable by reasoning already present.

## Issue 2: R1's statement is a single ~12-line sentence with nested conditions
Reason: Fully internal. Purely expository restructuring — enumerate the preconditions and split the `Δ ∈ {−1,0}` cases using R2/R3, all already stated in the ASN; no design intent or implementation evidence is needed.
