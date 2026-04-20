# Revision Categorization — ASN-0058 review-7

**Date:** 2026-03-22 17:33



## Issue 1: `v + k` reinvents OrdinalShift; M-aux re-derives TS3
Category: INTERNAL
Reason: The fix is purely notational — redefine `v + k` as shorthand for `shift(v, k)` from ASN-0034 and cite TS3 instead of re-deriving. All required definitions and proofs already exist in the referenced foundation ASN.

## Issue 2: C1a overclaims required conditions
Category: INTERNAL
Reason: The inconsistency is between C1a's general claim and M12's proof text, both within ASN-0058. The fix involves either adding S8a to C1a's condition list, rephrasing M12's parenthetical to avoid S8a, or removing the "verbatim" language — all derivable from the ASN's own content and the referenced properties in ASN-0036.
