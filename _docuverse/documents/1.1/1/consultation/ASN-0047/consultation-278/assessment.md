# Channel Assignment — ASN-0047 review-278

**Date:** 2026-06-01 19:11

## Issue 1: The fork k=0/k=1 allocation discrimination is stated three times
Reason: Pure editorial deduplication — consolidating the allocation discipline and operand-tracking rule to Definition (Fork) and replacing the J4 intro and step (i) restatements with references is entirely derivable from the ASN's own structure.

## Issue 2: K.μ⁻ precondition `dom(M(d)) ≠ ∅` is implied by the strict-contraction clause
Reason: The entailment (`n'_S < n_S ⟹ n_S ≥ 1 ⟹ V_S(d) ≠ ∅ ⟹ dom(M(d)) ≠ ∅`) is internal logic; dropping or folding the redundant conjunct needs no external evidence.

## Issue 3: Notation-section asserts a result it cannot yet support
Reason: Demoting the forward-pointer to a pure reference (the correspondence is already correctly derived at S3★) is an internal cross-reference fix requiring nothing beyond the ASN.
