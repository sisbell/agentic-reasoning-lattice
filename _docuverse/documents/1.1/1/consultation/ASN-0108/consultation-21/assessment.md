# Channel Assignment — ASN-0108 review-21

**Date:** 2026-06-12 23:42

## Issue 1: W5 declares tail-order preservation *necessary*, but W9d (and a clean counterexample) show it is not
Reason: The contradiction is between two of the note's own claims — W5's clause-2 necessity and W9d's "free tail permutation is a harmless reshuffle" — and the note's framework already fixes the operative notion of "well-defined resumption" as the no-skip/no-duplicate partition (W4) under present-tense per-call completeness (W7) and stateless recomputation (W3), which is precisely what rules out the order-faithfulness reading that alone would rescue "necessary." The resolution path (a) — clause 1 genuinely necessary at every cursor, clause 2 demoted into the sufficient discipline — is derivable from the ASN's own content.

## Issue 2: W9b's definition of "tail-inflow event" excludes its own kind (1), falsifying the "exhaustive basis" claim the termination proof rests on
Reason: This is a definitional/accounting defect internal to W9b's multiplicity-bound proof; either admitting "presence at the first call" as a base inflow contribution or restating the bound as `deliveries ≤ |initial tail| + |transition inflow events|` (with `|initial tail|` finite by M-fin, already imported) closes the gap without any design-intent or implementation evidence.

## Issue 3: anti-bloat — defensive/duplicated/forward-deferring prose to remove
Reason: Pure editorial removal of a false defensive claim, a duplicated orphaning mechanism, and a forward-deferral cross-pointer; folding load-bearing content into the claims it serves (W7 citing M-mut for the mechanism, etc.) follows from the note's own structure and the Issue 1/2 resolutions.
