# Channel Assignment — ASN-0051 review-64

**Date:** 2026-05-17 17:57

## Issue 1: K.μ~ composite admissibility not addressed in "After reordering" subsection
Reason: Fix is derivable from the ASN — the parallel admissibility treatment already appears in the later "Reordering that changes locate" subsection and can be mirrored (or cross-referenced) without external input.

## Issue 2: Construction-pattern generalisations lack at least one explicit higher-(m, p) witness
Reason: Fix is derivable from the ASN — the mechanical construction recipe (nested re-mappings with `min_k n_k ≥ 2m − 1`, single-element spans at odd offsets) is already described; instantiating it at (m=4, p=3) is a routine application requiring no design intent or implementation evidence.

## Issue 3: Consumer note conflicts with SV13(h)'s use of BilateralVitality
Reason: Pure editorial reconciliation between two passages within this ASN; the resolution (reword the Consumer note to acknowledge SV13(h) as the internal site) is determined by the ASN's own content.

## Issue 4: Architectural remark's per-transition check doesn't explicitly cover K.μ~ as composite
Reason: Fix is derivable from the ASN — the K.μ~ composite structure (K.μ⁻ + K.μ⁺, both M-only) and the inheritance argument are already established elsewhere in the note; the parenthetical merely makes the inheritance explicit at the point of use.
