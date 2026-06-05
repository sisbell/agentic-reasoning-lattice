# Channel Assignment — ASN-0108 review-6

**Date:** 2026-06-05 04:28

## Issue 1: M-mut presupposes the satisfaction predicate the ASN says it defers
Reason: The fix is to flag a scoping assumption — state that windowing assumes the discoverability reading of "matching" (already grounded in the cited ASN-0098 LP17/LP13) or make M-mut conditional. No design-intent or implementation evidence is needed to reframe a claim the ASN already deferred; it is internal bookkeeping.

## Issue 2: W4's completeness is proved only for fixed N, but W11 permits the reader to vary N
Reason: Purely a proof generalization — replace the uniform stride `iN` with cumulative cut-points `S_i = N_0+…+N_{i-1}`. Derivable from the ASN's own W4 induction; no external channel required.

## Issue 3: W8 — the load-bearing "cursor survives orphaning" claim has no concrete scenario
Reason: The fix adds a worked trace using machinery already present (T8 address permanence, the `After` definition, the W9 ambiguity). It instantiates existing claims rather than establishing new facts about design or implementation, so it is internal.
