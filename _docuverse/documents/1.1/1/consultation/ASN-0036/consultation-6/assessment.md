# Revision Categorization — ASN-0036 review-6

**Date:** 2026-03-14 17:15

## Issue 1: S8 cross-subspace disjointness cites T7 (identity) instead of T5/T1 (ordering)
Category: INTERNAL
Reason: The conclusion is correct and the fix (replace T7 citation with T5/ContiguousSubtrees and PrefixOrderingExtension) is fully specified by properties already defined in ASN-0034. No external evidence needed.

## Issue 2: V-position well-formedness is undefined
Category: INTERNAL
Reason: The ASN already contains the needed information informally — the worked example uses element-field tumblers, S8-depth describes the `s.x` form, and Gregory's evidence about V-address structure is already cited. The fix is formalizing what is already present into an explicit property parallel to S7b.
