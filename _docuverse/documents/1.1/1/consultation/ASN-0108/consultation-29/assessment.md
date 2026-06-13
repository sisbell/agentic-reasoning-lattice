# Channel Assignment — ASN-0108 review-29

**Date:** 2026-06-13 02:33

## Issue 1: W5 overclaims clause 1 as *necessary* for coherence
Reason: This is a pure logic defect in the note's own coherence claim — the counterexample (three both-states links, `N=1`), the corrected sufficiency framing, and the genuine global characterization are all already supplied in ASN-0108's own notation, so the fix is derivable from definitions and reasoning present in the note. No design intent or implementation evidence is at stake.

## Issue 2: The computability-vs-clause-1 distinction is asserted redundantly across sections
Reason: This is an editorial anti-bloat consolidation entirely internal to the note's prose — state the computability/clause-1 distinction once in the ladder, cross-reference it from W9, and drop the consumer enumeration and the re-listing of W5's three conditions. No channel needed.

## Issue 3: W6a's F-LAMBDA citation is to the wrong matching-set notion
Reason: The fix turns on ASN-0127's actual content — whether `findlinks_V` is defined through an image set that is a function of `M` (so K.λ's frame freezes it) and whether a `findlinks_V`-level analogue of F-LAMBDA exists to cite directly — which lives in the knowledge base, not in ASN-0108, so it falls to Gregory's evidence channel.
Gregory question: In ASN-0127, is `findlinks_V(W, d_q, Σ)` defined as `findlinks(image(W, d_q, Σ), Σ)` with the image determined solely by the arrangement family `M` (so a `K.λ` creation's `M' = M` frame leaves the image unchanged), and does ASN-0127 state a `findlinks_V`-level analogue of F-LAMBDA (disjoint addition of a fresh `K.λ` link to the discoverability matching set) that ASN-0108 could cite directly instead of the fixed-`I` F-LAMBDA?
