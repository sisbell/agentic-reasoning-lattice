# Channel Assignment — ASN-0110 review-6

**Date:** 2026-06-08 00:57

## Issue 1: V-side reduction relies on `image` being finite, but never establishes it
Reason: The fix is internal — it requires only citing an existing foundation guarantee (S8-fin, ASN-0036; C-fin/S8-fin, ASN-0093) that `dom(Σ.M(d))` is finite, then deriving `image(R, d, Σ) ⊆ ran(Σ.M(d))` finite. The review already supplies the exact citations, and the ASN itself relies on these same foundations elsewhere; no design-intent or implementation evidence is needed.
