# Channel Assignment — ASN-0119 review-17

**Date:** 2026-06-09 18:03

## Issue 1: The state model is stated as ASN-0036/0043's, but the discharged S3★ postcondition requires ASN-0047's link-subspace arrangement
Reason: The contradiction is between two specifications the note already cites — ASN-0043's L14a/S3 (arrangement maps only to content) versus ASN-0047's per-subspace S3★ (arrangement carries link V-positions). Resolving it means aligning the note's declared model with the invariants it discharges, and both models plus the deciding facts (L14a, K.μ⁺_L, S3 vs S3★) are already present in the cited lattice; no design-intent or implementation evidence is needed to pick one and apply it consistently.

## Issue 2: The contiguity analysis builds two overlapping taxonomies behind doubled forward-pointing framing
Reason: This is a pure reorganization of the note's own prose — collapsing two overlapping case analyses into one taxonomy and dropping the redundant `{B,E}`/`{B,C,D,E}` example and duplicated framing sentences. All the mathematical facts and examples are already in the note; nothing external is required.

## Issue 3: The Claims Introduced table reproduces body proofs in its cells
Reason: Purely editorial — the S3★ derivation already lives in the body, so reducing the table cell to claim statement plus provenance requires only deleting the duplicated proof. No external channel is involved.
