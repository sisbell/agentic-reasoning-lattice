# Channel Assignment — ASN-0036 review-97

**Date:** 2026-05-11 13:31

## Issue 1: `subspace(v)` function lacks a Formal Contract entry parallel to `subspace_I(a)`
Reason: The fix is a structural documentation addition that mirrors an existing pattern in the ASN (`subspace_I(a)`'s Formal Contract under S7c). All preconditions, definition, and postconditions are derivable from S8a and OrdShiftHom already present in the ASN.

## Issue 2: D-SEQ Step 3 quantifies over "any integer k" but the carrier is ℕ
Reason: This is a terminological precision fix internal to the proof. The ASN already establishes the ℕ carrier via T0 (ASN-0034) and the proof's S8a check requires k ≥ 1, so the correction is mechanical.
