# Channel Assignment — ASN-0042 review-104

**Date:** 2026-05-30 03:24

## Issue 1: O7(c) — internal inconsistency between the claim, the proof, and the Formal Contract on *when* conditions (ii)/(iv) are discharged
Reason: Fix is internal — the proof body already establishes that (ii)'s discharge relies on `Π_{Σ'} ∖ Π_Σ = {π'}` (true only at `Σ'`), and reconciling the statement, proof, and Formal Contract requires only aligning the three to that existing reasoning. No design intent or implementation evidence is involved.

## Issue 2: O1a preamble — forward-reference, non-circularity defense, and downstream use-site inventory in a structural slot
Reason: Fix is internal — a pure editorial reduction to a bare proof pointer; the invariant and its proof location already stand on their own within the ASN.

## Issue 3: O3 — proof narration and a duplicated corollary/invariant
Reason: Fix is internal — deleting meta-prose and removing one of two identical inequality statements is editorial deduplication within the ASN.

## Issue 4: O7(c) witness — same non-termination point stated twice
Reason: Fix is internal — deleting one of two redundant sentences asserting the chain is unbounded requires no external input.

## Issue 5: DelegatorAllocatesPrefix — Invariant restates the postcondition
Reason: Fix is internal — the Invariant line is the postcondition rephrased; removing or replacing it is derivable from the ASN's own content.

## Issue 6: Multiple sections defer to "the Delegation section" for the same proofs
Reason: Fix is internal — consolidating the O1a/O1b/T4 reachable-state invariant proofs into a single location and citing by lemma name is a structural reorganization within the ASN.
