# Channel Assignment — ASN-0070 review-5

**Date:** 2026-05-25 13:34

## Issue 1: F-canonical Step 2 characterisation argument has a literally-false intermediate claim
Reason: The fix is a purely mathematical rewriting of the reverse-direction proof using T1 (already cited in the ASN) via either induction on position or case-split on divergence positions. The reviewer supplied the exact structural template; no design intent or implementation evidence is required.

## Issue 2: F-multi's subspace conditional is vacuous
Reason: The fix follows directly from F-subspace (proved earlier in this same ASN), which forces `S₁ = S₂ = subspace_I(a)` under the F-multi precondition. The reviewer supplied the corrected wording; the correction is derivable internally.
