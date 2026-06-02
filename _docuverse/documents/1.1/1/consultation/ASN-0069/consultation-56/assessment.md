# Channel Assignment — ASN-0069 review-56

**Date:** 2026-06-02 15:24

## Issue 1: V6a (link discoverability inheritance) is derived against `d_src`, not `d_op`
Reason: The fix only propagates the `d_op` operand convention that V4, V4b, V8, and V12(d) already establish in this ASN; restating V6a(iii) and its ⊆/⊇ derivation against `d_op` (reducing to `d_src` when `d_op = d_src`) is mechanical and internal.

## Issue 2: Empty-source branch and V4/V8 vacuity conditioned on `V_{s_C}(d_src)` instead of `V_{s_C}(d_op)`
Reason: V0's dispatch and the section opening already test `V_{s_C}(d_op) = ∅`; the fix substitutes `d_op` for `d_src` in the two stray passages to match, fully derivable from the ASN's own operand convention.
