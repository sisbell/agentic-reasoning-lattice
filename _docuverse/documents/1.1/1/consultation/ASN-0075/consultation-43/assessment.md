# Channel Assignment — ASN-0075 review-43

**Date:** 2026-06-03 08:05

## Issue 1: The "P4★ is a composite-boundary property, not a per-state invariant" rationale is restated three times in three sections
Reason: Pure deduplication of an already-stated fact; the ASN itself establishes that P4★/P4a are composite-boundary properties and D-BOUND already owns the canonical statement. No design intent or implementation evidence is required to consolidate the redundant restatements.

## Issue 2: D-BOUND's body is a use-site inventory / "why the axiom is needed," not a statement of what the axiom says
Reason: Internal editorial restructuring — trimming the downstream-consumer inventory to the bare axiom statement. The axiom's content and its consuming call sites are already present in the ASN, so the fix is derivable from the ASN alone.
