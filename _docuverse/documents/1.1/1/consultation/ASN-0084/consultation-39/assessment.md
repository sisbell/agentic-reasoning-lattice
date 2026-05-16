# Channel Assignment — ASN-0084 review-39

**Date:** 2026-05-15 17:47

## Issue 1: R-NS(NS-inv) catalog conflates non-S-applicable invariants with subspace-S-specific ones
Reason: The fix is purely structural reorganization of the (NS-inv) catalog. The ASN itself already separates the justification — its earlier "Invariant preservation" paragraph treats D-CTG, D-CTG-depth, D-MIN, D-SEQ as dom-only invariants preserved globally by dom(M'(d)) = dom(M(d)). The reviser need only split the catalog into "preserved by dom-preservation" vs. "preserved by non-S restriction" sub-lists, with both arguments already present in the ASN.

## Issue 2: R-WP S8(a) discharge implicitly relies on R-COMM for run contiguity but doesn't cite it
Reason: The fix is to add a citation that mirrors the existing R-COMM usage in the S8(b) discharge two paragraphs below. R-COMM is already proven in this ASN, and the Phase-1-runs-lie-in-one-region property is already established by R-BLK Phase 1. The argument is fully derivable from material already in the ASN.

## Issue 3: R-WP omits S7 (StructuralAttribution) from its invariant catalog
Reason: The fix is editorial — add S7 to the catalog with a one-line preservation note. The issue itself states S7's content (origin(a) invariance across states where a ∈ dom(Σ.C)) and its preservation argument (C' = C plus origin(a)'s structural dependence on a, which the ASN already establishes through S4 and S7a–S7d preservation under C' = C).

## Issue 4: Necessity sketch addresses only one conjunct of R-PRE
Reason: The fix is either (a) construct one additional counterexample using the construction-step machinery already in the ASN (R-PIV/R-SWP's well-definedness steps identify exactly which conjunct guards which construction step), or (b) trim the over-promising claim to characterize the sketch as a single load-bearing example. Both options are internal editorial choices fully supported by content already in the ASN.
