# Channel Assignment — ASN-0126 review-88

**Date:** 2026-06-10 04:03

## Issue 1: The Nullify-fate caveat in "The registry" is a downstream preview
Reason: Pure relocation of exposition — every fact involved (empty-from Nullify has no `→_sh` image, the from-filled re-expression) is already stated and derived later in the ASN itself. Moving the caveat out of "The registry" and letting "The shape-gated emit" carry it requires no design intent or implementation evidence, only the ASN's own structure.

## Issue 2: The wp's reason for omitting precondition (0) is wrong, and clashes with the L3 claim two sentences later
Reason: A correction to the ASN's own weakest-precondition reasoning over a guarded command; the right justification (`Emit_K` always constructs the arity-3 triple `(F, G, K)`, so (0) is vacuously ⊤ and the same fact discharges L3) rests on facts the ASN already asserts (Gate realizability, effect-identity). The review spells out the correct argument, so it is derivable internally.

## Issue 3: (0) and (i) are glossed twice in adjacent sentences
Reason: Pure prose deduplication within "The shape-gated emit" — terse the first sentence's listing, keep only the well-definedness conclusion in the second. No external intent or implementation fact is at stake.
