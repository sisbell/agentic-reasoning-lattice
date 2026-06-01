# Channel Assignment — ASN-0086 review-157

**Date:** 2026-06-01 05:09

## Issue 1: R0 postcondition prose enumerates downstream consumers
Reason: Internal. The fix is to delete the use-site justification sentence and let the postcondition stand alone — a pure editorial removal derivable from R0's own statement, requiring no design intent or implementation evidence.

## Issue 2: NestedLinkWitness separating-witness deferral repeated across three sites
Reason: Internal. The fix drops the Remark's forward-pointer sentence and lets each definition cite the construction inline; the construction and its two uses are all present in the ASN, so no external input is needed.

## Issue 3: wp Case 1 contains forward-deferral and essay content in a structural slot
Reason: Internal. Removing the cross-deferral parenthetical and the "Non-weakestness" meta-commentary is editorial; Case 1's sufficient-precondition content and load-bearingness argument already stand in the ASN.

## Issue 4: R7a Corollary re-derives the substrate-conforming-layer definition
Reason: Internal. Compressing the proof to a one-sentence membership check against the existing Definition — substrate-conforming layer is purely a restructuring of material already present in the ASN.

## Issue 5: wp Case 2 conjunct K ∈ T_admissible conflates operation-indexing with state-precondition
Reason: Internal. The ASN's own Definition — Emit_K already resolves the ambiguity ("K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation"), so moving `K ∈ T_admissible` into the standing index condition follows directly from the ASN's stated design without external input.
