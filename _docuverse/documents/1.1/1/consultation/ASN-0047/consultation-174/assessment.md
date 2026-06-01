# Channel Assignment — ASN-0047 review-174

**Date:** 2026-05-31 21:43

## Issue 1: Three-step replacement worked example uses a concrete address whose origin contradicts the variant's premise
Reason: Internal fix — the contradiction is mechanical: `origin(1.0.1.0.1.0.1.5)` computes to `d` by T4b's projection, and the structural unreachability of `(aₓ, d) ∉ R` for a d-origin address follows from this ASN's own J0/J1★ coupling. Selecting a foreign-origin literal and splitting the pre-state is derivable from the ASN alone.

## Issue 2: The K.δ k=0 freshness discharge is forward-deferred three times to the same section
Reason: Internal fix — this is an editorial deduplication of three forward pointers to one downstream section; no design intent or implementation evidence bears on which pointer to keep.
