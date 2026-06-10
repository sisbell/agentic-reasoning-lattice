# Channel Assignment — ASN-0126 review-67

**Date:** 2026-06-09 21:01

## Issue 1: `touched` is dead inventory in the worked illustration
Reason: Internal fix. The choice — drop `touched` or exercise it — and the execution are both derivable from the ASN's own content: the Multi shape rule (`|F| = 1`, `|G| < ∞`), C0's coverage-class key-uniqueness (which is exactly what distinguishes a second Multi entry `touched` from `citation`), and the existing `citation` emit pattern together supply everything needed to either remove the entry or write a contrasting `touched` emit. The example types are illustrative constructs of this note, not design commitments or implementation artifacts, so neither Nelson's intent nor udanax-green evidence bears on the fix.
