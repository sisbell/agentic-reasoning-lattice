# Channel Assignment — ASN-0084 review-36

**Date:** 2026-05-15 16:29

## Issue 1: REARRANGE operation not explicitly defined
Reason: The fix is purely structural — add an Operation specification block tying R-PRE, postcondition clauses, and frame conditions together. All referents (R-PRE, PivotPostcondition, SwapPostcondition, R-FRAME-P/S) already exist in the ASN.

## Issue 2: S8 corollary preservation not addressed in R-WP
Reason: The fix invokes ASN-0036's S8 corollary, S7b/S7c (already audited as preserved via C' = C), and ShiftPreservation (cited elsewhere). All material is in the existing dependency chain.

## Issue 3: R-PPERM/R-SPERM surjectivity citation is imprecise
Reason: Internal proof bookkeeping — either spell out the image-coverage argument (using ordinal arithmetic already established) or invoke finite-set injectivity-implies-surjectivity. No external context required.

## Issue 4: R-BLK as both lemma and function
Reason: Purely expository — adding a clarifying sentence about R-BLK's dual role as lemma-and-procedure. The constructive Phases 1–3 are already specified in the ASN body.

## Issue 5: ArrangementRearrangement definition not labeled
Reason: Pure formatting fix — add a "Definition — ArrangementRearrangement" header to match the style of CutSequence, RegionPartition, etc. No semantic question.

## Issue 6: Multiplicity preservation derivation terse
Reason: Internal proof completion — both set inclusions follow from the defining property M'(d)(π(v)) = M(d)(v) plus bijectivity of π, both already stated in the ASN.

## Issue 7: Phase 1 "outside" case explanation could be sharper
Reason: Restructuring the chained argument into three explicit steps using CS2, R-PRE(iv), and S8 — all already cited in the existing one-sentence form. Internal exposition only.
