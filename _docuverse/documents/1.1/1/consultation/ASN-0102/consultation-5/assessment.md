# Channel Assignment — ASN-0102 review-5

**Date:** 2026-05-28 14:53

## Issue 1: ExtendedReachableStateInvariants discharge omits S8★ and S4
Reason: S8★ (PerSubspaceSpanDecomposition) and S4 (OriginBasedIdentity) are foundational conjuncts of ASN-0047, the reference base the note already works against and quotes; the witnesses (post-state functional, finite, contiguous, common-depth `m` via X16; `dom(Σ'.C)=dom(Σ.C)` via X1) are all present in the note. The fix is to add the two discharges from material already in hand — no design-intent or implementation evidence is required.

## Issue 2: S8a established only for copied positions, not displaced positions
Reason: The required citation is OrdShiftHom (c) from ASN-0058 (shift preserves S8a unconditionally; `#shift(u,W)=#u=m`), a foundational lemma the note already relies on; discharging S8a/depth for the displaced class is one citation, derivable from the ASN's own reference base.

## Issue 3: X8 descends into implementation mechanics beyond the abstract guarantee
Reason: The abstract claim (constructed `k`, canonical `≤ k`, equality iff no inter-reference boundary is I-adjacent) is already established in the note and grounded in M7/M12/M16 from ASN-0058; the required action is to reduce X8 to that claim and excise or relocate the POOM/spanfilade divergence — a scoping/editorial fix derivable from the note's own abstract-vs-implementation distinction.
