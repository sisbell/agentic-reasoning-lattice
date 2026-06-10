# Channel Assignment — ASN-0127 review-28

**Date:** 2026-06-10 14:12

## Issue 1: D-ZERO's "no link satisfying I was ever created" is supported only at the path's initial state
Reason: The fix is internal — both repair routes the review names (citing E-CONS's exact-difference characterization, or instantiating E-INV at the creation state and chasing the suffix) use lemmas already proven in this ASN; no design-intent or implementation question is involved, only recomposing the existing proof chain.

## Issue 2: duplicated bridge prose and a doubled point in D-NONMONO
Reason: The fix is internal — it is pure prose deduplication (state the bridging device once, cut one of two redundant injectivity sentences); the formal chains already carry the argument and no content changes.

## Issue 3: consumer inventory in F-CIL-perlink's introduction
Reason: The fix is internal — it is a sentence-level trim removing a consumer enumeration that duplicates citations already present at the use sites; nothing about design intent or implementation behavior bears on it.
