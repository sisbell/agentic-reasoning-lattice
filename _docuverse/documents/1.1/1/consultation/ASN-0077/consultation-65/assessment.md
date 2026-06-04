# Channel Assignment — ASN-0077 review-65

**Date:** 2026-06-04 13:46

## Issue 1: Form (F2) is introduced and proven equivalent but never consumed
Reason: Purely internal editorial fix — determining whether (F2) is consumed downstream and restructuring the equivalence chain to (F1)≡(F3) requires only reading the ASN's own proofs and claim usages.

## Issue 2: Five claims forward-defer to the operation spec's well-formedness preconditions
Reason: Internal restructuring — hoisting a named `WF_V(Σ, d, σ)` predicate from the six conjuncts already enumerated in "The operation" is a pure reorganization of existing content.

## Issue 3: Cross-subspace I-span behavior is both decided and re-posed as open
Reason: The edge case already settles the I-span behavior (link origins dropped by definition) from the ASN's own content; narrowing the Open Question to the residual part (a unified content-and-link origin operation) is derivable from the existing text without design-intent or implementation evidence.

## Issue 4: Intro and summary state the span-derivation point in duplicate
Reason: Internal anti-bloat trim — deduplicating two passages that make the same claim requires only comparing the ASN's own intro and summary wording.
