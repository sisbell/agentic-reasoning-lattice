# Channel Assignment — ASN-0077 review-61

**Date:** 2026-06-04 13:16

## Issue 1: Redundant pointwise-vs-span framing stated twice
Reason: Purely editorial deduplication; the fix is to drop one of two paragraphs already present in the ASN, requiring no design intent or implementation evidence.

## Issue 2: Defensive "m = 2 is not forced" asides
Reason: Internal cleanup; the O11' and worked-example derivations already establish `#v_ℓ = m` from S8-depth without fixing `m`, so removing the parentheticals is derivable from the ASN's own text.

## Issue 3: O5★ applies the closure schema to a union-membership clause outside the schema's clause grammar
Reason: The required fix — decomposing the disjunctive clause into two per-store membership-persistence clauses — is a logical restructuring using the schema form the review itself states ASN-0098 admits, so it is derivable from the cited foundation without consulting design intent or implementation.
