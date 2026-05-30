# Channel Assignment — ASN-0043 review-105

**Date:** 2026-05-30 14:26

## Issue 1: L11a recounts GlobalUniqueness's internal proof structure — essay content the reader skips
Reason: The fix is purely editorial — cut the clause recounting GlobalUniqueness's internal induction and keep the single-tree precondition plus the S7d-based 𝒯 discharge, both already present in the ASN. No design intent or implementation evidence is at stake.

## Issue 2: L9's `s_C ≥ 1 / s_L ≥ 1` justification is unused and rests on an existence assumption the precondition does not supply
Reason: Deleting the unused sentence is derivable from the ASN's own witness construction, which needs only `s_X ≥ 1`, `s_X ≠ s_C`, `s_X ≠ s_L` from T0(a) over fixed constants. The precondition (`dom(Σ.M) ≠ ∅`, admitting empty content/link stores) is stated in the ASN itself.

## Issue 3: L0 closing sentence restates the invariant in prose
Reason: Dropping or folding the redundant sentence is a self-contained editorial fix; the formula and the `s_C, s_L` introduction are both already in the ASN. No external channel needed.
