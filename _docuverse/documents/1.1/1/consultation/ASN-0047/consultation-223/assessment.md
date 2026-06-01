# Channel Assignment — ASN-0047 review-223

**Date:** 2026-06-01 06:24

## Issue 1: K.μ~ admissibility clause (i) mislabeled as "full per-state invariant package"
Reason: Internal fix. The ASN's own verification matrix already discharges CL-OWN, CL-UNIQ, S2, and S8★ for K.μ~ via fixity/bijection/rebuild rather than admissibility; renaming clause (i) and reclassifying those invariants as derived is a terminology correction consistent with the existing proof structure.

## Issue 2: P4a discharge mechanism stated three times verbatim
Reason: Internal fix. Consolidating the three restatements into a single canonical site (the P4a definition box) with pointers elsewhere is a purely editorial de-duplication requiring no design intent or implementation evidence.

## Issue 3: Redundant "caller-checked precondition" restatement in K.μ~ necessity/sufficiency
Reason: Internal fix. Deleting or compressing the redundant closing paragraph removes content already established by the formal necessity/sufficiency directions; no external grounding is needed.
