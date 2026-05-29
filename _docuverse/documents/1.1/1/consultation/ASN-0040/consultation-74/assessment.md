# Channel Assignment — ASN-0040 review-74

**Date:** 2026-05-29 00:39

## Issue 1: B6 necessity for condition (i) rests on an unstated "injectivity" property
Reason: This is a structural choice between two internal fixes — either formalize namespace-map injectivity (witnessed by S2, already in the ASN) or exclude trailing-zero parents directly via T4's `t_{#t} ≠ 0`. Both options use only material already present; no design intent or implementation evidence is required.

## Issue 2: Atomicity (B4) is asserted and re-glossed redundantly
Reason: Pure editorial deduplication — state B4 once and remove the meta-commentary and restated read-semantics. Entirely internal to the document.

## Issue 3: B6 necessity is over-exampled
Reason: Consolidating three worked examples into two representatives is an internal pruning task; the propagation mechanism and examples are all already in the ASN.
