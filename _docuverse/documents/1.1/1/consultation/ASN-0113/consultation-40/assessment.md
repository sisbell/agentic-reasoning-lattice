# Channel Assignment — ASN-0113 review-40

**Date:** 2026-06-08 10:36

## Issue 1: W20 conflates allocated home links with arranged links — the bijection is not surjective onto all home links
Reason: The fix turns on whether a link can be homed at `d` (origin = d) yet never placed in `M(d)` — i.e. whether link allocation and link-subspace arrangement are genuinely distinct transitions. That is an implementation/foundation fact (does such an unarranged-home-link state actually arise?), which Gregory can confirm; if so, the claim must be weakened to a bijection onto `ran(M(d)|_{s_L})`.
Gregory question: Can a link be allocated with `origin(ℓ) = d` and never appear in `d`'s link-subspace arrangement, or does the back end couple link creation to arrangement so that every home link of `d` is necessarily present in `M(d)`?

## Issue 2: W-pre cites an irrelevant foundation claim
Reason: Pure citation hygiene — drop the M1 reference (M0 alone discharges the equivalence) and pick one foundation's registration operation consistently. Both the relevant claims (M0, K.σ vs K.δ) are already named in the ASN and review, so the correction is internal.

## Issue 3: the contiguity load-bearing point is restated redundantly (anti-bloat)
Reason: Editorial de-duplication only — keep the load-bearing statement once in the body, trim the table note and Open Question. Fully derivable from the ASN's own text.
