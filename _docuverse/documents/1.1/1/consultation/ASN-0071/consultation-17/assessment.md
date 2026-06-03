# Channel Assignment — ASN-0071 review-17

**Date:** 2026-06-02 23:18

## Issue 1: The `actionPoint(ℓ) ≤ #u` precondition admits coarse spans that over-collect content
Reason: The fix is derivable from the ASN's own content — C0 (cited from ASN-0058) already establishes `actionPoint = m` as the tightness condition that prevents interior-displacement over-collection, and TumblerAdd's prefix-copy behavior (used throughout the confinement argument) determines what a coarse span resolves to. Tightening to `actionPoint(ℓ) = #u` to match C0, plus a `#u ≥ 3` worked example, requires only reasoning already present.

## Issue 2: Misstated reach in the confinement counterexample
Reason: Pure arithmetic correction of a TumblerAdd computation (`[1,5] ⊕ [2,0] = [3,5]`), fully derivable from the TumblerAdd rule the ASN already invokes; no design intent or implementation evidence involved.
