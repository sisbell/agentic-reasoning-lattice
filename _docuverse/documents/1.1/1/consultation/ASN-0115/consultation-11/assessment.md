# Channel Assignment — ASN-0115 review-11

**Date:** 2026-06-05 06:51

## Issue 1: R6 (SilentGapFiltering) has no concrete worked instance for the partial-delivery boundary
Reason: The fix is constructing a worked instance entirely from the ASN's own claims (R1, R3, R5, R6) and the model definitions already present (`act`, `item`, the half-open interval). No design intent or implementation evidence is needed — the prose already cites Gregory's clip behavior and Nelson's exactness; the instance just instantiates them.

## Issue 2: R6 establishes silent filtering but does not explore where gaps can occur
Reason: The sharpening is a mathematical derivation from substrate invariants already cited by the review (D-CTG/D-SEQ in ASN-0036, D-CTG★/D-SEQ★ in ASN-0047), which fix per-subspace contiguity. That every unbound named position is a terminal overrun follows from those axioms — no external channel required.

## Issue 3: No frame statement that RETRIEVEV leaves the state unchanged
Reason: Purity is already implicit in the functional definition `deliver(R, Σ)` (it returns material, not a new state), and the project convention exists internally in ASN-0086 (Observe). Adding the one-line frame statement is a convention-following derivation from the ASN's own content.
