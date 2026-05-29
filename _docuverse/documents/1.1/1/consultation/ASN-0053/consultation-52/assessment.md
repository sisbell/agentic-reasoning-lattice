# Channel Assignment — ASN-0053 review-52

**Date:** 2026-05-28 21:31

## Issue 1: S3 collapses two adjacency disjuncts without showing one is vacuous
Reason: Pure proof-structure fix. The vacuity of `reach(β) = start(α)` under `start(α) ≤ start(β)` follows by chaining the ASN's own non-emptiness fact (start < reach from T12/TA-strict); no design intent or implementation evidence is needed.

## Issue 2: S1 asserts the empty branch instead of deriving it
Reason: Internal restructuring. The forward inclusion is an order-only argument already present in the proof; hoisting it before the case split and noting `{t : s' ≤ t < r'} = ∅` when `r' ≤ s'` is entirely derivable from T1's totality as stated.

## Issue 3: use-site inventory in the reach section
Reason: Anti-bloat deletion. Removing the redundant global pre-certification sentence requires only confirming the per-claim discharges (S4/S5/WF/WR) carry level-uniformity locally, which they do within this ASN; no external channel involved.
