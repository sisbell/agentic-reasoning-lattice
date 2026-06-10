# Channel Assignment — ASN-0126 review-63

**Date:** 2026-06-09 18:42

## Issue 1: The R-Scope transfer argument covers only one of P-tgt's two cases
Reason: Internal fix. The repair is a case-split the review has already fully specified, using only facts ASN-0126 already establishes or cites: effect-identity makes `a_emit` and the C/M/L effect F-independent, so Nullify and the Binary wrapper emit at the *identical* fresh address with identical `dom(Σ'.L) = A_rel^{Σ'}`, transferring R-Scope's set-equation conclusion across both P-tgt disjuncts; R0a's antichain and the `A_rel = dom(Σ'.L)` definition (AddressPartition) are both already invoked in-note. No design intent (the self-emit wrapper is the note's own construction) and no implementation behavior (R-Scope, R0a, AddressPartition are spec-layer results) is in question.
