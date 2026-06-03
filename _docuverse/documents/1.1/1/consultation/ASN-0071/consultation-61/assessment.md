# Channel Assignment — ASN-0071 review-61

**Date:** 2026-06-03 11:27

## Issue 1: Forward-reference inventory in the vspec definition
Reason: Pure structural trim — delete the labeled forward inventory and the "amputate the reach" defense, keeping the vspec preconditions and the bare statement that it relaxes `ContentReference` conditions (i) and (iii). Every referenced boundary (F-DEEP, PC-RANGE, F-FILT) is already established at its own claim in the ASN, so no design intent or implementation evidence is needed.

## Issue 2: Relaxation rationale restated in *Resolution*
Reason: Editorial deduplication — retain the one contentful sentence (`iaddrs_one` is the set-valued, deduplicating, coverage-tolerant counterpart of `resolve`, coinciding on well-formed `ContentReference`s) and cut the repeated rationale. Both the kept fact and the cut justification are already present in the ASN.

## Issue 3: F-EMPTY miscited in the F-DEEP worked example
Reason: Internal logical correction — the conclusion rests on "empty `iaddrs` ⟹ empty `find`," which follows directly from F-find's definition (`ran(M(d)) ∩ ∅ = ∅` at every `d`), not from F-EMPTY's empty-query claim. The fix is derivable from the ASN's own definitions.
