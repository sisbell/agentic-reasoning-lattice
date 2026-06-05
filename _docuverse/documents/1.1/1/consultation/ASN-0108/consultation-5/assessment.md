# Channel Assignment — ASN-0108 review-5

**Date:** 2026-06-05 04:22

## Issue 1: The offset-cursor weakest precondition is stated strictly stronger than the genuine weakest
Reason: The fix is a purely formal correction derivable from the ASN's own definitions of `After`, `Window`, and `κ` — replacing the membership-identity condition with the count-at-cut condition `|{a ∈ Match(q,Σ') : κ(a) ≤ κ(c)}| = j` and verifying it via the supplied counterexample requires no design intent or implementation evidence.
