# Channel Assignment — ASN-0120 review-3

**Date:** 2026-06-08 23:04

## Issue 1: Resolution's containment `ρ(R, Σ) ⊆ dom(Σ.C)` is not discharged for partial spans
Reason: The fix is a formal repair internal to the ASN — strengthen the spec-set precondition so each `ℓ_j` is an ordinal displacement `δ(n_j, m)` (or add `subspace(v) = s_C` to `ρ`'s filter) and then derive containment from S3★ explicitly. All needed machinery (T12, `actionPoint`, ordinal displacement, S3★) is already cited in the ASN; this is a definitional confinement step, not a question of design intent or implementation behavior.

## Issue 2: `enabled(makelink)` omits source-document definedness
Reason: Purely a formal completeness fix derivable from the ASN's own definitions — either fold "all source documents of `R₁, R₂, R₃` are allocated" into `enabled(makelink)`, or declare source-document allocation a well-formedness presupposition of valid spec-set arguments. No design intent or implementation evidence is required to close the gap.
