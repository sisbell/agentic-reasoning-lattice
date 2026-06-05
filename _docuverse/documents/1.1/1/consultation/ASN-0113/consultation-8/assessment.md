# Channel Assignment — ASN-0113 review-8

**Date:** 2026-06-05 00:48

## Issue 1: W10's full-generality claim rests on a derivation that only covered one depth
Reason: The fix is internal — the corrected derivation (a two-line T1 argument on the first component over arbitrary-depth `t`) is already sketched in the review itself and rests only on T1, `start_S`, and `reach`, all defined in the ASN. No design intent or implementation behavior is at issue.

## Issue 2: The parenthetical characterization of the denotation's tumblers is false
Reason: The fix is internal — correcting the false `zeros = 0` claim and re-grounding disjointness in `t₁ = S` (Issue 1's argument) plus SC-NEQ uses only T1-interval semantics and the subspace convention already in the ASN. No external channel needed.
