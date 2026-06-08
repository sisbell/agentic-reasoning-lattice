# Channel Assignment — ASN-0102 review-72

**Date:** 2026-06-08 02:51

## Issue 1: Duplicated "natural framing" prose across two sections
Reason: Internal edit — both passages already exist in the ASN; the fix removes the redundant re-explanation in the example, keeping the `B = Σ` framing stated once in X14. No design intent or implementation evidence is needed.

## Issue 2: PC3 explains *why* the subspace choice is made rather than *what* it is
Reason: Internal edit — the store-disjointness justification and forward-pointer are already redundant with the wp computation present in the ASN; reducing PC3 to the bare choice needs nothing external.

## Issue 3: Implementation-essay sentence in X14's structural conclusion
Reason: Internal edit — the load-bearing point ("recorded against the destination, not the creator") is already stated in the preceding permanence sentence; dropping or folding the implementation narration requires no new evidence from Gregory.
