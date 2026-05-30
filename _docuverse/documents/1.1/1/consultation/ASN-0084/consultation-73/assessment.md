# Channel Assignment — ASN-0084 review-73

**Date:** 2026-05-30 15:26

## Issue 1: No worked example exercises a non-S position, yet non-S handling is load-bearing
Reason: The fix instantiates machinery already fully defined in the ASN (R-NS NS-π, R-BLK's non-S verbatim carry, R-COMM's non-S branch, T10 disjointness); tracing a concrete non-S position is mechanical instantiation of existing definitions, requiring neither design intent nor implementation evidence.

## Issue 2: R-CS3 states its claim twice
Reason: Pure prose deduplication within the section; the lemma and counterexample already carry the content, so the fix is internal.

## Issue 3: R-NS proof contains a redundant re-derivation
Reason: Deleting a self-described "already supplied" re-derivation is an internal editing fix; the two preceding sentences already discharge NS-π.

## Issue 4: "Invariant preservation" block pads preservation claims with restatements of what each invariant says
Reason: Consolidating preservation mechanisms and dropping per-invariant restatements of foundation (ASN-0036) content is internal; the load-bearing one-liners are already present in the ASN.
