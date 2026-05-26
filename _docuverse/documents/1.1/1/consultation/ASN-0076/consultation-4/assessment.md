# Channel Assignment — ASN-0076 review-4

**Date:** 2026-05-25 20:21

## Issue 1: Numerical error in element-level address minimum length
Reason: Fix is internal — the reviewer derives the correct bound (≥ 8) directly from L1, L1b, and T4 already cited in the ASN, and the worked example exhibits it. No design intent or implementation evidence is needed.

## Issue 2: E0 supersession step elides the max-recovery argument
Reason: Fix is internal — the reviewer specifies the two available paths (split into sub-cases, or cite T10a.7's EnumerationInjectivity), both grounded in foundation citations already in scope. This is a proof-completion issue within the ASN's own reasoning.
