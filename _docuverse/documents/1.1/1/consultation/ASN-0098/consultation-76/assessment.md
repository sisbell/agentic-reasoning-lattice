# Channel Assignment — ASN-0051 review-76

**Date:** 2026-05-17 22:48

## Issue 1: SV13 clause (i) bundles four distinct system-level facts
Reason: Pure structural reformatting — splitting prose into labelled sub-bullets. All content (SV7, SV9, SV10, SV14) already exists in the ASN; no design intent or implementation evidence required.

## Issue 2: The W(2, 2) explicit witness is structurally orphaned from the lift family
Reason: Editorial choice between two equally valid SV11-attaining witnesses, both already verified in the ASN. The decision is about presentational uniformity of the witness catalogue, derivable from the ASN's own structure.

## Issue 3: Cross-origin exclusion subsection in the Worked Example uses tumblers disjoint from the rest of the example
Reason: Presentational continuity within the worked example. The SV6 verification is already correct; the fix is either to rebuild on existing tumblers (mechanical exercise on the ASN's own definitions) or to retitle the subsection.

## Issue 4: The "degenerate" After-reordering subcase in the Worked Example is acknowledged but not removed
Reason: Self-acknowledged redundancy — the ASN's own prose labels the subsection as degenerate. Removing or folding it is an internal editorial choice with no external dependencies.

## Issue 5: The W(1, p ≥ 4) construction recipe contains two schedules and the relationship is ambiguous
Reason: The construction recipes and their correctness are fully developed in the ASN; the fix is to align the (m=1, p=4) explicit construction with the offset-1 schedule (or drop the inductive framing). Mechanical reorganisation of existing content.
