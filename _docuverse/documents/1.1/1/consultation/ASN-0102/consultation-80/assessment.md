# Channel Assignment — ASN-0102 review-80

**Date:** 2026-06-08 03:30

## Issue 1: J1'★ discharge conflates COPY's post-state residency (Σ') with the closing-boundary residency (Σ_clo) the coupling requires
Reason: The fix is internal — it concerns correctly scoping the proof's own coupling argument (BD-New is a `Σ_clo` property defined relative to `B`, SL establishes only `Σ'` residency). Both required remedies (scope COPY as the closing/standalone step, or separate local Σ'-residency from the composite-wide Σ_clo obligation) are restructurings derivable from the ASN's own definitions of `New`, SL, BD-New, and the composite-wide couplings; neither design intent nor implementation evidence is needed.
