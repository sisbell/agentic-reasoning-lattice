# Channel Assignment — ASN-0036 review-199

**Date:** 2026-05-30 00:29

## Issue 1: Internal inconsistency in S5's two constructions
Reason: The fix is a wording change derivable from the ASN's own "Shared facts" paragraph, which already establishes S0/S1 as transition-level and names S2, S3 as the only standalone obligations. No design intent or implementation evidence is needed.

## Issue 2: "Vacuously" misused for the length-1 run
Reason: The correction is a logical-terminology fix fully determined by the ASN's own convention `shift(t,0):=t` and the range of `k` at `n=1`. Derivable internally.

## Issue 3: OrdShiftHom cited for `i = 0`, outside its precondition
Reason: OrdShiftHom's precondition `n ≥ 1` and the S8a membership of `v ∈ dom(M(d))` are both stated within the ASN, so the citation split is derivable from existing content.

## Issue 4: S5's transition-level point stated twice (reviser drift)
Reason: Removing the duplicated restatement is a purely editorial deduplication using the ASN's own text; no external channel is required.
