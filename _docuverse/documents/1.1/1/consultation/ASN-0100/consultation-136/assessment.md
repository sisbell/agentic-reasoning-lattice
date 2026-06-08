# Channel Assignment — ASN-0100 review-136

**Date:** 2026-06-08 01:34

## Issue 1: Duplicated worked-example skeleton (empty-document vs. re-insertion)
Reason: Pure editorial collapse — both examples already exist in the ASN and the delta (subsequent-emission branch firing, V-index/I-chain decoupling) is fully stated in the ASN's own §Effect One and the re-insertion example itself. No design intent or implementation evidence is needed to trim restated structure.

## Issue 2: Overlapping well-definedness derivations in §Atomicity
Reason: Consolidation of three blocks that re-derive results already proved from the ASN's own K-step preconditions (ASN-0047/0093, all cited in-text). Replacing per-ordering re-derivations with one-line citations is internal to the document — no Nelson or Gregory input required.

## Issue 3: Forward deferral of a structural claim's own sub-case
Reason: The `d' ≠ d` projection-invariance conclusion is already derived downstream in INS.proj via the cross-document frame and LP4; either inlining the one-line conclusion or dropping the sentence is fully derivable from the ASN's existing content.
