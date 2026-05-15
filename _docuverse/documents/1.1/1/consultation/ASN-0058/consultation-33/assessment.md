# Channel Assignment — ASN-0058 review-33

**Date:** 2026-05-14 23:33

## Issue 1: M12's "two partitions coincide" step is implicit
Reason: The fix is a one-paragraph set-theoretic argument using B1, M12a, and M12b — all properties already established in the ASN. No external evidence needed.

## Issue 2: M12b's case analyses rely on block distinctness without establishing it
Reason: The reviewer provides the exact derivation needed, citing M0 (in this ASN) and TS4 (ASN-0034, already referenced throughout). Entirely internal proof-structure fix.

## Issue 3: M16a's structural decomposition relies implicitly on T4-validity of `a` and `a + k`
Reason: The fix is to cite the T10a + T10a.4 + S7d chain from ASN-0034/0036. These are existing axioms in the foundation; the issue is a missing citation, not missing knowledge.

## Issue 4: The forward inclusion `V(βⱼ) ⊆ [vⱼ, shift(vⱼ, nⱼ))` in M2 does not separately verify `vⱼ + k ∈ dom(M(d))` for `k = 0`
Reason: The fix is to make explicit that S8(b) at index 0 gives `vⱼ ∈ dom(M(d))` — purely a proof-presentation issue using ASN-0036's S8 as already cited.
