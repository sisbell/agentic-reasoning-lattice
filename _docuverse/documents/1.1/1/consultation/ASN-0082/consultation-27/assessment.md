# Channel Assignment — ASN-0082 review-27

**Date:** 2026-05-15 09:37

## Issue 1: D-DP(a) proof skips the R = ∅ case
Reason: Fix is a proof-structure case split derivable from the ASN's own definitions — Q₃ = ∅ when R = ∅ by Q₃'s definition, and D-SEP(b)'s R ≠ ∅ scoping is already stated in the ASN. No design intent or implementation evidence needed.

## Issue 2: I3-S2 wp Case 1's "contrapositive" reasoning conflates two transformations
Reason: Fix is a correction in proof framing — TS2 is already cited, and the correct discharge (assume equality, apply TS2, conclude by reflexivity) is derivable from the lemma the ASN already invokes. No external channels needed.

## Issue 3: Worked-example verification lists for contraction omit D-DP
Reason: Fix is to add D-DP tick-marks to existing worked examples; D-DP is defined in the ASN and its evaluation at boundary cases (Q₃ = ∅, L ∩ Q₃ = ∅ trivially) follows from definitions already present. No external channels needed.
