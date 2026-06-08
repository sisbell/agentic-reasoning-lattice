# Channel Assignment — ASN-0111 review-31

**Date:** 2026-06-08 13:05

## Issue 1: RL-REP is downstream-interpretation essay, not a READLINK guarantee
Reason: Internal. The fix is a scope/prose reduction: RL1 already fixes the verbatim return, and the downstream consumers (FOLLOWLINK, type-matching) are explicitly out of scope, so trimming RL-REP to a one-line pointer requires no design intent or implementation evidence.

## Issue 2: RL1's formal predicate is weaker than the claim and than the definition
Reason: Internal. The operation is defined as `readlink(a, Σ) = Σ.L(a)`; restating RL1 as componentwise equality `readlink(a, Σ).eᵢ = Σ.L(a).eᵢ` is derivable directly from that definition with no external input.

## Issue 3: RL0 weakest-precondition postcondition references the partial function off its domain
Reason: Internal. Rephrasing the postcondition to avoid dereferencing `Σ.L(a)` off-domain is a well-formedness fix on the note's own logic, fully derivable from the existing definition and RL0.
