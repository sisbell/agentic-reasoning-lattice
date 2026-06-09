# Channel Assignment — ASN-0116 review-6

**Date:** 2026-06-08 21:01

## Issue 1: Inserted content values are never typed in the precondition
Reason: Internal fix. The ASN already cites K.α (ASN-0093) whose contract requires `v ∈ Val`, and the Effect writes `C'(shift(a,k)) = w_k`; adding `(A k : 0 ≤ k < n : w_k ∈ Val)` simply surfaces the value-well-formedness obligation the composite already depends on. No design intent or implementation evidence is needed.
