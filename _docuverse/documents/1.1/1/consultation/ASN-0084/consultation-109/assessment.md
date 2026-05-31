# Channel Assignment — ASN-0084 review-109

**Date:** 2026-05-30 22:01

## Issue 1: Displacement Analysis Remark duplicates its own bullet derivation
Reason: Purely editorial deduplication of prose already present in the ASN; no design intent or implementation evidence is needed to choose between deleting the remark's claim or the per-bullet tails.

## Issue 2: A trivially-answerable question is left open, weakening the precondition analysis
Reason: The equivalence `R-PRE(iv) ⟺ ord(c_{n−1}) ≤ N + 1` follows directly from D-SEQ and EXT-VAC, both already stated and proved in the ASN; the derivation is internal arithmetic requiring no external channel.
