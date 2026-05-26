# Channel Assignment — ASN-0087 review-7

**Date:** 2026-05-26 13:13

## Issue 1: S4 misattribution in invariant preservation
Reason: The fix is a purely formal re-attribution between two invariants from already-cited dependencies (S4 in ASN-0036 covers content addresses; L11a in ASN-0043 covers link addresses). The frame `Σ'.C = Σ.C` and the existing freshness derivation in the ASN provide everything needed; no design intent or implementation evidence is required.
