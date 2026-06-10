# Channel Assignment — ASN-0116 review-61

**Date:** 2026-06-09 22:18

## Issue 1: The worked example asserts D(d) is both unchanged and changed for the same scenario
Reason: The fix is internal — the review itself confirms IP6 and its emptiness-vs-containment commentary are correct and only the example illustrates it inconsistently. Resolving the contradiction requires only the ASN's own IP6 definition of `Added`/`D(d,Σ)` and the worked setup: either split `ℓ` and `ℓ'` into separate pre-states or rescope the IP6-trap prose to `ℓ` alone, both derivable without design intent or implementation evidence.
