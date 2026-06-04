# Channel Assignment — ASN-0101 review-71

**Date:** 2026-06-04 09:04

## Issue 1: D8 claims "per-state invariant" scope but proves transition invariants too
Reason: The fix is a pure rephrasing of D8's headline to match its own group labels; the proof is already sound and the discrepancy is internal to the ASN's stated scope. No design intent or implementation evidence is needed.

## Issue 2: Implementation commentary the ASN itself declares irrelevant (anti-bloat)
Reason: This is a placement/trim decision about prose the ASN already concedes is mechanism-agnostic; the load-bearing fact (subspace isolation, spec mechanism-agnostic) is derivable from D0/D6 within the ASN. No external channel is needed to decide what to cut.
