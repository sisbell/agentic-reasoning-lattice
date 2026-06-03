# Channel Assignment — ASN-0071 review-46

**Date:** 2026-06-03 09:41

## Issue 1: "interior-action-point rejection" names a case the ASN neither defines nor demonstrates
Reason: Internal. The vspec preconditions (`actionPoint(ℓ) = #u ≥ 2`) and F-FILT's silent-filtering behavior are both fully specified within the ASN; whether an interior action point is excluded by the precondition (and that filtering ≠ rejection) is derivable from the ASN's own definitions without design intent or implementation evidence.

## Issue 2: "why the axiom is needed" meta-prose around S3★-aux
Reason: Internal. The required fix is a pure prose collapse to the bare entailment `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` by S3★ ∧ S3★-aux; both axioms are already cited and the substantive logic is unchanged.

## Issue 3: interpretive essay content in a derivation slot
Reason: Internal. The fix is simply to delete the interpretive framing sentence and let F-FILT carry the operative claim, which it already does — no external content needed.
