# Channel Assignment — ASN-0119 review-43

**Date:** 2026-06-10 08:32

## Issue 1: E and R frames asserted as prose, not as clauses, while load-bearing
Reason: Internal — the note already establishes that REARRANGE writes only `M(d)` and that ASN-0084 frames only `M`/`C`, so `E`/`R` inertness is derivable from the ASN's own lifting argument (the same reasoning that produced RA6 for `L`). The fix is purely notational: elevate the prose "inert" to labeled clauses `Σ'.E = Σ.E` and `Σ'.R = Σ.R`.

## Issue 2: Claim-label sequence skips RA4
Reason: Internal — this is editorial bookkeeping over the note's own claim labels. Renumbering RA5→RA9 to close the gap (or annotating the gap) requires no design intent or implementation evidence.

## Issue 3: P4a discharge re-derives a foundation result in full (anti-bloat)
Reason: Internal — the foundation result being re-derived is ASN-0047's own P4a trace-length induction, and the REARRANGE-specific delta (`R' = R` empties the new-entry branch) is already stated in the note's closing sentence. Citing the foundation and keeping only the delta is a trim derivable from material already present.
