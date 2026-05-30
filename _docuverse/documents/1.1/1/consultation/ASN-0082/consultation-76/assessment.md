# Channel Assignment — ASN-0082 review-76

**Date:** 2026-05-30 14:18

## Issue 1: Use-site inventory in OrdinalExceedsDisplacement
Reason: Pure deletion of forward-pointing prose; the `#v = 2` precondition is already explicit in the lemma and D-S can discharge `#r = 2` at its own site. No design intent or implementation evidence needed.

## Issue 2: Duplicate Statement Registry rows for associativity
Reason: Removing a redundant registry row that duplicates the cited TA-assoc lemma; the depth-1 specialization is already explained inline. Internal bookkeeping fix.

## Issue 3: Method-rationale prose in D-S derivation
Reason: Removing justification-of-structure prose; the ReverseInverse/TA-assoc/TA4 chain is self-evidently the argument. No external channel needed.
