# Channel Assignment — ASN-0108 review-2

**Date:** 2026-06-05 04:04

## Issue 1: W9a's termination condition uses "below the cursor" with two contradictory meanings
Reason: Fully internal — the ASN's own definitions fix the direction (`After(c, Σ)` is keys `> κ(c)`; the W6 blind spot is keys `< κ(c)`). Correcting the spatial convention requires only the note's existing claims, no design intent or implementation evidence.

## Issue 2: W6 reconciliation overstates that an address-based key is allocation-monotone
Reason: Fully internal — the body of W6 already scopes append-at-tail to a single home document (T9 `same_allocator`) and the first Open Question already names the multi-document gap. The reconciliation sentence need only be brought into line with claims already present in the note.

## Issue 3: Mandatory boundary cases are not exercised in the concrete walks
Reason: Fully internal — the `m = 0` and `N > m` traces follow mechanically from the existing `Window`/`After` definitions, the W4 induction's base case, and the W9a count formula already stated in the note.
