# Channel Assignment — ASN-0110 review-10

**Date:** 2026-06-08 01:22

## Issue 1: RE-reveal's degenerate pairing claim and its example are wrong
Reason: The fix is internal — RE-full and RE-result already establish that only touching slots appear in the result, which is exactly what makes the cited single-touching-link example self-contradictory. Replacing it with a multi-role single-link case and weakening the claim follows directly from the ASN's own definitions.

## Issue 2: RE-anon's "lower bound" is misidentified
Reason: The fix is internal — the counterexample (one arity-3 link with three distinct touching slots) and the correct per-role bound (`|Eᵢ|` lower-bounds distinct links touching via slot `i`) are both derivable from RE-result and RE-witness as already stated. No design intent or implementation evidence is at issue.
