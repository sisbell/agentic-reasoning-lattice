# Channel Assignment — ASN-0116 review-57

**Date:** 2026-06-09 21:20

## Issue 1: Partial function `C` applied outside its domain in IP0
Reason: Pure notational fix internal to the ASN — replace `C(shift(a, k))` with the post-allocation `C'(shift(a, k)) = w_k`. The note's own `C`/`C'` convention (I-ALLOC's `C'(shift(a, k)) = w_k`, IP5's domain-guarded `C(M(d')(v'))`) and IP0's already-correct substance (origin-based, value-independent identity) fully determine the correction; no design intent or implementation evidence is at issue.
