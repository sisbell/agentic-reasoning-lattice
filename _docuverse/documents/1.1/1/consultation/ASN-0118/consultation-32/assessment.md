# Channel Assignment — ASN-0118 review-32

**Date:** 2026-06-10 23:58

## Issue 1: V-spec definition silently weakens ASN-0058's ContentReference condition (iii)
Reason: The choice between inheriting the depth pin and deliberately relaxing it is a live admissibility question that the ASN's internal content cannot settle alone; the relaxed reading rests on cited implementation behavior (`acceptablevsa`, `specset2ispanset`), so Gregory must confirm what the resolution path actually does with a depth-mismatched span. Nelson's boundary-semantics quotes are already in the document and need no fresh consultation.
Gregory question: Does udanax-green's spec-set resolution path (specset2ispanset and the surrounding V-spec acceptance code) admit a spec whose span tumblers have a different depth than the document's bound V-positions — e.g., a depth-3 start/width over a depth-2 text subspace — and if so, does it resolve such a span by pure intersection with the bound positions, or does any check reject or normalize the depth mismatch?

## Issue 2: CP11's multiset gloss contradicts its own formula and the worked example
Reason: The formula and the worked example already fix the correct semantics (per-address counting, `⦃d_A, d_A, d_B⦄`); the fix is purely a wording correction to the gloss, derivable from the ASN's own content.

## Issue 3 (anti-bloat): REPLICATE is defined twice
Reason: This is an editorial deduplication — consolidate the REPLICATE definition into the transclusion-frame section and have the non-contiguous section cite it, keeping only the new consequences there. No design intent or implementation evidence is involved.
