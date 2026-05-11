# Channel Assignment — ASN-0036 review-88

**Date:** 2026-05-11 03:34

## Issue 1: S7a–S7d contracts implicitly assume T4-validity of `a ∈ dom(Σ.C)` but their Depends lists do not make this transparent
Reason: The fix is a contract-metadata adjustment — adding T10a.4 (and S0 where relevant) to Depends lists, or strengthening the axioms to state T4-validity explicitly. Both options are derivable from the ASN's existing content and its already-cited ASN-0034 foundations; no design intent or implementation evidence is needed.
