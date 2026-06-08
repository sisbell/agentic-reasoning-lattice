# Channel Assignment — ASN-0102 review-99

**Date:** 2026-06-08 05:03

## Issue 1: P4a discharge mischaracterizes the witnessing trace
Reason: The fix is internal — it is a logical correction to how P4a (ASN-0047) is discharged, using P4a-at-`Σ` as inductive hypothesis and the trace-factoring the review already spells out. No design intent or implementation evidence is needed; the invariant's definition and the ASN's own composite-boundary reasoning suffice.

## Issue 2: X14 / X17 state the unconditional-write fact twice, and X14 carries coupling-discharge prose belonging to X17
Reason: Purely editorial deduplication and relocation of prose between two claims in the same ASN. Derivable from the ASN's own content; no channel needed.

## Issue 3: The resolution preamble pre-stages X8's per-reference run analysis
Reason: Editorial relocation of the M7-maximality characterization from the preamble into X8, where the within-reference argument already lives. Internal to the ASN; no channel needed.
