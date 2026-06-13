# Channel Assignment — ASN-0123 review-2

**Date:** 2026-06-12 22:48

## Issue 1: V1's consequence gloss overstates content-volume independence
Reason: The fix is a precision correction internal to the ASN — it distinguishes allocation count (zero content/link addresses, one identity; content-volume-independent) from the abstract state delta (`M'(v)` and `ΔR = A × {v}` both scale with the content-position count `n`) from representation-level storage (span count via V2's representation invariance). All three are already articulated in the note: V1's own "`|A| ≤ n`", V2's M3/M11/M12 representation-invariance gloss, and the cited implementation reading; no design intent or new implementation evidence is needed.
