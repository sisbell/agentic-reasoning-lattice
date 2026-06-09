# Channel Assignment — ASN-0120 review-13

**Date:** 2026-06-09 11:56

## Issue 1: Load-bearing spec-set well-formedness is not part of the formal precondition
Reason: The fix is reorganizational — the conditions (content-subspace, depth `m`, ordinal displacement, `d_j ∈ dom(Σ.M)`) are all already stated in the ASN's spec-set definition; the task is to lift them into the `enabled`/precondition surface and qualify the ML1 row. Derivable from the ASN alone.

## Issue 2: Defensive scope-justification prose around the type restriction
Reason: Pure prose trimming — the substantive restriction is already proven as a consequence of ML1/ML3 within the ASN; removing the "not an oversight" defense and direct-address narration needs no external evidence.

## Issue 3: Repeated "this is implementation, not an abstract claim" disclaimer tails
Reason: Editorial deduplication of disclaimer tails (and the `do2.c` line citations) entirely within the author's control; no design-intent or implementation question is at stake.

## Issue 4: Counterexample motivates a precondition the precondition already excludes
Reason: Reducing the escape example to a one-clause justification is internal restructuring; the load-bearing T5 confinement derivation already present in the ASN is what remains.
