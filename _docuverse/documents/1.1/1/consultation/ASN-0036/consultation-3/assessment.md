# Revision Categorization — ASN-0036 review-3

**Date:** 2026-03-14 16:27

## Issue 1: S8 ordinal arithmetic introduces notation without citing TA7a (ASN-0034)
Category: INTERNAL
Reason: The fix is adding a citation to TA7a, which is already defined in ASN-0034. The ASN's own language already mirrors TA7a's formulation — it just needs the explicit reference.

## Issue 2: S7 cites T5 and T10 for origin uniqueness, but these are insufficient
Category: INTERNAL
Reason: The correct reference (GlobalUniqueness, ASN-0034) already exists and covers all cases including nesting prefixes. The fix is replacing an incorrect citation with the correct one, entirely derivable from ASN-0034's definitions.

## Issue 3: S5 quantifies over "Σ satisfying S0–S3" but S0 is a transition property
Category: INTERNAL
Reason: This is a formal logic error — transition invariants govern state pairs, not single states. The fix is rephrasing the quantifier to range over reachable states or restating as a meta-property of the invariants. Both alternatives are derivable from the definitions already present in the ASN.
