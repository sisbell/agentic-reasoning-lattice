# Channel Assignment — ASN-0051 review-73

**Date:** 2026-05-17 21:50

## Issue 1: SV5 proof reads to "composite endpoints" but worked example treats K.μ~ steps atomically without traceable intermediate verification
Reason: The fix derives the minimal upward-tail K.μ⁻ cut from the bijection ψ's altered V↦I positions, which is mechanical from the K.μ~ definition in ASN-0047 already cited in the ASN. Internal.

## Issue 2: SV11 m·p attainment biconditional - "no two non-empty terms within a block ordinally adjacent or overlap" needs sharper statement
Reason: Definitional sharpening of "non-adjacent" (gap ≥ 1) and "non-overlapping" (disjoint offset ranges) — both already used implicitly in the proof. Internal.

## Issue 3: SV6's case-(ii) of T4-validity check for t at boundary (k-1, k)
Reason: Rewording for clarity of a correct argument; the new phrasing uses the same field-separator ordering p₁ < p₂ < p₃ already established. Internal.

## Issue 4: SV11 (m = 1, p ≥ 4) recipe size-≥3 invariant bound
Reason: Algebraic rephrasing of the existing `i ≤ p` bound to match the `p−1` excision count. Internal.

## Issue 5: SV13(e) bullet on K.μ~ - "composite-level" π-invariance vs locate-set non-preservation needs clearer separation
Reason: Reorganization of an existing bullet into separate sub-bullets for π and locate; both contents are already in SV5/SV5b. Internal.

## Issue 6: ASN length and SV11 witness proof exhaustiveness
Reason: Consolidation of the four lift recipes into a single explicit lemma form referencing parameter deltas and biconditional preservation already verified per-lift. Internal.

## Issue 7: Worked Example V-positions unspecified
Reason: Explicit V-position values [s_C, k] follow from S8a (ASN-0036) and the standard D-MIN form (ASN-0047), both already cited. Internal.

## Issue 8: Withdrawn-labels (SV0, SV1, SV12) provenance
Reason: Editorial consolidation of revision history already distributed across the Properties Introduced section. Internal.

## Issue 9: SV11's "term cardinality inflation" identity is witness-specific but the scope of that witness-specificity could be sharper
Reason: Clarifying sentence about the structural identity's generality; the counting argument is already supplied in the ASN's text. Internal.
