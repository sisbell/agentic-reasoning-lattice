# Channel Assignment — ASN-0086 review-20

**Date:** 2026-05-17 00:53

## Issue 1: Misnamed reference to S7c
Reason: Pure citation correction — the reviewer has already identified that S7c is ElementFieldDepth (not DocumentArrangementSlot) and that the structural claim properly attaches to L0. The fix is a name substitution derivable from the foundation ASN content; neither design intent nor implementation evidence enters.

## Issue 2: R7 Step 3 conflates the substrate primitive with Emit_K
Reason: The note already distinguishes substrate primitive from Emit_K (see Setup's "Breadth of the primitive vs. the discipline R0a names" and Emit_K's "Why the construction is bound into the definition"). The fix is a logical scoping adjustment using vocabulary the ASN itself has established — fully internal.

## Issue 3: Forcing argument for the shared allocator commitment hand-waves
Reason: The fix is either to tighten the derivation via case-elimination on the foundation invariants (a logical exercise within the ASN's existing axiomatic vocabulary) or to relax the claim's modality from "forced" to "adopted as commitment" (a rewording). Both paths are internal.

## Issue 4: No concrete tumbler-level failure example in "Failure modes"
Reason: The reviewer specifies the exact tumbler value to use (`a' = 1.0.1.0.1.0.2.1.1`) and the L1c chain extension (`inc(a₁, 1)`); the verification follows mechanically from definitions already in the worked sketch. No external input required.

## Issue 5: R0a's antichain corollary's "second zero coincides" phrasing is underspecified
Reason: Pure clarification of an existing argument — the full prefix-agreement step is already implicit in `a' = a · w` and just needs to be made textually explicit. Internal phrasing fix.
