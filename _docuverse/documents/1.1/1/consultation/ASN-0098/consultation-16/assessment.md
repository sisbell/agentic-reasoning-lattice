# Channel Assignment — ASN-0098 review-16

**Date:** 2026-05-26 01:51

## Issue 1: LP12a boundary case ("content-subspace empty") hand-waves the coverage-subspace argument
Reason: The required corollary is a structural fact about F-candidates inside a canonical span's coverage, derivable from LP-Fin's existing #d ≤ #d_0 argument combined with the position-(#d_0+2) subspace-comparison already used in the "same document, cross subspace" achievability case. All ingredients (T1 case (i), structural form of F, SubspaceConventionAxiom citation pattern) are present in the ASN.

## Issue 2: LP-Fin's finiteness conclusion is asserted rather than derived case-by-case
Reason: The required case decomposition uses only T1 case (i), T4-validity of d_0 (specifying zero positions z_1, z_2), the prefix-copy region of TumblerAdd (for canonical ℓ), and the structural form of F — all already established in the ASN. The fix expands the existing finiteness assertion into the sharper #d < #d_0 (zero candidates) vs. #d = #d_0 (exactly n candidates) split.
