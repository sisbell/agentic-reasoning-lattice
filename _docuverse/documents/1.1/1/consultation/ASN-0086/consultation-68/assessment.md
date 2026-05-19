# Channel Assignment — ASN-0086 review-68

**Date:** 2026-05-19 15:13

## Issue 1: T_cat^Σ defined but never used as a load-bearing concept
Reason: The fix is a content decision (remove the Definition or articulate a downstream use) derivable from the ASN alone. No design-intent question or implementation evidence is required — T_cat^Σ's role within the note is internal to the note's own structure.

## Issue 2: R6c-Corollary proof citation is incomplete
Reason: The fix is a citation correction within the ASN. The "Broader transition relation ↦" paragraph already establishes the combined frame (L12 + L12a + partition fact); the R6c-Corollary proof just needs to cite that combined result. Fully derivable from the ASN's own content.

## Issue 3: Substrate-conforming layer Definition omits ASN-0093 invariants
Reason: The fix references invariants that ASN-0086 already consumes throughout (e.g., ChainMembershipForOrigin, SubAllocatorAxiom). The complete ASN-0093 invariant catalog is documented in ASN-0093 itself — extending the enumeration or removing it in favor of the general clause is derivable from the foundation ASN that ASN-0086 builds on.

## Issue 4: Worked Sketch does not concretely demonstrate R6b
Reason: Step 3 follows mechanically from existing patterns — K.λ's subsequent-emission rule (already used in Steps 1 and 2), R6b's Justification (already proved), and the audit-slice quantification range (already defined). No new design intent or implementation evidence is needed; the construction is template-driven from the existing Sketch.
