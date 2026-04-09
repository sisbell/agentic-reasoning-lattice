# Revision Categorization — ASN-0082 review-3

**Date:** 2026-04-09 15:04

## Issue 1: Region disjointness not derived
Category: INTERNAL
Reason: The derivation is fully sketched in the review itself using TS4, TS2, and subspace preservation — all already cited or established in the ASN. Writing out the three-line argument requires no external evidence.

## Issue 2: Gap region unacknowledged
Category: INTERNAL
Reason: The fix is adding an explicit note that the gap region is reserved for a future content-placement postcondition. The worked example already shows new content in the gap; this is a formal completeness issue resolvable from the ASN's own structure.

## Issue 3: No span-level derived property
Category: INTERNAL
Reason: The review provides the complete derivation using TA-assoc (ASN-0034) and SpanReach (ASN-0053), both already available foundations. Connecting I3 to the span framework requires only writing out the algebra from cited definitions.

## Issue 4: M(d) and subspace(v) absent from statement registry
Category: INTERNAL
Reason: Both concepts are already defined inline in the ASN text. The fix is mechanically adding two definition rows to the existing registry table.
