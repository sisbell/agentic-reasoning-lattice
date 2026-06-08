# Channel Assignment — ASN-0102 review-57

**Date:** 2026-06-08 01:30

## Issue 1: X8 restates X12's boundary-absorption conditions instead of deferring to it
Reason: Purely editorial deduplication within the ASN — X12 already states the leading/trailing iff-conditions in full, so X8 need only defer to it. No design intent or implementation evidence is required to remove restated text.

## Issue 2: X7 and X16 independently derive the same copied/displaced range-disjointness
Reason: Internal redundancy between two of the ASN's own claims; the fix is to pick X16 as the single derivation site and have X7 cite it. The disjointness is already proved in the ASN, so neither channel is needed.
