# Channel Assignment — ASN-0040 review-99

**Date:** 2026-05-29 03:43

## Issue 1: S(p,d), S0, and B7 reinvent foundation allocator-domain results
Reason: Internal. The fix is a structural decision between citing T10a.6/T10a.7 from the foundation (ASN-0034) or justifying standalone re-derivation; both the foundation results and S(p,d)'s definition are already in scope, so the relationship is determined by comparing definitions, not by external evidence.

## Issue 2: B3 depends on an undefined predicate via a dangling pointer
Reason: Internal. Dropping "(introduced elsewhere)", declaring `Occupied` as an explicit abstract predicate parameter, and marking B3 as an introduced constraint with no preservation obligation are all editorial moves derivable from the ASN's own scope statement.

## Issue 3: Forward-reference accretion around Bop
Reason: Internal. Stating the registry-mutation rule once and citing by label is a pure restructuring of existing content; no design intent or implementation evidence is at stake.

## Issue 4: B4 contains self-describing meta-prose
Reason: Internal. Reducing B4 to the guarantee itself is a prose edit fully derivable from the existing statement.
