# Channel Assignment — ASN-0119 review-4

**Date:** 2026-06-09 00:33

## Issue 1: The scope-restriction justification misstates the link subspace's invariants
Reason: Internal fix. The review already pinpoints the contradiction (citing D-CTG★/D-SEQ★/D-MIN★ as per-subspace while claiming s_L lacks them) and the correct grounds (REARRANGE_K defined only for S=1 via CS3; link rearrangement would touch CL-UNIQ/CL-OWN). Both are resolvable from the note's own cited foundations (ASN-0036/0043/0047/0084) — no design intent or implementation evidence required.

## Issue 2: The P7a claim-table phrase overstates fragmentation
Reason: Internal fix. The note's own prose ("fragmentation occurs exactly when a single contiguous run straddles a cut") and worked pivot already contain the correct statement; the table row simply needs to be brought into line with them. No external channel needed.
