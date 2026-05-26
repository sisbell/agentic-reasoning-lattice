# Channel Assignment — ASN-0087 review-9

**Date:** 2026-05-26 13:43

## Issue 1: L1c chain uniqueness claim has gaps in the argument
Reason: The fix is purely formal — it requires either weakening the claim to existence (which is what L1c demands) or supplying a per-step enumeration over TA5a's branching choices using the already-cited axioms (TA5a, SubAllocatorAxiom, SubspaceConventionAxiom). No design intent or implementation evidence is needed.

## Issue 2: Σ_mid invariant preservation bundles 8 invariants under "same reasoning"
Reason: This is a presentation issue with the per-invariant breakdown already sketched in the review itself. K.λ's precondition and frame are already stated in the ASN; expanding the bundled sentence into explicit per-invariant lines is internal mechanical work requiring neither design intent nor implementation evidence.
