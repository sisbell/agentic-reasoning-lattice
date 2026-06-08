# Channel Assignment — ASN-0100 review-119

**Date:** 2026-06-08 00:04

## Issue 1: Two-stream point stated twice in different words
Reason: Purely editorial deduplication of two paragraphs that restate content-immutability; the fix collapses prose already present in the ASN. No design intent or implementation evidence needed.

## Issue 2: L0 content-clause discharged redundantly, with a deferral chain
Reason: Internal proof-bookkeeping cleanup — the grouped per-address paragraph already discharges L0's content clause at both intermediate and boundary states, so reducing the other two sites to a pointer is derivable from the ASN's own structure.

## Issue 3: "Branch selection keys on dom(C), not the arrangement" explained three times
Reason: Editorial deduplication of a rule stated in §Effect One, re-explained in the example, and gestured at in INS.alloc; the worked steps already demonstrate it, so the fix is internal to the ASN.
