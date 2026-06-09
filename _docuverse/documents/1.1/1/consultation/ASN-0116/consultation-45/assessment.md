# Channel Assignment — ASN-0116 review-45

**Date:** 2026-06-09 12:08

## Issue 1: The `k = 0` boundary of the shift indexing is unaccounted for
Reason: Internal fix. The required correction is to cite the existing convention `shift(t, 0) := t`, which the review itself locates in foundations the note already builds on (ASN-0036 S8, ASN-0058 OrdinalShiftBase); this is a mechanical notational citation requiring neither design intent nor implementation evidence.

## Issue 2: The "position-based reader" J1'★ aside describes an impossible violation
Reason: Internal fix. The correction is derivable from the ASN's own state definition (provenance is `(I-address, document)` pairs, `Σ.R ⊆ T_elem × E_doc`, carrying no V-position) together with the composite-boundary invariants of ASN-0047 already invoked at the pre-state; restating the aside needs no design intent or implementation evidence.
