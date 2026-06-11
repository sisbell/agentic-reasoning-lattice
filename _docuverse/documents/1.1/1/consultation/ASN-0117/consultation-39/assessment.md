# Channel Assignment — ASN-0117 review-39

**Date:** 2026-06-11 03:04

## Issue 1: J1★ discharge contains a claim falsified by the ASN's own sharing analysis, and covers only half the post-state range
Reason: The fix is internal. The correct distinction (`A_del^{excl}` versus `A_del`) is already established in the ASN's own wp section and within-document-sharing example, and the missing `M(d)(L)` summand is discharged by DEL-LEFT, which the ASN already states — the repair is a matter of restating the J1★ argument consistently with material already present, not of consulting design intent or implementation behavior.

## Issue 2: DEL-CFRAME's discharge is stated twice with identical justification
Reason: This is a purely editorial defect — a duplicated derivation that must be consolidated into one location with the contract clause pointing to it. No semantic question about design intent or implementation evidence is involved.
