# Channel Assignment — ASN-0069 review-76

**Date:** 2026-06-03 00:08

## Issue 1: V8's transitive d_src ↔ d_new correspondence is misstated for subsequent forks
Reason: The fix is internal — either supply the `k=0` induction over `A_v(d_src)`'s emission sequence (built entirely from V8, V4, V5 and the allocator structure already in the ASN) or restrict the prose to the second-version case. No design intent or implementation evidence is needed; this is a proof-closure choice derivable from the ASN's own content.

## Issue 2: V2 re-derives a foundation result at length, then justifies the duplication in prose
Reason: The fix is internal — J4's `d_src ≼ d_new` consequence is already cited in the ASN, so restating V2 as a named one-line citation and deleting the nested induction and the Dependency-Audit defense requires only the ASN's own material.

## Issue 3: V11 carries defensive parentheticals that explain what is not needed
Reason: The fix is internal — deleting the "no X needed / only Y consumed" asides is pure pruning of existing prose; nothing about design intent or implementation bears on it.

## Issue 4: Dependency Audit contains a downstream-consumption inventory
Reason: The fix is internal — removing the consumption-tracking sentence while keeping the substantive used/unused-deps statement is derivable from the ASN alone.
