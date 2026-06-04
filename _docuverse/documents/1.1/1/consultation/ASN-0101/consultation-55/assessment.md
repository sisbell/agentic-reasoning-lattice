# Channel Assignment — ASN-0101 review-55

**Date:** 2026-06-04 06:07

## Issue 1: D8's enumerated per-state invariant groups omit S7d (and mislabel L14)
Reason: The fix is internal — S7d predicates over `dom(M)`/document tumblers, which D0's frame fixes (`dom(M') = dom(M)`, `E' = E`), so it slots into Group (ii)/(iii) by the same frame-fixed discharge already stated; the SD≡L14 label clarification is bookkeeping against the cited ASN-0047 theorem. No design intent or implementation evidence is required.

## Issue 2: Defensive citation-choice aside in the containment reduction
Reason: The fix is a pure deletion of around-the-claim prose; the T0 citation is self-sufficient and the removal requires no external input.
