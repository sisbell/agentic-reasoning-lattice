# Channel Assignment — ASN-0126 review-58

**Date:** 2026-06-09 17:09

## Issue 1: "Properties established" restates P1–P6 already stated at their home sections
Reason: Pure editorial restructuring — the fix removes duplicate glosses and leaves bare name→section pointers, all derivable from the ASN's own structure. No design-intent or implementation evidence bears on whether a navigation slot should re-state properties already proved inline.

## Issue 2: P2's coverage-class conjunct re-derives what "Registration entries" already established
Reason: Both the derivation and its target already live in the ASN; the fix is to keep one copy (in *Registration entries*) and replace P2's second conjunct with a citation. This is internal de-duplication with no dependence on Nelson's intent or Gregory's code.

## Issue 3: Self-referential and redundant back-pointers
Reason: The fix repoints a self-referential cross-reference to the actual locus where precondition (0) is defined (the `K.λ_sh` definition in *The shape-gated emit*) and drops the repeated `(Single-source)` tags after `|e|`'s first introduction — entirely a matter of the ASN's internal cross-referencing.
