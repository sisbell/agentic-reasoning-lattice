# Revision Categorization — ASN-0058 review-2

**Date:** 2026-03-20 15:14

## Issue 1: M0 derivation missing
Category: INTERNAL
Reason: The fix is a one-line derivation citing TA5(a) from ASN-0034, which is already established in the foundations. The chain (strict increase → injectivity → cardinality) is purely deductive from existing definitions.

## Issue 2: M12 gap-freeness without S8-depth
Category: INTERNAL
Reason: The fix is citing S8-depth from ASN-0036, an already-established property. This is a missing citation, not missing knowledge.

## Issue 3: M12 ordinal decrement undefined
Category: INTERNAL
Reason: The fix defines ordinal decrement using TumblerSub (⊖) from ASN-0034, which already exists in the foundations. The edge-case handling is already described in the parenthetical.

## Issue 4: M12 partition uniqueness unproven
Category: INTERNAL
Reason: The proof sketch uses only tools already present in the ASN (B3, maximality conditions, M(d) functionality). The review even supplies the argument; it just needs to be included.

## Issue 5: M12 left-extension by "symmetric argument"
Category: INTERNAL
Reason: The left case uses the same B2 disjointness and merge-condition reasoning already proven for the right case, plus ordinal decrement (once Issue 3 is resolved). All machinery is internal.

## Issue 6: M14 imprecise reasoning
Category: INTERNAL
Reason: The fix cites TA-strict from ASN-0034 (already established) and corrects the logical conclusion. No design intent or implementation evidence is needed.
