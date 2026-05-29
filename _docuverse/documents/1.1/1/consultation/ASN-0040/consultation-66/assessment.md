# Channel Assignment — ASN-0040 review-66

**Date:** 2026-05-28 23:35

## Issue 1: B0b claims "exactly one new element" as immediate from B0a, but freshness is not
Reason: Internal fix. The dependency structure (freshness proved in Bop via B1, consumers use only the union form) is fully present in the ASN; choosing to weaken B0b's wording or annotate the strictness source requires no design intent or implementation evidence.

## Issue 2: B8 cross-branch limitation stated twice
Reason: Internal fix. Removing one of two redundant scope statements is an editorial decision derivable from the ASN's own text; no external channel bears on which paragraph to keep.

## Issue 3: B6(i) injectivity rationale duplicated across S2 and B6
Reason: Internal fix. The injectivity rationale and its proper home (B6's necessity argument, where the d=1 exception is carved out) are already established in the ASN; consolidating is purely a placement decision.

## Issue 4: B9 carries meta-commentary on its own proof
Reason: Internal fix. Deleting self-referential and editorial sentences while retaining the NAT-closure step is an editorial trim fully determined by the existing proof content.
