# Revision Categorization — ASN-0063 review-15

**Date:** 2026-03-21 23:20



## Issue 1: CL11 misclassifies S8 and gives incorrect justification
Category: INTERNAL
Reason: S8's classification and justification are derivable from definitions already in the ASN — S8 follows from S8-fin, S8a, S2, and S8-depth, all verified in the preceding paragraph of CL11.

## Issue 2: S3★-aux proof omits K.λ
Category: INTERNAL
Reason: K.λ is defined in this ASN with an explicit frame clause M' = M. Adding it to the enumeration requires only reading the transition's own frame specification.

## Issue 3: Orphan link composite — coupling constraints verified but state invariants not
Category: INTERNAL
Reason: The invariant verification follows mechanically from K.λ's frame (M, C, E, R unchanged) and its preconditions (which directly establish L0, L1, L1a, L12, L14). All needed facts are already in the ASN.

## Issue 4: No extended reachable-state invariants theorem
Category: INTERNAL
Reason: The full invariant set and preservation arguments are already present across the ASN's sections — the theorem is a matter of collecting and stating them together, requiring no external evidence about design intent or implementation behavior.
