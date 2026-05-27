# Channel Assignment — ASN-0099 review-40

**Date:** 2026-05-27 07:14

## Issue 1: F1's formal definition lacks explicit precondition
Reason: Pure notational consistency fix. The precondition `a ∈ dom(Σ.L)` is already surfaced in the ASN's own prose ("Predicate domain" paragraph); restating it on F1 requires no external input.

## Issue 2: F4's anchoring of overlap predicate via LM 4/60 is asserted, not derived
Reason: The fix turns on interpreting LM 4/60's scope — whether "quantity of links not satisfying a request does not impede search on others" operates at the *link* level (across links in dom(L)) or at the *span* level (within an endset). The bridge from LM 4/60 to singleton overlap depends on this interpretive question, which is Nelson design-intent territory.
Nelson question: Does LM 4/60's robustness principle apply at the span level within a single link's endset — such that adding a non-overlapping span to an already-matching endset must not suppress the existing match — or does it only constrain interactions across distinct links?

## Issue 3: wp analysis for K.λ-induced increment is implicit
Reason: The reviewer explicitly notes the wp statement "follows from F1 + L12 + F11"; K.λ's effect clause is already published in the substrate (ASN-0093/ASN-0047). Construction is internal to the ASN's existing foundation.

## Issue 4: Worked example does not exercise F11's persistence claim across K.λ growth
Reason: Extending the worked example with a K.λ step requires only the existing K.λ preconditions and the ASN's own definitions. Construction is purely a matter of choosing endsets disjoint from `{α₂}` — no design intent or implementation evidence needed.
