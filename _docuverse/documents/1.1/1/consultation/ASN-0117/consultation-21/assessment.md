# Channel Assignment — ASN-0117 review-21

**Date:** 2026-06-09 10:08

## Issue 1: P3 (AddressPermanence) is logically contained in P0 (NonDestruction)
Reason: The fix is internal — it concerns whether one named claim's statement is wholly entailed by another's, which is decidable from the ASN's own definitions (P0's `dom(C') = dom(C)` plus value preservation). No design intent or implementation evidence bears on a redundancy-folding edit.

## Issue 2: P1 (ArrangementContraction) duplicates DEL-REMOVE near-verbatim
Reason: The fix is internal — merging two near-verbatim claims and relocating their shared justification to a single home is a structural editing decision derivable from the ASN's existing text. Neither Nelson's intent nor Gregory's evidence is needed to decide that the two statements coincide.
