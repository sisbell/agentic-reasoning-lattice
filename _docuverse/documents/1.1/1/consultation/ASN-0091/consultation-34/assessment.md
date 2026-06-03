# Channel Assignment — ASN-0091 review-34

**Date:** 2026-06-03 11:34

## Issue 1: The "value-uniform ⟺ M'(d) = M(d)" equivalence is false
Reason: The correct fixed-point criterion (rotation/swap-invariance of the affected-range value sequence) is pure mathematics derivable from the cut-permutation definitions already in the ASN — R-P1/R-P2 (pivot) and R-S1/R-S2/R-S3 (4-cut swap) plus K.μ~'s clause (ii), all stated here. The reviewer's own counterexample uses only the ASN's R-P1/R-P2, confirming no external design intent or implementation evidence is needed.

## Issue 2: Reverse direction of the bijection-class characterization asserted without proof
Reason: Assembling the global π from per-block bijections and verifying RA-π pointwise is a self-contained construction over the ASN's own definitions (RA-π, RA-dom, the pre-image partition) — no design intent or implementation evidence required.
