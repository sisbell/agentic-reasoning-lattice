# Channel Assignment — ASN-0045 review-15

**Date:** 2026-05-28 19:55

## Issue 1: Per-predicate Depends lists cite premises that do no work in the predicate's own postcondition
Reason: Internal fix. The bound `zeros(t) ≤ 3` and T4c's role are already adjudicated by the ASN's own Well-Definedness section ("T4c's injectivity ... does no work here"); stripping the extraneous citations and annotating T4c as label-only is a bookkeeping correction derivable from the proofs already present.

## Issue 2: `T4-valid(t)` used as a named predicate the foundation never defines
Reason: Internal fix. The four T4 clauses (zeros ≤ 3, no adjacent zeros, t₁ ≠ 0, t_{#t} ≠ 0) are already specified in T4 (ASN-0034); pinning `T4-valid(t)` to their conjunction is a definitional restatement, not a question about design intent or implementation behavior.
