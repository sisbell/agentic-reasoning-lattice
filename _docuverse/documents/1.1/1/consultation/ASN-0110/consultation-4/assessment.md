# Channel Assignment — ASN-0110 review-4

**Date:** 2026-06-08 00:40

## Issue 1: "Matches Gregory" claim conflates slot-length with empty-slot-in-position; leaves a completeness gap for arity > 3
Reason: Choosing between scoping to 3 slots vs. keeping length `N_max(Σ)` turns on two external facts: whether Nelson's design intends links beyond the from/to/type triple to be searchable as roles, and what udanax-green's RETRIEVEENDSETS actually emits (always 3 slots? does it ever hold arity-5 links?). Neither is settled by the ASN's own content.
Nelson question: Was RETRIEVEENDSETS intended to return endsets only for the three standard roles (from, to, type), or for every role of arbitrary-arity (N ≥ 3) links touching the region?
Gregory question: Does udanax-green's RETRIEVEENDSETS always emit exactly three endset slots, and can the link store ever hold links of arity greater than 3 whose extra-slot endsets touch the queried region?

## Issue 2: Misattributed foundation citation in RE-overlap
Reason: The fix is internal — RE-decide already cites T2 (ASN-0034) for the identical point-in-span membership predicate, so the correct foundation is present in the ASN itself; RE-overlap's SC (ASN-0053) citation just needs to be aligned to T1/T2.
