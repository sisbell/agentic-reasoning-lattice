# Channel Assignment — ASN-0126 review-53

**Date:** 2026-06-09 13:37

## Issue 1: The standard-triple shape of every stored value is presupposed but never established
Reason: Internal. Every element the fix needs is already in the note — precondition (0) on `K.λ_sh` ("the emitted value is a standard triple — arity 3"), the base `Σ_init.L = ∅`, and L12/P1/P4 already cited in P6's proof. Adding the standard-triple conjunct to P3's claim and P6's IH and citing (0) is pure proof bookkeeping over content already present; no design intent or implementation evidence is at stake.

## Issue 2: the no-image conclusion is derived twice in Single-source
Reason: Internal. This is a pure anti-bloat restructuring — replace para 3's re-derivation of the Nullify no-image conclusion with a back-reference to para 2's general claim and drop the connective sentence. No semantic claim changes and the Nullify definition is already cited from ASN-0086, so neither channel is implicated.
