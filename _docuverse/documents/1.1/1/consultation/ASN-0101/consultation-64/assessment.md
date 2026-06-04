# Channel Assignment — ASN-0101 review-64

**Date:** 2026-06-04 07:12

## Issue 1: D10 boundary derivation uses P4★/P7a at Σ without closing the induction over DEL-extended traces
Reason: Internal. The induction's base case (initialisation), non-DEL step (ASN-0047's ExtendedReachableStateInvariants), and DEL-terminated step (D10's own derivation) are all already present in the ASN; the fix only requires stating the closure explicitly. No design intent or implementation evidence is at stake.

## Issue 2: D8 restates its Group (ii)/(iii) collective justification twice
Reason: Internal. This is a purely expository deduplication — drop the redundant trailing restatement — derivable from the ASN's own text with no need for design intent or implementation evidence.
