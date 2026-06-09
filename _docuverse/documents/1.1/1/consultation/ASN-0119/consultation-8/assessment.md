# Channel Assignment — ASN-0119 review-8

**Date:** 2026-06-09 01:01

## Issue 1: P7a's necessity condition for fragmentation is false (and unproven)
Reason: The fix is purely internal — the body already proves the correct characterization ("survives as contiguous precisely when its π-image is again an interval") and supplies the `{A,B}` fragmentation behavior via the existing worked pivot. Reconciling the table with the body and exhibiting the stationary-content example requires only the ASN's own definitions and ASN-0084's permutation equations; no design intent or implementation evidence is at stake.
