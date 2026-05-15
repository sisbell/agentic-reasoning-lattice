# Channel Assignment — ASN-0084 review-26

**Date:** 2026-05-15 11:51

## Issue 1: Width-ordinal relationship is implicit but load-bearing throughout the proofs
Reason: The fix is derivable from the ASN's own content — the corollary follows from R-PRE(iv) and D-SEQ (ASN-0036), both already cited. The review provides the exact derivation; this is internal restructuring.

## Issue 2: TS2 precondition #a₁ = #a₂ elided in canonical decomposition (b)
Reason: The fix is a textual expansion of an already-cited ASN-0034 property (OrdinalShift's length preservation). The review supplies the explicit two-step derivation; no external channel is required.

## Issue 3: Misleading hedge in canonical decomposition (b), n_1 = n_2 sub-case
Reason: The fix is purely internal — the existing proof structure (k_c ≥ 1 from the contradiction assumption, n_b ≥ 1 from S8) supports removing the spurious hedge. The review provides the exact corrected phrasing.

## Issue 4: "Case v₁ < v₂ is symmetric" without explicit reflection
Reason: The fix is a one-line clarification about which run gets backward-extended in the symmetric reflection. Fully derivable from the existing proof; the review supplies the replacement text verbatim.
