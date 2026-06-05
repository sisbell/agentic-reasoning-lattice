# Channel Assignment — ASN-0100 review-89

**Date:** 2026-06-05 06:28

## Issue 1: Post-insertion shift and its invariant-preservation lemmas are re-derived instead of inherited from ASN-0082's I3 family
Reason: The fix is structural reorganization — match M'(d) to I3's post-insertion arrangement and invoke the I3-* family, or explicitly scope the re-derivation to the intermediate-state atomicity need. Neither design intent nor udanax-green evidence bears on this; whether ASN-0082's I3 family applies is settled by the foundation ASN's own content, not by Nelson or Gregory.

## Issue 2: Cross-document projection invariance is proven twice by the same argument
Reason: Pure de-duplication — have §Cross-document independence cite INS.proj's d' ≠ d case instead of re-running the LP4-composition argument. Entirely internal to the ASN's existing content.
