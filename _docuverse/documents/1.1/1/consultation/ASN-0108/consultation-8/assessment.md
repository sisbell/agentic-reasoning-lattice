# Channel Assignment — ASN-0108 review-8

**Date:** 2026-06-05 04:45

## Issue 1: The offset-cursor "weakest precondition" is over-claimed — it is sufficient but not weakest
Reason: The fix is internal — it concerns the logic of weakest preconditions over the ASN's own `After`/`Window` definitions and (M-mut), already established in the note. The reviewer even supplies the corrected condition `j' = j ∨ (j ≥ m' ∧ j' ≥ m')`; no design intent or implementation evidence is required to relabel or restate it.

## Issue 2: W5's concrete walk demonstrates the cut-point clause, not the tail-pair-order clause it is labeled as exercising
Reason: The fix is internal — it turns on W5's own formal decomposition into clause (1) and clause (2), and constructing a walk that isolates clause (2) follows from the enumeration-order semantics already defined (W0, `After`, next-cursor). The reviewer's tail-swap construction is derivable from the note alone; no Nelson or Gregory input is needed.
