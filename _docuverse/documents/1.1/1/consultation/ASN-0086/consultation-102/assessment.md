# Channel Assignment — ASN-0086 review-102

**Date:** 2026-05-31 19:53

## Issue 1: P1 mislabeled as an emission-gating precondition; contradicted by the WP analysis
Reason: Internal. The ASN already contains both halves of the contradiction — WP Case 1's necessity argument shows Emit_R produces a Σ' when `a ∉ A_rel^Σ` (only the postcondition fails), while P0's necessity shows non-execution. Reclassifying P1 alongside P2 as postcondition-establishing is derivable from the note's own Nullify definition (`Emit_R` with an arbitrary tumbler span, T12-well-formed by `#a ≥ 1`) and L9 ghost permission already cited; no external intent or implementation evidence is required.

## Issue 2: Frame-condition prose and forward operation-inventory duplicated across sections
Reason: Internal. Pure editorial deduplication — collapse the two frame-condition statements into one and delete the forward operation inventory from the transition-relation section. No design-intent or implementation question is involved.

## Issue 3: Single-tuple scope proved twice
Reason: Internal. Both proofs use the same R0a-antichain derivation already present in the note; choosing one site to carry the proof and having the other cite it is a structural edit derivable from the ASN's own content.
