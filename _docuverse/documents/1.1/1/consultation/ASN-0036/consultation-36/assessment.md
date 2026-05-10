# Revision Categorization — ASN-0036 review-36

**Date:** 2026-03-28 10:36

## Issue 1: S8a guarded quantification leaves universal V-position well-formedness unstated
Category: INTERNAL
Reason: The fix requires making `v₁ ≥ 1` a universal conjunct (citing T4's positive-component constraint already established in ASN-0034) and aligning the "text-subspace" labels with the actual formal scope — all information is present in the ASN and its dependencies.

## Issue 2: D-SEQ notation is ill-defined at depth m = 1
Category: INTERNAL
Reason: The fix is adding an explicit `m ≥ 2` precondition, which ValidInsertionPosition already requires and the ASN's own derivation already demonstrates is necessary — no external design intent or implementation evidence needed.
