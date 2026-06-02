# Channel Assignment — ASN-0069 review-57

**Date:** 2026-06-02 15:25

## Issue 1: Empty-source trigger condition stated against `d_src` instead of `d_op`
Reason: The fix is a purely internal consistency correction — the ASN already establishes the `d_op` vs `d_src` distinction and the correct keying on `V_{s_C}(d_op)` in V4, V7's formal statement, V0's Effects, and §"The Empty-Source Case"'s opening. The three slips simply contradict the ASN's own established convention; no design intent or implementation evidence is needed.
