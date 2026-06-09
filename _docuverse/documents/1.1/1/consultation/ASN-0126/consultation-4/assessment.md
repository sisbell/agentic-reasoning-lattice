# Channel Assignment — ASN-0126 review-4

**Date:** 2026-06-08 21:20

## Issue 1: R-as-Multi contradicts the unit-depth retraction discipline the note claims to inherit unchanged
Reason: The choice between (a) registering R as Binary or (b) relaxing the discipline turns on whether retracting multiple targets in one operation is a real capability the substrate must express — a design-intent question for Nelson — and whether the implementation ever batches targets in a single retraction — an evidence question for Gregory. The note's own content fixes the contradiction but not which branch to take.
Nelson question: Was retraction designed to address a single target per operation, or is retracting several targets in one operation an intended capability?
Gregory question: In udanax-green, does a retraction/delete record a single to-span, or can one retraction tuple carry multiple target spans?

## Issue 2: No weakest-precondition derivation for the shape-gated emit
Reason: Deriving `wp(Emit under →_sh, (a,F,G) ∈ A_K^{Σ'})` is a purely formal exercise over `K.λ_sh`'s stated preconditions and ASN-0086's already-inherited Case-2 wp; everything needed is present in this note and its cited parent.
