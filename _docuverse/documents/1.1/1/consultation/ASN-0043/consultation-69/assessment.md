# Channel Assignment — ASN-0043 review-69

**Date:** 2026-05-14 19:05

## Issue 1: L9 proof's content-side subspace argument is unsupported by L0
Reason: The fix is derivable from the ASN's own content. L0a already documents the s_C-residence scoping question, and the Required text gives two viable options (precondition or construction revision); choosing option (a) aligns L9's scope with L0a's existing treatment, requiring no external evidence.

## Issue 2: L11a Case (i) — unjustified length equality of homes
Reason: Purely a proof correction internal to the ASN. The Required fix invokes T4b's unique parse (ASN-0034) — a contrapositive that needs no design intent or implementation evidence.

## Issue 3: Worked example's L9 verification recycles the unsound L0 argument
Reason: Derivable from the ASN alone. The example's stores are concretely enumerated, so direct application of T7 to the listed addresses suffices; no Nelson or Gregory input needed.
