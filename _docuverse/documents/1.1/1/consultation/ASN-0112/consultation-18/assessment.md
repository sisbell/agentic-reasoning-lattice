# Channel Assignment — ASN-0112 review-18

**Date:** 2026-06-08 08:58

## Issue 1: Provenance narration and defenses against non-existent alternatives
Reason: Purely editorial — deleting the "does not route through WF" and "no such convention" disclaimers leaves the existing coverage and `inc(w,0)` tightness proofs intact. The arguments already stand in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: V10/V18 re-derive INSERT and DELETE mechanics
Reason: Derivable from the ASN's own content — V16 already establishes `σ_d` as a function of `O(d)`, so reducing V10/V18 to "any edit changes the span exactly insofar as it changes `O(d)`" and stating origin migration as a bound on V8's hypothesis are internal restructuring decisions. No new implementation facts or intent are needed.

## Issue 3: Repeated deferral to the span-set operation
Reason: Pure deduplication — V7 already states the single-convex-region-cannot-fragment fact; removing the echoes in the V6 paragraph and Open Question 1 needs nothing beyond the note itself.
