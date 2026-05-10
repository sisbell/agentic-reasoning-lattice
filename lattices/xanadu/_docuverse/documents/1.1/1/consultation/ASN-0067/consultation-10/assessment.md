# Revision Categorization — ASN-0067 review-10

**Date:** 2026-03-21 20:07



## Issue 1: Block decomposition scoped to text subspace while insertion position is unrestricted
Category: INTERNAL
Reason: The fix is derivable from the ASN's own definitions — either restrict S ≥ 1 in the COPY preconditions (aligning with COPY's stated role as content placement) or scope B to the target subspace. Both options are fully determined by the existing formal framework without needing external evidence.

## Issue 2: S8a preservation proof assumes text subspace
Category: INTERNAL
Reason: This is a proof argument error whose fix follows directly from Issue 1's resolution — if S ≥ 1 is added as a precondition, the proof holds as written; if not, the case split for S = 0 is derivable from S8a's existing guard condition. No external design intent or implementation evidence is needed.
