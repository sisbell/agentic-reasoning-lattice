# Channel Assignment — ASN-0116 review-51

**Date:** 2026-06-09 18:17

## Issue 1: The IP1 maximality parenthetical misattributes the backward-merge trigger
Reason: Internal. That the "`q_{J-1}` holds `a_prev`" configuration is reachable by ordinary append follows from the ASN's own machinery — K.α allocates `inc(a_prev, 0)` against the greatest origin-`d` address, and iterating INSERT's append case in allocation order leaves `q_N ↦ [d.0.s_C.N]`. The correction is a re-attribution among paths the ASN already defines (append vs. K.μ~ reordering), requiring no design intent or implementation evidence.

## Issue 2: Defensive prose reasoning about behaviors INSERT does not exhibit
Reason: Internal. Both deletions are licensed by facts already in the ASN — I-PROV records exactly `{(shift(a,k), d)}` keyed on fresh addresses (so the hypothetical re-recording reader is moot), and FirstEmissionFreshness alone discharges the `k=0` empty-region branch (so the SubsequentEmissionFreshness-exclusion gloss is surplus). Pure removal of redundant prose whose load-bearing content survives elsewhere.
