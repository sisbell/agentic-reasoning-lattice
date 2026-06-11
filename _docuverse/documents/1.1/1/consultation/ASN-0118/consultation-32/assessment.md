# Channel Assignment — ASN-0118 review-32

**Date:** 2026-06-10 21:29

## Issue 1: V-spec definition silently weakens ASN-0058's ContentReference condition (iii)
Reason: Choosing between inheriting the depth pin and explicitly relaxing it is a live design decision, not derivable from the ASN's own text: it turns on whether Nelson's span semantics intends boundaries to be free-form tumblers or aligned to the source's addressing depth, and on whether udanax-green's resolution actually admits and correctly resolves a depth-mismatched span. The ASN's existing Gregory citations (`acceptablevsa`, `specset2ispanset`) don't specifically address the depth-mismatch case.
Nelson question: When a span designates content by its boundary tumblers, did the design intend those boundaries to be arbitrary tumblers ("what lies between is implicit in the choice of first and last point"), or must a span's start and width carry the same depth as the V-positions of the subspace it draws from?
Gregory question: When a spec-set span's start or width has a different tumbler depth than the document's bound V-positions (e.g., a depth-3 span over a depth-2 text subspace), does the resolution path (`specset2ispanset` and the underlying tumbler intersection) admit the span and correctly select the bound positions inside its denotation, or does any check reject or misresolve depth-mismatched spans?

## Issue 2: CP11's multiset gloss contradicts its own formula and the worked example
Reason: The formula and the worked example already agree on per-address counting; only the prose gloss misuses "fragment." The fix is a wording correction fully determined by the ASN's own content.

## Issue 3 (anti-bloat): REPLICATE is defined twice
Reason: Purely editorial consolidation — define REPLICATE once and have the non-contiguous section cite it for the new consequence. No design intent or implementation evidence bears on it.
