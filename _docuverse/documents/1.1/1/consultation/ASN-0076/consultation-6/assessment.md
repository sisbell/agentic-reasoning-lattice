# Channel Assignment — ASN-0076 review-6

**Date:** 2026-05-25 20:41

## Issue 1: Missing intermediate step in #E ≥ 2 induction
Reason: Pure proof-patch within the ASN's existing citations (TA5(c), TA5-SigValid, T0, T4). The reviewer has identified the exact missing chain; no design intent or implementation evidence is required to insert it.

## Issue 2: Misleading L1c citation in E2 distinctness argument
Reason: Citation correction — reviewer has already identified the correct authority (SequentialTransitionAxiom, ASN-0047). Internal cross-reference fix only.

## Issue 3: Maximality argument at Step 2 leaves prefix structure implicit
Reason: Requires only a one-line inductive observation about K.λ's behavior (advancing the allocator enumeration by exactly one per fire), derivable from K.λ's specification in ASN-0047 which is already cited. No external consultation needed.
