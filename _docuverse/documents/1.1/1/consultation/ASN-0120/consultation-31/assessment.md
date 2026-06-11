# Channel Assignment — ASN-0120 review-31

**Date:** 2026-06-11 13:38

## Issue 1: Worked example asserts a specific identity and seating that its stipulations do not determine
Reason: Internal fix — the missing premises (`C` homes no links, `V_{s_L}(C) = ∅`) and their consequences (`a = C.0.s_L.1` via FirstEmission, `v_a = [s_L, 1]` via MLop's empty-subspace branch) are all derivable from the ASN's own MLop contract and its already-cited substrate properties (ASN-0093 FirstEmission, K.μ⁺_L). The review prescribes the exact stipulations to add; no design-intent or implementation question is open.

## Issue 2: Verbatim body-level duplication of `wf`, `enabled`, and the `v_a` determination (anti-bloat)
Reason: Internal fix — pure organizational deduplication (choosing one canonical definition site per formula and referencing it elsewhere, as MLop already does for `ρ`). No semantic content changes, so neither design intent nor implementation evidence bears on it.
