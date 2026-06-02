# Channel Assignment — ASN-0047 review-345

**Date:** 2026-06-02 07:38

## Issue 1: SSGU and CrossNodeAccountBase restate the same zero-separator-at-`#N+1` divergence argument in full, joined by a forward reference that does not prevent the restatement
Reason: This is a pure internal restructuring: both proofs already exist in the ASN, SSGU is explicitly the general form, and CrossNodeAccountBase is a strict instantiation (`a = b_account(N₁)`, `a' = b_account(N₂)`). Stating the divergence once and citing it requires no design intent or implementation evidence.
