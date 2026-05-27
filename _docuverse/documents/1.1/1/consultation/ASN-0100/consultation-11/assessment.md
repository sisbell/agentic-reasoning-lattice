# Channel Assignment — ASN-0100 review-11

**Date:** 2026-05-27 15:40

## Issue 1: Case (ii) "forced" inconsistency for V_{s_L}(d) = ∅
Reason: The fix is derivable from the ASN's own definitions — the alternative decomposition with n'_{s_C} < N is already identified by the ASN for the V_{s_L}(d) ≠ ∅ subcase, and the same construction applies to V_{s_L}(d) = ∅. Reclassification or symmetric justification requires only consistency with the ASN's stated definition of "forced".

## Issue 2: S4 misclassified as entity-set invariant
Reason: The fix is derivable from the ASN itself — S4's quantification over dom(C) is fixed by ASN-0036, and the chain-injectivity + freshness reasoning that actually discharges S4 is already established in Effect One. The repair relocates S4 to a content-allocation group and reuses existing in-ASN machinery.

## Issue 3: I3-V disclaimer wording ambiguity
Reason: The fix is a precision tightening derivable from the ASN's own region arithmetic — the coincidence condition k ≤ N − p_m follows directly from the Insertion last-component values {p_m, ..., p_m + n − 1} versus pre-state range {1, ..., N} already worked out in §Arrangement functionality.
