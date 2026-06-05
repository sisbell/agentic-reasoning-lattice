# Channel Assignment — ASN-0112 review-6

**Date:** 2026-06-05 00:38

## Issue 1: V10's "increases by exactly n" asserts a count-correspondence the ASN simultaneously declares open and forbids
Reason: Fix is internal — the body already states V10 in displacement terms (`shift(extent_before, n)`), and the count-coincidence rationale (dense run + D-MIN★ + uniform depth) is already supplied by V5's machinery; reconciling the three and narrowing Open Question 2 needs only the ASN's own content.

## Issue 2: No weakest-precondition treatment of a non-trivial result property
Reason: Fix is internal — the exact-cover precondition (single-subspace occupancy) and the reach-equality condition (`#origin_d ≤ #reach_d`) are both already derived inside V2/V5/V6; framing them as a wp characterization is a reformulation of facts already present, requiring no design intent or implementation evidence.
