# Channel Assignment — ASN-0108 review-11

**Date:** 2026-06-05 05:10

## Issue 1: W6a's "Regardless of key" universal is broader than its proof
Reason: The fix is internal — the ASN already contains the narrower scope the proof discharges (keys that are functions of `(address, matched-content-position)`), and W0's admission of arbitrary injective keys is stated in the note itself. Restricting the W6a heading to match its own body requires no design intent or implementation evidence; the conflict is between two passages already present.
