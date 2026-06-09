# Channel Assignment — ASN-0121 review-18

**Date:** 2026-06-09 02:19

## Issue 1: Element-rooted home-set vacuity claim is false for wide spans
Reason: Internal fix. The counterexample uses only T1/T12 (ASN-0034) machinery already cited in the ASN, and the remedy (restrict vacuity to unit-depth subtree spans, keep totality) is derivable from `athome`'s own definition.

## Issue 2: FL-WP(b) increment formula over-attributed to R6b and mis-indexed
Reason: Internal fix. The mis-attribution and indexing correction follow from the exact statement of R6b and the structure of `L_R`/`nullified` already imported from ASN-0086 — no design intent or implementation evidence is at stake, only correct restatement of cited foundation results.
