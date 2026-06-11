# Channel Assignment — ASN-0111 review-39

**Date:** 2026-06-10 22:54

## Issue 1: Evaluability of the structural screen rests on an undischarged step
Reason: The fix is internal — the missing step (`T4-valid(a) ∧ zeros(a) = 3 ⟹ #E(a) ≥ 1`) is derivable from T4a/T4b/T4c (ASN-0034) and SubspaceI (ASN-0043), all already cited in the ASN; the review even sketches the exact derivation to insert. Neither design intent nor implementation evidence bears on a citation-discipline repair.

## Issue 2: "Only success-branch results are permanent" contradicts RL0's own screen-necessity claim
Reason: The fix is internal — the ASN itself proves screen-conjunct necessity at every reachable state (RL0, via L0b/L1/L0/L1b of ASN-0043), so the permanence of `⊥` at screen-failing addresses follows from material already in the note; the revision is a qualification of RL5's caching advice, splitting screen-failing from screen-passing addresses, with no new fact required from design intent or the implementation.
