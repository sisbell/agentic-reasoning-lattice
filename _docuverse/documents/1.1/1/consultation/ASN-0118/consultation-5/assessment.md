# Channel Assignment — ASN-0118 review-5

**Date:** 2026-06-08 21:57

## Issue 1: Displacing-case decomposition does not discharge CP6 for the link subspace
Reason: The fix is a formal reconciliation of the K.μ⁻ per-subspace semantics (already cited from ASN-0047) with CP6's existing frame; stating `n'_{s_L} = n_{s_L}` is derivable from the ASN's own decomposition and cited primitives. No design intent or implementation evidence is at stake.

## Issue 2: Worked example does not exercise CP8, the most intricate postcondition
Reason: Extending the worked example to classify the resolved addresses against `d`'s pre-state range and exhibit a range-new vs. already-referenced split is a numeric instantiation of CP8's existing derivation. Fully internal to the ASN.
