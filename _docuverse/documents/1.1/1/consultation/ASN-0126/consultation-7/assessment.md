# Channel Assignment — ASN-0126 review-7

**Date:** 2026-06-08 21:45

## Issue 1: P2/P3 well-definedness rests on registry well-formedness, which is neither cited in the derivation nor asserted as a commitment
Reason: The fix is internal — the note already defines registry well-formedness (coverage-class-key uniqueness) and identifies it as "the load-bearing condition" for single-valuedness in *Registration entries*. The repair is purely structural: promote that condition to an explicit framework commitment and amend the P2/P3 derivations to cite both P1 (state-independence) and well-formedness (single-valuedness). No design intent or implementation evidence is needed.
