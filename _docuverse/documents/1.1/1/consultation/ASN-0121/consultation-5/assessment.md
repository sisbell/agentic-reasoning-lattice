# Channel Assignment — ASN-0121 review-5

**Date:** 2026-06-09 01:30

## Issue 1: The "forced" derivation of FL-DEF has slack — soundness does not exclude nullified links
Reason: The fix is internal — adding the `R ⊆ addressable(Σ)` requirement (or folding addressability into soundness) is a pure restatement of the derivation, using `addressable`/`nullified` already defined in the ASN and Nelson's "not currently addressable" (4/9) already cited. No design-intent or implementation evidence is in question; the omission is a logical gap in the ASN's own argument.

## Issue 2: FL-CUR's biconditional does not follow from FL-SND ∧ FL-CMP alone
Reason: The fix is internal — re-attributing the `a ∈ findlinks ⟹ a ∈ addressable` step to FL-DEF's set-builder (or the strengthened soundness from Issue 1) is a citation correction fully derivable from claims already present in the ASN. No channel needed.
